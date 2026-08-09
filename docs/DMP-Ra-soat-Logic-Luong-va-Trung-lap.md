# Rà soát logic, luồng dữ liệu và trùng lặp chức năng — DMP 8 module · 35 menu

### Đợt rà soát thứ hai, sau khi dựng xong demo

| | |
|---|---|
| **Mục đích** | Trả lời bốn câu: ① Báo cáo có phải chỉ là bảng output không · ② Mọi trường có truy được nguồn gốc không · ③ Giao diện đã đúng thực tế chưa · ④ Có menu nào trùng chức năng không |
| **Phạm vi** | 8 module · **35 menu** *(thêm menu 2.5 sau đợt rà soát này)* · 98 màn hình · 103 trường thông tin · 32 danh sách giá trị chọn |
| **Ngày** | 09/08/2026 |
| **Kết luận ngắn** | Tìm thấy **4 chỗ trùng lặp thật**, **3 chỗ trùng bề ngoài nhưng khác bản chất — giữ nguyên**, và **1 lỗ hổng nghiêm trọng về nguồn gốc trường thông tin** đã được xử lý bằng menu mới **2.5 Tiêu chuẩn thông tin mô tả** |

---

## 1. Báo cáo có phải chỉ là một bảng output không?

<details open>
<summary><b>Câu trả lời: đúng một nửa — và nửa còn lại quyết định thiết kế</b></summary>

**Nửa đúng.** Phần lớn báo cáo trong bối cảnh SQLWF thực chất đọc số liệu từ một **bảng kết quả đã tổng hợp sẵn**,
thường nằm ở vùng `mart` hoặc `bi`. Ví dụ:

| Báo cáo | Bảng kết quả đầu ra | Vùng |
|---|---|---|
| BC-001 Báo cáo doanh thu ngày | `mart.doanh_thu_ngay` | mart |
| BC-004 Báo cáo đối soát đối tác | `bi.doi_soat_giao_dich_A` | bi |
| BC-007 Báo cáo đối soát tháng | `mart.doi_soat_thang` | mart |
| BC-008 Báo cáo chi phí vận hành | `fin.chi_phi_van_hanh` | fin |

**Đã xử lý trong demo:**
- Thêm trường **`Bảng kết quả đầu ra`** cho báo cáo — tách bạch với **`Bảng nguồn`** *(bảng dùng để **tính**)*.
- Bảng nào được ít nhất một báo cáo khai là bảng kết quả thì tự động mang nhãn **`bảng báo cáo`** ở menu 1.2.
  Nhãn này **không khai tay** — nó suy ra từ khai báo phía báo cáo, nên không bao giờ lệch.

**Nửa còn lại — vì sao vẫn phải tách báo cáo thành đối tượng riêng.**
Báo cáo có **8 nhóm thông tin mà bảng không có chỗ để lưu**, và GĐ2 mục 5.5 liệt kê đủ cả 8:

| # | Thông tin của báo cáo | Bảng có lưu được không |
|:---:|---|:---:|
| 1 | Mục đích sử dụng · đơn vị sở hữu | ❌ |
| 2 | Danh sách chỉ tiêu thể hiện trong báo cáo | ❌ |
| 3 | Định nghĩa và công thức tính từng chỉ tiêu | ❌ |
| 4 | Điều kiện lấy dữ liệu và quy tắc tổng hợp | ❌ |
| 5 | Hình thức đầu ra *(màn hình / bảng dữ liệu / file)* | ❌ |
| 6 | Thời gian dữ liệu cam kết sẵn sàng | ⚠️ bảng có chu kỳ cập nhật, nhưng **cam kết của báo cáo khác cam kết của bảng** |
| 7 | Đối tượng và đơn vị sử dụng báo cáo | ❌ |
| 8 | Lượt xem thực tế | ❌ |

Thêm nữa, **không phải báo cáo nào cũng có bảng kết quả**. `BC-005` và `BC-016` dùng công cụ BI truy vấn thẳng
nhiều bảng nguồn và tính tại chỗ — không ghi ra bảng trung gian nào. Với những báo cáo này:
- Không gán được luật chất lượng lên kết quả cuối
- Quan hệ luồng dữ liệu tới báo cáo **phải khai thủ công** ở menu 2.3 vì công cụ BI không xuất được lineage

> ✅ **Quyết định giữ nguyên:** Báo cáo là **đối tượng riêng**, có liên kết hai chiều với bảng
> *(bảng kết quả đầu ra · bảng nguồn)*. Không gộp vào bảng.

