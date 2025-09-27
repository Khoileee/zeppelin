import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { DataTable } from "@/components/ui/data-table";
import { Badge } from "@/components/ui/badge";
import { Plus, Search, Edit, Trash2 } from "lucide-react";
import { TemplateDialog } from "@/components/templates/TemplateDialog";

interface Template {
  id: string;
  name: string;
  useCases: string[];
  conditions: string;
  updatedAt: string;
}

const mockData: Template[] = [
  {
    id: "1",
    name: "Trả lời GD Chuyển tiền lỗi - Ngân hàng bảo trì",
    useCases: ["Tra cứu chuyển tiền", "Đối soát giao dịch"],
    conditions: "Khi có lỗi và mã lỗi là 605",
    updatedAt: "15/03/2024",
  },
  {
    id: "2", 
    name: "Hướng dẫn xử lý không đủ số dư",
    useCases: ["Kiểm tra số dư"],
    conditions: "Khi số dư < số tiền giao dịch",
    updatedAt: "14/03/2024",
  },
  {
    id: "3",
    name: "Thông báo giao dịch thành công",
    useCases: ["Tra cứu chuyển tiền", "Kiểm tra số dư", "Đối soát giao dịch"],
    conditions: "Khi không có lỗi",
    updatedAt: "13/03/2024",
  },
];

export default function Templates() {
  const [searchTerm, setSearchTerm] = useState("");
  const [dialogOpen, setDialogOpen] = useState(false);
  const [selectedTemplate, setSelectedTemplate] = useState<Template | null>(null);

  const filteredData = mockData.filter((item) =>
    item.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    item.useCases.some((useCase) => 
      useCase.toLowerCase().includes(searchTerm.toLowerCase())
    )
  );

  const handleEdit = (template: Template) => {
    setSelectedTemplate(template);
    setDialogOpen(true);
  };

  const handleCreate = () => {
    setSelectedTemplate(null);
    setDialogOpen(true);
  };

  const columns = [
    {
      key: "name",
      header: "Tên mẫu trả lời",
      cell: (item: Template) => (
        <span className="font-semibold text-foreground">{item.name}</span>
      ),
    },
    {
      key: "useCases",
      header: "Áp dụng cho Nghiệp vụ",
      cell: (item: Template) => (
        <div className="flex flex-wrap gap-1">
          {item.useCases.slice(0, 2).map((useCase, index) => (
            <Badge key={index} variant="secondary" className="bg-accent text-accent-foreground text-xs">
              {useCase}
            </Badge>
          ))}
          {item.useCases.length > 2 && (
            <Badge variant="secondary" className="bg-muted text-muted-foreground text-xs">
              +{item.useCases.length - 2}
            </Badge>
          )}
        </div>
      ),
    },
    {
      key: "conditions",
      header: "Điều kiện áp dụng",
      cell: (item: Template) => (
        <span className="text-foreground">{item.conditions}</span>
      ),
    },
    {
      key: "updatedAt",
      header: "Ngày cập nhật",
      cell: (item: Template) => (
        <span className="text-muted-foreground">{item.updatedAt}</span>
      ),
    },
    {
      key: "actions",
      header: "Hành động",
      cell: (item: Template) => (
        <div className="flex items-center space-x-2">
          <Button
            variant="ghost"
            size="sm"
            className="text-primary hover:text-primary-hover p-1"
            onClick={() => handleEdit(item)}
          >
            <Edit className="h-4 w-4" />
          </Button>
          <Button
            variant="ghost"
            size="sm"
            className="text-destructive hover:text-destructive p-1"
          >
            <Trash2 className="h-4 w-4" />
          </Button>
        </div>
      ),
      className: "w-24",
    },
  ];

  return (
    <div className="p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-foreground">Quản lý Mẫu trả lời</h1>
        <div className="flex items-center space-x-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <Input
              placeholder="Tìm kiếm theo tên mẫu, nghiệp vụ..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 w-80"
            />
          </div>
          <Button onClick={handleCreate} className="bg-primary hover:bg-primary-hover">
            <Plus className="mr-2 h-4 w-4" />
            Thêm mới Mẫu trả lời
          </Button>
        </div>
      </div>

      {/* Data Table */}
      <DataTable data={filteredData} columns={columns} />

      {/* Pagination */}
      <div className="mt-4 flex justify-end">
        <p className="text-sm text-muted-foreground">
          Hiển thị 1-{filteredData.length} trên tổng số {mockData.length} mẫu trả lời
        </p>
      </div>

      {/* Dialog */}
      <TemplateDialog
        open={dialogOpen}
        onOpenChange={setDialogOpen}
        template={selectedTemplate}
      />
    </div>
  );
}