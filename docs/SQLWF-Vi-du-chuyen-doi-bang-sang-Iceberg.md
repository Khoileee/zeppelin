# VÍ DỤ THỰC HÀNH — CHUYỂN MỘT BẢNG SANG ICEBERG
### Hai cách làm, chạy trên cùng một bảng mẫu, so kết quả

> **Người viết:** Khôi (IT BA) · **Ngày:** 08/2026
> **Tài liệu liên quan:** [Chi tiết tính năng theo giai đoạn](./SQLWF-Chi-tiet-tinh-nang-theo-giai-doan.md) — mục 1.4 · [Đề xuất Kiến trúc Data Management](./SQLWF-De-xuat-Kien-truc-Data-Management.md)
>
> **Mục đích:** mục 1.4.1(c) của tài liệu chi tiết nói rằng bước "lập sổ Iceberg" có 2 cách làm, khác nhau rất nhiều. Bản này **chạy thử cả 2 cách trên một bảng mẫu 4 dòng** để thấy khác biệt bằng số liệu cụ thể, thay vì đọc bảng so sánh trừu tượng.
>
> ⚠️ **Cú pháp lệnh chỉ mang tính minh hoạ** — cú pháp thật phụ thuộc phiên bản Iceberg + Spark đang cài. Trọng tâm của tài liệu này là **kết quả khác nhau ra sao**, không phải cú pháp.

---

## MỤC LỤC