</details>

---

## 2. Nguồn gốc trường thông tin — lỗ hổng nghiêm trọng đã xử lý

<details open>
<summary><b>Vấn đề: trường trông đầy đủ nhưng không giải thích được nguồn gốc</b></summary>

**Lỗi trước đây.** Giao diện có rất nhiều trường và nhiều ô chọn, nhưng khi bị hỏi
*"trường này ở đâu ra, giá trị trong danh sách chọn ai quản lý"* thì không có chỗ nào trả lời được.
Cụ thể có ba kiểu sai:

| Kiểu sai | Ví dụ trước khi sửa | Vì sao sai |
|---|---|---|
| **Danh sách chọn viết cứng trong màn** | Ô *Đơn vị quản lý* liệt kê thẳng 8 tên ban trong mã nguồn màn 1.3 | Thêm một ban mới thì phải sửa mã. Hai màn khác nhau có thể liệt kê hai danh sách lệch nhau |
| **Tên người viết cứng** | Ô *Đầu mối kỹ thuật* liệt kê thẳng `Trần Văn Hùng`, `Đỗ Quang Vinh` | Người nghỉ việc vẫn hiện ra để chọn. Không lọc được theo vai trò |
| **Trường không nói được dùng ở đâu** | Nhiều trường khai xong không biết menu nào tiêu thụ | Đúng vấn đề *"khai rồi để đó"* mà chính tài liệu đề xuất đã nêu ở V2 |

</details>

<details open>
<summary><b>Cách xử lý — ba lớp</b></summary>

**Lớp 1 — Từ điển trường thông tin.** Xây `src/data/fieldMeta.ts` mô tả **103 trường**, mỗi trường có:

| Thuộc tính | Nội dung |
|---|---|
| `origin` | Cách có giá trị: khai tay · chọn từ danh mục · thu thập tự động · hệ thống tự tính · sinh từ quy trình · hằng số |
| `from` | Nguồn cụ thể — tên menu khai báo, tên hệ thống thu thập, hoặc **công thức tính** |
| `values` | Nếu là danh sách chọn: giá trị hợp lệ lấy từ đâu |
| `uses[]` | **Danh sách menu tiêu thụ trường này, kèm mô tả dùng để làm gì** |

**Lớp 2 — Dấu ⓘ trên giao diện.** Trỏ chuột vào bất kỳ nhãn cột hoặc nhãn trường nào có dấu ⓘ sẽ hiện thẻ hai chiều:
```
← Giá trị này từ đâu ra      → Khai xong thì dùng ở đâu (n)
```
Đã gắn vào **đầu cột các bảng danh sách** và **nhãn trường trong các form khai báo chính**.

**Lớp 3 — Menu 2.5 Tiêu chuẩn thông tin mô tả.** Màn tra cứu toàn bộ 103 trường, lọc theo nhóm đối tượng
và theo cách có giá trị; kèm tab **Danh sách giá trị chọn** liệt kê **32 danh sách** với người quản lý và nơi thêm giá trị.

> 💡 Menu này không phải phát minh thêm — GĐ1 mục 2.4 ghi rõ **"Bộ tiêu chuẩn thông tin mô tả dữ liệu"**
> là một trong **4 kết quả đầu ra bắt buộc** của Giai đoạn 1. Trước đợt rà soát này, kết quả đó không có chỗ nào trong tool.

</details>

<details open>
<summary><b>Kết quả rà soát 32 danh sách giá trị chọn</b></summary>

| Loại nguồn | Số danh sách | Nghĩa là gì | Ví dụ |
|---|:---:|---|---|
| **Danh mục quản lý được** | 8 | Người dùng thêm/sửa được ở một menu cụ thể | Đơn vị tổ chức *(menu 7.1)* · Miền dữ liệu *(1.7)* · Hệ thống *(1.3)* · Nhãn *(2.2)* · Danh mục tham chiếu *(1.8)* · Người dùng *(5.1)* |
| **Hằng số nghiệp vụ** | 24 | Cố định theo yêu cầu BDA hoặc quy định pháp lý, sửa phải đổi cấu hình | 4 mức phân loại *(GĐ4 §3)* · 5 vai trò *(GĐ1 §2.3)* · 6 chiều chất lượng *(GĐ3 §3)* · 5 trạng thái phê duyệt *(GĐ2 §8.1)* |
| **Suy từ dữ liệu** | 0 | — | *(mọi danh sách đều thuộc hai loại trên)* |

