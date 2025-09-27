import { NavLink } from "react-router-dom";
import { Compass, Tag, MessageSquare } from "lucide-react";
import { cn } from "@/lib/utils";

const menuItems = [
  {
    title: "Nghiệp vụ",
    path: "/use-cases",
    icon: Compass,
    description: "Use Cases",
  },
  {
    title: "Thư viện Biến", 
    path: "/variables",
    icon: Tag,
    description: "Variables",
  },
  {
    title: "Mẫu trả lời",
    path: "/templates", 
    icon: MessageSquare,
    description: "Templates",
  },
];

export function Sidebar() {
  return (
    <aside className="w-64 bg-sidebar border-r border-sidebar-border">
      <nav className="p-4">
        <ul className="space-y-2">
          {menuItems.map((item) => {
            const IconComponent = item.icon;
            return (
              <li key={item.path}>
                <NavLink
                  to={item.path}
                  className={({ isActive }) =>
                    cn(
                      "flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors",
                      "hover:bg-sidebar-accent hover:text-sidebar-accent-foreground",
                      isActive
                        ? "bg-sidebar-primary text-sidebar-primary-foreground"
                        : "text-sidebar-foreground"
                    )
                  }
                >
                  <IconComponent className="mr-3 h-5 w-5 flex-shrink-0" />
                  <span>{item.title}</span>
                </NavLink>
              </li>
            );
          })}
        </ul>
      </nav>
    </aside>
  );
}