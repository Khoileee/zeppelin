# DMP — Tổng quan một trang

### Toàn bộ 35 menu trong một bảng, xếp theo VAI TRÒ trong luồng chứ không theo module

| | |
|---|---|
| **Đọc cái này khi** | Bạn thấy 35 menu quá nhiều và không nắm được luồng |
| **Ngày** | 10/08/2026 |
| **Thay cho** | Không cần đọc walkthrough hay tài liệu đề xuất để nắm tổng quan — chỉ cần trang này |
| **⭐ Đã chốt** | Kiến trúc rút gọn còn **27 menu** — xem [DMP-Kien-truc-CHOT.md](DMP-Kien-truc-CHOT.md). Bảng dưới vẫn giữ **35 menu cũ** để đối chiếu |

---

## Vì sao nhìn vào thấy loạn

<details open>
<summary><b>Nguyên nhân — và cách sắp xếp lại cho dễ hiểu</b></summary>

**Nguyên nhân:** cả 35 menu đang được trình bày **ngang hàng nhau** trên thanh điều hướng, như thể mỗi cái là một chức năng phải học.

Thực tế **chúng không ngang hàng**. Trong 35 menu:

| Loại | Số menu | Bạn phải làm gì |
|---|:---:|---|
| 🟦 **Nền móng** | 7 | Khai **một lần** lúc thiết lập, sau đó gần như không mở lại |
| 🟩 **Trung tâm** | 1 | ⭐ Mở **hằng ngày** — đây gần như là toàn bộ trải nghiệm người dùng thường |
| 🟨 **Khai khi phát sinh** | 13 | Có bảng mới / job mới / chính sách mới thì mới vào |
| 🟪 **Hàng chờ việc** | 5 | Hệ thống đẩy việc tới, bạn xử lý — giống hộp thư đến |
| ⬜ **Chỉ để xem** | 9 | Không khai gì cả — chỉ đọc lại số liệu các menu khác sinh ra |

> ⭐ **Người dùng thường ngày chỉ chạm vào 2 nhóm: 🟩 trung tâm và 🟪 hàng chờ.**
> 🟦 nền móng là việc của quản trị viên lúc dựng hệ thống. ⬜ chỉ để xem là màn báo cáo.

**Luồng chạy — bốn chặng**

```
🟦 NỀN MÓNG            🟨 KHAI ĐỐI TƯỢNG         ⚙️ MÁY TỰ CHẠY          🟪 HÀNG CHỜ VIỆC
khai một lần      →    khai khi phát sinh   →   không ai bấm gì    →    người xử lý
                                                                            ↓
                                                                      ⬜ MÀN XEM
                                                                   đọc lại kết quả
```

*Ví dụ đi hết một vòng:* khai **hệ thống** 🟦 → khai **bảng** 🟩 → gán **luật chất lượng** 🟨 → máy chạy luật, phát hiện lỗi → sinh **sự cố** 🟪 → người xử lý → chỉ số lên **màn sức khoẻ** ⬜.

</details>

---

## Bảng tổng quan — 35 menu

<details open>
<summary><b>⭐ BẢNG CHÍNH — mở ra xem đủ 35 menu</b></summary>

**Cách đọc:** cột *Lấy từ* = menu nào phải khai trước. Cột *Cấp cho* = khai xong thì ai dùng lại.

