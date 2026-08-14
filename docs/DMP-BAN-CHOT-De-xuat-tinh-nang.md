# DMP — Đề xuất tính năng (BẢN CHỐT)

> **Ngày:** 13/08/2026 · **Người lập:** Khôi (BA)
>
> **File này thay thế toàn bộ các file đề xuất trước.** 48 tính năng, có đánh sao theo mức độ ưu tiên. Các file cũ giữ lại làm tư liệu tham chiếu, không dùng để trình bày.

**Cách đọc mức sao**

| Mức | Nghĩa |
|:---:|---|
| ⭐⭐⭐ | **Nên đưa vào báo cáo.** Giá trị rõ ràng, đo được, hoặc là điều kiện bắt buộc cho các tính năng khác |
| ⭐⭐ | Giá trị rõ, làm ở giai đoạn sau |
| ⭐ | Nên có, chưa gấp |

---

## 1. Tóm tắt cho lãnh đạo

**Hiện trạng đo được**

| Chỉ số | Con số |
|---|---|
| Tổng số bảng dữ liệu | 11.482 |
| Bảng có luật kiểm chất lượng | 64 — **0,6%** |
| Bảng chưa có người phụ trách | 7.578 — **66%** |
| Bảng chưa gán miền nghiệp vụ | 4.334 — **38%** |
| Bảng có mô tả nghiệp vụ đủ nghĩa | **28%** |
| Job đang quản lý | 1.842 — trong đó **186 job** không chạy 90 ngày |
| Cột đã gắn nhãn dữ liệu nhạy cảm | 412 |
| Thời gian trung bình từ lúc nhận yêu cầu tới lúc bắt đầu viết SQL | **≈ 4 ngày** |

**Ba việc DMP giải quyết**

1. **Không ai chịu trách nhiệm cho dữ liệu.** 66% bảng không có đầu mối. Hỏng thì không biết báo ai.
2. **Phát hiện lỗi sau khi đã dùng số sai.** 0,6% bảng được kiểm chất lượng. Phần còn lại chỉ biết hỏng khi người dùng phản ánh.
3. **Mất quá nhiều thời gian cho việc tìm kiếm.** Trước khi làm được một yêu cầu dữ liệu, BDA mất khoảng 4 ngày chỉ để xác định dùng bảng nào.

**Điểm cần nói rõ về AI**

SQLWF **đã có một hệ thống AI đang chạy** — module tối ưu câu lệnh SQL (`services/tuning`), giao tiếp qua RabbitMQ, có quy trình *AI đề xuất → người duyệt → áp dụng*. Các đề xuất AI trong tài liệu này **mở rộng hệ thống đã có**, không xây mới.

Và toàn bộ đề xuất tuân thủ một ràng buộc: **AI chỉ đọc siêu dữ liệu (metadata) và mã lệnh SQL. Không đọc nội dung dữ liệu.**

---

## 2. Nguyên tắc an toàn dữ liệu

Phần này cần chốt trước, vì mọi tính năng AI đều bị nó chi phối.

### Bốn loại thông tin

| | Loại | Ví dụ | Được gửi cho AI? |
|---|---|---|---|
| **A** | **Nội dung dữ liệu** | Giá trị trong ô: tên khách hàng, số điện thoại, số dư | ❌ **Không, không có ngoại lệ.** Kể cả lấy mẫu vài dòng |
| **B** | **Chỉ số thống kê** | Số dòng, tỷ lệ giá trị rỗng, thời điểm nạp | ✅ Được — nhưng phần lớn tính năng dùng loại này **không cần AI** |
| **C** | **Siêu dữ liệu (metadata)** | Tên bảng, tên cột, mô tả nghiệp vụ, nhãn phân loại, đầu mối | ⚠️ Được, **chỉ với AI nội bộ** |
| **D** | **Mã lệnh** | Câu SQL, cấu hình job, sơ đồ luồng xử lý | ⚠️ Được, **chỉ với AI nội bộ** — đây là thứ module tuning đang gửi hiện nay |

### Bốn quy tắc

1. AI đọc **cách dữ liệu được tạo ra** (mã lệnh, luồng xử lý, mô tả), **không đọc nội dung dữ liệu**.
2. Loại **C** và **D** chỉ gửi tới **AI trong mạng nội bộ**. Không dùng dịch vụ AI công cộng, không dùng API key cá nhân.
3. Mọi đề xuất của AI phải **qua người duyệt** mới có hiệu lực.
4. Mỗi lần gọi AI phải **ghi nhật ký**: ai gọi, khi nào, gửi gì, nhận gì.

> Quy tắc 1–3 hệ thống tuning hiện tại **đã tuân thủ**. Quy tắc 4 cần bổ sung — xem tính năng **47**.

### Ba việc cam kết không làm

| Không làm | Lý do |
|---|---|
| AI đọc dữ liệu mẫu để tự sinh mô tả cột hoặc tự đoán cột nhạy cảm | Vi phạm quy tắc 1. **Đây là tính năng phổ biến nhất của các sản phẩm trên thị trường — ta cố tình không làm** |
| Đưa nguyên văn tài liệu nội bộ (quy định, hợp đồng) cho AI xử lý | Tài liệu bị gửi ra ngoài phạm vi kiểm soát, và kết quả **không truy vết được tới điều khoản cụ thể** khi kiểm toán yêu cầu. Thay bằng tính năng **46** |
| AI tự sửa job, tự chạy, tự cấp quyền | Job sai chạy trên dữ liệu thật là sự cố thật |

> Khi so sánh với sản phẩm thị trường, nên chủ động nêu việc bỏ tính năng sinh mô tả tự động từ dữ liệu mẫu. Nêu trước thì đó là lựa chọn có chủ đích; để người khác phát hiện thì thành thiếu sót.

---

## 3. Danh mục 48 tính năng

<details open>
<summary><b>Nhóm I — Chất lượng và giám sát dữ liệu</b></summary>

