import { useState } from "react";
import { MessageCircle, Send, X, Mic } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { ScrollArea } from "@/components/ui/scroll-area";

interface Message {
  id: number;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
}

const ChatInterface = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      text: "नमस्ते! मैं AgriMitra हूं। मैं आपकी खेती में कैसे मदद कर सकता हूं?",
      sender: 'bot',
      timestamp: new Date()
    }
  ]);
  const [inputMessage, setInputMessage] = useState("");
  const [isOpen, setIsOpen] = useState(false);

  const sendMessage = () => {
    if (!inputMessage.trim()) return;

    const userMessage: Message = {
      id: messages.length + 1,
      text: inputMessage,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage("");

    // Simulate AI response
    setTimeout(() => {
      const botResponse: Message = {
        id: messages.length + 2,
        text: getAIResponse(inputMessage),
        sender: 'bot',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, botResponse]);
    }, 1000);
  };

  const getAIResponse = (userInput: string): string => {
    const responses = [
      "मैं आपकी फसल की समस्या को समझ रहा हूं। आपकी मिट्टी का pH स्तर जांचना जरूरी है।",
      "मौसम के अनुसार, आज सिंचाई न करें। कल बारिश की संभावना है।",
      "आपकी गेहूं की फसल के लिए यूरिया खाद की मात्रा 50 किलो प्रति एकड़ उपयुक्त है।",
      "कीट प्रबंधन के लिए नीम का तेल का छिड़काव करें। यह प्राकृतिक और सुरक्षित है।",
      "किसान क्रेडिट कार्ड के लिए आप नजदीकी बैंक में जाकर आवेदन कर सकते हैं।"
    ];
    return responses[Math.floor(Math.random() * responses.length)];
  };

  return (
    <>
      {/* Floating Chat Button */}
      <Sheet open={isOpen} onOpenChange={setIsOpen}>
        <SheetTrigger asChild>
          <Button
            className="fixed bottom-6 right-6 h-14 w-14 rounded-full shadow-lg bg-primary hover:bg-primary/90 z-50"
            size="icon"
          >
            <MessageCircle className="h-6 w-6 text-primary-foreground" />
          </Button>
        </SheetTrigger>

        <SheetContent side="bottom" className="h-[80vh] bg-card p-0">
          <div className="flex flex-col h-full">
            <SheetHeader className="px-4 py-3 border-b border-border">
              <div className="flex items-center justify-between">
                <SheetTitle className="text-primary">
                  Chat with AgriMitra
                </SheetTitle>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setIsOpen(false)}
                  className="h-8 w-8 p-0"
                >
                  <X className="h-4 w-4" />
                </Button>
              </div>
            </SheetHeader>

            {/* Chat Messages */}
            <ScrollArea className="flex-1 px-4 py-2">
              <div className="space-y-3">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex ${
                      message.sender === 'user' ? 'justify-end' : 'justify-start'
                    }`}
                  >
                    <div
                      className={`max-w-[80%] p-3 rounded-lg ${
                        message.sender === 'user'
                          ? 'bg-primary text-primary-foreground'
                          : 'bg-muted text-foreground'
                      }`}
                    >
                      <p className="text-sm">{message.text}</p>
                      <span className="text-xs opacity-70 mt-1 block">
                        {message.timestamp.toLocaleTimeString('en-IN', {
                          hour: '2-digit',
                          minute: '2-digit'
                        })}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </ScrollArea>

            {/* Input Area */}
            <div className="p-4 border-t border-border bg-card">
              <div className="flex items-center space-x-2">
                <div className="flex-1 relative">
                  <Input
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    placeholder="अपना सवाल पूछें... (Ask your question...)"
                    className="pr-10 bg-background border-border"
                    onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                  />
                  <Button
                    variant="ghost"
                    size="sm"
                    className="absolute right-1 top-1/2 -translate-y-1/2 h-8 w-8 p-0"
                  >
                    <Mic className="h-4 w-4 text-muted-foreground" />
                  </Button>
                </div>
                <Button
                  onClick={sendMessage}
                  className="h-10 w-10 bg-primary hover:bg-primary/90"
                  size="icon"
                >
                  <Send className="h-4 w-4 text-primary-foreground" />
                </Button>
              </div>
            </div>
          </div>
        </SheetContent>
      </Sheet>
    </>
  );
};

export default ChatInterface;