**Ba thay đổi cụ thể trong mã nguồn:**

| Trước | Sau |
|---|---|
| Mỗi màn tự liệt kê danh sách đơn vị | Dùng chung `ORG_UNITS` — nguồn ghi rõ là mô hình dữ liệu chủ MDM-DV, đồng bộ từ hệ thống nhân sự |
| Ô chọn người viết cứng tên | `usersByRole('Đầu mối kỹ thuật')` — **tự lọc theo vai trò và loại người đã nghỉ việc** |
| Ô chọn thuật ngữ liệt kê 3 mã cứng | Lấy từ từ điển, **chỉ thuật ngữ đã phê duyệt** |

**Chỉ số nghiệm thu:** 103/103 trường có nguồn gốc rõ ràng · **0 trường không có nơi sử dụng**.

</details>

---

## 3. Rà soát giao diện các màn danh sách

<details open>
<summary><b>Bốn lỗi giao diện đã sửa</b></summary>

| # | Lỗi | Cách sửa |
|:---:|---|---|
| **1** | **Không có số thứ tự bản ghi** — người xem không đếm được, không trỏ được "dòng thứ mấy" khi trao đổi | Thêm cột **`#`** cho toàn bộ **21 bảng danh sách** |
| **2** | **Cột quá hẹp, chữ bị bóp** — rõ nhất ở menu 1.3, cột *Hệ thống* chỉ còn ~120px trong khi tên dài | Đặt **chiều rộng tối thiểu** cho từng cột. Mặc định 128px cho cột chữ, 96px cho cột số. Cột chính đặt riêng 280–300px |
| **3** | **Quá nhiều cột** — menu 1.3 có 12 cột, menu 4.1 có 12 cột trên bề ngang 1330px | **Gộp cột liên quan thành ô hai dòng.** Menu 1.3: 12 → 8 cột · menu 1.2: 11 → 8 cột · menu 4.1: 12 → 8 cột |
| **4** | **Nhiều khoảng trắng thừa** ở sơ đồ nguồn gốc do tính chiều cao theo số nút lớn nhất | Tính lại khoảng cách nút theo từng cột nguồn/đích riêng, thu gọn chiều cao nút |

**Cách gộp cột — nguyên tắc áp dụng chung**

| Menu | Cột gộp | Thành |
|---|---|---|
| 1.2 Bảng dữ liệu | Hệ thống + Miền | Một ô: tên hệ thống trên, chip miền dưới |
| 1.2 Bảng dữ liệu | BDA + DE | Một ô: BDA trên, DE dưới |
| 1.2 Bảng dữ liệu | Số dòng + Độ tươi | Một ô: số dòng trên, độ tươi dưới |
| 1.2 Bảng dữ liệu | Điểm chất lượng + Số luật | Một ô: điểm to, số luật nhỏ |
| 1.3 Hệ thống | Loại + Công nghệ · Đơn vị + Môi trường · Người sở hữu + Đầu mối KT · Trạng thái + Phê duyệt | Bốn ô hai dòng |
| 4.1 Job | Lịch chạy + Giờ cam kết · Kết quả + Thời gian chạy · Số bước + Trạng thái lineage | Ba ô hai dòng |

> 💡 Ô hai dòng vừa **giảm số cột**, vừa **giữ nguyên lượng thông tin**, vừa đặt hai giá trị liên quan cạnh nhau
> để người xem so sánh được ngay — ví dụ *"lịch chạy 06:00 nhưng cam kết 07:00"* nằm cùng một ô.

</details>

---

## 4. Rà soát trùng lặp chức năng giữa các menu

<details open>
<summary><b>⚠️ Bốn chỗ trùng lặp THẬT — đã xử lý</b></summary>

### T1 — Ngưỡng chất lượng khai ở hai nơi

| Nơi | Trước |
|---|---|
| Menu 3.1 Thư viện luật | Trường *Ngưỡng mặc định* của từng loại kiểm tra |
| Menu 8.2 Cấu hình hệ thống | Tham số `nguong_canh_bao_mac_dinh` và `nguong_nghiem_trong_mac_dinh` |

**Vấn đề:** hai nơi cùng khai ngưỡng "mặc định", không rõ cái nào thắng.

**Đã xử lý — làm rõ thành chuỗi 4 cấp có thứ tự ưu tiên tường minh:**

```
① Ngưỡng khai ở lần gán luật    (menu 3.2)  ← ưu tiên cao nhất
② Ngưỡng của bảng theo Tier     (menu 8.2 — định nghĩa Tier)
③ Ngưỡng mặc định của loại luật (menu 3.1)
④ Tham số toàn cục              (menu 8.2)  ← chỉ dùng khi ③ chưa khai
```

