# Bài trình bày — Đưa AI vào DMP, bắt đầu từ luồng PYC

> **Ngày:** 13/08/2026 · **Người trình bày:** Khôi (BA) · **Thời lượng:** 15 phút + hỏi đáp
>
> Tài liệu này viết theo **ngôn ngữ nghiệp vụ**, để đọc thẳng trong cuộc họp. Phần kỹ thuật đầy đủ ở [Tài liệu AI và lộ trình](DMP-AI-va-Lo-trinh-Nen-tang-Chuan.md) · [Danh mục 47 tính năng](DMP-Danh-muc-Tinh-nang-De-xuat.md).

---

## 1. Hai phút đầu — nói gì

> **Chúng tôi không đề xuất "làm AI cho DMP".**
>
> Chúng tôi đề xuất đưa AI vào **đúng một chỗ**: chỗ mà hôm nay một BDA mất **bốn ngày chỉ để đi tìm**, trước khi viết được dòng đầu tiên.
>
> Bốn ngày đó lặp lại với **mọi phiếu yêu cầu, mọi BDA, mọi lần**. Không ai tạo ra giá trị gì trong bốn ngày đó. Toàn là đi hỏi và đợi.
>
> **Và điều quan trọng nhất tôi muốn nói ngay từ đầu:** AI trong đề xuất này **không đọc một dòng dữ liệu nào của khách hàng**. Nó chỉ đọc *cách dữ liệu được tạo ra* — mô tả bảng, sơ đồ luồng, câu lệnh. Không đọc *dữ liệu được tạo ra*.
>
> Đây là ràng buộc chúng tôi **tự đặt cho mình**, không phải bị ép.

---

## 2. AI đặt ở đâu — một chỗ, không rải khắp

Có 27 menu trong thiết kế DMP. Nếu gắn AI vào từng menu thì thành 27 chỗ nửa vời và không chỗ nào dùng được.

**Chúng tôi đề xuất một điểm duy nhất:** menu **5.3 — Yêu cầu dữ liệu**, chỗ tiếp nhận và xử lý phiếu yêu cầu.

Vì sao chọn đúng chỗ này:

| Lý do | Nội dung |
|---|---|
| **Đây là cửa vào của mọi việc** | Mọi báo cáo, mọi bảng mới đều bắt đầu từ một phiếu yêu cầu. Sửa được chỗ này là sửa được đầu nguồn |
| **Đây là chỗ mất nhiều thời gian nhất** | Bốn ngày đi tìm, so với một ngày viết |
| **Đây là chỗ AI làm được nhiều nhất** | Việc *đi tìm và đối chiếu* đúng là thứ máy làm nhanh hơn người rất nhiều |
| **Đây là chỗ đo được** | Trước và sau, so bằng số ngày. Không cần tranh luận cảm tính |
| **Và quan trọng nhất** | Nó **kéo theo việc khai metadata** — xem mục 7 |

Các menu khác **không đổi**. AI chỉ *đọc* dữ liệu khai báo ở đó, không chen vào giao diện của chúng.

---

## 3. Ba nhóm người — mỗi nhóm được gì

### 🟦 Đơn vị nghiệp vụ *(người gửi yêu cầu — Kinh doanh, Tài chính, Marketing…)*

Hôm nay họ gửi yêu cầu xong thì **mất dấu**. Không biết đang chờ ai, không biết bao giờ có, phải đi hỏi.

| Nhận được | Cụ thể |
|---|---|
| **Biết ngay yêu cầu của mình có làm được không** | Ngay khi gửi, hệ thống trả lời: *"Dữ liệu anh cần đã có, ước tính 2 ngày"* — hoặc *"Yêu cầu so sánh 3 năm, nhưng dữ liệu chỉ lưu 18 tháng. Cần trao đổi lại"* |
| **Biết đang ở bước nào** | Không phải đi hỏi |
| **Biết đã có sẵn báo cáo tương tự chưa** | Rất nhiều yêu cầu trùng với thứ đã làm rồi. Trả lời được ngay trong ngày thay vì làm lại từ đầu |

