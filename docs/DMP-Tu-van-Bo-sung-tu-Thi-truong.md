# Tư vấn bổ sung tính năng — học từ công cụ thị trường

### 9 đề xuất thị trường · 5 tính năng AI · 9 tính năng đột phá · **12 đề xuất từ góc nhìn người dùng**

| | |
|---|---|
| **Ngày** | **11/08/2026** · cập nhật **13/08/2026** *(thêm phần 7 và 8)* |
| **Vấn đề cần giải** | Thiết kế hiện tại **bám sát yêu cầu BDA** *(GĐ1 → GĐ5)* nhưng **chưa có ý tưởng nào từ thị trường** — đọc lên giống bảng liệt kê yêu cầu, không giống đề xuất của người có nghiên cứu |
| **Phạm vi** | Chỉ đề xuất thứ **DMP chưa có**. Không nhắc lại thứ đã thiết kế |
| **Đọc cùng** | [Đặc tả chức năng](DMP-Dac-ta-Chuc-nang-v1.md) *(27 menu hiện có)* · [Nghiên cứu thị trường](SQLWF-Nghien-cuu-thi-truong-Demo-cong-cu.md) *(DataHub · OpenMetadata · Soda · Ranger)* |

> ⚠️ **Về nguồn:** phần lớn bài so sánh công cụ trên mạng **do chính hãng viết** *(Atlan, Alation, DQLabs…)*, nên các so sánh cạnh tranh phải đọc như tài liệu tiếp thị. Tôi chỉ lấy phần **mô tả tính năng và xu hướng chung** — thứ nhiều nguồn độc lập cùng nói — và ghi rõ nguồn ở cuối.

---

## 1. Cách tôi chọn đề xuất

<details open>
<summary><b>Bốn tiêu chí — không phải cái gì thị trường có cũng bê về</b></summary>

| # | Tiêu chí | Vì sao |
|:---:|---|---|
| **1** | **Giải một con số đang xấu trong chính tài liệu của mình** | Đề xuất phải chữa được bệnh có thật, không phải thêm cho oai |
| **2** | **Tận dụng thứ DMP đã có**, không đòi hạ tầng mới | Ví dụ đã có sơ đồ luồng dữ liệu thì tận dụng nó, đừng xây thêm |
| **3** | **Nhiều công cụ cùng làm** — không phải tính năng riêng của một hãng | Tránh chạy theo tiếp thị |
| **4** | **Nói được bằng ngôn ngữ nghiệp vụ trong một câu** | Không giải thích được cho lãnh đạo thì không đề xuất |

**Ba con số đang xấu nhất trong tài liệu hiện tại — đề xuất bám vào đây**

| Con số | Nghĩa là |
|---|---|
| **0,6%** bảng đang được kiểm chất lượng | Điểm chất lượng 87 gần như vô nghĩa |
| **7.578** bảng không có người phụ trách · **38%** chưa gán miền | Khai metadata thủ công **không bao giờ đuổi kịp** |
| **1.409/1.847** chính sách quyền không rõ căn cứ | Quản trị đang chạy sau thực tế |

</details>

---

## 2. Bảng tổng hợp chín đề xuất

<details open>
<summary><b>⭐ Xếp theo giá trị so với công sức — đọc bảng này là đủ</b></summary>

| # | Đề xuất | Chữa con số nào | Vào menu | Công sức | Giá trị |
|:---:|---|---|---|:---:|:---:|
| **1** | ⭐ **Giám sát tự động — không cần khai luật** | **0,6%** → phủ được toàn bộ bảng | 3.2 | Trung bình | 🔥🔥🔥 |
| **2** | **Cảnh báo thay đổi cấu trúc bảng** | Nguyên nhân hàng đầu gây hỏng ngầm | 1.1 · 3.2 | Thấp | 🔥🔥🔥 |
| **3** | ⭐ **Gom sự cố theo nguyên nhân gốc** | Chống ngập cảnh báo → giảm tỷ lệ báo động giả | 3.3 | Trung bình | 🔥🔥🔥 |
| **4** | **Lan trạng thái tin cậy theo luồng dữ liệu** | Báo cáo tự gắn cờ nghi ngờ | 2.3 · 4.3 | Thấp | 🔥🔥 |
| **5** | **Cam kết dữ liệu giữa bên cấp và bên dùng** | Chuyển từ *phát hiện sau* sang *thoả thuận trước* | menu mới | Cao | 🔥🔥 |
| **6** | **Gian hàng dữ liệu — xin quyền theo giỏ** | Rút ngắn thời gian từ *cần* tới *có* dữ liệu | 1.1 · 5.3 | Trung bình | 🔥🔥 |
| **7** | ⭐ **Máy tự viết mô tả, người duyệt** | **8.267** bảng thiếu mô tả *(72%)* | 1.1 · 2.4 | Trung bình | 🔥🔥🔥 |
| **8** | **Tìm kiếm bằng câu nói thường** | Người dùng không cần biết tên bảng | thanh tìm kiếm | Trung bình | 🔥🔥 |
| **9** | **Mở kho metadata cho trợ lý AI** | Hỏi về dữ liệu ngay trong công cụ đang làm việc | 8.2 | Thấp | 🔥🔥 |

**Nếu chỉ chọn ba** — tôi chọn **1 · 3 · 7**. Ba cái này chữa đúng ba con số xấu nhất, và cả ba đều **tận dụng thứ DMP đã có** chứ không đòi hạ tầng mới.

</details>

---

## 3. Chi tiết từng đề xuất

<details open>
<summary><b>⭐ 1 — Giám sát tự động, không cần khai luật</b></summary>

**Một câu:** *máy tự học nhịp bình thường của mỗi bảng rồi báo khi lệch, thay vì chờ người khai từng luật.*

**Vấn đề đang có**

DMP hiện chỉ kiểm được bảng nào **có người ngồi khai luật**. Kết quả: **64 / 11.482 bảng — 0,6%**. Với 11 nghìn bảng thì khai tay **không bao giờ đuổi kịp**, và điểm chất lượng 87 chỉ phản ánh phần rất nhỏ.

**Thị trường làm gì**

Các công cụ giám sát dữ liệu chia thành **năm nhóm tín hiệu** và **tự theo dõi cả năm mà không cần cấu hình**:

| Nhóm tín hiệu | Máy tự phát hiện gì |
|---|---|
| **Độ tươi** | Bảng lẽ ra cập nhật hằng ngày mà hôm nay chưa có dữ liệu |
| **Khối lượng** | Số dòng tụt bất thường — ví dụ lô mới ít hơn 50% so với trung bình 7 ngày, thường là nạp thiếu ở nguồn |
| **Cấu trúc** | Thêm cột, mất cột, đổi kiểu dữ liệu |
| **Phân bố** | Tỷ lệ rỗng, khoảng giá trị, số giá trị phân biệt đổi đột ngột |
| **Quan hệ luồng** | Nhánh phụ thuộc đứt |

Điểm quan trọng: **máy học theo mùa vụ** — biết cuối tháng số dòng tăng là bình thường, nên không báo động giả.

**Thêm vào DMP thế nào**

Menu **3.2** có thêm **chế độ thứ hai** bên cạnh luật khai tay:

| | Luật khai tay *(đang có)* | Giám sát tự động *(đề xuất)* |
|---|---|---|
| Ai bật | Người khai từng luật cho từng cột | **Bật một lần cho cả miền hoặc cả hệ thống** |
| Phủ được | 0,6% số bảng | **100% số bảng ngay từ ngày đầu** |
| Bắt được | Đúng thứ người nghĩ ra | Thứ **không ai nghĩ tới** |
| Không bắt được | — | Lỗi **logic nghiệp vụ** *(số đúng định dạng nhưng sai nghĩa)* |

> ⭐ **Hai thứ này bổ sung nhau, không thay thế nhau.** Giám sát tự động phủ rộng và bắt bất thường; luật khai tay đi sâu vào quy tắc nghiệp vụ. Bảng quan trọng thì dùng cả hai.
>
> 🔴 **Cảnh báo triển khai:** bật giám sát tự động cho 11 nghìn bảng ngay ngày đầu sẽ **ngập cảnh báo**. Phải chạy **chế độ chỉ quan sát ít nhất một tháng** để máy học nhịp, rồi mới bật gửi thông báo — và bật theo từng miền một.

</details>

<details open>
<summary><b>2 — Cảnh báo thay đổi cấu trúc bảng</b></summary>

**Một câu:** *ai đó thêm cột, đổi kiểu dữ liệu, hay bỏ cột — báo ngay cho những người đang dùng bảng đó.*

**Vấn đề đang có**

Đổi cấu trúc bảng là **nguyên nhân hàng đầu gây hỏng ngầm** — job vẫn chạy, không báo lỗi, nhưng số ra sai hoặc thiếu. DMP có tab *Lịch sử* ghi lại thay đổi, nhưng **chỉ ghi để tra sau**, không ai được báo lúc nó xảy ra.

**Thêm vào DMP thế nào**

Tận dụng thứ đã có: DMP **đã biết bảng nào nuôi job nào, job nào nuôi báo cáo nào** *(menu 2.3)*. Nên khi phát hiện đổi cấu trúc thì **biết chính xác ai cần được báo**:

```
Cột `so_tien` đổi từ DECIMAL sang VARCHAR
  → 3 job đang đọc cột này
  → 2 báo cáo hạ nguồn
  → gửi cho: DE của 3 job + BDA của 2 báo cáo
```

**Công sức thấp** vì ba mảnh đã có sẵn: nhật ký thay đổi *(1.1 tab Lịch sử)* · quan hệ luồng *(2.3)* · kênh gửi *(3.4)*. Chỉ cần nối lại.

</details>

<details open>
<summary><b>⭐ 3 — Gom sự cố theo nguyên nhân gốc</b></summary>

**Một câu:** *một bảng gốc hỏng làm 20 bảng hạ nguồn hỏng theo — gom thành MỘT sự cố có nguyên nhân, thay vì 20 phiếu rời rạc.*

**Vấn đề đang có**

Thiết kế hiện tại: mỗi luật hỏng sinh một phiếu. Nghe hợp lý, nhưng khi bảng gốc hỏng thì **hàng chục luật ở hạ nguồn cùng hỏng một lúc** → hộp thư ngập 20 phiếu, người xử lý không biết bắt đầu từ đâu, và **19 phiếu trong đó sẽ tự hết khi sửa xong phiếu gốc**.

Đây chính là cách **tỷ lệ báo động giả** leo lên trên 25% — ngưỡng mà tài liệu của mình đã cảnh báo là *"người dùng sẽ tắt thông báo và cả module thành vô dụng"*.

**Thị trường làm gì**

Xu hướng rõ nhất là chuyển **từ phát hiện sang phân loại và tìm nguyên nhân**. Công cụ cũ coi mỗi bất thường là một sự kiện độc lập; công cụ mới **dùng quan hệ luồng dữ liệu để nối các bất thường liên quan lại**, chỉ ra **một sự kiện gốc** đã gây ra chuỗi hỏng phía sau.

**Thêm vào DMP thế nào**

DMP **đã có đủ nguyên liệu** — sơ đồ luồng dữ liệu ở 2.3. Việc cần làm ở menu **3.3**:

| Trước | Sau |
|---|---|
| 20 phiếu ngang hàng | **1 phiếu gốc** + 19 phiếu con gắn vào nó |
| Ai cũng phải xử lý | Chỉ **DE của bảng gốc** phải xử lý |
| Đóng từng phiếu | Sửa xong bảng gốc → **19 phiếu con tự kiểm tra lại và tự đóng** |

