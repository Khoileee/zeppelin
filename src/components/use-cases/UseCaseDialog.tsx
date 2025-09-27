import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
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
import { Checkbox } from "@/components/ui/checkbox";
import { Plus, Trash2 } from "lucide-react";

interface UseCase {
  id: string;
  name: string;
  businessId: string;
  description: string;
  status: "active" | "draft";
  updatedAt: string;
}

interface UseCaseDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  useCase?: UseCase | null;
}

interface Input {
  id: string;
  variableId: string;
  required: boolean;
  prompt: string;
}

interface Output {
  id: string;
  variableId: string;
  columnMapping: string;
}

const mockVariables = [
  { id: "1", name: "Số thuê bao", placeholder: "<so_thue_bao>" },
  { id: "2", name: "Số tiền giao dịch", placeholder: "<so_tien_giao_dich>" },
  { id: "3", name: "Thời gian giao dịch", placeholder: "<thoi_gian_giao_dich>" },
  { id: "4", name: "Mã giao dịch", placeholder: "<ma_giao_dich>" },
];

const mockDataSources = [
  { id: "vw_transfers_30d", name: "Giao dịch chuyển tiền 30 ngày" },
  { id: "vw_subscriber_basic", name: "Thông tin thuê bao cơ bản" },
  { id: "vw_transaction_history", name: "Lịch sử giao dịch" },
];

const mockProcessingRules = [
  "Lọc theo 30 ngày gần nhất",
  "Ưu tiên giao dịch lỗi", 
  "Sắp xếp mới->cũ",
  "Lấy 5 giao dịch gần nhất",
];