> ⭐ Điểm đáng nói: cái câu *"dữ liệu chỉ lưu 18 tháng"* — hôm nay chỉ **phát hiện ra ở ngày thứ tư**, sau khi BDA đã bỏ công đi tìm. Trả lời ngay hôm gửi thì tiết kiệm cho cả hai bên.

### 🟩 BDA *(người xử lý yêu cầu)*

| Nhận được | Cụ thể |
|---|---|
| ⭐ **Bốn ngày đi tìm → nửa ngày kiểm lại** | Máy dựng sẵn danh sách nguyên liệu, BDA kiểm và sửa |
| ⭐ **Không mắc bẫy bảng chết** | Máy gạch ngang bảng mà job sinh ra nó đã dừng — lỗi mà người mới **chắc chắn** sẽ mắc |
| **Không phải hỏi trên nhóm chat** | Thông tin nghiệp vụ về bảng nằm ngay trong phiếu |
| **Thấy ai đã làm việc tương tự** | Kèm câu lệnh cũ để tham khảo |
| **Biết trước rào cản** | *"Cột này gắn nhãn nhạy cảm, phát hành ngoài phòng ban cần duyệt"* — biết từ đầu thay vì biết lúc sắp bàn giao |

### 🟪 Lãnh đạo

| Nhận được | Cụ thể |
|---|---|
| **Thời gian phục vụ yêu cầu đo được** | Chỉ số duy nhất người dùng thật sự quan tâm |
| **Thấy chỗ nghẽn** | Nghẽn ở khâu tìm dữ liệu, hay khâu duyệt, hay khâu làm |
| ⭐ **Biết mức độ sẵn sàng của kho dữ liệu** | Tỷ lệ yêu cầu mà máy **không đề xuất được** chính là **thước đo dữ liệu còn thiếu khai báo tới đâu** — lần đầu tiên có con số cho việc này |

---

## 4. Kịch bản chính — kể bằng chuyện

### Hôm nay

> **Thứ hai.** Chị Phương nhận phiếu trên Jira: *"Xây báo cáo doanh thu theo chi nhánh, theo tháng, tách theo nhóm sản phẩm, so sánh cùng kỳ năm trước."*
>
> **Thứ hai – thứ ba.** Đi tìm doanh thu nằm ở bảng nào. Hỏi trên nhóm chat. Đợi người rảnh trả lời.
>
> **Thứ ba chiều.** Tìm ra ba bảng tên na ná nhau. Không rõ cái nào là bản dùng chính thức.
>
> **Thứ tư sáng.** Nghi có người từng làm báo cáo tương tự. Đi hỏi. Đúng là có, từ năm ngoái — nhưng phải hỏi ba người mới lần ra.
>
> **Thứ tư – thứ năm.** Kiểm tra bảng có tin được không: còn nạp đều không, số có sạch không.
>
> **Thứ sáu.** *Mới bắt đầu viết câu lệnh đầu tiên.*

**Bốn ngày. Không tạo ra gì. Toàn đi tìm.**

Và nếu chị Phương là người mới, có khả năng chị chọn nhầm bảng `bi.kh_360_revenue` — tên rất khớp, mở ra vẫn thấy dữ liệu — mà không biết **job sinh ra nó đã dừng từ tháng 3**.

### Sau khi có tính năng

> **Thứ hai, 9 giờ.** Phiếu về từ Jira. Hệ thống tự đọc, tự dựng **phiếu công thức**.
>
> **Thứ hai, 9 giờ 30.** Chị Phương mở ra xem. Chị bỏ một bảng máy gợi ý sai, thêm một điều kiện lọc mà chỉ chị biết, sửa lại cách tính so cùng kỳ.
>
> **Thứ hai chiều.** Bắt đầu viết câu lệnh.

**Bốn ngày rút xuống nửa ngày.** Không phải vì máy giỏi hơn người — mà vì **việc đi tìm và đối chiếu vốn không nên là việc của người**.

### Phiếu công thức trông như thế nào

Không phải một đoạn văn AI viết. Là **một tờ phiếu có cấu trúc, mỗi dòng dẫn được về nguồn** — vì thứ BDA cần là *dấu vết để tự kiểm*, không phải một bài văn hay.

