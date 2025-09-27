import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

interface Variable {
  id: string;
  displayName: string;
  placeholder: string;
  dataType: "text" | "number" | "currency" | "datetime" | "boolean";
  maskingRule: "none" | "full" | "middle" | "last4" | "first6";
}

interface VariableDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  variable?: Variable | null;
}

const dataTypeOptions = [
  { value: "text", label: "Text" },
  { value: "number", label: "Number" },
  { value: "currency", label: "Currency (Tiền tệ)" },
  { value: "datetime", label: "Datetime (Ngày giờ)" },
  { value: "boolean", label: "Boolean (Đúng/Sai)" },
];

const maskingRuleOptions = [
  { value: "none", label: "Không che" },
  { value: "full", label: "Che toàn bộ (Ví dụ: ********)" },
  { value: "middle", label: "Che phần giữa (Ví dụ: 090****567)" },
  { value: "last4", label: "Che 4 số cuối (Ví dụ: ****1234)" },
  { value: "first6", label: "Che 6 số đầu (Ví dụ: 123456******)" },
];

export function VariableDialog({ open, onOpenChange, variable }: VariableDialogProps) {
  const [formData, setFormData] = useState({
    displayName: variable?.displayName || "",
    placeholder: variable?.placeholder || "",
    dataType: variable?.dataType || "text",
    maskingRule: variable?.maskingRule || "none",
  });

  // Auto-generate placeholder from display name
  const generatePlaceholder = (displayName: string) => {
    const snake_case = displayName
      .toLowerCase()
      .replace(/\s+/g, "_")
      .replace(/[^a-z0-9_]/g, "");
    return `<${snake_case}>`;
  };

  const handleDisplayNameChange = (value: string) => {
    setFormData({
      ...formData,
      displayName: value,
      placeholder: value ? generatePlaceholder(value) : "",
    });
  };

  const isValid = formData.displayName.trim() !== "" && formData.placeholder.trim() !== "";

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-lg">
        <DialogHeader>
          <DialogTitle>
            {variable ? `Chỉnh sửa Biến: ${variable.displayName}` : "Tạo Biến mới"}
          </DialogTitle>
        </DialogHeader>

        <div className="space-y-4">
          {/* Tên hiển thị */}
          <div>
            <Label htmlFor="displayName">
              Tên hiển thị <span className="text-destructive">*</span>
            </Label>
            <Input
              id="displayName"
              value={formData.displayName}
              onChange={(e) => handleDisplayNameChange(e.target.value)}
              placeholder="Ví dụ: Số tiền giao dịch"
              className="mt-1"
            />
          </div>

          {/* Placeholder */}
          <div>
            <Label htmlFor="placeholder">
              Placeholder <span className="text-destructive">*</span>
            </Label>
            <Input
              id="placeholder"
              value={formData.placeholder}
              onChange={(e) => setFormData({ ...formData, placeholder: e.target.value })}
              className="mt-1"
            />
            <p className="text-xs text-muted-foreground mt-1">
              Dùng để chèn vào Mẫu trả lời. Không chứa dấu cách, ký tự đặc biệt.
            </p>
          </div>

          {/* Kiểu dữ liệu */}
          <div>
            <Label>
              Kiểu dữ liệu <span className="text-destructive">*</span>
            </Label>
            <Select
              value={formData.dataType}
              onValueChange={(value) => setFormData({ ...formData, dataType: value as any })}
            >
              <SelectTrigger className="mt-1">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {dataTypeOptions.map((option) => (
                  <SelectItem key={option.value} value={option.value}>
                    {option.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Quy tắc Masking */}
          <div>
            <Label>
              Quy tắc Masking <span className="text-destructive">*</span>
            </Label>
            <Select
              value={formData.maskingRule}
              onValueChange={(value) => setFormData({ ...formData, maskingRule: value as any })}
            >
              <SelectTrigger className="mt-1">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {maskingRuleOptions.map((option) => (
                  <SelectItem key={option.value} value={option.value}>
                    {option.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            Hủy
          </Button>
          <Button
            className="bg-primary hover:bg-primary-hover"
            disabled={!isValid}
          >
            Lưu Biến
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}