# Review đối chiếu — Thiết kế DMP ↔ Yêu cầu đội BDA

### Rà soát toàn bộ 6 tài liệu yêu cầu (Phương án + GĐ1 → GĐ5) với thiết kế 21 menu / 55 màn của DMP

| | |
|---|---|
| **Mục đích** | Trả lời một câu hỏi: **thiết kế DMP hiện tại đã phủ hết yêu cầu BDA chưa** — và nếu chưa thì thiếu gì, sửa thế nào |
| **Đầu vào** | `Yêu cầu từ BDA/` — 6 tệp `.docx` · `docs/DMP-De-xuat-tool-Data-Management.md` v2.1 · `docs/DMP-Plan-Dung-Demo-FE.md` |
| **Ngày** | 09/08/2026 |
| **Kết luận ngắn** | ⚠️ **Phủ khoảng 62%.** Phần đã làm thì làm rất sâu — nhưng **thiếu hẳn 2 nhóm chức năng cấp giai đoạn** (Chính sách & Tuân thủ, Quản lý dữ liệu chủ) và **3 loại đối tượng dữ liệu bắt buộc** (Hệ thống · Kênh trao đổi · Báo cáo/Chỉ tiêu) |

---

## 0. Tóm tắt cho lãnh đạo — đọc 60 giây

<details open>
<summary><b>Ba câu</b></summary>

**Câu 1 — Cái đang có thì tốt.** Module ① Data Catalog, ③ Data Quality, ⑤ Data Security của DMP **sâu hơn yêu cầu BDA**: BDA chỉ yêu cầu "che dữ liệu nhạy cảm", DMP đã thiết kế 8 kiểu che kèm câu SQL viết lại; BDA yêu cầu 4 trạng thái phiếu lỗi, DMP thiết kế 6 trạng thái có nguyên tắc 4 mắt.

**Câu 2 — Cái thiếu là thiếu cả nhóm, không phải thiếu chi tiết.** Yêu cầu BDA có **6 nhóm chức năng**; DMP phủ 4. Hai nhóm chưa có dòng nào trong thiết kế:
- **Chính sách & Tuân thủ dữ liệu** (Phương án §5.6, GĐ4 FR-05/FR-06) — chính sách, vòng đời lưu trữ/xóa, chia sẻ bên thứ ba, checklist tuân thủ, kế hoạch khắc phục.
- **Quản lý dữ liệu chủ — MDM** (Phương án §5.4, toàn bộ GĐ5) — mô hình dữ liệu chuẩn, phát hiện trùng, Golden Record, phân phối.

**Câu 3 — Gap nguy hiểm nhất không phải MDM mà là "Báo cáo & Chỉ tiêu".** GĐ2 §3 liệt kê **7 nhóm đối tượng bắt buộc quản lý**; DMP chỉ quản lý 3,5 nhóm. Trong đó **Báo cáo & Chỉ tiêu** là đối tượng mà GĐ2 §5.5 đặc tả tới **8 nhóm trường** — và là **đích cuối của mọi câu hỏi nghiệp vụ BDA đặt ra** ("chỉ tiêu này lấy từ đâu", "báo cáo nào bị ảnh hưởng"). Không có thực thể Báo cáo/Chỉ tiêu thì **lineage của DMP dừng ở bảng, không tới được đích** — mà đó chính là giá trị BDA muốn.

</details>

---

## 1. Bản đồ phủ — 6 nhóm chức năng BDA × 6 module DMP

<details open>
<summary><b>Nhóm nào đã có chủ, nhóm nào chưa</b></summary>