> ⭐ Thêm một cột đơn giản mà rất giá trị: **"số thứ bị ảnh hưởng"** trên phiếu gốc — *"sự cố này đang làm 12 bảng và 4 báo cáo sai số"*. Đó là thứ giúp xếp thứ tự ưu tiên mà không cần bàn.

</details>

<details open>
<summary><b>4 — Lan trạng thái tin cậy theo luồng dữ liệu</b></summary>

**Một câu:** *bảng gốc đang có sự cố thì mọi bảng và báo cáo phía sau tự mang cờ "số liệu nghi ngờ", cho tới khi sự cố được đóng.*

**Vấn đề đang có**

Màn 4.3 đã vẽ badge chất lượng lên sơ đồ, nhưng **badge chỉ hiện trên đúng bảng bị lỗi**. Người mở báo cáo hạ nguồn **không biết số mình đang đọc bắt nguồn từ một bảng đang hỏng**.

**Thêm vào DMP thế nào**

Ba mức trạng thái, lan tự động theo luồng:

| Trạng thái | Nghĩa | Hiện ở đâu |
|---|---|---|
| ✅ Tin cậy | Luật đạt, dữ liệu đúng hạn | Bảng · báo cáo |
| ⚠️ **Nghi ngờ** | **Ăn dữ liệu từ nhánh đang có sự cố** | Lan xuống toàn bộ hạ nguồn |
| 🛑 Đang hỏng | Chính nó có luật hỏng | Bảng gốc |

Cờ **⚠️ nghi ngờ** hiện ở **1.1, 1.3, 2.3, 4.3 và 8.1** — nghĩa là người mở báo cáo cũng thấy, không chỉ người trực ca.

**Công sức thấp** vì chỉ là một phép duyệt trên đồ thị đã có, cộng thêm một cờ hiển thị.

</details>

<details open>
<summary><b>5 — Cam kết dữ liệu giữa bên cấp và bên dùng</b></summary>

**Một câu:** *bên cấp dữ liệu ký cam kết về cấu trúc, độ tươi và chất lượng; đổi mà vi phạm cam kết thì hệ thống chặn.*

**Vấn đề đang có**

Hiện DMP phát hiện lỗi **sau khi lỗi đã xảy ra**. Đội cấp dữ liệu đổi cấu trúc bảng mà không ai ngăn được — chỉ báo động sau khi hạ nguồn đã hỏng.

**Thị trường làm gì**

**Cam kết dữ liệu** *(data contract)* là thoả thuận có thể kiểm tra tự động giữa bên cấp và bên dùng, gồm: danh sách cột và kiểu · độ tươi cam kết · ngưỡng chất lượng · quy tắc được phép đổi gì. Đây là nền của mô hình *sản phẩm dữ liệu* đang phổ biến.

**Thêm vào DMP thế nào**

| Thành phần cam kết | DMP đã có gì |
|---|---|
| Cột và kiểu dữ liệu | ✅ tab Cột của 1.1 |
| Độ tươi cam kết | ✅ **giờ cam kết** ở 4.1 |
| Ngưỡng chất lượng | ✅ luật ở 3.2 |
| **Ai là bên dùng** | ⚠️ có một phần qua 1.3 và 2.3 |
| **Quy tắc đổi và cơ chế chặn** | ❌ **chưa có** |

> 💡 **Nhìn kỹ thì DMP đã có 3/5 mảnh.** Việc thật sự mới chỉ là **gói chúng thành một bản cam kết có phiên bản, và chặn khi vi phạm**. Nhưng đây là đề xuất **công sức cao nhất** vì đụng tới quy trình làm việc giữa các đội — nên tôi xếp sau nhóm 1 · 3 · 7.

</details>

<details open>
<summary><b>6 — Gian hàng dữ liệu, xin quyền theo giỏ</b></summary>

**Một câu:** *thay vì tra danh mục kỹ thuật rồi xin từng bảng, người dùng vào "gian hàng" chọn gói dữ liệu đã đóng gói sẵn và bấm xin cả giỏ.*

**Thị trường phân biệt hai thứ**

| | **Danh mục dữ liệu** | **Gian hàng dữ liệu** |
|---|---|---|
| Trả lời | *"Công ty có dữ liệu gì"* | *"Tôi dùng nó thế nào"* |
| Đối tượng | Bảng kỹ thuật, hàng nghìn cái | **Gói dữ liệu đã đóng sẵn**, vài chục |
| Người dùng | Người kỹ thuật | **Người nghiệp vụ** |
| Ví von | Kho hàng | **Cửa hàng** |

Cách xin quyền phổ biến là **giỏ hàng**: chọn nhiều thứ, bấm một lần, hệ thống tự chạy quy trình duyệt và cấp quyền.

**Thêm vào DMP thế nào**

DMP đã có 5.3 xin quyền — nhưng **xin từng bảng một**. Nâng cấp:

| Việc | Vào đâu |
|---|---|
| Đóng gói vài chục **gói dữ liệu** có mô tả nghiệp vụ, người sở hữu, dữ liệu mẫu | Tận dụng **nhóm bảng** đã có ở 1.1 |
| Chọn nhiều thứ rồi **xin một lần** | 5.3 |
| Người duyệt xử lý cả giỏ trong một màn | 5.3 |

> 💡 **Đây là đề xuất dễ gây ấn tượng khi trình bày** — nó biến tool từ *"công cụ của đội kỹ thuật"* thành *"chỗ người nghiệp vụ tự phục vụ"*. Nhưng phải nói thật: giá trị của nó phụ thuộc vào việc **có ai chịu ngồi đóng gói dữ liệu hay không**.

</details>

<details open>
<summary><b>⭐ 7 — Máy tự viết mô tả, người duyệt</b></summary>

**Một câu:** *máy đọc tên cột, dữ liệu mẫu và câu SQL của job rồi đề xuất mô tả; người phụ trách chỉ việc sửa và duyệt.*

**Vấn đề đang có — đây là con số xấu nhất**

**7.578 bảng không có người phụ trách · chỉ 28% có mô tả đủ nghĩa.** Cách duy nhất hiện nay là **ngồi gõ tay**, và với 11 nghìn bảng thì việc này **sẽ không bao giờ xong**.

**Thị trường làm gì**

Đây là tính năng phổ biến nhất trong nhóm "danh mục có AI": tự động gắn nhãn metadata, tự dựng quan hệ luồng, tự chấm chất lượng và **tự sinh mô tả** — để đội không phải viết tay mọi thứ.

**Thêm vào DMP thế nào**

Máy có sẵn ba nguồn để đoán, đều đã nằm trong DMP:

| Nguồn | Suy ra được gì |
|---|---|
| Tên bảng, tên cột | `ngay_giao_dich` → *"Ngày phát sinh giao dịch"* |
| **Câu SQL của job sinh ra bảng** *(4.1)* | Bảng được tính từ đâu, lọc điều kiện gì |
| Chỉ số đo của cột *(tab Cột)* | Kiểu giá trị, khoảng, tỷ lệ rỗng |

> 🔴 **Bắt buộc có người duyệt — không được ghi thẳng.** Mô tả máy viết vào thẳng danh mục thì sau vài tháng **không ai phân biệt được đâu là mô tả thật đâu là máy đoán**, và niềm tin vào danh mục sụp đổ.
>
> **Cách làm đúng:** máy đề xuất → vào hàng chờ ở **2.4** → người phụ trách sửa và duyệt → mới thành mô tả chính thức. Mô tả nào do máy đề xuất thì **ghi rõ nguồn gốc**.

**Đo hiệu quả thế nào:** tỷ lệ đề xuất được duyệt mà **không cần sửa**. Dưới 50% thì máy đang đoán tệ, tắt đi cho đỡ phiền.

</details>

<details open>
<summary><b>8 — Tìm kiếm bằng câu nói thường</b></summary>

**Một câu:** *gõ "doanh thu tháng trước theo chi nhánh" thay vì phải biết bảng tên là `mart.doanh_thu_thang`.*

**Vấn đề đang có**

Thanh tìm kiếm hiện khớp theo **từ khoá**. Người nghiệp vụ **không biết tên bảng**, và đó chính là lý do họ đi hỏi đội kỹ thuật thay vì tự tra.

**Thêm vào DMP thế nào**

DMP có lợi thế mà công cụ ngoài không có: **từ điển nghiệp vụ đã gắn thuật ngữ vào cột thật** *(menu 2.1)*. Nên câu hỏi tiếng Việt có thể ánh xạ qua thuật ngữ để ra đúng bảng — **không cần mô hình ngôn ngữ phức tạp** cho phần lớn trường hợp.

> 💡 **Nên làm hai bước:** bước một dùng **từ điển + bí danh** *(công sức thấp, đã có sẵn dữ liệu)*. Chỉ khi bước một không đủ mới tính tới mô hình ngôn ngữ.

</details>

<details open>
<summary><b>9 — Mở kho metadata cho trợ lý AI</b></summary>

**Một câu:** *cho phép trợ lý AI mà đội đang dùng hỏi thẳng kho metadata — "bảng nào chứa số điện thoại khách hàng", "sửa bảng này thì hỏng gì".*

**Thị trường làm gì**

Xu hướng rõ nhất của 2026: danh mục dữ liệu chuyển vai thành **lớp ngữ cảnh cho AI**. Atlan mở kho metadata qua giao thức chuẩn để các trợ lý như Copilot, Claude, Cortex đọc được **ngay lúc đang làm việc**.

**Vì sao hợp với đội mình**

Đội **đang dùng trợ lý AI để viết mã và viết tài liệu**. Nếu trợ lý đọc được kho metadata thì trả lời được ngay trong lúc code: *"bảng này ai phụ trách"*, *"cột này có nhạy cảm không"*, *"đổi cột này thì hỏng job nào"* — không phải mở tool riêng.

**Công sức thấp** vì chỉ là **mở API đọc** trên dữ liệu đã có, không đụng vào giao diện.

> ⚠️ **Chỉ mở phần metadata, tuyệt đối không mở dữ liệu thật.** Và phải đi qua đúng lớp quyền ở 5.2 — nếu không thì vừa xây xong lớp che dữ liệu lại tự mở một cửa sau.

</details>

---

## 4. Ba thứ thị trường có mà tôi khuyên KHÔNG làm

<details open>
<summary><b>Nói rõ để tránh bị hỏi "sao không có cái này"</b></summary>

| Không làm | Vì sao |
|---|---|
| **Chấm điểm tin cậy bằng mô hình học máy phức tạp** | Không giải thích được vì sao bảng này 72 điểm còn bảng kia 65. Điểm mà **không giải thích được thì không ai tin và không ai dùng**. DMP nên giữ cách chấm **đếm được bằng tay** — bao nhiêu luật đạt trên tổng số luật |
| **Chia quyền tự trị theo miền kiểu *data mesh*** | Đòi mỗi miền có đội kỹ thuật riêng tự vận hành. Hiện **38% số bảng còn chưa gán được miền** — bàn tới tự trị là quá sớm. Quay lại sau khi độ phủ miền trên 90% |
| **Bán hoặc trao đổi dữ liệu ra bên ngoài** | Có trong các nền tảng gian hàng dữ liệu, nhưng **không phải bài toán của đơn vị**. Việc cần với dữ liệu ra ngoài là **kiểm soát và ghi dấu vết** — đã có ở 6.2 |