> **PHIẾU CÔNG THỨC — PYC-2026-0842 · Báo cáo doanh thu theo chi nhánh**
>
> **① Nguyên liệu — lấy dữ liệu ở đâu**
>
> | Bảng | Vì sao chọn | Sức khoẻ | Dùng được? |
> |---|---|---|---|
> | `bi.doanh_thu_chi_nhanh_thang` | Miền *Tài chính* · có sẵn chiều *chi nhánh* và *tháng* · mô tả khớp yêu cầu | 🟢 92đ · nạp đều 08:15 · 0 sự cố 30 ngày | **Nên dùng** |
> | `dim.nhom_san_pham` | Cần để tách theo nhóm sản phẩm | 🟢 Bảng danh mục, ít đổi | **Nên dùng** |
> | `dw.fact_revenue_daily` | Cùng miền, chi tiết theo ngày — dùng nếu cần chi tiết hơn | 🟡 74đ · 2 sự cố tháng trước | Phương án 2 |
> | ~~`bi.kh_360_revenue`~~ | Tên khớp, **nhưng job sinh ra nó đã dừng 12/03/2026** | 🔴 Ngừng nạp | **Không dùng** |
>
> **② Cách nối — ghép nguyên liệu với nhau**
>
> `bi.doanh_thu_chi_nhanh_thang` nối `dim.nhom_san_pham` qua `ma_nhom_sp`
> ⚠️ **Lưu ý:** hai bảng dùng **hai bộ mã chi nhánh khác nhau** — cần đi qua bảng ánh xạ `dim.chi_nhanh_mapping`
>
> **③ Cách tính**
>
> Gộp theo: `thang` · `ma_chi_nhanh` · `nhom_san_pham` — Tính: tổng `doanh_thu`
> So cùng kỳ: lệch 12 tháng trên cột `thang`
>
> **④ Đã có ai làm tương tự chưa**
>
> Có. **PYC-2025-1187** *"Doanh thu theo vùng"* (anh Tuấn, 09/2025) dùng chính bảng này. Thời gian làm thực tế: **3 ngày**. → `[Xem câu lệnh cũ]`
>
> **⑤ Rào cản cần biết trước**
>
> - ⚠️ Yêu cầu *so sánh cùng kỳ* cần dữ liệu từ 01/2025. Bảng lưu **18 tháng** → **đủ, nhưng sát mép**
> - ⚠️ Cột `doanh_thu` gắn nhãn `PD_BASIC` → phát hành ngoài phòng ban **cần xin duyệt**
> - ℹ️ Bảng chưa có mô tả nghiệp vụ do người khai — phần giải thích trên **suy từ câu lệnh của job**, chưa ai xác nhận
>
> **⑥ Đầu ra dự kiến**
>
> Bảng `bi.rpt_doanh_thu_cn_thang` — các trường `thang`, `ma_chi_nhanh`, `nhom_san_pham`, `doanh_thu`, `doanh_thu_cung_ky`, `tang_truong_pct`
>
> `⚠️ Bản nháp do máy dựng từ khai báo hiện có. BDA phải kiểm trước khi dùng.`

> ⭐ **Nếu chỉ được chỉ một dòng đáng tiền nhất trên tờ phiếu này** — đó là dòng gạch ngang `bi.kh_360_revenue`. Nó không giúp làm nhanh hơn; **nó chặn một báo cáo sai không ra tới cuộc họp**.

---

## 5. Bên dưới lưu gì — sáu nhóm nguyên liệu

Đây là phần trả lời câu *"muốn làm được như trên thì phải khai những gì"*.

Cách hình dung: muốn máy **gợi ý được công thức**, nó phải biết **trong bếp có gì**. Sáu nhóm thông tin dưới đây chính là *bản kê nguyên liệu*.

### Nhóm A — Nhận diện nguyên liệu *(khớp yêu cầu với bảng)*

