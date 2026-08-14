# DMP — Danh mục tính năng đề xuất

### 47 tính năng · đối chiếu với mã nguồn SQLWF · vì sao cần · hiện đã có gì

| | |
|---|---|
| **Ngày** | **13/08/2026** |
| **Mục đích** | Một file duy nhất liệt kê **mọi tính năng đề xuất**, mỗi tính năng trả lời ba câu: **vì sao cần · SQLWF hiện có gì · còn thiếu gì** |
| **Cách làm** | ⭐ Cột *"SQLWF hiện có"* **đọc thẳng từ mã nguồn** `sqlwf-be` và `sqlwf-fe`, không suy đoán |
| **Đọc cùng** | [Đặc tả 27 menu](DMP-Dac-ta-Chuc-nang-v1.md) · [Tư vấn từ thị trường](DMP-Tu-van-Bo-sung-tu-Thi-truong.md) · [Kiểm kê mã nguồn](DMP-Kiem-ke-man-hinh-SQLWF.md) |

---

## ⭐ Phát hiện quan trọng khi đọc lại mã nguồn

<details open>
<summary><b>SQLWF ĐÃ CÓ module AI tối ưu SQL và Job — chạy thật, có giao diện</b></summary>

Trong lượt tư vấn trước tôi đề xuất *"xây trợ lý AI tối ưu câu SQL của job"*. **Đề xuất đó sai ở chỗ coi như phải xây từ đầu.**

Đọc lại mã nguồn thấy SQLWF **đã có một hệ thống AI tuning hoàn chỉnh**:

| Thành phần | Đường dẫn trong mã nguồn |
|---|---|
| Dịch vụ tune cho **Job nhiều bước** | `services/tuning/job/JobTuningService.java` |
| Dịch vụ tune cho **câu SQL rời** | `services/tuning/sql/SqlTuningService.java` |
| Gửi yêu cầu sang **dịch vụ AI qua hàng đợi** | `services/tuning/producer/TuningProducer.java` |
| Nhận kết quả trả về | `services/tuning/listener/TuningResultListener.java` |
| **Giao diện** duyệt kết quả tune | `job-tuning-review` · `job-tuning-confirm` · `sql-tuning-confirm` |

**Kết quả AI trả về gồm những trường này** *(đọc từ `TuningResult.java`)*

| Trường | Nghĩa |
|---|---|
| `identifiedIssues` | ⭐ **Vấn đề AI phát hiện được** |
| `optimalContent` · `optimizedSql` | Nội dung đã tối ưu |
| `description` | Giải thích |
| `duration` | Thời gian xử lý |

**Vòng đời có kiểm soát** *(đọc từ `TuningStatus.java`)*

```
NONE → PROCESSING → TUNED_PENDING_APPLY → (người dùng áp dụng) → CLOSED
                  → FAILED / CANCELLED → tune lại
```

Và có cả **phân biệt nguồn gốc thay đổi** *(`StepsUpdateSource.java`)*: `USER` hay `AI_TUNING` — tức là hệ thống **biết bước nào do người sửa, bước nào do AI sửa**.

> ⭐ **Ý nghĩa cho tài liệu trình lãnh đạo:** đơn vị **đã đầu tư vào AI cho dữ liệu từ trước**, và đã làm đúng nguyên tắc *"máy đề xuất, người áp dụng"*. DMP **không đề xuất làm lại** — mà đề xuất **cho AI đó thêm ngữ cảnh để nó giỏi hơn**.
>
> Đây là lập luận mạnh hơn hẳn *"nên xây thêm tính năng AI"*.

**AI tuning hiện thiếu ngữ cảnh gì — và DMP cấp được ngay**

| AI tuning hiện chỉ thấy | DMP cấp thêm được | Nhờ đó AI làm được gì |
|---|---|---|
| Câu SQL | **Số dòng, dung lượng, phân vùng của bảng** *(1.1)* | Biết bảng nào lớn để ưu tiên tối ưu |
| — | **Lịch sử chạy từng bước** *(4.1)* | So trước–sau, đo tiết kiệm thật |
| — | **Quan hệ luồng dữ liệu** *(2.3)* | Biết sửa bước này ảnh hưởng ai |
| — | **Bảng nào đang có sự cố** *(3.3)* | Không khuyên dùng bảng đang hỏng |
| — | **Thuật ngữ nghiệp vụ** *(2.1)* | Hiểu cột `tong_tien` nghĩa là doanh thu |

</details>

---

## Bảng tra nhanh — 47 tính năng

<details open>
<summary><b>Bảng chỉ mục — bấm số để tìm mục chi tiết bên dưới</b></summary>

> 💡 Cột *Vì sao cần* ở đây chỉ là **một dòng tóm tắt**. Lý do đầy đủ kèm **tình huống cụ thể** nằm ở mục **Chi tiết từng tính năng** phía dưới.

**Ký hiệu cột "SQLWF hiện có":** ✅ đã có đủ · ⚠️ có một phần · ❌ chưa có

### Nhóm I — Chất lượng và giám sát dữ liệu

| # | Tính năng | Vì sao cần | SQLWF hiện có | Vào menu |
|:---:|---|---|---|---|
| 1 | **Giám sát tự động, không cần khai luật** | Chỉ **0,6%** bảng đang được kiểm — khai tay không đuổi kịp 11.482 bảng | ❌ `data-quality` chỉ bật/tắt và chọn chỉ số cố định | 3.2 |
| 2 | **Cảnh báo thay đổi cấu trúc bảng** | Nguyên nhân hàng đầu gây hỏng ngầm — job vẫn chạy nhưng số sai | ⚠️ `history-data` **ghi** thay đổi *(có giá trị cũ, mới, IP)* nhưng **không cảnh báo** | 1.1 · 3.2 |
| 3 | **Gom sự cố theo nguyên nhân gốc** | 1 bảng gốc hỏng sinh 20 phiếu rời rạc → đẩy tỷ lệ báo động giả qua ngưỡng | ❌ `warning-history` có duyệt hàng loạt nhưng **không gom theo nguyên nhân** | 3.3 |
| 4 | **Lan cờ tin cậy theo luồng dữ liệu** | Người đọc báo cáo không biết số bắt nguồn từ bảng đang hỏng | ❌ | 2.3 · 4.3 |
| 5 | **Cam kết dữ liệu giữa bên cấp và bên dùng** | Chuyển từ *phát hiện sau* sang *thoả thuận trước* | ⚠️ có `syncFrequency` và cấu hình chu kỳ, **chưa có khái niệm cam kết hai bên** | menu mới |
| 6 | **Cam kết chất lượng theo bảng** 🆕 | Bảng quan trọng cần cam kết *"độ trễ tối đa 2 giờ, tỷ lệ rỗng dưới 1%"* — nhẹ hơn cam kết đầy đủ | ⚠️ có `dqCycleType` `dqOffset` `dqDelay` — đã có mầm | 3.2 |

### Nhóm II — Vận hành job và hạ tầng

| # | Tính năng | Vì sao cần | SQLWF hiện có | Vào menu |
|:---:|---|---|---|---|
| 7 | ⭐ **Cấp ngữ cảnh cho AI tuning sẵn có** | AI đang tune **mà chỉ nhìn được câu SQL** — không biết bảng to nhỏ, chạy bao lâu, ai dùng | ✅ **Đã có cả hệ thống tuning** *(xem phát hiện ở trên)* — thiếu ngữ cảnh | 4.1 |
| 8 | **Báo trước job sắp hỏng vì hết bộ nhớ** | Kiểu hỏng này **đoán trước được** — dữ liệu tăng dần, thời gian chạy dài dần | ❌ `task-management` có kết quả lần chạy gần nhất, **không có xu hướng** | 4.1 · 4.3 |
| 9 | **Ước lượng chi phí trước khi cho chạy** | Người duyệt job cần biết *"job này ngốn gấp 6 lần trung bình"* **lúc duyệt** | ❌ | 4.1 |
| 10 | **Tìm job đang tính trùng nhau** | 1.842 job tích luỹ nhiều năm — chắc chắn có nhóm tính cùng một thứ | ❌ | 4.1 |
| 11 | ⭐ **Đang trả tiền cho thứ không ai dùng** | **186 job** không chạy 90 ngày vẫn cập nhật bảng không ai đọc | ⚠️ có dữ liệu rời *(lịch sử truy vấn, danh sách job)* nhưng **chưa ghép lại** | 6.2 · 8.1 |
| 12 | **Khôi phục bảng về thời điểm trước** 🆕 | Job ghi sai → thay vì chạy lại từ đầu thì **quay bảng về ảnh chụp trước đó** | ⚠️ Nền tảng dữ liệu dùng **Hudi/Iceberg** *(có ảnh chụp sẵn)* — DMP chưa khai thác | 1.1 · 4.1 |
| 13 | **So sánh hai lần chạy để biết vì sao số đổi** 🆕 | Câu hỏi phổ biến nhất của người dùng: *"sao hôm nay khác hôm qua"* | ❌ | 4.1 · 1.1 |
| 14 | **Kiểm thử trước khi lên chạy thật** 🆕 | Job mới nên chạy thử trên môi trường tách rời trước | ✅ **Đã có chế độ chạy thử** — `updateTestMode` | 4.1 |

### Nhóm III — Metadata và tự động hoá khai báo

| # | Tính năng | Vì sao cần | SQLWF hiện có | Vào menu |
|:---:|---|---|---|---|
| 15 | ⭐ **Tự dò cột nhạy cảm, đề xuất nhãn** | 412 cột gắn nhãn **bằng tay** trên tổng số cột của 11.482 bảng — chắc chắn còn sót | ⚠️ có `tagIds` mức cột và 3 nhãn, **gắn thủ công**, không có bộ dò | 2.2 |
| 16 | ⭐ **Máy viết mô tả, người duyệt** | **8.267 bảng** thiếu mô tả *(72%)* — gõ tay sẽ không bao giờ xong | ❌ | 1.1 · 2.4 |
| 17 | ⭐ **Thao tác hàng loạt** 🆕 | Gán miền cho **4.334 bảng** — không ai mở từng bảng để sửa | ⚠️ có nạp file ở `import-data`, **không có sửa hàng loạt theo bộ lọc** | 1.1 và mọi màn danh sách |
| 18 | **Tự sinh luật chất lượng từ mô tả tiếng Việt** 🆕 | *"số tiền không âm, không quá 10 tỷ"* → sinh luật, đỡ phải học cú pháp | ❌ | 3.2 |
| 19 | **Đề xuất chuẩn hoá tên khi khai** 🆕 | Kiểm tên là chặn; **gợi ý tên đúng** mới là giúp | ❌ | 1.1 · 8.2 |
| 20 | **Xuất/nhập cấu hình giữa các môi trường** 🆕 | Khai ở môi trường thử rồi chuyển sang thật, không khai lại | ⚠️ `configuration-management` có cấu hình theo `taskCode`, chưa có chuyển môi trường | 8.2 |

### Nhóm IV — Trợ lý và tri thức

| # | Tính năng | Vì sao cần | SQLWF hiện có | Vào menu |
|:---:|---|---|---|---|
| 21 | ⭐ **Bot hỏi đáp tri thức dữ liệu** | Một câu hỏi hiện phải mở **sáu màn** mới trả lời được | ❌ | thanh tìm kiếm |
| 22 | ⭐ **Hỏi đáp và nhận cảnh báo qua Telegram** 🆕 | Người dùng không mở tool cả ngày — **đưa tool tới chỗ họ đang ở** | ✅ **Đã có module `telegram` đang chạy** — chỉ mở rộng nội dung | 3.4 |
| 23 | **Tìm kiếm bằng câu nói thường** | Người nghiệp vụ **không biết tên bảng** — đó là lý do họ đi hỏi | ❌ **Không có màn tìm kiếm nào** trong 67 màn hiện tại | thanh tìm kiếm |
| 24 | **Tóm tắt tự viết cho lãnh đạo** | Bảng số không nói được *"điểm tăng do thêm bảng dễ, không phải cải thiện thật"* | ⚠️ `report-management` có báo cáo vận hành, không phải tóm tắt | 8.1 |
| 25 | **Trợ lý viết job biết ngữ cảnh** | Cảnh báo *"bảng này đang có sự cố, cân nhắc dùng bảng khác"* | ⚠️ AI tuning **sửa** SQL có sẵn, chưa **gợi ý lúc viết mới** | 4.1 |
| 26 | **Đọc văn bản quy định, đề xuất mục kiểm** | Module ⑥ bắt người tự đọc nghị định rồi tự nghĩ mục kiểm | ❌ | 6.1 · 6.3 |
| 27 | **Mở kho metadata cho trợ lý AI** | Đội đang dùng trợ lý AI viết mã — cho nó đọc metadata ngay lúc code | ❌ | 8.2 |
| 28 | **Chạy thử tác động trước khi đổi** | Biết **cụ thể hỏng ở bước nào**, không chỉ biết cái gì liên quan | ⚠️ `data-linage` có `getExpandLineage`, chỉ xem quan hệ | 2.3 · 2.4 |

### Nhóm V — Quy trình làm việc *(vai BDA)*

| # | Tính năng | Vì sao cần | SQLWF hiện có | Vào menu |
|:---:|---|---|---|---|
| 29 | ⭐ **Hộp thư "Việc của tôi"** | Việc nằm rải ở **6 hàng chờ** — phải mở 6 menu mới biết mình có bao nhiêu việc | ❌ Có duyệt ở `job-approval`, `channel-indexing`, `sync-management` nhưng **mỗi nơi một chỗ** | menu mới |
| 30 | **Cổng tiếp nhận yêu cầu dữ liệu** | Yêu cầu *"tôi cần số X"* đang đi qua chat, **không để lại dấu vết** | ❌ | menu mới |
| 31 | **Bàn giao trách nhiệm hàng loạt** | Một người phụ trách **148 bảng** — nghỉ phép là cảnh báo rơi vào hư không | ❌ | 5.1 |
| 32 | **Xem trước tác động khi sửa nghĩa** | Đổi nghĩa nguy hiểm hơn đổi kiểu — **mọi thứ vẫn chạy nhưng số bị hiểu sai** | ❌ | 2.1 · 2.2 |
| 33 | **Hướng dẫn tại chỗ cho người mới** 🆕 | 27 menu — người mới không biết bắt đầu từ đâu | ❌ | xuyên suốt |

### Nhóm VI — Phục vụ người dùng cuối

| # | Tính năng | Vì sao cần | SQLWF hiện có | Vào menu |
|:---:|---|---|---|---|
| 34 | ⭐ **Đăng ký theo dõi bảng và báo cáo** | 🔴 **Lỗ hổng lớn nhất** — cảnh báo chỉ gửi cho đầu mối, **người dùng chịu hậu quả thì không được báo** | ⚠️ `notify-manager` có nhóm nhận email — **theo nhóm cố định, không theo dõi được** | 1.1 · 1.3 |
| 35 | **Nhãn tin cậy đi kèm số liệu** | Có số rồi nhưng không biết tin được không | ❌ | 1.1 · 1.3 |
| 36 | **Theo dõi tiến trình yêu cầu** | Gửi xong mất dấu, không biết đang chờ ai | ❌ | 5.3 |
| 37 | ⭐ **Báo vấn đề ngay tại chỗ** | Người dùng là **người đầu tiên phát hiện số sai** — phản hồi đang đi vào chat rồi mất | ❌ | 1.1 · 1.3 |
| 38 | **Ai khác đang dùng bảng này** | Đầu mối thành nút thắt vì là cửa duy nhất để hỏi | ⚠️ có `sql-history` `query-history` — **chưa hiện lên chỗ người dùng cần** | 1.1 |
| 39 | **Trang chủ theo vai trò** 🆕 | Năm vai trò, nhu cầu khác nhau — mở lên nên thấy đúng thứ của mình | ⚠️ có phân quyền menu ở `acl`, chưa có trang chủ riêng | trang chủ |