- [1. Bàn xuất phát — bảng mẫu](#1-bàn-xuất-phát--bảng-mẫu)
- [2. Cách nhanh — lập sổ cho giấy sẵn có](#2-cách-nhanh--lập-sổ-cho-giấy-sẵn-có)
- [3. Cách chuẩn — chép lại sang sổ mới](#3-cách-chuẩn--chép-lại-sang-sổ-mới)
- [4. So sánh kết quả](#4-so-sánh-kết-quả)
- [5. Kết luận & khuyến nghị](#5-kết-luận--khuyến-nghị)

---

# 1. Bàn xuất phát — bảng mẫu

Bảng `DOI_SOAT_A`, phân vùng theo ngày, đang lưu Parquet thuần:

```
/storage/business_zone/bi/doi_soat_A/
├── PARTITION_DATE=20260801/part-00000.parquet
└── PARTITION_DATE=20260802/part-00000.parquet
```

**Schema khai báo trong SQLWF** nói `so_tien` là **số**. **Nhưng dữ liệu thật trong file là chữ** — vì dữ liệu vào qua đường Upload, mà toàn bộ cột nạp qua đường này hiện lưu dưới dạng chữ bất kể khai kiểu gì *(rủi ro số 4 trong tài liệu mẹ)*.

| ma_giao_dich | so_tien | ngay_gd |
|---|---|---|
| GD001 | `"1500000"` | 2026-08-01 |
| GD002 | `"900000"` | 2026-08-01 |
| GD003 | `"250000"` | 2026-08-02 |
| GD004 | `"N/A"` | 2026-08-02 |

> 🔴 **Để ý dòng GD004.** Dữ liệu bẩn, đang nằm im trong bảng mà **hiện tại không ai biết** — vì Parquet thuần không có gì để lộ ra chuyện đó.

---

# 2. Cách nhanh — lập sổ cho giấy sẵn có

## 2.1 Làm gì

Tạo vỏ bảng Iceberg với **đúng schema đang có**, rồi nhặt các file Parquet sẵn có vào sổ — **không đọc nội dung file**:

```sql
-- ① Tạo vỏ bảng, giữ nguyên kiểu như file đang có
CREATE TABLE bi.doi_soat_A (
    ma_giao_dich  string,
    so_tien       string,      -- ← giữ nguyên là CHỮ
    ngay_gd       date
) USING iceberg PARTITIONED BY (ngay_gd);

-- ② Nhặt file Parquet sẵn có vào sổ
CALL system.add_files(
    table        => 'bi.doi_soat_A',
    source_table => 'parquet.`/storage/business_zone/bi/doi_soat_A`'
);
```

**Xong sau khoảng 2 phút.** File Parquet không bị đụng tới, chỉ mọc thêm thư mục `metadata/`.

## 2.2 Thử đọc sổ xem được gì

```sql
SELECT record_count, null_value_counts, lower_bounds, upper_bounds
FROM   bi.doi_soat_A.files;
```

| Chỉ số | Iceberg trả về | Thực tế đúng phải là | |
|---|---|---|---|
| Số dòng | 4 | 4 | ✅ |
| Số ô trống cột `so_tien` | 0 | 0 | ✅ |
| **Giá trị nhỏ nhất `so_tien`** | `"1500000"` | 250.000 | 🔴 **SAI** |
| **Giá trị lớn nhất `so_tien`** | `"N/A"` | 1.500.000 | 🔴 **SAI** |

## 2.3 Vì sao sai

Cột đang là chữ nên hệ thống **so sánh theo bảng chữ cái**, không phải theo giá trị số:

```
   So sánh chữ:   "1500000"  <  "250000"  <  "900000"  <  "N/A"
                      ↑           ↑           ↑          ↑
                  ký tự '1'   ký tự '2'   ký tự '9'  ký tự 'N'

   So sánh số:     250.000  <  900.000  <  1.500.000
```

## 2.4 Hệ quả thật với Data Quality

Cấu hình DQ kiểu *"cảnh báo nếu số tiền giao dịch vượt 1 tỷ"* hoặc *"phát hiện giá trị âm"* sẽ chạy trên đúng 2 con số sai ở trên.

> 🔴 **Điểm nguy hiểm:** kết quả không phải "lỗi" mà là **"rác trông như đúng"**. Màn Tình trạng dữ liệu vẫn hiện đủ số, DQ vẫn ra điểm chất lượng, không có gì báo động. Chỉ là mấy con số đó không dùng được.

**Vẫn có 2 thứ dùng tốt** — vì không phụ thuộc kiểu dữ liệu:

| Chỉ số | Vì sao vẫn đúng |
|---|---|
| **Độ tươi dữ liệu** (cập nhật lần cuối) | Lấy từ thời điểm ghi, không liên quan nội dung cột |
| **Số dòng · dung lượng** | Đếm file, không liên quan nội dung cột |

---

# 3. Cách chuẩn — chép lại sang sổ mới

## 3.1 Làm gì

Đọc toàn bộ dữ liệu cũ, **ép về đúng kiểu**, ghi ra bảng Iceberg mới:

```sql
CREATE TABLE bi.doi_soat_A
USING iceberg
PARTITIONED BY (ngay_gd)
AS
SELECT ma_giao_dich,
       CAST(so_tien AS DECIMAL(18,2)) AS so_tien,   -- ← ép về đúng kiểu
       ngay_gd
FROM   parquet.`/storage/business_zone/bi/doi_soat_A`;
```

## 3.2 Chạy phát là gặp ngay dòng GD004

```
ERROR: Cannot cast 'N/A' to DECIMAL(18,2)
```

Hoặc tuỳ cấu hình thì nó lặng lẽ biến giá trị đó thành `NULL`.

> ### 💡 Cả hai trường hợp đều là TIN TỐT
>
> Dữ liệu bẩn lộ ra **ở đây** — trên 1 bảng thí điểm, lúc còn đang thí điểm — thay vì lộ ra sau này khi đã chuyển 500 bảng và Data Quality đã chạy trên số liệu rác được vài tháng.
>
> **Đây chính là mục đích của giai đoạn thí điểm: để lòi ra vấn đề.**

## 3.3 Xử lý dòng bẩn rồi chạy lại

```sql
CREATE TABLE bi.doi_soat_A
USING iceberg
PARTITIONED BY (ngay_gd)
AS
SELECT ma_giao_dich,
       CASE WHEN so_tien RLIKE '^[0-9]+(\.[0-9]+)?$'
            THEN CAST(so_tien AS DECIMAL(18,2))
            ELSE NULL                                -- giá trị không hợp lệ → để trống
       END AS so_tien,
       ngay_gd
FROM   parquet.`/storage/business_zone/bi/doi_soat_A`;
```

> ⚠️ **Quyết định nghiệp vụ ở đây:** giá trị không ép được kiểu thì **để trống** hay **tách ra file lỗi để xử lý riêng**? Với bảng đối soát, đề xuất tách ra file lỗi — vì mỗi dòng là một giao dịch, không thể lặng lẽ bỏ đi.

## 3.4 Đọc sổ lại

| Chỉ số | Iceberg trả về | |
|---|---|---|
| Số dòng | 4 | ✅ |
| **Số ô trống `so_tien`** | **1** ← chính là GD004, giờ đã nhìn thấy | ✅ |
| Giá trị nhỏ nhất | 250000.00 | ✅ |
| Giá trị lớn nhất | 1500000.00 | ✅ |

Giờ mấy con số này mới dùng được. Cấu hình DQ *"tỉ lệ trống cột `so_tien` không quá 1%"* chạy đúng ngay, và **không phải quét lại bảng** — chỉ đọc sổ.

---

# 4. So sánh kết quả

| Tiêu chí | Cách nhanh | Cách chuẩn |
|---|---|---|
| **Thời gian** (bảng 25 GB) | ~5 phút | ~2–4 giờ |
| **Dung lượng cần** | Không tốn thêm | Gấp đôi tạm thời (cũ + mới cùng tồn tại) |
| **File Parquet cũ** | Giữ nguyên, dùng lại luôn | Ghi lại toàn bộ |
| **File vụn (nhiều file nhỏ)** | Giữ nguyên | Được gộp lại, đọc nhanh hơn |
| **Dữ liệu bẩn** | 🔴 Vẫn nằm im trong bảng | ✅ Lộ ra ngay lúc chuyển |
| **Độ tươi · số dòng · dung lượng** | ✅ Dùng được | ✅ Dùng được |
| **Min/max · tỉ lệ trống theo cột** | 🔴 Có số nhưng **sai** | ✅ Đúng |
| **Xem lại số liệu quá khứ** | ✅ Có | ✅ Có |
| **Vết ghi dữ liệu** | ✅ Có | ✅ Có |
| **Số loại kiểm tra DQ "đọc sổ" dùng được** | ~4 / 8 | **8 / 8** |
| **Rủi ro khi chuyển** | Thấp | Có thể lỗi hàng loạt (nhưng lỗi = phát hiện được vấn đề) |

---

# 5. Kết luận & khuyến nghị

## 5.1 Nghịch lý cần nhớ

> **Cách nhanh nguy hiểm hơn ở chỗ nó không báo lỗi.**
>
> Bảng chuyển xong trông đẹp: màn Tình trạng dữ liệu hiện đủ số, DQ chạy ra điểm chất lượng, không ai thấy gì bất thường. Chỉ có điều một nửa số chỉ số là rác.
>
> Cách chuẩn thì gãy ngay lúc chuyển — mà gãy sớm trên 20 bảng thí điểm thì còn sửa được.

## 5.2 Khuyến nghị

| Phạm vi | Cách đề xuất | Lý do |
|---|---|---|
| **Nhóm bảng thí điểm (GĐ 1)** | ✅ **Cách chuẩn** | Mục đích của thí điểm là để lòi ra vấn đề kiểu dữ liệu, không phải để xong nhanh |
| **Mở rộng diện rộng (GĐ 2+)** | Quyết theo từng bảng | Bảng có schema sạch → Cách nhanh cũng đủ. Bảng nạp qua Upload → phải Cách chuẩn |
| **Bảng chỉ cần theo dõi độ tươi, không cần DQ sâu** | Cách nhanh | 2 chỉ số quan trọng nhất vẫn đúng, tiết kiệm rất nhiều thời gian |

## 5.3 Việc kéo theo cần đưa vào kế hoạch

| # | Việc | Ghi chú |
|---|---|---|
| 1 | **Rà kiểu dữ liệu trước khi chuyển** | Chạy thử `CAST` trên bảng nguồn để đếm bao nhiêu dòng không ép được kiểu — làm trước, không đợi đến lúc chuyển mới biết |
| 2 | **Chốt cách xử lý dòng không ép được kiểu** | Để trống hay tách file lỗi — là quyết định nghiệp vụ, khác nhau theo loại bảng |
| 3 | **Bổ sung tầng ép kiểu ở cửa nạp** | Nếu không, chuyển xong bảng sạch rồi ngày mai Upload lại đổ chữ vào — quay về vạch xuất phát |

> 📌 **Việc số 3 là quan trọng nhất về lâu dài.** Chuyển đổi chỉ dọn được dữ liệu quá khứ; không sửa cửa nạp thì dữ liệu bẩn tiếp tục chảy vào.

---

> **Tài liệu này là ví dụ minh hoạ phục vụ thảo luận, dựa trên hiện trạng khảo sát mã nguồn SQLWF tháng 07–08/2026.**
> Cú pháp lệnh cần đội hạ tầng xác nhận theo phiên bản Iceberg + Spark thực tế trước khi áp dụng.