| Lưu ở đâu | Các trường |
|---|---|
| **Bảng** | tên · **miền nghiệp vụ** · **mô tả nghiệp vụ** · lớp *(thô / kho / báo cáo)* · chủ sở hữu · từ khoá chủ đề |
| **Cột** | tên · kiểu · **mô tả nghiệp vụ** · **đơn vị đo** *(đồng · %·  cái)* · nhãn nhạy cảm |

**Trả lời câu:** *"Doanh thu nằm ở bảng nào?"*
**Tính ra được:** điểm khớp giữa từ khoá trong phiếu yêu cầu và mô tả bảng/cột → danh sách bảng ứng viên xếp hạng.

### Nhóm B — ⭐ Vai trò của từng cột *(nhóm quan trọng nhất và đang thiếu hoàn toàn)*

| Trường | Bốn giá trị |
|---|---|
| **Vai trò cột** | **Chiều** *(gộp theo nó — chi nhánh, nhóm sản phẩm)* · **Đo lường** *(tính toán trên nó — doanh thu, số lượng)* · **Thời gian** *(trục thời gian — tháng, ngày)* · **Khoá** *(dùng để nối bảng)* |

**Trả lời câu:** *"Gộp theo cái gì, tính cái gì?"*

**Tính ra được:** đây chính là thứ cho phép máy **tự dựng phần ③ Cách tính**. Yêu cầu nói *"doanh thu theo chi nhánh theo tháng"* → máy tìm cột vai trò *đo lường* tên khớp *doanh thu*, hai cột vai trò *chiều* và *thời gian* khớp *chi nhánh* và *tháng*. Không có trường này thì máy **chỉ đoán mò theo tên cột**.

> ⭐ **Đây là chỗ hay nhất của cả đề xuất, và cũng là chỗ ít người nghĩ tới:**
>
> Vai trò cột **không cần ai gõ tay** — máy suy được từ **chính câu lệnh của 1.842 job đang chạy**:
>
> | Cột xuất hiện ở đâu trong câu lệnh | Suy ra vai trò |
> |---|---|
> | Trong mệnh đề gộp `GROUP BY` | **Chiều** |
> | Trong phép tính `SUM` / `AVG` / `COUNT` | **Đo lường** |
> | Kiểu ngày, dùng để chia phân vùng | **Thời gian** |
> | Trong điều kiện nối `JOIN ... ON` | **Khoá** |
>
> Nghĩa là: **đọc mã lệnh, không đọc dữ liệu** — đúng nguyên tắc an toàn đã đặt. Và làm một lần cho toàn bộ 1.842 job thì **phủ được phần lớn các bảng đang thực sự được dùng**.
>
> **Một nhóm thông tin đang thiếu 100%, nhưng lấp được gần hết bằng máy, mà không đụng tới dữ liệu.**

### Nhóm C — Nguyên liệu còn tươi không

| Trường |
|---|
| lần nạp gần nhất · **giờ nạp thường lệ** · **số dòng thường lệ** · **tỷ lệ rỗng thường lệ** · điểm chất lượng · số sự cố 30/90 ngày · trạng thái job nguồn · ⭐ **độ sâu lịch sử** *(lưu được bao nhiêu tháng)* |

**Trả lời câu:** *"Bảng này tin được không?"*

**Tính ra được:** cờ 🟢🟡🔴 cho từng nguyên liệu · **gạch ngang bảng chết** · và cảnh báo sớm loại này:

> *"Yêu cầu so sánh cùng kỳ cần dữ liệu từ 01/2025. Bảng chỉ lưu 18 tháng."*

Hôm nay câu này **chỉ lộ ra ở ngày thứ tư**. Có trường *độ sâu lịch sử* thì lộ ra **trong 5 giây**.

### Nhóm D — Lấy ở đâu, đã có bản chuẩn chưa

| Trường |
|---|
| job nào sinh ra bảng · bảng đọc từ đâu · bảng nào dùng nó · ⭐ **đánh dấu bản dùng chính thức** · nhóm bảng trùng lặp |

**Trả lời câu:** *"Ba bảng tên na ná, dùng cái nào?"*

**Tính ra được:** chọn đúng bảng ở lớp phù hợp · loại bảng không còn nạp · cảnh báo *"còn 2 bảng khác gần giống, đã có bản chuẩn là bảng X"*.

