import { Bell, Globe, User, ChevronDown } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { Badge } from "@/components/ui/badge";

const Header = () => {
  const notifications = [
    {
      id: 1,
      title: "Weather Alert",
      message: "Heavy rainfall expected in your area tomorrow",
      time: "2 hours ago",
      type: "warning"
    },
    {
      id: 2,
      title: "Loan Reminder",
      message: "Your loan payment is due in 3 days",
      time: "5 hours ago",
      type: "info"
    },
    {
      id: 3,
      title: "Crop Advisory",
      message: "Best time to apply fertilizer for wheat crop",
      time: "1 day ago",
      type: "success"
    }
  ];

  return (
    <header className="bg-card border-b border-border shadow-sm">
      <div className="flex items-center justify-between px-4 py-3">
        {/* Logo */}
        <div className="flex items-center space-x-3">
          <img 
            src="/lovable-uploads/34c7665e-e910-427d-8446-19df044069bc.png" 
            alt="AgriMitra Logo" 
            className="h-10 w-10"
          />
          <h1 className="text-xl font-bold text-primary">AgriMitra</h1>
        </div>

        {/* Right side controls */}
        <div className="flex items-center space-x-2">
          {/* Language Switcher */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="sm" className="h-9 px-2">
                <Globe className="h-4 w-4 mr-1" />
                <span className="text-sm">EN</span>
                <ChevronDown className="h-3 w-3 ml-1" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="bg-popover border border-border">
              <DropdownMenuItem className="hover:bg-accent">
                English
              </DropdownMenuItem>
              <DropdownMenuItem className="hover:bg-accent">
                हिंदी (Hindi)
              </DropdownMenuItem>
              <DropdownMenuItem className="hover:bg-accent">
                ಕನ್ನಡ (Kannada)
              </DropdownMenuItem>
              <DropdownMenuItem className="hover:bg-accent">
                तमिळ (Tamil)
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>

          {/* Notifications */}
          <Sheet>
            <SheetTrigger asChild>
              <Button variant="ghost" size="sm" className="h-9 w-9 p-0 relative">
                <Bell className="h-4 w-4" />
                <Badge className="absolute -top-1 -right-1 h-5 w-5 p-0 flex items-center justify-center text-xs bg-warning text-warning-foreground">
                  {notifications.length}
                </Badge>
              </Button>
            </SheetTrigger>
            <SheetContent className="bg-card w-80">
              <SheetHeader>
                <SheetTitle className="text-primary">Notifications</SheetTitle>
              </SheetHeader>
              <div className="mt-4 space-y-3">
                {notifications.map((notification) => (
                  <div
                    key={notification.id}
                    className="p-3 rounded-lg border border-border bg-muted/50 hover:bg-muted transition-colors"
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <h4 className="font-medium text-sm text-foreground">
                          {notification.title}
                        </h4>
                        <p className="text-xs text-muted-foreground mt-1">
                          {notification.message}
                        </p>
                        <span className="text-xs text-muted-foreground">
                          {notification.time}
                        </span>
                      </div>
                      <Badge 
                        variant="secondary" 
                        className={`text-xs ml-2 ${
                          notification.type === 'warning' ? 'bg-warning text-warning-foreground' :
                          notification.type === 'success' ? 'bg-success text-success-foreground' :
                          'bg-secondary text-secondary-foreground'
                        }`}
                      >
                        {notification.type}
                      </Badge>
                    </div>
                  </div>
                ))}
              </div>
            </SheetContent>
          </Sheet>

          {/* User Profile */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="sm" className="h-9 px-2">
                <User className="h-4 w-4 mr-1" />
                <span className="text-sm hidden sm:inline">Profile</span>
                <ChevronDown className="h-3 w-3 ml-1" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="bg-popover border border-border">
              <DropdownMenuItem className="hover:bg-accent">
                My Profile
              </DropdownMenuItem>
              <DropdownMenuItem className="hover:bg-accent">
                Settings
              </DropdownMenuItem>
              <DropdownMenuItem className="hover:bg-accent">
                Help & Support
              </DropdownMenuItem>
              <DropdownMenuItem className="hover:bg-accent">
                Sign Out
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
    </header>
  );
};

export default Header;