Cột **Nguồn ngưỡng** trên menu 3.2 hiện rõ cấp nào đang áp dụng, và trường `rule.thresholdSource`
trong từ điển trường ghi đúng chuỗi ưu tiên này.

---

### T2 — "Người phụ trách" bị hiểu thành ba thứ khác nhau

Trước đây các menu dùng lẫn lộn ba khái niệm: *người sở hữu · đầu mối nghiệp vụ · đầu mối kỹ thuật*.

**Đã xử lý:** chuẩn hoá theo đúng **5 vai trò của GĐ1 mục 2.3**, và mỗi vai trò có **trách nhiệm không chồng nhau**:

| Vai trò | Quyết định gì | Không làm gì |
|---|---|---|
| **Người sở hữu dữ liệu** | Phê duyệt định nghĩa · phê duyệt cấp quyền | Không cập nhật nội dung |
| **Đầu mối nghiệp vụ** | Cập nhật mô tả, thuật ngữ, quy tắc · nhận sự cố nghiệp vụ | Không phê duyệt |
| **Đầu mối kỹ thuật** | Cập nhật cấu trúc, nguồn, job · nhận sự cố kỹ thuật | Không phê duyệt |
| **Đơn vị vận hành** | Quản người dùng, kết nối, thu hồi quyền | Không quyết định nội dung dữ liệu |
| **Người sử dụng** | Tra cứu, xin quyền, phản hồi | Không sửa gì |

Ô chọn người ở mọi form nay **tự lọc theo vai trò** — chọn Người sở hữu dữ liệu thì chỉ hiện người có vai trò đó.

---

### T3 — Kênh trao đổi dữ liệu ↔ Cửa nạp dữ liệu

**Nghi ngờ:** menu 1.4 và menu 4.2 nghe như cùng một thứ.

**Kết luận: KHÔNG trùng — nhưng phải nói rõ ranh giới.**

| | 1.4 Kênh trao đổi dữ liệu | 4.2 Cửa nạp dữ liệu |
|---|---|---|
| **Là gì** | **Đối tượng metadata** — mô tả đường ống tồn tại giữa hai hệ thống | **Cấu hình vận hành** — mẫu nạp cụ thể chạy theo lịch |
| **Trả lời câu hỏi** | *"Hệ thống nào trao đổi dữ liệu gì với hệ thống nào, xác thực ra sao"* | *"Lô dữ liệu này nạp vào bảng nào, kiểm luật gì trước khi cho vào"* |
| **Chiều** | Cả **gửi đi** và nhận về | Chủ yếu **nhận về** |
| **Ai khai** | Đầu mối kỹ thuật, một lần khi thiết lập kết nối | Người vận hành, mỗi khi có luồng nạp mới |
| **Thuộc nhóm nào của GĐ2** | Nhóm đối tượng số 4 — bắt buộc quản lý | Không thuộc 7 nhóm, là chức năng vận hành |

**Quan hệ:** mỗi mẫu nạp ở 4.2 **bắt buộc trỏ về một kênh** ở 1.4. Không cho khai nguồn tự do bằng chữ.
Nhờ vậy lineage nối được từ kênh → bảng thô mà không đứt.

---

### T4 — Bảng đích của job ↔ Bảng trong danh mục

**Vấn đề:** 214 job ghi vào bảng chưa có trong danh mục — tức là hệ thống có hai "danh sách bảng" không khớp nhau.

**Đã xử lý:** ràng buộc **RB2** — ô *Bảng đích* ở menu 4.1 chỉ chọn được từ danh mục bảng, không gõ tự do.
Job có bảng đích ngoài danh mục bị đánh dấu đỏ và không lưu được phiên bản mới.

</details>

<details open>
<summary><b>✅ Ba chỗ trùng BỀ NGOÀI nhưng khác bản chất — giữ nguyên</b></summary>

### K1 — Ba màn cùng hiện "quan hệ luồng dữ liệu"

| Màn | Góc nhìn | Người dùng điển hình |
|---|---|---|
| **Tab Nguồn gốc** trong chi tiết bảng *(1.2)* | Xuất phát từ **một bảng cụ thể** — lên nguồn, xuống đích | Người đang xử lý sự cố trên bảng đó |
| **Menu 2.3 Truy vết luồng dữ liệu** | **Bản đồ toàn cảnh** theo 4 mức, và **khai báo thủ công** | Người quản trị dữ liệu rà soát độ phủ |
| **Menu 4.3 Theo dõi & Pipeline** | Góc nhìn **theo job và theo lần chạy**, phủ badge chất lượng | Người vận hành theo dõi ca trực |

