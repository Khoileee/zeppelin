# DMP — Kiến trúc CHỐT

### 8 module · 27 menu — bản duy nhất đúng, mọi tài liệu và demo phải theo bản này

| | |
|---|---|
| **Ngày chốt** | 10/08/2026 |
| **Thay cho** | Mọi con số menu ở các tài liệu cũ *(21 · 34 · 35)* đều **không còn hiệu lực** |
| **Căn cứ rút gọn** | Nguyên tắc **NT7** — *menu = một thực thể được QUẢN LÝ; thứ chỉ để xem là tab* |
| **Đọc cùng** | [Tổng quan một trang](DMP-Tong-quan-1-trang.md) — bảng 5 nhóm vai trò |

> 🔴 **Quy tắc từ nay:** tài liệu nào ghi số menu khác 27 là tài liệu chưa cập nhật. Đối chiếu về đây.

---

## 1. Kiến trúc chốt — 27 menu

<details open>
<summary><b>⭐ BẢNG CHỐT — 8 module · 27 menu · tab bên trong từng menu</b></summary>

| Module | # | Menu | Các tab bên trong | Nhóm vai trò |
|---|:---:|---|---|:---:|
| **① DATA CATALOG** | 1.1 | **Bảng dữ liệu** ⭐ | Tổng quan · **Cột** *(gồm chỉ số đo)* · Chất lượng · Nguồn gốc · Quyền · Lịch sử | 🟩 |
| | 1.2 | **Hệ thống & Nguồn** | Hệ thống · **Kênh trao đổi** | 🟦 |
| | 1.3 | **Báo cáo & Chỉ tiêu** | Báo cáo · Chỉ tiêu | 🟨 |
| | 1.4 | **Miền dữ liệu** | — | 🟦 |
| | 1.5 | **Danh mục tham chiếu** | Dữ liệu · Định nghĩa trường · Phiên bản · Chờ duyệt | 🟦 |
| **② GOVERNANCE** | 2.1 | **Từ điển nghiệp vụ** | — | 🟨 |
| | 2.2 | **Phân loại & Nhãn** | Mức phân loại · Nhãn nhạy cảm | 🟨 |
| | 2.3 | **Truy vết luồng dữ liệu** | Bản đồ · Khai báo thủ công · Độ phủ | ⬜ |
| | 2.4 | **Phê duyệt & Phiên bản** | Chờ tôi duyệt · Đã duyệt · Lịch sử phiên bản | 🟪 |
| **③ DATA QUALITY** | 3.1 | **Thư viện luật** | — | 🟦 |
| | 3.2 | **Luật & Kết quả** | Bảng điều khiển · Gán luật · Theo chiều chất lượng | 🟨 |
| | 3.3 | **Sự cố chất lượng** | Đang mở · Tôi xử lý · Chờ tôi duyệt · Đã đóng | 🟪 |
| | 3.4 | **Cảnh báo** | Quy tắc · Kênh gửi · Lịch sử gửi | 🟨 |
| **④ NẠP & ĐIỀU PHỐI** | 4.1 | **Luồng xử lý (Job)** | Bước · Lịch chạy · Lần chạy · Phiên bản | 🟨 |
| | 4.2 | **Cửa nạp dữ liệu** | Mẫu nạp · Lịch sử nạp · Cổng chất lượng · **Vùng chờ** | 🟨 |
| | 4.3 | **Theo dõi & Pipeline** | Sơ đồ · Danh sách tác vụ · Đang hỏng | ⬜ |
| **⑤ DATA SECURITY** | 5.1 | **Người dùng & Nhóm** | Người dùng · Nhóm · Vai trò · Quyền menu | 🟦 |
| | 5.2 | **Chính sách truy cập** | Quyền dữ liệu · Che dữ liệu · Lọc theo dòng · Theo nhãn · **Báo cáo quyền** | 🟨 |
| | 5.3 | **Yêu cầu cấp quyền** | Chờ tôi duyệt · Tôi đã xin · Sắp hết hạn | 🟪 |
| | 5.4 | **Nhật ký kiểm toán** | Tất cả · Truy vấn · Xuất dữ liệu · Thay đổi quyền | ⬜ |
| **⑥ CHÍNH SÁCH & TUÂN THỦ** | 6.1 | **Chính sách dữ liệu** | — | 🟨 |
| | 6.2 | **Vòng đời & Lưu trữ** | Vòng đời · **Đến hạn xử lý** · Chia sẻ bên thứ ba | 🟨🟪 |
| | 6.3 | **Đánh giá tuân thủ** | Kỳ đánh giá · Danh mục kiểm · Kế hoạch khắc phục | 🟪 |
| **⑦ DỮ LIỆU CHỦ (MDM)** | 7.1 | **Mô hình dữ liệu chủ** | — | 🟨 |
| | 7.2 | **Dữ liệu chủ** | **Bản ghi nguồn** · **Nghi ngờ trùng** · **Bản ghi chuẩn & Phân phối** | 🟪 |
| **⑧ OPERATIONS** | 8.1 | **Sức khoẻ dữ liệu** | Tổng quan · Độ phủ · Theo miền | ⬜ |
| | 8.2 | **Cấu hình hệ thống** | Kết nối · Tier · Chuẩn đặt tên · Tham số · **Tiêu chuẩn thông tin mô tả** | 🟦 |
| | **27** | | | |