| # | Nhóm chức năng BDA *(Phương án §5)* | Module DMP tương ứng | Mức phủ | Nhận xét |
|:---:|---|---|:---:|---|
| **5.1** | Danh mục & Thông tin mô tả dữ liệu | ① Data Catalog + ② Governance | 🟡 **65%** | Bảng/cột rất mạnh. **Thiếu 3 loại đối tượng** và **thiếu màn tìm kiếm** |
| **5.2** | Quản lý chất lượng dữ liệu | ③ Data Quality | 🟢 **90%** | Vượt yêu cầu. Thiếu bước *kiểm tra lại tự động* trước khi đóng lỗi |
| **5.3** | Phân loại & Bảo mật dữ liệu | ⑤ Data Security | 🟡 **75%** | Che dữ liệu/lọc dòng/xin quyền rất tốt. **Thiếu trục "mức phân loại 4 cấp"** và **giám sát truy cập bất thường** |
| **5.4** | **Quản lý dữ liệu chủ (MDM)** | — | 🔴 **0%** | **Không có menu nào** |
| **5.5** | Truy vết luồng dữ liệu (Lineage) | tab trong ① | 🟡 **55%** | Thiết kế "lineage là tab" hợp lý nhưng **chưa đủ** — xem §4 |
| **5.6** | **Chính sách & Tuân thủ dữ liệu** | — *(chỉ có Nhật ký kiểm toán)* | 🔴 **15%** | **Không có menu chính sách, vòng đời, tuân thủ** |
| — | *(ngoài yêu cầu BDA)* Nạp & Điều phối | ④ Ingestion & Orchestration | ➕ | **Giữ** — là bối cảnh SQLWF thật, và GĐ2 §3 có yêu cầu quản lý *"Job và tiến trình xử lý dữ liệu"* |
| — | Chức năng nền *(Phương án §6)* | ⑤ + ⑥ | 🟡 **70%** | Thiếu **hàng đợi phê duyệt dùng chung** |

**Điểm phủ tổng: ~62%.**

</details>

---

## 2. Gap A — Ba loại đối tượng dữ liệu bắt buộc chưa có trong danh mục

<details open>
<summary><b>GĐ2 §3 yêu cầu 7 nhóm đối tượng — DMP đang quản lý mấy nhóm</b></summary>

| # | Nhóm đối tượng *(GĐ2 §3)* | DMP hiện có | Kết luận |
|:---:|---|---|:---:|
| 1 | **Hệ thống và nơi lưu trữ dữ liệu** | Chỉ có *Kết nối* trong 6.2 Cấu hình hệ thống — thiên về JDBC/FTP/Kafka, **không có** đơn vị quản lý · đầu mối kỹ thuật · môi trường · trạng thái sử dụng · mục đích | 🔴 **Thiếu** |
| 2 | Bảng và cột dữ liệu | 1.1 Bảng dữ liệu — 6 tab, rất đầy đủ | 🟢 **Đủ** |
| 3 | Job và tiến trình xử lý dữ liệu | 4.1 Luồng xử lý — có DAG, bước, lịch, phiên bản | 🟡 **Gần đủ** — thiếu *mục đích xử lý* · *người phụ trách* như trường metadata, và job **không xuất hiện trong tra cứu danh mục chung** |
| 4 | **Kênh trao đổi dữ liệu** *(API · Kafka · FTP)* | 4.2 Cửa nạp chỉ quản lý **chiều vào**. Không có: hệ thống gửi ↔ hệ thống nhận · phương thức xác thực · dữ liệu/định dạng trao đổi · kênh **đi ra** | 🔴 **Thiếu** |
| 5 | **Thông tin nghiệp vụ (Báo cáo, Chỉ tiêu)** | Không có thực thể. Chỉ là chuỗi văn bản *"6 báo cáo dùng bảng này"* trong `consumers[]` | 🔴 **Thiếu — nghiêm trọng nhất** |
| 6 | Thuật ngữ nghiệp vụ | 2.1 Business Glossary — có CDE, steward, phân cấp, duyệt | 🟢 **Vượt yêu cầu** |
| 7 | Quan hệ luồng dữ liệu (Lineage) | Tab *Nguồn gốc* trong 1.1 | 🟡 **Chưa đủ** — xem §4 |

</details>

<details open>
<summary><b>⭐ Vì sao "Báo cáo & Chỉ tiêu" là gap nghiêm trọng nhất — không phải MDM</b></summary>

GĐ2 §5.5 đặc tả **8 nhóm trường** cho riêng đối tượng này — nhiều hơn cả bảng/cột:

| Trường BDA yêu cầu | DMP có chỗ để lưu không |
|---|:---:|
| Thông tin chung báo cáo *(tên, mô tả, mục đích, đơn vị sở hữu, người phụ trách)* | ❌ |
| Danh sách chỉ tiêu trong báo cáo | ❌ |
| Dữ liệu và nguồn dữ liệu sử dụng *(bảng/cột nguồn)* | ⚠️ chỉ ngược lại: bảng → tên báo cáo dạng chữ |
| **Định nghĩa và công thức tính từng chỉ tiêu** | ⚠️ nằm nhờ ở Glossary, nhưng Glossary là *thuật ngữ*, không phải *chỉ tiêu của một báo cáo* |
| Điều kiện lấy dữ liệu, quy tắc tính toán, tổng hợp | ❌ |
| Tần suất cập nhật & thời gian dữ liệu sẵn sàng | ❌ |
| Hình thức đầu ra *(màn hình / bảng / file)* | ❌ |
| Đối tượng, đơn vị sử dụng báo cáo | ❌ |