### Nhóm E — Đã ai nấu món này chưa

| Trường |
|---|
| PYC cũ: mô tả · **bảng đã dùng** · câu lệnh / job kết quả · báo cáo đầu ra · người làm · ⭐ **thời gian làm thực tế** |

**Trả lời câu:** *"Có phải làm lại từ đầu không?"*

**Tính ra được:** gợi ý tái sử dụng · và **ước lượng công sức có căn cứ**: *"phiếu tương tự năm ngoái mất 3 ngày"* — thay vì đoán.

> ⭐ Đây là nhóm **rẻ nhất mà giá trị lên nhanh nhất**: mỗi phiếu làm xong tự động trở thành nguyên liệu cho phiếu sau. Càng dùng càng tốt lên, không cần ai bỏ công riêng.

### Nhóm F — Có được phép không

| Trường |
|---|
| nhãn nhạy cảm của cột · chính sách che đang áp · phạm vi được phép phát hành · điều khoản quy định liên quan |

**Trả lời câu:** *"Báo cáo này có được gửi ra ngoài phòng ban không?"*

**Tính ra được:** cảnh báo **ngay từ đầu** thay vì lúc sắp bàn giao.

---

## 6. Máy tính ra được gì — sáu đầu ra

| # | Đầu ra | Từ nhóm nào |
|:---:|---|---|
| 1 | **Danh sách nguyên liệu xếp hạng** — bảng nào, vì sao, có gạch ngang cái không dùng được | A · C · D |
| 2 | **Cách nối** — nối bảng nào với bảng nào qua cột gì, cảnh báo khác bộ mã | B · D |
| 3 | **Cách tính** — gộp theo gì, tính gì, so kỳ thế nào | B |
| 4 | **Việc đã làm tương tự** — kèm câu lệnh cũ và thời gian thực tế | E |
| 5 | **Danh sách rào cản** — thiếu lịch sử, cần duyệt phát hành, khác bộ mã | C · F |
| 6 | **Khung câu lệnh nháp + khung báo cáo** để BDA sửa tiếp | tất cả |

**Và một đầu ra cho lãnh đạo, không nằm trong phiếu:**

> **Tỷ lệ phiếu mà máy không đề xuất được** — chia theo miền nghiệp vụ.
>
> Đây là **thước đo mức độ sẵn sàng của kho dữ liệu**, lần đầu tiên có số. Miền nào tỷ lệ cao thì miền đó khai báo còn thiếu — và biết chính xác thiếu nhóm nào trong sáu nhóm trên.

---

## 7. Hôm nay có bao nhiêu phần trong sáu nhóm đó

Phần này **không tô hồng**, vì nó quyết định lộ trình.

| Nhóm | Hôm nay | Đánh giá |
|---|---|---|
| **A** Nhận diện | Miền: **62%** · Chủ sở hữu: **34%** · Mô tả bảng: **28%** · Mô tả cột: chưa đo | 🟡 Một nửa |
| **B** ⭐ Vai trò cột | **0%** — hệ thống chưa có khái niệm này | 🔴 Thiếu hoàn toàn — **nhưng lấp được bằng máy** |
| **C** Độ tươi | Chất lượng: **0,6%** bảng có luật kiểm · Nhịp nạp: chưa có · Độ sâu lịch sử: chưa có trường | 🔴 Gần như chưa có |
| **D** Nguồn gốc | Có cơ chế luồng dữ liệu · Chưa đánh dấu bản chuẩn · **Chưa biết bao nhiêu % job bật ghi nhận luồng** | 🟡 Có nền, cần đo |
| **E** Việc cũ | PYC nằm ở Jira, **chưa đồng bộ về** | 🔴 Chưa có |
| **F** Quyền phát hành | **412 cột** đã gắn nhãn · Có cơ chế chính sách | 🟡 Có cơ chế, phủ còn mỏng |

### Đọc bảng này ra ba kết luận

**① Chưa làm được ngay toàn công ty.** Nói thẳng điều này thì đáng tin hơn.