</details>

---

## 5. Đề xuất đưa vào lộ trình

<details open>
<summary><b>Xếp vào các đợt đã có, không đẻ thêm đợt mới</b></summary>

| Đợt | Đã có trong lộ trình | Thêm đề xuất nào | Vì sao đặt ở đây |
|:---:|---|---|---|
| **2** | Từ vựng + chất lượng | **7** máy viết mô tả · **8** tìm kiếm bằng câu nói | Cùng lúc với việc khai metadata — đúng lúc cần nhất |
| **3** | Sự cố + quyền | ⭐ **1** giám sát tự động · **2** cảnh báo đổi cấu trúc · ⭐ **3** gom theo nguyên nhân gốc | Ba cái này phải đi **cùng nhau**: bật giám sát mà không gom nguyên nhân thì ngập cảnh báo |
| **4** | Che dữ liệu + sức khoẻ | **4** lan cờ tin cậy · **9** mở metadata cho trợ lý AI | Cần sơ đồ luồng đã chạy ổn |
| **5** | Dữ liệu chủ | **6** gian hàng dữ liệu | Cần có gói dữ liệu đủ chín để đóng gói |
| *(sau)* | — | **5** cam kết dữ liệu | Đụng quy trình giữa các đội — làm khi tổ chức đã quen |

> 🔴 **Điểm quan trọng nhất về thứ tự:** ba đề xuất **1 · 2 · 3 phải làm cùng một đợt**.
>
> Bật giám sát tự động *(1)* mà chưa có gom theo nguyên nhân gốc *(3)* thì **hộp thư ngập vài trăm cảnh báo trong tuần đầu**, người dùng tắt thông báo, và cả module chất lượng chết đúng như cách tính năng cũ của SQLWF đã chết.

**Một câu để trả lời sếp**

> *Thiết kế hiện tại phủ đủ yêu cầu BDA. Chín đề xuất này lấy từ cách các công cụ thị trường đang làm, và tất cả đều nhắm vào ba con số đang xấu nhất: chỉ 0,6% bảng được kiểm chất lượng, 8.267 bảng thiếu mô tả, và cảnh báo rời rạc dễ làm người dùng tắt thông báo. Ba đề xuất đáng làm trước là giám sát tự động, gom sự cố theo nguyên nhân gốc, và để máy viết mô tả cho người duyệt — cả ba đều dùng lại thứ đã thiết kế, không đòi hạ tầng mới.*

</details>

---

## 6. Nhóm tính năng AI — cái nào thật, cái nào chỉ để trình diễn

<details open>
<summary><b>⭐ Trước hết: một lập luận đổi hẳn cách trình bày DMP với lãnh đạo</b></summary>

Năm 2026 câu hỏi của lãnh đạo không còn là *"có nên làm quản trị dữ liệu không"* mà là *"bao giờ dùng được AI"*. Nên nếu trình bày DMP như **một công cụ quản trị** thì nó cạnh tranh trực tiếp với các đề xuất về AI — và thường thua.

**Cách trình bày mạnh hơn: DMP là điều kiện cần để dùng AI an toàn.**

| Nếu chưa có DMP | Hậu quả khi đưa AI vào |
|---|---|
| Không biết cột nào chứa dữ liệu cá nhân | Trợ lý AI **đọc luôn cả số căn cước, số điện thoại khách hàng** |
| Không có lớp che dữ liệu | AI **nhắc lại nguyên văn dữ liệu nhạy cảm** trong câu trả lời |
| Không có sơ đồ luồng dữ liệu | Không truy được **AI đã đọc dữ liệu từ đâu** khi bị hỏi |
| Không có nhật ký theo chính sách | **Không chứng minh được** AI chỉ đọc thứ nó được phép |

> ⭐ Tài liệu thị trường nói thẳng một câu đáng dùng làm luận điểm chính:
> ***Trợ lý AI kế thừa đúng những quy tắc quản trị của dữ liệu mà nó đọc. Không có quản trị thì nó rò rỉ thứ lẽ ra không được rò.***
>
> Nói cách khác: **lớp kiểm soát cho AI chỉ tốt bằng đúng lớp phân loại dữ liệu nằm dưới nó.** Mà lớp phân loại đó chính là menu 2.2 và 5.2 của DMP.

**Một câu để mở đầu buổi trình bày**

> *Đơn vị muốn dùng AI trên dữ liệu của mình. Trước khi làm được điều đó thì phải trả lời được ba câu: dữ liệu nào là nhạy cảm, ai được đọc cái gì, và chứng minh thế nào. DMP là chỗ trả lời ba câu đó — nó không cạnh tranh với AI, nó là điều kiện để dùng AI mà không vi phạm.*

</details>

<details open>
<summary><b>⭐ Ba tính năng AI đáng làm thật — giá trị rõ, rủi ro thấp</b></summary>

Tiêu chí chọn: **máy đề xuất, người quyết** · có chỗ để đo xem máy đoán tốt hay tệ · sai thì hậu quả nhẹ.

---

### AI-1 · Tự dò cột nhạy cảm rồi đề xuất nhãn 🔥🔥🔥

**Một câu:** *máy quét toàn bộ cột trong kho, đoán cột nào chứa dữ liệu cá nhân, đề xuất nhãn cho người xác nhận.*

**Vì sao đây là đề xuất AI số một**

Thiết kế hiện tại đã có **412 cột được gắn nhãn** — nhưng gắn **bằng tay**. Trên tổng số cột của 11.482 bảng thì con số đó gần như chắc chắn **còn sót rất nhiều**. Mà một cột chứa số căn cước bị bỏ sót thì **mọi lớp bảo mật phía sau đều vô nghĩa với cột đó**.

Đây là bài toán mà máy làm tốt hơn người: **đọc tên cột + mẫu giá trị + kiểu dữ liệu** rồi nhận ra *"cột này trông như số căn cước"* — kể cả khi cột đặt tên là `ma_kh_02` chứ không phải `so_cccd`.

**Thêm vào DMP thế nào**

Thiết kế đã có sẵn chỗ: menu **2.2** đã có nút *"xem các cột hệ thống nghi ngờ"*. Việc cần làm là **nâng từ gợi ý lẻ tẻ thành quét định kỳ toàn kho**:

| Việc | Chi tiết |
|---|---|
| Quét | Định kỳ hằng tuần trên toàn bộ cột, không chỉ bảng mới |
| Kết quả | Hàng chờ *"cột nghi ngờ chứa dữ liệu nhạy cảm"* kèm **mức độ tin** và **lý do đoán** |
| Người xác nhận | Đầu mối nghiệp vụ của bảng — bấm **Đúng** hoặc **Không phải** |
| ⭐ Ghi nhớ | *"Không phải"* phải nhớ, lần sau không hỏi lại cột đó nữa |

> 🔴 **Bắt buộc có người xác nhận, không tự gắn nhãn.** Tự gắn nhãn sai thì hoặc là che nhầm dữ liệu bình thường *(người dùng kêu)*, hoặc bỏ sót dữ liệu thật *(nguy hiểm hơn nhiều)*.

**Đo thế nào:** tỷ lệ đề xuất được xác nhận là đúng. Dưới 60% thì máy đang đoán tệ, chỉnh lại trước khi mở rộng.

---

### AI-2 · Máy viết mô tả, người duyệt 🔥🔥🔥

Đã nêu ở đề xuất **7** phần trên. Nhắc lại vì đây thuộc nhóm AI và là thứ chữa con số **8.267 bảng thiếu mô tả**.

Điểm quan trọng nhắc lại: **máy đề xuất → hàng chờ duyệt ở 2.4 → mới thành mô tả chính thức**, và mô tả nào do máy viết thì **ghi rõ nguồn gốc**.

---

### AI-3 · Tóm tắt sự cố và gợi ý nguyên nhân 🔥🔥

**Một câu:** *khi sự cố sinh ra, máy đọc mọi manh mối rồi viết sẵn một đoạn tóm tắt cho người xử lý — thay vì để họ tự đi ghép.*

**Vấn đề đang có**

Người nhận phiếu sự cố hiện phải tự đi ghép: luật nào hỏng, dòng nào sai, gần đây ai đổi gì trên bảng, bảng này lấy dữ liệu từ đâu. **Mất thời gian nhất là bước ghép manh mối**, không phải bước sửa.

**Máy có sẵn bốn manh mối, đều nằm trong DMP**

| Manh mối | Lấy từ |
|---|---|
| Luật nào hỏng, sai bao nhiêu dòng | 3.2 |
| Mẫu dòng lỗi | 3.3 |
| Thay đổi gần đây trên bảng và trên job | 1.1 tab Lịch sử · 4.1 tab Phiên bản |
| Bảng này ăn dữ liệu từ đâu, nhánh nào cũng đang hỏng | 2.3 |

Kết quả là một đoạn tóm tắt kiểu:

> *Luật "số tiền không âm" hỏng trên 1.204 dòng, bắt đầu từ lần chạy 06:00 hôm nay. Job JOB-0412 vừa đổi phiên bản lúc 22:15 hôm qua, có sửa câu SQL ở bước 4. Bảng nguồn `raw.doi_soat_A_tho` cũng đang có sự cố chưa đóng. **Nhiều khả năng nguyên nhân nằm ở bảng nguồn, không phải ở job.***

> ⭐ **Đây là trợ lý, không phải người quyết.** Máy đưa giả thuyết kèm căn cứ, người xử lý xác nhận hoặc bác bỏ. Bác bỏ cũng là dữ liệu để chỉnh lại về sau.

</details>

<details open>
<summary><b>Hai tính năng AI đáng làm nhưng phải cẩn thận</b></summary>

### AI-4 · Đọc văn bản quy định rồi đề xuất mục kiểm tuân thủ 🔥🔥

**Một câu:** *tải văn bản quy định lên, máy trích ra các yêu cầu kiểm soát và đề xuất thành mục kiểm cho kỳ đánh giá.*

Module ⑥ hiện bắt người dùng **tự đọc nghị định rồi tự nghĩ ra mục kiểm**. Máy làm được bước nháp đó: đọc văn bản, tách từng yêu cầu, đề xuất mục kiểm kèm cách kiểm *(tự động hay thủ công)*.

Ví dụ với một điều khoản về thời hạn lưu dữ liệu cá nhân, máy đề xuất mục kiểm *"mọi bảng chứa nhãn dữ liệu cá nhân phải có quy tắc vòng đời"* và đánh dấu **kiểm tự động** — vì DMP đọc được số này từ menu 6.2.

> 🔴 **Rủi ro pháp lý nếu máy hiểu sai điều khoản.** Bắt buộc: người phụ trách pháp chế duyệt từng mục kiểm, và **luôn hiện kèm trích dẫn nguyên văn đoạn văn bản** mà máy dựa vào — để người duyệt đối chiếu chứ không phải tin máy.

---

### AI-5 · Hỏi về dữ liệu bằng tiếng Việt 🔥🔥

**Một câu:** *gõ câu hỏi thường vào ô tìm kiếm, nhận câu trả lời kèm đường dẫn tới đúng màn.*

Ba loại câu hỏi đáng làm — **đều chỉ đọc metadata, không đụng dữ liệu thật**:

| Câu hỏi | Máy trả lời bằng |
|---|---|
| *"Bảng nào chứa số điện thoại khách hàng"* | Nhãn ở 2.2 + tab Cột |
| *"Sửa cột `so_tien` thì hỏng gì"* | Sơ đồ luồng ở 2.3 |
| *"Ai chịu trách nhiệm bảng doanh thu"* | Đầu mối ở 1.1 |