### Nhóm VII — Quản trị và điều hành

| # | Tính năng | Vì sao cần | SQLWF hiện có | Vào menu |
|:---:|---|---|---|---|
| 40 | ⭐ **Bảng điều khiển tắc nghẽn quy trình** | DMP đo chất lượng dữ liệu nhưng **chưa ai đo chính quy trình của DMP** | ❌ | 8.1 |
| 41 | **So sánh miền và giao chỉ tiêu** | Giao *"nâng điểm lên 90"* thì không ai biết bắt đầu từ đâu | ⚠️ `domain-management` hiện BDA/DE theo miền, chưa có chỉ tiêu | 8.1 |
| 42 | **Ba rủi ro lớn nhất tuần này** | Lãnh đạo không có thời gian đọc mười chỉ số ngang hàng | ❌ | 8.1 |
| 43 | **Đo mức độ dùng chính tool** 🆕 | Menu nào không ai mở suốt 3 tháng thì **nên bỏ**, đừng bảo trì | ⚠️ có nhật ký truy cập, chưa dùng để đo tool | 8.1 |

### Nhóm VIII — Nền tảng chuẩn và trợ lý theo yêu cầu *(bổ sung 13/08/2026)*

| # | Tính năng | Vì sao cần | SQLWF hiện có | Vào menu |
|:---:|---|---|---|---|
| 44 | ⭐ **Đồng bộ PYC từ Jira → đề xuất hướng làm** 🆕 | BDA mất **bốn ngày đi tìm** trước khi viết được dòng SQL đầu tiên — và lặp lại y hệt với mọi PYC | ❌ | 5.3 · menu mới |
| 45 | **Từ bảng tới khung báo cáo (Tableau / VDSD)** 🆕 | Dựng báo cáo phần lớn là **thao tác lặp**; mọi báo cáo cùng loại lặp gần giống nhau | ❌ | 5.3 |
| 46 | **Danh mục quy định có cấu trúc, máy đối chiếu tuân thủ** 🆕 | Thay cho ý *"upload PDF cho AI đọc"* — cách đó **không truy vết được tới điều khoản** khi kiểm toán hỏi | ❌ | 6.1 · 6.3 |
| 47 | **Nhật ký gọi AI** 🆕 | Đã có kênh AI chạy thật mà **chưa có màn tra cứu ai gọi gì, gửi gì đi** — điều kiện bắt buộc trước khi mở rộng AI | ⚠️ `CommandInfo` **đã mang `username` + `ip`**, chưa có màn tra cứu | 8.1 |

