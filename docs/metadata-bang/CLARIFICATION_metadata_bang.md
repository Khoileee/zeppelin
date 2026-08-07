# DANH SÁCH CẦN BỔ SUNG SRS — Module Quản lý bảng / Metadata bảng (FR-MTD)

> **Mục đích:** Liệt kê các điểm còn thiếu/chưa rõ trong `SRS_metadata_bang.md` v3.x **để viết được KBKT (kịch bản kiểm thử) chính xác**, không phải đoán.
> **Người điền:** BA / PO / BE (tùy mục). Vui lòng điền cột **Trả lời** rồi gửi lại.
> **Quy ước mức độ:** 🔴 Chặn viết case · 🟠 Case đang phải đoán · 🟢 Nên có để đủ độ phủ.
>
> **Đã loại khỏi danh sách:** Phân quyền theo role (A2) — vì hệ thống phân quyền theo **API** (chỉ cần kiểm tra có/không quyền gọi), không theo ma trận role.

---

## A. Thiếu nghiêm trọng — chặn viết case chính xác

### A1. 🔴 UI/Design thật (liên quan NI-01)

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| A1.1 | Có Figma/mockup cho 5 màn (Business Metadata, Thông tin chung, Tab Schema, Tab Sample data, Tab Quản lý upload)? | |
| A1.2 | **Nhãn chính xác** trên UI của từng control (đang lấy theo Functional Spec, cần xác nhận đúng từng chữ)? | |
| A1.3 | **Nội dung tooltip** khi nút bị disable: "Download schema" và "Refresh Sample data" khi bảng chưa có schema hiển thị tooltip gì? | |
| A1.4 | Kiểu thông báo lỗi/thành công: **inline / toast / modal**? (SRS ghi "Inline/Toast" chưa thống nhất) | |
| A1.5 | Đường dẫn (route/URL) thật của từng màn? (KBKT đang tạm đặt `/quan-ly-bang/chi-tiet/...`) | |

### A3. 🔴 Template Import/Download — chốt cột chính thức (liên quan NI-05)

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| A3.1 | File template **final** (đã bỏ "Giá trị mẫu", đổi "Tần suất tổng hợp"→"Tần suất đồng bộ") cho cả 3: Table / Schema / Download Metadata? | |
| A3.2 | **Header cột chính xác** từng template (đúng tên, đúng thứ tự) — KBKT round-trip cần khớp 100%. | |
| A3.3 | Cột nào là **bắt buộc** (đánh dấu \*) → để test đúng case "thiếu cột bắt buộc" (VAL-MTD-04)? | |
| A3.4 | Template Schema dùng **chung** cho Download (FUNC-05) và Import (FUNC-07) — xác nhận giống hệt nhau (gồm cột "Tên bảng")? | |

### A4. 🔴 Maxlength & ràng buộc nhập của trường text

| # | Trường | Maxlength | Ký tự đặc biệt? | Trim? | Trả lời khác |
|---|--------|-----------|-----------------|-------|--------------|
| A4.1 | Ô "Tần suất khác" (FUNC-03) | | | | |
| A4.2 | "Tập giá trị/Khoảng" (FUNC-04, textarea) | | | | |
| A4.3 | "Quy tắc nghiệp vụ" (FUNC-04, textarea) | | | | |
| A4.4 | "Mô tả" cột schema / mô tả bảng | | | | |
| A4.5 | Tên trường (schema) | | | | |
| A4.6 | Tên file khai báo upload (FUNC-01) — giới hạn độ dài tên? | | | | |

### A5. 🔴 Tập giá trị (enum) cho các trường "Chọn"

| # | Trường | Câu hỏi | Trả lời |
|---|--------|---------|---------|
| A5.1 | **Phân loại dữ liệu** | Danh sách giá trị cụ thể (Nhạy cảm / Cơ bản / …)? Nguồn từ governance? | |
| A5.2 | **Kiểu dữ liệu** (cột schema) | Free text hay dropdown cố định? Nếu cố định: liệt kê (string/double/float/…)? | |
| A5.3 | **Glossary term** | Dropdown chọn từ governance hay nhập tự do? | |
| A5.4 | **Domain (Tag)** | Danh sách giá trị / nguồn? | |
| A5.5 | **DE / BDA phụ trách** | Chọn từ danh sách user hay nhập text? | |

---

## B. Thiếu chi tiết nghiệp vụ — case đang bị mơ hồ

