import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { DataTable } from "@/components/ui/data-table";
import { Badge } from "@/components/ui/badge";
import { Plus, Search, Edit, Trash2 } from "lucide-react";
import { VariableDialog } from "@/components/variables/VariableDialog";

interface Variable {
  id: string;
  displayName: string;
  placeholder: string;
  dataType: "text" | "number" | "currency" | "datetime" | "boolean";
  maskingRule: "none" | "full" | "middle" | "last4" | "first6";
}

const mockData: Variable[] = [
  {
    id: "1",
    displayName: "Số thuê bao",
    placeholder: "<so_thue_bao>",
    dataType: "text",
    maskingRule: "middle",
  },
  {
    id: "2",
    displayName: "Số tiền giao dịch",
    placeholder: "<so_tien_giao_dich>",
    dataType: "currency", 
    maskingRule: "none",
  },
  {
    id: "3",
    displayName: "Thời gian giao dịch",
    placeholder: "<thoi_gian_giao_dich>",
    dataType: "datetime",
    maskingRule: "none",
  },
  {
    id: "4",
    displayName: "Mã giao dịch",
    placeholder: "<ma_giao_dich>",
    dataType: "text",
    maskingRule: "last4",
  },
];

const dataTypeLabels = {
  text: "Text",
  number: "Number", 
  currency: "Currency",
  datetime: "Datetime",
  boolean: "Boolean",
};

const maskingRuleLabels = {
  none: "Không che",
  full: "Che toàn bộ",
  middle: "Che phần giữa", 
  last4: "Che 4 số cuối",
  first6: "Che 6 số đầu",
};

export default function Variables() {
  const [searchTerm, setSearchTerm] = useState("");
  const [dialogOpen, setDialogOpen] = useState(false);
  const [selectedVariable, setSelectedVariable] = useState<Variable | null>(null);

  const filteredData = mockData.filter(
    (item) =>
      item.displayName.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.placeholder.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleEdit = (variable: Variable) => {
    setSelectedVariable(variable);
    setDialogOpen(true);
  };

  const handleCreate = () => {
    setSelectedVariable(null);
    setDialogOpen(true);
  };

  const columns = [
    {
      key: "displayName",
      header: "Tên hiển thị",
      cell: (item: Variable) => (
        <span className="font-semibold text-foreground">{item.displayName}</span>
      ),
    },
    {
      key: "placeholder",
      header: "Placeholder",
      cell: (item: Variable) => (
        <code className="text-sm bg-muted px-2 py-1 rounded text-muted-foreground">
          {item.placeholder}
        </code>
      ),
    },
    {
      key: "dataType",
      header: "Kiểu dữ liệu",
      cell: (item: Variable) => (
        <Badge variant="secondary" className="bg-accent text-accent-foreground">
          {dataTypeLabels[item.dataType]}
        </Badge>
      ),
    },
    {
      key: "maskingRule", 
      header: "Quy tắc Masking",
      cell: (item: Variable) => (
        <span className="text-foreground">{maskingRuleLabels[item.maskingRule]}</span>
      ),
    },
    {
      key: "actions",
      header: "Hành động", 
      cell: (item: Variable) => (
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
        <h1 className="text-2xl font-bold text-foreground">Thư viện Biến</h1>
        <div className="flex items-center space-x-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <Input
              placeholder="Tìm kiếm theo tên hoặc placeholder..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 w-80"
            />
          </div>
          <Button onClick={handleCreate} className="bg-primary hover:bg-primary-hover">
            <Plus className="mr-2 h-4 w-4" />
            Thêm mới Biến
          </Button>
        </div>
      </div>

      {/* Data Table */}
      <DataTable data={filteredData} columns={columns} />

      {/* Pagination */}
      <div className="mt-4 flex justify-end">
        <p className="text-sm text-muted-foreground">
          Hiển thị 1-{filteredData.length} trên tổng số {mockData.length} biến
        </p>
      </div>

      {/* Dialog */}
      <VariableDialog
        open={dialogOpen}
        onOpenChange={setDialogOpen}
        variable={selectedVariable}
      />
    </div>
  );
}