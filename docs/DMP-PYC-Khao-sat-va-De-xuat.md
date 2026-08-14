# Ứng dụng AI vào luồng PYC — Hiện trạng, đề xuất và câu hỏi khảo sát

---

## 1. Nền tảng đã có sẵn trong SQLWF

### 1.1 PYC đã được đồng bộ từ Jira

Dịch vụ riêng `jira-scanner` đang chạy trên môi trường thật.
Màn hình: `pyc-management` (route `data-delivery/pyc-management`).

`PycEntity` — bảng `tbl_pyc` (PostgreSQL):

| Trường | Nội dung |
|---|---|
| `pycCode` | Mã phiếu |
| `orgRequest` | Đơn vị yêu cầu |
| `summary` · `description` | Tiêu đề, mô tả yêu cầu |
| `issueType` · `source` | Loại phiếu, nguồn |
| `baInCharge` · `deInCharge` | BDA và DE phụ trách |
| `jiraLink` | Liên kết ngược Jira |
| `sqlWfJobIds` | Job trên SQLWF sinh ra từ phiếu |
| `jobs` | Bảng nối `tbl_pyc_job_mappings` — tên job, lịch chạy, thư mục |
| `relatedBusinessIds` | Liên kết sang bản ghi nghiệp vụ |

Có thêm `PycHistoryEntity` lưu lịch sử thay đổi phiếu.

### 1.2 Đã có nơi lưu nghiệp vụ kèm SQL và bảng

`BusinessInformationEntity` — màn hình `business-management/profession` — chứa đủ thông tin đầu vào cho AI:

| Trường | Nội dung |
|---|---|
| `name` · `normalizedName` | Tên nghiệp vụ, tên đã chuẩn hoá sẵn để so khớp |
| `description` | Mô tả nghiệp vụ bằng tiếng Việt |
| `sql` | Câu SQL đã dùng |
| `tableIds` | Bảng đã dùng |
| `ticketCodes` | Mã PYC liên quan |
| `jiraLink` | Liên kết Jira |
| `status` · `rejectReason` | Trạng thái duyệt |
| `version` · `oldVersions` | Lịch sử phiên bản |

Bộ *mô tả nghiệp vụ ↔ câu SQL ↔ bảng đã dùng ↔ mã PYC* là dữ liệu để AI đối chiếu, và **không cần xây mới**.

> **Vấn đề: hiện đã khai được bao nhiêu bản ghi?** — câu hỏi 16, 17 ở mục 7.

### 1.3 Đăng ký đồng bộ từ hệ thống sản phẩm

`DatabaseSyncInfo` — màn hình `sync-management` (khối *Thông tin đồng bộ*) — cho biết dữ liệu nào đã được kéo về từ DB bên sản phẩm:

| Trường | Nội dung |
|---|---|
| `databaseType` · `cluster` · `ipPort` | Loại và vị trí DB nguồn |
| `databaseName` · `tableName` | **Database và bảng bên hệ thống sản phẩm** |
| `owner` · `account` · `dbLink` | Chủ sở hữu schema, tài khoản kết nối |
| `isConnected` | Đã kết nối được chưa |
| `syncCommand` | Câu lệnh đồng bộ |
| `bdaResponsible` · `deResponsible` | **BDA và DE phụ trách đường đồng bộ này** |
| `status` · `rejectReason` | Trạng thái duyệt (bắt đầu từ `DRAFT`) |
| `notes` | Ghi chú |

Đây là nơi trả lời câu *"dữ liệu này đã kéo về chưa, từ hệ thống nào, ai phụ trách"*.

**Thiếu một trường:** `DatabaseSyncInfo` có BDA và DE **phía mình**, nhưng **không có đầu mối bên hệ thống sản phẩm** — người mà BDA phải hỏi khi đối ứng nghiệp vụ.

### 1.4 Vai trò cột

| Vai trò | Hiện trạng |
|---|---|
| Khoá liên kết | ✅ `Field.isKey` + `Field.keyType` (PK / FK) |
| Trục thời gian | 🟡 Suy được từ `Field.dateFormat` + `Field.type` |
| Chiều phân tích | ❌ Chưa có |
| Chỉ số đo lường | ❌ Chưa có |

---

## 2. Luồng đề xuất