**Hệ quả dây chuyền — bốn chỗ hỏng theo:**

| Chỗ hỏng | Vì sao |
|---|---|
| **Lineage không tới đích** | GĐ2 FR-06 yêu cầu chuỗi *"nguồn → job → bảng đích → **báo cáo, chỉ tiêu**"*. Thiếu 2 mắt xích cuối, sơ đồ nguồn gốc của DMP dừng ở bảng |
| **Phân tích ảnh hưởng thành phỏng đoán** | Màn 6 có nút *"Phân tích ảnh hưởng → liệt kê 6 báo cáo"* — nhưng 6 báo cáo đó là **chuỗi chữ tự do**, không phải bản ghi. Không bấm vào được, không biết ai dùng, không biết chỉ tiêu nào hỏng |
| **Chất lượng không áp được lên báo cáo/chỉ tiêu** | GĐ3 §3 ghi rõ đối tượng áp dụng gồm *"báo cáo, chỉ tiêu"*. DMP chỉ gán luật cho bảng/cột |
| **Chỉ số nghiệm thu không tính được** | GĐ2 §10 có chỉ số *"Tỷ lệ báo cáo/chỉ tiêu truy vết được đến nguồn"* — không có thực thể thì không có mẫu số |

</details>

**➡️ Đề xuất sửa:** thêm **3 menu** vào Module ①
`1.x Hệ thống & Nguồn dữ liệu` · `1.x Kênh trao đổi dữ liệu` · `1.x Báo cáo & Chỉ tiêu` *(2 cấp: Báo cáo → Chỉ tiêu)*

---

## 3. Gap B — Hai nhóm chức năng cấp giai đoạn chưa có trong thiết kế

<details open>
<summary><b>B1 — Chính sách & Tuân thủ dữ liệu (Phương án §5.6 · GĐ4 FR-05, FR-06)</b></summary>

| Yêu cầu BDA | DMP hiện có | Mức |
|---|---|:---:|
| Quản lý **danh mục chính sách**: nội dung · phạm vi áp dụng · ngày hiệu lực · đơn vị ban hành · phiên bản | — | 🔴 |
| **Vòng đời dữ liệu**: thời gian sử dụng · thời gian lưu trữ · lưu kho (archive) · điều kiện xóa | — | 🔴 |
| **Mục đích xử lý · phạm vi sử dụng · chia sẻ cho bên thứ ba** *(mục đích, phạm vi, thời hạn)* | — | 🔴 |
| **Checklist đánh giá tuân thủ** · ghi nhận phát hiện không phù hợp · **kế hoạch khắc phục** *(nội dung, người phụ trách, hạn)* | — | 🔴 |
| Lưu bằng chứng: chính sách · nhật ký quyền · nhật ký truy cập · lịch sử metadata · kết quả kiểm tra chất lượng | ⚠️ có 4/5 mảnh nhưng **rời rạc, không có hồ sơ bằng chứng gộp theo kỳ đánh giá** | 🟡 |

> ⚠️ **Đây là phần lãnh đạo và kiểm toán hỏi đầu tiên.** GĐ4 §10 đặt câu hỏi nghiệm thu: *"Có đủ bằng chứng để chứng minh việc tuân thủ khi được kiểm tra không?"* — DMP hiện chỉ trả lời được vế nhật ký, không trả lời được vế chính sách và vế đánh giá.

</details>

<details open>
<summary><b>B2 — Quản lý dữ liệu chủ / MDM (Phương án §5.4 · toàn bộ GĐ5)</b></summary>

| FR *(GĐ5)* | Nội dung | DMP |
|:---:|---|:---:|
| FR-01 | Thiết kế **mô hình dữ liệu chuẩn** — thuộc tính bắt buộc, khóa định danh, quy tắc sinh mã | 🔴 |
| FR-02 | **Thu thập & chuẩn hóa** dữ liệu từ nhiều hệ thống nguồn | 🔴 |
| FR-03 | **Phát hiện bản ghi trùng** — so khớp, danh sách nghi ngờ, không tự động hợp nhất | 🔴 |
| FR-04 | **Tạo bản ghi chuẩn (Golden Record)** — hợp nhất, lưu liên kết ngược, lịch sử thay đổi | 🔴 |
| FR-05 | **Phân phối dữ liệu chuẩn** — API / theo lô / theo sự kiện | 🔴 |
| FR-06 | Mở rộng phạm vi quản trị | 🔴 |