> 💡 **Nên làm hai bước.** Bước một dùng **từ điển nghiệp vụ và bí danh đã có ở 2.1** — phần lớn câu hỏi giải được mà không cần mô hình ngôn ngữ. Chỉ khi bước một không đủ mới tính tới AI.
>
> Đây cũng là lợi thế DMP có mà công cụ mua ngoài không có: **từ điển đã gắn thuật ngữ vào cột thật**, tức là máy có sẵn bản đồ giữa cách nói của người và tên cột kỹ thuật.

</details>

<details open>
<summary><b>⚠️ Hai thứ đang được quảng cáo mạnh mà tôi khuyên KHÔNG làm</b></summary>

### Không làm · Để AI tự quyết cấp quyền và tự che dữ liệu

Thị trường gọi là *quản trị dữ liệu tự hành* — AI tự đọc ngữ cảnh rồi tự quyết **cho phép · từ chối · che · trì hoãn · đẩy lên người duyệt**, không cần luật cố định.

**Vì sao tôi khuyên không:**

| Vấn đề | Giải thích |
|---|---|
| **Không giải thích được** | Kiểm toán hỏi *"vì sao người này xem được cột căn cước"* mà câu trả lời là *"mô hình quyết vậy"* thì **không chấp nhận được** |
| **Đúng thứ DMP đang cố sửa** | Cả thiết kế đang xây quanh việc **mọi quyền phải truy được lý do cấp**. Để AI tự quyết là **phá chính nguyên tắc đó** |
| **Sai một chiều rất nặng** | Cấp nhầm quyền đọc dữ liệu cá nhân là sự cố phải báo cáo, không phải lỗi sửa sau |

> ⭐ **Cách đúng: AI đề xuất, người quyết.** Ví dụ ở menu 5.3, máy gợi ý *"4/9 người trong nhóm đã xin bảng này — nên cấp cho cả nhóm"* hoặc *"người này xin quyền tương tự 3 lần trong 2 tháng"*. Người duyệt vẫn bấm nút.

---

### Không làm ngay · Cho người nghiệp vụ hỏi thẳng dữ liệu bằng tiếng Việt

Đây là tính năng **được quảng cáo nhiều nhất** — gõ câu hỏi, máy sinh câu truy vấn, trả về số.

**Ba lý do để sau:**

| Rủi ro | Giải thích |
|---|---|
| **Cửa sau bỏ qua lớp bảo mật** | Nếu máy sinh truy vấn chạy thẳng xuống kho dữ liệu thì **vượt qua lớp che dữ liệu và lọc theo dòng** vừa xây ở 5.2 |
| **Số sai mà người dùng không biết** | Máy hiểu nhầm câu hỏi thì vẫn trả về **một con số trông rất hợp lý**. Người nghiệp vụ không có cách nào kiểm |
| **Chất lượng phụ thuộc metadata** | Với **8.267 bảng chưa có mô tả**, máy không có gì để hiểu ngữ cảnh — làm bây giờ chắc chắn đoán sai nhiều |

> **Điều kiện để làm sau:** metadata phủ trên 80% · mọi truy vấn máy sinh ra **bắt buộc đi qua lớp quyền ở 5.2** như người dùng thật · và luôn **hiện câu truy vấn đã sinh** để người dùng đối chiếu.

</details>

<details open>
<summary><b>⭐ Lợi thế sẵn có mà đội chưa khai thác: đã có OPA</b></summary>

Tài liệu thị trường nói rằng nền của quản trị dữ liệu tự hành là **chính sách viết dưới dạng mã** *(policy-as-code)*, và công cụ được nhắc tên cụ thể là **Open Policy Agent — OPA**.

> 🔥 **SQLWF đã có OPA và đang chạy.** Kết quả kiểm kê mã nguồn cho thấy hệ thống hiện đã đồng bộ nhãn dữ liệu sang OPA qua các đầu nối `/api/table/sync/` và `/api/function/sync/tag/`.

**Nghĩa là gì**

| | |
|---|---|
| **Hiện tại** | OPA mới dùng để **chặn một số hàm SQL theo nhãn** — dùng chưa hết một phần nhỏ khả năng |
| **Có thể làm** | Chuyển toàn bộ chính sách ở 5.2 *(che dữ liệu · lọc theo dòng · hạn chế tải xuống)* thành **chính sách dạng mã chạy trên OPA** |
| **Được gì** | Chính sách **kiểm tra được bằng máy**, **có phiên bản như mã nguồn**, và **áp cùng một luật cho cả người dùng lẫn trợ lý AI** |

> ⭐ **Đây là điểm đáng nói nhất khi trình bày:** phần hạ tầng khó nhất mà thị trường coi là nền của quản trị hiện đại thì **đơn vị đã có sẵn và đã chạy**. Việc còn lại là **dùng cho đúng tầm**, không phải mua thêm.

</details>

<details open>
<summary><b>Tóm tắt — năm tính năng AI, xếp theo thứ tự nên làm</b></summary>

| Thứ tự | Tính năng | Vào menu | Điều kiện cần | Giá trị |
|:---:|---|---|---|:---:|
| **1** | ⭐ Tự dò cột nhạy cảm, đề xuất nhãn | 2.2 | Không — làm được ngay | 🔥🔥🔥 |
| **2** | ⭐ Máy viết mô tả, người duyệt | 1.1 · 2.4 | Cần hàng chờ duyệt ở 2.4 | 🔥🔥🔥 |
| **3** | Tóm tắt sự cố, gợi ý nguyên nhân | 3.3 | Cần sơ đồ luồng ở 2.3 chạy ổn | 🔥🔥 |
| **4** | Hỏi metadata bằng tiếng Việt | thanh tìm kiếm | Cần từ điển 2.1 đủ dày | 🔥🔥 |
| **5** | Đọc văn bản quy định, đề xuất mục kiểm | 6.1 · 6.3 | Cần module ⑥ đã dựng | 🔥🔥 |

**Nguyên tắc chung áp cho cả năm — viết vào tài liệu để không ai làm sai**

| # | Nguyên tắc |
|:---:|---|
| **1** | ⭐ **Máy đề xuất, người quyết.** Không tính năng AI nào được ghi thẳng vào danh mục hay tự áp chính sách |
| **2** | **Luôn hiện căn cứ.** Máy đoán gì cũng phải nói dựa vào đâu — tên cột, mẫu dữ liệu, hay đoạn văn bản nào |
| **3** | **Ghi rõ cái gì do máy tạo.** Mô tả, nhãn, mục kiểm do máy đề xuất phải phân biệt được với thứ người viết |
| **4** | **Có chỗ đo máy đoán tốt hay tệ.** Tỷ lệ đề xuất được duyệt mà không phải sửa. Dưới ngưỡng thì tắt |
| **5** | **Nhớ câu trả lời "không phải".** Người đã bác một đề xuất thì đừng hỏi lại — đây là lỗi làm người dùng bỏ mặc hàng chờ |

</details>

---

## 7. ⭐ NHÓM ĐỘT PHÁ — thứ DMP làm được mà công cụ mua ngoài không làm được

<details open>
<summary><b>Lợi thế không mua được: DMP nắm thứ mà trợ lý AI bên ngoài không có</b></summary>

Phần 6 ở trên là **AI an toàn cho quản trị** — hữu ích nhưng không tạo khác biệt, và công cụ nào cũng đang làm.

Phần này khác. Nó dựa vào một điều mà **không sản phẩm mua ngoài nào có được**:

> ⭐ **DMP nắm đồng thời sáu thứ về hệ thống dữ liệu của chính đơn vị.**

| DMP đang nắm | Có ở đâu | Trợ lý AI mua ngoài có không |
|---|---|:---:|
| **Toàn bộ câu SQL của 1.842 job** | 4.1 tab Bước xử lý | ❌ |
| **Lịch sử chạy từng bước** — thời gian, số dòng, hỏng ở đâu | 4.1 tab Lần chạy | ❌ |
| **Sơ đồ luồng dữ liệu** — job nào nuôi bảng nào nuôi báo cáo nào | 2.3 | ❌ |
| **Kích thước, phân vùng, số dòng từng bảng** | 1.1 | ❌ |
| **Thuật ngữ nghiệp vụ đã gắn vào cột thật** | 2.1 | ❌ |
| **Luật chất lượng và lịch sử sự cố** | 3.2 · 3.3 | ❌ |

Một trợ lý viết mã thông thường nhìn được **một câu SQL rời rạc**. DMP nhìn được **câu SQL đó chạy trên bảng nào, bảng đó bao nhiêu dòng, lần trước chạy mất bao lâu, hỏng ở bước nào, và ai đang đọc kết quả**.

> **Đây là lý do đề xuất trong phần này không thể mua, chỉ có thể tự xây — và cũng là lý do nó đáng đưa vào tài liệu trình lãnh đạo.**

</details>

---

### Nhóm A — Tối ưu vận hành: đo được bằng tiền

<details open>
<summary><b>⭐ Đ1 — Trợ lý tối ưu câu SQL của job 🔥🔥🔥</b></summary>

**Một câu:** *máy đọc câu SQL cùng lịch sử chạy và thống kê bảng, chỉ ra chỗ đang lãng phí tài nguyên, đề xuất cách sửa kèm ước lượng tiết kiệm.*

**Có thật không**

Có. Datadog công bố **giảm 44% chi phí tính toán Spark** bằng một trợ lý AI đọc số liệu từng chặng, kế hoạch thực thi SQL và dữ liệu vận hành để chỉ ra điểm nghẽn và gợi ý cách sửa.

**Máy tìm được những gì — đều là lỗi kinh điển trong job SQL**

| Kiểu lãng phí | Máy phát hiện bằng cách nào |
|---|---|
| **Quét cả bảng khi chỉ cần một phân vùng** | Câu SQL không lọc theo cột phân vùng đã khai ở 1.1 |
| **`SELECT *` trên bảng chục triệu dòng** | Đối chiếu số cột dùng thật với số cột đọc về |
| **Nối bảng thiếu điều kiện** | Số dòng ra lớn bất thường so với số dòng vào |
| **Đọc lại thứ bước trước đã tính** | So sánh các bước trong cùng job |
| **Sắp xếp lại dữ liệu không cần thiết** | Thời gian một bước lệch hẳn so với các bước khác |

**Đầu ra trình bày cho người dùng**

> *Bước 4 của `JOB-0412` đang đọc cả 12 tháng dữ liệu trong khi chỉ dùng 1 tháng. Thêm điều kiện lọc theo cột phân vùng `ngay_du_lieu`.*
> *Ước tính: thời gian chạy từ 2 phút 14 xuống khoảng 20 giây.*
> ***Áp cho 23 job khác đang có cùng kiểu lãng phí.***

> 🔴 **Bài học quan trọng từ chính Datadog:** những gợi ý đầu tiên của họ **sai mục tiêu** — máy khuyên cắt bớt cột trong khi Spark đã tự cắt rồi; và **càng thêm ngữ cảnh thì càng nhiều gợi ý sai**. Họ phải thêm một lớp lọc bỏ gợi ý không liên quan.
>
> **Áp dụng cho mình:** không bung ra 1.842 job ngay. Chạy trên **20 job tốn nhiều tài nguyên nhất trước**, đo tỷ lệ gợi ý được DE chấp nhận. Dưới 50% thì dừng lại chỉnh, đừng mở rộng.

</details>