| Nhóm | Menu | Để làm gì — một câu | Lấy từ | Cấp cho |
|:---:|---|---|---|---|
| 🟦 | **1.3** Hệ thống & Nguồn | Khai các hệ thống đang có dữ liệu *(CRM, tính cước…)* | 5.1 · 7.1 | Ô chọn *Hệ thống* ở 1.2, 1.4 |
| 🟦 | **1.7** Miền dữ liệu | Chia dữ liệu công ty thành các miền nghiệp vụ, mỗi miền có người chịu trách nhiệm | 5.1 | Ô *Miền* ở 1.2 · phạm vi quyền ở 5.2 |
| 🟦 | **1.8** Danh mục tham chiếu | Bảng mã dùng chung *(tỉnh/thành, loại hợp đồng…)* | — | Tập giá trị hợp lệ của cột ở 1.2 |
| 🟦 | **2.5** Tiêu chuẩn thông tin mô tả | Tra cứu: khai một bảng thì bắt buộc điền trường nào | — | Chuẩn để tính *độ hoàn thiện metadata* |
| 🟦 | **3.1** Thư viện luật | Khai **mẫu** 28 loại kiểm tra chất lượng, dùng lại cho mọi bảng | — | Danh sách chọn khi gán luật ở 3.2, 4.2 |
| 🟦 | **5.1** Người dùng & Nhóm | Tài khoản, nhóm, **5 vai trò**, quyền vào menu | đồng bộ AD | ⭐ Mọi ô chọn người trên toàn hệ thống |
| 🟦 | **8.2** Cấu hình hệ thống | Kết nối nguồn · định nghĩa Tier · chuẩn đặt tên · tham số chung | — | Toàn hệ thống |
| 🟩 | **1.2** Bảng dữ liệu ⭐ | **Trung tâm của cả tool.** Khai bảng, khai cột, gắn thuật ngữ, gắn nhãn. Chi tiết có 6 tab | 1.3 · 1.7 · 5.1 · 8.2 | ⭐ **Nuôi toàn bộ**: 3.x · 4.x · 5.2 · 2.3 · 1.5 |
| 🟨 | **1.4** Kênh trao đổi | Khai đường dữ liệu đi giữa hai hệ thống — cả **vào và ra** | 1.3 | Mắt xích đầu của chuỗi truy vết 2.3 |
| 🟨 | **1.5** Báo cáo & Chỉ tiêu | Khai báo cáo, chỉ tiêu, công thức tính | 1.2 | Mắt xích cuối của truy vết 2.3 |
| 🟨 | **1.6** Nhóm bảng | Gom bảng thành gói để cấp quyền một lần cho cả gói | 1.2 | Phạm vi *Nhóm bảng* ở 5.2 |
| 🟨 | **2.1** Từ điển nghiệp vụ | Thống nhất cách hiểu khái niệm, đánh cờ **CDE** cho dữ liệu trọng yếu | 5.1 | Ô *Thuật ngữ* ở tab Cột · CDE bắt buộc có luật ở 3.2 |
| 🟨 | **2.2** Phân loại & Nhãn | Đánh dấu cột nhạy cảm *(số ĐT, CCCD)* và mức mật của bảng | 1.2 | ⭐ **Tự sinh chính sách che** ở 5.2 |
| 🟨 | **3.2** Luật & Kết quả | **Gán** luật vào bảng/cột, đặt ngưỡng, chọn hành động khi hỏng | 1.2 · 3.1 | Điểm chất lượng · sinh sự cố 3.4 |
| 🟨 | **3.5** Cảnh báo | Khai ai nhận thông báo gì, qua kênh nào | 1.2 · 1.7 | Gửi tới đầu mối |
| 🟨 | **4.1** Luồng xử lý (Job) | Khai job, bảng đích, giờ cam kết, **công tắc quét nguồn gốc** | 1.2 | ⭐ **Tự sinh quan hệ luồng dữ liệu** |
| 🟨 | **4.2** Cửa nạp dữ liệu | Khai mẫu nạp và **luật kiểm tại cửa** — chặn dữ liệu xấu trước khi ghi | 1.4 · 3.1 | Vùng chờ giữ lô lỗi |
| 🟨 | **5.2** Chính sách truy cập | Ai đọc được **dòng nào, cột nào** — gồm che dữ liệu và lọc theo dòng | 1.2 · 2.2 · 5.1 | Quyết định cho/chặn ở cổng truy vấn |
| 🟨 | **6.1** Chính sách dữ liệu | Số hoá **quy định** *(NĐ13, quy chế nội bộ)* và gắn vào nhóm dữ liệu | — | Mỗi yêu cầu thành một mục kiểm ở 6.3 |
| 🟨 | **6.2** Vòng đời & Lưu trữ | Dữ liệu giữ bao lâu, khi nào xoá, ai được chia sẻ ra ngoài | 1.2 · 6.1 | Job dọn dữ liệu đọc quy tắc này |
| 🟨 | **7.1** Mô hình dữ liệu chủ | Định nghĩa *"một Khách hàng chuẩn gồm trường gì"*, khoá so khớp | 1.2 | Cơ sở tính điểm trùng ở 7.3 |
| 🟪 | **2.4** Phê duyệt & Phiên bản | Hộp thư *"chờ tôi duyệt"* — duyệt / trả về hồ sơ metadata | 5.1 | Trạng thái phê duyệt mọi đối tượng |
| 🟪 | **3.4** Sự cố chất lượng | Phiếu **tự sinh khi luật hỏng**, tự gán người, có hạn xử lý | 3.2 · 1.2 | Chỉ số sự cố ở 8.1 |
| 🟪 | **5.3** Yêu cầu cấp quyền | Xin quyền → người phụ trách duyệt → quyền **có thời hạn** | 5.1 · 1.2 | ⭐ Sinh chính sách ở 5.2 **kèm lý do cấp** |
| 🟪 | **6.3** Đánh giá tuân thủ | Chạy kỳ đánh giá, phần lớn mục kiểm **máy tự chấm**, ghi việc khắc phục | 6.1 · 5.4 | Điểm tuân thủ ở 8.1 |
| 🟪 | **7.3** Nghi ngờ trùng | Máy gợi ý cặp trùng, **người quyết định** gộp hay không | 7.1 · 7.2 | Bản ghi chuẩn ở 7.4 |
| ⬜ | **1.1** Tìm kiếm toàn hệ thống | Gõ từ khoá tìm mọi loại đối tượng | — | *(chỉ đọc)* |
| ⬜ | **2.3** Truy vết luồng dữ liệu | Bản đồ toàn cảnh dữ liệu chạy từ đâu tới đâu | 4.1 · 4.2 | Chỉ số độ phủ truy vết ở 8.1 |
| ⬜ | **3.3** Phân tích dữ liệu | Kết quả **đo** cột: tỷ lệ rỗng, số giá trị phân biệt *(không phán đạt/không đạt)* | 1.2 | Gợi ý nên gán luật gì ở 3.2 |
| ⬜ | **4.3** Theo dõi & Pipeline | Sơ đồ job → bảng, phủ badge chất lượng, xem nút nào đang hỏng | 4.1 · 4.2 | *(chỉ đọc)* |
| ⬜ | **5.4** Nhật ký kiểm toán | Ai truy cập gì, lúc nào, **chính sách nào quyết định** | — | Bằng chứng cho 6.3 |
| ⬜ | **5.5** Báo cáo quyền & Giám sát | Một người đang có quyền gì · quyền nào không dùng · truy cập bất thường | 5.2 · 5.4 | Đề xuất thu hồi quyền |
| ⬜ | **7.2** Bản ghi nguồn | Xem cùng một khách hàng đang nằm ở những hệ thống nào | 7.1 | Đầu vào cho so khớp 7.3 |
| ⬜ | **7.4** Bản ghi chuẩn & Phân phối | Xem bản ghi đúng duy nhất và theo dõi phát ngược cho hệ thống khác | 7.3 | ⭐ Mã chuẩn mọi hệ thống phải dùng |
| ⬜ | **8.1** Sức khoẻ dữ liệu | Màn cho lãnh đạo — 10 chỉ số quản trị, tiến độ 5 giai đoạn | tất cả | *(chỉ đọc)* |

