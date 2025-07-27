# main.py
# This FastAPI application handles incoming Twilio webhooks for SMS/WhatsApp messages.
# It validates the incoming request, manages sessions for the ADK agent,
# and invokes the root_agent to generate replies.

GOOGLE_CLOUD_PROJECT="ace-beanbag-466817-i6"
GOOGLE_CLOUD_LOCATION="us-central1"
GCS_BUCKET_NAME = "agrimitra-audio-response"
GOOGLE_MODEL_FOR_IMAGE = "gemini-2.5-flash-lite"
GOOGLE_MODEL_FOR_AUDIO = "gemini-2.5-flash-lite"


import os
import requests
from fastapi import FastAPI, HTTPException, Request, Response
from twilio.twiml.messaging_response import MessagingResponse
from twilio.request_validator import RequestValidator
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService, VertexAiSessionService, DatabaseSessionService
from google.genai import types
from google.cloud import texttospeech
from google.cloud import speech_v1p1beta1 as speech # Use v1p1beta1 for better features if needed, or v1
from vertexai.generative_models import GenerativeModel, Part
from google.cloud import storage
import uuid
from pydantic import BaseModel
# Import the root_agent from the agent module.
from agrimitra.agent import root_agent
# from starlette.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError



app = FastAPI(
    title="ADK Agent Twilio Webhook",
    description="Handles Twilio webhooks, manages ADK sessions, and invokes the ADK agent."
)

origins = [
    "https://agri-mitra-ui.web.app",
    "http://localhost:3000",
    "http://localhost:5173",
    "*"
]


# --- Configuration ---
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN',"")


# Initialize Twilio Request Validator
# This validator is crucial for verifying that incoming requests genuinely originate from Twilio.
if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
    validator = RequestValidator(TWILIO_AUTH_TOKEN)
else:
    print("CRITICAL WARNING: TWILIO_ACCOUNT_SID or TWILIO_AUTH_TOKEN not set. Twilio webhook validation will be skipped.")
    validator = None # Disable validation if credentials are missing

# Initialize Google Cloud Speech-to-Text client
speech_client = speech.SpeechClient()

# Text-to-Speech client for generating audio responses
tts_client = texttospeech.TextToSpeechClient()
storage_client = storage.Client()


# session_service = VertexAiSessionService(project=GOOGLE_CLOUD_PROJECT, location=GOOGLE_CLOUD_LOCATION)

session_service = InMemorySessionService()  # Use in-memory sessions for simplicity
user_adk_sessions = {}

# --- Pydantic Model for /query endpoint ---
class QueryInput(BaseModel):
    """Defines the expected request body for the /query endpoint."""
    input: str

async def process_agent_response(event):
    """Process and extract the final text response from agent events."""
    # print(f"Event ID: {event.id}, Author: {event.author}") # For debugging agent events

    final_response = ""
    if event.is_final_response():
        if event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, "text") and part.text and not part.text.isspace():
                    final_response += part.text.strip() + " "
    return final_response.strip()

async def call_agent_async(runner, user_id, session_id, query):
    """Call the agent asynchronously with the user's query and return the final response."""
    content = types.Content(role="user", parts=[types.Part(text=query)])
    final_response_text = ""

    try:
        async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content
        ):
            response_part = await process_agent_response(event)
            if response_part:
                final_response_text += response_part + " " # Accumulate parts if agent sends multiple final_response events
    except Exception as e:
        print(f"ERROR during agent run for user {user_id}, session {session_id}: {e}")
        final_response_text = f"An error occurred while processing your request. Please try again later. Error: {str(e)}"

    return final_response_text.strip()

async def transcribe_audio_with_gemini(audio_url: str, mime_type: str) -> str:
    """
    Downloads an audio file and transcribes it using the Vertex AI Gemini 1.5 Pro model.
    """
    print(f"Attempting to transcribe audio from: {audio_url} with mime_type: {mime_type}")
    try:
        # 1. Download audio with authentication
        response = requests.get(audio_url, auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN))
        response.raise_for_status()
        audio_content = response.content

        # 2. Prepare for Vertex AI Gemini
        audio_part = Part.from_data(data=audio_content, mime_type=mime_type)
        model = GenerativeModel(GOOGLE_MODEL_FOR_AUDIO) # Using a powerful multimodal model

        # 3. Perform transcription
        print("Transcribing with Vertex AI Gemini...")
        transcription_response = await model.generate_content_async([audio_part, "Transcribe this audio."])

        transcribed_text = transcription_response.text.strip()
        print(f"Transcribed text: '{transcribed_text}'")
        return transcribed_text

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error downloading audio from {audio_url}: {e}")
        raise HTTPException(status_code=500, detail="Failed to download audio for transcription.")
    except Exception as e:
        print(f"Error during audio transcription with Gemini: {e}")
        raise HTTPException(status_code=500, detail="Failed to transcribe audio.")