BDA đứng giữa: **đơn vị yêu cầu cần gì** và **hệ thống sản phẩm đang có gì**.

```
        PYC trên Jira
              │  jira-scanner — ĐÃ CÓ
              ▼
     PYC trong SQLWF ──────────► File đính kèm
   summary · description              │ đọc CẤU TRÚC, bỏ phần thân dữ liệu
   orgRequest · baInCharge            ▼
              │            Danh sách cột đầu ra mong muốn
              └──────────┬────────────┘
                         ▼
           ┌──────────────────────────────┐
           │  Đối chiếu 4 nguồn            │
           │ ① Nghiệp vụ đã làm            │ ← business-management
           │ ② PYC cũ + job đã sinh        │ ← pyc-management
           │ ③ Danh mục bảng tầng A        │ ← table-management
           │ ④ Đã đồng bộ từ nguồn nào     │ ← sync-management
           └──────────────┬───────────────┘
                          ▼
              Dữ liệu đã có trong kho chưa?
                 ┌────────┴─────────┐
                CÓ                KHÔNG
                 │                  │
                 ▼                  ▼
       Chấm điểm độ khớp    NHÁNH ĐỐI ỨNG NGHIỆP VỤ
       → Cao / TB / Thấp    • chỉ ra hệ thống sản phẩm khả dĩ
                 │          • chỉ ra đầu mối để hỏi
                 │          • mở yêu cầu đồng bộ mới
                 ▼                  │
           BDA duyệt / sửa          ▼
                 │          Đồng bộ → ETL → quay lại nhánh trái
                 ▼
       Viết job → chạy thử → bàn giao
                 ▼
    Ghi ngược thành bản ghi nghiệp vụ mới
```

- Bước đồng bộ Jira đã có sẵn
- AI chỉ nằm ở khối **đối chiếu và chấm điểm** — không đụng dữ liệu thật
- Bước ghi ngược làm hệ thống tốt dần mà không ai phải khai thêm


### Về việc tra cứu trên Jira

BDA hiện tra từ khoá trên Jira để tìm job, PYC và nghiệp vụ liên quan. Đây **chính là thao tác mà đề xuất này tự động hoá**

Khác biệt so với tra tay trên Jira:

| Tra trên Jira | Tra trong SQLWF |
|---|---|
| Chỉ tìm được trong nội dung phiếu | Tìm cả trong mô tả nghiệp vụ, câu SQL, tên bảng |
| Không biết phiếu đó cuối cùng dùng bảng nào | Có `relatedBusinessIds` và `sqlWfJobIds` dẫn thẳng tới bảng và job |
| Không biết bảng đó giờ còn hoạt động không | Có trạng thái bảng, điểm chất lượng, job nguồn còn chạy không |
| Phụ thuộc người viết phiếu dùng đúng từ khoá | Mở rộng từ khoá bằng từ điển thuật ngữ (`data-glossary`) |

---

## 3. Input SQLWF đã có để làm context cho AI

Mọi trường dưới đây đã tồn tại, chưa được dùng cho mục đích này.

### 3.1 Phân loại bảng — tách bảng đáng dùng khỏi bảng rác

| Tín hiệu | Lấy từ đâu | Nói lên điều gì |
|---|---|---|
| `dataMart` | `TableInfo` — `table-management` | Bảng phục vụ khai thác, ứng viên hàng đầu |
| `isTemplateTable` | `TableInfo` — `table-management` | Bảng khuôn mẫu, không phải dữ liệu thật |
| `active` | `TableInfo` — `table-management` | Bảng đã ngừng sử dụng |
| `approvedUser` · `approvedDate` | `TableInfo` — `table-management` | Đã qua phê duyệt, đã có người chịu trách nhiệm |
| Quy ước tên `tmp_` `_bak` `_test` `draft_` `_20250812` | Tên bảng | Gần như chắc chắn là bảng tạm |
| `area` · `path` | `TableInfo` · `AreaInfo` | Lớp dữ liệu: thô / trung gian / khai thác |
| `totalSize` | `TableInfo` — `table-management` | Bảng rỗng hoặc quá nhỏ thường là bảng thử |
| `createdDate` vs `updatedDate` | `TableInfo` — `table-management` | Tạo xong không đụng tới = bảng bỏ |
| Có ai truy vấn tay không | `SQLQueryHistory.creator` — `sql-query-history` · `LogRunSql.username` — `query-history` | Bảng có người mở ra query = có giá trị nghiệp vụ thật |
| Bảng là đầu ra cuối chuỗi job | Lineage suy từ SQL của job — `job-management` | Không job nào đọc tiếp = bảng phục vụ người dùng |

