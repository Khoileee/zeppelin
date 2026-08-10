# Việc cần sửa Demo — đưa từ 35 menu về 27 menu

### Đặc tả để một phiên Claude mới chạy trên máy có repo `dmp`

| | |
|---|---|
| **Đầu vào bắt buộc** | [Kiến trúc CHỐT](DMP-Kien-truc-CHOT.md) — bảng 27 menu và bảng ánh xạ cũ → mới |
| **Repo** | `dmp` *(React + Vite + TypeScript)* — **không nằm trên máy đang viết tài liệu này** |
| **Nguyên tắc** | ⭐ **Không xoá một màn nào.** Chỉ đổi chỗ đứng: menu → tab |
| **Ngày** | 10/08/2026 |

---

## 0. Làm gì trước

<details open>
<summary><b>Ba bước bắt buộc trước khi sửa dòng mã đầu tiên</b></summary>

| # | Bước | Lý do |
|:---:|---|---|
| **1** | Đọc [Kiến trúc CHỐT](DMP-Kien-truc-CHOT.md) — mục 1 và mục 2 | Toàn bộ việc sửa bám theo hai bảng đó |
| **2** | Chạy `npm run dev`, mở lần lượt **cả 35 menu**, chụp lại danh sách màn hiện có | Để đối chiếu sau khi sửa — không màn nào được biến mất |
| **3** | Tạo nhánh riêng: `git checkout -b rut-gon-27-menu` | Sửa cấu trúc điều hướng là thay đổi lớn, phải quay lại được |

</details>

---

## 1. Sửa thanh điều hướng

<details open>
<summary><b>Bước 1 — đổi danh sách menu về 27 mục</b></summary>

Tìm tệp khai danh sách menu *(thường là `src/layout/menu.ts` hoặc tương đương)* và thay bằng đúng 27 mục theo bảng chốt.

**Ba việc trong bước này**

| Việc | Chi tiết |
|---|---|
| Xoá **8 mục** khỏi danh sách | Menu cũ 1.1 · 1.4 · 1.6 · 2.5 · 3.3 · 5.5 · 7.2 · 7.4 |
| Đổi số **7 mục** | Theo bảng ánh xạ mục 2 của tài liệu chốt |
| Giữ nguyên **15 mục** | Không đụng vào |

> 🔴 **Chỉ xoá khỏi DANH SÁCH MENU, không xoá tệp màn.** Các tệp màn của 8 mục đó sẽ được dùng lại làm tab ở bước 3.

</details>

<details open>
<summary><b>Bước 2 — thêm thanh tìm kiếm lên đầu trang</b></summary>

Menu *Tìm kiếm toàn hệ thống* bị bỏ, nội dung chuyển thành thanh tìm kiếm **hiện ở mọi màn**.

| Yêu cầu | Chi tiết |
|---|---|
| Vị trí | Trong `PageHeader`, bên trái khu vực nút hành động |
| Hình thức | Ô nhập rộng ~360px, biểu tượng 🔍, chữ gợi ý *"Tìm bảng, cột, thuật ngữ, báo cáo, job…"* |
| Hành vi | Gõ vào → mở lớp phủ kết quả **ngay tại chỗ**, không rời màn đang xem |
| Nội dung kết quả | Dùng lại đúng nội dung màn *Tìm kiếm toàn hệ thống* cũ, nhóm theo loại đối tượng |
| Route cũ | `/search` giữ lại để không hỏng liên kết, nhưng không còn mục trên thanh điều hướng |

> ⭐ Đây là thay đổi **người xem demo cảm nhận rõ nhất** — tìm kiếm luôn trong tầm tay thay vì phải rời màn.

</details>

---

## 2. Chuyển 8 màn thành tab

<details open>
<summary><b>Bước 3 — bảng việc chi tiết cho từng màn</b></summary>

**Cách làm chung cho mọi trường hợp**

