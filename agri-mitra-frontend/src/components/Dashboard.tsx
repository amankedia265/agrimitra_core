import { 
  MessageCircle, 
  MapPin, 
  Cloud, 
  CreditCard, 
  Sprout,
  TrendingUp,
  Calendar,
  Phone
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

const Dashboard = () => {
  const quickAccessCards = [
    {
      title: "Ask a Question",
      description: "Get instant help from AgriMitra AI",
      icon: MessageCircle,
      color: "bg-accent",
      action: "chat"
    },
    {
      title: "My Farm Info",
      description: "View and manage your farm details",
      icon: MapPin,
      color: "bg-secondary",
      action: "farm"
    },
    {
      title: "Weather Today",
      description: "Current weather and 7-day forecast",
      icon: Cloud,
      color: "bg-muted",
      action: "weather"
    },
    {
      title: "Credit Support",
      description: "Loans, schemes, and financial help",
      icon: CreditCard,
      color: "bg-warning/30",
      action: "credit"
    }
  ];

  const additionalFeatures = [
    {
      title: "Crop Calendar",
      description: "Track your crop cycles",
      icon: Calendar,
      color: "bg-success/20"
    },
    {
      title: "Market Prices",
      description: "Live commodity rates",
      icon: TrendingUp,
      color: "bg-accent/20"
    },
    {
      title: "Expert Helpline",
      description: "Talk to agriculture experts",
      icon: Phone,
      color: "bg-primary/10"
    },
    {
      title: "Disease Detection",
      description: "AI-powered crop diagnosis",
      icon: Sprout,
      color: "bg-secondary/30"
    }
  ];

  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <div className="bg-gradient-to-br from-primary/5 to-accent/10 px-4 py-8">
        <div className="max-w-md mx-auto text-center">
          <h2 className="text-2xl font-bold text-primary mb-2">
            Welcome to AgriMitra
          </h2>
          <p className="text-muted-foreground">
            Your intelligent farming companion
          </p>
        </div>
      </div>

      {/* Quick Access Cards */}
      <div className="px-4 -mt-4">
        <div className="max-w-md mx-auto">
          <h3 className="text-lg font-semibold text-foreground mb-4">
            Quick Access
          </h3>
          <div className="grid grid-cols-2 gap-3 mb-6">
            {quickAccessCards.map((card, index) => (
              <Card 
                key={index}
                className="border border-border hover:shadow-md transition-all duration-200 cursor-pointer active:scale-95"
              >
                <CardContent className="p-4">
                  <div className={`${card.color} w-12 h-12 rounded-full flex items-center justify-center mb-3`}>
                    <card.icon className="h-6 w-6 text-foreground" />
                  </div>
                  <h4 className="font-medium text-sm text-foreground mb-1">
                    {card.title}
                  </h4>
                  <p className="text-xs text-muted-foreground leading-relaxed">
                    {card.description}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Additional Features */}
          <h3 className="text-lg font-semibold text-foreground mb-4">
            More Features
          </h3>
          <div className="grid grid-cols-1 gap-3 pb-20">
            {additionalFeatures.map((feature, index) => (
              <Card 
                key={index}
                className="border border-border hover:shadow-md transition-all duration-200 cursor-pointer active:scale-[0.98]"
              >
                <CardContent className="p-4">
                  <div className="flex items-center space-x-3">
                    <div className={`${feature.color} w-10 h-10 rounded-full flex items-center justify-center`}>
                      <feature.icon className="h-5 w-5 text-foreground" />
                    </div>
                    <div className="flex-1">
                      <h4 className="font-medium text-sm text-foreground">
                        {feature.title}
                      </h4>
                      <p className="text-xs text-muted-foreground">
                        {feature.description}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;