### 3.2 Hiểu nội dung bảng

| Tín hiệu | Lấy từ đâu | Nói lên điều gì |
|---|---|---|
| `description` | `TableInfo` — `table-management` | Mô tả nghiệp vụ của bảng |
| `useCases` → `queryName` · `description` · `query` | `TableInfo` — `table-management` | Tình huống sử dụng kèm câu SQL mẫu |
| `domainIds` · `subDomainIds` · `domainNames` | `TableInfo` · `Domain` — `table-management` · `domain-management` | Miền và miền con nghiệp vụ |
| `businessLink` | `TableInfo` — `table-management` | Liên kết sang tài liệu nghiệp vụ |
| `businessMetadataFile` | `TableInfo` — `table-management` | File metadata nghiệp vụ đính kèm |
| `jobName` | `TableInfo` — `table-management` | Job sinh ra bảng, mở đường sang câu lệnh SQL |
| `syncFrequency` | `TableInfo` — `table-management` | Chu kỳ cập nhật, lọc theo yêu cầu ngày/tháng |
| `tableGroupName` · `accessibleTableIds` | `TableGroup` — `table-monitor` | Bảng nào hay đi cùng nhau |
| `pathPatterns` | `TableGroup` — `table-monitor` | Nhóm bảng theo đường dẫn |

### 3.3 Hiểu từng cột

| Tín hiệu | Lấy từ đâu | Nói lên điều gì |
|---|---|---|
| `name` · `type` | `Field` — `table-management`, phần khai trường | Định danh và kiểu dữ liệu |
| `description` | `Field` — `table-management`, phần khai trường | Mô tả nghiệp vụ của cột |
| `glossaryTeam` | `Field` → `DataGlossary` — `data-glossary` | Thuật ngữ nghiệp vụ chuẩn gắn vào cột |
| `isKey` · `keyType` (PK/FK) | `Field` — `table-management`, phần khai trường | Khoá liên kết, dùng để đề xuất cách nối bảng |
| `dateFormat` | `Field` — `table-management`, phần khai trường | Cột thuộc trục thời gian |
| `valueRange` · `dqEnum` | `Field` — `table-management`, phần khai trường | Tập giá trị hợp lệ, cột là chiều phân loại |
| `businessRule` | `Field` — `table-management`, phần khai trường | Ràng buộc nghiệp vụ |
| `nullable` | `Field` — `table-management`, phần khai trường | Cột bắt buộc = cột lõi của bảng |
| `tagIds` | `Field` — `table-management`, phần khai trường | Nhãn phân loại, gồm nhãn nhạy cảm |
| `codecable` | `Field` — `table-management`, phần khai trường | Cột thuộc diện mã hoá |
| `order` | `Field` — `table-management`, phần khai trường | Cột đầu thường là khoá và chiều |
| Vị trí cột trong SQL của job | Câu lệnh job — `job-management` | `GROUP BY` → chiều · `SUM/AVG/COUNT` → chỉ số · `JOIN ON` → khoá |

### 3.4 Thuật ngữ và miền nghiệp vụ

| Tín hiệu | Lấy từ đâu | Nói lên điều gì |
|---|---|---|
| `name` · `alias` · `definition` | `DataGlossary` — `data-glossary` | Tên gọi khác của cùng một khái niệm, dùng để khớp từ ngữ trong PYC |
| `relates` | `DataGlossary` — `data-glossary` | Thuật ngữ liên quan, mở rộng từ khoá tìm kiếm |
| `cde` | `DataGlossary` — `data-glossary` | Đánh dấu dữ liệu trọng yếu |
| `parent` · `level` · `path` | `DataGlossary` — `data-glossary` | Cây phân cấp thuật ngữ |
| `owner` · `stewards` | `DataGlossary` — `data-glossary` | Ai định nghĩa thuật ngữ |
| `parentId` · `ancestorIds` | `Domain` — `domain-management` *(Quản lý Domains)* | Cây miền nghiệp vụ |

