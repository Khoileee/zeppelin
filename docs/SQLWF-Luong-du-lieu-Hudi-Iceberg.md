# SQLWF — Luồng dữ liệu hiện trạng & Vì sao cần Hudi / Iceberg
### Bản giải thích cho người mới (kèm ví dụ + diagram ASCII)

> Phạm vi bản này: **chỉ** giải thích (1) SQLWF là gì, (2) dữ liệu đi như thế nào, (3) Hudi/Iceberg là gì và vì sao cần.
> **Data Quality tạm gác lại** — sẽ viết ở tài liệu riêng.
> Ký hiệu ⚠️ = chỗ tôi đang suy luận từ khảo sát code, **cần bạn xác nhận** để chốt (không dám khẳng định chắc).

---

## MỤC LỤC
- [1. SQLWF là gì? (hiểu trong 1 phút)](#1-sqlwf-là-gì)
- [2. Dữ liệu được cất ở đâu — HDFS, Parquet, "bảng"](#2-dữ-liệu-được-cất-ở-đâu)
- [3. Dữ liệu đi như thế nào — luồng 5 chặng](#3-dữ-liệu-đi-như-thế-nào)
- [4. Một bảng ra đời & sống ra sao (vòng đời)](#4-một-bảng-ra-đời--sống-ra-sao)
- [5. Vấn đề của cách làm hiện tại (Parquet thuần)](#5-vấn-đề-của-cách-làm-hiện-tại)
- [6. "Table format" là gì — chìa khóa để hiểu Hudi/Iceberg](#6-table-format-là-gì)
- [7. Iceberg — giải thích + ví dụ](#7-iceberg)
- [8. Hudi — giải thích + ví dụ](#8-hudi)
- [9. So sánh & bảng nào nên dùng loại nào](#9-so-sánh--bảng-nào-nên-dùng-loại-nào)
- [10. Trước / Sau khi áp dụng vào SQLWF](#10-trước--sau-khi-áp-dụng-vào-sqlwf)
- [11. Từ điển thuật ngữ](#11-từ-điển-thuật-ngữ)

---

## 1. SQLWF là gì?

Hình dung SQLWF (SQL Workflow) như một **nhà máy + nhà kho cho dữ liệu**, chạy trên nền **Hadoop**.

- **Nhà kho** = nơi cất dữ liệu (HDFS — xem §2).
- **Nhà máy** = các dây chuyền đưa dữ liệu vào, làm sạch, gộp, đối soát (các module trong app).
- **Văn phòng quản lý** = nơi khai báo *bảng nào là gì, ai sở hữu, dữ liệu đến từ đâu* (Quản lý bảng — metadata).

```
                       ┌──────────────────────────────────────────┐
                       │                 NGƯỜI DÙNG                 │
                       │        (BA / Data Engineer / vận hành)     │
                       └───────────────────┬────────────────────────┘
                                           │ thao tác trên web app
                       ┌───────────────────▼────────────────────────┐
                       │            SQLWF (Web App - Angular)         │
                       │  Quản lý bảng · Quản lý danh mục · Upload ·   │
                       │  Quản lý job (ETL) · SQL query · Đối soát ... │
                       └───────────────────┬────────────────────────┘
                                           │ gọi API (Java backend)
        ┌──────────────────────┬───────────┼───────────┬─────────────────────┐
        ▼                      ▼           ▼           ▼                     ▼
   ┌─────────┐          ┌────────────┐ ┌────────┐ ┌──────────┐        ┌────────────┐
   │ MongoDB │          │ HDFS +     │ │ MariaDB│ │ MinIO    │        │ RabbitMQ / │
   │ metadata│          │ Parquet    │ │ menu + │ │ (file    │        │ Email/SMS  │
   │ + config│          │ (DATA LAKE)│ │ quyền  │ │ tài chính)│       │ (thông báo)│
   └─────────┘          └────────────┘ └────────┘ └──────────┘        └────────────┘
     "sổ sách"           "nhà kho hàng"  "thẻ ra    "kho phụ"          "băng chuyền +
                                          vào cửa"                      loa thông báo"
```

**Điểm cốt lõi cần nhớ:** dữ liệu *thật* (số liệu doanh thu, giao dịch...) nằm ở **HDFS dưới dạng file Parquet**. MongoDB chỉ giữ **thông tin mô tả** (bảng tên gì, cột gì, ai sở hữu) chứ không giữ số liệu lớn.

---

## 2. Dữ liệu được cất ở đâu?

Ba khái niệm xếp chồng nhau:

```
   "BẢNG" (cái người dùng nhìn thấy: revenue_merchant)
      │  thực chất là...
      ▼
   MỘT THƯ MỤC trên HDFS:  /data/lake/revenue_merchant/
      │  bên trong chứa...
      ▼
   NHIỀU FILE PARQUET:  part-0001.parquet, part-0002.parquet, ...
```

| Khái niệm | Là gì (nói đơn giản) | Ví dụ |
|---|---|---|
| **HDFS** | Một "ổ cứng khổng lồ" ghép từ nhiều máy — chứa được rất nhiều file lớn | như Google Drive nội bộ của công ty |
| **Parquet** | Một **định dạng file** lưu bảng theo **cột** (nén tốt, đọc nhanh khi chỉ cần vài cột) | 1 file = một "lát" dữ liệu của bảng |
| **"Bảng"** | Một **thư mục** gom nhiều file Parquet + được **Hive** biết cấu trúc (tên cột, kiểu) để query bằng SQL | `revenue_merchant` |
| **Partition (phân vùng)** | Cách chia bảng thành thư mục con theo 1 cột (thường theo ngày) để tìm nhanh | `.../revenue_merchant/date=2026-07-24/` |

> **Tại sao chia partition theo ngày?** Vì khi hỏi "doanh thu ngày 24/07", hệ thống chỉ mở đúng thư mục `date=2026-07-24/` thay vì quét cả bảng → nhanh hơn nhiều.

Ví dụ một bảng có partition theo ngày:

```
/data/lake/revenue_merchant/
   ├── date=2026-07-22/  →  part-0001.parquet   (dữ liệu ngày 22)
   ├── date=2026-07-23/  →  part-0001.parquet   (dữ liệu ngày 23)
   └── date=2026-07-24/  →  part-0001.parquet   (dữ liệu ngày 24)
```

---

## 3. Dữ liệu đi như thế nào?

Luồng chính gồm **5 chặng**. Ta bám theo **một ví dụ xuyên suốt**:

> 🧩 **Ví dụ:** Mỗi ngày có 1 file Excel "doanh thu theo merchant" cần đưa vào bảng `revenue_merchant`.

```
   FILE Excel                                                     BẢNG TỔNG HỢP
   doanh thu   ①NẠP      ②VALIDATE     ③STAGING      ④MERGE        (Data Lake)
   ngày 24/07 ───────►  ┌─────────┐   ┌─────────┐   ┌──────────┐  ┌──────────────┐
      📄               │ Kiểm tra │   │ bảng    │   │Coordinator│ │ revenue_     │
                        │ cấu trúc │──►│ tạm     │──►│ gộp vào   │►│ merchant     │
                        │ kiểu/bắt │   │ _TMP    │   │ bảng chính│ │ date=24/07 ✔ │
                        │ buộc/... │   │ (HDFS)  │   │           │ │              │
                        └─────────┘   └─────────┘   └──────────┘  └──────────────┘
                          Python          ⚠️           ⚠️
                        (service ngoài)  staging     "nền job"
```

**Giải thích từng chặng (ví dụ hoá):**

| Chặng | Chuyện gì xảy ra với file ngày 24/07 |
|---|---|
| ① **Nạp (ingest)** | Người dùng chọn template + tải file lên. Có 3 "cửa" nạp — xem bảng bên dưới. |
| ② **Validate** | Hệ thống gọi **service Python** kiểm tra: đúng số cột không? cột "doanh thu" có phải số không? cột bắt buộc có trống không? ngày đúng định dạng không? → sai thì **chặn ngay**, xuất file báo lỗi. |
| ③ **Staging (`_TMP`)** | Dữ liệu hợp lệ được đẩy lên HDFS và nạp vào **bảng tạm `revenue_merchant_TMP`**. Đây là "khu vực chờ", chưa phải bảng chính. |
| ④ **Merge (hợp nhất)** | ⚠️ Một **nền chạy job ("Coordinator")** lấy dữ liệu từ `_TMP` ghi vào **bảng chính** `revenue_merchant`, phân vùng `date=2026-07-24`. |
| ⑤ **Khai thác** | Xong. Giờ có thể xem/query dữ liệu ngày 24/07. |

**3 cửa NẠP dữ liệu vào một bảng:**

| Cửa nạp | Khi nào dùng | Ví dụ |
|---|---|---|
| **Quản lý Upload** | Có file sẵn (Excel/CSV) cần đưa vào theo template | File doanh thu hằng ngày |
| **Quản lý job (ETL)** | Cần tự động đọc nguồn → biến đổi → ghi bảng, chạy theo lịch | Job chạy 1h sáng mỗi ngày gom dữ liệu |
| **Quản lý danh mục** | Dữ liệu tham chiếu (danh mục) nhập tay/upload, có duyệt | Danh mục mã tỉnh, loại dịch vụ |

**4 cửa XEM dữ liệu của một bảng:**

| Cửa xem | Đặc điểm |
|---|---|
| **Màn dữ liệu trong app** | Xem dạng bảng, có phân trang, tìm kiếm (giống màn "Dữ liệu danh mục") |
| **SQL query** | Gõ câu SQL truy vấn trực tiếp |
| **HDFS Explorer** ⚠️ | Xem thẳng **file Parquet thô** trên HDFS (cần xác nhận vị trí/chức năng menu này) |
| **Export / Delivery** | Xuất Excel/CSV, hoặc gửi ra ngoài |

---

## 4. Một bảng ra đời & sống ra sao

```
  (1) TẠO BẢNG                         (2) DỮ LIỆU ĐỔ VÀO              (3) XEM
  ┌───────────────────┐               ┌───────────────────┐          ┌──────────────┐
  │ Quản lý bảng:      │  tạo folder   │ Upload / Job /     │  ghi     │ App / SQL /  │
  │ - tên bảng         │──────────────►│ Danh mục           │─────────►│ HDFS Explorer│
  │ - schema (cột/kiểu)│  HDFS + Hive  │ (qua _TMP→merge)   │  Parquet │ / Export     │
  │ - metadata nghiệp  │               │                    │          │              │
  │   vụ (job, domain, │               └───────────────────┘          └──────────────┘
  │   owner, datamart, │
  │   tần suất...)     │  ◄── phần "khai báo" này chính là METADATA, nằm ở Quản lý bảng
  └───────────────────┘
```

- **Tạo bảng** = khai báo *cấu trúc* + *metadata*. Về vật lý sinh ra một thư mục Parquet trên HDFS (kèm đăng ký Hive để query SQL).
- **Metadata** (rất quan trọng cho báo cáo sau này): bảng này *do job nào sinh ra*, *thuộc domain nào*, *ai sở hữu*, *đồng bộ mấy lần/ngày*, *có phải datamart không*... — tất cả nằm ở **Quản lý bảng**.

---

## 5. Vấn đề của cách làm hiện tại

Hiện các bảng SQLWF chủ yếu là **Parquet/Hive thuần**. Kiểu này rất tốt cho *ghi thêm (append) + đọc*, nhưng **yếu ở 3 việc** — và đây chính là lý do cần Hudi/Iceberg.

### Vấn đề 1 — Muốn SỬA/XÓA vài dòng → phải ghi đè cả partition

> 🧩 Ví dụ: merchant `CP001` đổi tên từ "Cửa hàng A" → "Cửa hàng A1". Chỉ cần sửa **1 dòng** trong ngày 24/07.

```
   Parquet thuần: KHÔNG sửa được 1 dòng trong file.
   Phải: đọc CẢ file ngày 24/07  →  sửa dòng đó  →  GHI ĐÈ lại CẢ file.
   ┌──────────────────────────┐        ┌──────────────────────────┐
   │ date=2026-07-24 (10 triệu │  ───►  │ date=2026-07-24 (10 triệu │
   │ dòng) — viết lại TẤT CẢ   │ tốn kém│ dòng) — chỉ khác 1 dòng   │
   └──────────────────────────┘        └──────────────────────────┘
```

→ Đây chính là lý do SQLWF phải dùng mẹo **`_TMP` → Coordinator ghi đè partition**: vì Parquet không cho "sửa tại chỗ". Cơ chế này là **giải pháp chữa cháy cho việc thiếu upsert**.

### Vấn đề 2 — Không "xem lại quá khứ" được (không time-travel)

> 🧩 Ví dụ: "Cho tôi xem bảng này **đúng như lúc 8h sáng hôm qua**, trước khi job chạy đè." → Parquet thuần **chịu**, vì đã ghi đè là mất bản cũ.

### Vấn đề 3 — Đổi cấu trúc (schema) dễ vỡ

> 🧩 Ví dụ: thêm cột `discount` vào bảng. Với Hive thuần, thao tác thêm/đổi/xoá cột hoặc đổi cách partition dễ làm **query cũ gãy** hoặc đọc sai file cũ.

---

## 6. "Table format" là gì?

Đây là khái niệm chìa khóa. **Hudi và Iceberg KHÔNG thay thế Parquet** — chúng là **một lớp "sổ quản lý" đặt TRÊN các file Parquet**.

```
   ┌─────────────────────────────────────────────────────────┐
   │  ENGINE (công cụ đọc/ghi): Spark, Trino, Flink, Hive...  │  ← ai xử lý
   ├─────────────────────────────────────────────────────────┤
   │  TABLE FORMAT: Hudi / Iceberg                            │  ← "sổ mục lục + sổ
   │   • biết file nào là mới nhất / đã xoá                    │     thay đổi" (LỚP MỚI)
   │   • ghi nhật ký thay đổi (commit), cho time-travel        │
   │   • quản lý schema an toàn                                │
   ├─────────────────────────────────────────────────────────┤
   │  FILE FORMAT: Parquet (vẫn y nguyên)                     │  ← dữ liệu thật
   ├─────────────────────────────────────────────────────────┤
   │  STORAGE: HDFS (vẫn y nguyên)                            │  ← ổ cứng
   └─────────────────────────────────────────────────────────┘
```

**Ví von cho dễ nhớ:**
- **Parquet** = những **trang giấy** rời ghi số liệu.
- **Table format (Hudi/Iceberg)** = **quyển sổ mục lục + nhật ký chỉnh sửa** kẹp cùng xấp giấy đó. Nhờ quyển sổ này mà ta biết: *trang nào mới nhất, trang nào đã bỏ, hôm qua xấp giấy trông thế nào, và sửa 1 dòng thì ghi thêm 1 trang nhỏ thay vì chép lại cả xấp*.

Nhờ lớp "sổ" này, data lake có được các khả năng **như database** (gọi là mô hình **Lakehouse** = Lake + Warehouse):

| Khả năng | Nghĩa là | Giải quyết vấn đề nào ở §5 |
|---|---|---|
| **ACID / commit** | Mỗi lần ghi là 1 "giao dịch" trọn vẹn, không nửa vời | an toàn khi nhiều job cùng ghi |
| **Upsert / Delete theo dòng** | Sửa/xoá đúng dòng cần, không đụng phần còn lại | Vấn đề 1 |
| **Time-travel** | Xem lại bảng ở thời điểm/phiên bản cũ | Vấn đề 2 |
| **Schema/Partition evolution** | Thêm/đổi cột, đổi cách partition **an toàn** | Vấn đề 3 |

---

## 7. Iceberg

**Iceberg mạnh nhất cho: bảng phân tích lớn, ổn định lâu dài, nhiều công cụ cùng đọc, cần đổi schema an toàn & xem lại lịch sử.**

### Cơ chế cốt lõi: "snapshot" (ảnh chụp)
Mỗi lần ghi, Iceberg tạo một **snapshot** — như chụp một tấm ảnh trạng thái bảng tại thời điểm đó. Bảng = danh sách snapshot theo thời gian.

```
   Ghi ngày 22 ──► snapshot S1  (bảng gồm file A)
   Ghi ngày 23 ──► snapshot S2  (bảng gồm file A + B)
   Sửa 1 dòng   ──► snapshot S3  (bảng gồm file A + B' + C)   ← "hiện tại"
                     ▲
                     └── vẫn giữ S1, S2 → xem lại được!
```

> 🧩 **Ví dụ time-travel (rất hữu ích cho đối soát/audit):**
> ```sql
> -- Xem bảng ĐÚNG như hôm qua (snapshot S2), dù giờ đã có S3
> SELECT * FROM revenue_merchant FOR TIMESTAMP AS OF '2026-07-23 23:59:59';
> ```
> → Trả về đúng dữ liệu ngày 23, cực hợp để **truy vết "số liệu lúc đó là bao nhiêu"** khi có tranh cãi đối soát.

### Vài điểm hay khác
- **Schema evolution an toàn:** thêm cột `discount` → query cũ vẫn chạy, dữ liệu cũ hiểu là `discount = null`. Không phải viết lại bảng.
- **Hidden partitioning:** người viết SQL **không cần** nhớ tên cột partition. Iceberg tự biết cắt đúng partition → ít lỗi, ít quét thừa.
- **Đa engine / vendor-neutral:** cùng 1 bảng Iceberg, Spark/Trino/Flink/… đều đọc được (chuẩn mở). Tốt cho tương lai mở rộng công cụ.

**Khi nào dùng Iceberg:** bảng tổng hợp lớn để phân tích/báo cáo, ít sửa dòng lẻ nhưng cần **ổn định, đổi schema, xem lịch sử, nhiều tool cùng dùng**.

---

## 8. Hudi

**Hudi mạnh nhất cho: bảng CẬP NHẬT LIÊN TỤC — cần sửa/xoá dòng thường xuyên, CDC, gần thời gian thực.**

### Cơ chế cốt lõi: "upsert" theo **record key**
Bạn khai báo một **khóa** cho bảng (vd `merchant_id`). Khi nạp dữ liệu mới, Hudi **tự so khóa**:
- Khóa đã tồn tại → **cập nhật (update)** đúng dòng đó.
- Khóa chưa có → **thêm mới (insert)**.
(→ gọi chung là **upsert** = update + insert.)

```
   Bảng đang có:            File mới nạp (upsert theo merchant_id):
   ┌──────────────────┐     ┌──────────────────┐
   │ CP001  Cửa hàng A│     │ CP001  Cửa hàng A1│  → CP001 đã có → SỬA dòng
   │ CP002  Cửa hàng B│  +  │ CP003  Cửa hàng C │  → CP003 chưa có → THÊM mới
   └──────────────────┘     └──────────────────┘
                    ▼ Hudi tự xử lý, KHÔNG cần _TMP/ghi đè cả partition
   ┌──────────────────────────────┐
   │ CP001  Cửa hàng A1   (updated)│
   │ CP002  Cửa hàng B             │
   │ CP003  Cửa hàng C    (inserted)│
   └──────────────────────────────┘
```

> 🧩 So với hiện tại: chính cái mẹo **`_TMP` → Coordinator ghi đè** ở §3 có thể được thay bằng **1 lệnh upsert của Hudi** — gọn hơn, không phải viết lại cả partition.

### Hai kiểu ghi của Hudi (giải thích siêu ngắn)
| Kiểu | Cách làm | Hợp cho |
|---|---|---|
| **CoW** (Copy-on-Write) | Sửa → viết lại **file nhỏ** chứa dòng đó ngay | Đọc nhanh, cập nhật vừa phải |
| **MoR** (Merge-on-Read) | Sửa → ghi vào **file log** trước, gộp lại sau | Ghi/cập nhật **rất nhiều, liên tục** (streaming) |

**Khi nào dùng Hudi:** bảng trạng thái thay đổi liên tục (merchant, tài khoản...), luồng CDC (bắt thay đổi từ DB nguồn), cần cập nhật gần thời gian thực.

---

## 9. So sánh & bảng nào nên dùng loại nào

| Tiêu chí | Parquet/Hive thuần (hiện tại) | **Hudi** | **Iceberg** |
|---|---|---|---|
| Sửa/xoá 1 dòng | ❌ ghi đè cả partition | ✅ **upsert theo khóa** | ✅ (được, nhưng thiên phân tích) |
| Time-travel (xem lại quá khứ) | ❌ | ✅ | ✅ |
| Đổi schema an toàn | ❌ dễ vỡ | ✅ | ✅ **mạnh nhất** |
| Nhiều engine cùng đọc | 🟡 hạn chế | 🟡 khá | ✅ **tốt nhất, chuẩn mở** |
| Hợp nhất cho | dữ liệu bất biến, append + đọc | **cập nhật liên tục / CDC / near-real-time** | **phân tích lớn, ổn định, đa engine** |

### Đề xuất sơ bộ cho SQLWF ⚠️ (định hướng, chốt sau khi rà từng bảng)

| Loại bảng trong SQLWF | Nên dùng | Vì sao |
|---|---|---|
| Bảng append theo ngày, gần như không sửa | **giữ Parquet** | đơn giản, đủ dùng, không cần thêm phức tạp |
| Bảng danh mục / trạng thái hay sửa, cần lịch sử phiên bản | **Hudi** | upsert theo khóa thay cho replace/`_TMP`; hợp cơ chế version đang có |
| Bảng tổng hợp lớn để phân tích/đối soát, cần time-travel + đa engine | **Iceberg** | time-travel phục vụ đối soát/audit; schema evolution; mở đường Trino/Spark |

---

## 10. Trước / Sau khi áp dụng vào SQLWF

**Chặng MERGE (④) hiện tại vs khi có Hudi/Iceberg:**

```
   HIỆN TẠI (Parquet):
   file mới ─► _TMP (bảng tạm) ─► Coordinator GHI ĐÈ cả partition ─► bảng chính
              (2 bước, tốn công, không giữ lịch sử, khó sửa 1 dòng)

   KHI CÓ HUDI/ICEBERG:
   file mới ─────────── UPSERT / MERGE trực tiếp ───────────► bảng chính
              (1 bước; sửa đúng dòng; tự lưu snapshot ⇒ xem lại được)
```

**Lợi ích kéo theo (liên quan các tài liệu sau):**
- **Đối soát / audit:** time-travel cho phép trả lời "số liệu tại thời điểm X là bao nhiêu", rollback khi nạp nhầm.
- **Metadata & Lineage:** table format ghi sẵn commit/snapshot/schema → dễ lấy *freshness* (cập nhật lần cuối khi nào), *thay đổi schema*, phục vụ giám sát sau này.
- **Bớt cơ chế thủ công:** giảm phụ thuộc mẹo `_TMP` + ghi đè.

**Lưu ý khi triển khai** ⚠️ (đề cập để không hiểu nhầm là "bật là xong"):
- Cần engine hỗ trợ (Spark/Flink/Trino…) và cấu hình phù hợp; Hudi cần chọn đúng CoW/MoR theo tải.
- Bảng cũ phải **chuyển đổi (migrate)** sang định dạng mới, không tự động.
- Không nên áp cho *mọi* bảng — chỉ nơi thực sự cần (xem §9).

---

## 11. Từ điển thuật ngữ

| Thuật ngữ | Giải thích 1 câu |
|---|---|
| **HDFS** | "Ổ cứng khổng lồ" ghép nhiều máy, chứa file lớn. |
| **Parquet** | Định dạng file lưu bảng theo cột, nén tốt. |
| **Hive** | Lớp giúp coi thư mục file như "bảng" để query SQL. |
| **Partition** | Chia bảng thành thư mục con theo 1 cột (thường theo ngày) cho nhanh. |
| **Staging / `_TMP`** | Bảng tạm giữ dữ liệu chờ trước khi gộp vào bảng chính. |
| **Coordinator** ⚠️ | Nền chạy job hợp nhất dữ liệu vào bảng chính (cần xác nhận là Oozie hay nền riêng). |
| **Data Lake** | Kho chứa dữ liệu thô/lớn (ở đây là HDFS + Parquet). |
| **Table format** | Lớp "sổ quản lý" trên file (Hudi/Iceberg) thêm tính năng như database. |
| **Lakehouse** | Data Lake + tính năng của Warehouse (nhờ table format). |
| **ACID** | Ghi dữ liệu trọn vẹn, an toàn (không nửa vời). |
| **Upsert** | Update nếu đã có + Insert nếu chưa có (theo khóa). |
| **CDC** | Bắt thay đổi (thêm/sửa/xoá) từ nguồn để đồng bộ tiếp. |
| **Time-travel** | Xem lại bảng ở thời điểm/phiên bản trong quá khứ. |
| **Snapshot** | "Ảnh chụp" trạng thái bảng tại 1 thời điểm (Iceberg). |
| **Schema evolution** | Thêm/đổi cột an toàn, không phá dữ liệu/query cũ. |
| **CoW / MoR** | 2 cách Hudi ghi cập nhật: viết lại file ngay / ghi log gộp sau. |

---

### 📌 Chỗ cần bạn xác nhận (để tôi chốt bản chính xác)
1. **Coordinator** là gì (Oozie? nền tự viết?) và cơ chế merge `_TMP` → bảng chính đúng như mô tả §3 chứ?
2. **HDFS Explorer** nằm ở menu nào, xem được gì (file thô? preview?).
3. Hiện đã có bảng nào là **Hive/Parquet có partition theo ngày** như ví dụ chưa, hay cấu trúc khác?
4. Định hướng Hudi/Iceberg: áp cho **bảng mới** hay **migrate bảng cũ**? Ưu tiên nhóm bảng nào trước?

> Trả lời 4 ý trên, tôi sẽ (a) sửa các chỗ ⚠️ cho khớp thực tế, (b) nếu bạn muốn — chuyển diagram ASCII sang **PlantUML render đẹp** và/hoặc **đẩy Confluence** như bộ SRS.