</details>

---

## Đơn giản hoá được gì

<details open>
<summary><b>⚠️ Gộp được 9 menu — 35 xuống 26, không mất tính năng nào</b></summary>

**Căn cứ:** nguyên tắc **NT7** do chính tài liệu đề xuất đặt ra —
> *"menu = một thực thể được QUẢN LÝ; thứ chỉ để xem là tab"*

Trong 35 menu hiện có **9 menu vi phạm nguyên tắc này** — chúng không quản lý thực thể nào, chỉ xem hoặc tra cứu.

| # | Bỏ menu | Chuyển thành | Vì sao gộp được | Rủi ro |
|:---:|---|---|---|:---:|
| 1 | **1.1** Tìm kiếm | **Thanh tìm kiếm trên đầu trang**, hiện ở mọi màn | Tìm kiếm không quản lý gì. Để thành menu còn **bất tiện hơn** — phải rời màn đang xem mới tìm được | Không |
| 2 | **1.4** Kênh trao đổi | **Tab** trong 1.3 Hệ thống | Kênh là **quan hệ giữa hai hệ thống** — thuộc về hệ thống, không đứng riêng | Thấp |
| 3 | **1.6** Nhóm bảng | Nút *Tạo nhóm* trong 1.2 + phạm vi ở 5.2 | Nhóm bảng chỉ tồn tại để cấp quyền theo gói. Chọn nhiều bảng ở 1.2 rồi bấm gộp là xong | Thấp |
| 4 | **2.5** Tiêu chuẩn thông tin mô tả | **Tab** trong 8.2 Cấu hình | Đây là **bộ chuẩn cấu hình**, chỉ tra cứu, không khai gì | Không |
| 5 | **3.3** Phân tích dữ liệu | **Tab Cột** của 1.2 *(vốn đã hiển thị các chỉ số này)* | Chỉ số đo của cột thuộc về cột. Hiện đang **hiện ở cả hai nơi** | Thấp |
| 6 | **5.5** Báo cáo quyền | **Tab** trong 5.2 Chính sách truy cập | Chỉ đọc lại dữ liệu của 5.2 và 5.4 theo góc nhìn *"theo người"* | Thấp |
| 7 | **6.2** Vòng đời & Lưu trữ | **Tab** trong 6.1 Chính sách dữ liệu | Vòng đời **chính là một loại chính sách**, và luôn phải viện dẫn 6.1 làm căn cứ | Trung bình |
| 8–9 | **7.2** Bản ghi nguồn · **7.4** Bản ghi chuẩn | **Tab** trong một menu *Dữ liệu chủ* cùng 7.3 | Ba menu này là **ba trạng thái của cùng một bản ghi** — nguồn → nghi ngờ → chuẩn | Thấp |