async def text_to_speech_and_upload(text: str) -> str:
    """
    Converts text to an OGG/Opus audio file, uploads it to GCS, and returns the public URL.
    This format is required for WhatsApp to render it as a playable voice note.
    """
    try:
        print(f"Generating OGG/Opus audio for text: '{text[:50]}...'")
        # 1. Synthesize Speech
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        # UPDATED: Changed audio encoding to OGG_OPUS for native playback in WhatsApp
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.OGG_OPUS
        )
        tts_response = tts_client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # 2. Upload to Google Cloud Storage
        bucket = storage_client.bucket(GCS_BUCKET_NAME)
        # UPDATED: Changed file extension and content type to .ogg
        blob_name = f"audio-responses/{uuid.uuid4()}.ogg"
        blob = bucket.blob(blob_name)
        
        print(f"Uploading audio to GCS bucket '{GCS_BUCKET_NAME}' as '{blob_name}'")
        blob.upload_from_string(tts_response.audio_content, content_type="audio/ogg")
        
        print("Audio uploaded successfully.")
        return blob.public_url
        
    except Exception as e:
        print(f"Error during Text-to-Speech or GCS upload: {e}")
        raise  # Re-raise the exception to be handled by the caller

async def describe_image_with_gemini(image_url: str, mime_type: str) -> str:
    """
    Downloads an image file and generates a description using the Vertex AI Gemini 1.5 Pro model.
    """
    print(f"Attempting to describe image from: {image_url} with mime_type: {mime_type}")
    try:
        response = requests.get(image_url, auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN))
        response.raise_for_status()
        image_content = response.content

        image_part = Part.from_data(data=image_content, mime_type=mime_type)
        model = GenerativeModel(GOOGLE_MODEL_FOR_IMAGE)

        print("Describing image with Vertex AI Gemini...")
        prompt = """Analyze the following image from an agricultural perspective. Describe what you see in detail. If it's a plant, identify it if possible and comment on its apparent health, noting any visible signs of disease, pests, or nutrient deficiencies. If it's a picture of soil or a field, describe that. Provide a detailed textual description that can be used by an agricultural assistant to provide advice."""
        description_response = await model.generate_content_async([image_part, prompt])

        description_text = description_response.text.strip()
        print(f"Image description: '{description_text}'")
        return description_text

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error downloading image from {image_url}: {e}")
        raise HTTPException(status_code=500, detail="Failed to download image for analysis.")
    except Exception as e:
        print(f"Error during image description with Gemini: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze image.")