> 🔄 **Sửa lại đề xuất 26.** Mục 26 vốn là *"AI đọc văn bản quy định rồi đề xuất mục kiểm"*. Sau khi rà lại rủi ro, **26 được thay bằng 46**: người đọc văn bản và khai thành dòng luật có cấu trúc, AI chỉ đọc bảng đã khai. Lý do đầy đủ ở [tài liệu AI và lộ trình](DMP-AI-va-Lo-trinh-Nen-tang-Chuan.md#21-câu-hỏi-cụ-thể--upload-pdf-quy-định-rồi-ai-đề-xuất).

</details>

---

## Chi tiết từng tính năng

> **Cách đọc mỗi mục:** **Tình huống** *(chuyện có thật hoặc sẽ xảy ra)* → **Nếu không có tính năng này** → **Tính năng làm gì** → **SQLWF hiện có gì** → **Cần làm thêm**.

---

### Nhóm I — Chất lượng và giám sát dữ liệu

<details open>
<summary><b>1 · Giám sát tự động, không cần khai luật ⭐🔥🔥🔥</b></summary>

**Tình huống**

> Sáng thứ Hai, bảng `dwh.thue_bao_ngay` chỉ nhận về **60% số dòng bình thường** vì hệ thống nguồn lỗi lúc 3 giờ sáng. Bảng này **không nằm trong 64 bảng đã được gán luật**, nên hệ thống không kiểm gì cả và **không ai được báo**.
>
> Ba báo cáo đọc bảng này chạy bình thường, ra số thấp hơn thực tế. Cả tuần không ai thấy bất thường. **Đến kỳ chốt tháng, kế toán phát hiện lệch — lúc đó đã 3 tuần trôi qua.**

**Nếu không có tính năng này**

Chỉ **64 trên 11.482 bảng** *(0,6%)* được kiểm. **11.418 bảng còn lại là vùng tối hoàn toàn** — không phải chúng không có lỗi, mà là **không ai biết chúng có lỗi hay không**.

Điểm chất lượng **87** hiện chỉ tính trên 64 bảng đó. Đưa con số này cho lãnh đạo mà không nói rõ mẫu là **báo cáo gây hiểu lầm**.

**Tính năng làm gì**

Máy **tự học nhịp bình thường của từng bảng** trong khoảng một tháng — mỗi ngày về bao nhiêu dòng, thường về lúc mấy giờ, tỷ lệ rỗng bao nhiêu — rồi **tự báo khi lệch khỏi nhịp đó**. Không ai phải khai luật.

Máy theo dõi năm nhóm tín hiệu: **độ tươi** *(hôm nay chưa có dữ liệu)* · **khối lượng** *(số dòng tụt bất thường)* · **cấu trúc** *(thêm/mất cột)* · **phân bố** *(tỷ lệ rỗng đổi đột ngột)* · **quan hệ luồng** *(nhánh phụ thuộc đứt)*.

**SQLWF hiện có gì**

❌ `data-quality` có bật/tắt kiểm và chọn chỉ số từ **danh sách cố định**, nhưng **phải khai cho từng bảng một**. Không có cơ chế nào tự phát hiện bất thường trên bảng chưa khai.

**Cần làm thêm**

Chế độ **giám sát tự động** bật một lần cho cả miền. Chạy **chế độ chỉ quan sát ít nhất một tháng** để máy học nhịp trước khi bật gửi cảnh báo — nếu không sẽ ngập cảnh báo tuần đầu.

</details>

<details open>
<summary><b>2 · Cảnh báo khi cấu trúc bảng thay đổi 🔥🔥🔥</b></summary>

**Tình huống**

> DE đổi kiểu cột `so_tien` từ **số thập phân sang chuỗi** để chứa được ký tự đặc biệt trong một trường hợp đặc thù. Job vẫn chạy trơn tru, **không báo lỗi gì**.
>
> Nhưng job hạ nguồn dùng hàm tổng trên cột đó — cộng chuỗi ra kết quả rỗng. **Báo cáo doanh thu hiện 0 đồng suốt hai ngày** trước khi có người thắc mắc.

**Nếu không có tính năng này**

Đổi cấu trúc là **nguyên nhân hàng đầu gây hỏng ngầm** — vì nó **không làm job báo lỗi**, chỉ làm số sai. Người phát hiện thường là người dùng cuối, sau vài ngày.

**Tính năng làm gì**

Khi phát hiện thêm cột, mất cột hoặc đổi kiểu, hệ thống **tra ngay xem ai đang dùng cột đó** rồi báo cho đúng người:

```
Cột `so_tien` đổi từ số thập phân sang chuỗi
  → 3 job đang đọc cột này: JOB-0412, JOB-0119, JOB-0233
  → 2 báo cáo hạ nguồn: BC-001, BC-004
  → gửi cho: DE của 3 job + đầu mối của 2 báo cáo
```

**SQLWF hiện có gì**

⚠️ `history-data` **đã ghi lại thay đổi rất chi tiết** — có `Giá trị cũ`, `Giá trị mới`, `Người thay đổi`, `IP Address`. Nhưng đây là **nhật ký để tra sau**, không ai được báo lúc nó xảy ra.

**Cần làm thêm**

Nối ba mảnh **đã có sẵn**: nhật ký thay đổi *(1.1)* + quan hệ luồng dữ liệu *(2.3)* + kênh gửi cảnh báo *(3.4)*. **Công sức thấp** vì không phải xây mới cái nào.

</details>

<details open>
<summary><b>3 · Gom sự cố theo nguyên nhân gốc ⭐🔥🔥🔥</b></summary>

**Tình huống**

> 6 giờ sáng, bảng `raw.doi_soat_A_tho` nạp thiếu dữ liệu vì đối tác gửi file lỗi.
> 7 giờ, `JOB-0412` chạy, ghi số sai vào `bi.doi_soat_giao_dich_A`.
> 7 giờ 15, năm job hạ nguồn khác chạy tiếp, làm **12 bảng bị sai theo**.
>
> Mỗi bảng có 2–3 luật chất lượng. **Trong 30 phút, hệ thống sinh ra 28 phiếu sự cố.**
>
> Anh Hùng mở máy lúc 8 giờ, thấy **28 việc đang chờ**. Không biết bắt đầu từ đâu. Thực tế **chỉ cần sửa một chỗ** — lô dữ liệu gốc — thì 27 phiếu kia tự hết.

**Nếu không có tính năng này**

Đây chính là cách **tỷ lệ báo động giả leo qua ngưỡng 25%** — ngưỡng mà tài liệu của mình đã cảnh báo là *"người dùng sẽ tắt thông báo và cả module chất lượng thành vô dụng"*.

Và nó **đã xảy ra một lần rồi**: tính năng chất lượng cũ của SQLWF chết đúng theo kiểu này.

**Tính năng làm gì**

Dùng **quan hệ luồng dữ liệu** để nối các sự cố cùng nhánh lại: sinh **một phiếu gốc** *(lô dữ liệu nạp thiếu)* và **27 phiếu con gắn vào nó**. Chỉ DE của bảng gốc phải xử lý. Sửa xong bảng gốc thì 27 phiếu con **tự kiểm tra lại và tự đóng**.

Thêm một cột đơn giản mà quyết định thứ tự ưu tiên: **"sự cố này đang làm 12 bảng và 4 báo cáo sai số"**.

**SQLWF hiện có gì**

❌ `warning-history` có **duyệt cảnh báo hàng loạt** và tạo phiếu SOC — nhưng đó là **duyệt cho nhanh**, không phải **gom theo nguyên nhân**. Hai việc khác hẳn nhau.

**Cần làm thêm**

Nguyên liệu **đã có đủ** — sơ đồ luồng dữ liệu ở 2.3. Việc cần làm là thêm quan hệ cha–con giữa các phiếu và cơ chế tự đóng phiếu con.

</details>

<details open>
<summary><b>4 · Lan cờ tin cậy theo luồng dữ liệu 🔥🔥</b></summary>

**Tình huống**

> Chị Lan ở Ban Kinh doanh mở báo cáo doanh thu lúc 9 giờ sáng để chuẩn bị họp chiều. Số liệu hiện ra bình thường, không có dấu hiệu gì lạ.
>
> Chị không biết rằng bảng nguồn `bi.doi_soat_giao_dich_A` **đang có sự cố từ 6 giờ sáng**, đội kỹ thuật đang xử lý. Số chị đang xem là **số sai**.
>
> 2 giờ chiều, chị trình bày con số đó trong cuộc họp.

**Nếu không có tính năng này**

Màn 4.3 **đã vẽ badge chất lượng** — nhưng badge **chỉ hiện trên đúng bảng bị lỗi**. Bảng hạ nguồn và báo cáo **trông vẫn bình thường**, dù số của chúng bắt nguồn từ bảng đang hỏng.

**Tính năng làm gì**

Ba mức trạng thái **lan tự động** theo luồng dữ liệu:

| Trạng thái | Nghĩa |
|---|---|
| ✅ Tin cậy | Luật đạt, dữ liệu về đúng hạn |
| ⚠️ **Nghi ngờ** | **Ăn dữ liệu từ nhánh đang có sự cố** — lan xuống toàn bộ hạ nguồn |
| 🛑 Đang hỏng | Chính nó có luật hỏng |

Cờ ⚠️ hiện ở **cả màn báo cáo**, không chỉ ở màn kỹ thuật.

**SQLWF hiện có gì**

❌ Chưa có khái niệm trạng thái tin cậy.

**Cần làm thêm**

Một phép duyệt trên đồ thị luồng đã có, cộng một cờ hiển thị. **Công sức thấp.**

</details>

<details open>
<summary><b>5 · Cam kết dữ liệu giữa bên cấp và bên dùng 🔥🔥</b></summary>

**Tình huống**

> Đội quản trị hệ thống CRM đổi tên cột `sdt` thành `so_dien_thoai` cho dễ đọc. Việc này hợp lý với họ, và họ **không biết có ai đang đọc bảng đó**.
>
> Ba job của đội Dữ liệu hỏng ngay đêm đó. Sáng hôm sau hai bên ngồi lại, và câu hỏi đầu tiên là: *"sao không báo trước?"* — nhưng thực tế **không có kênh nào để báo, và cũng không có thoả thuận nào bị vi phạm**.

**Nếu không có tính năng này**

DMP hiện **phát hiện lỗi sau khi lỗi đã xảy ra**. Không có cơ chế nào **ngăn** bên cấp dữ liệu đổi thứ mà bên dùng đang phụ thuộc.

**Tính năng làm gì**

Một bản cam kết có thể kiểm tra tự động, ghi rõ: **danh sách cột và kiểu · độ tươi cam kết · ngưỡng chất lượng · được phép đổi gì và phải báo trước bao lâu**. Vi phạm cam kết thì hệ thống **chặn thay đổi** hoặc bắt đi qua quy trình phê duyệt có bên dùng tham gia.

**SQLWF hiện có gì**

⚠️ Có `syncFrequency` và bộ cấu hình chu kỳ chất lượng — tức **đã có vài mảnh của cam kết**, nhưng chưa gom thành một thoả thuận hai bên và **chưa có hệ quả khi vi phạm**.

**Cần làm thêm**

Gói các mảnh đã có thành một bản cam kết có phiên bản, thêm cơ chế chặn. ⚠️ **Đây là đề xuất đụng tới quy trình làm việc giữa các đội**, nên công sức thật nằm ở khâu thoả thuận chứ không phải khâu lập trình.

</details>

<details open>
<summary><b>6 · Cam kết chất lượng theo bảng 🆕🔥</b></summary>

**Tình huống**

> Bảng `bi.doi_soat_giao_dich_A` là bảng quan trọng nhất của nghiệp vụ đối soát. Nhưng **không ở đâu ghi rõ nó phải đạt mức nào** — chỉ có các luật rời rạc.
>
> Khi bảng về trễ 4 tiếng, không ai biết đó là **bình thường hay bất thường**, vì chưa từng có ai nói *"bảng này chậm quá 2 tiếng là sự cố"*.

**Nếu không có tính năng này**

Mọi bảng bị đối xử như nhau. Bảng Tier 1 chậm 4 tiếng và bảng tạm chậm 4 tiếng **sinh ra cảnh báo giống hệt nhau**, nên không ai biết cái nào đáng lo.

**Tính năng làm gì**

Ba con số cam kết cho bảng quan trọng: **độ trễ tối đa · tỷ lệ rỗng tối đa · tỷ lệ đạt luật tối thiểu**. Vi phạm thì sự cố sinh ra **mang sẵn mức ưu tiên cao**, không cần ai phân loại.

**SQLWF hiện có gì**

⚠️ **Đã có mầm khá rõ**: `dqCycleType` · `dqOffset` · `dqDelay` · `dqComparedCycle` — tức đã có khái niệm chu kỳ và độ trễ chấp nhận được. Chỉ **chưa gọi tên là cam kết** và **chưa có hệ quả khi vi phạm**.

**Cần làm thêm**

Nhẹ hơn tính năng 5 nhiều — chỉ là ba trường khai thêm ở 3.2 và một quy tắc xếp mức ưu tiên.

</details>

---

### Nhóm II — Vận hành job và hạ tầng

<details open>
<summary><b>7 · Cấp ngữ cảnh cho AI tuning sẵn có ⭐🔥🔥🔥</b></summary>

**Tình huống**

> DE bấm nút tune cho `JOB-0412`. AI trả về gợi ý: *"thêm chỉ mục cho cột `ma_giao_dich` để tăng tốc phép nối"*.
>
> Gợi ý nghe hợp lý — nhưng **bảng đó chỉ có 2.000 dòng**, thêm chỉ mục **không tiết kiệm được gì**. AI không biết điều đó vì **nó chỉ nhìn thấy câu SQL**, không thấy bảng to hay nhỏ.
>
> Lần khác, AI đề xuất đọc thêm từ bảng `raw.doi_soat_B_tho` cho nhanh hơn — nhưng bảng đó **đang có sự cố chưa đóng**. AI cũng không biết.

**Nếu không có tính năng này**

Đây là bài học mà **Datadog đã công bố** khi làm cùng loại tính năng: những gợi ý đầu tiên của họ **sai mục tiêu** — máy khuyên cắt bớt cột trong khi hệ thống đã tự cắt rồi. Nguyên nhân chung là **thiếu ngữ cảnh**.

Kết quả: DE thử vài lần thấy gợi ý không dùng được thì **bỏ luôn tính năng** — và khoản đầu tư vào AI tuning thành lãng phí.

**Tính năng làm gì**

Gửi kèm ngữ cảnh mà DMP đã có sẵn khi gọi dịch vụ AI:

| Ngữ cảnh gửi thêm | AI làm được gì nhờ đó |
|---|---|
| Số dòng, dung lượng, phân vùng của bảng | Không đề xuất tối ưu cho bảng nhỏ |
| Lịch sử chạy từng bước | **So được trước và sau, đo tiết kiệm thật** |
| Quan hệ luồng dữ liệu | Biết sửa bước này ảnh hưởng ai |
| Bảng nào đang có sự cố | Không khuyên dùng bảng đang hỏng |
| Thuật ngữ nghiệp vụ | Hiểu `tong_tien` nghĩa là doanh thu |

**SQLWF hiện có gì**

✅ **Đã có toàn bộ hệ thống AI tuning và đang chạy** — `JobTuningService`, `SqlTuningService`, gửi qua hàng đợi tới dịch vụ AI, có giao diện duyệt kết quả *(`job-tuning-review`, `job-tuning-confirm`)*, có vòng đời `PROCESSING → TUNED_PENDING_APPLY → áp dụng`, và phân biệt được thay đổi do `USER` hay `AI_TUNING`.

**Cần làm thêm**

Chỉ **bổ sung ngữ cảnh vào gói tin gửi đi**, và thêm bước **đo kết quả sau khi áp dụng** *(so thời gian chạy trước và sau)*. Không phải xây mới.

> ⭐ **Đây là đề xuất có tỷ lệ giá trị trên công sức cao nhất trong cả danh mục** — vì phần đắt nhất đã được đầu tư từ trước.

</details>

<details open>
<summary><b>8 · Báo trước job sắp hỏng vì hết bộ nhớ 🔥🔥🔥</b></summary>

**Tình huống**

> `JOB-0501` chạy hằng tháng để tính KPI kinh doanh. Ngày 1 tháng 8, nó **hỏng ở bước 7 vì hết bộ nhớ** — đúng kỳ chốt số, lúc 3 giờ sáng. Đội trực phải xử lý gấp, báo cáo tháng chậm một ngày.
>
> Nhìn lại lịch sử: tháng 3 bước 7 chạy **12 phút**, tháng 5 **18 phút**, tháng 7 **24 phút**. Xu hướng rõ ràng suốt 5 tháng — **nhưng không ai nhìn vào, vì không màn nào hiện xu hướng**.

**Nếu không có tính năng này**

Loại hỏng này **luôn xảy ra vào lúc tệ nhất** — kỳ chốt số, cuối tháng, giữa đêm — vì đó là lúc dữ liệu lớn nhất. Và nó **hoàn toàn đoán trước được**, chỉ là chưa ai đo.

**Tính năng làm gì**

Vẽ đường xu hướng cho ba chuỗi số mà DMP đã có: **số dòng vào từng bước** · **thời gian chạy từng bước** · **dung lượng bảng nguồn**. Khi đường xu hướng sắp chạm ngưỡng thì cảnh báo:

> ⚠️ *`JOB-0501` — thời gian bước 7 tăng đều 8% mỗi tháng trong 5 tháng. Với nhịp này, **khoảng cuối tháng 10 sẽ vượt hạn mức bộ nhớ**.*
> *Đề xuất: chia bước 7 theo phân vùng, hoặc tăng bộ nhớ trước kỳ chốt tháng 10.*

**SQLWF hiện có gì**

❌ `task-management` có `taskCode`, `cronExpression`, `cyclePattern` và **kết quả lần chạy gần nhất** — nhưng chỉ lần gần nhất, **không có xu hướng theo thời gian**.

**Cần làm thêm**

Lưu lịch sử chạy đủ dài *(ít nhất 6 tháng)* và vẽ đường xu hướng. **Không cần mô hình phức tạp** — ngoại suy tuyến tính đã đủ bắt phần lớn ca.

</details>

<details open>
<summary><b>9 · Ước lượng chi phí trước khi cho job chạy 🔥🔥</b></summary>

**Tình huống**

> DE mới viết một job nối ba bảng lớn nhưng **quên lọc theo phân vùng ngày**. Job được duyệt vì nhìn câu SQL thì thấy hợp lý.
>
> Đêm đó job chạy **4 tiếng**, chiếm gần hết tài nguyên cụm máy, khiến **6 job khác chạy trễ** và hai báo cáo sáng không có số.
>
> Người duyệt job **không có cách nào biết trước** điều này lúc bấm duyệt.

**Nếu không có tính năng này**

Chi phí hạ tầng chỉ được phát hiện **sau khi hoá đơn về** hoặc **sau khi cụm máy quá tải** — tức là sau khi đã tốn.

**Tính năng làm gì**

Trước khi gửi duyệt, hệ thống ước lượng và hiện ngay:

> *Job này ước tính chạy **~8 phút**, đọc **~40 GB**. So với trung bình các job cùng nhóm: **gấp 6 lần**.*
> ⚠️ *Vượt ngưỡng cảnh báo — cần giải thích lý do trước khi gửi duyệt.*

Có nghiên cứu năm 2026 làm đúng bài toán này: dự báo tài nguyên **trước khi chạy** dựa trên độ phức tạp câu lệnh, khối lượng dữ liệu ước tính và đặc trưng từ chính văn bản câu lệnh — vì các công thức tĩnh của bộ tối ưu **không mô hình hoá được lệch phân bố và tranh chấp tài nguyên**.

**SQLWF hiện có gì**

❌ Chưa có ước lượng nào trước khi chạy.

**Cần làm thêm**

Mô hình đơn giản học từ lịch sử chạy của chính 1.842 job đã có. ⭐ **Giá trị không nằm ở độ chính xác của con số, mà ở chỗ đặt nó — ngay trước nút duyệt.**

</details>

<details open>
<summary><b>10 · Tìm job đang tính trùng nhau 🔥🔥</b></summary>

**Tình huống**

> Ban Kinh doanh cần doanh thu theo ngày → đội Dữ liệu viết `JOB-0119`.
> Sáu tháng sau, Ban Tài chính cũng cần doanh thu theo ngày nhưng lọc khác một chút → **viết job mới** vì không biết job cũ đã có.
> Năm sau, Ban Sản phẩm lặp lại lần thứ ba.
>
> Kết quả: **năm job cùng đọc `dwh.giao_dich_ngay`, cùng tính doanh thu ngày, ghi ra năm bảng đích khác nhau** — chênh nhau chỉ ở điều kiện lọc.

**Nếu không có tính năng này**

Với **1.842 job tích luỹ qua nhiều năm và nhiều người làm**, đây gần như chắc chắn đang xảy ra. Mỗi job trùng là **một lần chạy hằng ngày + một bảng phải lưu + một thứ phải bảo trì**.

**Tính năng làm gì**

So sánh trên hai mặt: **cấu trúc câu SQL** *(cùng nhóm theo cột nào, cùng tính chỉ tiêu gì)* và **quan hệ luồng** *(cùng đọc từ bảng nào)*. Đưa ra nhóm nghi ngờ để người xác nhận.

**SQLWF hiện có gì**

❌ Chưa có. Muốn tìm phải đọc tay 1.842 câu SQL.

**Cần làm thêm**

Cần **bộ phân tích cú pháp SQL** — thứ đã được đề xuất từ đầu cho việc dò quan hệ luồng. ⚠️ **Không tự gộp** — hai job giống nhau vẫn có thể phục vụ hai mục đích khác nhau.

</details>

<details open>
<summary><b>11 · Đang trả tiền cho thứ không ai dùng ⭐🔥🔥</b></summary>

**Tình huống**

> `JOB-0644` chạy **mỗi 15 phút** để cập nhật bảng `ops.log_truy_cap`. Job này được dựng cho một dự án đã kết thúc **từ 8 tháng trước**.
>
> Nhật ký truy cập cho thấy **không ai đọc bảng đó suốt 6 tháng**. Nhưng job vẫn chạy 96 lần mỗi ngày, và bảng vẫn lớn dần trên vùng lưu trữ đắt tiền.
>
> Đây là **một trong 186 job không ai chạy tay suốt 90 ngày**.

**Nếu không có tính năng này**

Chi phí này **vô hình** — không ai thấy nó trong hoá đơn tổng, và cũng không ai chịu trách nhiệm dọn.

**Tính năng làm gì**

Ghép ba nguồn dữ liệu **đã có sẵn** thành một con số lãnh đạo hiểu ngay:

| Nguồn | Có ở đâu |
|---|---|
| 186 job không ai chạy 90 ngày | 4.1 |
| Bảng có lượt đọc bằng 0 | 5.4 nhật ký truy cập |
| Dung lượng từng bảng | 1.1 |

> *Hiện có **X TB dữ liệu không ai đọc trong 6 tháng**, và **186 job vẫn chạy hằng ngày** để cập nhật chúng. Dừng lại tiết kiệm **Y giờ máy mỗi tháng**.*

**SQLWF hiện có gì**

⚠️ **Có đủ dữ liệu rời rạc** — `sql-history`, `query-history` ghi lịch sử truy vấn; danh sách job có trạng thái. Nhưng **chưa ai ghép lại** thành con số chi phí.

**Cần làm thêm**

Chỉ là một màn tổng hợp. ⭐ **Đây là tính năng công sức thấp nhất mà tự trả tiền cho chính nó** — nên làm đầu tiên.

</details>

<details open>
<summary><b>12 · Khôi phục bảng về thời điểm trước 🆕🔥🔥</b></summary>

**Tình huống**

> `JOB-0412` chạy lúc 6 giờ với một lỗi trong câu SQL vừa sửa hôm qua, **ghi đè 12 triệu dòng bằng dữ liệu sai**.
>
> Cách xử lý hiện tại: sửa câu SQL, rồi **chạy lại từ đầu — mất 4 tiếng**. Trong 4 tiếng đó, mọi báo cáo đọc bảng này đều sai.

**Nếu không có tính năng này**

Mỗi lần ghi sai là **một lần chạy lại toàn bộ**, và thời gian phục hồi bằng đúng thời gian chạy job.

**Tính năng làm gì**

Chọn ảnh chụp trước lần ghi sai → **xem trước khác biệt** *(bao nhiêu dòng sẽ đổi)* → cần **người phê duyệt** → khôi phục trong vài phút → ghi vào nhật ký.

**SQLWF hiện có gì**

⚠️ **Nền tảng dữ liệu của đội dùng Hudi và Iceberg** *(có tài liệu luồng dữ liệu riêng)*. Hai định dạng này **tự giữ ảnh chụp theo thời điểm** — nghĩa là **khả năng quay lại đã có sẵn ở tầng lưu trữ**, chỉ chưa ai mở ra cho người dùng.

> ⚠️ **Mức chắc chắn:** tôi thấy Hudi/Iceberg trong tài liệu luồng dữ liệu của đội, nhưng **không tìm thấy mã nào trong `sqlwf-be` gọi tới ảnh chụp bảng**. Cần đội hạ tầng xác nhận trước khi đưa vào bản trình lãnh đạo.

**Cần làm thêm**

Một nút trong chi tiết bảng, gọi xuống khả năng có sẵn của tầng lưu trữ. 💡 **Giống hệt trường hợp OPA — không phải mua thêm, chỉ là chưa ai mở ra dùng.**

</details>

<details open>
<summary><b>13 · So sánh hai lần chạy để biết vì sao số đổi 🆕🔥🔥</b></summary>

**Tình huống**

> Chị Lan gọi cho anh Hùng: *"Hôm qua báo cáo ra 418.112 giao dịch, hôm nay 412.808. Giảm 5 nghìn. Có phải dữ liệu lỗi không?"*
>
> Anh Hùng **không có cách nào trả lời nhanh**. Phải mở nhật ký job, so số dòng từng bước, đoán xem thay đổi đến từ đâu. Mất nửa buổi, và kết luận cuối cùng là **nghiệp vụ giảm thật**, không phải lỗi.

**Nếu không có tính năng này**

Đây là **câu hỏi phổ biến nhất** của người dùng nghiệp vụ, và mỗi lần hỏi là **nửa buổi của một người kỹ thuật**.

**Tính năng làm gì**

So hai lần chạy hoặc hai ảnh chụp của cùng một bảng, trả lời trong vài giây:

> *So `bi.doi_soat_giao_dich_A` ngày 12/08 với 13/08:*
> *· Bớt **5.304 dòng** — tập trung ở chi nhánh HN và HP*
> *· Cột `so_tien` tổng giảm 2,1%*
> *· ⚠️ **Trùng thời điểm `JOB-0412` đổi sang phiên bản v4.2 lúc 22:15 ngày 12/08***

**SQLWF hiện có gì**

❌ Chưa có so sánh dữ liệu giữa hai thời điểm.

**Cần làm thêm**

Dựa trên ảnh chụp của Hudi/Iceberg *(cùng điều kiện với tính năng 12)*. **Dòng cuối — nối với lịch sử phiên bản job — là thứ giá trị nhất**, vì nó chỉ thẳng nguyên nhân.

</details>

<details open>
<summary><b>14 · Kiểm thử trước khi lên chạy thật ✅ đã có</b></summary>

**Tình huống**

> DE viết job mới, muốn chạy thử xem ra số đúng không, **nhưng không muốn ghi đè dữ liệu thật**.

**SQLWF hiện có gì**

✅ **Đã có** — `updateTestMode` cho phép chạy job ở chế độ thử. Đây là một trong ba tính năng SQLWF đã làm sẵn.

**Cần làm thêm**

Chỉ cần **hiện rõ trên giao diện DMP** và nhắc DE dùng trước khi gửi duyệt. Không phải xây gì.

</details>
---

### Nhóm III — Metadata và tự động hoá khai báo

<details open>
<summary><b>15 · Tự dò cột nhạy cảm, đề xuất nhãn ⭐🔥🔥🔥</b></summary>

**Tình huống**

> Bảng `crm.khach_hang_v2` có cột tên `ma_kh_02`. Nhìn tên thì **không ai đoán được nó chứa gì** — nhưng thực tế nó chứa **số căn cước công dân**.
>
> Vì cột không được gắn nhãn nhạy cảm, nên **mọi chính sách che dữ liệu không áp cho nó**. Bất kỳ ai có quyền đọc bảng đều thấy số căn cước nguyên vẹn — kể cả cộng tác viên thuê ngoài.

**Nếu không có tính năng này**

Hiện **412 cột đã gắn nhãn — tất cả gắn bằng tay**. Trên tổng số cột của 11.482 bảng thì con số đó **chắc chắn còn sót rất nhiều**.

Và **một cột bị bỏ sót làm vô hiệu mọi lớp bảo mật phía sau** — che dữ liệu, lọc theo dòng, nhật ký kiểm toán đều không biết cột đó tồn tại.

**Tính năng làm gì**

Máy quét định kỳ **toàn bộ cột trong kho**, đọc **tên cột + mẫu giá trị + kiểu dữ liệu** rồi nhận ra *"cột này trông như số căn cước"* — **kể cả khi tên cột không gợi ý gì**.

Kết quả vào một hàng chờ kèm **mức độ tin** và **lý do đoán**. Đầu mối nghiệp vụ bấm **Đúng** hoặc **Không phải**.

⭐ Câu trả lời *"Không phải"* **phải được ghi nhớ** — lần sau không hỏi lại cột đó nữa. Không nhớ thì người dùng bỏ mặc cả hàng chờ.

**SQLWF hiện có gì**

⚠️ Có `tagIds` ở **mức cột** với ba nhãn `PD_BASIC` · `PD_SENSITIVE` · `DATA_GENERAL`, và **đã đồng bộ sang OPA**. Nhưng việc gắn nhãn **hoàn toàn thủ công** — không có bộ dò nào.

**Cần làm thêm**

Bộ quét chạy định kỳ + hàng chờ xác nhận. 🔴 **Bắt buộc có người xác nhận, không tự gắn** — gắn sai thì hoặc che nhầm dữ liệu bình thường, hoặc bỏ sót dữ liệu thật.

</details>

<details open>
<summary><b>16 · Máy viết mô tả, người duyệt ⭐🔥🔥🔥</b></summary>

**Tình huống**

> Người mới vào đội mở danh mục, thấy hai bảng: `mart.kpi_kinh_doanh` và `mart.kpi_kinh_doanh_v2`. **Cả hai đều không có mô tả.**
>
> Không biết bảng nào đang dùng, khác nhau chỗ nào, có được xoá bảng cũ không. Phải đi hỏi — và người biết thì đang bận.

**Nếu không có tính năng này**

**7.578 bảng không có người phụ trách, chỉ 28% có mô tả đủ nghĩa.** Cách duy nhất hiện nay là **ngồi gõ tay từng bảng** — với 11 nghìn bảng thì việc này **sẽ không bao giờ xong**, và ai cũng biết điều đó nên **không ai bắt đầu**.

**Tính năng làm gì**

Máy có sẵn **ba nguồn để đoán**, đều đã nằm trong DMP:

| Nguồn | Suy ra được gì |
|---|---|
| Tên bảng và tên cột | `ngay_giao_dich` → *"Ngày phát sinh giao dịch"* |
| ⭐ **Câu SQL của job sinh ra bảng** | Bảng được tính từ đâu, lọc điều kiện gì, gộp theo cột nào |
| Chỉ số đo của cột | Kiểu giá trị, khoảng, tỷ lệ rỗng |

Nguồn thứ hai là thứ **công cụ mua ngoài không có** — vì chúng không nắm câu SQL của job.

**SQLWF hiện có gì**

❌ Chưa có. `data-dictionary` có trường mô tả nhưng **để trống chờ người điền**.

**Cần làm thêm**

🔴 **Máy đề xuất → hàng chờ duyệt ở 2.4 → mới thành mô tả chính thức.** Ghi thẳng vào danh mục thì sau vài tháng **không ai phân biệt được đâu là mô tả thật đâu là máy đoán**, và niềm tin vào danh mục sụp đổ.

**Đo hiệu quả:** tỷ lệ đề xuất được duyệt mà không phải sửa. Dưới 50% thì tắt đi cho đỡ phiền.

</details>

<details open>
<summary><b>17 · Thao tác hàng loạt ⭐🆕🔥🔥🔥</b></summary>

**Tình huống**

> Tài liệu đặt mục tiêu: **gán miền cho 4.334 bảng chưa có miền** và **gán đầu mối cho 7.578 bảng**.
>
> Cách duy nhất hiện nay: mở từng bảng, chọn miền, bấm lưu. Cứ cho là **30 giây một bảng** thì 4.334 bảng mất **36 ngày công** — chưa kể 7.578 bảng còn lại.
>
> Kết quả thực tế: **không ai bắt đầu**, và mục tiêu đó nằm trên giấy.

**Nếu không có tính năng này**

Đây là **tính năng thiếu vắng nghiêm trọng nhất so với quy mô thực tế**. Không có nó thì **mọi con số mục tiêu trong tài liệu đều là lời hứa suông** — không phải vì người lười, mà vì **cách làm bất khả thi về mặt số học**.

**Tính năng làm gì**

| Việc | Chi tiết |
|---|---|
| Chọn nhiều dòng, hoặc **chọn tất cả theo bộ lọc** | *"Tất cả bảng vùng `raw` chưa có miền"* → 1.204 bảng |
| Sửa một hoặc vài trường cho cả nhóm | Gán miền · đầu mối · mức quan trọng · nhãn |
| ⭐ **Xem trước trước khi áp** | *"Sẽ sửa 1.204 bảng — xem danh sách"* |
| **Ghi nhật ký thành một thao tác, hoàn tác được** | Sửa nhầm 1.204 bảng mà không hoàn tác được là thảm hoạ |

**SQLWF hiện có gì**

⚠️ Có **nạp từ file** ở `import-data` với quản lý mẫu đầy đủ — nhưng đó là **nạp dữ liệu nghiệp vụ**, không phải **sửa metadata hàng loạt theo bộ lọc**.

**Cần làm thêm**

Thêm ô tích chọn nhiều dòng + thanh thao tác hàng loạt cho **mọi màn danh sách**, không riêng bảng dữ liệu. ⭐ **Tôi xếp đây là tính năng đáng làm nhất trong nhóm mới.**

</details>

<details open>
<summary><b>18 · Tự sinh luật chất lượng từ mô tả tiếng Việt 🆕🔥</b></summary>

**Tình huống**

> Chị Phương biết chắc quy tắc nghiệp vụ: *"số tiền giao dịch không được âm và không quá 10 tỷ"*. Chị muốn đưa nó thành luật kiểm.
>
> Nhưng màn gán luật đòi chọn loại kiểm tra, điền tham số, và với luật định dạng thì phải **viết biểu thức chính quy**. Chị không biết viết. Phải nhờ DE — DE bận, để đó ba tuần.

**Nếu không có tính năng này**

**Người biết quy tắc nghiệp vụ** *(BDA)* và **người biết viết luật** *(DE)* là hai người khác nhau. Mỗi luật phải đi qua một lần chuyển giao, và đó là chỗ **phần lớn luật chết trước khi được khai**.

Đây là một nguyên nhân của con số **0,6% bảng được kiểm**.

**Tính năng làm gì**

Gõ mô tả bằng tiếng Việt → máy đề xuất luật cụ thể → người xác nhận:

> **Gõ:** *"số tiền không âm và không quá 10 tỷ"*
> **Máy đề xuất:** loại kiểm `value_range` trên cột `so_tien`, từ `0` đến `10.000.000.000`
> **Người bấm:** Đúng → luật được tạo

**SQLWF hiện có gì**

❌ Chưa có. `data-quality` chọn chỉ số từ danh sách cố định.

**Cần làm thêm**

Tận dụng **thư viện 28 loại kiểm tra** đã thiết kế — máy chỉ cần **chọn đúng loại và điền tham số**, không phải sinh mã tự do. Việc này **dễ và an toàn hơn nhiều** so với sinh SQL.

</details>

<details open>
<summary><b>19 · Đề xuất tên đúng chuẩn khi khai 🆕🔥</b></summary>

**Tình huống**

> DE tạo bảng mới, gõ tên `tbl_DoanhThu_2026`. Hệ thống báo đỏ: *"tên không đúng chuẩn"*.
>
> DE **không biết phải sửa thành gì** — chuẩn đặt tên nằm trong một tab của menu cấu hình mà anh chưa từng mở. Anh thử vài lần, cuối cùng gõ đại một tên khác cho qua.

**Nếu không có tính năng này**

Kiểm chuẩn đặt tên là **chặn**. Chặn mà không hướng dẫn thì người dùng **tìm cách lách** chứ không sửa cho đúng — và chuẩn đặt tên thành hình thức.

**Tính năng làm gì**

Thay vì chỉ báo sai, **đề xuất luôn tên đúng**:

> ❌ `tbl_DoanhThu_2026` — sai chuẩn *(có chữ hoa, có tiền tố `tbl_` không nằm trong danh sách)*
> 💡 **Đề xuất:** `bi_doanh_thu_2026` — bấm để dùng

**SQLWF hiện có gì**

❌ Chưa có kiểm chuẩn đặt tên nào *(đây là mục mới trong thiết kế DMP)*.

**Cần làm thêm**

Làm luôn cùng lúc với việc kiểm — **chi phí thêm gần bằng không**, nhưng khác biệt giữa *"bị chặn"* và *"được giúp"*.

</details>

<details open>
<summary><b>20 · Xuất nhập cấu hình giữa các môi trường 🆕🔥</b></summary>

**Tình huống**

> Đội khai **40 luật chất lượng** cho nhóm bảng đối soát trên môi trường thử, kiểm cẩn thận hai tuần, mọi thứ chạy đúng.
>
> Chuyển sang môi trường thật: **phải khai lại từ đầu 40 luật**. Vừa mất công, vừa **có nguy cơ khai lệch** so với bản đã kiểm.

**Nếu không có tính năng này**

Mọi cấu hình cẩn thận trên môi trường thử **không mang sang được**, nên nhiều đội **bỏ luôn bước thử** và khai thẳng lên môi trường thật.

**Tính năng làm gì**

Xuất một nhóm cấu hình *(luật, nhãn, chính sách, mẫu nạp)* ra tệp → nhập vào môi trường khác → **xem trước khác biệt** trước khi áp.

**SQLWF hiện có gì**

⚠️ `configuration-management` có cấu hình theo `taskCode` và **nhật ký cấu hình** *(`detail-log-configuration`)* — có nền, nhưng **chưa có khái niệm chuyển giữa môi trường**.

**Cần làm thêm**

Chức năng xuất/nhập theo nhóm, kèm bước đối chiếu trước khi áp.

</details>

---

### Nhóm IV — Trợ lý và tri thức

<details open>
<summary><b>21 · Bot hỏi đáp tri thức dữ liệu ⭐🔥🔥🔥</b></summary>

**Tình huống**

> 8 giờ sáng, chị Lan cần biết: *"Báo cáo doanh thu ngày hôm nay có dùng được không?"*
>
> Để tự trả lời, chị phải mở **sáu màn**: xem báo cáo lấy số từ bảng nào → mở bảng đó xem chất lượng → xem job nào sinh ra nó → xem job chạy lúc mấy giờ, có lỗi không → xem bảng nguồn có sự cố không → xem ai đang phụ trách để hỏi.
>
> **Mất mười lăm phút.** Nên thực tế chị nhắn tin cho anh Hùng — và anh Hùng cũng phải mở sáu màn đó.

**Nếu không có tính năng này**

Mọi câu hỏi về dữ liệu **đều đổ về một vài người biết việc**, và họ thành nút thắt. Đây là lý do đội kỹ thuật *"suốt ngày bị hỏi"*.

**Tính năng làm gì**

Một câu hỏi, máy tổng hợp từ nhiều menu và trả lời kèm đường dẫn:

> **Hỏi:** *"Báo cáo doanh thu ngày đang có vấn đề gì không?"*
>
> **Trả lời:** *Báo cáo lấy số từ `bi.doanh_thu_thang`, do `JOB-0119` sinh lúc 07:00 hằng ngày, đầu mối là chị Phương.*
> *⚠️ Bảng nguồn `bi.doi_soat_giao_dich_A` **đang có sự cố chưa đóng từ 6 giờ sáng** — số hôm nay nên coi là chưa tin cậy.*
> *Báo cáo có 37 người xem mỗi tuần. Đã gửi cảnh báo cho 2 đầu mối lúc 06:05.*
> *→ Xem: sự cố SC-0231 · báo cáo BC-001 · sơ đồ luồng*

Câu trả lời đó gộp dữ liệu từ **sáu menu** — thứ mà người dùng phải tự mở từng cái.

**SQLWF hiện có gì**

❌ Chưa có.

**Cần làm thêm**

🔴 **Chỉ đọc metadata, tuyệt đối không đọc dữ liệu thật.** Nhờ vậy tính năng này **an toàn hơn hẳn** loại bot hỏi thẳng dữ liệu — sai thì chỉ trỏ nhầm chỗ, mở ra là biết.

</details>

<details open>
<summary><b>22 · Hỏi đáp và nhận cảnh báo qua Telegram ⭐🆕🔥🔥🔥</b></summary>

**Tình huống**

> Hệ thống gửi cảnh báo *"bảng doanh thu có sự cố"* vào màn hình DMP lúc 6 giờ 05.
>
> Nhưng người cần biết là chị Lan — và chị **không mở DMP** vì công việc hằng ngày của chị nằm ở chỗ khác. Chị chỉ mở tool khi cần tra cứu, khoảng một tuần một lần.
>
> **Cảnh báo nằm im trên màn hình không ai xem.**

**Nếu không có tính năng này**

Cảnh báo gửi vào nơi người dùng không mở là **cảnh báo không tồn tại**. Đây là lý do nhiều hệ thống quản trị có đủ tính năng mà **không ai thấy hữu ích**.

**Tính năng làm gì**

| Việc | Chi tiết |
|---|---|
| Nhận cảnh báo **về bảng mình theo dõi** | Nối với tính năng 34 |
| **Hỏi ngược lại ngay trong Telegram** | *"bảng doanh thu hôm nay thế nào"* → trả lời tại chỗ |
| Thao tác nhanh trên tin nhắn | Bấm **Nhận việc** hoặc **Hoãn** không cần mở tool |

**SQLWF hiện có gì**

✅ **Đã có module `telegram` đang chạy**, và `warning-history` đã gửi cảnh báo *(có cả tạo phiếu SOC)*. **Phần khó nhất — kết nối và xác thực — đã xong từ trước.**

**Cần làm thêm**

Mở rộng nội dung tin nhắn và thêm nút thao tác. ⭐ **Đây là tính năng rẻ nhất mà đổi cảm nhận nhiều nhất về tool.**

</details>

<details open>
<summary><b>23 · Tìm kiếm bằng câu nói thường 🔥🔥</b></summary>

**Tình huống**

> Anh Tuấn ở Ban Sản phẩm cần số doanh thu theo chi nhánh. Anh gõ vào ô tìm kiếm: **"doanh thu chi nhánh"**.
>
> Không ra gì — vì bảng thật tên là `mart_dt_cn`, và mô tả của nó để trống.
>
> Anh thử **"doanh thu"**, ra 40 kết quả không biết chọn cái nào. Cuối cùng anh nhắn tin hỏi.

**Nếu không có tính năng này**

Người dùng nghiệp vụ **không biết tên bảng và không cần biết**. Bắt họ tìm theo tên kỹ thuật thì họ sẽ **không dùng tool** — và quay lại hỏi người.

**Tính năng làm gì**

Ánh xạ câu hỏi tiếng Việt qua **từ điển nghiệp vụ và bí danh** để ra đúng bảng. DMP có lợi thế mà công cụ ngoài không có: **thuật ngữ đã được gắn vào cột thật** ở menu 2.1 — tức là **đã có sẵn bản đồ giữa cách nói của người và tên cột kỹ thuật**.

**SQLWF hiện có gì**

❌ **Không có màn tìm kiếm nào** trong 67 màn hiện tại. Muốn tìm bảng phải biết nó nằm ở menu nào.

**Cần làm thêm**

💡 Làm **hai bước**: bước một dùng từ điển và bí danh *(công sức thấp, dữ liệu đã có)*. Chỉ khi bước một không đủ mới tính tới mô hình ngôn ngữ.

</details>

<details open>
<summary><b>24 · Bản tóm tắt tự viết cho lãnh đạo 🔥🔥</b></summary>

**Tình huống**

> Đầu tháng, lãnh đạo mở màn sức khoẻ dữ liệu. Thấy điểm chất lượng **tăng từ 84 lên 87**. Kết luận: *"đang tiến bộ"*.
>
> Thực tế: mức tăng đó đến từ việc **thêm 12 bảng dễ đạt vào diện kiểm**. Nếu chỉ tính trên nhóm bảng đã kiểm từ tháng trước thì điểm **gần như đứng yên**.
>
> **Bảng số không nói ra điều đó** — và cũng không ai có thời gian tự phân tích.

**Nếu không có tính năng này**

Mười chỉ số ngang hàng **không tự giải thích được**, nên lãnh đạo hoặc **hiểu sai xu hướng**, hoặc **bỏ qua luôn màn đó**.

**Tính năng làm gì**

Máy viết một trang tóm tắt bằng lời, nêu **cả điều tốt lẫn điều đáng nghi**:

> **Tháng 8/2026**
> *Điểm chất lượng tăng từ 84 lên 87. **Nhưng phần lớn mức tăng đến từ việc thêm 12 bảng dễ đạt vào diện kiểm, không phải từ cải thiện thật.***
> *Ba sự cố quá hạn đều thuộc miền Vận hành, cùng một đầu mối — nên xem lại phân công.*
> *Việc đáng làm nhất tháng tới: 4.334 bảng chưa gán miền, chiếm 38%.*

**SQLWF hiện có gì**

⚠️ `report-management` có báo cáo quản trị, nhưng đó là **báo cáo vận hành hệ thống**, không phải tóm tắt tình hình dữ liệu.

**Cần làm thêm**

⭐ **Câu quan trọng nhất là câu thứ hai** — thứ khiến bản tóm tắt **đáng tin hơn bảng số**, vì nó tự chỉ ra điểm yếu thay vì chỉ khoe.

</details>

<details open>
<summary><b>25 · Trợ lý viết job biết ngữ cảnh 🔥🔥</b></summary>

**Tình huống**

> DE mới vào đội, được giao viết job tính doanh thu. Anh không biết **bảng nào là bảng chuẩn** để lấy số — trong danh mục có ba bảng tên na ná nhau.
>
> Anh chọn đại một bảng. Bảng đó **đang có sự cố chưa đóng** và **sắp bị ngừng dùng** — nhưng không có gì cảnh báo anh lúc viết.

**Nếu không có tính năng này**

Người mới **mất vài tháng** mới biết bảng nào tin được — kiến thức này hiện nằm trong đầu vài người cũ.

**Tính năng làm gì**

Khác hẳn trợ lý viết mã thông thường:

| Trợ lý viết mã thường | Trợ lý trong DMP |
|---|---|
| Biết cú pháp SQL | Biết **bảng nào thật sự tồn tại**, cột tên gì, kiểu gì |
| Không biết nghiệp vụ | Biết *"doanh thu ghi nhận"* ứng với cột nào bảng nào |
| Không biết tình trạng | ⭐ **Cảnh báo *"bảng này đang có sự cố, cân nhắc dùng bảng khác"*** |
| Không biết quy ước | Kiểm chuẩn đặt tên ngay lúc viết |

**SQLWF hiện có gì**

⚠️ AI tuning **sửa câu SQL đã có**, nhưng **chưa gợi ý lúc đang viết mới**. Đây là mở rộng tự nhiên của thứ đã có.

**Cần làm thêm**

⭐ Dòng đáng giá nhất là **cảnh báo bảng đang có sự cố** — không công cụ bên ngoài nào biết điều đó.

</details>

<details open>
<summary><b>26 · Đọc văn bản quy định, đề xuất mục kiểm 🔥🔥</b></summary>

**Tình huống**

> Pháp chế gửi cho đội một tệp PDF nghị định về bảo vệ dữ liệu cá nhân, kèm lời nhắn: *"đối chiếu xem hệ thống đã đáp ứng chưa"*.
>
> BDA mở ra, **40 trang văn bản pháp lý**. Không biết điều nào liên quan tới dữ liệu mình quản, và **không biết chuyển thành mục kiểm gì**.
>
> Tệp nằm đó ba tháng.

**Nếu không có tính năng này**

Module ⑥ bắt người dùng **tự đọc nghị định rồi tự nghĩ ra danh mục kiểm** — một việc đòi hỏi hiểu cả pháp lý lẫn kỹ thuật, mà **rất ít người làm được cả hai**.

**Tính năng làm gì**

Tải văn bản lên → máy tách từng yêu cầu → đề xuất mục kiểm kèm **cách kiểm**:

> *Điều 17 — thời hạn lưu dữ liệu cá nhân*
> **Đề xuất mục kiểm:** *"Mọi bảng có cột mang nhãn dữ liệu cá nhân phải có quy tắc vòng đời"* — 🤖 **kiểm tự động** *(đọc từ menu 6.2)*
> *📎 Trích dẫn: "...chỉ được lưu trữ trong thời hạn cần thiết..."*

**SQLWF hiện có gì**

❌ Chưa có *(module ⑥ là thiết kế mới của DMP)*.

**Cần làm thêm**

🔴 **Rủi ro pháp lý nếu máy hiểu sai điều khoản.** Bắt buộc: pháp chế duyệt từng mục kiểm, và **luôn hiện kèm trích dẫn nguyên văn** để người duyệt đối chiếu chứ không phải tin máy.

</details>

<details open>
<summary><b>27 · Mở kho metadata cho trợ lý AI 🔥🔥</b></summary>

**Tình huống**

> DE đang viết mã trong công cụ lập trình, dùng trợ lý AI hỗ trợ. Anh muốn biết: *"cột `so_tien` này đang được job nào dùng?"*
>
> Trợ lý AI **không trả lời được** vì nó không thấy kho metadata. Anh phải **rời công cụ đang làm**, mở DMP, tìm bảng, mở tab nguồn gốc, rồi quay lại.
>
> Mỗi lần chuyển ngữ cảnh như vậy mất vài phút — và một ngày làm việc có hàng chục lần.

**Nếu không có tính năng này**

DMP chỉ hữu ích khi người ta **chủ động mở nó**. Thứ hữu ích nhất là thứ **có mặt ngay chỗ người đang làm việc**.

**Tính năng làm gì**

Mở một lớp cho phép trợ lý AI **đọc metadata** — trả lời ngay trong công cụ lập trình: *"cột này ai dùng"*, *"bảng này có nhạy cảm không"*, *"đổi cột này thì hỏng job nào"*.

**SQLWF hiện có gì**

❌ Chưa có lớp mở nào cho trợ lý AI.

**Cần làm thêm**

**Công sức thấp** — chỉ là mở giao diện đọc trên dữ liệu đã có, không đụng giao diện người dùng.

🔴 **Chỉ mở metadata, tuyệt đối không mở dữ liệu thật.** Và phải đi qua đúng lớp quyền ở 5.2 — nếu không thì vừa xây xong lớp che dữ liệu lại **tự mở một cửa sau**.

</details>

<details open>
<summary><b>28 · Chạy thử tác động trước khi đổi 🔥🔥</b></summary>

**Tình huống**

> DE muốn bỏ cột `ma_kh_cu` khỏi bảng vì nghĩ nó không còn dùng. Anh mở sơ đồ nguồn gốc, thấy bảng này **liên quan tới 5 job và 3 báo cáo**.
>
> Nhưng sơ đồ chỉ cho biết **có liên quan** — không cho biết **5 job đó có dùng đúng cột `ma_kh_cu` hay không**. Có thể chúng chỉ dùng các cột khác của cùng bảng.
>
> Không dám xoá. Cột nằm đó thêm hai năm.

**Nếu không có tính năng này**

Sơ đồ luồng trả lời ở **mức bảng**. Nhưng phần lớn thay đổi thật xảy ra ở **mức cột** — nên sơ đồ không giúp ra quyết định được.

**Tính năng làm gì**

Trả lời cụ thể tới từng bước:

> **Hỏi:** *"Bỏ cột `ma_kh_cu` thì sao?"*
>
> **Trả lời:** *2 job sẽ lỗi:*
> *· `JOB-0233` bước 3 — dùng cột này để nối bảng*
> *· `JOB-0501` bước 5 — dùng trong điều kiện lọc*
> *3 job còn lại **không dùng cột này** — an toàn*
> *1 báo cáo hiển thị cột này: BC-007*

**SQLWF hiện có gì**

⚠️ `data-linage` có `getDetailNodeTable`, `getDetailEdge`, `getExpandLineage` — nhưng **thuần xem quan hệ ở mức bảng**, không phân tích mức cột.

**Cần làm thêm**

Cần **bộ phân tích cú pháp SQL** để biết cột được dùng vào việc gì. 💡 Nối thẳng vào quy trình duyệt ở 2.4 — hồ sơ đổi cấu trúc **tự kèm kết quả chạy thử**.

</details>
---

### Nhóm V — Quy trình làm việc *(vai BDA)*

<details open>
<summary><b>29 · Hộp thư "Việc của tôi" ⭐🔥🔥🔥</b></summary>

**Tình huống**

> 8 giờ sáng, anh Hùng mở DMP. Để biết hôm nay phải làm gì, anh phải mở **sáu menu**:
>
> *Phê duyệt* xem có hồ sơ nào chờ mình → *Sự cố chất lượng* xem có phiếu nào được gán → *Yêu cầu cấp quyền* xem có ai xin quyền bảng mình phụ trách → *Đánh giá tuân thủ* xem có mục nào cần khắc phục → *Dữ liệu chủ* xem có cặp trùng nào chờ quyết → *Vòng đời* xem có dữ liệu nào đến hạn xoá.
>
> **Sáu lần mở, sáu lần chờ tải.** Hôm nào bận thì bỏ qua vài menu — và việc ở đó **nằm im không ai biết**.

**Nếu không có tính năng này**

Đây là **tắc nghẽn rõ nhất và rẻ nhất để sửa** trong toàn bộ thiết kế. Hàng chờ nào không được nhìn tới thì **việc trong đó bị bỏ quên** — và bỏ quên hàng chờ chính là cách các tính năng quản trị **chết dần mà không ai để ý**.

**Tính năng làm gì**

Một màn gộp cả sáu nguồn việc, mỗi dòng có:

| Cột | Vì sao cần |
|---|---|
| Loại việc · từ menu nào | Biết bản chất việc |
| **Hạn xử lý và mức quá hạn** | ⭐ Thứ quyết định làm gì trước |
| **Ảnh hưởng tới bao nhiêu thứ** | Sự cố làm sai 4 báo cáo phải xếp trên phiếu chỉ ảnh hưởng 1 bảng tạm |
| Bấm vào là mở đúng màn xử lý | Không phải đi tìm |

**SQLWF hiện có gì**

❌ Có ba chỗ duyệt riêng biệt — `job-approval`, `channel-indexing-management`, `sync-management` — nhưng **mỗi nơi một hàng chờ**, không có chỗ gộp.

**Cần làm thêm**

Gộp thứ đã có thành một màn. **Dữ liệu không phải sinh mới**, chỉ đọc lại từ sáu nguồn. ⭐ **Công sức thấp nhất trong nhóm này.**

</details>

<details open>
<summary><b>30 · Cổng tiếp nhận yêu cầu dữ liệu 🔥🔥</b></summary>

**Tình huống**

> Trưởng phòng Kinh doanh nhắn cho anh Hùng: *"Cho anh số doanh thu theo chi nhánh nhé."*
>
> Hùng phải hỏi lại: doanh thu ghi nhận hay thực thu? · kỳ nào? · chi nhánh cấp mấy? · cần một lần hay định kỳ? · để làm gì?
>
> **Bốn lượt nhắn qua lại trong hai ngày** mới đủ hiểu yêu cầu. Và ba tháng sau, khi có người hỏi *"tháng vừa rồi đội nhận bao nhiêu yêu cầu"* — **không ai trả lời được**, vì tất cả nằm trong chat.

**Nếu không có tính năng này**

Menu 5.3 hiện chỉ xử lý **xin quyền vào bảng đã biết**. Nhưng phần lớn yêu cầu thực tế là loại khác: ***"tôi cần số liệu X mà chưa biết có bảng nào chứa"*** — và loại này **không có chỗ nào trong tool**.

Hệ quả: **không đo được khối lượng công việc của đội**, và không biết bao nhiêu yêu cầu thực ra là **dữ liệu đã có sẵn mà người dùng không tìm thấy**.

**Tính năng làm gì**

Biểu mẫu chuẩn hỏi đủ ngay từ đầu: *cần dữ liệu gì (mô tả bằng lời)* · *dùng để làm gì* · *cần khi nào* · *đã tự tìm chưa*.

Bốn kết cục, cái nào cũng lưu lại:

| Kết cục | Nghĩa |
|---|---|
| ✅ **Đã có sẵn** | Trỏ tới bảng có sẵn → chuyển thành yêu cầu quyền ở 5.3 |
| 🔧 Cần bổ sung | Bảng có nhưng thiếu cột → việc cho DE |
| 🆕 Cần làm mới | Thành yêu cầu dựng job mới |
| ❌ Không làm | **Kèm lý do — cũng phải lưu** |

**SQLWF hiện có gì**

❌ Chưa có. Yêu cầu đi qua chat và email.

**Cần làm thêm**

⭐ **Giá trị lớn nhất không phải biểu mẫu, mà là con số nó tạo ra** — nhất là *"bao nhiêu % yêu cầu hoá ra dữ liệu đã có sẵn"*. Con số đó **đo thẳng chất lượng của tìm kiếm và metadata**, thứ hiện không có cách nào đo.

</details>

<details open>
<summary><b>31 · Bàn giao trách nhiệm hàng loạt 🔥🔥</b></summary>

**Tình huống**

> Anh Hùng phụ trách **148 bảng**. Anh nghỉ phép hai tuần.
>
> Về lý thuyết anh nên chuyển đầu mối sang người khác. Nhưng làm thế nghĩa là **mở 148 bảng, sửa từng cái** — mất cả ngày. Nên anh không làm.
>
> Hai tuần đó, **mọi cảnh báo và sự cố của 148 bảng vẫn gửi cho anh** — và rơi vào hư không.

**Nếu không có tính năng này**

Không chỉ nghỉ phép. Chuyển bộ phận, nghỉ việc, thay đổi phân công — **mọi trường hợp đều tạo ra khoảng mù**.

Nối thẳng với con số trong tài liệu: **9 tài khoản đã nghỉ việc mà chưa khoá, còn quyền trên 132 bảng**.

**Tính năng làm gì**

| Việc | Chi tiết |
|---|---|
| Chọn người bàn giao và người nhận | |
| **Xem trước danh sách sẽ chuyển** | *148 bảng · 12 job · 5 việc đang chờ · 3 quyền phê duyệt* |
| **Chọn kiểu** | Tạm thời *(có ngày về, tự trả lại)* hoặc vĩnh viễn |
| Loại trừ vài mục | Có thứ muốn giữ nguyên |
| Ghi nhật ký | Ai bàn giao cho ai, lúc nào |

**SQLWF hiện có gì**

❌ Chưa có. Phải sửa từng bảng.

**Cần làm thêm**

Dựa trên **tính năng 17 (thao tác hàng loạt)** — về bản chất đây là một trường hợp áp dụng cụ thể của nó. ⭐ Biến việc cho nghỉ việc thành **một thao tác có kiểm soát** thay vì việc ai đó phải nhớ làm.

</details>

<details open>
<summary><b>32 · Xem trước tác động khi sửa nghĩa 🔥</b></summary>

**Tình huống**

> Chị Hà sửa định nghĩa thuật ngữ **"Doanh thu ghi nhận"** cho rõ hơn — thêm một câu về cách xử lý khoản trả lại.
>
> Chị không biết thuật ngữ này **đang gắn vào 18 cột trên 7 bảng, và 4 báo cáo đang dùng nghĩa cũ**.
>
> Sau khi sửa, **mọi thứ vẫn chạy bình thường** — nhưng bốn báo cáo giờ được hiểu theo nghĩa mới, trong khi số liệu vẫn tính theo cách cũ.

**Nếu không có tính năng này**

⚠️ **Đổi nghĩa nguy hiểm hơn đổi kiểu dữ liệu.** Đổi kiểu thì job báo lỗi ngay; **đổi nghĩa thì không có gì báo lỗi cả** — chỉ có người hiểu sai số.

**Tính năng làm gì**

Trước khi lưu, hiện ngay:

> *Thuật ngữ "Doanh thu ghi nhận" đang gắn vào **18 cột** trên **7 bảng**, được **4 báo cáo** dùng.*
> *3 đầu mối cần được báo: chị Phương, anh Hùng, chị Hà.*
> ☑ *Gửi thông báo cho họ sau khi lưu*

**SQLWF hiện có gì**

❌ `data-glossary` có quy trình duyệt thuật ngữ, nhưng **không hiện tác động** lúc sửa.

**Cần làm thêm**

Dữ liệu đã có *(số cột đã gắn ở 2.1, quan hệ luồng ở 2.3)*. Chỉ cần hiện lên **đúng lúc**.

</details>

<details open>
<summary><b>33 · Hướng dẫn tại chỗ cho người mới 🆕🔥</b></summary>

**Tình huống**

> Nhân sự mới vào đội, được cấp tài khoản DMP. Mở lên thấy **27 menu** chia 8 nhóm.
>
> Không biết bắt đầu từ đâu, việc của mình là menu nào, và **thứ tự khai báo ra sao**. Đọc tài liệu thì dài. Hỏi thì ngại.
>
> Kết quả: dùng được 2–3 menu quen thuộc, **24 menu còn lại không bao giờ mở**.

**Nếu không có tính năng này**

Tool càng nhiều tính năng thì **người mới càng dùng ít** — vì không biết cái nào dành cho mình. Đây cũng là lý do các con số độ phủ metadata **không cải thiện** dù tool đã có đủ chức năng.

**Tính năng làm gì**

| Việc | Chi tiết |
|---|---|
| **Danh sách việc cần làm** cho người mới | *"Khai bảng đầu tiên của bạn"* · *"Gán một luật chất lượng"* — có đánh dấu đã xong |
| Chú thích bật tắt được trên màn phức tạp | Chỉ vào từng vùng, giải thích một câu |
| **Gợi ý theo vai trò** | Người dùng thường thấy hướng dẫn khác quản trị viên |

**SQLWF hiện có gì**

❌ Chưa có hướng dẫn tại chỗ.

**Cần làm thêm**

Công sức trung bình nhưng **quyết định tỷ lệ người thật sự dùng tool** — thứ mà mọi tính năng khác đều phụ thuộc vào.

</details>

---

### Nhóm VI — Phục vụ người dùng cuối

<details open>
<summary><b>34 · Đăng ký theo dõi bảng và báo cáo ⭐🔥🔥🔥</b></summary>

**Tình huống**

> 6 giờ sáng, bảng `bi.doi_soat_giao_dich_A` có sự cố. Hệ thống gửi cảnh báo cho **anh Hùng (DE)** và **chị Phương (BDA)** — hai đầu mối phụ trách. Họ biết và đang xử lý.
>
> 9 giờ, chị Lan mở báo cáo doanh thu để chuẩn bị họp. **Chị không nhận được cảnh báo nào**, vì chị không phải đầu mối của bảng đó — chị chỉ là **người dùng số liệu**.
>
> 14 giờ, chị trình bày con số sai trong cuộc họp ban lãnh đạo.

**Nếu không có tính năng này**

🔴 **Đây là lỗ hổng lớn nhất trong toàn bộ thiết kế hiện tại.**
Toàn bộ cơ chế cảnh báo gửi cho **người phụ trách**. Nhưng **người chịu hậu quả** của dữ liệu sai lại là **người dùng nó** — và họ **không nằm trong danh sách nhận cảnh báo nào cả**.

Đội kỹ thuật biết và đang xử lý; người dùng thì không biết gì. **Cả hai bên đều làm đúng việc của mình, mà kết quả vẫn là số sai vào cuộc họp.**

**Tính năng làm gì**

| Việc | Chi tiết |
|---|---|
| Nút **Theo dõi** trên mọi bảng, báo cáo, chỉ tiêu | |
| ⭐ **Tự động theo dõi thứ mình hay dùng** | Suy từ nhật ký truy cập — **không bắt người dùng nhớ bấm** |
| Chọn muốn nhận gì | Chỉ sự cố nghiêm trọng · mọi sự cố · cả thay đổi cấu trúc |
| **Viết bằng lời người dùng hiểu** | Không phải *"luật not_null hỏng"* mà *"số liệu bảng doanh thu hôm nay chưa tin cậy, đang xử lý, dự kiến xong 10 giờ"* |

**SQLWF hiện có gì**

⚠️ `notify-manager` có quản lý **nhóm nhận email** — nhưng đó là **nhóm cố định do quản trị viên khai**, không phải cơ chế người dùng tự đăng ký theo bảng.

**Cần làm thêm**

**Dùng lại toàn bộ hạ tầng cảnh báo đã có** — chỉ mở rộng danh sách người nhận và viết lại nội dung tin nhắn cho người không chuyên. ⭐ **Công sức thấp, giá trị cao nhất trong nhóm này.**

</details>

<details open>
<summary><b>35 · Nhãn tin cậy đi kèm số liệu 🔥🔥</b></summary>

**Tình huống**

> Anh Tuấn xuất một tệp Excel từ hệ thống để gửi cho đối tác. Tệp có 40 nghìn dòng số liệu.
>
> Ba ngày sau đối tác hỏi: *"số này tính đến ngày nào?"* — anh **không nhớ**, và trong tệp **không có thông tin gì** về thời điểm lấy số hay tình trạng dữ liệu lúc đó.

**Nếu không có tính năng này**

Số liệu **rời khỏi hệ thống là mất hết ngữ cảnh**. Mọi thứ DMP biết về chất lượng và thời điểm **không đi theo con số** tới nơi nó được dùng.

**Tính năng làm gì**

| Nơi hiện số | Nhãn kèm theo |
|---|---|
| Tệp Excel xuất ra | Một dòng đầu ghi **thời điểm lấy số + tình trạng dữ liệu** |
| Kết quả truy vấn | *⚠️ Bảng nguồn đang có sự cố chưa đóng* |
| Báo cáo trên công cụ báo cáo | *Số liệu tính lúc 07:11 hôm nay · ✅ nguồn tin cậy* |

**SQLWF hiện có gì**

❌ Chưa có.

**Cần làm thêm**

💡 **Việc khó không phải kỹ thuật mà là tích hợp** — phải chạm vào công cụ báo cáo bên ngoài. Nên làm **tệp xuất trước** *(dễ nhất, DMP kiểm soát được)*, rồi mới tính tới công cụ báo cáo.

</details>

<details open>
<summary><b>36 · Theo dõi tiến trình yêu cầu 🔥</b></summary>

**Tình huống**

> Anh Tuấn gửi yêu cầu xin quyền đọc một bảng. Ba ngày trôi qua, **không có phản hồi gì**.
>
> Anh không biết yêu cầu **đang chờ ai duyệt**, có bị bỏ quên không, hay đơn giản là người duyệt đang bận. Anh cũng **không dám giục** vì không biết giục ai.
>
> Ngày thứ tư anh bỏ cuộc, nhắn tin nhờ đồng nghiệp **lấy hộ số liệu** — vòng qua toàn bộ cơ chế phân quyền.

**Nếu không có tính năng này**

Quy trình xin quyền càng mờ mịt thì người dùng càng **tìm cách lách** — và mọi công sức xây lớp phân quyền thành vô nghĩa.

**Tính năng làm gì**

Màn *"Yêu cầu của tôi"* hiện: đang ở bước nào · **đang chờ ai** · đã chờ bao lâu · dự kiến bao giờ xong *(dựa trên thời gian duyệt trung bình)* · nút **nhắc khéo**.

**SQLWF hiện có gì**

❌ Chưa có màn theo dõi cho người gửi yêu cầu.

**Cần làm thêm**

⭐ Cột **"đang chờ ai"** tạo áp lực xã hội lành mạnh — người duyệt biết mình đang bị nhìn thì xử lý nhanh hơn. Và nó cho lãnh đạo thấy **nút thắt nằm ở người nào** *(nối với tính năng 40)*.

</details>

<details open>
<summary><b>37 · Báo vấn đề ngay tại chỗ ⭐🔥🔥</b></summary>

**Tình huống**

> Chị Lan mở báo cáo doanh thu, thấy con số chi nhánh Hải Phòng **cao gấp ba lần bình thường**. Chị biết chắc là sai — vì chị theo dõi chi nhánh đó hằng tháng.
>
> Nhưng **luật chất lượng không bắt được lỗi này**: số vẫn đúng định dạng, vẫn nằm trong khoảng cho phép, vẫn không rỗng. Chỉ có **người hiểu nghiệp vụ** mới biết nó vô lý.
>
> Chị nhắn cho anh Hùng. Anh đang bận, đọc lướt rồi quên. **Ba tuần sau lỗi mới được phát hiện lại.**

**Nếu không có tính năng này**

Người dùng nghiệp vụ thường là **người đầu tiên phát hiện dữ liệu sai** — vì họ biết con số **lẽ ra phải khoảng bao nhiêu**. Nhưng phản hồi của họ hiện **đi vào chat rồi biến mất**.

**Tính năng làm gì**

Một nút **Báo vấn đề** ngay trên bảng và báo cáo → sinh phiếu ở 3.3, tự gán đầu mối, có hạn xử lý.

⭐ **Vòng lặp đáng giá nhất nằm ở bước sau:**

> Người dùng báo sai → BDA xác nhận đúng là lỗi → **sinh một luật chất lượng để lần sau máy tự bắt**

Đây là cách con số **0,6% bảng được kiểm** tăng lên **theo đúng thứ tự ưu tiên thực tế** — bảng nào hay sai thì được kiểm trước, thay vì khai luật theo cảm tính.

**SQLWF hiện có gì**

❌ Chưa có kênh phản hồi từ người dùng.

**Cần làm thêm**

Rẻ — một nút và một biểu mẫu ngắn, nối vào cơ chế sự cố đã có.

</details>

<details open>
<summary><b>38 · Ai khác đang dùng bảng này 🔥</b></summary>

**Tình huống**

> Anh Tuấn cần hiểu cách tính một cột trong bảng đối soát. Anh nhắn chị Phương *(đầu mối)*.
>
> Chị Phương phụ trách **12 bảng** và nhận khoảng chục câu hỏi mỗi ngày. Ba tiếng sau chị mới trả lời.
>
> Thực tế **anh Nam ở bàn bên** đã làm việc với bảng đó suốt sáu tháng và trả lời được ngay — nhưng anh Tuấn **không biết điều đó**.

**Nếu không có tính năng này**

Đầu mối thành **cửa duy nhất** để hỏi, và cũng thành **nút thắt**. Trong khi tri thức thật ra **đang phân tán ở nhiều người dùng khác**.

**Tính năng làm gì**

Hiện trên chi tiết bảng: *"5 người dùng bảng này nhiều nhất"* và *"3 báo cáo đang dùng"*.

**SQLWF hiện có gì**

⚠️ **Đã có dữ liệu** — `sql-history`, `query-history`, `sql-query-report` ghi lại ai truy vấn gì. Nhưng **chưa hiện lên chỗ người dùng cần**.

**Cần làm thêm**

Chỉ là hiện dữ liệu đã có. 🔴 **Chỉ hiện tên người, không hiện họ đã truy vấn gì** — nếu không thì thành lộ thông tin công việc của nhau.

</details>

<details open>
<summary><b>39 · Trang chủ theo vai trò 🆕🔥🔥</b></summary>

**Tình huống**

> Ba người mở DMP buổi sáng, **cả ba đều thấy màn sức khoẻ dữ liệu** với mười chỉ số quản trị.
>
> Anh Hùng *(DE)* cần biết **việc của mình** — nhưng phải đi tìm.
> Chị Lan *(người dùng)* cần biết **bảng chị theo dõi có sao không** — chỉ số quản trị không liên quan gì tới chị.
> Lãnh đạo cần biết **rủi ro lớn nhất** — mười chỉ số ngang hàng không nói ra điều đó.

**Nếu không có tính năng này**

Màn chung cho tất cả nghĩa là **không phù hợp với ai**. Người dùng phải **tự đi tìm phần liên quan tới mình** mỗi lần mở tool.

**Tính năng làm gì**

| Vai | Mở lên thấy gì |
|---|---|
| Đầu mối nghiệp vụ · kỹ thuật | **Việc của tôi** + bảng tôi phụ trách đang có vấn đề |
| Người dùng | Bảng tôi theo dõi + yêu cầu của tôi đang ở đâu |
| Quản trị dữ liệu | Độ phủ metadata + hàng chờ phê duyệt |
| Lãnh đạo | Ba rủi ro lớn nhất + tiến độ theo miền |

**SQLWF hiện có gì**

⚠️ `acl` có ma trận phân quyền menu theo vai trò — **nền đã có**, nhưng chưa dùng để đổi trang chủ.

**Cần làm thêm**

Ghép các khối đã có theo vai trò. Phụ thuộc tính năng **29** *(hộp thư việc)* và **34** *(theo dõi)*.

</details>

---

### Nhóm VII — Quản trị và điều hành

<details open>
<summary><b>40 · Bảng điều khiển tắc nghẽn quy trình ⭐🔥🔥🔥</b></summary>

**Tình huống**

> Lãnh đạo hỏi trong cuộc họp: *"Sao đội mình xử lý yêu cầu chậm thế?"*
>
> Không ai trả lời được bằng số. Cảm giác chung là *"chắc do nhiều việc quá"*. Nhưng thực tế có thể là: **một người duyệt đang giữ 80% hồ sơ**, hoặc **40% hồ sơ bị trả về vì biểu mẫu khó hiểu** nên phải làm lại từ đầu.
>
> **Hai nguyên nhân đó cần hai cách sửa hoàn toàn khác nhau** — mà không có số thì không biết đường nào.

**Nếu không có tính năng này**

DMP đang **đo chất lượng dữ liệu** rất kỹ, nhưng **chưa ai đo chính quy trình của DMP**. Trong khi dữ liệu để đo thì **tool tự sinh ra hằng ngày** và đang nằm im.

**Tính năng làm gì**

| Chỉ số | Nói lên điều gì |
|---|---|
| **Thời gian từ lúc xin tới lúc có dữ liệu** | Chỉ số quan trọng nhất với người dùng |
| ⭐ **Người duyệt nào đang là nút thắt** | Cả tổ chức biết mơ hồ nhưng không ai có số. Có số thì giải bằng **phân thêm người duyệt**, không phải bằng giục |
| ⭐ **Tỷ lệ hồ sơ bị trả về** | Cao thì **biểu mẫu đang khó hiểu**, không phải người khai kém — chỉ số **tự chỉ ra lỗi thiết kế của chính tool** |
| **Việc tồn đọng lâu nhất ở trạng thái nào** | Chỗ quy trình bị nghẽn |
| ⭐ **Sự cố lặp lại trên cùng một bảng** | Hỏng 6 lần trong 3 tháng = **6 lần chữa triệu chứng**, chưa chữa gốc |

**SQLWF hiện có gì**

❌ Chưa có đo lường quy trình.

**Cần làm thêm**

Đọc lại dữ liệu **đã có sẵn** ở các hàng chờ. Không cần thu thập gì mới.

</details>

<details open>
<summary><b>41 · So sánh miền và giao chỉ tiêu 🔥🔥</b></summary>

**Tình huống**

> Lãnh đạo muốn cải thiện chất lượng dữ liệu, giao chỉ tiêu: *"nâng điểm chất lượng toàn công ty lên 90 trong quý IV"*.
>
> Không ai biết bắt đầu từ đâu. Chỉ tiêu chung cho cả công ty nghĩa là **không ai chịu trách nhiệm cụ thể**, và quý sau họp lại thì điểm vẫn thế.

**Nếu không có tính năng này**

Chỉ tiêu không giao được cho ai thì **không phải chỉ tiêu**.

**Tính năng làm gì**

| Thêm | Chi tiết |
|---|---|
| **Xu hướng theo tháng của từng miền** | Miền nào đang tiến, miền nào đứng yên |
| ⭐ **Chỉ tiêu giao cho từng miền và tiến độ** | *"Miền Vận hành: gán đầu mối cho 500 bảng trong quý III — đã làm 180/500"* |

**SQLWF hiện có gì**

⚠️ `domain-management` đã hiện **BDA/DE phụ trách theo miền** — nền để giao việc đã có. Nhưng chưa có chỉ tiêu và chưa có xu hướng.

**Cần làm thêm**

Thêm bảng chỉ tiêu và biểu đồ xu hướng vào màn 8.1.

</details>

<details open>
<summary><b>42 · Ba rủi ro lớn nhất tuần này 🔥🔥</b></summary>

**Tình huống**

> Lãnh đạo mở màn sức khoẻ dữ liệu trước cuộc họp giao ban. Thấy **mười chỉ số ngang hàng nhau**: điểm chất lượng, độ phủ metadata, số sự cố, tỷ lệ báo động giả…
>
> Con số nào cũng có, nhưng **không biết tuần này nên lo cái nào**. Ba phút trước họp thì không đủ để tự phân tích.

**Nếu không có tính năng này**

Màn nhiều chỉ số **không giúp ra quyết định** — nó chỉ chứng minh là tool có đo. Người bận sẽ **bỏ qua luôn**.

**Tính năng làm gì**

Đúng **ba dòng** ở đầu màn, máy tự xếp theo **mức ảnh hưởng × mức khẩn**:

> 🔴 *Bảng `bi.doi_soat_giao_dich_A` hỏng 3 ngày liên tiếp — 6 báo cáo đang đọc số sai*
> 🟠 *12 quyền truy cập dữ liệu nhạy cảm hết hạn tuần này mà chưa ai xin gia hạn*
> 🟠 *Kỳ đánh giá tuân thủ quý III còn 2 tuần, 8 mục kiểm chưa chạy*

**SQLWF hiện có gì**

❌ Chưa có xếp hạng rủi ro.

**Cần làm thêm**

Một công thức xếp hạng đơn giản trên dữ liệu đã có. ⭐ **Dùng được ngay trong cuộc họp giao ban** — đó là tiêu chí thành công của tính năng này.

</details>

<details open>
<summary><b>43 · Đo mức độ dùng chính tool 🆕🔥</b></summary>

**Tình huống**

> Sau sáu tháng chạy, đội họp đánh giá. Câu hỏi: *"menu nào thật sự có người dùng?"*
>
> Không ai biết. Cảm giác là **vài menu rất hay được mở**, còn lại thì **không chắc**. Nhưng vẫn phải bảo trì cả 27 menu như nhau.

**Nếu không có tính năng này**

Tool **phình dần mà không ai dám bỏ gì** — vì không có bằng chứng menu nào vô dụng. Đây đúng là vấn đề mà tài liệu này **đã phải xử lý một lần** khi rút từ 35 xuống 27 menu.

**Tính năng làm gì**

| Đo gì | Dùng để |
|---|---|
| Menu nào được mở bao nhiêu lần, bởi bao nhiêu người | Menu không ai mở 3 tháng → **cân nhắc bỏ** |
| Tính năng nào được bấm | Nút không ai bấm → bỏ khỏi giao diện |
| Người dùng bỏ dở ở bước nào của biểu mẫu | Chỉ ra chỗ biểu mẫu khó hiểu |

**SQLWF hiện có gì**

⚠️ Có nhật ký truy cập, **nhưng dùng để kiểm toán dữ liệu**, chưa dùng để đo chính tool.

**Cần làm thêm**

⭐ Đây là **cách tự bảo vệ khỏi việc phình menu** — thứ đã xảy ra một lần với chính thiết kế này.

</details>

---

### Nhóm VIII — Nền tảng chuẩn và trợ lý theo yêu cầu

<details open>
<summary><b>44 · Đồng bộ PYC từ Jira → đề xuất hướng làm ⭐🔥🔥🔥</b></summary>

**Tình huống**

> Chị Phương nhận PYC trên Jira: *"Xây báo cáo doanh thu theo chi nhánh, theo tháng, tách theo nhóm sản phẩm, so sánh cùng kỳ năm trước."*
>
> Việc chị làm sau đó, gần như lặp lại y hệt mỗi lần:
>
> | Ngày | Làm gì |
> |---|---|
> | 1–2 | Tìm xem doanh thu nằm ở bảng nào. Hỏi trên nhóm chat. Đợi |
> | 2 (chiều) | Có 3–4 bảng tên na ná. Không rõ cái nào là bản dùng chính thức |
> | 3 (sáng) | Tìm xem đã ai làm báo cáo tương tự chưa — thường là **có**, nhưng không biết ở đâu |
> | 3–4 | Kiểm tra bảng có tin được không: còn nạp không, chất lượng ra sao |
> | 5 | **Mới bắt đầu viết SQL** |
>
> **Bốn ngày đầu không tạo ra gì cả. Toàn là đi tìm.**

**Nếu không có tính năng này**

Bốn ngày đó lặp lại với **mọi PYC, mọi BDA, mọi lần**. Và nguy hiểm hơn: một BDA mới vào **không có cách nào biết** bảng `bi.kh_360_revenue` đã ngừng nạp từ tháng 3 — tên rất khớp, mở ra vẫn có dữ liệu cũ, dùng xong ra số sai.

**Tính năng làm gì**

Đồng bộ PYC từ Jira về, rồi tự dựng một **phiếu đề xuất có cấu trúc, mỗi dòng dẫn được về nguồn**:

| Bảng đề xuất | Vì sao chọn | Sức khoẻ | Độ tin |
|---|---|---|---|
| `bi.doanh_thu_chi_nhanh_thang` | Miền *Tài chính*, có `chi_nhanh` + `thang`, mô tả khớp | 🟢 92đ · nạp đều 08:15 · 0 sự cố 30 ngày | **Cao** |
| `dw.fact_revenue_daily` | Cùng miền, chi tiết theo ngày — cần gộp thêm | 🟡 74đ · 2 sự cố tháng trước | Trung bình |
| ~~`bi.kh_360_revenue`~~ | Tên khớp nhưng **job sinh ra nó đã dừng từ 12/03/2026** | 🔴 Ngừng nạp | **Không dùng** |

Kèm theo: **đã có ai làm tương tự chưa** *(PYC-2025-1187 dùng chính bảng này → xem SQL cũ)* · **điểm cần lưu ý** *(hai bảng dùng hai bộ mã chi nhánh khác nhau; cột `doanh_thu` gắn `PD_BASIC` nên phát hành ngoài phòng ban phải xin duyệt)* · **đầu ra dự kiến**.

⭐ Dòng gạch ngang `bi.kh_360_revenue` **là giá trị lớn nhất** — nó chặn đúng cái lỗi mà người mới chắc chắn sẽ mắc.

**AI nhìn thấy gì:** mô tả PYC + danh sách bảng ứng viên + mô tả bảng + sơ đồ luồng. **Không một dòng dữ liệu nào.**

**SQLWF hiện có gì**

❌ Không có kết nối Jira. Mục 30 *(Cổng tiếp nhận yêu cầu)* là biểu mẫu trong DMP — khác việc: PYC vẫn sẽ ở Jira vì đó là nơi nghiệp vụ đang dùng.

**Cần làm thêm**

Đọc PYC từ Jira · đối chiếu danh mục + luồng + chất lượng · gọi AI nội bộ dựng bản nháp · màn duyệt.

> ⚠️ **Điều kiện phải nói thẳng:** tính năng này **chỉ tốt bằng đúng chất lượng khai báo**. Với 38% bảng chưa gán miền, đề xuất sẽ bỏ sót nhiều. → **Chạy thử trên 2–3 miền đã khai sạch trước**, không mở toàn công ty ngay.
>
> ⭐ **Nhưng đây cũng chính là tính năng biến khai metadata từ *nghĩa vụ* thành *quyền lợi*.** Hôm nay khai xong không ai thấy gì nên không ai khai. Khi khai xong thì PYC của chính mình được đề xuất nguồn tự động — **đó là cách duy nhất tôi thấy để 4.334 bảng kia được gán miền**.

</details>

<details open>
<summary><b>45 · Từ bảng tới khung báo cáo (Tableau / VDSD) 🔥🔥</b></summary>

**Tình huống**

> Chốt xong nguồn dữ liệu, chị Phương còn phải dựng báo cáo trên Tableau: kéo trường vào hàng, kéo trường vào cột, đặt phép gộp, đặt bộ lọc, làm bộ lọc theo tháng, làm cột so sánh cùng kỳ, đặt định dạng số.
>
> Báo cáo tháng trước chị cũng làm đúng chuỗi thao tác đó. Báo cáo tháng trước nữa cũng vậy.

**Nếu không có tính năng này**

Phần **lặp lại** chiếm phần lớn thời gian dựng báo cáo, trong khi phần **cần suy nghĩ** (logic nghiệp vụ riêng) mới là chỗ đáng để BDA bỏ công.

**Tính năng làm gì**

Sinh **bản mô tả báo cáo** — chọn bảng nào, trường nào ra hàng, trường nào ra cột, gộp theo phép gì, lọc gì, biểu đồ loại nào — rồi xuất thành tệp cấu hình cho Tableau hoặc VDSD.

**Ranh giới phải rất rõ:**

| Làm | Không làm |
|---|---|
| Sinh **định nghĩa** báo cáo *(văn bản mô tả cấu trúc)* | ❌ Truy vấn dữ liệu thật |
| Đưa ra **bảng so sánh trước/sau** để người kiểm | ❌ Tự đẩy lên Tableau |
| Xuất tệp cấu hình để người mở lên | ❌ Tự xuất bản, tự chia sẻ |

**SQLWF hiện có gì**

❌ Không có phần báo cáo trực quan.

⭐ **Nhưng khung duyệt thì đã có sẵn:** `sql-history/sql-diff-view` *(so sánh hai phiên bản)* · `job-tuning-review` → `job-tuning-confirm` · trạng thái `TUNED_PENDING_APPLY` · trường `StepsUpdateSource` phân biệt `USER` / `AI_TUNING`. Quy trình *"AI đề xuất → người so sánh → duyệt → mới áp dụng"* **đã dựng xong và đang chạy**.

**Cần làm thêm**

Bộ sinh mô tả báo cáo · bộ xuất sang định dạng Tableau/VDSD · dùng lại màn diff đã có.

> ⚠️ **Đặt kỳ vọng đúng ngay từ đầu:** báo cáo dạng phổ biến *(tổng hợp theo thời gian và một chiều phân loại)* thì bản nháp dùng được **60–70%**. Báo cáo có logic đặc thù *(quy tắc phân bổ, điều kiện loại trừ riêng của phòng ban)* thì AI **không đoán được, và cũng không nên đoán**. Hứa quá thì lần đầu dùng sẽ thất vọng và không ai quay lại.

</details>

<details open>
<summary><b>46 · Danh mục quy định có cấu trúc, máy đối chiếu tuân thủ 🔥🔥</b></summary>

**Tình huống**

> Ý tưởng ban đầu nghe rất tiện: *upload file PDF quy định nội bộ lên, AI đọc rồi đề xuất chính sách bảo vệ dữ liệu.*
>
> Giả sử AI làm đúng, nó đề xuất: *"cột `so_cccd` nên áp mức che PD_SENSITIVE"*. Áp xong, xong việc.
>
> **Sáu tháng sau kiểm toán hỏi: "căn cứ vào đâu?"**

**Nếu không có tính năng này**

Hai rủi ro, và cái thứ hai ít người để ý nhưng nghiêm trọng hơn:

| Rủi ro | Nội dung |
|---|---|
| **Tài liệu rời khỏi nhà** | Quy chế bảo mật, phân cấp phê duyệt, danh mục dữ liệu mật — đẩy lên AI đám mây là gửi ra ngoài |
| ⭐ **Không truy vết được** | Căn cứ là *"AI tóm tắt từ PDF"* thì **không trả lời được kiểm toán**. AI không chỉ ra được điều nào khoản nào, và bản tóm tắt tháng sau sẽ khác bản tháng này |

**Tính năng làm gì**

Đảo ngược chiều: **người đọc, máy đối chiếu.**

```
❌ PDF quy định → AI đọc → AI đề xuất chính sách → áp

✅ PDF quy định → NGƯỜI đọc (Ban Pháp chế / Quản trị dữ liệu)
               → khai vào "Danh mục quy định":
                    số hiệu · ngày ban hành · hiệu lực
                    điều / khoản
                    yêu cầu: "dữ liệu định danh cá nhân phải che khi hiển thị"
                    áp cho: nhãn PD_SENSITIVE
               → MÁY đối chiếu với 412 cột nhạy cảm đang có
               → "144 cột gắn PD_SENSITIVE, trong đó 31 cột chưa có
                  chính sách che nào — vi phạm Điều 7 khoản 2"
               → người duyệt từng dòng
```

Khai một văn bản mất chừng **nửa ngày, làm một lần**. Đổi lại ba thứ mà cách upload PDF không có:

1. ⭐ **Truy vết tới điều khoản** — *"Điều 7 khoản 2 Quy định 123/QĐ-VDS ngày 10/03/2026, người khai chị Phương, ngày khai 15/03/2026"*
2. **Tài liệu không rời khỏi nhà** — AI chỉ thấy dòng luật đã khai
3. **Máy kiểm liên tục** — cột mới gắn `PD_SENSITIVE` là đối chiếu ngay, không chờ ai upload lại PDF

**SQLWF hiện có gì**

❌ Không có danh mục văn bản quy định.

**Cần làm thêm**

Màn khai văn bản → điều khoản → yêu cầu → nhóm dữ liệu áp dụng · bộ đối chiếu định kỳ · phiếu vi phạm.

> 🔄 **Đây là bản thay thế cho mục 26.** Không phải *"không được upload PDF"* — mà **"upload PDF là cách kém hơn"**, kể cả khi bảo mật cho phép.

</details>

<details open>
<summary><b>47 · Nhật ký gọi AI 🔥🔥</b></summary>

**Tình huống**

> Team BDA đã tự làm một tiện ích Chrome *(BDAI)* để hỏi AI về job SQL. Tool làm tốt — nhúng ngữ nghĩa chạy cục bộ, không gửi đi đâu.
>
> **Nhưng bước cuối gọi thẳng `api.openai.com` / `api.anthropic.com` / Gemini bằng API key cá nhân của từng người.**
>
> Nghĩa là: SQL job nội bộ đang rời khỏi nhà mỗi ngày, bằng tài khoản cá nhân, **không ai log lại, không ai biết ai gửi gì**.

**Nếu không có tính năng này**

Không thể mở rộng AI một cách có trách nhiệm. Khi bị hỏi *"AI đang thấy những gì của công ty mình?"* — không trả lời được. Và một câu trả lời không chắc chắn thường dẫn tới quyết định **cấm hết**, mất luôn phần giá trị thật.

**Tính năng làm gì**

Một màn tra cứu, mỗi lần gọi AI một dòng:

| Cột | Nội dung |
|---|---|
| Ai gọi · lúc nào · từ đâu | `username` · thời điểm · `ip` |
| Loại yêu cầu | Tối ưu SQL · giải thích · đề xuất PYC · hỏi đáp |
| **Đã gửi loại thông tin gì** | Mã lệnh · siêu dữ liệu — **và khẳng định không có dữ liệu thật** |
| Đối tượng | Job/bảng nào |
| Kết quả | Thành công · lỗi · người dùng có áp dụng đề xuất không |

Kèm quy tắc: **không ghi được nhật ký thì không cho gọi.**

**SQLWF hiện có gì**

⚠️ **Đã có một nửa.** Gói tin `CommandInfo` gửi sang AI đã mang sẵn `requestId` · `username` · `ip` · `command` · `content`, và `SqlTuningLog` / `JobTuningLog` đã lưu trên Mongo. **Thiếu màn tra cứu và báo cáo tổng hợp.**

**Cần làm thêm**

Màn tra cứu trên dữ liệu log đã có · thống kê theo người/loại/tháng · cảnh báo khi có mẫu bất thường.

> ⭐ **Đây là tính năng rẻ nhất trong cả danh mục mà lại mở khoá cho mọi tính năng AI khác.** Không có nó thì mỗi đề xuất AI mới đều phải tranh luận lại từ đầu về bảo mật.

</details>

---

## Ghi chú về bảy tính năng mới

<details open>
<summary><b>Chi tiết những đề xuất chưa nêu ở các tài liệu trước</b></summary>

### 🆕 17 · Thao tác hàng loạt 🔥🔥🔥

**Vì sao cần**

Đây là **tính năng thiếu vắng nghiêm trọng nhất** so với quy mô thực tế. Tài liệu đặt mục tiêu *gán miền cho 4.334 bảng* và *gán đầu mối cho 7.578 bảng* — nhưng **không màn nào cho sửa nhiều bảng cùng lúc**. Với cách khai từng bảng thì hai việc đó **không bao giờ xong**.

**SQLWF hiện có gì**

⚠️ Có nạp file ở `import-data` với quản lý mẫu đầy đủ. Nhưng đó là **nạp dữ liệu**, không phải **sửa metadata hàng loạt**.

**Cần thêm gì**

| Việc | Chi tiết |
|---|---|
| Chọn nhiều dòng bằng ô tích, hoặc **chọn tất cả theo bộ lọc** | *"Tất cả bảng thuộc vùng `raw` chưa có miền"* |
| Sửa một hoặc vài trường cho cả nhóm | Gán miền · gán đầu mối · gán mức quan trọng · gán nhãn |
| ⭐ **Xem trước trước khi áp** | *"Sẽ sửa 1.204 bảng — xem danh sách"* |
| Ghi nhật ký thành **một thao tác**, hoàn tác được | Sửa nhầm 1.204 bảng mà không hoàn tác được là thảm hoạ |

> ⭐ **Không có tính năng này thì mọi con số mục tiêu trong tài liệu đều là lời hứa suông.** Đây là hạng mục tôi xếp cao nhất trong nhóm mới.

---

### 🆕 22 · Hỏi đáp và nhận cảnh báo qua Telegram 🔥🔥🔥

**Vì sao cần**

Người dùng nghiệp vụ **không mở tool cả ngày**. Cảnh báo gửi vào tool là cảnh báo không ai thấy. Đưa tool tới chỗ họ đang ở thì mới có người dùng.

**SQLWF hiện có gì**

✅ **Đã có module `telegram` đang chạy**, và `warning-history` đã gửi cảnh báo. Hạ tầng có sẵn.

**Cần thêm gì**

| Việc | Chi tiết |
|---|---|
| Nhận cảnh báo **về bảng mình theo dõi** | Nối với tính năng 34 |
| **Hỏi ngược lại** | *"bảng doanh thu hôm nay thế nào"* → trả lời ngay trong Telegram |
| Thao tác nhanh | Bấm nút **Nhận việc** hoặc **Hoãn** ngay trên tin nhắn |

> ⭐ **Đây là tính năng rẻ nhất mà đổi cảm nhận nhiều nhất** — vì phần khó *(kết nối Telegram)* đã chạy từ trước.

---

### 🆕 12 · Khôi phục bảng về thời điểm trước 🔥🔥

**Vì sao cần**

Job ghi sai dữ liệu thì hiện phải **xoá và chạy lại từ đầu** — mất hàng giờ, và trong lúc đó báo cáo đọc phải số sai.

**SQLWF hiện có gì**

⚠️ Nền tảng dữ liệu của đội **dùng Hudi và Iceberg** *(có tài liệu luồng dữ liệu riêng)*. Hai định dạng này **giữ sẵn ảnh chụp theo thời điểm** — tức là **khả năng quay lại đã có sẵn ở tầng lưu trữ**, chỉ là DMP chưa mở ra cho người dùng.

**Cần thêm gì**

Nút **Khôi phục về thời điểm** trong chi tiết bảng: chọn ảnh chụp → xem trước khác biệt → cần **người phê duyệt** → khôi phục → ghi nhật ký.

> 💡 **Đây là ví dụ điển hình của việc *dùng cho đúng tầm thứ đã có*** — giống trường hợp OPA. Không phải mua thêm, chỉ là chưa ai mở ra dùng.

---

### 🆕 13 · So sánh hai lần chạy để biết vì sao số đổi 🔥🔥

Câu hỏi phổ biến nhất của người dùng nghiệp vụ: ***"sao hôm nay số khác hôm qua?"*** — và hiện **không màn nào trả lời được**.

Có ảnh chụp của Hudi/Iceberg thì so được **hai phiên bản của cùng một bảng**: bao nhiêu dòng thêm, bớt, sửa; cột nào đổi nhiều nhất; **thay đổi có trùng với lần đổi phiên bản job nào không**.

---

### 🆕 6 · Cam kết chất lượng theo bảng 🔥

Nhẹ hơn *cam kết dữ liệu đầy đủ* ở tính năng 5. Chỉ là **ba con số cam kết cho bảng quan trọng**: độ trễ tối đa · tỷ lệ rỗng tối đa · tỷ lệ đạt luật tối thiểu. Vi phạm thì mở sự cố kèm mức ưu tiên cao.

⚠️ SQLWF **đã có mầm**: `dqCycleType` · `dqOffset` · `dqDelay` · `dqComparedCycle` — đã có khái niệm chu kỳ và độ trễ, chỉ chưa gọi tên là cam kết và chưa có hệ quả khi vi phạm.

---

### 🆕 39 · Trang chủ theo vai trò 🔥🔥

Năm vai trò có nhu cầu khác hẳn nhau, nhưng hiện **ai mở lên cũng thấy màn sức khoẻ dữ liệu**.

| Vai | Mở lên nên thấy |
|---|---|
| Đầu mối nghiệp vụ · kỹ thuật | **Việc của tôi** + bảng tôi phụ trách đang có vấn đề |
| Người dùng | Bảng tôi theo dõi + yêu cầu của tôi đang ở đâu |
| Quản trị dữ liệu | Độ phủ metadata + hàng chờ phê duyệt |
| Lãnh đạo | Ba rủi ro lớn nhất + tiến độ theo miền |

⚠️ SQLWF đã có phân quyền menu ở `acl` — nền để làm việc này đã có.

---

### 🆕 43 · Đo mức độ dùng chính tool 🔥

Sau 6 tháng chạy, cần biết **menu nào thật sự có người dùng**. Menu không ai mở suốt 3 tháng thì **nên bỏ, đừng bảo trì**.

> ⭐ Đây cũng là **cách tự bảo vệ khỏi việc phình menu** — vấn đề mà tài liệu này đã phải xử lý một lần khi rút từ 35 xuống 27 menu.

</details>

---

## Tổng kết đối chiếu

<details open>
<summary><b>SQLWF đang ở đâu so với 47 tính năng</b></summary>

| Mức | Số tính năng | Nghĩa là |
|---|:---:|---|
| ✅ **Đã có, dùng lại được** | **3** | AI tuning *(7)* · Telegram *(22)* · chế độ chạy thử *(14)* · một phần khôi phục qua Hudi/Iceberg *(12)* |
| ⚠️ **Có một phần, cần nối lại hoặc mở rộng** | **17** | Nhật ký thay đổi · nhóm nhận email · lịch sử truy vấn · cấu hình chu kỳ chất lượng · phân quyền menu · nạp file |
| ❌ **Chưa có** | **27** | Phần lớn nằm ở nhóm **quy trình làm việc** và **phục vụ người dùng cuối** |

> ⭐ **Điều đáng nói nhất khi trình bày:** trong 4 tính năng SQLWF đã có, **hai cái là thứ hiện đại nhất trong cả danh mục** — AI tuning và nền tảng có ảnh chụp dữ liệu. Đơn vị **không đi sau về công nghệ**; cái thiếu là **lớp phối hợp giữa người với người**.

**Sáu tính năng nên làm trước — công sức thấp, tận dụng thứ đã có**

| # | Tính năng | Vì sao chọn |
|:---:|---|---|
| **17** | ⭐ Thao tác hàng loạt | **Không có nó thì mọi con số mục tiêu là lời hứa suông** |
| **22** | ⭐ Telegram hỏi đáp và cảnh báo | Hạ tầng **đã chạy sẵn**, chỉ mở rộng nội dung |
| **29** | ⭐ Hộp thư "Việc của tôi" | Gộp thứ đã có ở 6 hàng chờ |
| **34** | ⭐ Đăng ký theo dõi bảng | Lấp **lỗ hổng lớn nhất**: người dùng không được báo khi dữ liệu hỏng |
| **37** | Báo vấn đề ngay tại chỗ | Rẻ, tạo vòng lặp sinh luật chất lượng mới |
| **7** | ⭐ Cấp ngữ cảnh cho AI tuning | **Nâng cấp thứ đã đầu tư**, không phải xây mới |

**Một câu để trình bày cả danh mục**

> *Đơn vị đã có nền tảng tốt hơn nhiều người nghĩ — có AI tối ưu câu lệnh chạy thật, có nền dữ liệu giữ được ảnh chụp theo thời điểm, có kênh Telegram, có cơ chế phân quyền tới từng hàm. Cái thiếu không phải công nghệ, mà là lớp nối giữa những thứ đó với công việc hằng ngày của người dùng. Sáu tính năng đề xuất làm trước đều dựa trên thứ đã có, không cái nào đòi hạ tầng mới.*

</details>

---

## Phụ lục — Bảy việc sửa trình soạn SQL *(không tính vào danh mục)*

<details open>
<summary><b>Vì sao tách riêng, và vì sao vẫn nên làm trước tiên</b></summary>

Đây là **sửa lỗi dùng của SQLWF**, không phải tính năng mới của DMP — nên không đánh số vào danh mục 47. Nhưng đề nghị **làm trước mọi thứ khác**, vì ba lý do: BDA chạm vào hằng ngày nên cảm nhận được ngay · nó mua lòng tin cho phần trừu tượng phía sau · và **cả bảy việc gộp lại rất rẻ**.

Toàn bộ phản hồi của BDA đã được đối chiếu với mã nguồn — **đều đúng, và chỉ được ra dòng cụ thể**.

| # | Việc | Sự thật trong mã | Công sức |
|:---:|---|---|---|
| a | **Chạy đoạn bôi đen** | `runSqlEvent.emit()` **không truyền tham số**; `getRawQuery()` trả toàn bộ. Cả tệp **không chỗ nào gọi `getSelectedText()`** | **Rất nhỏ** |
| b | **Chú thích khối `Ctrl+Shift+/`** | Không có lệnh nào đăng ký cho việc này | **Rất nhỏ** |
| c | **Bỏ tự định dạng khi rời chuột** | `on('blur')` → định dạng lại **toàn bộ** SQL và nạp lại. Bước job 300 dòng bị xáo cách xuống dòng, con trỏ nhảy sai chỗ | **Rất nhỏ** |
| d | **Trình soạn co giãn** | `minLines: 100` cố định — câu 3 dòng vẫn chiếm một màn hình | Nhỏ |
| e | **Bật gợi ý cột ở mọi màn soạn** | `allowSuggestColumn` mặc định `false`, **chỉ 1 màn bật**. Màn soạn bước job **không có bộ gợi ý cột nào** | Nhỏ |
| f | ⭐ **Gợi ý cột theo bí danh** | `detectTableNames` **chỉ khớp `${BẢNG}` và ``parquet.`...` ``** — không đọc `FROM x AS c`, nên hệ thống **không biết `c` là gì**. Và nó gom cột của mọi bảng vào một danh sách phẳng, không dùng `prefix` | **Vừa** |
| g | **Ngăn lịch sử cạnh trình soạn** | Có **ba** màn lịch sử riêng — phải rời chỗ đang viết mới xem được | Vừa |

**Việc a–e gộp lại chưa tới một ngày công.**

> ⭐ **Điều BDA chưa biết:** họ đang phàn nàn về màn *có* gợi ý cột. Màn soạn bước job — chỗ làm việc chính — **không có gợi ý cột nào cả**, và mọi người đã quen chịu.

Chi tiết từng dòng mã ở [tài liệu AI và lộ trình, Phần 4](DMP-AI-va-Lo-trinh-Nen-tang-Chuan.md#phần-4--trình-soạn-sql-đối-chiếu-phản-hồi-bda-với-mã-nguồn).

</details>
