import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { MainLayout } from "./components/layout/MainLayout";
import UseCases from "./pages/UseCases";
import Variables from "./pages/Variables";
import Templates from "./pages/Templates";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<MainLayout />}>
            <Route index element={<Navigate to="/use-cases" replace />} />
            <Route path="/use-cases" element={<UseCases />} />
            <Route path="/variables" element={<Variables />} />
            <Route path="/templates" element={<Templates />} />
          </Route>
          {/* Catch all other routes */}
          <Route path="*" element={<Navigate to="/use-cases" replace />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