### 3.5 Độ tin cậy của bảng

| Tín hiệu | Lấy từ đâu | Nói lên điều gì |
|---|---|---|
| `tableQuality` | `TableInfo` — `table-management` | Điểm chất lượng |
| `dqEnable` · `dqType` · `dqMin` · `dqMax` | `TableInfo` — `data-quality` | Bảng có được giám sát không |
| `dqCycleType` · `dqDelay` | `TableInfo` — `data-quality` | Chu kỳ và độ trễ cho phép |
| `metrics` | `Field` — `table-management`, phần khai trường | Cột nào có ràng buộc chất lượng |
| Lịch sử chạy job | `JobHistory` · `ExecutionHistoryEntity` — `job-management` | Job nguồn còn chạy đều không |
| `status` · `executionTime` | `SQLQueryHistory` — `sql-query-history` | Truy vấn trên bảng này hay lỗi hoặc chậm không |
| Nhật ký thay đổi cấu trúc | `history-data` *(Lịch sử thay đổi)* | Bảng hay đổi cột = rủi ro khi dùng |

### 3.6 Người liên quan

| Tín hiệu | Lấy từ đâu | Nói lên điều gì |
|---|---|---|
| `businessOwner` | `TableInfo` — `table-management` | Đầu mối nghiệp vụ, hỏi ai khi không rõ |
| `dataEngineerOwner` | `TableInfo` — `table-management` | Đầu mối kỹ thuật |
| `createdUser` · `updatedUser` | `TableInfo` — `table-management` | Ai dựng, ai sửa gần nhất |
| `creator` | `SQLQueryHistory` — `sql-query-history` | Ai hay truy vấn bảng này, người hiểu bảng nhất trên thực tế |
| `baInCharge` · `deInCharge` | `PycEntity` — `pyc-management` | BDA và DE từng xử lý loại yêu cầu này |
| `owner` · `stewards` | `DataGlossary` — `data-glossary` | Người định nghĩa thuật ngữ |

### 3.7 Nguồn dữ liệu và đường đồng bộ

| Tín hiệu | Lấy từ đâu | Nói lên điều gì |
|---|---|---|
| `databaseName` · `tableName` | `DatabaseSyncInfo` — `sync-management` | Bảng nào bên hệ thống sản phẩm đã được kéo về |
| `databaseType` · `cluster` · `ipPort` | `DatabaseSyncInfo` — `sync-management` | Dữ liệu đến từ hệ thống nào |
| `isConnected` · `status` | `DatabaseSyncInfo` — `sync-management` | Đường đồng bộ còn sống hay đang chờ duyệt |
| `syncCommand` | `DatabaseSyncInfo` — `sync-management` | Đồng bộ toàn bộ hay chỉ một phần cột |
| `bdaResponsible` · `deResponsible` | `DatabaseSyncInfo` — `sync-management` | **Ai từng làm việc với hệ thống nguồn này — người hỏi được đầu tiên** |
| `connectionName` · `databaseType` | `ConnectionInfo` — `connection-management` | Danh mục kết nối đã thiết lập |
| `inputAdapter` · `dbConfig` · `ftpConfig` · `kafkaConfig` | `IOInfo` | Đường dữ liệu vào: DB, FTP hay Kafka |
| `schema` của file nạp | `FileIOInfo` | Cấu trúc dữ liệu nhận từ ngoài |

### 3.8 Nghiệp vụ đã xử lý