<details open>
<summary><b>⭐ Đ2 — Báo trước job sắp hỏng, thay vì báo sau khi đã hỏng 🔥🔥🔥</b></summary>

**Một câu:** *dữ liệu lớn dần theo tháng — máy ngoại suy và báo "job này còn khoảng ba tuần nữa sẽ hết bộ nhớ", trước khi nó hỏng giữa đêm.*

**Vì sao đề xuất này thuyết phục**

Ngay trong dữ liệu minh hoạ của demo đã có ca này: **`JOB-0501` hỏng ở bước 7 vì hết bộ nhớ**. Đây không phải giả định — đây là kiểu hỏng quen thuộc, và nó luôn xảy ra **giữa đêm, vào đúng kỳ chốt số**, khi dữ liệu đạt ngưỡng.

Điều đáng nói: **kiểu hỏng này đoán trước được**, vì nó không đến đột ngột. Số dòng tăng dần qua từng tháng, thời gian chạy dài dần, rồi một hôm vượt ngưỡng.

**DMP có sẵn ba chuỗi số để ngoại suy**

| Chuỗi số | Lấy từ |
|---|---|
| Số dòng vào từng bước qua các lần chạy | 4.1 tab Lần chạy |
| Thời gian chạy từng bước theo thời gian | 4.1 tab Lần chạy |
| Số dòng và dung lượng bảng nguồn tăng dần | 1.1 |

**Đầu ra**

> ⚠️ *`JOB-0501` — thời gian bước 7 tăng đều 8% mỗi tháng trong 5 tháng qua. Với nhịp này, **khoảng cuối tháng 10 sẽ vượt hạn mức bộ nhớ**.*
> *Đề xuất: chia bước 7 theo phân vùng, hoặc tăng bộ nhớ trước kỳ chốt số tháng 10.*

> 💡 **Nói thật về mức độ chắc chắn:** tôi tìm được nghiên cứu về **dự báo tài nguyên** và **ước lượng chi phí truy vấn trước khi chạy**, nhưng **chưa tìm được nguồn về dự báo lỗi tràn bộ nhớ cụ thể**.
>
> Nên đề xuất này nên làm ở mức **ngoại suy xu hướng đơn giản** — vẽ đường xu hướng và cảnh báo khi sắp chạm ngưỡng. Không hứa mô hình phức tạp. Cách đơn giản này đã đủ để tránh phần lớn ca hỏng giữa đêm.

</details>

<details open>
<summary><b>Đ3 — Ước lượng chi phí và thời gian TRƯỚC khi cho job chạy 🔥🔥</b></summary>

**Một câu:** *DE bấm lưu job mới, DMP báo ngay "job này sẽ chạy khoảng 8 phút, đọc 40 GB" và cảnh báo nếu vượt ngưỡng.*

**Có nghiên cứu thật**

Một nghiên cứu năm 2026 giải đúng bài toán này: dự báo tài nguyên tiêu tốn **trước khi chạy**, chỉ dùng các tín hiệu quan sát được — **độ phức tạp câu lệnh** *(từ chi phí các phép toán)*, **khối lượng dữ liệu** *(từ ước lượng của bộ tối ưu và siêu dữ liệu)*, và **đặc trưng từ chính văn bản câu lệnh**.

Lý do phải dùng học máy: các công thức tĩnh của bộ tối ưu **không mô hình hoá được lệch phân bố dữ liệu, hiệu ứng bộ nhớ đệm và tranh chấp tài nguyên**, nên ước lượng có thể sai tới vài bậc.

**Áp vào DMP thế nào**

Đặt ngay trong luồng khai job ở **4.1**, ở bước cuối trước khi gửi duyệt:

| Hiện | Thêm |
|---|---|
| Bấm lưu → gửi duyệt | Bấm lưu → **hiện ước lượng** → cảnh báo nếu vượt ngưỡng → gửi duyệt |

> ⭐ **Giá trị lớn nhất không phải con số ước lượng, mà là chỗ đặt nó.** Người duyệt job nhìn thấy *"job này ngốn gấp 6 lần job trung bình"* **ngay lúc duyệt** — chứ không phải một tháng sau khi hoá đơn hạ tầng tăng.

</details>

<details open>
<summary><b>Đ4 — Tìm job đang tính trùng nhau 🔥🔥</b></summary>

**Một câu:** *1.842 job — máy so cấu trúc câu SQL và sơ đồ luồng để tìm những job đang tính cùng một thứ từ cùng một nguồn.*

Với gần hai nghìn job tích luỹ qua nhiều năm và nhiều người làm, **gần như chắc chắn có nhóm job tính trùng nhau** — mỗi đội tự viết một bản cho riêng mình.

**Máy so được vì DMP có cả hai mặt**

| Mặt | Dùng để |
|---|---|
| **Cấu trúc câu SQL** | Hai job cùng nhóm theo cùng cột, cùng tổng hợp cùng chỉ tiêu |
| **Sơ đồ luồng** | Hai job cùng đọc từ một bảng nguồn, ghi ra hai bảng đích khác nhau |

**Đầu ra**

> *Năm job đang cùng tính doanh thu ngày từ `dwh.giao_dich_ngay`, ghi ra năm bảng đích khác nhau, chênh nhau chỉ ở điều kiện lọc.*
> *Gộp lại: bớt 4 job chạy hằng ngày, bớt 4 bảng phải lưu.*

> ⚠️ **Không tự gộp.** Máy chỉ ra nhóm nghi ngờ, người xác nhận — vì hai job trông giống nhau vẫn có thể phục vụ hai mục đích nghiệp vụ khác nhau.

</details>

<details open>
<summary><b>Đ5 — Đang trả tiền cho thứ không ai dùng 🔥🔥</b></summary>

**Một câu:** *quy chi phí hạ tầng về từng bảng và từng job, chỉ ra thứ đang tốn tiền mà không ai đọc.*

**DMP đã có sẵn các con số**

| Con số | Có ở đâu |
|---|---|
| **186 job không ai chạy 90 ngày** | 4.1 |
| Bảng có lượt đọc bằng 0 | 5.4 nhật ký truy cập |
| Dung lượng từng bảng | 1.1 |
| Số lần chạy và thời gian mỗi job | 4.1 |

Ghép lại ra một con số mà **lãnh đạo hiểu ngay**:

> *Hiện có **X TB dữ liệu không ai đọc trong 6 tháng**, và **186 job vẫn chạy hằng ngày để cập nhật những bảng đó**.*
> *Dừng lại: tiết kiệm Y giờ máy mỗi tháng.*

> ⭐ **Đây là đề xuất dễ được duyệt nhất trong cả tài liệu**, vì nó **tự trả tiền cho chính nó** và số liệu thì DMP đã có, chỉ cần ghép lại.
>
> Nối thẳng vào menu **6.2 Vòng đời & Lưu trữ** — vốn đã có hàng chờ *"đến hạn xử lý"*.

</details>

---

### Nhóm B — Trợ lý tri thức

<details open>
<summary><b>⭐ Đ6 — Bot hỏi đáp trên tri thức dữ liệu của đơn vị 🔥🔥🔥</b></summary>

**Một câu:** *hỏi bằng tiếng Việt về dữ liệu và nghiệp vụ, máy tổng hợp câu trả lời từ toàn bộ 27 menu kèm đường dẫn tới chỗ xem chi tiết.*

**⭐ Điểm mấu chốt phân biệt với thứ tôi đã khuyên KHÔNG làm ở phần 6**

| | Hỏi **dữ liệu thật** *(khuyên chưa làm)* | Hỏi **tri thức về dữ liệu** *(nên làm)* |
|---|---|---|
| Câu hỏi | *"Doanh thu tháng trước bao nhiêu"* | *"Báo cáo doanh thu lấy số từ đâu, ai làm, tính thế nào"* |
| Máy đọc gì | **Dữ liệu thật** trong kho | **Chỉ metadata** trong DMP |
| Rủi ro lộ dữ liệu | 🔴 Cao — có thể vòng qua lớp che | ✅ **Không có** — không đụng tới dữ liệu |
| Sai thì sao | Người dùng ra quyết định trên **số sai** | Chỉ trỏ sai chỗ, mở ra là biết |

**Một câu hỏi, máy tổng hợp từ nhiều menu**

> **Hỏi:** *"Báo cáo doanh thu ngày đang có vấn đề gì không?"*
>
> **Trả lời:** *Báo cáo này lấy số từ `bi.doanh_thu_thang`, do `JOB-0119` sinh ra lúc 07:00 hằng ngày, đầu mối là chị Phương.*
> *⚠️ Bảng nguồn `bi.doi_soat_giao_dich_A` **đang có sự cố chưa đóng từ sáng nay** — nên số trên báo cáo hôm nay nên coi là chưa tin cậy.*
> *Báo cáo có 37 người xem mỗi tuần. Đã gửi cảnh báo cho 2 đầu mối lúc 06:05.*
> *→ Xem chi tiết: sự cố SC-0231 · báo cáo BC-001 · sơ đồ luồng*

Câu trả lời đó gộp dữ liệu từ **1.1 · 1.3 · 2.3 · 3.3 · 4.1 · 5.4** — sáu menu. Người dùng tự làm việc này mất **mười lăm phút mở sáu màn**.

> ⭐ **Đây là tính năng gây ấn tượng mạnh nhất khi trình bày**, và cũng là tính năng **an toàn nhất** trong nhóm đột phá — vì nó chỉ đọc metadata.

</details>

<details open>
<summary><b>Đ7 — Bản tóm tắt tự viết cho lãnh đạo, kèm biểu đồ 🔥🔥</b></summary>

**Một câu:** *đầu tháng, máy tự viết một trang tóm tắt tình hình dữ liệu bằng lời, kèm biểu đồ — thay vì để lãnh đạo tự đọc bảng số.*

**Vấn đề của màn sức khoẻ dữ liệu hiện tại**

Màn 8.1 có mười chỉ số. Nhưng lãnh đạo nhìn vào **không biết cái nào đáng lo** — và quan trọng hơn, **không biết con số tăng là do cải thiện thật hay do đổi cách đo**.

**Máy viết được vì nó thấy cả xu hướng lẫn nguyên nhân**

> **Tháng 8/2026**
> *Điểm chất lượng tăng từ 84 lên 87. **Nhưng phần lớn mức tăng đến từ việc thêm 12 bảng dễ đạt vào diện kiểm, không phải từ cải thiện thật** — nếu chỉ tính trên nhóm bảng đã kiểm từ tháng trước thì điểm gần như đứng yên.*
> *Ba sự cố quá hạn đều thuộc miền Vận hành, cùng một đầu mối — nên xem lại phân công.*
> *Việc đáng làm nhất tháng tới: 4.334 bảng chưa gán miền, chiếm 38%.*

> ⭐ **Câu quan trọng nhất là câu thứ hai** — thứ mà một bảng số không nói ra được, và cũng là thứ khiến bản tóm tắt này **đáng tin hơn dashboard**.

</details>

<details open>
<summary><b>Đ8 — Trợ lý viết job biết ngữ cảnh doanh nghiệp 🔥🔥</b></summary>

**Một câu:** *DE viết job mới, trợ lý gợi ý dựa trên cấu trúc bảng thật, thuật ngữ nghiệp vụ, chuẩn đặt tên và tình trạng bảng — chứ không phải gợi ý chung chung.*

**Khác gì trợ lý viết mã thông thường**