**Ngoài thanh điều hướng**

| Thành phần | Vị trí |
|---|---|
| 🔍 **Tìm kiếm toàn hệ thống** | ⭐ Thanh tìm kiếm trên **đầu trang, hiện ở mọi màn** — không còn là menu |
| ➕ **Tạo nhóm bảng** | Nút trong menu 1.1, chọn nhiều bảng rồi gộp |

</details>

---

## 2. Bảng ánh xạ cũ → mới

<details open>
<summary><b>⭐ Dùng bảng này để sửa demo và tài liệu — 35 menu cũ đi về đâu</b></summary>

| Menu cũ | → | Vị trí mới | Loại thay đổi |
|---|:---:|---|---|
| 1.1 Tìm kiếm toàn hệ thống | → | **Thanh tìm kiếm đầu trang** | 🔀 Bỏ khỏi menu |
| 1.2 Bảng dữ liệu | → | **1.1** Bảng dữ liệu | 🔢 Đổi số |
| 1.3 Hệ thống & Nguồn | → | **1.2** Hệ thống & Nguồn | 🔢 Đổi số |
| 1.4 Kênh trao đổi | → | **1.2** › tab *Kênh trao đổi* | 🔀 Thành tab |
| 1.5 Báo cáo & Chỉ tiêu | → | **1.3** Báo cáo & Chỉ tiêu | 🔢 Đổi số |
| 1.6 Nhóm bảng | → | **1.1** › nút *Tạo nhóm* | 🔀 Thành chức năng |
| 1.7 Miền dữ liệu | → | **1.4** Miền dữ liệu | 🔢 Đổi số |
| 1.8 Danh mục tham chiếu | → | **1.5** Danh mục tham chiếu | 🔢 Đổi số |
| 2.1 Từ điển nghiệp vụ | → | **2.1** | ✅ Giữ nguyên |
| 2.2 Phân loại & Nhãn | → | **2.2** | ✅ Giữ nguyên |
| 2.3 Truy vết luồng dữ liệu | → | **2.3** | ✅ Giữ nguyên |
| 2.4 Phê duyệt & Phiên bản | → | **2.4** | ✅ Giữ nguyên |
| 2.5 Tiêu chuẩn thông tin mô tả | → | **8.2** › tab *Tiêu chuẩn thông tin mô tả* | 🔀 Thành tab |
| 3.1 Thư viện luật | → | **3.1** | ✅ Giữ nguyên |
| 3.2 Luật & Kết quả | → | **3.2** | ✅ Giữ nguyên |
| 3.3 Phân tích dữ liệu | → | **1.1** › tab *Cột* | 🔀 Thành tab |
| 3.4 Sự cố chất lượng | → | **3.3** Sự cố chất lượng | 🔢 Đổi số |
| 3.5 Cảnh báo | → | **3.4** Cảnh báo | 🔢 Đổi số |
| 4.1 · 4.2 · 4.3 | → | **4.1 · 4.2 · 4.3** | ✅ Giữ nguyên |
| 5.1 · 5.2 · 5.3 · 5.4 | → | **5.1 · 5.2 · 5.3 · 5.4** | ✅ Giữ nguyên |
| 5.5 Báo cáo quyền & Giám sát | → | **5.2** › tab *Báo cáo quyền* | 🔀 Thành tab |
| 6.1 · 6.2 · 6.3 | → | **6.1 · 6.2 · 6.3** | ✅ Giữ nguyên |
| 7.1 Mô hình dữ liệu chủ | → | **7.1** | ✅ Giữ nguyên |
| 7.2 Bản ghi nguồn | → | **7.2** › tab *Bản ghi nguồn* | 🔀 Thành tab |
| 7.3 Nghi ngờ trùng | → | **7.2** › tab *Nghi ngờ trùng* | 🔀 Thành tab |
| 7.4 Bản ghi chuẩn & Phân phối | → | **7.2** › tab *Bản ghi chuẩn & Phân phối* | 🔀 Thành tab |
| 8.1 · 8.2 | → | **8.1 · 8.2** | ✅ Giữ nguyên |