| Tín hiệu | Lấy từ đâu | Nói lên điều gì |
|---|---|---|
| `name` · `normalizedName` | `BusinessInformationEntity` — `business-management/profession` | Tên nghiệp vụ chuẩn hoá, khớp trực tiếp với mô tả PYC mới |
| `description` | `BusinessInformationEntity` — `business-management/profession` | Mô tả nghiệp vụ bằng tiếng Việt |
| `sql` | `BusinessInformationEntity` — `business-management/profession` | Câu SQL đã chạy thật, đã có người kiểm |
| `tableIds` | `BusinessInformationEntity` — `business-management/profession` | Bảng nào thực sự được dùng cho nghiệp vụ đó |
| `ticketCodes` | `BusinessInformationEntity` — `business-management/profession` | Các PYC cùng loại |
| `oldVersions` | `BusinessInformationEntity` — `business-management/profession` | Nghiệp vụ đã thay đổi qua thời gian |
| `summary` · `description` · `orgRequest` | `PycEntity` — `pyc-management` | Yêu cầu gốc và đơn vị đề nghị |
| `sqlWfJobIds` · `jobs` | `PycEntity` — `pyc-management` | Job sinh ra từ phiếu, mở đường tới toàn bộ câu lệnh |
| `relatedBusinessIds` | `PycEntity` — `pyc-management` | Nối phiếu sang bản ghi nghiệp vụ |
| `issueType` | `PycEntity` — `pyc-management` | Phân loại yêu cầu |
| `pycCode` · `deliveryTime` | `IoHistoryInfo` — `delivery` | Phiếu này đã bàn giao gì, cho ai, lúc nào |
| `commands` · `cronExpression` | `TaskInfo` · `TempJob` — `job-management` | Câu lệnh và lịch chạy của job |

---

## 4. Đề xuất bổ sung

### 4.1 Gắn nhãn cho bảng

Hệ thống có `tagIds` cho cột nhưng chưa có nhãn ở cấp bảng.

| Nhóm nhãn | Giá trị | Ai gắn |
|---|---|---|
| Mức sử dụng | Khai thác · Trung gian · Tạm · Ngừng dùng | Máy đề xuất từ tín hiệu mục 3.1, người xác nhận |
| Chủ đề nghiệp vụ | Khách hàng · Giao dịch · Doanh thu · Sản phẩm · Kênh | Máy đề xuất từ miền và thuật ngữ, người xác nhận |
| Độ tin cậy | Đã chuẩn hoá · Chưa kiểm chứng | Đầu mối |
| Bản chính thức | Đánh dấu bảng chuẩn khi có nhiều bảng gần giống | Đầu mối |

Hai cách gắn để không ai phải mở từng bảng:

- Gắn hàng loạt trên màn danh sách sau khi lọc
- Nạp từ file — mở rộng chức năng nạp dữ liệu đã có, thêm cột nhãn vào mẫu

### 4.2 Bổ sung vai trò cột

Thêm một trường vào `Field`, nhận bốn giá trị: chiều phân tích · chỉ số đo lường · trục thời gian · khoá liên kết.

| Bước | Cách làm | Độ phủ ước tính |
|---|---|---|
| 1 | Lấy từ `isKey` / `keyType` sẵn có | Cột khoá: gần đủ |
| 2 | Suy từ `dateFormat`, `type`, quy ước tên (`ngay_*`, `ma_*`, `so_tien_*`) | ~60% |
| 3 | Phân tích vị trí cột trong câu lệnh SQL của job | ~80–85% |

Không ai phải khai tay.

---

## 5. Học từ nghiệp vụ cũ — học cái gì

Không huấn luyện mô hình. Dựng bộ tra cứu rồi tìm bản ghi giống nhất.

### 5.1 Mỗi bản ghi gồm

| Thành phần | Lấy từ | Vai trò |
|---|---|---|
| Câu hỏi | `PycEntity.summary` + `description`, `BusinessInformationEntity.description` | Vế trái để so khớp |
| Từ khoá chuẩn hoá | `normalizedName` + thuật ngữ khớp trong `data-glossary` | Xử lý cùng nghĩa khác chữ |
| Đơn vị yêu cầu | `PycEntity.orgRequest` | Cùng đơn vị thường yêu cầu giống nhau |
| Loại yêu cầu | `PycEntity.issueType` | Phân nhóm thống kê / đối soát / báo cáo định kỳ |
| Đáp án — bảng | `BusinessInformationEntity.tableIds` | Bảng thực sự đã dùng |
| Đáp án — câu lệnh | `BusinessInformationEntity.sql` | SQL đã chạy thật |
| Đáp án — job | `PycEntity.sqlWfJobIds` → `TaskInfo.commands` | Toàn bộ các bước xử lý |
| Cột đầu ra | Phân tích mệnh đề `SELECT` của câu SQL | Danh sách trường kết quả |
| Người làm | `baInCharge` · `deInCharge` | Hỏi ai khi cần |
| Thời gian thực hiện | `createdDate` → `IoHistoryInfo.deliveryTime` | Ước lượng công sức cho phiếu mới |