| Trợ lý viết mã thường | Trợ lý trong DMP |
|---|---|
| Biết cú pháp SQL | Biết **bảng nào thật sự tồn tại**, cột tên gì, kiểu gì |
| Không biết nghiệp vụ | Biết *"doanh thu ghi nhận"* ứng với cột nào ở bảng nào |
| Không biết tình trạng | ⚠️ **Cảnh báo *"bảng này đang có sự cố chưa đóng, cân nhắc dùng bảng khác"*** |
| Không biết quy ước | Kiểm **chuẩn đặt tên** khai ở 8.2 ngay lúc viết |
| Không biết hệ quả | Nhắc *"bảng đích chưa khai trong danh mục — khai trước khi lưu"* |

> ⭐ **Dòng đáng giá nhất là dòng cảnh báo bảng đang có sự cố.** Không công cụ bên ngoài nào biết điều đó, vì chỉ DMP nắm trạng thái sự cố.

</details>

<details open>
<summary><b>Đ9 — Chạy thử tác động trước khi đổi 🔥🔥</b></summary>

**Một câu:** *trước khi đổi kiểu một cột hay bỏ một bảng, hỏi máy "đổi cái này thì hỏng gì" và nhận câu trả lời cụ thể tới từng bước job.*

**Khác gì sơ đồ luồng đang có**

Sơ đồ ở 2.3 cho biết **cái gì liên quan tới cái gì**. Chạy thử tác động cho biết **cụ thể hỏng ở đâu và hỏng thế nào**:

> **Hỏi:** *"Đổi `so_tien` từ số thập phân sang chuỗi thì sao?"*
>
> **Trả lời:** *3 job sẽ lỗi:*
> *· `JOB-0412` bước 4 — phép trừ trên cột chuỗi*
> *· `JOB-0119` bước 2 — hàm tổng trên cột chuỗi*
> *· `JOB-0233` bước 6 — so sánh lớn hơn*
> *2 báo cáo sai số: BC-001, BC-004*
> *1 luật chất lượng ngừng chạy: "số tiền không âm"*

Máy làm được vì DMP có **câu SQL của từng bước** — nên biết cột đó **được dùng vào việc gì**, không chỉ biết nó được dùng.

> 💡 Nối thẳng vào quy trình phê duyệt ở **2.4**: hồ sơ đổi cấu trúc bảng **tự kèm sẵn kết quả chạy thử tác động** để người duyệt biết mình đang duyệt cái gì.

</details>

---

<details open>
<summary><b>⭐ Tóm tắt nhóm đột phá — và điều kiện cần</b></summary>

| # | Đề xuất | Đo bằng | Công sức | Điều kiện cần |
|:---:|---|---|:---:|---|
| **Đ1** | Tối ưu SQL của job | **Giờ máy tiết kiệm được** | Cao | Bộ phân tích cú pháp SQL |
| **Đ2** | Báo trước job sắp hỏng | Số ca hỏng giữa đêm giảm | Trung bình | Lịch sử chạy đủ dài |
| **Đ3** | Ước lượng chi phí trước khi chạy | Số job bị chặn vì quá tốn | Trung bình | Lịch sử chạy |
| **Đ4** | Tìm job tính trùng | Số job gộp được | Trung bình | Bộ phân tích cú pháp SQL |
| **Đ5** | ⭐ Trả tiền cho thứ không ai dùng | **Dung lượng và giờ máy cắt được** | **Thấp** | Đã có đủ số liệu |
| **Đ6** | ⭐ Bot hỏi đáp tri thức dữ liệu | Số câu hỏi tự trả lời được | Trung bình | Metadata đủ dày |
| **Đ7** | Tóm tắt cho lãnh đạo | — | Thấp | Cần 8.1 chạy vài tháng |
| **Đ8** | Trợ lý viết job | Thời gian dựng job mới | Cao | Bộ phân tích cú pháp SQL |
| **Đ9** | Chạy thử tác động | Số lần đổi gây hỏng giảm | Trung bình | Bộ phân tích cú pháp SQL |

**Một thứ mở khoá bốn đề xuất**

> 🔑 **Bộ phân tích cú pháp SQL** — đọc câu SQL thành cấu trúc để biết nó động vào bảng nào, cột nào, làm phép gì.
>
> Thứ này **đã nằm trong tài liệu đề xuất từ đầu** *(để thay cách dò quan hệ luồng bằng cách tìm chuỗi `${…}`)*. Làm nó thì mở khoá luôn **Đ1 · Đ4 · Ð8 · Đ9**.
>
> **Đây là hạng mục nên ưu tiên nhất về mặt kỹ thuật** — một việc, bốn tính năng.

**Nếu chỉ chọn ba để trình bày**

| Chọn | Vì sao |
|---|---|
| ⭐ **Đ5** Trả tiền cho thứ không ai dùng | **Công sức thấp nhất, số liệu đã có, tự trả tiền cho chính nó** — nên làm đầu tiên |
| ⭐ **Đ6** Bot hỏi đáp tri thức dữ liệu | **Gây ấn tượng mạnh nhất khi demo**, mà lại an toàn vì chỉ đọc metadata |
| ⭐ **Đ2** Báo trước job sắp hỏng | Chạm đúng nỗi đau có thật — `JOB-0501` đang hỏng vì hết bộ nhớ |

**Một câu để trình bày cả nhóm này**

> *Đơn vị đang có 1.842 job, 11.482 bảng và nhiều năm lịch sử chạy — nhưng chưa ai từng dùng đống dữ liệu vận hành đó để làm gì. DMP là chỗ duy nhất nắm đồng thời câu lệnh, lịch sử chạy, sơ đồ luồng và tình trạng chất lượng. Nhóm tính năng này biến đống dữ liệu vận hành đó thành ba thứ đo được: cắt chi phí hạ tầng, báo trước sự cố thay vì báo sau, và trả lời câu hỏi về dữ liệu trong vài giây thay vì mở sáu màn.*

</details>

---

## 8. ⭐ NHÌN TỪ NGƯỜI DÙNG — tắc nghẽn thật trong công việc hằng ngày

<details open>
<summary><b>Cách làm phần này khác gì hai phần trên</b></summary>

Phần 6 và 7 xuất phát từ **thị trường có gì**. Phần này xuất phát từ **một ngày làm việc của ba người**, và hỏi: *chỗ nào họ đang mất thời gian mà tool chưa đỡ được?*

> ⭐ **Phát hiện chung cho cả ba vai:** thiết kế hiện tại rất mạnh ở phần **khai báo và kiểm soát**, nhưng gần như **chưa đụng tới phần phối hợp giữa người với người** — mà đó mới là chỗ thời gian thật sự bị đốt.
>
> Cụ thể: yêu cầu vẫn đi qua chat · việc của một người nằm rải ở năm menu · người **dùng** dữ liệu không được báo khi dữ liệu hỏng · và **không ai đo được chính quy trình của DMP đang tắc ở đâu**.

</details>

---

### Vai 1 — BDA, người phụ trách dữ liệu

<details open>
<summary><b>Một ngày của BDA và bốn chỗ đang mất thời gian</b></summary>

**Ngày làm việc điển hình**

> Sáng mở máy: 3 tin nhắn hỏi *"bảng nào có số thuê bao rời mạng"* · 1 email xin quyền · 1 cảnh báo luật hỏng · 1 hồ sơ chờ duyệt từ hôm qua. Chưa làm gì đã hết buổi sáng.

**Bốn tắc nghẽn**

| # | Tắc ở đâu | Hiện tại | Đề xuất |
|:---:|---|---|---|
| **1** | **Việc nằm rải ở năm chỗ** | Phê duyệt ở 2.4 · sự cố ở 3.3 · yêu cầu quyền ở 5.3 · đánh giá ở 6.3 · nghi ngờ trùng ở 7.2 — phải mở năm menu mới biết mình có bao nhiêu việc | **B1 · Hộp thư "Việc của tôi"** |
| **2** | **Yêu cầu đến qua chat, thiếu thông tin** | Nghiệp vụ nhắn *"cho anh số doanh thu"* → BDA hỏi lại 3–4 lượt mới đủ hiểu | **B2 · Cổng tiếp nhận yêu cầu** |
| **3** | **Bàn giao khi nghỉ phép hoặc chuyển việc** | Phải mở từng bảng đổi đầu mối. Một người phụ trách 148 bảng thì **không ai làm nổi** | **B3 · Bàn giao hàng loạt** |
| **4** | **Sửa định nghĩa mà không biết ảnh hưởng ai** | Đổi định nghĩa một thuật ngữ → không biết bao nhiêu cột, bao nhiêu báo cáo đang dùng nghĩa cũ | **B4 · Xem trước tác động khi sửa metadata** |

---

#### ⭐ B1 · Hộp thư "Việc của tôi" — gộp năm hàng chờ 🔥🔥🔥

**Một câu:** *một màn duy nhất liệt kê mọi việc đang chờ tôi, xếp theo hạn và mức quan trọng — không cần nhớ việc nào nằm ở menu nào.*

Đây là **tắc nghẽn rõ nhất và dễ sửa nhất** trong toàn bộ thiết kế. Hiện có **năm hàng chờ riêng biệt**, và người dùng phải **tự đi tuần qua năm menu**.

| Nguồn việc | Menu |
|---|---|
| Hồ sơ metadata chờ duyệt | 2.4 |
| Sự cố chất lượng được gán | 3.3 |
| Yêu cầu cấp quyền chờ duyệt | 5.3 |
| Mục kiểm tuân thủ chờ khắc phục | 6.3 |
| Cặp bản ghi nghi ngờ trùng | 7.2 |
| *(thêm)* Dữ liệu đến hạn xoá | 6.2 |

**Màn gộp cần có gì**

| Cột | Vì sao cần |
|---|---|
| Loại việc · nguồn | Biết từ đâu tới |
| **Hạn xử lý và mức quá hạn** | ⭐ Thứ quyết định làm gì trước |
| **Ảnh hưởng tới bao nhiêu thứ** | Sự cố làm sai 4 báo cáo phải trên phiếu chỉ ảnh hưởng 1 bảng tạm |
| Bấm vào là mở đúng màn xử lý | Không phải đi tìm |

> ⭐ **Đây là thứ biến DMP từ "tool phải nhớ vào" thành "tool tự nhắc việc".** Không có nó thì hàng chờ nào cũng có nguy cơ bị bỏ quên — mà bỏ quên hàng chờ chính là cách các tính năng quản trị chết dần.
>
> **Công sức thấp** — dữ liệu đã có ở năm menu, chỉ cần gộp lại một màn và bổ sung số đếm lên thanh điều hướng *(demo đã làm phần số đếm)*.

---

#### B2 · Cổng tiếp nhận yêu cầu dữ liệu 🔥🔥

**Một câu:** *nghiệp vụ cần dữ liệu thì điền một biểu mẫu chuẩn, thay vì nhắn tin — và yêu cầu đó trở thành một việc có người, có hạn, theo dõi được.*

**Vấn đề**

Hiện DMP có 5.3 xin **quyền truy cập vào bảng đã có**. Nhưng phần lớn yêu cầu thực tế là loại khác: ***"tôi cần số liệu X mà chưa biết có bảng nào chứa không"***. Loại này đang đi qua chat và **không để lại dấu vết nào**.

**Biểu mẫu nên hỏi gì**

