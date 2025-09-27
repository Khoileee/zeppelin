import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
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
import { Badge } from "@/components/ui/badge";
import { Plus, Trash2, X } from "lucide-react";

interface Template {
  id: string;
  name: string;
  useCases: string[];
  conditions: string;
  updatedAt: string;
}

interface TemplateDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  template?: Template | null;
}

interface Condition {
  id: string;
  field: string;
  operator: string;
  value: string;
}

const mockUseCases = [
  { id: "1", name: "Tra cứu chuyển tiền" },
  { id: "2", name: "Kiểm tra số dư" },
  { id: "3", name: "Đối soát giao dịch" },
  { id: "4", name: "Tra cứu lịch sử" },
];

const mockFields = [
  { value: "flags.has_error", label: "flags.has_error" },
  { value: "flags.record_found", label: "flags.record_found" },
  { value: "<ma_loi>", label: "<mã lỗi>" },
  { value: "<trang_thai_giao_dich>", label: "<trạng thái giao dịch>" },
  { value: "<so_tien_giao_dich>", label: "<số tiền giao dịch>" },
];

const operators = [
  { value: "==", label: "bằng (==)" },
  { value: "!=", label: "không bằng (!=)" },
  { value: "contains", label: "chứa (contains)" },
  { value: ">", label: "lớn hơn (>)" },
  { value: "<", label: "nhỏ hơn (<)" },
];

const mockPlaceholders = [
  "<so_thue_bao>",
  "<so_tien_giao_dich>", 
  "<thoi_gian_giao_dich>",
  "<ma_giao_dich>",
  "<trang_thai_giao_dich>",
];

