import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { DataTable } from "@/components/ui/data-table";
import { StatusBadge } from "@/components/ui/status-badge";
import { Plus, Search, Edit, Trash2 } from "lucide-react";
import { UseCaseDialog } from "@/components/use-cases/UseCaseDialog";

interface UseCase {
  id: string;
  name: string;
  businessId: string;
  description: string;
  status: "active" | "draft";
  updatedAt: string;
}

const mockData: UseCase[] = [
  {
    id: "1",
    name: "Tra cứu giao dịch chuyển tiền",
    businessId: "tra_cuu_chuyen_tien",
    description: "Tra cứu thông tin giao dịch chuyển tiền của khách hàng",
    status: "active",
    updatedAt: "15/03/2024",
  },
  {
    id: "2", 
    name: "Kiểm tra số dư tài khoản",
    businessId: "kiem_tra_so_du",
    description: "Kiểm tra số dư hiện tại trong tài khoản",
    status: "draft",
    updatedAt: "14/03/2024",
  },
  {
    id: "3",
    name: "Đối soát giao dịch lỗi",
    businessId: "doi_soat_giao_dich_loi", 
    description: "Đối soát và xử lý các giao dịch bị lỗi",
    status: "active",
    updatedAt: "13/03/2024",
  },
];

export default function UseCases() {
  const [searchTerm, setSearchTerm] = useState("");
  const [dialogOpen, setDialogOpen] = useState(false);
  const [selectedUseCase, setSelectedUseCase] = useState<UseCase | null>(null);

  const filteredData = mockData.filter(
    (item) =>
      item.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.businessId.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleEdit = (useCase: UseCase) => {
    setSelectedUseCase(useCase);
    setDialogOpen(true);
  };

  const handleCreate = () => {
    setSelectedUseCase(null);
    setDialogOpen(true);
  };

  const columns = [
    {
      key: "name",
      header: "Tên nghiệp vụ",
      cell: (item: UseCase) => (
        <span className="font-semibold text-foreground">{item.name}</span>
      ),
    },
    {
      key: "businessId",
      header: "ID nghiệp vụ",
      cell: (item: UseCase) => (
        <code className="text-sm bg-muted px-2 py-1 rounded text-muted-foreground">
          {item.businessId}
        </code>
      ),
    },
    {
      key: "description",
      header: "Mô tả",
      cell: (item: UseCase) => (
        <span className="text-foreground">{item.description}</span>
      ),
    },
    {
      key: "status",
      header: "Trạng thái",
      cell: (item: UseCase) => (
        <StatusBadge variant={item.status}>
          {item.status === "active" ? "Đang hoạt động" : "Bản nháp"}
        </StatusBadge>
      ),
    },
    {
      key: "updatedAt",
      header: "Ngày cập nhật",
      cell: (item: UseCase) => (
        <span className="text-muted-foreground">{item.updatedAt}</span>
      ),
    },
    {
      key: "actions",
      header: "Hành động",
      cell: (item: UseCase) => (
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
        <h1 className="text-2xl font-bold text-foreground">Quản lý Nghiệp vụ</h1>
        <div className="flex items-center space-x-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <Input
              placeholder="Tìm kiếm theo tên hoặc ID nghiệp vụ..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 w-80"
            />
          </div>
          <Button onClick={handleCreate} className="bg-primary hover:bg-primary-hover">
            <Plus className="mr-2 h-4 w-4" />
            Thêm mới Nghiệp vụ
          </Button>
        </div>
      </div>

      {/* Data Table */}
      <DataTable data={filteredData} columns={columns} />

      {/* Pagination */}
      <div className="mt-4 flex justify-end">
        <p className="text-sm text-muted-foreground">
          Hiển thị 1-{filteredData.length} trên tổng số {mockData.length} nghiệp vụ
        </p>
      </div>

      {/* Dialog */}
      <UseCaseDialog
        open={dialogOpen}
        onOpenChange={setDialogOpen}
        useCase={selectedUseCase}
      />
    </div>
  );
}