| Trường | Vì sao |
|---|---|
| Cần dữ liệu gì — mô tả bằng lời | Không bắt nghiệp vụ biết tên bảng |
| Dùng để làm gì | ⭐ Quyết định BDA gợi ý bảng nào |
| Cần đến khi nào | Xếp thứ tự ưu tiên |
| Đã tự tìm chưa | Gắn kết quả tìm kiếm nếu có |

**Bốn kết cục có thể của một yêu cầu**

| Kết cục | Nghĩa |
|---|---|
| ✅ **Đã có sẵn** | BDA trỏ tới bảng có sẵn → chuyển thành yêu cầu quyền ở 5.3 |
| 🔧 Cần bổ sung | Bảng có nhưng thiếu cột → thành việc cho DE |
| 🆕 Cần làm mới | Thành yêu cầu dựng job mới |
| ❌ Không làm | Kèm lý do — **cũng phải lưu lại** |

> ⭐ **Giá trị lớn nhất không phải cái biểu mẫu, mà là con số nó tạo ra:** *bao nhiêu yêu cầu mỗi tháng · bao lâu thì được đáp ứng · bao nhiêu % hoá ra dữ liệu đã có sẵn mà người dùng không tìm thấy*.
>
> Con số cuối cùng đó **đo thẳng chất lượng của menu tìm kiếm và của metadata** — thứ hiện không có cách nào đo.

---

#### B3 · Bàn giao trách nhiệm hàng loạt 🔥🔥

**Một câu:** *một người nghỉ phép, chuyển việc hay nghỉ hẳn — chuyển toàn bộ bảng, job và việc đang chờ của họ sang người khác trong một thao tác.*

**Vấn đề**

Anh Hùng phụ trách **148 bảng**. Anh nghỉ phép hai tuần. Hiện phải:
- Mở từng bảng đổi đầu mối, hoặc
- Không đổi gì cả và **mọi cảnh báo trong hai tuần rơi vào hư không**

Vế thứ hai mới là thứ đang xảy ra trong thực tế.

**Màn bàn giao cần có**

| Việc | Chi tiết |
|---|---|
| Chọn người bàn giao và người nhận | |
| **Xem trước danh sách sẽ chuyển** | 148 bảng · 12 job · 5 việc đang chờ · 3 quyền phê duyệt |
| **Chọn kiểu** | Tạm thời *(có ngày về, tự trả lại)* hoặc vĩnh viễn |
| Loại trừ vài mục | Có thứ muốn giữ nguyên |
| Ghi vào nhật ký | Ai bàn giao cho ai, lúc nào |

> ⭐ Nối thẳng với con số đang có trong tài liệu: **9 tài khoản đã nghỉ việc mà chưa khoá, còn quyền trên 132 bảng**. Có màn bàn giao thì việc cho nghỉ việc trở thành **một thao tác có kiểm soát** thay vì một việc ai đó phải nhớ làm.

---

#### B4 · Xem trước tác động khi sửa metadata 🔥

**Một câu:** *trước khi lưu thay đổi định nghĩa thuật ngữ hay nhãn, hiện ngay ai và cái gì bị ảnh hưởng.*

Đề xuất **Đ9** ở phần trên làm việc này cho **thay đổi kỹ thuật** *(đổi kiểu cột)*. Chỗ này là cho **thay đổi nghĩa**:

> *Đổi định nghĩa thuật ngữ "Doanh thu ghi nhận" — đang gắn vào **18 cột** trên **7 bảng**, được **4 báo cáo** dùng. Ba đầu mối cần được báo.*

> 💡 **Đổi nghĩa nguy hiểm hơn đổi kiểu dữ liệu**, vì đổi kiểu thì job báo lỗi ngay, còn đổi nghĩa thì **mọi thứ vẫn chạy nhưng số được hiểu sai** — không ai phát hiện.

</details>

---

### Vai 2 — Người dùng nghiệp vụ

<details open>
<summary><b>Người cần số để làm việc, không quan tâm tới quản trị dữ liệu</b></summary>

**Ngày làm việc điển hình**

> Cần số doanh thu chi nhánh để làm báo cáo họp chiều. Không biết bảng nào có. Nhắn BDA. Chờ. Được trỏ tới một bảng. Không có quyền. Xin quyền. Chờ tiếp. Có quyền rồi thì **không biết số đó có tin được không**.

**Năm tắc nghẽn**

| # | Tắc ở đâu | Đề xuất |
|:---:|---|---|
| **1** | Xin quyền rồi **không biết đang chờ ai, bao giờ xong** | **E1 · Theo dõi tiến trình như theo dõi đơn hàng** |
| **2** | ⭐ **Dữ liệu hỏng nhưng người dùng không được báo** — chỉ đầu mối được báo | **E2 · Đăng ký theo dõi bảng và báo cáo** |
| **3** | Có số rồi **không biết có tin được không** | **E3 · Nhãn tin cậy đi kèm số liệu** |
| **4** | Thấy số sai **không biết báo cho ai** | **E4 · Báo vấn đề ngay tại chỗ** |
| **5** | Không biết **ai khác đang dùng cùng dữ liệu** để hỏi | **E5 · Người dùng khác của bảng này** |

---

#### ⭐ E2 · Đăng ký theo dõi bảng và báo cáo 🔥🔥🔥

**Một câu:** *bấm "theo dõi" một bảng hoặc báo cáo — có sự cố, đổi cấu trúc hay chậm dữ liệu thì được báo, dù mình không phải người phụ trách.*

**Đây là lỗ hổng lớn nhất trong toàn bộ thiết kế hiện tại**

Toàn bộ cơ chế cảnh báo đang gửi cho **đầu mối phụ trách**. Nhưng người **chịu hậu quả** của dữ liệu sai lại là **người dùng nó** — và họ **không nằm trong danh sách nhận cảnh báo nào cả**.

> Kết quả thực tế: bảng hỏng lúc 6 giờ sáng, đầu mối biết và đang xử lý. Người làm báo cáo **không biết gì**, vẫn lấy số lúc 9 giờ, mang vào họp lúc 2 giờ chiều.

**Cần có gì**

| Việc | Chi tiết |
|---|---|
| Nút **Theo dõi** trên mọi bảng, báo cáo, chỉ tiêu | Ở 1.1 và 1.3 |
| **Tự động theo dõi** thứ mình hay dùng | Suy từ nhật ký truy cập ở 5.4 — không bắt người dùng nhớ bấm |
| Chọn muốn nhận gì | Chỉ sự cố nghiêm trọng · mọi sự cố · cả thay đổi cấu trúc |
| Thông báo **viết bằng lời người dùng hiểu** | Không phải *"luật not_null hỏng"* mà *"số liệu bảng doanh thu hôm nay chưa tin cậy, đang xử lý, dự kiến xong 10 giờ"* |

> ⭐ **Đây là tính năng đổi hẳn cảm nhận về tool.** Từ *"công cụ của đội kỹ thuật"* thành *"thứ bảo vệ tôi khỏi mang số sai vào họp"*. Và nó **dùng lại toàn bộ hạ tầng cảnh báo đã có ở 3.4** — chỉ mở rộng danh sách người nhận.

---

#### ⭐ E3 · Nhãn tin cậy đi kèm số liệu 🔥🔥

**Một câu:** *mọi chỗ hiện số liệu đều kèm một nhãn nhỏ cho biết số này lấy lúc nào và có đang tin được không.*

Đề xuất **4** ở phần trên lan cờ tin cậy **trong DMP**. Chỗ này đi xa hơn: **đưa nhãn đó ra ngoài, tới nơi người dùng thật sự nhìn số** — công cụ báo cáo, file xuất Excel.

| Nơi hiện số | Nhãn kèm theo |
|---|---|
| Báo cáo trên công cụ BI | *Số liệu tính lúc 07:11 hôm nay · ✅ nguồn tin cậy* |
| File Excel xuất ra | Thêm một dòng đầu ghi thời điểm và trạng thái |
| Kết quả truy vấn | *⚠️ Bảng nguồn đang có sự cố chưa đóng* |

> 💡 **Việc khó không phải kỹ thuật mà là tích hợp** — phải chạm vào công cụ báo cáo. Nên làm **file xuất Excel trước** *(dễ nhất, DMP kiểm soát được)*, rồi mới tính tới công cụ BI.

---

#### E1 · Theo dõi tiến trình yêu cầu 🔥

Người xin quyền hiện **gửi xong là mất dấu**. Cần một màn *"yêu cầu của tôi"* hiện: đang ở bước nào · **đang chờ ai** · đã chờ bao lâu · dự kiến bao giờ xong *(dựa trên thời gian duyệt trung bình)* · nút **nhắc khéo** người duyệt.

> ⭐ Cột **"đang chờ ai"** là thứ tạo áp lực xã hội lành mạnh — người duyệt biết mình đang bị nhìn thì xử lý nhanh hơn. Và nó cho lãnh đạo thấy **nút thắt nằm ở người nào**.

---

#### E4 · Báo vấn đề ngay tại chỗ 🔥🔥

**Một câu:** *người dùng thấy số trông sai thì bấm một nút ngay trên bảng, thành một phiếu có người nhận — thay vì nhắn tin rồi thôi.*

**Vì sao đáng làm**

Người dùng nghiệp vụ thường là **người đầu tiên phát hiện dữ liệu sai** — vì họ biết con số đó **lẽ ra phải khoảng bao nhiêu**. Luật chất lượng không bắt được loại lỗi này *(số đúng định dạng, đúng khoảng, nhưng sai nghĩa)*.

Hiện phản hồi đó **đi vào chat rồi biến mất**. Có nút báo thì nó thành **phiếu ở 3.3**, tự gán cho đầu mối, và quan trọng hơn — **thành dữ liệu để sinh luật chất lượng mới**.

> ⭐ **Vòng lặp đáng giá nhất:** người dùng báo sai → BDA xác nhận → **sinh một luật chất lượng để lần sau máy tự bắt**. Đây là cách con số *0,6% bảng được kiểm* tăng lên theo đúng thứ tự ưu tiên thực tế — bảng nào hay sai thì được kiểm trước.

---

#### E5 · Ai khác đang dùng bảng này 🔥

Hiện muốn hỏi gì về một bảng thì **chỉ có một cửa: đầu mối phụ trách** — và đầu mối thành nút thắt.

Hiện thêm *"5 người dùng nhiều nhất bảng này"* và *"3 báo cáo đang dùng"* thì người dùng **hỏi đồng nghiệp đã làm việc với bảng đó**, nhanh hơn và không làm phiền BDA.

> 💡 Dữ liệu đã có sẵn ở nhật ký truy cập **5.4**. Chỉ cần hiện lên — nhưng **chỉ hiện tên, không hiện họ đã truy vấn gì**.

</details>

---

### Vai 3 — Ban lãnh đạo

<details open>
<summary><b>Ba câu hỏi lãnh đạo thật sự quan tâm</b></summary>

Màn 8.1 hiện trả lời *"dữ liệu khoẻ hay yếu"*. Nhưng lãnh đạo còn ba câu khác mà tool **chưa trả lời được**:

| Câu hỏi | Hiện có trả lời được không |
|---|:---:|
| *"Đội đang tắc ở đâu?"* | ❌ |
| *"Đơn vị nào làm tốt, đơn vị nào chậm?"* | ⚠️ có bảng theo miền nhưng chưa so sánh được |
| *"Tuần này rủi ro lớn nhất là gì?"* | ❌ |

---

#### ⭐ L1 · Bảng điều khiển tắc nghẽn quy trình 🔥🔥🔥

**Một câu:** *DMP đang đo chất lượng dữ liệu — nhưng chưa ai đo chính quy trình của DMP đang tắc ở đâu.*