### 5.2 Khi có PYC mới, so khớp trên bốn trục

| Trục | So cái gì | Trọng số |
|---|---|---|
| Ngữ nghĩa yêu cầu | Mô tả PYC mới ↔ mô tả nghiệp vụ cũ, sau khi mở rộng bằng từ điển thuật ngữ | Cao nhất |
| Cột đầu ra | Tiêu đề trong mẫu Excel đính kèm ↔ cột `SELECT` của nghiệp vụ cũ | Cao |
| Đơn vị và loại phiếu | `orgRequest` · `issueType` | Trung bình |
| Miền dữ liệu | Miền suy từ từ khoá ↔ `domainIds` của bảng đã dùng | Trung bình |

### 5.3 Ghi ngược sau khi làm xong

Sau khi BDA bàn giao, hệ thống tự đề nghị tạo bản ghi nghiệp vụ mới với SQL và bảng đã dùng — BDA chỉ đặt tên và bấm lưu.

Mỗi phiếu xử lý xong làm cho phiếu sau dễ hơn.

---

## 6. Ba mức đầu ra

| Mức | Điều kiện | Đầu ra | Người làm gì |
|---|---|---|---|
| **Cao** | Có nghiệp vụ cũ đủ giống, bảng đã dùng vẫn còn hoạt động | Sinh SQL dựa trên câu lệnh cũ, thay tham số kỳ và điều kiện lọc. Kèm liên kết phiếu cũ và tên người từng làm | Kiểm và sửa |
| **Trung bình** | Không có nghiệp vụ cũ đủ giống, nhưng khớp được phần lớn cột đầu ra với bảng tầng A | Danh sách bảng ứng viên · cách nối theo khoá · cột nào chưa tìm được nguồn · rào cản (dữ liệu lưu bao nhiêu tháng, cột nhạy cảm cần duyệt) | Quyết định chọn bảng |
| **Chưa có trong kho** | Không tìm thấy bảng nào trong kho chứa dữ liệu cần, và `sync-management` không có đường đồng bộ tương ứng | Chuyển sang nhánh đối ứng nghiệp vụ: liệt kê hệ thống sản phẩm khả dĩ theo miền nghiệp vụ · chỉ ra BDA và DE từng làm việc với hệ thống đó · mở phiếu yêu cầu đồng bộ | Liên hệ đầu mối bên sản phẩm |
| **Thấp** | Dữ liệu có thể đã có trong kho nhưng dưới ngưỡng khớp | Không đề xuất. Chỉ đưa danh sách bảng gần nhất, nêu rõ *chưa đủ dữ liệu để đề xuất*, và sinh việc bổ sung metadata cho đúng vùng nghiệp vụ đó | Xử lý như hiện nay |

### Nếu triển khai xong mà đa số rơi vào mức thấp

**Đo trước khi xây.** Thử nghiệm đối chiếu, một người làm trong vài ngày, không cần code sản phẩm:

1. Lấy 30 PYC gần nhất đã xử lý xong
2. Giả vờ chưa biết đáp án, chạy so khớp bằng script trên dữ liệu hiện có
3. Đối chiếu bảng hệ thống đề xuất với bảng BDA thực tế đã dùng
4. Đếm số phiếu rơi vào mỗi mức

| Tỷ lệ đạt cao + trung bình | Kết luận |
|---|---|
| ≥ 50% | Triển khai theo lộ trình |
| 20–50% | Làm giàu dữ liệu nghiệp vụ trước |
| < 20% | Chưa làm. Quay lại phân tầng bảng và làm giàu nghiệp vụ |

---

## 7. Câu hỏi khảo sát BDA lead

### Nhóm A — Cách phân công phiếu yêu cầu

*Để biết có tồn tại nhóm phiếu giống nhau không, và nhận ra bằng dấu hiệu gì.*

