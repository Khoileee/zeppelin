import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { User, LogOut } from "lucide-react";

export function Header() {
  return (
    <header className="h-16 bg-card border-b border-border px-6 flex items-center justify-between">
      {/* Logo */}
      <div className="flex items-center">
        <h1 className="text-xl font-bold text-foreground">SQLWF</h1>
      </div>

      {/* User Menu */}
      <DropdownMenu>
        <DropdownMenuTrigger className="flex items-center space-x-3 hover:bg-muted rounded-lg p-2 transition-colors">
          <span className="text-sm font-medium text-foreground">Khôi Lê</span>
          <Avatar className="h-8 w-8">
            <AvatarImage src="/placeholder.svg" alt="Khôi Lê" />
            <AvatarFallback className="bg-primary text-primary-foreground text-sm">KL</AvatarFallback>
          </Avatar>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end" className="w-48">
          <DropdownMenuItem className="cursor-pointer">
            <User className="mr-2 h-4 w-4" />
            Thông tin tài khoản
          </DropdownMenuItem>
          <DropdownMenuSeparator />
          <DropdownMenuItem className="cursor-pointer text-destructive focus:text-destructive">
            <LogOut className="mr-2 h-4 w-4" />
            Đăng xuất
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </header>
  );
}