**Kiến trúc sau khi gộp — 8 module · 26 menu**

| Module | Trước | Sau | Còn lại |
|---|:---:|:---:|---|
| ① Data Catalog | 8 | **5** | Bảng dữ liệu · Hệ thống *(+tab Kênh)* · Báo cáo & Chỉ tiêu · Miền · Danh mục tham chiếu |
| ② Governance | 5 | **4** | Từ điển · Phân loại & Nhãn · Truy vết · Phê duyệt |
| ③ Data Quality | 5 | **4** | Thư viện luật · Luật & Kết quả · Sự cố · Cảnh báo |
| ④ Nạp & Điều phối | 3 | **3** | *(giữ nguyên)* |
| ⑤ Data Security | 5 | **4** | Người dùng · Chính sách truy cập *(+tab Báo cáo quyền)* · Yêu cầu quyền · Nhật ký |
| ⑥ Chính sách & Tuân thủ | 3 | **2** | Chính sách dữ liệu *(+tab Vòng đời)* · Đánh giá tuân thủ |
| ⑦ Dữ liệu chủ | 4 | **2** | Mô hình · Dữ liệu chủ *(3 tab)* |
| ⑧ Operations | 2 | **2** | *(giữ nguyên)* |
| | **35** | **26** | |

> ⭐ **Không menu nào bị bỏ chức năng.** Toàn bộ 9 menu trên vẫn còn nguyên nội dung — chỉ đổi chỗ đứng từ *mục trên thanh điều hướng* thành *tab bên trong menu cha*.
>
> Lợi ích: thanh điều hướng ngắn hơn **26%**, và mỗi menu còn lại đều trả lời được câu *"tôi quản lý thực thể gì ở đây"*.

**Một điểm cần bạn quyết**

> Mục **7** *(gộp Vòng đời vào Chính sách dữ liệu)* có rủi ro trung bình: menu 6.2 có **hàng chờ riêng** *(dữ liệu đến hạn xoá trong 30 ngày)*. Hàng chờ nằm trong tab thì dễ bị bỏ quên.
>
> ✅ **ĐÃ CHỐT: giữ 6.2 riêng — kiến trúc cuối cùng là 27 menu.** Việc xoá dữ liệu quá hạn là nghĩa vụ pháp lý, hàng chờ của nó không nên giấu trong tab.
>
> Bảng 27 menu đầy đủ và bảng ánh xạ cũ → mới nằm ở [**DMP-Kien-truc-CHOT.md**](DMP-Kien-truc-CHOT.md).