1. Khi nhận PYC mới, chị dựa vào đâu để giao cho BDA nào? *(đơn vị yêu cầu · miền dữ liệu · ai đang rảnh · người từng làm việc tương tự)*
2. Có nhóm phiếu nào lặp theo chu kỳ không — báo cáo tháng, đối soát định kỳ? Ước chừng bao nhiêu phần trăm tổng số phiếu?
3. Chị có nhận ra *"phiếu này giống phiếu tháng trước"* không? Nhận ra bằng cách nào, có ghi lại ở đâu hay chỉ nhớ?
4. Có trường hợp hai đơn vị yêu cầu cùng một thứ nhưng diễn đạt khác nhau không? Xử lý thế nào?
5. Mỗi BDA có mảng nghiệp vụ riêng cố định, hay ai cũng làm mọi mảng?
6. Một phiếu trung bình mất bao lâu từ nhận tới bàn giao? Trong đó bao lâu là đi tìm dữ liệu, bao lâu là làm thật?
7. Phiếu nào hay chậm nhất, chậm vì lý do gì?

### Nhóm B — Cách BDA tìm ra bảng cần dùng

*Để biết máy thay được khâu nào trong quy trình thật.*

8. Khi nhận yêu cầu mới hoàn toàn, BDA làm gì đầu tiên để tìm bảng?
9. Nguồn nào hay dùng nhất: tra từ khoá trên Jira · tự tìm trên SQLWF · xem lại SQL cũ · hỏi người · tài liệu?
10. Khi tra từ khoá trên Jira, thường tìm được gì — phiếu cũ, tên job, hay cả câu SQL? Tỷ lệ tìm được thứ dùng lại được là bao nhiêu?
11. Tra trên Jira có hay bị trượt vì người viết phiếu dùng từ khác không? Xử lý thế nào?
12. Anh BDA có nói *"thông tin khách hàng nằm ở rất nhiều bảng, lấy từ datamart chỉ hợp với phiếu đơn giản"*. Với phiếu phức tạp hơn thì thực tế xử lý thế nào — đi hỏi ai, hỏi cái gì, mất bao lâu?
13. Có xảy ra chọn nhầm bảng rồi phải làm lại không? Nguyên nhân thường là gì?
14. Khi có nhiều bảng tên gần giống, dựa vào đâu để biết bảng nào là bản dùng chính thức?
15. Có danh sách bảng *hay dùng* mà BDA tự truyền tay nhau không?

### Nhóm C — Đối ứng nghiệp vụ và nguồn dữ liệu

*Nhánh yêu cầu mới hoàn toàn, dữ liệu chưa có trong kho.*

16. Bao nhiêu phần trăm phiếu rơi vào trường hợp **dữ liệu chưa có trong kho**, phải đối ứng với bên sản phẩm?
17. BDA phát hiện ra điều đó ở thời điểm nào — ngay khi đọc phiếu, hay sau khi đã tìm khắp kho?
18. Khi phải đối ứng nghiệp vụ, tìm ra đầu mối bên hệ thống sản phẩm bằng cách nào? Có danh sách sẵn không hay hỏi vòng quanh?
19. Đầu mối bên sản phẩm thường là vai trò gì — quản trị hệ thống, người phát triển, hay người nghiệp vụ?
20. Một lần đối ứng thường mất bao lâu, từ lúc gửi câu hỏi tới lúc xác định được bảng và trường bên nguồn?
21. Sau khi xác định được, thủ tục để mở đường đồng bộ mới gồm những bước gì? Mất bao lâu?
22. Thông tin đối ứng đó có được ghi lại ở đâu không, hay chỉ nằm trong trao đổi qua chat và email?
23. Có trường hợp đối ứng xong mới biết bên sản phẩm không có dữ liệu đó không? Bao nhiêu phần trăm?
24. Màn `sync-management` hiện có bao nhiêu bản ghi đăng ký đồng bộ? Có phản ánh đúng thực tế đang chạy không?
25. Đơn vị yêu cầu có nắm được dữ liệu của họ nằm ở hệ thống sản phẩm nào không, hay chỉ mô tả nhu cầu?

### Nhóm D — Mức độ đã khai của dữ liệu hiện có

*Các con số quyết định lộ trình.*