> 💡 **Nhưng đây là gap "đúng lịch".** GĐ5 là giai đoạn **cuối** và kế thừa GĐ1–4. Không sai khi DMP chưa thiết kế sâu — **cái sai là không có ô nào trên bản đồ menu**, khiến lãnh đạo đọc tài liệu sẽ hiểu là "tool này không làm MDM".
>
> **Cách xử lý đúng:** đưa MDM vào **thành một module có mặt trên thanh điều hướng**, thiết kế ở mức khung *(4 menu)*, ghi rõ *"triển khai ở Đợt 5"*. Vừa không phình khối lượng đợt 1, vừa cho thấy tool có đường đi tới cuối lộ trình.

</details>

---

## 4. Gap C — Lineage: thiết kế "chỉ là tab" đúng một nửa

<details open>
<summary><b>Lập luận của DMP và chỗ nó hụt</b></summary>

**Lập luận của DMP** *(tài liệu đề xuất, §4 Module ①)*:
> *"Nguồn gốc dữ liệu không có gì để khai, không có gì để tạo — nó được sinh tự động từ câu SQL của job. Và người dùng luôn xuất phát từ một bảng cụ thể."*

**Nhận xét: đúng cho 70% tình huống, hụt ở 30% còn lại** — và 30% đó là phần BDA yêu cầu tường minh:

| Yêu cầu GĐ2 FR-06 / §5.7 | Tab "Nguồn gốc" giải quyết được? |
|---|:---:|
| Truy vết ở mức **hệ thống** | ❌ tab chỉ có mức bảng/cột — không có góc nhìn "hệ thống A cấp dữ liệu cho hệ thống B" |
| Truy vết ở mức **nghiệp vụ** *(chỉ tiêu ← bảng ← nguồn)* | ❌ chưa có thực thể chỉ tiêu |
| **Cho phép khai báo thủ công** khi không thu thập tự động được | ❌ **DMP nói thẳng là "không có gì để khai"** — trái với yêu cầu BDA |
| Lưu **"bước biến đổi chính"**, **"mức truy vết"**, **"lịch chạy liên quan"** như trường dữ liệu | ❌ |
| **Trạng thái phê duyệt** cho lineage khai thủ công *(GĐ2 §8 áp cho cả lineage)* | ❌ |
| Phân tích ảnh hưởng → *"xác định bảng đích, báo cáo, chỉ tiêu và **người dùng** bị ảnh hưởng"* | 🟡 có nút, nhưng dữ liệu đích là chuỗi chữ |

**➡️ Đề xuất sửa — giữ tab, thêm 1 menu:**

| Giữ nguyên | Thêm mới |
|---|---|
| Tab *Nguồn gốc* trong chi tiết bảng — vẫn là lối vào chính, đúng thói quen người dùng | Menu **`Truy vết luồng dữ liệu`** trong Module ② với 3 tab:<br>① **Bản đồ luồng** *(lọc theo hệ thống/miền, xem mức hệ thống → bảng → cột → chỉ tiêu)*<br>② **Khai báo thủ công** *(danh sách quan hệ khai tay, có 5 trạng thái phê duyệt)*<br>③ **Phân tích ảnh hưởng** *(chọn đối tượng → ra danh sách bảng · báo cáo · chỉ tiêu · **người dùng** bị ảnh hưởng, xuất được)* |

</details>

---

## 5. Gap D — Mười điểm chi tiết cần sửa trong các module đã có

<details open>
<summary><b>Bảng gap chi tiết — có mã để theo dõi</b></summary>