1. Màn cha đổi từ *trang đơn* sang *trang có tab* — nếu chưa có tab thì thêm component `Tabs`
2. Tab mới là một route con, ví dụ `/catalog/systems/channels`
3. Nội dung tab **giữ nguyên component cũ**, chỉ bỏ phần `PageHeader` riêng của nó *(vì đã dùng header của màn cha)*
4. Route cũ chuyển hướng sang route tab mới — để liên kết cũ không hỏng

**Tám việc cụ thể**

| # | Màn cũ | Vào làm tab của | Tên tab | Ghi chú riêng |
|:---:|---|---|---|---|
| 1 | Kênh trao đổi *(1.4)* | **1.2** Hệ thống & Nguồn | *Kênh trao đổi* | Màn cha vốn chưa có tab — phải thêm |
| 2 | Nhóm bảng *(1.6)* | **1.1** Bảng dữ liệu | *(không thành tab)* | ⭐ Thành **nút "Tạo nhóm"**: chọn nhiều dòng bằng ô tích → bấm nút → hộp thoại đặt tên nhóm. Danh sách nhóm đã tạo hiện trong hộp thoại chọn phạm vi ở 5.2 |
| 3 | Tiêu chuẩn thông tin mô tả *(2.5)* | **8.2** Cấu hình hệ thống | *Tiêu chuẩn thông tin mô tả* | Màn cha đã có tab — thêm tab thứ 5 |
| 4 | Phân tích dữ liệu *(3.3)* | **1.1** › tab *Cột* | — | ⭐ **Không thêm tab mới.** Tab *Cột* vốn đã hiện tỷ lệ rỗng và số giá trị phân biệt. Bổ sung phần còn thiếu *(phân bố giá trị, lịch sử quét)* vào cuối tab Cột dưới dạng khối gập được |
| 5 | Báo cáo quyền & Giám sát *(5.5)* | **5.2** Chính sách truy cập | *Báo cáo quyền* | Màn cha đã có 4 tab — thành tab thứ 5 |
| 6 | Bản ghi nguồn *(7.2)* | **7.2** Dữ liệu chủ | *Bản ghi nguồn* | Xem ghi chú dưới bảng |
| 7 | Nghi ngờ trùng *(7.3)* | **7.2** Dữ liệu chủ | *Nghi ngờ trùng* | |
| 8 | Bản ghi chuẩn *(7.4)* | **7.2** Dữ liệu chủ | *Bản ghi chuẩn & Phân phối* | |

**Ghi chú riêng cho module ⑦**

> Ba màn cũ 7.2 · 7.3 · 7.4 gộp thành **một menu mới tên "Dữ liệu chủ"** có 3 tab. Đây là menu **mới hoàn toàn về mặt điều hướng** — không phải một trong ba màn cũ làm cha.
>
> Thêm một dải trạng thái ở đầu màn cho thấy **dây chuyền ba bước**, số đếm trên mỗi bước:
> `Bản ghi nguồn (1.284) → Nghi ngờ trùng (37) → Bản ghi chuẩn (892)`
> Bấm vào bước nào thì mở tab đó. Đây là thứ làm rõ luồng mà ba menu rời rạc không làm được.

</details>

---

## 3. Sửa mọi liên kết chéo

<details open>
<summary><b>Bước 4 — chỗ dễ sót nhất</b></summary>

Sau khi đổi số menu, **mọi chỗ nhắc tới số menu cũ đều sai**. Ba nơi phải rà:

| Nơi | Cách tìm | Ví dụ phải sửa |
|---|---|---|
| **Chuỗi hiển thị trong màn** | Tìm toàn bộ mã nguồn các mẫu `menu 1.2` · `ở 3.4` · `(5.5)` | *"Ô Thuật ngữ ở tab Cột của **1.2**"* → **1.1** |
| **Từ điển trường** `fieldMeta.ts` | Trường `from` và `uses[]` chứa tên/số menu | `uses: ['3.3 Phân tích dữ liệu']` → `'1.1 › tab Cột'` |
| **Đường dẫn route** | Các `<Link to=...>` trỏ tới màn đã thành tab | `/quality/profiling` → `/catalog/tables/:id/columns` |