# --- Twilio Webhook Endpoint ---
@app.post("/sms")
async def twilio_webhook(request: Request):
    """
    Handles incoming Twilio messages, transcribes audio, invokes the agent,
    and replies with text or a generated playable audio file.
    """
    form_data = await request.form()
    sender_number = form_data.get('From', '').strip()
    is_audio_input = False
    
    # --- Input Processing ---
    agent_input_text = form_data.get('Body', '').strip()
    media_url = form_data.get('MediaUrl0', '').strip()
    media_content_type = form_data.get('MediaContentType0', '').strip()
    
    if media_url:
        if media_content_type.startswith('audio/'):
            is_audio_input = True
            try:
                agent_input_text = await transcribe_audio_with_gemini(media_url, media_content_type)
                if not agent_input_text:
                    agent_input_text = "(No speech detected in audio)"
            except HTTPException as e:
                resp = MessagingResponse()
                resp.message(f"Sorry, I had trouble processing your audio: {e.detail}")
                return Response(content=str(resp), media_type="text/xml")
        else:
            agent_input_text = await describe_image_with_gemini(media_url, media_content_type)
            if not agent_input_text:
                agent_input_text = "(Could not describe the image)"

    if not agent_input_text:
        resp = MessagingResponse().message("Please send a text or voice message.")
        return Response(content=str(resp), media_type="text/xml")

    # --- Session Management ---
    current_session_id = user_adk_sessions.get(sender_number)
    
    # -----Delete old sessions if they ask with create-new-session-----
    if agent_input_text.lower() == "create new session":
        if current_session_id:
            try:
                await session_service.delete_session(current_session_id)
                print(f"Deleted old session for {sender_number}: {current_session_id}")
            except Exception as e:
                print(f"ERROR deleting old session: {e}")
        current_session_id = None
        user_adk_sessions[sender_number] = None
    
    # --- Create a new session if none exists ---
    if not current_session_id:
        try:
            session_name = f"/projects/{GOOGLE_CLOUD_PROJECT}/locations/{GOOGLE_CLOUD_LOCATION}/sessions/{uuid.uuid4()} "
            new_session = await session_service.create_session(app_name="agrimitra", user_id=sender_number)
            current_session_id = new_session.id
            user_adk_sessions[sender_number] = current_session_id
            print(f"Created new ADK session for {sender_number}: {current_session_id}")
        except Exception as e:
            print(f"ERROR creating ADK session: {e}")
            resp = MessagingResponse().message("Sorry, I couldn't start a new conversation right now.")
            return Response(content=str(resp), media_type="text/xml")

    # --- Invoke Agent ---
    runner = Runner(agent=root_agent, app_name="agrimitra", session_service=session_service)
    agent_response_text = await call_agent_async(
        runner, sender_number, current_session_id, agent_input_text
    )

    # --- Create Response (Text or Audio) ---
    resp = MessagingResponse()
    if is_audio_input:
        try:
            # If input was audio, respond with a playable voice note and the text transcript.
            # audio_response_url = await text_to_speech_and_upload(agent_response_text)
            
            # UPDATED: Send the audio file in one message and the text in a second message.
            # This ensures the audio is rendered as a playable voice note.
            # Note: Twilio sends these as two separate, sequential messages.
            # resp.message().media(audio_response_url)
            # print(f"Audio response URL: {audio_response_url} sent successfully.")
            # print(f"Sending as text message due to time.")
            resp.message(agent_response_text)

        except Exception as e:
            # Fallback to text if TTS fails
            print(f"CRITICAL: TTS process failed. Falling back to text-only response. Error: {e}")
            resp.message(agent_response_text)
    else:
        # If input was text, respond with text
        print(f"Text response: {agent_response_text}. Sending as text message.")
        resp.message(agent_response_text)
        print("Text response sent successfully.")

    return Response(content=str(resp), media_type="text/xml")

# --- General Query Endpoint (NEW) ---
@app.exception_handler(RequestValidationError)
@app.post("/query")
async def handle_query(query: QueryInput):
    """
    Handles a single, stateless query to the agent via a JSON API.
    Creates a temporary session for each request.
    """
    user_id = "api_user"  # A generic user ID for API requests
    session_id = None
    try:
        # Create a new, temporary session for each API call to ensure statelessness
        new_session = await session_service.create_session(app_name="agrimitra", user_id=user_id)
        session_id = new_session.id
        print(f"Created temporary ADK session for API query: {session_id}")

        # Invoke the agent with the user's input
        runner = Runner(agent=root_agent, app_name="agrimitra", session_service=session_service)
        agent_response_text = await call_agent_async(
            runner, user_id, session_id, query.input
        )

        # Check if the agent itself returned an error message
        if "An error occurred" in agent_response_text:
            raise HTTPException(status_code=500, detail=agent_response_text)

        return {"output": agent_response_text}

    except Exception as e:
        print(f"Error in /query endpoint: {e}")
        # Ensure we don't re-wrap FastAPI's own exceptions
        if isinstance(e, HTTPException):
            raise
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {str(e)}")

    finally:
        # Clean up the session after the request is complete
        if session_id:
            try:
                await session_service.delete_session(session_id)
                print(f"Deleted temporary ADK session: {session_id}")
            except Exception as e:
                # Log the error but don't fail the request if deletion fails
                print(f"WARNING: Failed to delete temporary session {session_id}: {e}")


# --- Health Check Endpoint ---
@app.get("/health")
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok", "message": "ADK Agent Twilio Webhook is running."}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow all origins for simplicity, adjust as needed
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"],  # Expose all headers to the client
)

print(f"Following App Middleware is added: {app.user_middleware}")