| # | Tính năng | Giá trị | SQLWF hiện có | |
|:---:|---|---|---|:---:|
| 1 | **Tự thiết lập ngưỡng cảnh báo từ dữ liệu lịch sử** | Đưa tỷ lệ bảng được giám sát từ **0,6% lên gần 100%** mà không ai phải khai luật | ❌ `data-quality` chỉ bật/tắt luật khai tay | ⭐⭐⭐ |
| 2 | **Cảnh báo thay đổi cấu trúc bảng** | Thêm/xoá/đổi kiểu cột là nguyên nhân hàng đầu gây sai số ngầm — job vẫn chạy nhưng kết quả sai | ⚠️ `history-data` có ghi nhật ký thay đổi, chưa sinh cảnh báo | ⭐⭐ |
| 3 | **Gộp sự cố theo nguyên nhân gốc** | Một bảng nguồn hỏng sinh ra hàng chục phiếu rời rạc; người xử lý không biết chỉ cần sửa một chỗ | ❌ `warning-history` có duyệt từng phiếu, không gộp | ⭐⭐ |
| 4 | **Truyền cảnh báo theo luồng dữ liệu** | Người đọc báo cáo không biết số của mình bắt nguồn từ bảng đang lỗi | ❌ | ⭐⭐ |
| 5 | **Thoả thuận mức dịch vụ dữ liệu (data contract)** | Chuyển từ phát hiện lỗi sau sang thống nhất yêu cầu trước | ⚠️ Có cấu hình chu kỳ, chưa có thoả thuận hai bên | ⭐ |
| 6 | **Cam kết chất lượng theo từng bảng** | Bản rút gọn của mục 5, áp cho bảng quan trọng | ⚠️ Có cấu hình chất lượng, chưa có ràng buộc | ⭐ |

</details>

<details open>
<summary><b>Nhóm II — Vận hành job và hạ tầng</b></summary>

| # | Tính năng | Giá trị | SQLWF hiện có | |
|:---:|---|---|---|:---:|
| 7 | **Cấp thêm ngữ cảnh cho module AI tuning** | AI đang tối ưu SQL **mà chỉ nhìn thấy câu lệnh** — không biết bảng lớn nhỏ, chạy bao lâu, ai đang dùng. Bổ sung ngữ cảnh thì chất lượng đề xuất tăng ngay | ✅ **Đã có module tuning hoàn chỉnh** | ⭐⭐⭐ |
| 8 | **Dự báo job sắp lỗi do hết bộ nhớ** | Kiểu lỗi này dự báo được: dữ liệu tăng dần, thời gian chạy dài dần | ❌ Có theo dõi tài nguyên, chưa dự báo | ⭐⭐ |
| 9 | **Ước lượng chi phí trước khi phê duyệt job** | Người duyệt cần biết job này tiêu tốn gấp mấy lần trung bình **tại thời điểm duyệt** | ❌ | ⭐⭐ |
| 10 | **Phát hiện job tính toán trùng nhau** | 1.842 job tích luỹ nhiều năm, chắc chắn có nhóm cùng tính một chỉ tiêu | ❌ | ⭐ |
| 11 | **Rà soát job và bảng không còn được sử dụng** | 186 job không chạy 90 ngày vẫn chiếm tài nguyên và vẫn cập nhật bảng không ai đọc | ⚠️ Có dữ liệu rời rạc, chưa tổng hợp | ⭐⭐ |
| 12 | **Khôi phục bảng về thời điểm trước** | Job ghi sai thì quay bảng về bản trước, không phải chạy lại từ đầu | ⚠️ Nền tảng lưu trữ có hỗ trợ, chưa có giao diện | ⭐⭐ |
| 13 | **So sánh hai lần chạy để giải thích chênh lệch** | Câu hỏi phổ biến nhất từ người dùng: *"sao hôm nay khác hôm qua"* | ❌ | ⭐⭐ |
| 14 | **Chạy thử trước khi đưa lên môi trường thật** | Job mới cần chạy thử trên môi trường tách biệt | ✅ **Đã có chế độ chạy thử** (`updateTestMode`) | ⭐ |

</details>

<details open>
<summary><b>Nhóm III — Metadata và tự động hoá khai báo</b></summary>

