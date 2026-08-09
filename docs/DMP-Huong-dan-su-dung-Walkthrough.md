# DMP — Hướng dẫn sử dụng từ đầu (Walkthrough cho người dùng mới)

> **Đọc tài liệu này nếu bạn chưa từng dùng DMP.** Tài liệu đi từ "hệ thống này để làm gì"
> tới "tôi phải vào đâu, gõ cái gì, và sau khi gõ xong thì nó chạy đi đâu".
> Mọi ví dụ trong đây là dữ liệu thật đang có trong bản demo — mở song song
> `http://localhost:5173` và bấm theo là thấy đúng màn hình được mô tả.
>
> Liên quan: [Đề xuất tool DMP](DMP-De-xuat-tool-Data-Management.md) ·
> [Đối chiếu yêu cầu BDA](DMP-Review-Doi-chieu-Yeu-cau-BDA.md) ·
> [Rà soát logic & trùng lặp](DMP-Ra-soat-Logic-Luong-va-Trung-lap.md)

---

## Mục lục

- [Phần 0 — Ba phút để hiểu DMP là cái gì](#phần-0--ba-phút-để-hiểu-dmp-là-cái-gì)
- [Phần 1 — Bức tranh tổng thể: dữ liệu chảy qua hệ thống thế nào](#phần-1--bức-tranh-tổng-thể-dữ-liệu-chảy-qua-hệ-thống-thế-nào)
- [Phần 2 — Thứ tự khai báo: cái gì phải có trước cái gì](#phần-2--thứ-tự-khai-báo-cái-gì-phải-có-trước-cái-gì)
- [Phần 3 — Walkthrough: đi hết một vòng đời của một bảng dữ liệu](#phần-3--walkthrough-đi-hết-một-vòng-đời-của-một-bảng-dữ-liệu)
- [Phần 4 — Sáu cách một ô trên màn hình có giá trị](#phần-4--sáu-cách-một-ô-trên-màn-hình-có-giá-trị)
- [Phần 5 — Cái gì máy tự làm, cái gì người phải làm, và làm lúc nào](#phần-5--cái-gì-máy-tự-làm-cái-gì-người-phải-làm-và-làm-lúc-nào)
- [Phần 6 — Đi qua từng menu: 35 màn hình](#phần-6--đi-qua-từng-menu-35-màn-hình)
- [Phần 7 — Tự rà soát logic: 8 phép thử bạn tự làm được](#phần-7--tự-rà-soát-logic-8-phép-thử-bạn-tự-làm-được)
- [Phần 8 — Những chỗ demo khác thực tế](#phần-8--những-chỗ-demo-khác-thực-tế)

---

## Phần 0 — Ba phút để hiểu DMP là cái gì

### DMP không chứa dữ liệu

Đây là điều đầu tiên và hay bị hiểu nhầm nhất.

DMP **không lưu một dòng dữ liệu nghiệp vụ nào**. Doanh thu vẫn nằm ở kho DWH,
hồ sơ khách hàng vẫn nằm ở CRM. DMP chỉ lưu **thông tin về dữ liệu đó**: bảng này
tên gì, ai chịu trách nhiệm, chứa số điện thoại hay không, được sinh ra bởi job nào,
đang phục vụ báo cáo nào, chất lượng bao nhiêu điểm.

Nói cách khác: **DMP là cuốn sổ hộ khẩu của dữ liệu**, không phải là kho dữ liệu.

### DMP trả lời năm câu hỏi

Cả 35 menu đều tồn tại để trả lời đúng năm câu này:

| # | Câu hỏi | Ai hay hỏi | Module trả lời |
|---|---|---|---|
| 1 | **Dữ liệu tôi cần nằm ở đâu?** | Người phân tích | ① Data Catalog |
| 2 | **Con số này nghĩa là gì, tính thế nào?** | Lãnh đạo, kiểm toán | ② Governance |
| 3 | **Số này có tin được không?** | Người dùng báo cáo | ③ Data Quality |
| 4 | **Ai được xem cái gì, căn cứ nào?** | An ninh, kiểm toán | ⑤ Security · ⑥ Tuân thủ |
| 5 | **Số này từ đâu ra? Sửa bảng gốc thì hỏng cái gì?** | Kỹ thuật, quản trị | ② Truy vết · ④ Điều phối |

### Năm vai trò — bạn là ai trong đó

Mọi thứ trong DMP đều xoay quanh năm vai trò này (định nghĩa tại **GĐ1 mục 2.3**,
khai tại menu **5.1 Người dùng & Nhóm**). Đọc kỹ đoạn này, vì hầu hết các trường
"người phụ trách" trên toàn hệ thống đều chỉ cho chọn đúng một trong năm vai trò:

| Vai trò | Làm gì | Nhìn thấy vai trò này ở đâu |
|---|---|---|
| **Người sở hữu dữ liệu** | Phê duyệt định nghĩa, phê duyệt cấp quyền | Duyệt hồ sơ ở 2.4, duyệt xin quyền ở 5.3 |
| **Đầu mối nghiệp vụ (BDA)** | Viết mô tả, gắn thuật ngữ, định nghĩa quy tắc nghiệp vụ | Tự nhận **sự cố nghiệp vụ** ở 3.4 |
| **Đầu mối kỹ thuật (DE)** | Khai cấu trúc, job, kết nối | Tự nhận **sự cố kỹ thuật** ở 3.4 |
| **Đơn vị vận hành hệ thống** | Khai chuẩn đặt tên, Tier, tham số toàn cục | Menu 8.2 |
| **Người sử dụng dữ liệu** | Tra cứu, xin quyền | Menu 1.1, 5.3 |

> **Vì sao phải nhớ:** khi bạn khai một bảng và chọn "Đầu mối nghiệp vụ", danh sách
> xổ ra **không phải toàn bộ nhân viên công ty** — nó chỉ lọc ra người đang làm việc
> và **có vai trò Đầu mối nghiệp vụ**. Ai không được gán vai trò ở 5.1 thì không
> xuất hiện ở bất kỳ ô chọn người nào trên toàn hệ thống.

---

## Phần 1 — Bức tranh tổng thể: dữ liệu chảy qua hệ thống thế nào

### Một hình duy nhất bạn cần nhớ

```
   ┌── KHAI NỀN (làm một lần, ít thay đổi) ──────────────────────────┐
   │  8.2 Chuẩn đặt tên · Tier · tham số                             │
   │  5.1 Người dùng + vai trò                                       │
   │  1.7 Miền dữ liệu   1.8 Danh mục tham chiếu                     │
   └────────────────────────┬────────────────────────────────────────┘
                            ▼
   ┌── KHAI TÀI SẢN (mỗi khi có hệ thống/bảng mới) ──────────────────┐
   │  1.3 Hệ thống  ──►  1.2 BẢNG DỮ LIỆU  ◄──  1.4 Kênh trao đổi    │
   │                        ▲   ▲   ▲                                 │
   │            2.1 Thuật ngữ┘   │   └2.2 Nhãn nhạy cảm              │
   └────────────────────────┬───┴─────────────────────────────────────┘
                            ▼
   ┌── DỰNG LUỒNG (khai job, hệ thống tự dò) ────────────────────────┐
   │  4.2 Cửa nạp ──► 4.1 Job ──► bảng đích                          │
   │                    │                                             │
   │                    └──(tự phân tích SQL)──► 2.3 TRUY VẾT LUỒNG   │
   └────────────────────────┬────────────────────────────────────────┘
                            ▼
   ┌── ĐO VÀ CANH (chạy liên tục, không cần người bấm) ──────────────┐
   │  3.3 Phân tích ─► 3.2 Luật ─► điểm chất lượng ─► 3.4 Sự cố      │
   │                                                  └─► 3.5 Cảnh báo│
   └────────────────────────┬────────────────────────────────────────┘
                            ▼
   ┌── SỬ DỤNG VÀ KIỂM SOÁT ─────────────────────────────────────────┐
   │  1.5 Báo cáo & Chỉ tiêu    5.2/5.3 Quyền    6.x Tuân thủ        │
   │                     └──────────┬──────────┘                      │
   │                        8.1 SỨC KHOẺ DỮ LIỆU (bảng điểm)         │
   └─────────────────────────────────────────────────────────────────┘
```

### Nguyên tắc chi phối toàn hệ thống

Bốn nguyên tắc này giải thích **99% các câu hỏi "sao trường này lại thế"**:

**① Đo một nơi, hiện nhiều nơi.**
Ví dụ *Tỷ lệ rỗng* của một cột chỉ được **đo duy nhất một lần** ở menu 3.3 (Phân tích dữ liệu).
Nó hiện lại ở tab Cột của 1.2, ở gợi ý gán luật của 3.2, ở màn 8.1 — nhưng tất cả
chỉ là **đọc lại**, không ai sửa được ở đó. Bạn sẽ không bao giờ thấy hai chỗ trong DMP
cho hai con số khác nhau về cùng một thứ.

**② Mọi ô chọn đều có nơi quản lý.**
Không có dropdown nào được viết cứng trong màn hình. 32 danh sách giá trị của toàn hệ thống
đều liệt kê tại menu **2.5 → tab "Danh sách giá trị chọn"**, kèm cột *"Ai quản lý"* và
đường dẫn tới menu quản lý nó. Nếu một giá trị sai, bạn biết đích xác phải vào menu nào để sửa.

**③ Có ⓘ thì bấm vào.**
Bên cạnh nhãn của các trường quan trọng có dấu **ⓘ**. Rê chuột vào sẽ mở một khung
hai phần:
- **← Giá trị này từ đâu ra** — khai tay ở menu nào, hay máy tự tính bằng công thức gì
- **→ Khai xong thì dùng ở đâu (n)** — liệt kê đủ n màn hình sẽ nhận trường này làm đầu vào,
  và nhận để làm gì

Đây chính là công cụ để bạn tự rà soát logic mà không cần hỏi ai.

**④ Trường có ⭐ là trường "khai sai thì hỏng chỗ khác".**
Trong khung ⓘ, dòng nào có ⭐ nghĩa là trường này không chỉ để hiển thị — nó **điều khiển
hành vi** của một màn khác. Ví dụ *Chu kỳ cập nhật* của bảng có ⭐ vì nó là tham số
của luật "Độ tươi dữ liệu"; không khai chu kỳ thì luật kịp thời không sinh ra được.

---

## Phần 2 — Thứ tự khai báo: cái gì phải có trước cái gì

Đây là phần quan trọng nhất cho người triển khai. **Khai sai thứ tự thì bạn sẽ bị
kẹt ở giữa chừng** vì ô chọn không có giá trị nào để chọn.

### Bốn đợt khai báo

| Đợt | Menu | Ai làm | Vì sao phải làm trước | Bao lâu một lần |
|---|---|---|---|---|
| **Đợt 0**<br>Nền | 8.2 Cấu hình<br>5.1 Người dùng | Vận hành hệ thống | Chuẩn đặt tên là **cổng chặn** — chưa có thì không lưu được bảng nào.<br>Chưa có người + vai trò thì mọi ô "người phụ trách" đều rỗng | Một lần, sửa hiếm |
| **Đợt 1**<br>Khung phân loại | 1.7 Miền dữ liệu<br>1.8 Danh mục tham chiếu<br>2.1 Từ điển nghiệp vụ<br>2.2 Nhãn phân loại | Sở hữu dữ liệu + BDA | Đây là các **danh mục mà bảng sẽ trỏ tới**. Chưa có miền thì bảng không gán được miền, mà không có miền thì không ai chịu trách nhiệm | Một lần, bổ sung dần |
| **Đợt 2**<br>Tài sản | 1.3 Hệ thống<br>1.4 Kênh<br>1.2 **Bảng dữ liệu** | DE + BDA | Bảng là **trung tâm của cả hệ thống**. Nhưng bảng phải thuộc một hệ thống → khai 1.3 trước | Mỗi khi có hệ thống/bảng mới |
| **Đợt 3**<br>Luồng và đo | 4.2 Cửa nạp<br>4.1 Job<br>3.1→3.2 Luật<br>1.5 Báo cáo | DE + BDA | Job phải chọn được **bảng đích** → bảng phải có trước (ràng buộc **RB2**).<br>Luật phải gán vào bảng/cột → bảng phải có trước | Liên tục |

### Ba ràng buộc cứng — hệ thống sẽ chặn, không chỉ cảnh báo

| Mã | Ràng buộc | Bạn gặp nó ở đâu |
|---|---|---|
| **RB1** | Tên bảng **sai chuẩn đặt tên** khai ở 8.2 thì **không lưu được** | Nút Lưu ở 1.2 → Thêm bảng bị vô hiệu |
| **RB2** | Job **không chọn được bảng đích chưa có trong danh mục** | Ô "Bảng đích" ở 4.1 chỉ xổ ra bảng đã khai ở 1.2 |
| **RB3** | Bảng **Tier 1** thì **không tắt được** quét nguồn gốc | Công tắc ở 4.1 bị khoá khi bảng đích là Tier 1 |

> **Vì sao đặt ràng buộc kiểu này:** đây là cách duy nhất để danh mục không bị rỗng ruột.
> Nếu cho phép job trỏ tới bảng chưa khai, sau sáu tháng bạn sẽ có 4.000 bảng "ma"
> chạy trong pipeline mà không có trong sổ — và sơ đồ truy vết sẽ đứt.

---

## Phần 3 — Walkthrough: đi hết một vòng đời của một bảng dữ liệu

Phần này bạn **mở demo lên và bấm theo**. Ta sẽ đi theo một câu chuyện có thật:

> *Khối Tài chính cần một báo cáo doanh thu ngày. Bạn là Đầu mối nghiệp vụ,
> được giao "đưa bảng doanh thu vào quản trị".*

Ta sẽ đi hết 12 bước, từ lúc chưa có gì tới lúc báo cáo **BC-001 Báo cáo doanh thu ngày**
truy vết được về tận dữ liệu gốc.

---

### Bước 1 — Kiểm tra nền đã sẵn chưa

**Vào:** `8.2 Cấu hình hệ thống` → tab **Chuẩn đặt tên**

**Bạn nhìn thấy gì:** danh sách quy tắc CT-01, CT-02, CT-03 kèm biểu thức chuẩn
và ví dụ đúng. Ví dụ CT-01 quy định tên bảng phải có dạng `<vùng>.<tên_snake_case>`.

**Vì sao đứng ở đây trước:** vì lát nữa khi bạn gõ tên bảng, hệ thống sẽ đối chiếu
với đúng biểu thức này. Gõ `DoanhThuNgay` sẽ **bị chặn**, phải gõ `mart.doanh_thu_ngay`.

**Sang tab Kết nối nguồn:** đây là nơi khai đường dây kỹ thuật tới từng hệ thống.
Có kết nối thì hệ thống mới **tự đọc được** danh sách bảng, tên cột, kiểu dữ liệu,
số dòng — bạn không phải gõ tay. Kết nối `KN-05` đang lỗi xác thực nên các bảng
thuộc hệ thống đó sẽ không có số dòng.

---

### Bước 2 — Kiểm tra người đã có vai trò chưa

**Vào:** `5.1 Người dùng & Nhóm`

**Bạn làm gì:** tìm người sẽ làm Đầu mối nghiệp vụ cho bảng doanh thu. Xem cột **Vai trò**.

**Điểm cần hiểu:** cột **Tài khoản** và cột **Trạng thái nhân sự** là **DMP đọc về
từ hệ thống khác** (AD và hệ thống nhân sự), không tạo được ở đây. Cột **Vai trò**
mới là thứ bạn gán trong DMP.

**Hệ quả trực tiếp:** người chưa được gán vai trò *Đầu mối nghiệp vụ* sẽ **không
xuất hiện** trong ô chọn ở bước 5. Đây là chỗ người mới hay kẹt nhất.

---

### Bước 3 — Bảo đảm miền dữ liệu đã có

**Vào:** `1.7 Miền dữ liệu`

**Bạn nhìn thấy:** cây miền hai cấp, mỗi miền có một **người chịu trách nhiệm**.

**Vì sao quan trọng hơn vẻ ngoài:** miền dữ liệu không phải là cái nhãn trang trí.
Nó quyết định ba thứ:
1. **Ai chịu trách nhiệm** khi bảng có vấn đề (menu 8.1 → tab Theo miền dữ liệu)
2. **Cấp quyền theo cả miền** thay vì đi cấp từng bảng một (menu 5.2)
3. **Phạm vi áp quy tắc cảnh báo** (menu 3.5)

Ở màn 8.1 tab *Theo miền dữ liệu* bạn sẽ thấy dòng đỏ **"4.334 bảng chưa gán miền —
không ai chịu trách nhiệm"**. Đó chính là hậu quả của việc bỏ qua bước này.

---

### Bước 4 — Khai hệ thống chứa bảng

**Vào:** `1.3 Hệ thống & Nguồn dữ liệu` → nút **Thêm hệ thống**

**Bạn gõ tay:** Tên hệ thống · Mục đích sử dụng · Công nghệ nền tảng

**Bạn chọn từ danh mục:**
- *Đơn vị quản lý* → lấy từ **mô hình dữ liệu chủ Đơn vị tổ chức (menu 7.1)**,
  vốn được đồng bộ từ hệ thống nhân sự
- *Đầu mối kỹ thuật* và *Người sở hữu dữ liệu* → lấy từ **menu 5.1**, đã lọc theo vai trò

**Máy tự điền:**
- *Mã hệ thống* → tự sinh `HT-` + số thứ tự
- *Số bảng* → đếm ngược từ menu 1.2, ban đầu là 0
- *Độ hoàn thiện metadata* → tính bằng: số trường bắt buộc đã điền ÷ tổng số trường
  bắt buộc trong bộ tiêu chuẩn ở menu 2.5

**Trong demo:** hệ thống doanh thu đã có sẵn — `HT-03 Kho dữ liệu tập trung (DWH)`.

---

### Bước 5 — Khai bảng dữ liệu ⭐ (bước quan trọng nhất)

**Vào:** `1.2 Bảng dữ liệu` → nút **Thêm bảng**

Đây là màn có nhiều trường nhất, và cũng là màn mà mọi menu khác đều trỏ về.
Ta đi từng nhóm trường:

#### Nhóm ① — Định danh

| Trường | Từ đâu ra | Ghi chú |
|---|---|---|
| **Tên bảng** | Máy **tự đọc** từ lược đồ hệ thống nguồn qua kết nối ở 8.2 — hoặc gõ tay nếu chưa nối được | Bị kiểm theo chuẩn CT-01, **sai là không lưu được** |
| **Vùng lưu trữ** | Máy **tự tách** từ tiền tố của tên bảng | Gõ `mart.doanh_thu_ngay` thì vùng tự thành `mart` |
| **Hệ thống lưu trữ** | Chọn từ menu 1.3, **chỉ hệ thống đang sử dụng** | Hệ thống đã dừng không xổ ra |

#### Nhóm ② — Nghiệp vụ (bạn phải gõ)

| Trường | Khai xong dùng ở đâu |
|---|---|
| **Mô tả nghiệp vụ** | → vào chỉ mục tìm kiếm ở 1.1 · → tính chỉ số "Tỷ lệ có mô tả" ở 8.1 |
| **Miền dữ liệu** | → cấp quyền theo miền ở 5.2 · → bảng sức khoẻ theo miền ở 8.1 · → phạm vi cảnh báo ở 3.5 |
| **Chu kỳ cập nhật** ⭐ | → **là tham số của luật "Độ tươi dữ liệu"** ở 3.2. Không khai thì không sinh được luật kịp thời |

#### Nhóm ③ — Trách nhiệm

Ba ô người, ba vai trò khác nhau, **không được nhầm**:

| Trường | Chọn ai | Khai xong thì điều gì tự xảy ra |
|---|---|---|
| **Người sở hữu dữ liệu** | vai trò Người sở hữu dữ liệu | Hồ sơ metadata của bảng **tự vào hàng đợi duyệt** của người này ở 2.4 |
| **Đầu mối nghiệp vụ (BDA)** ⭐ | vai trò Đầu mối nghiệp vụ | Sự cố **nghiệp vụ** của bảng **tự gán** cho người này ở 3.4 |
| **Đầu mối kỹ thuật (DE)** | vai trò Đầu mối kỹ thuật | Sự cố **kỹ thuật** (độ tươi, cấu trúc, job hỏng) tự gán cho người này |

> **Hệ quả nếu bỏ trống:** sự cố sinh ra sẽ nằm ở trạng thái *Mới*, **không ai nhận**.
> Đây là lý do trường này để bắt buộc.

#### Nhóm ④ — Mức quan trọng và bảo mật

**Mức quan trọng (Tier)** không phải nhãn trang trí. Chọn Tier 1 thì:
- Số trường bắt buộc điền **tăng lên** ngay tại form này
- Ngưỡng chất lượng ở 3.2 **siết chặt hơn**
- Hạn xử lý sự cố ở 3.4 rút xuống **24 giờ** (Tier 2 là 72 giờ)
- Job ghi vào bảng này **không tắt được** quét nguồn gốc (RB3)

Tiêu chí phân Tier khai ở **8.2 → tab Định nghĩa mức quan trọng**.

**Mức phân loại** (Công khai · Nội bộ · Mật · Hạn chế truy cập) — đây là **trục
độc lập** với nhãn dữ liệu nhạy cảm ở bước 7. Đừng lẫn hai cái. Xem [Phần 4](#hai-trục-phân-loại--chỗ-dễ-nhầm-nhất).

#### Sau khi bấm Lưu

Bảng vào trạng thái **Dự thảo**. Nó **chưa có hiệu lực**. Xem bước 8.

---

### Bước 6 — Bổ sung ý nghĩa cho từng cột

**Vào:** `1.2` → mở bảng vừa tạo → tab **Cột**

**Máy đã tự điền sẵn** (đọc từ lược đồ qua kết nối ở 8.2): Tên cột · Kiểu dữ liệu

**Bạn bổ sung:**

| Trường | Từ đâu | Vì sao phải làm |
|---|---|---|
| **Mô tả cột** | Gõ tay | → vào chỉ mục tìm kiếm |
| **Thuật ngữ nghiệp vụ** | Chọn từ **menu 2.1**, chỉ thuật ngữ **Đã phê duyệt** | ⭐ Gõ tên thuật ngữ ở 1.1 sẽ ra được cột này. Đây là lý do duy nhất phải gắn |
| **Quy tắc nghiệp vụ** | Gõ tay | ⭐ Là **nguồn gợi ý tham số** khi gán luật ở 3.2 |
| **Tập giá trị hợp lệ** | Gõ tay, hoặc trỏ tới danh mục ở **menu 1.8** | ⭐ Là **tham số trực tiếp** của luật "Thuộc tập giá trị cho phép" |

> **Đây là chỗ thể hiện rõ nhất triết lý của DMP:** bạn không khai thông tin để cho đẹp.
> Mỗi trường bạn gõ ở đây sẽ **trở thành đầu vào** cho một luật kiểm tra chất lượng ở module ③.
> Khai kỹ ở đây = ít phải cấu hình luật thủ công về sau.

---

### Bước 7 — Gắn nhãn dữ liệu nhạy cảm

**Vào:** `2.2 Phân loại & Nhãn`

**Bạn nhìn thấy:** cây nhãn — `PD_BASIC` (dữ liệu cá nhân cơ bản), `PD_SENSITIVE`
(dữ liệu cá nhân nhạy cảm) và các nhãn con.

**Cách hoạt động:**
1. Bộ dò tự động quét tên cột và mẫu dữ liệu → **đề xuất** nhãn
2. Người có thẩm quyền **xác nhận** — máy không tự gắn
3. Nhãn được gắn vào cột

**Điều gì tự xảy ra ngay sau đó** — đây là điểm hay nhất của thiết kế:

```
Gắn nhãn PD_BASIC cho cột "so_dien_thoai"
   │
   ├─► Nhãn có sẵn "Kiểu che mặc định = Giữ 4 ký tự cuối"
   │      └─► 5.2 TỰ SINH chính sách che cho cột này
   │           (không phải vào khai từng cột một)
   │
   ├─► 1.2 cột "Số cột nhạy cảm" của bảng +1
   │
   ├─► Mức phân loại của bảng TỰ NÂNG lên nếu đang thấp hơn
   │
   └─► 8.1 chỉ số "Cột nhạy cảm đã có chính sách che" cập nhật
```

> **Nguyên tắc:** chính sách bảo mật ở 5.2 được viết **theo nhãn**, không viết theo
> tên cột. Gắn nhãn một lần → chính sách tự áp cho **mọi cột mang nhãn đó** trên
> toàn hệ thống, kể cả bảng khai sau này.

---

### Bước 8 — Đưa hồ sơ đi phê duyệt

**Vào:** `2.4 Phê duyệt & Phiên bản`

Bảng bạn khai ở bước 5 đang là **Dự thảo**. Vòng đời phê duyệt có 5 trạng thái
(theo **GĐ2 mục 8.1**):

```
Dự thảo ──gửi──► Chờ phê duyệt ──┬──duyệt──► Đã phê duyệt ──► Ngừng sử dụng
                                  └──trả về──► Yêu cầu chỉnh sửa ──┐
                                       ▲                            │
                                       └────────────────────────────┘
```

**Ai duyệt:** chính là **Người sở hữu dữ liệu** bạn chọn ở bước 5. Hệ thống tự
đưa hồ sơ vào hàng đợi của người đó — không cần ai chuyển tay.

**Cái gì bắt buộc qua duyệt, cái gì không:**

| Loại thay đổi | Có phải duyệt? |
|---|---|
| Metadata bảng, cột | Có |
| Định nghĩa thuật ngữ có **cờ CDE** | Có, cấp Người sở hữu dữ liệu |
| Quan hệ luồng dữ liệu **khai tay** | ⭐ **Có** |
| Quan hệ luồng dữ liệu **máy tự dò từ SQL** | **Không** — máy dò thì tin được |

---

### Bước 9 — Khai job sinh ra bảng

**Vào:** `4.1 Luồng xử lý (Job)` → **Thêm job**

**Bạn chọn:**
- *Bảng đích* → chỉ xổ ra bảng đã khai ở 1.2 (**ràng buộc RB2**)
- *Giờ cam kết* → job phải xong trước mấy giờ

**Bạn để nguyên (thường là bật):**
- *Bật quét nguồn gốc* → cho phép hệ thống **đọc câu SQL của job** để tự dựng luồng dữ liệu

**Máy tự làm — đây là phần tự động quan trọng nhất của cả hệ thống:**

Sau khi bạn lưu job, bộ phân tích SQL đọc từng bước của job, tìm tên bảng
trong mệnh đề `FROM` và `JOIN`, rồi **tự sinh ra**:

```
bảng nguồn  ──►  job  ──►  bảng đích
```

Bạn **không phải vẽ tay sơ đồ luồng dữ liệu**. Mở job `JOB-0412` trong demo,
tab *Sơ đồ bước xử lý* — 5 bước xử lý, bước 2 và 3 chạy song song rồi hội tụ ở bước 4,
bước 5 ghi vào bảng đích. Bấm vào từng nút để xem câu SQL của bước đó.

**Giới hạn thật của việc tự dò — cần biết để không bị bất ngờ:**

> Bảng tạm khai bằng `CREATE TEMP VIEW` thì **máy không dò được**. Những quan hệ đó
> phải khai tay ở menu 2.3, và vì khai tay nên **bắt buộc qua phê duyệt**.
> Trong demo, panel *"Bảng nguồn dò được"* ở màn chi tiết job hiển thị đúng
> những gì máy dò ra — nếu thiếu, bạn biết ngay là phải bổ sung tay.

---

### Bước 10 — Xem luồng dữ liệu đã dựng xong

**Vào:** `2.3 Truy vết luồng dữ liệu`

Bạn **không khai gì ở đây trong trường hợp thông thường** — màn này chủ yếu để **xem**.
Dữ liệu của nó được tổng hợp tự động từ ba nguồn:

| Nguồn quan hệ | Đến từ đâu | Cần duyệt? |
|---|---|---|
| Tự động — phân tích SQL | Job ở menu 4.1 | Không |
| Tự động — cấu hình cửa nạp | Mẫu nạp ở menu 4.2 | Không |
| Khai báo thủ công | Người dùng khai tại chính màn 2.3 | **Có** |

**Bốn mức xem** (theo **GĐ2 mục 5.7**) — cùng một dữ liệu, bốn cách nhìn:

| Mức | Trả lời câu hỏi | Ai xem |
|---|---|---|
| **Hệ thống** | Hệ thống nào cấp dữ liệu cho hệ thống nào | Kiến trúc |
| **Bảng** | Bảng nào sinh ra bảng nào | Kỹ thuật |
| **Cột** | Cột doanh thu này tính từ cột nào | Phân tích chi tiết |
| **Nghiệp vụ** | Chỉ tiêu → báo cáo → ai dùng | Lãnh đạo |

---

### Bước 11 — Khai báo cáo dùng bảng này

**Vào:** `1.5 Báo cáo & Chỉ tiêu`

Đây là màn giải đáp câu hỏi *"báo cáo có phải chỉ là bảng output không"*.
**Đúng một nửa** — và panel *"Bảng kết quả đầu ra"* trên màn này giải thích rõ nửa còn lại.

Một báo cáo có hai loại quan hệ với bảng, **đừng nhầm**:

| Trường | Nghĩa là gì | Ví dụ với BC-001 |
|---|---|---|
| **Bảng kết quả đầu ra** | Bảng chứa sẵn số đã tổng hợp, báo cáo **đọc thẳng** để hiện | `mart.doanh_thu_ngay` |
| **Bảng nguồn** | Các bảng **cung cấp dữ liệu để tính ra** số đó | `dwh.giao_dich_thanh_toan`, `dwh.san_pham`, … |

**Cái gì tự xảy ra khi bạn chọn "Bảng kết quả đầu ra":**

⭐ Bảng được chọn **tự động được đánh chip "bảng báo cáo"** ở menu 1.2. Bạn không
phải vào 1.2 gắn tay. Và vì tính ngược từ phía báo cáo nên **không bao giờ lệch** —
gỡ báo cáo thì chip cũng mất.

**Ba trường còn lại rất đáng khai:**

| Trường | Dùng làm gì |
|---|---|
| **Thời gian dữ liệu sẵn sàng** | ⭐ Là tham số của luật "Dữ liệu về đúng giờ cam kết". Cũng là căn cứ để đặt ngược *Giờ cam kết* cho job ở bước 9 |
| **Đối tượng sử dụng** | ⭐ Là **danh sách người cần thông báo** khi phân tích ảnh hưởng — xuất ra được |
| **Chỉ tiêu thể hiện** | Nối chỉ tiêu → báo cáo trên sơ đồ mức nghiệp vụ |

**Chỉ tiêu** (`CT-001 Doanh thu ghi nhận`, …) khai riêng, có hai trường then chốt:
- **Công thức tính** — viết đủ để người khác tính lại ra **cùng con số**
- **Điều kiện lấy dữ liệu** — cái gì bị loại trừ. ⭐ Đây là **chỗ hay lệch số nhất
  giữa các đơn vị**, và là trường đầu tiên cần đọc khi hai báo cáo ra hai con số khác nhau.

---

### Bước 12 — Đặt luật chất lượng và để hệ thống tự canh

Bước cuối. Từ đây trở đi hệ thống chạy **không cần bạn bấm gì nữa**.

#### 12a. Xem trước dữ liệu — `3.3 Phân tích dữ liệu`

Máy quét bảng và trả về: **tỷ lệ rỗng** từng cột, **số giá trị phân biệt**,
phân bố giá trị. Đây là **đo, không phải kiểm tra** — chưa có khái niệm đạt/không đạt.

Kết quả này dùng để **gợi ý bạn nên đặt luật gì**:
- Tỷ lệ rỗng cao bất thường → gợi ý luật *Tỷ lệ điền tối thiểu*
- Số giá trị phân biệt = số dòng → gợi ý cột này là **khoá**, nên đặt luật *Không trùng*
- Ít giá trị phân biệt → gợi ý luật *Thuộc tập giá trị cho phép*

#### 12b. Chọn loại kiểm tra — `3.1 Thư viện luật`

Đây là **thư viện mẫu**, không gắn với bảng nào. Mỗi loại kiểm tra thuộc một trong
**6 chiều chất lượng** (theo **GĐ3 mục 3**): Đầy đủ · Hợp lệ · Nhất quán ·
Không trùng lặp · Chính xác · Kịp thời.

#### 12c. Gán luật vào bảng — `3.2 Luật & Kết quả`

Đây mới là chỗ luật gắn vào dữ liệu thật.

**Ngưỡng cảnh báo lấy từ đâu — 4 cấp, cấp trên thắng cấp dưới:**

```
① Ngưỡng khai ngay lúc gán luật     ← ưu tiên cao nhất
② Ngưỡng của bảng theo Tier
③ Ngưỡng mặc định của loại luật (menu 3.1)
④ Tham số toàn cục nguong_canh_bao_mac_dinh (menu 8.2)   ← chốt chặn cuối
```

Cột **"Nguồn ngưỡng"** trên màn 3.2 hiện đúng cấp nào đang được áp — nên khi
hai luật cùng loại có ngưỡng khác nhau, bạn nhìn cột đó là hiểu ngay, không phải đoán.

**Cách kích hoạt** (3 kiểu, theo **GĐ3 · FR-02**):

| Kiểu | Chạy khi nào |
|---|---|
| Theo lịch | Đúng khung giờ đã đặt |
| **Theo sự kiện** | ⭐ **Ngay sau khi job sinh ra bảng đích chạy xong thành công** |
| Thủ công | Khi có người bấm |

**Chặn job hạ nguồn:** bật công tắc này thì khi luật hỏng, các job đọc bảng này
chuyển sang trạng thái **Bị chặn** thay vì chạy trên dữ liệu xấu.
⚠️ Chỉ bật được với bảng đạt Tier khai ở tham số `bat_cong_chan_tu_tier` (menu 8.2).

#### 12d. Khi luật hỏng — `3.4 Sự cố chất lượng`

Sự cố **tự sinh**, không cần ai tạo phiếu. Và **tự gán người xử lý** theo đúng
đầu mối bạn khai ở bước 5.

```
Luật hỏng dưới ngưỡng nghiêm trọng
   │
   ├─► Tự sinh phiếu sự cố
   ├─► Tự gán: lỗi nghiệp vụ → BDA · lỗi kỹ thuật → DE
   └─► Tự đặt hạn: thời điểm phát hiện + cam kết theo Tier (T1: 24h · T2: 72h)
         │
         ▼
   Người xử lý khắc phục → chuyển "Chờ kiểm tra lại"
         │
         └─► ⭐ Hệ thống TỰ CHẠY LẠI đúng luật đã sinh ra sự cố
               ├─ Đạt      → cho đóng
               └─ Không đạt → phiếu QUAY LẠI trạng thái phân công (GĐ3 mục 6)
```

> **Hai quy tắc chống gian lận trong quy trình này:**
> 1. **Nguyên tắc bốn mắt** — người xử lý **không được tự đóng** sự cố mình xử lý
> 2. **Không tự khai là đã sửa xong** — máy chạy lại luật rồi mới cho đóng

#### 12e. Cảnh báo — `3.5 Cảnh báo`

Đây là nơi khai **quy tắc gửi thông báo**, không phải nơi phát sinh vấn đề.
Người nhận mặc định lấy theo đầu mối của bảng ở 1.2.

⚠️ Màn 8.1 có ô **"Tỷ lệ báo động giả"**. Chỉ số này vượt vạch đỏ nghĩa là bạn
đang đặt ngưỡng quá nhạy — và hậu quả thực tế là **người ta bắt đầu bỏ qua cảnh báo**.
Đây là chỉ số cần theo dõi ngang với chỉ số chất lượng.

---

### Kết quả sau 12 bước — bạn đã có gì

Vào `8.1 Sức khoẻ dữ liệu` và xem. Toàn bộ 10 chỉ số trên màn này
**không có chỉ số nào được gõ tay** — tất cả tính ngược từ những gì bạn vừa khai:

| Chỉ số trên 8.1 | Tính từ bước nào |
|---|---|
| Tỷ lệ có mô tả | Bước 5 — trường Mô tả nghiệp vụ |
| Tỷ lệ có người phụ trách | Bước 5 — ba ô đầu mối |
| Tỷ lệ đã được phê duyệt | Bước 8 |
| Độ phủ quan hệ luồng dữ liệu | Bước 9 — công tắc quét nguồn gốc |
| Tỷ lệ báo cáo truy vết được đến nguồn | Bước 10 + 11 |
| Điểm chất lượng | Bước 12 |
| Cột nhạy cảm đã có chính sách che | Bước 7 |

Và bảng **"Bốn bảng yếu nhất đang được dùng nhiều"** — đây là bảng đáng xem nhất
của cả hệ thống. Nó **nhân điểm chất lượng thấp với lượt dùng cao** để xếp thứ tự
ưu tiên. Bảng điểm 40 mà không ai dùng thì không đáng sửa; bảng điểm 70 mà
5.000 lượt/tuần thì phải sửa ngay.

---

## Phần 4 — Sáu cách một ô trên màn hình có giá trị

Toàn bộ 103 trường trong từ điển được phân đúng vào sáu loại. Rê chuột vào ⓘ
sẽ thấy chip màu tương ứng.

| Loại | Số trường | Nghĩa | Bạn sửa được không |
|---|---|---|---|
| 🔵 **Người dùng khai tay** | 31 | Gõ trực tiếp trên form | Được |
| 🟣 **Hệ thống tự tính** | 29 | Suy ra bằng công thức từ dữ liệu đã có | **Không** |
| 🟦 **Chọn từ danh mục có sẵn** | 20 | Trỏ tới bản ghi của một menu khác | Sửa ở **menu gốc** |
| 🟢 **Hệ thống thu thập tự động** | 11 | Đọc về từ hệ thống nguồn / AD / nhân sự | **Không** |
| ⚪ **Hằng số của hệ thống** | 11 | Danh sách cố định theo quy định | Chỉ đổi bằng thay đổi cấu hình |
| 🟠 **Sinh ra từ quy trình** | 1 | Do một quy trình đặt ra (phê duyệt) | Đổi bằng cách chạy quy trình |

**Số cần nhớ khi có người chất vấn:** **103/103 trường có nguồn gốc truy được**,
và **0 trường mồ côi** — nghĩa là không có trường nào khai xong rồi không ai dùng.
Bạn kiểm chứng được ngay tại menu **2.5 Tiêu chuẩn thông tin mô tả**.

### Hai trục phân loại — chỗ dễ nhầm nhất

Đây là điểm thiết kế quan trọng nhất của module bảo mật, và cũng là chỗ mà
**GĐ4 mục 3** yêu cầu tách bạch. Hai trục **hoàn toàn độc lập**:

|  | **Trục 1 — Mức phân loại** | **Trục 2 — Nhãn dữ liệu nhạy cảm** |
|---|---|---|
| Trả lời | Thông tin này **bí mật tới mức nào** | Dữ liệu này **thuộc loại gì** |
| Giá trị | Công khai · Nội bộ · Mật · Hạn chế truy cập | PD_BASIC · PD_SENSITIVE và nhãn con |
| Gắn vào | Bảng, cột, báo cáo, kênh | Chỉ cột |
| Khai ở | 1.2 (và tự nâng nếu có cột nhạy cảm) | 2.2, máy đề xuất — người xác nhận |
| **Điều khiển** | **Được tải xuống không · thời hạn quyền tối đa · quy tắc lưu trữ** | **Che dữ liệu kiểu gì · có cảnh báo truy cập bất thường không** |

**Ví dụ cụ thể để thấy vì sao phải tách:**
Một bảng báo cáo tổng hợp có thể ở mức **Nội bộ** (không bí mật lắm) nhưng vẫn chứa
cột mang nhãn **PD_BASIC** (có số điện thoại). Nếu gộp một trục, bạn buộc phải chọn:
hoặc siết cả bảng thành *Mật* (làm khó người dùng vô cớ), hoặc để *Nội bộ* và
**số điện thoại lộ ra không bị che**. Tách hai trục thì cột số điện thoại được che
theo nhãn, còn cả bảng vẫn tải xuống bình thường theo mức *Nội bộ*.

---

## Phần 5 — Cái gì máy tự làm, cái gì người phải làm, và làm lúc nào

Bảng này trả lời trực tiếp câu hỏi *"khi nào, như nào thông tin này xuất hiện"*.

### Máy tự chạy theo lịch — không ai bấm

| Việc | Nhịp | Kết quả hiện ở đâu |
|---|---|---|
| Đọc lược đồ hệ thống nguồn (tên bảng, tên cột, kiểu, số dòng, dung lượng) | Theo lịch của từng kết nối ở 8.2 | 1.2 và tab Cột |
| Đồng bộ tài khoản từ AD | Theo lịch | 5.1 cột Tài khoản |
| Đồng bộ trạng thái nhân sự | Hằng ngày | 5.1 — ⭐ nghỉ việc mà chưa khoá tài khoản → cảnh báo Nghiêm trọng ở 5.5 |
| Đồng bộ đơn vị tổ chức | Theo lịch | 7.1 mô hình MDM-DV |
| Đọc lịch sử truy vấn từ SQLWF | Theo lịch | 1.2 cột Lượt dùng/tuần |
| Đọc nhật ký sử dụng của công cụ BI | Theo lịch | 1.5 cột Lượt xem/tháng |
| Chạy luật chất lượng kiểu *Theo lịch* | Khung giờ đã đặt | 3.2 |
| Quét phân tích dữ liệu | Theo lịch | 3.3 |
| Thu hồi quyền hết hạn | Hằng ngày | 5.2 + ghi nhật ký 5.4 |

### Máy tự chạy khi có sự kiện — phản ứng tức thì

| Sự kiện kích hoạt | Máy làm gì ngay |
|---|---|
| Lưu một job mới ở 4.1 | Phân tích SQL → **tự sinh quan hệ luồng dữ liệu** ở 2.3 |
| Job chạy xong thành công | Chạy các luật kiểu *Theo sự kiện* trên bảng đích |
| Luật hỏng dưới ngưỡng nghiêm trọng | **Tự sinh sự cố** + **tự gán người** + **tự đặt hạn** ở 3.4 |
| Sự cố chuyển "Chờ kiểm tra lại" | **Tự chạy lại đúng luật đó**, không đạt thì đẩy phiếu quay lại |
| Xác nhận nhãn nhạy cảm ở 2.2 | **Tự sinh chính sách che** ở 5.2 + nâng mức phân loại bảng |
| Chọn "Bảng kết quả đầu ra" ở 1.5 | Bảng đó **tự được đánh chip "bảng báo cáo"** ở 1.2 |
| Người duyệt bấm Duyệt ở 2.4 | Metadata **có hiệu lực**, vào chỉ mục tìm kiếm |
| Lô dữ liệu vi phạm luật tại cửa nạp | Giữ lô hoặc tách dòng lỗi vào **Vùng chờ** theo mức đã đặt ở 4.2 |
| Người dùng truy vấn dữ liệu | Cổng ghi lại **mã chính sách đã quyết định** cho phép/từ chối → 5.4 |

### Máy tính lại mỗi lần bạn mở màn hình

29 trường loại *tự tính* không được lưu — chúng tính lại từ dữ liệu gốc mỗi lần hiển thị.
Đó là lý do **không bao giờ có chuyện lệch số** giữa hai màn.

Ví dụ: *Số bảng* của một hệ thống = đếm bản ghi ở 1.2 có trường Hệ thống bằng mã đó.
Bạn thêm một bảng ở 1.2, quay lại 1.3 là con số đã đổi — không cần "làm mới".

### Người phải làm tay — máy không thay được

| Việc | Ai | Vì sao máy không làm được |
|---|---|---|
| Viết **mô tả nghiệp vụ** của bảng và cột | BDA | Máy không biết bảng này phục vụ nghiệp vụ gì |
| Khai **công thức chỉ tiêu** và **điều kiện lấy dữ liệu** | BDA | Đây là thoả thuận giữa người với người |
| **Xác nhận** nhãn nhạy cảm | Người có thẩm quyền | Máy chỉ **đề xuất**; gắn sai nhãn = che nhầm dữ liệu |
| **Phê duyệt** hồ sơ | Người sở hữu dữ liệu | Trách nhiệm không uỷ quyền cho máy được |
| Khai quan hệ luồng dữ liệu **máy không dò được** | DE | `CREATE TEMP VIEW` nằm ngoài tầm phân tích SQL |
| Khai **chuẩn đặt tên, Tier, tham số** | Vận hành hệ thống | Đây là quyết định chính sách |
| Khai **thời gian lưu trữ** kèm căn cứ pháp lý | Ban Pháp chế | Phải có căn cứ pháp lý, không suy ra được |
| **Quyết định hợp nhất** bản ghi trùng ở 7.3 | Người sở hữu dữ liệu chủ | Máy tính điểm khớp, người quyết |

---

## Phần 6 — Đi qua từng menu: 35 màn hình

Bảng tra nhanh. Mỗi dòng: **cần có gì trước → bạn làm gì → sinh ra gì cho màn khác**.

### ① DATA CATALOG — dữ liệu nằm ở đâu

| Menu | Cần có trước | Bạn làm gì ở đây | Sinh ra gì cho màn khác |
|---|---|---|---|
| **1.1** Tìm kiếm toàn hệ thống | Không | Gõ từ khoá, lọc theo loại/miền/trạng thái | — (chỉ đọc) |
| **1.2** Bảng dữ liệu ⭐ | 1.3, 1.7, 5.1, 8.2 | Khai bảng, khai cột, gắn thuật ngữ | **Trung tâm** — nuôi 3.x, 4.x, 5.2, 2.3, 1.5 |
| **1.3** Hệ thống & Nguồn | 5.1, 7.1 | Khai hệ thống, đầu mối | Ô chọn "Hệ thống" ở 1.2 và 1.4 |
| **1.4** Kênh trao đổi | 1.3, 1.2 | Khai đường trao đổi dữ liệu giữa hai hệ thống | Mắt xích **đầu tiên** của chuỗi truy vết 2.3 |
| **1.5** Báo cáo & Chỉ tiêu | 1.2 | Khai báo cáo, chỉ tiêu, công thức | Chip "bảng báo cáo" ở 1.2 · mắt xích cuối 2.3 |
| **1.6** Nhóm bảng | 1.2 | Gom bảng thành gói để cấp quyền theo gói | Cấp phạm vi "Nhóm bảng" ở 5.2 |
| **1.7** Miền dữ liệu | 5.1 | Khai cây miền + người chịu trách nhiệm | Ô "Miền" ở 1.2 · bảng theo miền ở 8.1 |
| **1.8** Danh mục tham chiếu | Không | Khai bảng mã dùng chung | Tập giá trị hợp lệ của cột ở 1.2 |

### ② GOVERNANCE — hiểu đúng và tin được

| Menu | Cần có trước | Bạn làm gì ở đây | Sinh ra gì cho màn khác |
|---|---|---|---|
| **2.1** Từ điển nghiệp vụ | 5.1 | Khai thuật ngữ, đánh cờ **CDE** | Ô "Thuật ngữ" ở tab Cột · CDE bắt luật ở 3.2 |
| **2.2** Phân loại & Nhãn | 1.2 | Khai cây nhãn, xác nhận nhãn cho cột | ⭐ **Tự sinh chính sách che** ở 5.2 |
| **2.3** Truy vết luồng dữ liệu | 4.1, 4.2 | **Chủ yếu để xem**; khai tay phần máy không dò được | Chỉ số truy vết ở 8.1 |
| **2.4** Phê duyệt & Phiên bản | 5.1 | Duyệt / trả về hồ sơ, xem lịch sử phiên bản | Trạng thái phê duyệt của mọi đối tượng |
| **2.5** Tiêu chuẩn thông tin mô tả | Không | **Tra cứu** bộ trường bắt buộc + 32 danh sách giá trị | Là chuẩn để tính "Độ hoàn thiện metadata" |

> **2.5 là màn bạn nên mở khi bị chất vấn.** Tab *"Danh sách giá trị chọn"* liệt kê
> đủ 32 dropdown của toàn hệ thống, mỗi cái có cột **"Ai quản lý"** và link tới menu quản lý.
> Không có giá trị nào không giải thích được nguồn.

### ③ DATA QUALITY — số có tin được không

| Menu | Cần có trước | Bạn làm gì ở đây | Sinh ra gì cho màn khác |
|---|---|---|---|
| **3.1** Thư viện luật | Không | Khai **mẫu** loại kiểm tra, ngưỡng mặc định | Danh sách chọn khi gán luật ở 3.2 và 4.2 |
| **3.2** Luật & Kết quả | 1.2, 3.1 | **Gán** luật vào bảng/cột, đặt ngưỡng, hành động khi hỏng | Điểm chất lượng bảng · sinh sự cố 3.4 |
| **3.3** Phân tích dữ liệu | 1.2 | Xem kết quả quét (đo, **không** đạt/không đạt) | Tỷ lệ rỗng, số giá trị phân biệt → gợi ý luật |
| **3.4** Sự cố chất lượng | 3.2, 1.2 | Xử lý phiếu **tự sinh, tự gán** | Chỉ số sự cố đang mở ở 8.1 |
| **3.5** Cảnh báo | 1.2, 1.7 | Khai **quy tắc gửi thông báo** và kênh gửi | Thông báo tới đầu mối |

> **Phân biệt 3.2 với 3.3 — hay bị hỏi:** 3.3 là **đo** (bảng này 12% rỗng),
> 3.2 là **chấm** (12% rỗng, ngưỡng là 5% → **hỏng**). Đo không cần biết ngưỡng;
> chấm thì phải có ngưỡng. Hai việc khác nhau nên tách hai màn.

### ④ NẠP & ĐIỀU PHỐI — dữ liệu đi vào và chảy đi đâu

| Menu | Cần có trước | Bạn làm gì ở đây | Sinh ra gì cho màn khác |
|---|---|---|---|
| **4.1** Luồng xử lý (Job) | 1.2 (**RB2**) | Khai job, bảng đích, giờ cam kết, công tắc quét nguồn gốc | ⭐ **Tự sinh quan hệ lineage** · kích hoạt luật theo sự kiện |
| **4.2** Cửa nạp dữ liệu | 1.4, 3.1 | Khai mẫu nạp, luật kiểm tại cửa, mức xử lý khi vi phạm | Vùng chờ giữ lô/dòng lỗi |
| **4.3** Theo dõi & Pipeline | 4.1, 4.2 | **Xem** trạng thái chạy, nút nào bị chặn | — (chỉ đọc) |

> **Phân biệt 1.4 Kênh với 4.2 Cửa nạp:** 1.4 mô tả **đường dây tồn tại** giữa hai
> hệ thống (SFTP tới Cổng đối tác A, dùng khoá gì, ai đầu mối). 4.2 mô tả **cách nạp
> một loại dữ liệu cụ thể** đi qua đường dây đó (tệp tên gì, cấu trúc ra sao, kiểm gì
> trước khi cho vào). Một kênh phục vụ nhiều cửa nạp. Mẫu nạp **bắt buộc trỏ tới một kênh**.

### ⑤ DATA SECURITY — ai được xem cái gì

| Menu | Cần có trước | Bạn làm gì ở đây | Sinh ra gì cho màn khác |
|---|---|---|---|
| **5.1** Người dùng & Nhóm | Không (đồng bộ AD) | **Gán vai trò** + ma trận Menu × Vai trò | ⭐ Mọi ô chọn người trên toàn hệ thống |
| **5.2** Chính sách truy cập | 1.2, 2.2, 5.1 | Khai chính sách theo bảng / miền / **nhãn** | Quyết định cho phép/từ chối ở cổng truy vấn |
| **5.3** Yêu cầu cấp quyền | 5.1, 1.2 | Nộp và duyệt yêu cầu xin quyền | ⭐ Sinh chính sách ở 5.2 có **truy được lý do cấp** |
| **5.4** Nhật ký kiểm toán | — | **Xem** ai làm gì, **căn cứ chính sách nào** | Bằng chứng cho 6.3 |
| **5.5** Báo cáo quyền & Giám sát | 5.2, 5.4 | Xem quyền thừa, truy cập bất thường | Đề xuất thu hồi quyền |

> **Vì sao phải xin quyền qua 5.3 chứ không cấp thẳng ở 5.2:** chính sách tạo qua 5.3
> có trường **Nguồn = Yêu cầu cấp quyền** kèm mã YC, truy ngược ra **ai xin, xin làm gì,
> ai duyệt**. Chính sách cấp thẳng có Nguồn = *Thủ công* — và ⭐ ở kỳ đánh giá tuân thủ 6.3,
> chính sách nguồn Thủ công bị đánh là **phát hiện không phù hợp** vì không truy được lý do.

### ⑥ CHÍNH SÁCH & TUÂN THỦ

| Menu | Cần có trước | Bạn làm gì ở đây | Sinh ra gì cho màn khác |
|---|---|---|---|
| **6.1** Chính sách dữ liệu | — | Khai chính sách + **yêu cầu kiểm soát đo được** | Mỗi yêu cầu thành một mục checklist ở 6.3 |
| **6.2** Vòng đời & Lưu trữ | 1.2, 6.1 | Khai thời gian lưu + căn cứ pháp lý | Job dọn dữ liệu đọc quy tắc này |
| **6.3** Đánh giá tuân thủ | 6.1, 5.4 | Chạy kỳ đánh giá, ghi kết luận **kèm bằng chứng** | Điểm tuân thủ ở 8.1 |

> ⭐ Trường **Yêu cầu kiểm soát** ở 6.1 phải viết **ở dạng đo được** —
> ví dụ *"Mọi bảng Tier 1 phải có Người sở hữu dữ liệu"*, chứ không phải
> *"Cần tăng cường quản trị"*. Chỉ khi viết đo được thì 6.3 mới chấm tự động
> và trường **Bằng chứng** mới trỏ thẳng vào số liệu trong hệ thống
> (*"7.578/11.482 bảng chưa có người phụ trách"*) thay vì ảnh chụp màn hình rời rạc.

### ⑦ DỮ LIỆU CHỦ (MDM) — Đợt 5

| Menu | Cần có trước | Bạn làm gì ở đây | Sinh ra gì cho màn khác |
|---|---|---|---|
| **7.1** Mô hình dữ liệu chủ | 1.2 | Khai **khoá so khớp** + **quy tắc chọn giá trị khi hợp nhất** | Cơ sở tính điểm khớp ở 7.3 |
| **7.2** Bản ghi nguồn | 7.1 | Xem bản ghi từ từng hệ thống nguồn | Đầu vào cho so khớp |
| **7.3** Nghi ngờ trùng | 7.1, 7.2 | **Quyết định** hợp nhất hay không | Bản ghi chuẩn ở 7.4 |
| **7.4** Bản ghi chuẩn & Phân phối | 7.3 | Xem golden record, theo dõi phân phối ngược | ⭐ Mã chuẩn mà **mọi hệ thống phải dùng** |

Ngưỡng điểm khớp: **≥95%** đề xuất hợp nhất · **85–94%** cần người xem xét ·
**70–84%** nghi ngờ · dưới 70% không đưa vào danh sách.

### ⑧ OPERATIONS

| Menu | Bạn làm gì ở đây |
|---|---|
| **8.1** Sức khoẻ dữ liệu | **Xem** 10 chỉ số quản trị, bảng ưu tiên cải thiện, tiến độ 5 giai đoạn |
| **8.2** Cấu hình hệ thống | Khai **kết nối nguồn · Tier · chuẩn đặt tên · tham số toàn cục** |

---

## Phần 7 — Tự rà soát logic: 8 phép thử bạn tự làm được

Đây là phần để bạn **tự kiểm chứng** thay vì tin lời tôi. Làm lần lượt 8 phép thử này
trên demo, mỗi cái mất chưa tới một phút.

### Phép thử 1 — Có trường nào bịa không?

Vào **2.5 → tab Danh sách giá trị chọn**. Đọc cột *"Ai quản lý"*.
Chọn ngẫu nhiên 3 dòng, bấm vào link menu quản lý, xem đúng giá trị đó có ở đó không.
Nếu có dòng nào không dẫn về đâu → **đó là lỗi thật, báo lại**.

### Phép thử 2 — Trường này khai xong dùng ở đâu?

Vào bất kỳ màn danh sách nào, rê chuột vào ⓘ cạnh tên cột.
Phần **"→ Khai xong thì dùng ở đâu (n)"** phải có ít nhất 1 mục.
Nếu thấy `(0)` → trường đó **mồ côi**, khai vô ích. Hiện tại đếm được **0 trường mồ côi**.

### Phép thử 3 — Đi ngược từ một con số về nguồn

Mở **1.5** → `BC-001 Báo cáo doanh thu ngày` → xem *Bảng nguồn*.
Bấm vào một bảng nguồn → sang **1.2** → tab **Nguồn gốc**.
Bạn phải đi ngược được tới tận job và bảng gốc. Nếu chuỗi đứt ở đâu → chỗ đó
thiếu khai báo lineage.

### Phép thử 4 — Đi xuôi: sửa bảng này thì hỏng cái gì?

Vẫn ở **1.2** → tab **Nguồn gốc** → phần phân tích ảnh hưởng.
Nó liệt kê báo cáo nào sẽ sai và **đối tượng sử dụng nào cần thông báo**.
Đây là câu trả lời cho câu hỏi kinh điển *"đổi cột này có ảnh hưởng gì không"*.

### Phép thử 5 — Vì sao hai luật cùng loại lại khác ngưỡng?

Vào **3.2**, tìm hai luật cùng loại nhưng ngưỡng khác nhau.
Xem cột **"Nguồn ngưỡng"** — nó phải chỉ rõ đang lấy ở cấp nào trong 4 cấp.
Nếu cột này trống → hệ thống không giải thích được ngưỡng của chính nó.

### Phép thử 6 — Sự cố này ai xử lý, tại sao là người đó?

Vào **3.4**, mở một sự cố bất kỳ. Xem *Người xử lý*.
Rồi vào **1.2** mở đúng bảng đó, xem *Đầu mối nghiệp vụ* / *Đầu mối kỹ thuật*.
**Phải khớp**. Nếu không khớp → luật tự gán bị sai.

### Phép thử 7 — Ai cho người này xem bảng đó?

Vào **5.4 Nhật ký kiểm toán**, chọn một dòng truy cập.
Xem cột **"Chính sách quyết định"** → bấm vào → phải ra được chính sách ở 5.2.
Nếu chính sách đó có *Nguồn = Yêu cầu cấp quyền*, bạn còn truy ngược được ra
**mã yêu cầu, người xin, lý do xin, người duyệt**.

### Phép thử 8 — Chỉ số trên 8.1 có bịa không?

Vào **8.1**, chọn một chỉ số. Tự tính lại bằng tay từ các menu nguồn.
Ví dụ *"Tỷ lệ có người phụ trách"* = số bảng ở 1.2 có đủ ba đầu mối ÷ tổng số bảng.
Con số phải khớp — vì nó được tính lại mỗi lần mở màn, không lưu sẵn.

---

## Phần 8 — Những chỗ demo khác thực tế

Nói thẳng để bạn không bị hỏi bất ngờ trong buổi demo.

### Bản chất demo

| Điểm | Trong demo | Thực tế cần |
|---|---|---|
| Dữ liệu | Nằm trong tệp TypeScript, cố định | Cơ sở dữ liệu + API |
| Kết nối nguồn ở 8.2 | Chỉ hiển thị, bấm "Kiểm tra kết nối" ra kết quả dựng sẵn | Kết nối JDBC/API thật |
| Quét lược đồ tự động | Kết quả đã có sẵn trong dữ liệu mẫu | Bộ thu thập chạy theo lịch |
| Phân tích SQL sinh lineage | Kết quả đã có sẵn | Bộ phân tích cú pháp SQL |
| Thêm mới / Sửa | Popup mở được, kiểm tra hợp lệ chạy được, **không lưu xuống đâu** | Ghi DB |
| Số lượng bản ghi | Vài chục dòng cho dễ nhìn | Hàng chục nghìn |

### Những gì chưa làm — và vì sao

| Điểm | Trạng thái | Ghi chú |
|---|---|---|
| **Phân trang** danh sách | Chưa có | Cố ý bỏ trong demo. **Bắt buộc** khi dữ liệu thật |
| **Tuỳ biến cột** theo người dùng | Chưa có | Ngoài phạm vi demo, nên có khi triển khai |
| Dấu **ⓘ** | Phủ **các trường chính** trên bảng danh sách và form thêm mới, **chưa phủ 100%** mọi trường mọi màn | Từ điển 103 trường đã có sẵn; bổ sung chỉ là gắn thêm `info` cho từng ô |
| Từ điển trường | **103 trường**, phủ đủ 7 nhóm đối tượng của GĐ2 và mọi trường từng bị chất vấn | Chưa phải mọi trường xuất hiện trên UI |
| Module ⑦ **MDM** | Có đủ khung màn hình và logic | Triển khai thật để **Đợt 5** theo lộ trình BDA |

### Hai quyết định còn treo, cần chốt trước khi triển khai thật

**① Tách hai trục phân loại (gap D1).**
Thiết kế hiện tại đã tách *mức phân loại* khỏi *nhãn nhạy cảm* theo đúng GĐ4 mục 3.
Cần **chốt chính thức** trước khi bắt đầu gắn nhãn thật, vì khi đã áp cho 412 cột
và đồng bộ sang hệ thống phân quyền thì **không sửa ngược được** — mã nhãn không đổi được sau khi tạo.

**② Phạm vi cổng chặn.**
Tham số `bat_cong_chan_tu_tier` ở 8.2 quyết định từ Tier nào trở lên thì được bật
chặn dữ liệu xấu. ⚠️ Đặt quá rộng ngay từ đầu sẽ khiến người dùng **không khai được gì
và quay lưng với hệ thống**. Khuyến nghị bắt đầu từ Tier 1, mở rộng dần.

---

## Tóm tắt một trang

Nếu chỉ nhớ được một trang, nhớ trang này:

1. **DMP không chứa dữ liệu** — nó chứa thông tin về dữ liệu.
2. **Khai theo thứ tự**: cấu hình + người → miền + thuật ngữ + nhãn → hệ thống → **bảng** → job → luật → báo cáo.
3. **Bảng dữ liệu (menu 1.2) là trung tâm.** Mọi menu khác đều trỏ về nó.
4. **Ba ô đầu mối ở 1.2 quyết định ai nhận sự cố.** Bỏ trống = sự cố không ai nhận.
5. **Khai job xong là hệ thống tự dựng luồng dữ liệu** — bạn không vẽ tay.
6. **Nhãn nhạy cảm gắn một lần, chính sách che tự áp** cho mọi cột mang nhãn.
7. **Sự cố tự sinh, tự gán, tự chạy lại kiểm chứng** — không tự khai là đã sửa xong được.
8. **Có ⓘ thì rê chuột vào** — nó nói trường này từ đâu ra và đi đâu về đâu.
9. **Bị chất vấn thì mở menu 2.5** — 32 danh sách giá trị, mỗi cái có nơi quản lý.
10. **Muốn biết ưu tiên sửa gì thì mở 8.1** — bảng "yếu nhất mà dùng nhiều nhất".
