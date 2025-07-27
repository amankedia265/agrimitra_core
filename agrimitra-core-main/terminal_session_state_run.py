import asyncio

from agrimitra.agent import agrimitra_agent
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from utils2 import add_user_query_to_history, call_agent_async

load_dotenv()



# Create a new session service to store state
session_service = InMemorySessionService()

initial_state = {
    "user_name": "Aditya Jha",
    "user_preferences": """
    I have a millet feild in karnataka,
    "interaction history":[]
    """,
}
async def main_async():
    # Setup constants
    APP_NAME = "agrimitra"
    USER_ID = "agrimitra-aditya"

    # ===== PART 3: Session Creation =====
    # Create a new session with initial state
    new_session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state=initial_state,
    )

    SESSION_ID = new_session.id
    print(f"Created new session: {SESSION_ID}")

    runner = Runner(
        agent=agrimitra_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
    print("\nWelcome to Agrimitra!")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    while True:
        # Get user input
        user_input = input("You: ")

        # Check if user wants to exit
        if user_input.lower() in ["exit", "quit"]:
            print("Ending conversation. Goodbye!")
            break

        # Update interaction history with the user's query
        await add_user_query_to_history(session_service, APP_NAME, USER_ID, SESSION_ID, user_input)

        # Process the user query through the agent
        await call_agent_async(runner, USER_ID, SESSION_ID, user_input)


def main():
    """Entry point for the application."""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()