| # | Tính năng | Giá trị | SQLWF hiện có | |
|:---:|---|---|---|:---:|
| 15 | **Tự phát hiện cột chứa dữ liệu nhạy cảm** | 412 cột đang gắn nhãn thủ công trên tổng số cột của 11.482 bảng — chắc chắn còn sót. Cột tên `ma_kh_02` chứa số căn cước thì nhìn tên không ai đoán ra | ⚠️ Có cơ chế gắn nhãn, chưa có phát hiện tự động | ⭐⭐ |
| 16 | **Máy soạn mô tả nghiệp vụ, người duyệt** | 8.267 bảng thiếu mô tả (72%). Gõ tay sẽ không bao giờ hoàn thành | ❌ | ⭐⭐ |
| 17 | **Sửa thông tin hàng loạt** | Gán miền cho 4.334 bảng, mỗi bảng 30 giây là **36 ngày công**. Không ai bắt đầu, không phải vì lười mà vì cách làm bất khả thi | ⚠️ Có nạp file ở `import-data`, **không có màn sửa hàng loạt** | ⭐⭐⭐ |
| 18 | **Sinh luật chất lượng từ mô tả bằng tiếng Việt** | Người khai không cần học cú pháp luật | ❌ | ⭐ |
| 19 | **Gợi ý tên chuẩn khi khai báo** | Hiện chỉ kiểm tra và chặn; gợi ý tên đúng mới là hỗ trợ | ❌ | ⭐ |
| 20 | **Xuất/nhập cấu hình giữa các môi trường** | Khai ở môi trường thử rồi chuyển sang thật, không khai lại | ⚠️ Có quản lý cấu hình, chưa có xuất/nhập | ⭐ |
| **48** | ⭐ **Suy ra vai trò của cột từ câu lệnh job** *(mới)* | Xem [mục 4.9](#49--48--suy-ra-vai-trò-của-cột-từ-câu-lệnh-job) — **nhóm metadata đang thiếu 100% nhưng lấp được bằng máy** | ❌ Hệ thống chưa có khái niệm vai trò cột | ⭐⭐⭐ |

</details>

<details open>
<summary><b>Nhóm IV — Tra cứu và hỗ trợ người dùng</b></summary>

| # | Tính năng | Giá trị | SQLWF hiện có | |
|:---:|---|---|---|:---:|
| 21 | **Trang tra cứu bảng tổng hợp + hỏi đáp** | Câu hỏi phổ biến nhất trên nhóm chat: *"bảng này nghiệp vụ là gì, job nào sinh ra, tin được không"*. Hiện phải mở 6 màn mới trả lời được | ❌ Không có trang tra cứu tổng hợp | ⭐⭐⭐ |
| 22 | **Hỏi đáp và nhận cảnh báo qua Telegram** | Người dùng không mở công cụ cả ngày | ✅ **Đã có module `telegram` đang chạy** | ⭐⭐ |
| 23 | **Tìm kiếm bằng ngôn ngữ tự nhiên** | Người nghiệp vụ không biết tên bảng — đó chính là lý do họ đi hỏi | ❌ **Không có màn tìm kiếm nào** trong 67 màn hiện tại | ⭐⭐ |
| 24 | **Bản tóm tắt định kỳ cho lãnh đạo** | Bảng số không giải thích được *"điểm tăng do thêm bảng dễ, không phải cải thiện thật"* | ⚠️ Có báo cáo dạng bảng | ⭐ |
| 25 | **Trợ lý viết job có ngữ cảnh** | Cảnh báo ngay khi soạn: *"bảng này đang có sự cố, cân nhắc dùng bảng khác"* | ⚠️ AI tuning **sửa** SQL có sẵn, chưa **gợi ý lúc soạn** | ⭐⭐ |
| ~~26~~ | ~~AI đọc văn bản quy định~~ | **Đã thay bằng mục 46** — lý do ở đó | — | — |
| 27 | **Mở kho metadata cho công cụ lập trình** | Đội phát triển đang dùng trợ lý lập trình; cho nó đọc metadata ngay lúc viết mã | ❌ | ⭐ |
| 28 | **Mô phỏng tác động trước khi thay đổi** | Biết cụ thể hỏng ở bước nào, không chỉ biết cái gì liên quan | ⚠️ `data-linage` có truy vết mở rộng | ⭐⭐ |

</details>

<details open>
<summary><b>Nhóm V — Quy trình làm việc</b></summary>

| # | Tính năng | Giá trị | SQLWF hiện có | |
|:---:|---|---|---|:---:|
| 29 | **Hộp thư việc cần xử lý tập trung** | Công việc đang nằm rải ở **6 hàng chờ khác nhau** — phải mở 6 menu mới biết mình có bao nhiêu việc | ❌ Có duyệt ở từng màn riêng, không có nơi tổng hợp | ⭐⭐⭐ |
| 30 | **Cổng tiếp nhận yêu cầu dữ liệu** | Yêu cầu *"tôi cần số X"* đang đi qua chat, không để lại dấu vết, không đo được | ❌ | ⭐⭐ |
| 31 | **Chuyển giao trách nhiệm hàng loạt** | Một người phụ trách 148 bảng; nghỉ phép là cảnh báo không tới ai | ❌ | ⭐⭐ |
| 32 | **Cảnh báo khi thay đổi định nghĩa nghiệp vụ** | Đổi ý nghĩa nguy hiểm hơn đổi kiểu dữ liệu — mọi thứ vẫn chạy nhưng số bị hiểu sai | ❌ | ⭐ |
| 33 | **Hướng dẫn tại chỗ cho người mới** | 27 menu, người mới không biết bắt đầu từ đâu | ❌ | ⭐ |

</details>

<details open>
<summary><b>Nhóm VI — Phục vụ người dùng cuối</b></summary>

| # | Tính năng | Giá trị | SQLWF hiện có | |
|:---:|---|---|---|:---:|
| 34 | **Đăng ký theo dõi bảng và báo cáo** | **Lỗ hổng lớn nhất hiện nay:** cảnh báo chỉ gửi cho đầu mối kỹ thuật. Người dùng số liệu — chính là người chịu hậu quả — không nhận được gì. Xem [mục 4.5](#45--34--đăng-ký-theo-dõi-bảng-và-báo-cáo) | ❌ Chỉ có nhóm nhận email theo cấu hình sẵn | ⭐⭐⭐ |
| 35 | **Nhãn độ tin cậy đi kèm số liệu** | Có số rồi nhưng không biết có tin được không | ❌ | ⭐⭐ |
| 36 | **Theo dõi tiến độ yêu cầu** | Gửi xong mất dấu, không biết đang chờ ai | ❌ | ⭐⭐ |
| 37 | **Báo vấn đề ngay tại chỗ xem số** | Người dùng thường là người đầu tiên phát hiện số sai. Luật chất lượng không bắt được loại lỗi *"đúng định dạng nhưng vô lý về nghiệp vụ"* | ❌ | ⭐⭐ |
| 38 | **Hiển thị ai khác đang dùng bảng này** | Đầu mối đang là nút thắt vì là cửa duy nhất để hỏi | ⚠️ Có lịch sử truy vấn, chưa hiển thị ở màn bảng | ⭐ |
| 39 | **Trang chủ theo vai trò** | Năm nhóm vai trò, nhu cầu khác nhau | ⚠️ Có phân quyền menu, chưa có trang chủ riêng | ⭐ |

</details>

<details open>
<summary><b>Nhóm VII — Quản trị và điều hành</b></summary>

| # | Tính năng | Giá trị | SQLWF hiện có | |
|:---:|---|---|---|:---:|
| 40 | **Bảng điều khiển đo hiệu quả quy trình** | DMP đo chất lượng dữ liệu rất kỹ nhưng chưa ai đo chính quy trình của DMP. Dữ liệu để đo thì hệ thống đã tự sinh ra hằng ngày | ❌ | ⭐⭐ |
| 41 | **So sánh giữa các miền và giao chỉ tiêu** | Giao *"nâng điểm lên 90"* mà không ai biết bắt đầu từ đâu | ⚠️ Có phân miền, chưa có chỉ tiêu | ⭐ |
| 42 | **Bản tin ba rủi ro lớn nhất trong tuần** | Lãnh đạo không có thời gian đọc mười chỉ số ngang hàng | ❌ | ⭐ |
| 43 | **Đo mức độ sử dụng chính công cụ** | Menu nào không ai mở suốt 3 tháng thì nên bỏ, đừng bảo trì | ⚠️ Có nhật ký truy cập, chưa dùng để đo | ⭐ |

</details>

<details open>
<summary><b>Nhóm VIII — Ứng dụng AI vào luồng yêu cầu dữ liệu</b></summary>

| # | Tính năng | Giá trị | SQLWF hiện có | |
|:---:|---|---|---|:---:|
| 44 | **Đồng bộ yêu cầu từ Jira và đề xuất phương án xử lý** | BDA mất **4 ngày** xác định dùng bảng nào trước khi viết dòng SQL đầu tiên. Xem [mục 4.1](#41--44--đồng-bộ-yêu-cầu-từ-jira-và-đề-xuất-phương-án-xử-lý) | ❌ Không có kết nối Jira | ⭐⭐⭐ |
| 45 | **Sinh khung định nghĩa báo cáo cho Tableau / VDSD** | Dựng báo cáo phần lớn là thao tác lặp lại. Chỉ sinh **định nghĩa**, không truy vấn dữ liệu, không tự xuất bản | ❌ | ⭐⭐ |
| 46 | **Danh mục văn bản quy định và đối chiếu tuân thủ** | Thay cho phương án đưa file PDF cho AI đọc. Xem [mục 4.7](#47--46--danh-mục-văn-bản-quy-định-và-đối-chiếu-tuân-thủ) | ❌ | ⭐⭐ |
| 47 | **Nhật ký gọi AI** | Đã có hệ thống AI chạy thật mà chưa có màn tra cứu ai gọi gì, gửi gì. **Điều kiện bắt buộc trước khi mở rộng AI** | ⚠️ Gói tin gửi AI **đã mang `username` và `ip`**, log đã lưu — thiếu màn tra cứu | ⭐⭐⭐ |

</details>

### Phân bố

| | Số lượng |
|---|:---:|
| ⭐⭐⭐ **Nên đưa vào báo cáo** | **9** |
| ⭐⭐ | 20 |
| ⭐ | 18 |
| Đã có sẵn, dùng lại được | 3 *(7 · 14 · 22)* |
| Có một phần, cần mở rộng | 17 |
| Chưa có | 27 |

---

## 4. Chi tiết chín tính năng ⭐⭐⭐

### 4.1 — **44** · Đồng bộ yêu cầu từ Jira và đề xuất phương án xử lý
**Vấn đề.** Chị Phương nhận yêu cầu trên Jira: *"Báo cáo doanh thu theo chi nhánh, theo tháng, tách theo nhóm sản phẩm, so sánh cùng kỳ năm trước."*

Bốn ngày tiếp theo chị làm việc này, lặp lại y hệt với mọi yêu cầu:

| Ngày | Nội dung |
|---|---|
| 1–2 | Xác định doanh thu nằm ở bảng nào. Hỏi trên nhóm chat, chờ người rảnh trả lời |
| 2 (chiều) | Tìm ra 3–4 bảng tên gần giống nhau, không rõ bảng nào là bản chính thức |
| 3 (sáng) | Tìm xem đã có ai làm yêu cầu tương tự chưa — thường là có, nhưng phải hỏi vài người mới lần ra |
| 3–4 | Kiểm tra bảng có còn nạp đều không, chất lượng ra sao |
| 5 | **Mới bắt đầu viết SQL** |

Và nếu là người mới, khả năng cao chọn nhầm bảng `bi.kh_360_revenue` — tên rất khớp, mở ra vẫn thấy dữ liệu cũ — mà không biết **job sinh ra nó đã dừng từ 12/03/2026**.

**Tính năng.** Hệ thống đọc yêu cầu từ Jira, đối chiếu với danh mục bảng, luồng dữ liệu, điểm chất lượng và các yêu cầu cũ, rồi dựng **bản phân tích sơ bộ**:

| Phần | Nội dung |
|---|---|
| ① Nguồn dữ liệu đề xuất | Bảng nào, vì sao chọn, điểm chất lượng, có gạch ngang bảng không dùng được |
| ② Cách liên kết | Nối bảng nào với bảng nào qua cột gì; cảnh báo khi hai bảng dùng hai bộ mã khác nhau |
| ③ Cách tính | Nhóm theo cột nào, tính chỉ tiêu gì, so sánh cùng kỳ thế nào |
| ④ Yêu cầu tương tự đã xử lý | Kèm câu lệnh cũ và thời gian thực hiện thực tế |
| ⑤ Rào cản cần biết trước | Dữ liệu chỉ lưu 18 tháng · cột gắn nhãn nhạy cảm cần duyệt khi phát hành |
| ⑥ Đầu ra dự kiến | Tên bảng kết quả và danh sách trường |

**AI nhìn thấy gì.** Mô tả yêu cầu, danh sách bảng ứng viên, mô tả bảng, sơ đồ luồng. **Không có dòng dữ liệu nào.**

**Giá trị.** 4 ngày rút xuống nửa ngày kiểm tra lại.

Nhưng phần đáng giá nhất không phải tốc độ — là **dòng gạch ngang bảng đã ngừng nạp**. Nó ngăn một báo cáo sai đi ra tới cuộc họp.

**Điều kiện.** Chất lượng đề xuất phụ thuộc hoàn toàn vào chất lượng khai báo. Với 38% bảng chưa gán miền, đề xuất sẽ bỏ sót nhiều. **Phải chạy thử trên 2–3 miền đã khai tương đối đầy đủ trước**, không mở toàn công ty ngay.

> **Điểm nên nhấn mạnh khi báo cáo:** tính năng này thay đổi động lực khai báo metadata. Hiện nay khai xong không thấy gì thay đổi nên không ai khai. Khi tính năng này chạy, khai đầy đủ thì yêu cầu của chính mình được đề xuất nguồn tự động. Đây là cơ chế duy nhất tôi thấy có thể khiến 4.334 bảng chưa gán miền được khai — chỉ thị hành chính đã thử và không hiệu quả.

---

### 4.2 — **1** · Tự thiết lập ngưỡng cảnh báo từ dữ liệu lịch sử
**Vấn đề.** 11.482 bảng, chỉ 64 bảng có luật kiểm chất lượng — **0,6%**.

Nguyên nhân không phải người dùng lười. Để khai một luật, người khai phải **biết trước ngưỡng đúng là bao nhiêu** — mà chính đầu mối cũng không biết. Hỏi *"bảng này mỗi ngày về bao nhiêu dòng là bình thường"*, câu trả lời thật thường là *"cũng không rõ"*.

**Tính năng.** Hệ thống quan sát mỗi bảng trong 30 ngày, ghi lại **năm chỉ số** mỗi ngày: số dòng nạp thêm · thời điểm nạp xong · tỷ lệ giá trị rỗng từng cột · số lượng cột · trạng thái job nguồn.

Từ 30 dòng đó tính ra **khoảng giá trị thông thường**, ví dụ: *số dòng 2,7–3,1 triệu · nạp xong 08:05–08:25 · cột `sdt` rỗng 2,8–3,4% · 47 cột*.

Ngày nào lệch khỏi khoảng đó thì sinh cảnh báo.

**Năm nhóm tín hiệu theo dõi**

| Nhóm | Nội dung | Ví dụ cảnh báo |
|---|---|---|
| Độ mới | Hôm nay đã có dữ liệu chưa | *"9h30 chưa có dữ liệu ngày 13/08, thường 08:14 là xong"* |
| Khối lượng | Số dòng bất thường | *"Về 1,2 triệu dòng, thường 2,7–3,1 triệu. Hụt 58%"* |
| Cấu trúc | Thêm hoặc mất cột | *"Cột `ma_don_vi` biến mất"* |
| Phân bố | Tỷ lệ rỗng thay đổi đột ngột | *"Cột `sdt` rỗng 31%, thường 3%"* |
| Phụ thuộc | Bảng thượng nguồn có vấn đề | *"Bảng nguồn chưa về, bảng này sắp thiếu"* |

Nhóm cuối cảnh báo **trước khi** sự cố xảy ra; bốn nhóm còn lại cảnh báo sau.

**Cần nói rõ: tính năng này không dùng AI.** Toàn bộ phép tính là đếm, cộng, chia, so sánh. Kết quả lưu trong hai bảng của DMP (`dq_table_profile_daily` ghi nhật ký ngày, `dq_table_baseline` ghi khoảng thông thường). Có giao diện: một tab trong màn chi tiết bảng, hiển thị biểu đồ 30 ngày và cho phép chỉnh ngưỡng thủ công. **Không có thông tin nào gửi ra ngoài hệ thống.**

**Giá trị.** Tỷ lệ bảng được giám sát từ **0,6% lên gần 100%**, không ai phải khai luật.

**Ba giới hạn cần ghi vào tài liệu ngay từ đầu**

1. Cần 30 ngày mới có ngưỡng. Bảng mới tạo phải khai tay hoặc chờ.
2. Nếu 30 ngày đó bảng vốn đã lỗi thì hệ thống coi trạng thái lỗi là bình thường. **Cần nút chỉnh ngưỡng thủ công và bước đầu mối xác nhận lần đầu.**
3. Bảng có tính mùa vụ (cuối tháng, ngày lễ, chiến dịch) sẽ báo nhầm. Cần lịch loại trừ.

> Không ghi ba giới hạn này từ đầu thì tuần đầu vận hành sẽ có hàng loạt cảnh báo sai, người dùng mất tin, và tính năng bị bỏ.

---

### 4.3 — **17** · Sửa thông tin hàng loạt
**Vấn đề.** Mục tiêu *gán miền nghiệp vụ cho 4.334 bảng*. Với thao tác hiện tại — mở từng bảng, chọn miền, lưu — mỗi bảng 30 giây thì tổng cộng là **36 ngày công liên tục**.

Không ai bắt đầu. Không phải vì lười, mà vì **cách làm bất khả thi về mặt số học**, và ai cũng ngầm hiểu điều đó.

**Tính năng.** Màn danh sách cho phép: lọc theo điều kiện → chọn nhiều dòng → sửa cùng lúc một hoặc nhiều trường → xem trước thay đổi → xác nhận. Kèm nhật ký để hoàn tác.

Áp dụng cho: gán miền · gán đầu mối · gắn nhãn phân loại · gắn thẻ chủ đề.

**Giá trị.** 36 ngày công xuống còn vài giờ.

> **Đây là tính năng nền.** Không có nó thì mọi con số mục tiêu trong đề án đều là cam kết không thực hiện được. Nên xếp cùng nhóm ưu tiên với các tính năng chính, dù bản thân nó không hấp dẫn khi trình bày.

---

### 4.4 — **29** · Hộp thư việc cần xử lý tập trung
**Vấn đề.** Công việc chờ xử lý của một người đang nằm rải ở **sáu hàng chờ khác nhau**: duyệt job · duyệt cấp quyền · phiếu sự cố chất lượng · yêu cầu dữ liệu · đánh giá tuân thủ · rà soát trùng lặp.

Muốn biết hôm nay mình có bao nhiêu việc, phải mở sáu menu.

Hệ quả thực tế: việc bị bỏ quên không phải vì người xử lý không muốn làm, mà vì **họ không biết là có việc**.

**Tính năng.** Một màn tổng hợp mọi việc đang chờ chính người đang đăng nhập, xếp theo mức khẩn và thời gian chờ. Bấm vào là nhảy thẳng tới màn xử lý. Có bộ đếm hiển thị trên thanh menu.

**Giá trị.** Không xây gì mới — chỉ tổng hợp lại thứ đã có ở sáu chỗ. Công sức thấp, hiệu quả thấy ngay.

---

### 4.5 — **34** · Đăng ký theo dõi bảng và báo cáo
**Vấn đề — đây là lỗ hổng lớn nhất trong thiết kế hiện tại.**

> 6 giờ sáng, bảng `bi.doi_soat_giao_dich_A` gặp sự cố. Hệ thống gửi cảnh báo cho anh Hùng (kỹ thuật dữ liệu) và chị Phương (BDA). Hai người biết và đang xử lý.
>
> 9 giờ, chị Lan mở báo cáo doanh thu chuẩn bị cho cuộc họp. **Chị không nhận được cảnh báo nào**, vì chị không phải đầu mối — chị là **người sử dụng số liệu**.
>
> 14 giờ, chị trình bày số sai trong cuộc họp ban lãnh đạo.

**Cả hai bên đều làm đúng phần việc của mình, và kết quả vẫn là số sai đi vào cuộc họp.**

Nguyên nhân: cơ chế cảnh báo hiện nay gửi theo **quan hệ sở hữu kỹ thuật**, không gửi theo **quan hệ sử dụng**.

**Tính năng.** Người dùng bấm *Theo dõi* trên bất kỳ bảng hoặc báo cáo nào. Khi có sự cố ảnh hưởng tới thứ đang theo dõi — kể cả sự cố ở bảng thượng nguồn — họ nhận được thông báo, kèm câu tóm tắt *"số liệu bạn đang dùng có thể chưa chính xác, đang xử lý, dự kiến 11h"*.

**Giá trị.** Lấp đúng khoảng trống giữa người vận hành dữ liệu và người sử dụng dữ liệu. Chi phí thấp vì dùng lại cơ chế cảnh báo và luồng dữ liệu đã có.

---

### 4.6 — **21** · Trang tra cứu bảng tổng hợp và hỏi đáp
**Vấn đề.** Câu hỏi lặp đi lặp lại trên nhóm chat: *"bảng này nghiệp vụ là gì"* · *"job nào sinh ra nó"* · *"số này có tin được không"* · *"báo cáo nào đang dùng bảng này, tôi muốn sửa cột"*.

Mỗi câu tiêu tốn: người hỏi chờ nửa buổi tới một ngày, người trả lời bị cắt ngang 10–20 phút, và câu trả lời trôi mất — tuần sau người khác hỏi lại y hệt.

**Tính năng — hai bước.**

**Bước 1: trang tra cứu, chưa cần AI.** Sáu khối thông tin ghép từ dữ liệu đã có:

| Khối | Nội dung |
|---|---|
| Danh tính | Tên · miền · đầu mối · mô tả · phân loại bảo mật |
| Nguồn gốc | Job nào sinh ra, bước nào, lần chạy gần nhất, đọc từ bảng nào |
| Đang được dùng bởi | Job hạ nguồn · báo cáo · người truy vấn nhiều nhất |
| Tình trạng | Điểm chất lượng · luật đang áp · sự cố gần đây · lịch nạp |
| Cấu trúc | Danh sách cột · nhãn nhạy cảm · lịch sử thay đổi cấu trúc |
| Tài liệu liên quan | Hỏi đáp cũ · tài liệu · yêu cầu từng sử dụng bảng này |

Riêng bước này đã trả lời được khoảng 80% câu hỏi trên, và **đáng làm kể cả không bao giờ gắn AI**.

**Bước 2: ô hỏi đáp, dùng AI nội bộ.** AI trả lời **chỉ dựa trên nội dung trang đó**, mỗi câu kèm nguồn trích dẫn. Không dẫn được nguồn thì trả lời *"chưa có thông tin"*.

Điểm thiết kế quan trọng: khi thiếu thông tin, hệ thống **nói rõ là thiếu** và gửi nhắc cho đầu mối: *"có người hỏi về bảng của anh/chị, bổ sung mô tả giúp"*.

> Hiện nay không ai khai mô tả cho 11.482 bảng vì đó là việc trừu tượng, không có hạn, không ai đọc. Nhưng *"có người đang cần biết bảng này dùng làm gì"* là việc cụ thể, mất hai phút. Cùng một việc, đặt vào đúng thời điểm thì làm được.

---

### 4.7 — **46** · Danh mục văn bản quy định và đối chiếu tuân thủ
*(Xếp ⭐⭐ về mức ưu tiên nhưng đưa vào phần chi tiết, vì đây là câu trả lời cho một phương án đã được nêu ra.)*

**Bối cảnh.** Có ý kiến đề xuất: đưa file PDF văn bản quy định nội bộ lên, để AI đọc rồi tự đề xuất chính sách bảo vệ dữ liệu.

**Hai rủi ro của phương án đó**

| Rủi ro | Nội dung |
|---|---|
| Phạm vi kiểm soát | Quy chế bảo mật, phân cấp phê duyệt, danh mục dữ liệu mật là tài liệu lưu hành nội bộ. Đưa lên dịch vụ AI công cộng là gửi ra ngoài phạm vi kiểm soát |
| **Không truy vết được** | Nghiêm trọng hơn. Nếu căn cứ áp chính sách là *"bản tóm tắt của AI"* thì khi kiểm toán hỏi *"căn cứ điều nào khoản nào"*, không trả lời được. Và bản tóm tắt lần sau sẽ khác lần này |

**Phương án đề xuất thay thế**

Ban Pháp chế hoặc bộ phận Quản trị dữ liệu đọc văn bản và khai vào danh mục có cấu trúc: **số hiệu văn bản · ngày ban hành · hiệu lực · điều khoản · nội dung yêu cầu · nhóm dữ liệu áp dụng**.

Hệ thống đối chiếu danh mục đó với thực tế và sinh phiếu vi phạm:

> *"Có 144 cột gắn nhãn PD_SENSITIVE, trong đó 31 cột chưa áp chính sách che — không phù hợp Điều 7 khoản 2 Quy định 123/QĐ-VDS."*

Khai một văn bản mất khoảng nửa ngày, làm một lần. Đổi lại ba điểm:

1. **Truy vết được tới điều khoản** — trả lời được kiểm toán, có tên người khai và ngày khai
2. **Văn bản không ra khỏi hệ thống nội bộ** — AI chỉ đọc dòng đã khai
3. **Đối chiếu liên tục** — cột mới gắn nhãn là kiểm ngay, không chờ ai đưa lại tài liệu

> Kết luận không phải *"không được đưa PDF lên"*, mà *"đưa PDF lên là phương án kém hơn"* — kể cả khi quy định bảo mật cho phép.

---

### 4.8 — **47** · Nhật ký gọi AI
**Vấn đề.** Team BDA đã tự phát triển một tiện ích Chrome để hỏi AI về job SQL. Công cụ được làm tốt: phần đối chiếu ngữ nghĩa chạy cục bộ trên máy, không gửi đi đâu.

Nhưng bước cuối — gọi AI trả lời — kết nối trực tiếp tới dịch vụ AI công cộng **bằng API key cá nhân của từng người**.

Nghĩa là câu lệnh SQL nội bộ đang được gửi ra ngoài hằng ngày, bằng tài khoản cá nhân, **không có ghi nhận tập trung**.

**Tính năng.** Một màn tra cứu, mỗi lần gọi AI ghi một dòng: ai gọi · khi nào · từ địa chỉ nào · loại yêu cầu · đã gửi loại thông tin gì · đối tượng là job/bảng nào · kết quả · người dùng có áp dụng đề xuất không.

Kèm quy tắc vận hành: **không ghi được nhật ký thì không cho gọi.**

**Hiện trạng.** Đã có sẵn một nửa — gói tin gửi sang AI đã mang `requestId`, `username`, `ip`, và log đã lưu trên Mongo. Thiếu màn tra cứu và báo cáo tổng hợp.

**Vì sao xếp ⭐⭐⭐.** Đây là tính năng chi phí thấp nhất trong toàn bộ danh mục, nhưng là **điều kiện bắt buộc để mở rộng AI**. Không có nó, mỗi đề xuất AI mới đều phải tranh luận lại từ đầu về bảo mật, và kết quả thường là quyết định cấm toàn bộ — mất luôn phần giá trị thật.

---

### 4.9 — **48** · Suy ra vai trò của cột từ câu lệnh job
**Vấn đề.** Muốn hệ thống đề xuất được cách tính cho một yêu cầu báo cáo (tính năng 44), nó phải biết **vai trò nghiệp vụ của từng cột**:

| Vai trò | Nghĩa | Ví dụ |
|---|---|---|
| **Chiều phân tích** | Cột dùng để nhóm dữ liệu | chi nhánh, nhóm sản phẩm |
| **Chỉ tiêu đo lường** | Cột dùng để tính toán | doanh thu, số lượng |
| **Trục thời gian** | Cột xác định kỳ báo cáo | tháng, ngày |
| **Khoá liên kết** | Cột dùng để nối bảng | mã khách hàng |

Hệ thống hiện **hoàn toàn chưa có khái niệm này** — 0%. Không có nó, mọi đề xuất về cách tính chỉ là đoán theo tên cột.

**Tính năng — và đây là điểm đáng chú ý nhất.**

Không cần ai khai tay. Hệ thống suy ra được từ **chính câu lệnh của 1.842 job đang chạy**:

| Cột xuất hiện ở vị trí nào trong câu lệnh | Suy ra vai trò |
|---|---|
| Trong mệnh đề `GROUP BY` | Chiều phân tích |
| Trong hàm `SUM` / `AVG` / `COUNT` | Chỉ tiêu đo lường |
| Kiểu ngày, dùng chia phân vùng | Trục thời gian |
| Trong điều kiện `JOIN ... ON` | Khoá liên kết |

Chạy một lần trên toàn bộ job thì phủ được phần lớn các bảng **đang thực sự được sử dụng** — đúng những bảng cần ưu tiên.

**Vì sao xếp ⭐⭐⭐**

1. Đây là nhóm metadata **thiếu 100%** mà **lấp được gần hết bằng máy**, không ai phải gõ tay.
2. Nó chỉ đọc **mã lệnh**, không đọc dữ liệu — tuân thủ đúng nguyên tắc an toàn đã đặt.
3. Nó là điều kiện để tính năng **44** hoạt động đúng.
4. Ngoài ra còn dùng được cho: gợi ý cột trong trình soạn SQL, phát hiện job tính trùng (mục 10), và xác định bảng nào là bảng phân tích chính.

---

## 5. Metadata cần có

Đây là điều kiện kỹ thuật để nhóm tính năng AI hoạt động. Sáu nhóm thông tin, kèm mức độ sẵn sàng hiện tại.

| Nhóm | Trường cần có | Trả lời câu hỏi | Hiện trạng |
|---|---|---|---|
| **A. Nhận diện** | Bảng: miền · mô tả nghiệp vụ · lớp dữ liệu · đầu mối · thẻ chủ đề. Cột: mô tả · đơn vị đo · nhãn nhạy cảm | *"Chỉ tiêu này nằm ở bảng nào?"* | 🟡 Miền 62% · Đầu mối 34% · Mô tả 28% |
| **B. Vai trò cột** | Chiều · chỉ tiêu · thời gian · khoá | *"Nhóm theo cột nào, tính chỉ tiêu gì?"* | 🔴 **0%** — nhưng lấp được bằng tính năng 48 |
| **C. Tình trạng** | Lịch nạp thông thường · điểm chất lượng · số sự cố · **độ sâu lịch sử (lưu bao nhiêu tháng)** | *"Bảng này tin được không?"* | 🔴 Chất lượng 0,6% · chưa có lịch nạp · **chưa có trường độ sâu lịch sử** |
| **D. Nguồn gốc** | Job sinh ra bảng · bảng đọc từ đâu · **đánh dấu bảng chính thức** · nhóm bảng trùng lặp | *"Ba bảng tên gần giống, dùng cái nào?"* | 🟡 Có cơ chế truy vết; **chưa đo được bao nhiêu % job bật ghi nhận luồng** |
| **E. Yêu cầu đã xử lý** | Mô tả yêu cầu cũ · bảng đã dùng · câu lệnh kết quả · **thời gian thực hiện thực tế** | *"Có phải làm lại từ đầu không?"* | 🔴 Đang ở Jira, chưa đồng bộ |
| **F. Quyền phát hành** | Nhãn nhạy cảm · chính sách che · phạm vi được phát hành | *"Báo cáo này gửi ra ngoài phòng ban được không?"* | 🟡 412 cột đã gắn nhãn, phạm vi phủ còn mỏng |

**Ba kết luận từ bảng này**

1. **Chưa thể triển khai toàn công ty ngay.** Nêu rõ điều này thì đáng tin hơn là hứa.
2. **Ba nhóm thiếu nhất (B, C, E) đều bù được bằng máy**, không cần người khai: B từ câu lệnh job (tính năng 48) · C từ quan sát 30 ngày (tính năng 1) · E từ đồng bộ Jira (tính năng 44), và tự tích luỹ về sau.
3. **Đề nghị chạy thử phạm vi hẹp:** chọn 2–3 miền nghiệp vụ đã khai tương đối đầy đủ, hoàn thiện đủ sáu nhóm cho riêng miền đó, đo kết quả thật, rồi mới mở rộng.

---

## 6. Thứ tự triển khai

Nguyên tắc: **mỗi giai đoạn phải kết thúc bằng một kết quả người dùng dùng được ngay.** Không có giai đoạn nào chỉ làm hạ tầng.

| Giai đoạn | Nội dung | Kết quả |
|---|---|---|
| **1** | Sửa lỗi trình soạn SQL *(mục 7)* | Chưa tới một ngày công. BDA thấy hiệu quả ngay |
| **2** | **17** sửa hàng loạt · **1** ngưỡng tự động · **21** trang tra cứu · **48** suy vai trò cột | Giám sát từ 0,6% lên gần 100%. Khai báo bắt đầu đầy đủ. **Đây là giai đoạn quyết định** |
| **3** | **29** hộp thư việc · **34** đăng ký theo dõi · **47** nhật ký AI · **46** danh mục quy định | Việc không bị bỏ quên. Người dùng cuối được cảnh báo. Đủ điều kiện mở rộng AI |
| **4** | **44** đồng bộ Jira và đề xuất phương án · **45** khung báo cáo · **25** trợ lý viết job | Thời gian xử lý yêu cầu từ 4 ngày xuống dưới 1 ngày |

**Lưu ý khi trình bày:** không nên mở đầu bằng giai đoạn 4 dù đó là phần hấp dẫn nhất. Khi bị hỏi *"bao giờ có"*, câu trả lời trung thực là *"sau khi hoàn thành giai đoạn 2"*. Nên trình bày theo đúng thứ tự, để giai đoạn 4 là đích đến chứ không phải cam kết về thời hạn.

---

## 7. Sửa lỗi trình soạn SQL

Không tính vào danh mục 48 vì đây là sửa lỗi sử dụng của SQLWF, không phải tính năng mới của DMP. Nhưng đề nghị làm trước tiên: chi phí rất thấp và BDA cảm nhận được ngay.

Toàn bộ phản hồi của BDA đã được đối chiếu với mã nguồn — **đều chính xác**.

| # | Việc | Nguyên nhân trong mã nguồn | Chi phí |
|:---:|---|---|---|
| a | **Chạy phần câu lệnh được bôi đen** | Sự kiện chạy SQL phát đi **không mang tham số**; hàm lấy câu lệnh trả về toàn bộ nội dung. Cả tệp không có chỗ nào gọi hàm lấy vùng chọn | Rất thấp |
| b | **Chú thích khối `Ctrl+Shift+/`** | Chưa đăng ký lệnh cho thao tác này | Rất thấp |
| c | **Bỏ tự động định dạng lại khi rời con trỏ** | Mỗi lần trình soạn mất tiêu điểm là toàn bộ SQL bị định dạng lại và nạp lại, làm mất cách trình bày của người viết và nhảy vị trí con trỏ | Rất thấp |
| d | **Cho khung soạn co giãn theo nội dung** | Đang cố định tối thiểu 100 dòng | Thấp |
| e | **Bật gợi ý cột ở mọi màn soạn thảo** | Cờ bật gợi ý cột mặc định tắt, **chỉ 1 màn bật**. Màn soạn bước job — nơi làm việc chính — **không nạp bộ gợi ý cột nào** | Thấp |
| f | **Gợi ý cột theo bí danh bảng** | Bộ nhận diện bảng chỉ khớp hai dạng cú pháp, **không phân tích mệnh đề `FROM ... AS c`** nên hệ thống không biết `c` là bảng nào. Và nó gộp cột của mọi bảng trong file vào một danh sách phẳng, không lọc theo ký tự đang gõ | Trung bình |
| g | **Ngăn lịch sử truy vấn ngay cạnh trình soạn** | Có ba màn lịch sử riêng biệt — phải rời khỏi màn đang soạn mới xem được | Trung bình |

**Việc a–e cộng lại chưa tới một ngày công.**

> Thông tin bổ sung: BDA đang phản ánh về màn **có** gợi ý cột. Màn soạn bước job — nơi họ làm việc nhiều nhất — **không có gợi ý cột nào cả**, và mọi người đã quen với việc đó.

---

## 8. Đề nghị và cách đo

### Đề nghị

| # | Nội dung | Cần ai quyết |
|:---:|---|---|
| 1 | Phê duyệt nguyên tắc *"AI đọc metadata và mã lệnh, không đọc nội dung dữ liệu"* | Lãnh đạo |
| 2 | Chọn 2–3 miền nghiệp vụ để triển khai thử | Lãnh đạo |
| 3 | Cho phép đọc yêu cầu từ Jira (chỉ đọc) | Đội quản trị Jira |
| 4 | Xác nhận hệ thống AI phía sau module tuning đặt ở đâu, ràng buộc dữ liệu thế nào | Đội hạ tầng |
| 5 | Mời team BDA tham gia từ đầu để tránh làm trùng | Trưởng nhóm BDA |
| 6 | Xác định đơn vị chịu trách nhiệm khai danh mục văn bản quy định | Lãnh đạo |

### Cách đo

| Chỉ số | Hiện tại | Mục tiêu sau triển khai thử |
|---|---|---|
| Thời gian từ nhận yêu cầu tới bắt đầu viết SQL | ≈ 4 ngày | ≤ 1 ngày |
| Tỷ lệ bảng có giám sát chất lượng | 0,6% | ≥ 80% trên miền thử |
| Tỷ lệ yêu cầu hệ thống đề xuất được nguồn dữ liệu | — | ≥ 70% trên miền thử |
| Tỷ lệ đề xuất bị BDA đánh dấu sai | — | ≤ 20% |
| **Số bảng được gán miền và mô tả trong kỳ** | Gần như không tăng | **Tăng rõ rệt** |

> Chỉ số cuối là chỉ số quan trọng nhất. Nếu nó không tăng, nghĩa là cơ chế tạo động lực khai báo chưa hình thành, và cần xem lại cách làm thay vì triển khai tiếp.

---

## 9. Câu hỏi có thể gặp

| Câu hỏi | Trả lời |
|---|---|
| *"AI có đọc được dữ liệu khách hàng không?"* | Không. Gói tin gửi sang AI chỉ có một trường nội dung, chứa câu lệnh và mô tả. Không có trường nào chứa dòng dữ liệu — **điều này đã đúng như vậy trong hệ thống hiện tại**, không phải ràng buộc mới thêm |
| *"AI đề xuất sai thì sao?"* | Mọi đề xuất là bản nháp, phải qua người duyệt. Mỗi mục đều dẫn được về nguồn để kiểm tra. Quy trình duyệt này **đã có sẵn và đang vận hành** cho module tuning |
| *"Bao giờ dùng được toàn công ty?"* | Chưa cam kết. Triển khai thử 2–3 miền trước, đo bằng năm chỉ số ở mục 8, rồi mới quyết |
| *"Sao không mua sản phẩm có sẵn?"* | Sản phẩm thị trường dựa nhiều vào việc AI đọc dữ liệu mẫu — thứ ta không cho phép. Và họ không có sẵn kết nối tới hệ thống job nội bộ |
| *"Chi phí AI?"* | Dùng lại hệ thống AI nội bộ đã đầu tư và đang vận hành cho module tuning. Không phát sinh hạ tầng mới |
| *"Metadata chưa đầy đủ thì AI đề xuất sai?"* | Đúng, và đây là lý do triển khai thử phạm vi hẹp. Mục 5 nêu rõ hiện trạng thay vì che đi |
| *"Đã có tool của team BDA rồi mà?"* | Công cụ đó chạy được, chứng minh nhu cầu có thật. Nhưng nó gửi câu lệnh nội bộ ra dịch vụ AI công cộng bằng tài khoản cá nhân, không có ghi nhận. Đưa lên hệ thống thì vừa kiểm soát được, vừa có thêm thông tin về chất lượng và đầu mối mà công cụ cá nhân không có |

---

## Phụ lục — Các file tư liệu

Giữ lại để tra cứu, **không dùng để trình bày**.

| File | Nội dung |
|---|---|
| [DMP-Kien-truc-CHOT.md](DMP-Kien-truc-CHOT.md) | Cấu trúc 27 menu |
| [DMP-Dac-ta-Chuc-nang-v1.md](DMP-Dac-ta-Chuc-nang-v1.md) | Đặc tả từng menu và tab |
| [DMP-Danh-muc-Tinh-nang-De-xuat.md](DMP-Danh-muc-Tinh-nang-De-xuat.md) | Bản dài của danh mục tính năng, có tình huống minh hoạ chi tiết |
| [DMP-AI-va-Lo-trinh-Nen-tang-Chuan.md](DMP-AI-va-Lo-trinh-Nen-tang-Chuan.md) | Phân tích an toàn AI và đối chiếu mã nguồn trình soạn SQL |
| [DMP-Tu-van-Bo-sung-tu-Thi-truong.md](DMP-Tu-van-Bo-sung-tu-Thi-truong.md) | Khảo sát công cụ thị trường |
| [DMP-Bai-trinh-bay-AI-cho-PYC.md](DMP-Bai-trinh-bay-AI-cho-PYC.md) | Bản trình bày riêng cho nhóm tính năng 44 |

---

*Lập ngày 13/08/2026. Các mô tả về hệ thống hiện tại được đối chiếu trực tiếp với mã nguồn SQLWF.*