export function UseCaseDialog({ open, onOpenChange, useCase }: UseCaseDialogProps) {
  const [formData, setFormData] = useState({
    name: useCase?.name || "",
    businessId: useCase?.businessId || "",
    description: useCase?.description || "",
    status: useCase?.status || "draft",
    dataSource: "",
    processingRules: [] as string[],
  });

  const [inputs, setInputs] = useState<Input[]>([]);
  const [outputs, setOutputs] = useState<Output[]>([]);

  const addInput = () => {
    const newInput: Input = {
      id: Date.now().toString(),
      variableId: "",
      required: false,
      prompt: "",
    };
    setInputs([...inputs, newInput]);
  };

  const removeInput = (id: string) => {
    setInputs(inputs.filter((input) => input.id !== id));
  };

  const updateInput = (id: string, field: keyof Input, value: any) => {
    setInputs(inputs.map((input) => 
      input.id === id ? { ...input, [field]: value } : input
    ));
  };

  const addOutput = () => {
    const newOutput: Output = {
      id: Date.now().toString(),
      variableId: "",
      columnMapping: "",
    };
    setOutputs([...outputs, newOutput]);
  };

  const removeOutput = (id: string) => {
    setOutputs(outputs.filter((output) => output.id !== id));
  };

  const updateOutput = (id: string, field: keyof Output, value: any) => {
    setOutputs(outputs.map((output) =>
      output.id === id ? { ...output, [field]: value } : output
    ));
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="text-xl">
            {useCase ? "Chỉnh sửa Nghiệp vụ" : "Tạo Nghiệp vụ mới"}
          </DialogTitle>
        </DialogHeader>

        <div className="space-y-8">
          {/* PHẦN 1: THÔNG TIN CƠ BẢN */}
          <div>
            <h3 className="text-lg font-semibold mb-4">PHẦN 1: THÔNG TIN CƠ BẢN</h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="name">Tên hiển thị nghiệp vụ *</Label>
                <Input
                  id="name"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  placeholder="Ví dụ: Tra cứu giao dịch chuyển tiền bị lỗi"
                />
              </div>
              <div>
                <Label htmlFor="businessId">ID nghiệp vụ (để AI Bot gọi) *</Label>
                <Input
                  id="businessId"
                  value={formData.businessId}
                  onChange={(e) => setFormData({ ...formData, businessId: e.target.value })}
                  placeholder="tra_cuu_giao_dich_loi"
                />
                <p className="text-xs text-muted-foreground mt-1">
                  Không chứa dấu cách, ký tự đặc biệt. Ví dụ: tra_cuu_giao_dich_loi
                </p>
              </div>
            </div>
            <div className="mt-4">
              <Label htmlFor="description">Mô tả</Label>
              <Textarea
                id="description"
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                rows={3}
              />
            </div>
            <div className="mt-4">
              <Label>Trạng thái</Label>
              <RadioGroup
                value={formData.status}
                onValueChange={(value) => setFormData({ ...formData, status: value as "active" | "draft" })}
                className="flex mt-2"
              >
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="draft" id="draft" />
                  <Label htmlFor="draft">Bản nháp</Label>
                </div>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="active" id="active" />
                  <Label htmlFor="active">Đang hoạt động</Label>
                </div>
              </RadioGroup>
            </div>
          </div>

          {/* PHẦN 2: CẤU HÌNH ĐẦU VÀO */}
          <div>
            <h3 className="text-lg font-semibold mb-2">PHẦN 2: CẤU HÌNH ĐẦU VÀO (INPUTS)</h3>
            <p className="text-sm text-muted-foreground mb-4">
              Định nghĩa các thông tin mà AI Bot cần cung cấp để thực thi nghiệp vụ này.
            </p>
            <Button
              type="button"
              variant="outline"
              onClick={addInput}
              className="mb-4"
            >
              <Plus className="mr-2 h-4 w-4" />
              Thêm Input
            </Button>
            <div className="space-y-3">
              {inputs.map((input) => (
                <div key={input.id} className="flex items-center space-x-3 p-3 border rounded-lg">
                  <Select
                    value={input.variableId}
                    onValueChange={(value) => updateInput(input.id, "variableId", value)}
                  >
                    <SelectTrigger className="w-64">
                      <SelectValue placeholder="Chọn Biến" />
                    </SelectTrigger>
                    <SelectContent>
                      {mockVariables.map((variable) => (
                        <SelectItem key={variable.id} value={variable.id}>
                          {variable.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <div className="flex items-center space-x-2">
                    <Checkbox
                      checked={input.required}
                      onCheckedChange={(checked) => updateInput(input.id, "required", checked)}
                    />
                    <Label className="text-sm">Bắt buộc?</Label>
                  </div>
                  <Input
                    placeholder="Câu hỏi gợi ý cho Bot"
                    value={input.prompt}
                    onChange={(e) => updateInput(input.id, "prompt", e.target.value)}
                    className="flex-1"
                  />
                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    onClick={() => removeInput(input.id)}
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              ))}
            </div>
          </div>

          {/* PHẦN 3: CẤU HÌNH XỬ LÝ & NGUỒN DỮ LIỆU */}
          <div>
            <h3 className="text-lg font-semibold mb-4">PHẦN 3: CẤU HÌNH XỬ LÝ & NGUỒN DỮ LIỆU</h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label>Nguồn dữ liệu *</Label>
                <Select
                  value={formData.dataSource}
                  onValueChange={(value) => setFormData({ ...formData, dataSource: value })}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Chọn nguồn dữ liệu" />
                  </SelectTrigger>
                  <SelectContent>
                    {mockDataSources.map((source) => (
                      <SelectItem key={source.id} value={source.id}>
                        {source.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label>Quy tắc xử lý</Label>
                <div className="mt-2 space-y-2">
                  {mockProcessingRules.map((rule, index) => (
                    <div key={index} className="flex items-center space-x-2">
                      <Checkbox />
                      <Label className="text-sm">{rule}</Label>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* PHẦN 4: CẤU HÌNH ĐẦU RA */}
          <div>
            <h3 className="text-lg font-semibold mb-2">PHẦN 4: CẤU HÌNH ĐẦU RA (OUTPUTS)</h3>
            <p className="text-sm text-muted-foreground mb-4">
              Định nghĩa các thông tin sẽ được trả về cho AI Bot sau khi xử lý.
            </p>
            <Button
              type="button"
              variant="outline"
              onClick={addOutput}
              className="mb-4"
            >
              <Plus className="mr-2 h-4 w-4" />
              Thêm Output
            </Button>
            <div className="space-y-3">
              {outputs.map((output) => (
                <div key={output.id} className="flex items-center space-x-3 p-3 border rounded-lg">
                  <Select
                    value={output.variableId}
                    onValueChange={(value) => updateOutput(output.id, "variableId", value)}
                  >
                    <SelectTrigger className="w-64">
                      <SelectValue placeholder="Chọn Biến" />
                    </SelectTrigger>
                    <SelectContent>
                      {mockVariables.map((variable) => (
                        <SelectItem key={variable.id} value={variable.id}>
                          {variable.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <Input
                    placeholder="Ánh xạ từ cột nguồn (ví dụ: amount)"
                    value={output.columnMapping}
                    onChange={(e) => updateOutput(output.id, "columnMapping", e.target.value)}
                    className="flex-1"
                  />
                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    onClick={() => removeOutput(output.id)}
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              ))}
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