| Mã | Ở đâu | Yêu cầu BDA | Hiện trạng DMP | Sửa thế nào |
|:---:|---|---|---|---|
| **D1** | ⑤ Security 2.2 Classification | GĐ4 FR-01: phân loại **4 mức — Công khai · Nội bộ · Mật · Hạn chế truy cập** | DMP dùng `PD_BASIC` / `PD_SENSITIVE` / `DATA_GENERAL` — đây là **loại dữ liệu nhạy cảm**, không phải **mức phân loại**. **Đang trộn 2 trục làm 1** | Tách thành **2 trục độc lập**: ① *Mức phân loại* (4 cấp, gán cho bảng/cột/báo cáo) ② *Nhãn dữ liệu nhạy cảm* (số ĐT, CCCD, số tài khoản…). Chính sách che viết theo trục ②, hạn chế tải xuống viết theo trục ① |
| **D2** | ② Governance | GĐ2 FR-05 + §8: quy trình **5 trạng thái** *(Dự thảo · Chờ phê duyệt · Yêu cầu chỉnh sửa · Đã phê duyệt · Ngừng sử dụng)* áp cho **mọi** metadata và cả lineage thủ công | Chỉ Glossary và Danh mục tham chiếu có duyệt. Bảng/cột/job **không có** trạng thái phê duyệt. Không có **hàng đợi "Chờ tôi duyệt"** | Thêm menu **`Phê duyệt & Phiên bản`**: hàng đợi gộp mọi loại đối tượng, có *Duyệt · Yêu cầu chỉnh sửa · Từ chối*, và tab *So sánh phiên bản* |
| **D3** | ① Catalog | GĐ2 FR-04: **tìm kiếm** theo tên · hệ thống · nhóm lĩnh vực · người phụ trách; lọc theo loại đối tượng · mức quan trọng · trạng thái | Tài liệu nêu "thiếu tìm kiếm toàn văn" nhưng **không có màn tìm kiếm nào trong 55 màn** | Thêm màn **`Tìm kiếm toàn hệ thống`** — một ô tìm, kết quả gộp mọi loại đối tượng, có bộ lọc mặt (facet) bên trái |
| **D4** | ① Catalog 1.1 | GĐ1 §2.3 + GĐ2 §9: **5 vai trò**, trong đó **Người sở hữu dữ liệu** là người **phê duyệt** | DMP chỉ có `BDA` *(≈ đầu mối nghiệp vụ)* và `DE` *(≈ đầu mối kỹ thuật)*. **Thiếu hẳn vai trò Người sở hữu dữ liệu** — mà đây là người duyệt định nghĩa và duyệt cấp quyền | Thêm trường **Người sở hữu dữ liệu (Data Owner)** trên mọi đối tượng, tách khỏi BDA. Gán quyền duyệt cho vai trò này |
| **D5** | ③ Quality 3.4 | GĐ3 FR-04 + §6.1: sau khi xử lý phải **kiểm tra lại tự động** rồi mới đóng; nếu vẫn hỏng thì **quay về trạng thái phân công** | DMP có 6 trạng thái nhưng *Chờ duyệt* là **4 mắt của người**, không phải **máy chạy lại luật**. Thiếu vòng lặp "hỏng lại → mở lại phiếu" | Bổ sung trạng thái **`Chờ kiểm tra lại`** + nút *Chạy kiểm tra lại*, và luồng quay lui khi kết quả vẫn không đạt |
| **D6** | ③ Quality 3.2 | GĐ3 FR-02: chạy **theo lịch · theo sự kiện (khi dữ liệu được cập nhật) · thủ công** | DMP mới có lịch + thủ công | Thêm chế độ kích hoạt **theo sự kiện** *(job ghi xong bảng đích → chạy luật)* — nối vào 4.1 |
| **D7** | ③ Quality | GĐ3 §3: đối tượng áp dụng gồm bảng · cột · **file · báo cáo · chỉ tiêu · dữ liệu chủ** | DMP chỉ bảng/cột | Sau khi có thực thể Báo cáo/Chỉ tiêu và MDM thì **mở rộng ô "Đối tượng áp dụng"** của luật |
| **D8** | ⑤ Security 5.2/5.4 | GĐ4 FR-04: **hạn chế tải xuống** với dữ liệu Mật/Hạn chế · **cảnh báo truy cập bất thường** *(vd tải xuống số lượng lớn)* | Hạn chế tải xuống mới ở mức "phải nối vào màn ngoài phạm vi". Giám sát bất thường **chưa có màn** | Thêm tab **`Giám sát truy cập`** trong 5.5: danh sách cảnh báo bất thường, ngưỡng, xử lý; và chính sách **Hạn chế tải xuống** trong 5.2 |
| **D9** | ⑥ Operations 6.1 | GĐ2 §10 + GĐ3 §8 + GĐ4 §8 + GĐ5 §8: bộ chỉ số nghiệm thu **4 nhóm** | 6.1 mới phủ nhóm Catalog + Quality | Bổ sung chỉ số: *tỷ lệ đã phê duyệt* · *số thông tin quá hạn cập nhật* · *tỷ lệ báo cáo/chỉ tiêu truy vết được* · *số quyền quá hạn chưa thu hồi* · *số phát hiện tuân thủ chưa khắc phục* · *tỷ lệ bản ghi trùng đã xử lý* |
| **D10** | Toàn hệ thống | GĐ2 §7: **tải lên bằng file Excel/CSV** để thêm/cập nhật hàng loạt — *"khởi tạo ban đầu hoặc cập nhật nhiều đối tượng cùng lúc"* | Chỉ Danh mục tham chiếu và Glossary có nạp file | Thêm nút **`⬆️ Nạp từ file`** ở mọi màn danh sách của Module ①, kèm màn *đối chiếu trước khi nạp* |