**② Nhưng ba nhóm thiếu nhất lại là ba nhóm bù được bằng máy, không cần người gõ tay:**

| Nhóm | Cách bù | Ghi chú |
|---|---|---|
| **B** Vai trò cột | Đọc câu lệnh 1.842 job → suy vai trò | Chỉ đọc mã, không đọc dữ liệu |
| **C** Nhịp nạp | Quan sát 30 ngày → tự tính khoảng bình thường | Chỉ đếm dòng, không đọc nội dung |
| **E** Việc cũ | Đồng bộ PYC từ Jira, tự tích luỹ từ đây về sau | Càng dùng càng dày |

**③ Cho nên đề nghị chạy thử có phạm vi:** chọn **2–3 miền nghiệp vụ** đã khai tương đối sạch, làm đủ sáu nhóm cho riêng miền đó, đo kết quả thật, rồi mới mở rộng.

> ⭐ **Và đây là điều tôi muốn nhấn mạnh nhất trong cả buổi:**
>
> Hôm nay chúng ta bảo mọi người *"hãy khai metadata cho đầy đủ"* — và **không ai làm**. Không phải vì lười. Vì khai xong **không thấy gì thay đổi**. Đó là nghĩa vụ, không có phần thưởng.
>
> Khi tính năng này chạy, khai metadata thành **quyền lợi**: khai xong thì **phiếu yêu cầu của chính mình được đề xuất nguồn tự động**, đỡ được bốn ngày.
>
> **Theo tôi đây là cách duy nhất để 4.334 bảng chưa gán miền kia được khai.** Không phải bằng chỉ thị.

---

## 8. Ranh giới — những gì chúng tôi cam kết KHÔNG làm

| Không làm | Vì sao |
|---|---|
| ❌ **AI không đọc một dòng dữ liệu nào** — không lấy mẫu, không "chỉ 5 dòng đầu để đoán kiểu cột" | Đây là điều cấm, không có ngoại lệ |
| ❌ **Không đưa tài liệu nội bộ nguyên văn cho AI** | Thay bằng khai thành dòng luật có cấu trúc — vừa an toàn, vừa **truy vết được tới điều khoản** khi kiểm toán hỏi |
| ❌ **AI không tự sửa job, không tự chạy, không tự cấp quyền** | Mọi đề xuất đều qua người duyệt |
| ❌ **Không dùng AI đám mây bằng tài khoản cá nhân** | Dùng kênh nội bộ, có ghi nhật ký |
| ❌ **Không tự xuất bản báo cáo** | Sinh bản nháp thì được; xuất bản là việc của người |

**Một điều nên nói trước khi bị hỏi:**

> Gần như mọi công cụ trên thị trường đều có tính năng *"AI đọc dữ liệu mẫu rồi tự viết mô tả cột"*. Đó là tính năng bán chạy nhất của họ.
>
> **Chúng tôi cố tình bỏ tính năng đó.** Đổi lại, ngữ nghĩa lấy từ câu lệnh của job và từ khai báo của người dùng — chậm hơn, nhưng không đánh đổi dữ liệu khách hàng.
>
> Nói trước thì đó là **lựa chọn có chủ đích**. Không nói, để phát hiện sau, thì đó là **thiếu sót**.

**Và một điều nữa nên nói, vì sớm muộn cũng lộ:**

> Team BDA đã tự làm một công cụ hỏi AI về job SQL, và nó chạy được. **Đó là bằng chứng nhu cầu này có thật.**
>
> Nhưng công cụ đó đang gửi câu lệnh nội bộ ra dịch vụ AI bên ngoài bằng tài khoản cá nhân, không ai ghi nhận lại. **Đưa việc này lên hệ thống thì vừa an toàn hơn, vừa mạnh hơn** — vì có thêm thông tin về chất lượng, đầu mối, nhãn nhạy cảm mà công cụ cá nhân không thể có.

---

## 9. Chúng tôi xin gì

