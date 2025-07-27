import Header from "@/components/Header";
import Dashboard from "@/components/Dashboard";
import ChatInterface from "@/components/ChatInterface";

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <Dashboard />
      <ChatInterface />
    </div>
  );
};

export default Index;