**Đây là đề xuất tôi thấy sắc nhất trong cả phần này**, vì nó dùng đúng dữ liệu DMP tự sinh ra mà **chưa ai nghĩ tới việc đọc lại**.

| Chỉ số | Nói lên điều gì | Dữ liệu lấy từ |
|---|---|---|
| **Thời gian từ lúc xin tới lúc có dữ liệu** | Chỉ số quan trọng nhất với người dùng | 5.3 |
| **Người duyệt nào đang là nút thắt** | ⭐ Ai giữ hồ sơ lâu nhất | 5.3 · 2.4 |
| **Tỷ lệ hồ sơ bị trả về** | Cao thì **biểu mẫu khai đang khó hiểu**, không phải người khai kém | 2.4 |
| **Việc tồn đọng lâu nhất ở trạng thái nào** | Chỗ quy trình bị nghẽn | mọi hàng chờ |
| **Tỷ lệ việc quá hạn** | Đội đang quá tải hay không | 3.3 · 5.3 · 6.3 |
| **Sự cố lặp lại trên cùng một bảng** | Chữa triệu chứng chứ chưa chữa gốc | 3.3 |

**Ba chỉ số tôi cho là đáng nhất**

> ⭐ **Người duyệt nào đang là nút thắt** — thường cả tổ chức biết mơ hồ nhưng không ai có số. Có số thì giải quyết được bằng **phân thêm người duyệt**, không phải bằng giục.
>
> ⭐ **Tỷ lệ hồ sơ bị trả về** — nếu 40% hồ sơ khai bảng bị trả về thì vấn đề nằm ở **biểu mẫu hoặc hướng dẫn**, không phải ở người khai. Đây là chỉ số **tự chỉ ra lỗi thiết kế của chính tool**.
>
> ⭐ **Sự cố lặp lại trên cùng một bảng** — một bảng hỏng 6 lần trong 3 tháng nghĩa là **6 lần chữa triệu chứng**. Đây là danh sách ưu tiên sửa gốc.

---

#### L2 · So sánh giữa các đơn vị và giao chỉ tiêu 🔥🔥

Màn 8.1 đã có bảng theo miền. Thêm hai thứ để nó **dùng được cho việc quản lý**:

| Thêm | Vì sao |
|---|---|
| **Xu hướng theo tháng của từng miền** | Miền nào đang tiến, miền nào đứng yên |
| ⭐ **Chỉ tiêu giao cho từng miền và tiến độ** | *"Miền Vận hành: gán đầu mối cho 500 bảng trong quý III — đã làm 180/500"* |

> ⭐ **Không giao chỉ tiêu chung cho cả công ty** — kiểu *"nâng điểm chất lượng lên 90"* thì không ai biết bắt đầu từ đâu. Giao **theo miền, có tên người chịu trách nhiệm, có con số cụ thể**.

---

#### L3 · Ba rủi ro lớn nhất tuần này 🔥🔥

Thay vì mười chỉ số ngang hàng, hiện **đúng ba dòng** ở đầu màn 8.1 — máy tự xếp hạng theo **mức ảnh hưởng × mức khẩn**:

> 🔴 *Bảng `bi.doi_soat_giao_dich_A` hỏng 3 ngày liên tiếp — 6 báo cáo đang đọc số sai*
> 🟠 *12 quyền truy cập dữ liệu nhạy cảm hết hạn tuần này mà chưa ai xin gia hạn*
> 🟠 *Kỳ đánh giá tuân thủ quý III còn 2 tuần, 8 mục kiểm chưa chạy*

> ⭐ **Lãnh đạo không có thời gian đọc mười chỉ số.** Ba dòng có thứ tự ưu tiên rõ ràng thì dùng được ngay trong cuộc họp giao ban.

</details>

---

<details open>
<summary><b>⭐ Tóm tắt — mười hai đề xuất từ góc nhìn người dùng</b></summary>

| # | Đề xuất | Vai | Tắc nghẽn giải được | Công sức | Giá trị |
|:---:|---|:---:|---|:---:|:---:|
| **B1** | ⭐ Hộp thư "Việc của tôi" | BDA | Việc rải ở 5–6 menu | **Thấp** | 🔥🔥🔥 |
| **B2** | Cổng tiếp nhận yêu cầu dữ liệu | BDA | Yêu cầu qua chat, không dấu vết | Trung bình | 🔥🔥 |
| **B3** | Bàn giao trách nhiệm hàng loạt | BDA | Nghỉ phép là cảnh báo rơi vào hư không | Thấp | 🔥🔥 |
| **B4** | Xem trước tác động khi sửa nghĩa | BDA | Đổi nghĩa không ai biết | Trung bình | 🔥 |
| **E1** | Theo dõi tiến trình yêu cầu | Người dùng | Gửi xong mất dấu | Thấp | 🔥 |
| **E2** | ⭐ Đăng ký theo dõi bảng, báo cáo | Người dùng | **Người dùng không được báo khi dữ liệu hỏng** | Thấp | 🔥🔥🔥 |
| **E3** | Nhãn tin cậy đi kèm số liệu | Người dùng | Có số mà không biết tin được không | Cao | 🔥🔥 |
| **E4** | ⭐ Báo vấn đề ngay tại chỗ | Người dùng | Phản hồi đi vào chat rồi mất | **Thấp** | 🔥🔥 |
| **E5** | Ai khác đang dùng bảng này | Người dùng | Đầu mối thành nút thắt | **Thấp** | 🔥 |
| **L1** | ⭐ Bảng điều khiển tắc nghẽn quy trình | Lãnh đạo | **Không ai đo được quy trình đang tắc đâu** | Trung bình | 🔥🔥🔥 |
| **L2** | So sánh miền và giao chỉ tiêu | Lãnh đạo | Không giao được việc cụ thể | Thấp | 🔥🔥 |
| **L3** | Ba rủi ro lớn nhất tuần này | Lãnh đạo | Mười chỉ số ngang hàng, không biết lo cái nào | **Thấp** | 🔥🔥 |

**Bốn cái nên làm trước — công sức thấp, giá trị cao, dữ liệu đã có**

| Chọn | Vì sao |
|---|---|
| ⭐ **B1** Hộp thư "Việc của tôi" | Gộp thứ đã có. **Không có nó thì mọi hàng chờ đều có nguy cơ bị bỏ quên** — và đó là cách tính năng quản trị chết dần |
| ⭐ **E2** Đăng ký theo dõi | Lấp **lỗ hổng lớn nhất**: người chịu hậu quả của dữ liệu sai lại không được báo |
| ⭐ **E4** Báo vấn đề tại chỗ | Rẻ, và tạo **vòng lặp**: người dùng báo sai → sinh luật chất lượng mới → tăng độ phủ theo đúng ưu tiên thực tế |
| ⭐ **L1** Tắc nghẽn quy trình | Dùng dữ liệu DMP **tự sinh ra mà chưa ai đọc lại** |

> ⭐ **Một nhận xét về cả bốn:** không cái nào cần AI, không cái nào cần hạ tầng mới. Chúng chỉ **nối lại thứ đã có** và **mở rộng đối tượng phục vụ từ người quản trị sang người dùng**.
>
> Đây có lẽ là điểm yếu lớn nhất của thiết kế hiện tại: **27 menu gần như đều phục vụ người quản trị dữ liệu. Người dùng cuối — nhóm đông nhất — gần như không có màn nào của riêng họ.**

</details>

---

## Nguồn

<details open>
<summary><b>Các bài đã đọc — kèm lưu ý về tính khách quan</b></summary>

| Chủ đề | Nguồn |
|---|---|
| Danh mục dữ liệu và tính năng AI | [Atlan — Data Catalog Tools 2026](https://atlan.com/data-catalog-tools/) · [Atlan — Data Catalog for AI](https://atlan.com/know/data-catalog-for-ai/) · [Techno-Pulse — Alation vs Collibra vs Atlan vs DataHub](https://www.techno-pulse.com/2026/05/best-ai-data-catalog-tools-in-2026.html) · [StackFYI — so sánh bốn công cụ](https://www.stackfyi.com/guides/data-catalog-tools-atlan-collibra-datahub-openmetadata-2026) |
| Giám sát dữ liệu, phát hiện bất thường | [DataKitchen — Bối cảnh phần mềm 2026](https://datakitchen.io/the-2026-data-quality-and-data-observability-commercial-software-landscape/) · [Decube — So sánh công cụ giám sát](https://www.decube.io/post/best-data-observability-tools) · [DQLabs — Giám sát và phát hiện bất thường](https://www.dqlabs.ai/blog/data-pipeline-monitoring-and-anomaly-detection/) · [Atlan — Công cụ giám sát dữ liệu](https://atlan.com/know/data-observability-tools/) |
| **Quản trị dữ liệu tự hành, phân loại dữ liệu nhạy cảm bằng AI** | [Atlan — Automated PII Classification](https://atlan.com/know/data-governance/automated-pii-classification/) · [Atlan — Xử lý dữ liệu cá nhân trong luồng AI](https://atlan.com/know/ai-agent/data-for-ai/how-to-handle-pii-in-ai-pipelines/) · [Acceldata — Agent thực thi chính sách dữ liệu](https://www.acceldata.io/blog/how-governance-aware-ai-agents-enforce-data-policies) · [OvalEdge — Khung tự động hoá quản trị bằng agent](https://www.ovaledge.com/blog/ai-agents-data-governance-automation) · [arXiv — AI trong quản lý metadata](https://arxiv.org/pdf/2501.16605) |
| **Tối ưu SQL, dự báo tài nguyên, chi phí hạ tầng** | [Datadog — giảm 44% chi phí Spark bằng trợ lý AI](https://www.datadoghq.com/blog/using-agentic-ai-with-jobs-monitoring/) · [arXiv 2026 — Dự báo tài nguyên truy vấn trước khi chạy](https://arxiv.org/html/2604.20145v1) · [EDBT — Tối ưu giá/hiệu năng cho truy vấn](https://openproceedings.org/2023/conf/edbt/paper-186.pdf) · [Datavidhya — AI cho tối ưu truy vấn](https://datavidhya.com/learn/ai-for-data-engineering/ai-for-sql/ai-query-optimization/) |
| Gian hàng dữ liệu, cam kết dữ liệu | [Alation — Data Marketplace là gì](https://www.alation.com/blog/what-is-data-marketplace-benefits-challenges/) · [Murdio — Gian hàng so với danh mục](https://murdio.com/insights/data-marketplace-vs-data-catalog/) · [Harbr — Catalog vs Marketplace](https://www.harbrdata.com/blog/data-catalog-vs-data-marketplace) · [Huwise — Tính năng gian hàng dữ liệu](https://www.huwise.com/en/blog/key-features-data-product-marketplace/) |

> ⚠️ **Lưu ý khi trích dẫn cho lãnh đạo:** Atlan, Alation, Decube, DQLabs, Huwise **đều là hãng bán sản phẩm trong lĩnh vực này**. Phần **mô tả tính năng và xu hướng** thì nhiều nguồn trùng khớp nên tin được; phần **so sánh hơn kém giữa các hãng** thì nên bỏ qua.
>
> Các con số dự báo thị trường *(kiểu "50% doanh nghiệp sẽ áp dụng vào 2026")* trong các bài này **dẫn lại từ hãng phân tích mà tôi chưa kiểm chứng được bản gốc** — không nên đưa vào tài liệu trình lãnh đạo.

</details>