| # | Xin | Ghi chú |
|:---:|---|---|
| 1 | **Chấp thuận nguyên tắc** *"AI đọc cách dữ liệu được tạo ra, không đọc dữ liệu"* | Đây là thứ cần chốt trước mọi thứ khác |
| 2 | **Chọn 2–3 miền nghiệp vụ để chạy thử** | Đề nghị chọn miền có đầu mối rõ và đang nhiều yêu cầu |
| 3 | **Cho phép đồng bộ phiếu yêu cầu từ Jira** *(chỉ đọc)* | Cần phối hợp với đội quản trị Jira |
| 4 | **Xác nhận AI service nội bộ đang dùng cho tối ưu câu lệnh** đặt ở đâu, có ràng buộc dữ liệu gì | Cần đội hạ tầng trả lời |
| 5 | **Rủ team BDA tham gia từ đầu** | Họ đã có kinh nghiệm thực tế, và tránh làm trùng |

### Đo thành công bằng gì

| Chỉ số | Hôm nay | Mục tiêu sau chạy thử |
|---|---|---|
| Thời gian từ nhận phiếu tới bắt đầu viết câu lệnh | **~4 ngày** | **≤ 1 ngày** |
| Tỷ lệ phiếu máy đề xuất được nguồn | — | **≥ 70%** trên miền chạy thử |
| Tỷ lệ đề xuất bị BDA đánh dấu sai | — | **≤ 20%** |
| Số bảng được gán miền / mô tả trong kỳ | Gần như không tăng | **Tăng rõ** — hệ quả gián tiếp |

> Chỉ số cuối cùng là chỉ số tôi quan tâm nhất. Nếu nó không tăng, nghĩa là **động lực khai báo vẫn chưa hình thành** — và khi đó phải xem lại cách làm, chứ không phải làm tiếp cho xong.

---

## 10. Nếu chỉ được nói một câu

> *Hôm nay một yêu cầu dữ liệu mất bốn ngày chỉ để đi tìm nguyên liệu, trước khi ai đó bắt đầu làm. Chúng tôi đề xuất để máy làm phần đi tìm đó — đọc mô tả, sơ đồ luồng và câu lệnh sẵn có để dựng trước một bản công thức, rồi người kiểm lại. AI trong đề xuất này không đọc một dòng dữ liệu khách hàng nào. Và tác dụng phụ đáng giá nhất là nó biến việc khai metadata từ nghĩa vụ thành quyền lợi — thứ mà mọi chỉ thị từ trước tới nay chưa làm được.*

---

## Phụ lục — Câu hỏi có thể bị hỏi

| Câu hỏi | Trả lời |
|---|---|
| *"AI có đọc được dữ liệu khách hàng không?"* | Không. Gói tin gửi sang AI chỉ có một trường nội dung, chứa câu lệnh và mô tả. Không có trường nào chứa dòng dữ liệu — điều này **đã đúng như vậy từ hệ thống hiện tại**, không phải chúng tôi mới thêm ràng buộc |
| *"Nếu AI đề xuất sai thì sao?"* | Mọi đề xuất đều là **bản nháp**, phải qua BDA duyệt. Và mỗi dòng đều dẫn được về nguồn để kiểm |
| *"Bao giờ dùng được toàn công ty?"* | Chưa hứa. Chạy thử 2–3 miền trước, đo bằng bốn chỉ số ở mục 9, rồi mới quyết |
| *"Sao không mua sản phẩm có sẵn?"* | Sản phẩm thị trường dựa nhiều vào việc AI đọc dữ liệu mẫu — thứ chúng ta cấm. Và họ không có sẵn kết nối tới hệ thống job của mình |
| *"Chi phí AI?"* | Dùng lại kênh AI nội bộ **đã đầu tư và đang chạy** cho tính năng tối ưu câu lệnh. Không phát sinh hạ tầng mới |
| *"Nếu metadata bẩn thì AI nói bậy?"* | **Đúng, và chúng tôi thừa nhận.** Đó chính là lý do chạy thử có phạm vi, và lý do mục 7 nêu rõ hiện trạng thay vì che đi |

---

*Lập ngày 13/08/2026. Các con số hiện trạng lấy từ khảo sát hệ thống; các mô tả về hệ thống hiện tại được đối chiếu trực tiếp với mã nguồn.*