</details>

---

## 6. Những chỗ DMP **vượt** yêu cầu — giữ nguyên, đừng cắt

<details open>
<summary><b>Bảy điểm nên nêu bật khi trình bày với BDA</b></summary>

| # | DMP có | BDA chỉ yêu cầu | Vì sao nên giữ |
|:---:|---|---|---|
| 1 | **8 kiểu che dữ liệu** + hiện câu SQL viết lại tương ứng | *"Che dữ liệu nhạy cảm (masking) hoặc mã hóa"* | Là thứ chứng minh được tính khả thi kỹ thuật, không chỉ là lời hứa |
| 2 | **Lọc theo dòng (row-level filter)** — bỏ được 41 bảng sao chép | Không yêu cầu | Tiết kiệm hạ tầng thật, con số đo được |
| 3 | **Cổng chất lượng tại cửa nạp** + Vùng chờ (quarantine) 3 mức xử lý | *"Phát hiện sớm lỗi dữ liệu"* | BDA muốn *phát hiện*; DMP làm được *chặn trước khi vào* — mạnh hơn hẳn |
| 4 | **Nguyên tắc 4 mắt** khi đóng sự cố + 6 lý do đóng bắt buộc chọn | 4 trạng thái phiếu | Chống "đóng lỗi cho đẹp số liệu" |
| 5 | **Ngưỡng 3 cấp** *(loại luật → bảng → lần gán)* | Không nêu | Cần thiết thật khi lên 11.482 bảng |
| 6 | **Thư viện 28 loại kiểm tra** dùng chung | *"thiết lập quy tắc theo 6 tiêu chí"* | Khai một lần dùng nhiều nơi — đúng tinh thần chuẩn hóa của BDA |
| 7 | **Cờ CDE** + steward tách khỏi owner trong Glossary | *"tên thuật ngữ, định nghĩa, công thức, đơn vị sở hữu, trạng thái"* | Đã sẵn sàng cho giai đoạn nâng cao |

</details>

---

## 7. Kiến trúc menu đề xuất sau khi sửa — **8 module · 34 menu**

<details open>
<summary><b>Bảng menu mới — 🆕 là bổ sung sau review</b></summary>