**Tổng hợp**

| Loại | Số menu |
|---|:---:|
| ✅ Giữ nguyên số | 15 |
| 🔢 Chỉ đổi số | 7 |
| 🔀 Thành tab hoặc chức năng | 8 |
| | **35 → 27** |

> ⚠️ **Không menu nào bị xoá chức năng.** 8 menu chuyển thành tab vẫn giữ nguyên toàn bộ nội dung màn.

</details>

---

## 3. Ba lý do để trả lời khi bị hỏi "sao lại rút gọn"

<details open>
<summary><b>Lập luận bảo vệ quyết định này</b></summary>

| # | Lý do | Bằng chứng |
|:---:|---|---|
| **1** | **Thiết kế đang vi phạm nguyên tắc của chính nó.** NT7 nói *thứ chỉ để xem là tab*, nhưng có 9 menu không quản lý thực thể nào | 1.1 · 2.5 · 3.3 · 5.5 · 7.2 · 7.4 đều là màn chỉ đọc |
| **2** | **Người dùng thường ngày chỉ chạm 6 menu**, còn lại là việc của quản trị viên hoặc màn báo cáo. Bày 35 mục ngang hàng làm người dùng tưởng phải học cả 35 | Xem bảng 5 nhóm vai trò ở [Tổng quan một trang](DMP-Tong-quan-1-trang.md) |
| **3** | **Ba menu MDM là ba trạng thái của cùng một bản ghi** — nguồn → nghi ngờ → chuẩn. Tách ba menu bắt người dùng tự ghép lại trong đầu | Luồng 7.2 → 7.3 → 7.4 chỉ đi một chiều, không ai mở 7.4 mà không qua 7.3 |

**Câu trả lời ngắn cho lãnh đạo**

> *Không cắt tính năng nào. Chỉ xếp lại: những màn chỉ để xem thì đưa vào làm tab của màn cha, thay vì bày ngang hàng trên thanh điều hướng. Thanh điều hướng ngắn hơn 23%, và mỗi mục còn lại đều trả lời được câu "tôi quản lý cái gì ở đây".*

</details>

---

## 4. Việc phải làm để mọi thứ khớp nhau

<details open>
<summary><b>Danh sách việc — theo thứ tự bắt buộc</b></summary>

| # | Việc | Trạng thái | Ghi chú |
|:---:|---|:---:|---|
| 1 | Chốt kiến trúc 27 menu | ✅ **Xong** | Tài liệu này |
| 2 | Cập nhật *Tổng quan một trang* theo 27 menu | ✅ **Xong** | |
| 3 | Đánh dấu tài liệu cũ là hết hiệu lực | ✅ **Xong** | Có khối cảnh báo ở đầu mỗi tài liệu |
| 4 | **Sửa demo theo 27 menu** | ⏸ **Chờ repo** | Đặc tả đầy đủ ở [Việc cần sửa Demo](DMP-Viec-can-sua-Demo.md) |
| 5 | Viết lại thân bài *Đề xuất tool* theo 27 menu | ⏸ | Khối lượng lớn — làm sau khi demo xong để hai bên khớp |
| 6 | Sinh lại 55 ảnh minh hoạ với thanh điều hướng 27 menu | ⏸ | Sửa `MENU` trong `tools/mockgen/dmp.py` rồi chạy lại `run.py` |
| 7 | Viết lại walkthrough theo **một kịch bản liền mạch** | ⏸ | Không đi theo menu — đi theo công việc thật |

</details>