26. Màn khai nghiệp vụ (`business-management/profession`) hiện có khoảng bao nhiêu bản ghi? Trong đó bao nhiêu có đủ cả mô tả, câu SQL và danh sách bảng?
27. Ai khai nghiệp vụ — bắt buộc hay tự nguyện? Khai trước khi làm hay sau khi bàn giao?
28. Màn PYC (`pyc-management`) hiện có bao nhiêu phiếu đã đồng bộ về, từ thời điểm nào?
29. Trường **BDA phụ trách** và **job liên quan** trên phiếu có được điền đầy đủ không hay thường bỏ trống?
30. Có bao nhiêu bảng được đánh dấu **datamart**? Bảng datamart có bắt buộc phải có mô tả không?
31. Phần **tình huống sử dụng** kèm câu SQL mẫu trong chi tiết bảng — có ai đang dùng không, ước chừng bao nhiêu bảng đã khai?
32. Từ điển thuật ngữ (`data-glossary`) hiện có bao nhiêu thuật ngữ? Đã gắn được vào cột của bảng chưa?
33. Trong tổng số bảng, ước chừng bao nhiêu phần trăm là bảng tạm, bảng nháp, bảng thử?
34. Có quy ước đặt tên nào để phân biệt bảng tạm với bảng chính thức không?

### Nhóm E — File đính kèm trong phiếu

*Để quyết định có xử lý file đính kèm không và tới đâu.*

35. Một phiếu thường đính kèm những loại file gì? Loại nào hay gặp nhất?
36. **File Excel đính kèm thường là mẫu trống hay đã điền số liệu thật?**
37. Mẫu Excel có cấu trúc tương đối giống nhau giữa các phiếu không, hay mỗi đơn vị một kiểu?
38. Có trường hợp đính kèm chính báo cáo tháng trước làm ví dụ không?
39. File PDF đính kèm thường là gì — công văn, tờ trình, hay có cả mô tả yêu cầu kỹ thuật?
40. Thông tin quan trọng nhất để làm được phiếu nằm ở đâu: mô tả trên Jira, file đính kèm, hay phải trao đổi thêm?
41. Bao nhiêu phần trăm phiếu chỉ đọc mô tả là đủ hiểu, không cần hỏi lại?

### Nhóm F — Đầu ra và bàn giao

*Để xác định phạm vi đề xuất dừng ở đâu.*

42. Kết quả bàn giao thường ở dạng gì — bảng dữ liệu, file, hay dashboard trên Tableau / VDSD?
43. Nếu là dashboard, ai dựng: BDA hay đơn vị yêu cầu tự dựng?
44. Câu SQL sau khi làm xong có được lưu lại ở đâu không, hay nằm trong job rồi thôi?
45. Có bước nào bắt buộc xin duyệt trước khi bàn giao không — dữ liệu nhạy cảm, phát hành ra ngoài đơn vị?
46. Sau khi bàn giao, có theo dõi xem đơn vị còn dùng không?

### Nhóm G — Nếu có công cụ hỗ trợ

*Để kiểm tra giả định có đúng nhu cầu thật không.*

47. Nếu hệ thống gợi ý sẵn *"phiếu này giống phiếu X năm ngoái, đã dùng bảng Y, đây là câu SQL cũ"* — dùng được không, hay vẫn phải làm lại từ đầu?
48. Nếu hệ thống trả lời được ngay trong ngày đầu *"dữ liệu này chưa có trong kho, cần đối ứng với hệ thống Z, người từng làm là anh A"* — tiết kiệm được bao nhiêu?
49. Gợi ý sai ở mức nào thì vẫn chấp nhận được, mức nào thì gây phiền hơn là giúp?
50. Cái nào giá trị hơn: **gợi ý bảng nên dùng**, hay **cảnh báo bảng không nên dùng** *(đã ngừng nạp, chất lượng kém)*?
51. Nếu phải bỏ công khai thêm metadata để đổi lấy tính năng này, mức nào là chấp nhận được?

---

## 8. Đề nghị

| # | Việc | Cần ai |
|:---:|---|---|
| 1 | Khảo sát theo bộ câu hỏi mục 7 | BDA lead |
| 2 | Lấy số liệu nhóm D: số bản ghi nghiệp vụ, số phiếu đã đồng bộ, số bảng datamart | Quản trị hệ thống |
| 3 | Chạy thử nghiệm đối chiếu trên 30 phiếu gần nhất (mục 6) | 1 người, vài ngày |
| 4 | Căn cứ kết quả bước 3 quyết định phạm vi và thời điểm triển khai | Lãnh đạo |

Không cam kết phạm vi trước khi có kết quả bước 3.