| Module | # | Menu | Ghi chú |
|---|:---:|---|---|
| **① DATA CATALOG** | 1.1 | 🆕 **Tìm kiếm toàn hệ thống** | Gap **D3** |
| | 1.2 | Bảng dữ liệu | giữ · thêm Data Owner *(D4)*, trạng thái phê duyệt *(D2)*, nạp file *(D10)* |
| | 1.3 | 🆕 **Hệ thống & Nguồn dữ liệu** | Gap **A1** |
| | 1.4 | 🆕 **Kênh trao đổi dữ liệu** | Gap **A4** |
| | 1.5 | 🆕 **Báo cáo & Chỉ tiêu** | Gap **A5** — ưu tiên cao nhất |
| | 1.6 | Nhóm bảng | giữ |
| | 1.7 | Miền dữ liệu | giữ |
| | 1.8 | Danh mục tham chiếu | giữ |
| **② GOVERNANCE** | 2.1 | Từ điển nghiệp vụ | giữ |
| | 2.2 | Phân loại & Nhãn | **tách 2 trục** *(D1)* |
| | 2.3 | 🆕 **Truy vết luồng dữ liệu** | Gap **C** — 3 tab |
| | 2.4 | 🆕 **Phê duyệt & Phiên bản** | Gap **D2** |
| **③ DATA QUALITY** | 3.1–3.5 | Thư viện luật · Luật & Kết quả · Phân tích dữ liệu · Sự cố · Cảnh báo | giữ · thêm *Chờ kiểm tra lại* **(D5)**, kích hoạt theo sự kiện **(D6)** |
| **④ INGESTION & ORCHESTRATION** | 4.1–4.3 | Luồng xử lý · Cửa nạp · Theo dõi & Pipeline | giữ |
| **⑤ DATA SECURITY** | 5.1–5.5 | Người dùng · Chính sách truy cập · Yêu cầu cấp quyền · Nhật ký kiểm toán · Báo cáo quyền | giữ · thêm tab **Giám sát truy cập bất thường** *(D8)* |
| **⑥ POLICY & COMPLIANCE** 🆕 | 6.1 | 🆕 **Chính sách dữ liệu** | Gap **B1** |
| | 6.2 | 🆕 **Vòng đời & Lưu trữ** | Gap **B1** |
| | 6.3 | 🆕 **Đánh giá tuân thủ** | Gap **B1** |
| **⑦ MASTER DATA** 🆕 | 7.1 | 🆕 **Mô hình dữ liệu chủ** | Gap **B2** |
| | 7.2 | 🆕 **Bản ghi nguồn** | |
| | 7.3 | 🆕 **Nghi ngờ trùng & Hợp nhất** | |
| | 7.4 | 🆕 **Bản ghi chuẩn & Phân phối** | |
| **⑧ OPERATIONS** | 8.1 | Sức khoẻ dữ liệu | mở rộng chỉ số *(D9)* |
| | 8.2 | Cấu hình hệ thống | giữ |

**Tổng: 8 module · 34 menu** *(21 cũ + 13 mới)*.

</details>

<details open>
<summary><b>Ánh xạ module ↔ giai đoạn BDA — dùng để báo cáo tiến độ</b></summary>

| Giai đoạn BDA | Module DMP phụ trách | Đợt triển khai đề xuất |
|---|---|:---:|
| **GĐ1** Khảo sát & nền tảng | *(không phải phần mềm)* — kết quả nạp vào 1.3, 1.7, 2.2, 8.2 | Đợt 0 |
| **GĐ2** Danh mục · Metadata · Lineage | ① + ② | **Đợt 1–2** |
| **GĐ3** Chất lượng dữ liệu | ③ *(+ ④ hỗ trợ)* | **Đợt 2–3** |
| **GĐ4** Phân loại · Bảo mật · Tuân thủ | ⑤ + ⑥ | **Đợt 3–4** |
| **GĐ5** Dữ liệu chủ & mở rộng | ⑦ | **Đợt 5** |
| Xuyên suốt | ⑧ Operations | mọi đợt |

</details>

---

## 8. Rà soát tính hợp lý của thiết kế — ngoài phần "đủ hay thiếu"

<details open>
<summary><b>Bảy nhận xét về logic, luồng dữ liệu và cách chia module</b></summary>

| # | Nhận xét | Đánh giá |
|:---:|---|:---:|
| **L1** | **NT1 "một nguồn sự thật"** — mọi module tham chiếu mã bảng từ 1.1. Đúng và phải giữ bằng mọi giá | ✅ **Rất tốt** |
| **L2** | **NT7 "menu = một thực thể được quản lý"** — thứ chỉ để xem thì là tab. Nguyên tắc tốt, nhưng **áp hơi cứng với lineage** khiến rơi mất yêu cầu khai báo thủ công *(§4)* | ⚠️ **Nới nhẹ** |
| **L3** | **Thứ tự khai báo 9 bước** *(nhãn/miền/Tier → bảng → cột → job → lineage → luật → sự cố → quyền → báo cáo)* — logic chặt, phản ánh đúng phụ thuộc thật | ✅ **Rất tốt** — chỉ cần chèn thêm *"khai hệ thống"* trước bước ② và *"khai báo cáo/chỉ tiêu"* sau bước ⑤ |
| **L4** | **Ba ràng buộc cứng RB1–RB3** — cổng chặn thay vì cảnh báo | ✅ Đúng tinh thần NT4. ⚠️ Cần **lường trước phản ứng**: bật cổng chặn ngay từ đợt 1 trên 11.482 bảng sẽ khiến người dùng không khai được gì. **Đề xuất: cổng chặn chỉ bật cho Tier 1 ở đợt 1, mở rộng dần** |
| **L5** | **Gộp 6 màn nạp về 4.2** — đúng, nhưng 6 màn đó có nghiệp vụ khá khác nhau *(`invoice-uploader`, `clean-delivery`)*. Rủi ro gộp ép | ⚠️ Giữ ý định gộp, nhưng thiết kế **"loại cửa nạp"** như một trường phân loại có cấu hình riêng theo loại — tài liệu đã làm đúng hướng này |
| **L6** | **Chính sách viết theo nhãn, không theo tên cột** *(RB3)* — quyết định kiến trúc rất đúng, scale được lên 11.482 bảng | ✅ **Điểm sáng nhất của thiết kế** |
| **L7** | **Module ⑥ Operations chỉ có 2 menu** trong khi gánh toàn bộ chỉ số nghiệm thu của 5 giai đoạn | ⚠️ Sau khi thêm chỉ số *(D9)*, nên tách 8.1 thành **2 tab**: *Sức khoẻ dữ liệu* và *Tiến độ quản trị (theo giai đoạn)* |