### B1–B2. 🟠 Tab Schema (FUNC-04)

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| B1.1 | User được **thêm/xóa dòng cột** trong grid Schema không, hay chỉ sửa cột có sẵn? | |
| B1.2 | Bấm "Refresh schema" khi đang có edit **chưa lưu** → ghi đè mất dữ liệu? Có popup xác nhận không? | |
| B2.1 | **Tên trường trùng nhau** trong schema → xử lý thế nào (báo lỗi / cho phép)? | |
| B2.2 | Lưu schema **rỗng (0 cột)** có được không? | |
| B2.3 | Khi thêm dòng cột mới, "Tên trường" có bắt buộc nhập trước khi Lưu không? | |

### B3–B6. 🟠 Import (FUNC-07)

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| B3.1 | Lỗi mức **dòng hay mức file**? File 100 dòng có 3 dòng sai → import 97 dòng đúng hay **fail toàn bộ**? | |
| B4.1 | Phân biệt **cột vắng mặt hẳn** vs **cột có nhưng ô trống**: cột không bắt buộc mà vắng hẳn thì giữ giá trị cũ hay set null? (ô trống đã chốt = null) | |
| B5.1 | Giá trị **NULLABLE** trong file: chỉ chấp nhận `YES`/`NO` hay cả `Y/N`, `true/false`, `1/0`, chữ thường, có khoảng trắng? | |
| B5.2 | Giá trị **Khóa**: chỉ `PK`/`FK` hay biến thể khác? Phân biệt hoa/thường? | |
| B5.3 | Map **Tên bảng**: phân biệt **hoa/thường**? Có **trim** khoảng trắng đầu/cuối không? | |
| B6.1 | File bất thường — kỳ vọng xử lý cho: **file 0 byte, file Excel hỏng, file có mật khẩu, đúng đuôi `.xlsx` nhưng sai định dạng thật (MIME)**? | |
| B6.2 | **Giới hạn dung lượng / số dòng** của file import (FUNC-07)? (FUNC-01 đã có 50MB; FUNC-07 chưa nêu) | |
| B6.3 | Upload **trùng tên file** → cho phép / cảnh báo? | |

### B7. 🟠 Sample data (FUNC-08) (liên quan NI-06)

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| B7.1 | **Nguồn** dữ liệu mẫu: HDFS hay DB? | |
| B7.2 | **Giới hạn số dòng** cụ thể (con số)? ("theo cơ chế hiện hành" = bao nhiêu?) | |
| B7.3 | Hiển thị **những cột nào** (toàn bộ schema hay giới hạn)? Có timeout query không? | |
| B7.4 | Bảng **có schema nhưng 0 dòng dữ liệu** → hiển thị gì (empty state) so với **query lỗi** (VAL-MTD-06)? | |

### B8. 🟠 Tên file export (FUNC-02, FUNC-05)

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| B8.1 | Quy ước **tên file tải về** (vd `Metadata_<TenBang>_<yyyyMMdd>.xlsx`)? | |

---

## C. Thiếu để hoàn thiện độ phủ (nên có)

| # | Mức | Câu hỏi | Trả lời |
|---|-----|---------|---------|
| C1 | 🟢 | Ngoài `ERR-MTD-500`, có yêu cầu xử lý: **timeout mạng, mất kết nối khi upload, sửa schema đồng thời (2 user)**? | |
| C2 | 🟢 | Cờ "Đã có schema" có **quay lại false** (xóa schema) không? Nếu có → Download schema & Sample data ẩn lại? | |
| C3 | 🟢 | Có yêu cầu **ghi log/audit** (ai sửa metadata, khi nào) cần kiểm thử không? | |
| C4 | 🟢 | NI-07: **nơi lưu file vật lý** (MinIO?) — ảnh hưởng test "tải lại đúng file gốc" về tính bền vững/khôi phục. | |
| C5 | 🟢 | An toàn dữ liệu file Excel: kỳ vọng xử lý **Formula/CSV injection** (ô bắt đầu bằng `= + - @`) khi import rồi export lại — escape/literal hay bỏ qua? | |

---

## Mức độ sẵn sàng hiện tại của KBKT

- ✅ **Đã gen được (200 case / 4 sheet):** luồng chính + validation có mã lỗi (VAL/EX) + business rule (BR-MTD) + mapping NULLABLE/PK-FK — phần SRS đã đủ rõ.
- ⏳ **Để hoàn chỉnh, ưu tiên đóng:** **A3 (template chốt) → A4 (maxlength) → A5 (enum) → A1 (Figma)** + nhóm **B** (edge case nghiệp vụ). Đóng được nhóm A là bổ sung được ngay các case biên + round-trip chính xác.

> Sau khi BA điền, gửi lại file này — sẽ cập nhật/bổ sung KBKT tương ứng (case biên, round-trip, edge case import, empty/error sample data…).