</details>

<details open>
<summary><b>✅ Ba chỗ TRÔNG như trùng nhưng KHÔNG gộp — giữ nguyên</b></summary>

| Nhóm | Các màn | Vì sao không gộp |
|---|---|---|
| **Ba màn cùng vẽ sơ đồ luồng dữ liệu** | Tab *Nguồn gốc* của 1.2 · **2.3** Truy vết · **4.3** Pipeline | Cùng dữ liệu nhưng **ba câu hỏi khác nhau**: *"bảng này lấy từ đâu"* · *"toàn hệ thống phủ được bao nhiêu"* · *"ca trực này có gì đang hỏng"*. Gộp lại thì mỗi nhóm người phải lọc bỏ 2/3 thông tin |
| **Hai màn cùng hiện chất lượng** | Tab *Chất lượng* của 1.2 · **3.2** Luật & Kết quả | Một cái hỏi về **một bảng**, một cái hỏi về **toàn hệ thống** |
| **Ba màn cùng hiện nhật ký** | Tab *Lịch sử* của 1.2 · **5.4** Nhật ký · **2.4** Phê duyệt | Ghi ba loại việc khác nhau: đổi metadata · truy cập dữ liệu · phê duyệt |

</details>

---

## Tài liệu nào còn dùng được

<details open>
<summary><b>Tình trạng 5 tài liệu DMP — cái nào đã cũ</b></summary>

| Tài liệu | Tình trạng | Nên làm gì |
|---|:---:|---|
| **DMP-Kien-truc-CHOT.md** | ✅ **Nguồn sự thật** | ⭐ Đọc đầu tiên — 27 menu + ánh xạ cũ→mới |
| **Tổng quan một trang** *(trang này)* | ✅ Còn dùng | Bảng 5 nhóm vai trò, giúp hiểu luồng |
| **DMP-Viec-can-sua-Demo.md** | ✅ Mới | Đặc tả sửa demo về 27 menu |
| `DMP-Ra-soat-Logic-Luong-va-Trung-lap.md` | ✅ Còn đúng | Đọc khi cần biết vì sao một thiết kế được chọn |
| `DMP-Review-Doi-chieu-Yeu-cau-BDA.md` | ✅ Còn đúng | Đọc khi cần đối chiếu với yêu cầu BDA |
| `DMP-Huong-dan-su-dung-Walkthrough.md` | ⚠️ Đúng nội dung nhưng **khó theo** | Bạn đã phản ánh: *nhảy từ màn này sang màn khác*. Nên viết lại theo **một kịch bản liền mạch** thay vì đi theo menu |
| `DMP-De-xuat-tool-Data-Management.md` | 🔴 **Đã cũ** | Thân bài vẫn mô tả **21 menu / 55 màn**, chỉ có mục 4B–4C nói về 35 menu. **Số liệu vênh nhau** *(34 vs 35 menu · 96 vs 98 màn)* |
| `DMP-Plan-Dung-Demo-FE.md` | 🔴 **Đã cũ** | Viết cho 21 menu / 55 màn, trong khi demo thật đã là 35 menu / 98 màn |

**Ba việc đề xuất — theo thứ tự ưu tiên**

| # | Việc | Vì sao |
|:---:|---|---|
| **1** | **Chốt số menu**: 35 · 26 · hay 27 | Mọi tài liệu khác phải sửa theo con số này — làm sau sẽ phải sửa hai lần |
| **2** | **Viết lại thân bài tài liệu đề xuất** theo con số đã chốt | Hiện thân bài và phần cập nhật **mâu thuẫn nhau**, người đọc không biết tin cái nào |
| **3** | **Viết lại walkthrough theo một kịch bản liền mạch** | Ví dụ: *"nhận một bảng mới từ đối tác — đi từ khai hệ thống tới lúc báo cáo chạy được"*, đi qua các menu theo đúng trình tự công việc thật |

</details>