</details>

<details open>
<summary><b>Ba rủi ro thiết kế cần quyết trước khi code</b></summary>

| # | Rủi ro | Vì sao nguy hiểm | Đề xuất |
|:---:|---|---|---|
| **R1** | **Trộn 2 trục phân loại** *(D1)* | Chính sách bảo mật viết sai trục thì **không sửa lại được** khi đã áp lên 412 cột và đồng bộ sang OPA | Quyết **ngay bây giờ**, trước khi khai nhãn |
| **R2** | **Không có thực thể Báo cáo/Chỉ tiêu** | Càng khai nhiều bảng, càng khó bổ sung ngược *(phải đi hỏi lại từng đơn vị dùng báo cáo gì)* | Đưa vào **đợt 1**, khai song song với bảng |
| **R3** | **MDM để trắng trên bản đồ** | Lãnh đạo và BDA đọc tài liệu sẽ kết luận tool không làm được GĐ5 → xin ngân sách tool thứ hai | Đưa module ⑦ lên thanh menu ngay, dù chỉ dựng khung |

</details>

---

## 9. Kết luận và việc phải làm

<details open>
<summary><b>Việc phải làm, xếp theo thứ tự</b></summary>

| Ưu tiên | Việc | Gap | Khối lượng |
|:---:|---|:---:|---|
| **1** | Thêm menu **Báo cáo & Chỉ tiêu** *(2 cấp)* + nối vào lineage và luật chất lượng | A5 · D7 | Lớn |
| **2** | **Tách 2 trục phân loại** — mức phân loại 4 cấp ⟂ nhãn dữ liệu nhạy cảm | D1 · R1 | Trung bình |
| **3** | Thêm module **⑥ Chính sách & Tuân thủ** *(3 menu)* | B1 | Lớn |
| **4** | Thêm module **⑦ Dữ liệu chủ** *(4 menu, mức khung)* | B2 · R3 | Trung bình |
| **5** | Thêm menu **Truy vết luồng dữ liệu** *(3 tab, có khai báo thủ công)* | C | Trung bình |
| **6** | Thêm menu **Hệ thống & Nguồn dữ liệu** và **Kênh trao đổi dữ liệu** | A1 · A4 | Trung bình |
| **7** | Thêm menu **Phê duyệt & Phiên bản** + trường **Data Owner** | D2 · D4 | Trung bình |
| **8** | Thêm màn **Tìm kiếm toàn hệ thống** | D3 | Nhỏ |
| **9** | Bổ sung **Chờ kiểm tra lại** + kích hoạt **theo sự kiện** cho luật | D5 · D6 | Nhỏ |
| **10** | Tab **Giám sát truy cập bất thường** + chính sách **hạn chế tải xuống** | D8 | Nhỏ |
| **11** | Mở rộng chỉ số nghiệm thu ở Sức khoẻ dữ liệu | D9 | Nhỏ |
| **12** | Nút **Nạp từ file** ở các màn danh sách Module ① | D10 | Nhỏ |

**Sau khi làm xong 12 việc trên: mức phủ yêu cầu BDA đạt ~95%.** Phần 5% còn lại là những thứ chỉ chốt được khi có hạ tầng thật *(cơ chế thu thập tự động, đồng bộ OPA, tích hợp Jira)*.

</details>

---

<div align="center">

**HẾT BÁO CÁO REVIEW**

*Kiến trúc sau review đã được dựng thành demo chạy được — xem repo `dmp`*

</div>