> Cùng dữ liệu gốc nhưng **ba câu hỏi khác nhau**. Gộp lại sẽ làm mỗi nhóm người dùng phải lọc bỏ 2/3 thông tin không cần.

### K2 — Hai màn cùng hiện "chất lượng của bảng"

- **Tab Chất lượng** trong chi tiết bảng: *"bảng NÀY có luật gì, đang đạt không"*
- **Menu 3.2 Luật & Kết quả**: *"toàn hệ thống có luật gì, cái nào đang hỏng"*

Một cái hỏi về **một bảng**, một cái hỏi về **nhiều bảng** — đúng nguyên tắc NT7 mà tài liệu đề xuất đặt ra.

### K3 — Ba màn cùng hiện "nhật ký"

| Màn | Ghi gì | Dùng khi nào |
|---|---|---|
| **Tab Lịch sử** trong chi tiết bảng | Thay đổi metadata của bảng đó | Truy vì sao mô tả bảng bị đổi |
| **Menu 5.4 Nhật ký kiểm toán** | Mọi lượt truy cập dữ liệu toàn hệ thống | Trả lời kiểm toán |
| **Menu 2.4 Phê duyệt & Phiên bản** | Lịch sử phê duyệt và so sánh phiên bản | Truy ai duyệt thay đổi nào |

</details>

<details open>
<summary><b>Ba điểm logic khác đã kiểm và xác nhận đúng</b></summary>

| # | Điểm kiểm | Kết luận |
|:---:|---|---|
| **L1** | **Chuỗi khai báo có bị vòng tròn không** — bảng cần hệ thống, hệ thống cần đơn vị, đơn vị nằm ở MDM, MDM cần bảng? | ✅ Không vòng tròn. MDM ở Đợt 5 dùng danh mục đơn vị **đồng bộ từ hệ thống nhân sự**, không phụ thuộc ngược vào danh mục bảng |
| **L2** | **Sự cố có tự gán được người không khi bảng thiếu đầu mối** | ✅ Đúng thiết kế: để trống và cảnh báo, **không tự gán bừa cho người khác** — đây là hành vi mong muốn, thấy rõ ở sự cố SC-0229 |
| **L3** | **Che dữ liệu và hạn chế tải xuống có chồng nhau không** | ✅ Không: che viết theo **nhãn dữ liệu nhạy cảm** (trục 2), hạn chế tải xuống viết theo **mức phân loại** (trục 1). Hai trục độc lập, áp đồng thời |

</details>

---

## 5. Việc còn lại — nêu rõ để không ai hiểu nhầm là đã xong

<details open>
<summary><b>Bốn hạng mục chưa làm và lý do</b></summary>

| # | Chưa làm | Vì sao | Khi nào cần làm |
|:---:|---|---|---|
| 1 | Dấu ⓘ mới gắn cho **các bảng danh sách chính và form khai báo chính**, chưa phủ 100% ô trên mọi màn | Ưu tiên các màn hay bị hỏi nhất; hạ tầng đã có sẵn, gắn thêm chỉ là thêm một thuộc tính `info` | Khi dev thật — gắn nốt theo từ điển đã có |
| 2 | Từ điển mới có **103 trường**, chưa phải toàn bộ trường trên giao diện | 103 trường này phủ hết **7 nhóm đối tượng bắt buộc của GĐ2** và mọi trường có tranh cãi về nguồn gốc | Bổ sung dần khi phát sinh trường mới |
| 3 | Chưa có **phân trang** ở bảng danh sách | Dữ liệu minh hoạ chỉ 6–20 dòng mỗi bảng, thêm phân trang làm demo rối mà không chứng minh thêm điều gì | Bắt buộc khi lên dữ liệu thật 11.482 bảng |
| 4 | Chưa có **chỉnh cột hiển thị theo người dùng** | Không thuộc phạm vi demo | Nên có khi dev thật — mỗi vai trò quan tâm cột khác nhau |

</details>

---

<div align="center">

**HẾT BÁO CÁO RÀ SOÁT**

*Kết quả rà soát đã được áp thẳng vào demo — xem menu **2.5 Tiêu chuẩn thông tin mô tả** để tra nguồn gốc mọi trường*

</div>