**Cách kiểm nhanh sau khi sửa**

```bash
# tim moi tham chieu so menu con sot
grep -rnE "menu [0-9]\.[0-9]|\([0-9]\.[0-9]\)" src/ | grep -vE "1\.[1-5]|2\.[1-4]|3\.[1-4]|4\.[1-3]|5\.[1-4]|6\.[1-3]|7\.[1-2]|8\.[1-2]"
```

Lệnh trên liệt kê những chỗ còn nhắc số menu **không nằm trong 27 mục hợp lệ** — mỗi dòng hiện ra là một chỗ phải sửa.

</details>

---

## 4. Ba việc làm demo bớt bị chê

<details open>
<summary><b>Ngoài chuyện rút gọn menu — ba điểm người xem sẽ soi</b></summary>

| # | Vấn đề | Cách sửa |
|:---:|---|---|
| **1** | **Không thấy luồng** — mở menu nào cũng là một bảng, không biết bước tiếp theo là gì | ⭐ Thêm khối **"Bước tiếp theo"** ở cuối các màn khai báo chính: sau khi khai bảng → *"Bước tiếp: gán luật chất lượng"* kèm nút đi thẳng. Áp cho 1.1 · 1.2 · 3.2 · 4.1 |
| **2** | **Không rõ menu nào quan trọng** — 27 mục vẫn bày ngang hàng | Trên thanh điều hướng, đánh dấu **1.1 Bảng dữ liệu** bằng biểu tượng ⭐, và **gom 5 nhóm vai trò** bằng màu nhạt ở lề trái mục *(🟦 nền móng · 🟩 trung tâm · 🟨 khai · 🟪 hàng chờ · ⬜ xem)* |
| **3** | **Hàng chờ không nổi bật** — 5 menu 🟪 là nơi có việc cần làm nhưng nhìn như mọi menu khác | Hiện **số đếm việc đang chờ** ngay cạnh nhãn menu: `Sự cố chất lượng ⑭` · `Phê duyệt ⑤` · `Yêu cầu quyền ⑫`. Đây là thứ làm demo trông "đang sống" |

> ⭐ **Việc số 1 là thứ trả lời trực tiếp câu *"không rõ luồng như nào"*.** Người xem không cần đọc tài liệu — demo tự chỉ đường.

</details>

---

## 5. Nghiệm thu

<details open>
<summary><b>Bảng kiểm trước khi báo xong</b></summary>

| # | Hạng mục | Đạt |
|:---:|---|:---:|
| 1 | Thanh điều hướng đúng **27 mục**, đúng thứ tự bảng chốt | ☐ |
| 2 | Mở đủ 27 menu, không menu nào lỗi hoặc trắng | ☐ |
| 3 | **Không màn nào biến mất** — đối chiếu với danh sách chụp ở bước 0 | ☐ |
| 4 | 8 màn đã chuyển thành tab đều mở được từ menu cha | ☐ |
| 5 | Route cũ của 8 màn đó **chuyển hướng** sang tab mới, không lỗi 404 | ☐ |
| 6 | Thanh tìm kiếm hiện ở **mọi màn**, gõ ra kết quả | ☐ |
| 7 | Menu 7.2 *Dữ liệu chủ* có 3 tab và dải trạng thái ba bước | ☐ |
| 8 | Lệnh `grep` ở mục 3 **không còn dòng nào** | ☐ |
| 9 | Khối *Bước tiếp theo* có ở 1.1 · 1.2 · 3.2 · 4.1 | ☐ |
| 10 | Số đếm việc chờ hiện cạnh 5 menu nhóm 🟪 | ☐ |
| 11 | `README.md` của repo demo cập nhật con số **27 menu** | ☐ |

</details>