export function TemplateDialog({ open, onOpenChange, template }: TemplateDialogProps) {
  const [formData, setFormData] = useState({
    name: template?.name || "",
    selectedUseCases: template?.useCases || [],
    content: "",
  });

  const [conditions, setConditions] = useState<Condition[]>([]);

  const addCondition = () => {
    const newCondition: Condition = {
      id: Date.now().toString(),
      field: "",
      operator: "==",
      value: "",
    };
    setConditions([...conditions, newCondition]);
  };

  const removeCondition = (id: string) => {
    setConditions(conditions.filter((condition) => condition.id !== id));
  };

  const updateCondition = (id: string, field: keyof Condition, value: string) => {
    setConditions(conditions.map((condition) =>
      condition.id === id ? { ...condition, [field]: value } : condition
    ));
  };

  const addUseCase = (useCaseId: string) => {
    const useCase = mockUseCases.find(uc => uc.id === useCaseId);
    if (useCase && !formData.selectedUseCases.includes(useCase.name)) {
      setFormData({
        ...formData,
        selectedUseCases: [...formData.selectedUseCases, useCase.name]
      });
    }
  };

  const removeUseCase = (useCaseName: string) => {
    setFormData({
      ...formData,
      selectedUseCases: formData.selectedUseCases.filter(name => name !== useCaseName)
    });
  };

  const insertPlaceholder = (placeholder: string) => {
    const textarea = document.getElementById('content') as HTMLTextAreaElement;
    if (textarea) {
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const text = formData.content;
      const before = text.substring(0, start);
      const after = text.substring(end, text.length);
      
      setFormData({
        ...formData,
        content: before + placeholder + after
      });
      
      // Set cursor position after inserted placeholder
      setTimeout(() => {
        textarea.selectionStart = textarea.selectionEnd = start + placeholder.length;
        textarea.focus();
      }, 0);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>
            {template ? "Chỉnh sửa Mẫu trả lời" : "Tạo Mẫu trả lời mới"}
          </DialogTitle>
        </DialogHeader>

        <div className="space-y-6">
          {/* Phần 1: Thông tin cơ bản */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Thông tin cơ bản</h3>
            
            <div className="space-y-4">
              <div>
                <Label htmlFor="name">
                  Tên mẫu trả lời <span className="text-destructive">*</span>
                </Label>
                <Input
                  id="name"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  placeholder="Hướng dẫn xử lý lỗi không đủ số dư"
                />
              </div>

              <div>
                <Label>
                  Áp dụng cho nghiệp vụ <span className="text-destructive">*</span>
                </Label>
                <div className="mt-2">
                  <Select onValueChange={addUseCase}>
                    <SelectTrigger>
                      <SelectValue placeholder="Chọn nghiệp vụ để thêm" />
                    </SelectTrigger>
                    <SelectContent>
                      {mockUseCases
                        .filter(uc => !formData.selectedUseCases.includes(uc.name))
                        .map((useCase) => (
                        <SelectItem key={useCase.id} value={useCase.id}>
                          {useCase.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  
                  {formData.selectedUseCases.length > 0 && (
                    <div className="flex flex-wrap gap-2 mt-2">
                      {formData.selectedUseCases.map((useCaseName) => (
                        <Badge
                          key={useCaseName}
                          variant="secondary"
                          className="bg-accent text-accent-foreground"
                        >
                          {useCaseName}
                          <Button
                            type="button"
                            variant="ghost"
                            size="sm"
                            className="ml-1 h-auto p-0 text-accent-foreground hover:bg-transparent"
                            onClick={() => removeUseCase(useCaseName)}
                          >
                            <X className="h-3 w-3" />
                          </Button>
                        </Badge>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* Phần 2: Thiết lập Điều kiện kích hoạt */}
          <div>
            <h3 className="text-lg font-semibold mb-2">Thiết lập Điều kiện kích hoạt</h3>
            <p className="text-sm text-muted-foreground mb-4">
              Mẫu này sẽ được sử dụng KHI tất cả các điều kiện dưới đây đều đúng.
            </p>
            
            <Button
              type="button"
              variant="outline"
              onClick={addCondition}
              className="mb-4"
            >
              <Plus className="mr-2 h-4 w-4" />
              Thêm điều kiện
            </Button>

            <div className="space-y-3">
              {conditions.map((condition) => (
                <div key={condition.id} className="flex items-center space-x-3 p-3 border rounded-lg">
                  <Select
                    value={condition.field}
                    onValueChange={(value) => updateCondition(condition.id, "field", value)}
                  >
                    <SelectTrigger className="w-64">
                      <SelectValue placeholder="Trường dữ liệu" />
                    </SelectTrigger>
                    <SelectContent>
                      {mockFields.map((field) => (
                        <SelectItem key={field.value} value={field.value}>
                          {field.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>

                  <Select
                    value={condition.operator}
                    onValueChange={(value) => updateCondition(condition.id, "operator", value)}
                  >
                    <SelectTrigger className="w-40">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {operators.map((op) => (
                        <SelectItem key={op.value} value={op.value}>
                          {op.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>

                  <Input
                    placeholder="Giá trị so sánh"
                    value={condition.value}
                    onChange={(e) => updateCondition(condition.id, "value", e.target.value)}
                    className="flex-1"
                  />

                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    onClick={() => removeCondition(condition.id)}
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              ))}
            </div>
          </div>

          {/* Phần 3: Nội dung trả lời */}
          <div>
            <h3 className="text-lg font-semibold mb-2">Nội dung trả lời (THÌ)</h3>
            
            <div className="grid grid-cols-3 gap-4">
              <div className="col-span-2">
                <Label htmlFor="content">
                  Nội dung trả lời <span className="text-destructive">*</span>
                </Label>
                <Textarea
                  id="content"
                  value={formData.content}
                  onChange={(e) => setFormData({ ...formData, content: e.target.value })}
                  placeholder="Soạn nội dung trả lời cho khách hàng tại đây. Sử dụng các biến từ danh sách bên cạnh để cá nhân hóa."
                  rows={8}
                  className="mt-1"
                />
              </div>
              
              <div>
                <Label>Placeholder có sẵn</Label>
                <div className="mt-1 space-y-2 max-h-48 overflow-y-auto">
                  {mockPlaceholders.map((placeholder) => (
                    <Button
                      key={placeholder}
                      type="button"
                      variant="outline"
                      size="sm"
                      className="w-full justify-start text-xs"
                      onClick={() => insertPlaceholder(placeholder)}
                    >
                      {placeholder}
                    </Button>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            Hủy
          </Button>
          <Button className="bg-primary hover:bg-primary-hover">
            Lưu
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}