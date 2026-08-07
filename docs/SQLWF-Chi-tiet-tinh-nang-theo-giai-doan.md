# SQLWF — CHI TIẾT TÍNH NĂNG THEO GIAI ĐOẠN
### Bản đặc tả mức nghiệp vụ cho từng đầu việc trong lộ trình Data Management

> **Người viết:** Khôi (IT BA) · **Ngày:** 08/2026
> **Tài liệu mẹ:** [SQLWF — Đề xuất Kiến trúc Data Management](./SQLWF-De-xuat-Kien-truc-Data-Management.md)
> **Tham chiếu màn hình:** [SRS Metadata bảng](../metadata-bang/SRS_metadata_bang.md)
>
> **Mục đích bản này:** tài liệu mẹ dừng ở mức "việc gì – ai làm – gỡ rào cản nào". Bản này trả lời tiếp: **trên tool hiển thị như thế nào, người dùng thao tác gì, nhập gì – ra gì, FE/BE đảm nhận phần nào.**
>
> **Không phải tài liệu kỹ thuật.** Mô tả ở mức tính năng để BA/PO hình dung và nghiệm thu được.
> **Ký hiệu:** 🆕 tính năng mới · 🔧 sửa cái đang có · 🏗️ hạ tầng (không có màn hình) · ⚠️ cần xác nhận
>
> 📄 **Đặc tả đầy đủ kiểu SRS cho Giai đoạn 1** — 10 chức năng, quy tắc nghiệp vụ, validation, phân rã công việc BA/FE/BE/QC, kịch bản kiểm thử: xem [SRS Data Management — Giai đoạn 1](./SRS-Data-Management-Giai-doan-1.md).

---

## MỤC LỤC

- [0. Nền tảng cần biết trước](#0-nền-tảng-cần-biết-trước)
- [GIAI ĐOẠN 1 — DỌN NỀN](#giai-đoạn-1--dọn-nền)
  - [1.1 Quy hoạch lại danh mục bảng](#11-quy-hoạch-lại-danh-mục-bảng)
  - [1.2 Dựng Catalog](#12-dựng-catalog)
  - [1.3 Cài thư viện Iceberg vào TaskUtil](#13-cài-thư-viện-iceberg-vào-taskutil)
  - [1.4 Chuyển nhóm bảng thí điểm sang Iceberg](#14-chuyển-nhóm-bảng-thí-điểm-sang-iceberg)
  - [1.5 Thêm "Định dạng bảng" + sửa chỗ sinh câu SQL](#15-thêm-định-dạng-bảng--sửa-chỗ-sinh-câu-sql)
  - [1.6 Khối "Tình trạng dữ liệu"](#16-khối-tình-trạng-dữ-liệu)
- [GIAI ĐOẠN 2 — BẬT DATA QUALITY](#giai-đoạn-2--bật-data-quality)
- [GIAI ĐOẠN 3 — NỐI BA TRỤ](#giai-đoạn-3--nối-ba-trụ)
- [Phụ lục A — Bảng tổng hợp tính năng](#phụ-lục-a--bảng-tổng-hợp-tính-năng)
- [Phụ lục B — Điểm cần chốt](#phụ-lục-b--điểm-cần-chốt)

---
---

# 0. Nền tảng cần biết trước

<details open>
<summary><b>Nền tảng cần biết trước</b></summary>


Ba sự thật về hệ thống hiện tại, quyết định cách thiết kế mọi tính năng bên dưới. Cả ba đều đã đối chiếu mã nguồn.

## 0.1 Màn "Quản lý bảng" hiện có gì

<details open>
<summary><b>Màn "Quản lý bảng" hiện có gì</b></summary>


Chi tiết một bảng gồm **4 khu vực**:

| Khu vực | Nội dung hiện tại |
|---|---|
| **(B) Thông tin chung** | Tên bảng · Mô tả · Domain + Sub domain · DE phụ trách · BDA phụ trách · Tần suất đồng bộ · Tên job · Link nghiệp vụ · Datamart · nút Download Metadata bảng |
| **(A) Business Metadata** | Upload / tải lại 1 file Excel khai báo đồng bộ (chỉ lưu trữ, không bóc tách) |
| **(C) Cấu trúc bảng** | Tab **Schema** (Tên trường · Kiểu · Mô tả · NULLABLE · PK/FK · Phân loại dữ liệu · Tập giá trị · Quy tắc nghiệp vụ · Glossary term) + tab **Sample data** |
| **(D) Quản lý upload** | Lịch sử import · Import Table / Schema / Use Case · tải lại file gốc · file lỗi |

> **Hệ quả thiết kế:** mọi trường metadata mới đề xuất bên dưới đều **gắn vào khu vực (B)** và **phải có mặt trong template Import + Download** — vì với 11.000 bảng, không ai ngồi sửa tay từng bảng.

</details>

## 0.2 SQLWF gọi bảng bằng đường dẫn, không bằng tên

<details open>
<summary><b>SQLWF gọi bảng bằng đường dẫn, không bằng tên</b></summary>


Bảng trong SQLWF được mô tả bằng **3 mảnh ghép**: `Định dạng` + `Vùng lưu trữ (Area)` + `Đường dẫn (Path)`.

Khi cần đọc dữ liệu, hệ thống **ghép 3 mảnh này lại** thành tham chiếu bảng:

```
   type        areaPath                     path
   ─────  ───────────────────────  ──────────────
   parquet . `/storage/business_zone  /  bi/doi_soat_A`
   └──────────────── cái này đi vào câu SQL ────────────────┘
```

Người dùng viết SQL bằng **bí danh** `${TEN_BANG}`, hệ thống thay bí danh bằng chuỗi trên rồi mới gửi sang TaskUtil chạy.

> 🔑 **Đây là điểm mấu chốt của mục 1.5.** Chuyển sang Iceberg = đổi cách ghép mảnh này, vì Iceberg gọi bảng bằng **tên trong catalog** chứ không bằng đường dẫn file.

</details>

## 0.3 Trường "Định dạng bảng" thật ra ĐÃ CÓ trong dữ liệu

<details open>
<summary><b>Trường "Định dạng bảng" thật ra ĐÃ CÓ trong dữ liệu</b></summary>


Bản ghi bảng trong SQLWF đã có sẵn thuộc tính **`type`** với 2 giá trị `parquet` / `csv`. Nhưng:

| | Thực tế |
|---|---|
| Có hiện trên giao diện không? | ❌ **Không** — không màn nào cho xem/sửa |
| Ai đang set giá trị? | Hệ thống tự gán `"parquet"` khi tạo bảng, **cứng trong mã nguồn** |
| Có ảnh hưởng gì không? | ✅ Có — nó chính là mảnh đầu tiên trong chuỗi tham chiếu ở 0.2 |

> 💡 **Tin tốt cho ước lượng:** việc 1.5 **không phải thêm mới một khái niệm**, mà là **đưa một thuộc tính đã có ra giao diện + mở rộng tập giá trị + rẽ nhánh chỗ ghép chuỗi**. Nhẹ hơn nhiều so với hình dung ban đầu.

</details>

</details>

---
---

# GIAI ĐOẠN 1 — DỌN NỀN

<details open>
<summary><b>GIAI ĐOẠN 1 — DỌN NỀN</b></summary>


## 1.1 Quy hoạch lại danh mục bảng

<details open>
<summary><b>Quy hoạch lại danh mục bảng</b></summary>


> **Câu hỏi cần trả lời:** *"Phân loại 11.000 bảng — người dùng có phải thao tác gì trên SQLWF không, hay chỉ ngồi làm Excel?"*
>
> **Trả lời ngắn:** Phải thao tác trên tool, **và tool hiện chưa đủ chỗ để ghi kết quả phân loại**. Cần bổ sung 2 trường + 3 tính năng hỗ trợ.

### 1.1.1 Bản chất công việc

Đây là **việc nghiệp vụ**, không phải việc code: ngồi rà từng nhóm bảng, quyết định bảng nào là bảng chính thức, bảng nào là rác, ai chịu trách nhiệm. Nhưng **kết quả rà soát phải ghi được vào tool**, nếu không thì sau này Data Quality vẫn không biết phải giám sát bảng nào.

### 1.1.2 Tool hiện đã có sẵn một phần

Trước khi đề xuất thêm, cần ghi nhận những gì đã có:

| Thông tin đã có | Dùng được vào việc gì |
|---|---|
| **Trạng thái hoạt động** của bảng | Đã lọc được bảng còn dùng / đã ngừng |
| **Cờ "bảng thuộc template"** — đánh dấu bảng chính và bảng tạm `_TMP` sinh từ luồng import | ✅ **Nhận diện được một phần bảng tạm mà không cần rà tay** |
| **Domain / Sub domain** | Đã nhóm được theo lĩnh vực |
| **DE phụ trách / BDA phụ trách** | Đã có khái niệm người phụ trách |
| **Datamart (có/không)** | Đã phân biệt được bảng phục vụ khai thác |

> ⇒ Việc quy hoạch **không bắt đầu từ số 0**. Phần thiếu là *phân loại bản chất bảng* và *mức độ quan trọng*.

### 1.1.3 🆕 Tính năng A — Thêm 2 trường vào Thông tin chung

**Vị trí:** Quản lý bảng → Chi tiết bảng → mục **Thông tin chung**

| Control | Loại | Bắt buộc | Giá trị | Mô tả |
|---|---|---|---|---|
| **Phân loại bảng** | Dropdown | Không (mặc định trống = *chưa phân loại*) | `Bảng chính thức` · `Bảng tạm` · `Bảng sao chép / backup` · `Bảng ngừng sử dụng` | Trả lời câu hỏi *bảng này có phải bảng thật không* |
| **Mức độ quan trọng** | Dropdown | Không (mặc định trống) | `Trọng yếu` · `Quan trọng` · `Thông thường` · `Không giám sát` | Trả lời câu hỏi *bảng này có cần Data Quality theo dõi không, ở mức nào* |

**Vì sao phải là 2 trường tách rời, không gộp làm một:** một bảng có thể *là bảng chính thức* nhưng *không cần giám sát* (ví dụ bảng danh mục tĩnh ít khi đổi). Gộp lại sẽ mất một chiều thông tin.

**Ai điền:**

| Trường | Ai quyết | Ghi chú |
|---|---|---|
| Phân loại bảng | **DE** — người biết bảng sinh ra từ đâu | Có thể gợi ý sẵn theo cờ "bảng thuộc template" |
| Mức độ quan trọng | **Đơn vị nghiệp vụ + BDA** — người biết bảng nào ra báo cáo cho ai | Không để DE tự quyết, vì đây là câu hỏi nghiệp vụ |

### 1.1.4 🔧 Tính năng B — Đưa 2 trường vào Import + Download

**Đây là phần quan trọng nhất của 1.1.** Không có nó thì quy hoạch 11.000 bảng là bất khả thi.

| Chức năng | Thay đổi |
|---|---|
| **Download Metadata bảng** (đã có) | Thêm 2 cột `Phân loại bảng` · `Mức độ quan trọng` vào phần Thông tin bảng |
| **Import Table** (đã có) | Thêm 2 cột tương ứng vào template; nhận giá trị và ghi vào bảng |

**Luồng làm việc thực tế của BA khi quy hoạch:**

```
① Lọc danh sách bảng theo Domain (VD: nhóm đối soát ~200 bảng)
        ↓
② Bấm Download → được file Excel 200 dòng, đã có sẵn tên bảng, mô tả, BDA/DE phụ trách
        ↓
③ Gửi file cho đơn vị nghiệp vụ điền 2 cột phân loại
        ↓
④ Nhận lại → Import Table → tool ghi vào 200 bảng một lần
        ↓
⑤ Xem lại kết quả bằng bộ lọc "Chưa phân loại" → còn sót thì làm tiếp
```

> ⚠️ **Điểm phải kiểm tra khi làm:** chức năng Import hiện có 2 kiểu ứng xử với ô trống — **ghi đè** (Import Table) và **giữ nguyên giá trị cũ** (Import Schema kiểu PATCH). Với 2 trường phân loại này, phải dùng kiểu **giữ nguyên giá trị cũ**, nếu không mỗi lần import bảng nào đó vì lý do khác sẽ vô tình xoá sạch kết quả phân loại đã làm.

### 1.1.5 🆕 Tính năng C — Bộ lọc và cột mới trên danh sách bảng

**Vị trí:** Quản lý bảng → màn danh sách

| Bổ sung | Nội dung |
|---|---|
| **Bộ lọc** | Thêm 2 ô lọc: `Phân loại bảng` · `Mức độ quan trọng`, mỗi ô có thêm lựa chọn **"Chưa phân loại"** |
| **Cột hiển thị** | Thêm 2 cột tương ứng, hiện dạng nhãn màu để quét mắt nhanh |
| **Chỉ số tiến độ** | Dòng tóm tắt đầu danh sách: *"Đã phân loại 3.204 / 11.087 bảng (28,9%)"* |

> **Vì sao cần chỉ số tiến độ:** quy hoạch 11.000 bảng là việc kéo dài nhiều tháng qua nhiều đơn vị. Không có con số tiến độ thì không ai biết đang ở đâu, và lãnh đạo không có gì để theo dõi.

### 1.1.6 🆕 Tính năng D — Màn "Rà soát danh mục bảng"

**Vị trí:** menu mới trong nhóm Quản lý bảng
**Người dùng:** BA / DE, chạy định kỳ (đề xuất hằng tuần)

Màn này **đối chiếu khai báo trong SQLWF với thực tế trên HDFS** và liệt kê những chỗ lệch:

| Nhóm bất thường | Nghĩa là | Việc cần làm |
|---|---|---|
| **Bảng "ma"** | Có khai báo trong SQLWF nhưng **không tìm thấy thư mục dữ liệu** | Xoá khai báo hoặc đánh dấu Ngừng sử dụng |
| **Dữ liệu "mồ côi"** | Có thư mục dữ liệu trên HDFS nhưng **không có bảng nào khai báo** | Khai báo bổ sung hoặc dọn dẹp |
| **Bảng chết** | Có khai báo, có thư mục, nhưng **không có dữ liệu mới quá N ngày** | Xác nhận còn dùng không |
| **Bảng chưa có người phụ trách** | Không khai DE hoặc BDA phụ trách | Gán BDA / DE phụ trách |
| **Bảng chưa phân loại** | Trống 1 trong 2 trường ở 1.1.3 | Phân loại tiếp |

**Thao tác trên màn:**

| Control | Hành vi |
|---|---|
| Ô chọn khoảng ngày "bảng chết" | Mặc định 30 ngày, cho sửa |
| Nút **Quét lại** | Chạy đối chiếu, hiện thanh tiến trình |
| Bảng kết quả | Mỗi dòng: tên bảng · nhóm bất thường · đường dẫn · lần ghi cuối · BDA/DE phụ trách |
| Nút **Xuất Excel** | Xuất danh sách để gửi đơn vị nghiệp vụ xử lý |
| Nút **Đánh dấu hàng loạt** | Chọn nhiều dòng → gán Phân loại / Mức độ quan trọng / BDA-DE phụ trách một lần |

> **Sau khi có Iceberg (mục 1.4), màn này chính xác hơn nhiều:** "lần ghi cuối" lấy từ nhật ký ghi của Iceberg thay vì đoán qua tên thư mục.

### 1.1.7 Đầu vào — đầu ra của 1.1

| | Nội dung |
|---|---|
| **Đầu vào** | Danh sách ~11.000 bảng đang có · kiến thức nghiệp vụ của các đơn vị |
| **Người thao tác** | BA chủ trì · DE điền phân loại · đơn vị nghiệp vụ điền mức độ quan trọng |
| **Đầu ra** | Mỗi bảng có đủ: phân loại · mức độ quan trọng · BDA phụ trách + DE phụ trách · domain |
| **Nghiệm thu bằng** | Chỉ số *"đã phân loại X%"* trên màn danh sách; màn Rà soát không còn nhóm "Chưa có chủ" trong phạm vi đã cam kết |

</details>

---

## 1.2 Dựng Catalog

<details open>
<summary><b>Dựng Catalog</b></summary>


**🏗️ Phần lớn là hạ tầng — không có màn hình mới**, nhưng màn chi tiết bảng **có thêm 2 trường hiển thị**.

### 1.2.1 Catalog là gì, dưới góc nhìn người dùng tool

Hiện SQLWF định danh bảng bằng **đường dẫn thư mục**. Catalog cho phép định danh bằng **tên có cấu trúc**:

```
   Hôm nay:   /storage/business_zone/bi/doi_soat_A     ← đường dẫn
   Có Catalog: bi.doi_soat_A                            ← tên bảng
               └┬┘ └────┬────┘
             không gian   tên bảng
              tên (db)
```

Cần tách bạch 2 chuyện, vì rất dễ lẫn:

| | Có đổi không |
|---|---|
| **Người dùng NHÌN THẤY gì** | ✅ **Có đổi** — màn chi tiết bảng hiện thêm tên định danh trong Catalog, VD `bi.doi_soat_A` (xem 1.2.2) |
| **Người dùng PHẢI LÀM gì khác không** | ❌ **Không đổi** — vẫn chọn bảng từ danh sách, vẫn viết SQL bằng bí danh `${TÊN_BẢNG}`. **Không ai phải học gõ tên catalog** |

Nói cách khác: tên catalog là **thông tin để tra cứu và đối chiếu**, không phải thứ người dùng phải nhập.

### 1.2.2 🆕 Thay đổi trên tool

| Thay đổi | Vị trí | Mô tả |
|---|---|---|
| Thêm 2 trường **chỉ đọc** | Thông tin chung | `Không gian tên (Namespace)` và `Tên bảng trong Catalog` — hệ thống tự sinh, người dùng **không sửa được** |
| Hiển thị có điều kiện | Thông tin chung | Chỉ hiện khi bảng đã đăng ký Catalog; chưa đăng ký thì hiện *"Chưa đăng ký Catalog"* |

**Vì sao chỉ đọc:** tên trong catalog phải khớp tuyệt đối với tên đã đăng ký ở tầng hạ tầng. Cho sửa tay = sinh ra lệch, và lệch kiểu này **không báo lỗi ngay** mà chỉ làm câu SQL chạy sai về sau.

### 1.2.3 Đầu vào — đầu ra

| | Nội dung |
|---|---|
| **Đầu vào** | Quyết định chọn loại Catalog (⚠️ tận dụng Hive Metastore sẵn có hay dựng mới — cần đội hạ tầng xác nhận) |
| **Người thao tác** | Đội hạ tầng dựng · Team tool bổ sung 2 trường hiển thị |
| **Đầu ra** | Mỗi bảng đã chuyển đổi có một tên định danh duy nhất, dùng chung cho cả 3 trụ |
| **Người dùng cuối thấy gì** | Ở mục Thông tin chung của bảng, thấy thêm dòng **Tên bảng trong Catalog: `bi.doi_soat_A`** (chỉ đọc). Ngoài ra **cách làm việc không đổi** — không phải học thêm thao tác nào |
| **Nghiệm thu bằng** | Mở 1 bảng đã chuyển: thấy tên catalog hiển thị đúng · mở 1 bảng chưa chuyển: hiện *"Chưa đăng ký Catalog"* |

</details>

---

## 1.3 Cài thư viện Iceberg vào TaskUtil

<details open>
<summary><b>Cài thư viện Iceberg vào TaskUtil</b></summary>


**🏗️ Hạ tầng thuần — không có bất kỳ màn hình nào.**

| | Nội dung |
|---|---|
| **Việc làm** | Nạp thư viện Iceberg vào dịch vụ chạy SQL (TaskUtil), cấu hình trỏ tới Catalog |
| **Người thao tác** | Đội hạ tầng |
| **Trạng thái** | ✅ Đã xác nhận khả thi |
| **Nghiệm thu bằng** | Chạy thử một câu SQL đọc bảng Iceberg qua đúng đường TaskUtil hiện tại, trả về kết quả |
| **Người dùng cuối thấy gì** | Không thấy gì |

> **Điểm đáng mừng đã kiểm chứng:** bộ phân tích câu lệnh SQL mà SQLWF đang dùng (để chặn cú pháp nguy hiểm, để phát hiện bảng bị ảnh hưởng) **đã hiểu sẵn** cú pháp riêng của Iceberg như `FOR TIMESTAMP AS OF`, `MERGE INTO`. Không phải sửa tầng kiểm tra SQL.

</details>

---

## 1.4 Chuyển nhóm bảng thí điểm sang Iceberg

<details open>
<summary><b>Chuyển nhóm bảng thí điểm sang Iceberg</b></summary>


### 1.4.1 "Chuyển bảng sang Iceberg" thực chất là làm gì

#### a) Không phải đổi dữ liệu — mà là lập sổ cho dữ liệu

Nhớ lại ví von ở tài liệu mẹ: **Parquet = những trang giấy rời** ghi số liệu · **Iceberg = quyển sổ mục lục + nhật ký** kẹp cùng xấp giấy đó.

Vậy "chuyển bảng sang Iceberg" = **lập quyển sổ cho xấp giấy đang có**. Xấp giấy (file dữ liệu) không bị vứt đi, không đổi định dạng.

**Trên HDFS, trước và sau:**

```
   TRƯỚC                                    SAU
   /storage/.../doi_soat_A/                 /storage/.../doi_soat_A/
   │                                        │
   └── PARTITION_DATE=20260801/             ├── data/                    ← file cũ, Y NGUYÊN
       └── part-00000.parquet               │   └── PARTITION_DATE=20260801/
       └── part-00001.parquet               │       └── part-00000.parquet
   └── PARTITION_DATE=20260802/             │       └── part-00001.parquet
       └── part-00000.parquet               │   └── PARTITION_DATE=20260802/
                                            │       └── part-00000.parquet
                                            │
                                            └── metadata/               ← ★ MỚI MỌC RA
                                                ├── v1.metadata.json     cấu trúc bảng
                                                ├── snap-4821....avro    ảnh chụp mỗi lần ghi
                                                └── 4821...-m0.avro      thống kê từng file:
                                                                          số dòng, số ô trống
                                                                          theo từng cột
```

> **Chỉ mọc thêm thư mục `metadata/`.** Dữ liệu cũ không mất, không phải chuyển sang định dạng file khác.

#### b) Ví dụ cụ thể — chuyển bảng `DOI_SOAT_DOI_TAC_A`

> 🧩 **Giả định:** bảng đối soát, phân vùng theo ngày, đang có 90 ngày dữ liệu ≈ 40 triệu dòng ≈ 25 GB. Mỗi sáng 06:00 có 1 job ETL ghi thêm dữ liệu ngày hôm trước.

| Bước | Ai làm | Việc | Thời gian ⚠️ |
|---|---|---|---|
| **B0** | DE + BA | Kiểm tra schema bảng có sạch không (kiểu dữ liệu khai đúng chưa), chốt cửa sổ dừng job | 1 ngày |
| **B1** | Hạ tầng | Đăng ký bảng vào Catalog → sinh ra tên định danh `bi.doi_soat_doi_tac_a` | vài phút |
| **B2** | Hạ tầng | **Tạo quyển sổ Iceberg** cho dữ liệu đang có — 2 cách, xem phần (c) | phút → giờ |
| **B3** | DE + BA | **Đối chiếu:** đếm số dòng bảng cũ và bảng Iceberg xem có khớp không; chạy thử vài câu SQL nghiệp vụ so kết quả | vài giờ |
| **B4** | Team tool / DE | Vào SQLWF, đổi trường **Định dạng bảng** từ `Parquet` → `Iceberg` | vài giây |
| **B5** | DE | Sửa job ETL 06:00 để ghi vào bảng Iceberg thay vì ghi đè thư mục Parquet | nửa ngày |
| **B6** | DE + BA | Theo dõi 3–5 ngày: job chạy có ra snapshot mới không, số liệu có khớp không. **Giữ bản sao dữ liệu cũ** làm dự phòng, sau đó mới dọn | 1 tuần |

**Kết quả người dùng nhìn thấy sau B6:**

```
  TRƯỚC (bảng Parquet)                    SAU (bảng Iceberg)
  ┌──────────────────────────┐            ┌──────────────────────────────────┐
  │ Chi tiết bảng            │            │ Chi tiết bảng                    │
  │  Tên: DOI_SOAT_DOI_TAC_A │            │  Tên: DOI_SOAT_DOI_TAC_A         │
  │  Định dạng: (không hiện) │            │  Định dạng: Iceberg  🟢          │
  │                          │            │  Catalog: bi.doi_soat_doi_tac_a  │
  │  [không có gì thêm]      │            │                                  │
  │                          │            │  📊 TÌNH TRẠNG DỮ LIỆU           │
  │                          │            │   Cập nhật lần cuối: 06:15 hôm nay│
  │                          │            │   Số dòng: 40.128.554            │
  │                          │            │   Số lần ghi hôm nay: 1          │
  │                          │            │                                  │
  │                          │            │  🕐 Xem lại số liệu ngày ...     │
  └──────────────────────────┘            └──────────────────────────────────┘
```

#### c) Bước B2 có 2 cách làm — khác nhau rất nhiều

| | **Cách nhanh** — lập sổ cho giấy sẵn có | **Cách chuẩn** — chép lại sang sổ mới |
|---|---|---|
| **Làm gì** | Giữ nguyên file Parquet đang có, chỉ **sinh thư mục `metadata/`** liệt kê các file đó | **Đọc toàn bộ dữ liệu cũ, ghi lại** thành bảng Iceberg mới |
| **Thời gian** (ví dụ 25 GB) | **Vài phút** — không đọc dữ liệu | **Vài giờ** — phải đọc và ghi lại toàn bộ |
| **Dung lượng cần** | Không tốn thêm | **Gấp đôi tạm thời** (cũ + mới cùng tồn tại) |
| **Kiểu dữ liệu** | 🔴 **Giữ nguyên như cũ.** Cột số đang lưu dạng chữ thì vẫn là chữ | ✅ **Ép về đúng kiểu khai báo** |
| **File vụn** | Giữ nguyên (bảng nhiều file nhỏ vẫn nhiều file nhỏ) | ✅ Gộp lại, đọc nhanh hơn |
| **Rủi ro** | Thấp | Có thể **lỗi hàng loạt** nếu dữ liệu không ép được kiểu |

> ### 🔑 Vì sao chi tiết này quan trọng với nghiệp vụ
>
> Rủi ro số 4 trong tài liệu mẹ đã nêu: **toàn bộ cột nạp qua đường Upload hiện đang lưu dưới dạng chữ**, bất kể khai báo kiểu gì.
>
> Nếu chọn **Cách nhanh**, bảng vẫn là "chữ hết" → mất một phần lợi ích: thống kê *giá trị nhỏ nhất / lớn nhất theo cột* mà Iceberg cho sẵn sẽ **vô nghĩa** (so sánh chữ chứ không so sánh số), và các kiểm tra Data Quality dựa trên đó cũng vô nghĩa theo.
>
> **Đề xuất:** nhóm thí điểm dùng **Cách chuẩn** — chậm hơn nhưng lộ hết vấn đề kiểu dữ liệu ngay từ đầu, trên phạm vi nhỏ còn xử lý được. Để đến lúc mở rộng ra hàng nghìn bảng mới phát hiện thì rất khó quay lại.

> 📄 **Ví dụ chạy thử cả 2 cách trên một bảng mẫu**, kèm số liệu cụ thể cho thấy Cách nhanh trả về min/max sai như thế nào: xem [Ví dụ thực hành — Chuyển một bảng sang Iceberg](./SQLWF-Vi-du-chuyen-doi-bang-sang-Iceberg.md).

#### d) Vì sao gọi là "việc một lần cho mỗi bảng"

Sau khi bảng đã chuyển xong (qua B6):

| Từ đó về sau | Ai làm | Có phải thao tác gì không |
|---|---|---|
| Job ETL ghi dữ liệu hằng ngày | Tự động | ❌ Không — mỗi lần ghi, Iceberg **tự sinh snapshot mới**, tự cập nhật thống kê |
| Người dùng xem tình trạng dữ liệu | Người dùng | Chỉ bấm nút Cập nhật, không liên quan việc chuyển đổi |
| Người dùng xem lại số liệu quá khứ | Người dùng | Chọn thời điểm, không liên quan việc chuyển đổi |
| Chuyển đổi lại | — | ❌ **Không bao giờ phải làm lại** cho bảng đó |

⇒ Toàn bộ quy trình 6 bước ở trên **chỉ chạy đúng một lần cho mỗi bảng**, rồi thôi. Đó là lý do **không cần xây một màn hình cho người dùng bấm** — với vài chục bảng thí điểm, DE chạy tay là đủ. Chỉ khi mở rộng ra hàng trăm bảng thì mới đáng cân nhắc làm chức năng trong tool (xem 1.4.2).

#### e) Trong lúc chuyển đổi thì bảng có dùng được không

| Giai đoạn | Người dùng truy vấn bảng được không |
|---|---|
| B1–B2 (lập sổ) | ✅ Được — dữ liệu cũ vẫn nguyên |
| B3 (đối chiếu) | ✅ Được |
| **B4 (đổi Định dạng bảng)** | ⚠️ **Cần vài phút gián đoạn** — trước khi đổi thì tool đọc kiểu cũ, sau khi đổi thì đọc kiểu mới. Nên làm ngoài giờ cao điểm |
| B5 (sửa job) | ✅ Được — nhưng **phải dừng job trong lúc sửa**, nếu không job cũ ghi đè lên bảng mới |

> ⚠️ **Điểm phải nhắc DE:** B4 và B5 phải làm **liền nhau**. Nếu đổi Định dạng bảng (B4) mà chưa sửa job (B5), sáng hôm sau job cũ vẫn chạy theo cách ghi đè thư mục Parquet → **dữ liệu ghi vào một nơi, tool đọc ở một nơi khác**, và không có gì báo lỗi.

### 1.4.2 Hai cách làm — cần chọn

| | Cách 1: Script ngoài tool | Cách 2: Chức năng trong tool |
|---|---|---|
| **Cách làm** | DE chạy script chuyển đổi, sau đó vào SQLWF sửa trường Định dạng bảng | Màn "Chuyển đổi định dạng bảng" — chọn bảng, bấm Chuyển đổi, tool điều phối |
| **Ưu** | Nhanh, không tốn công xây | Có lịch sử, có kiểm soát, người không phải DE cũng làm được |
| **Nhược** | Không có vết ai chuyển bảng nào lúc nào; dễ quên bước sửa metadata → **tool và thực tế lệch nhau** | Tốn công xây một màn dùng vài chục lần rồi thôi |
| **Đề xuất** | ✅ **Dùng cho giai đoạn thí điểm** (vài chục bảng) | Cân nhắc ở GĐ 2 khi mở rộng ra hàng trăm bảng |

> ⚠️ **Rủi ro của Cách 1 phải nói rõ:** nếu DE chuyển dữ liệu xong mà quên đổi trường Định dạng bảng trong SQLWF, tool vẫn sinh câu SQL kiểu cũ → **truy vấn lỗi hoặc trả sai dữ liệu**. Cần một bước kiểm tra đối chiếu sau khi chuyển (dùng màn Rà soát ở 1.1.6).

### 1.4.3 Đầu vào — đầu ra

| | Nội dung |
|---|---|
| **Đầu vào** | Danh sách nhóm bảng thí điểm (đề xuất: **nhóm đối soát**) |
| **Người thao tác** | Đội hạ tầng + DE |
| **Đầu ra** | Nhóm bảng thí điểm chạy Iceberg, đã đăng ký Catalog, đã cập nhật Định dạng bảng trong SQLWF |
| **Nghiệm thu bằng** | Người dùng mở màn bảng thấy khối "Tình trạng dữ liệu" có số liệu thật (mục 1.6) |

> ⚠️ **Rủi ro kỹ thuật đã biết:** toàn bộ cột dữ liệu nạp qua đường Upload hiện **lưu dưới dạng chữ**, bất kể khai báo kiểu gì. Iceberg **ép kiểu chặt** ngay lúc ghi → chuyển đổi có thể lỗi hàng loạt. Phải chọn nhóm bảng thí điểm có schema sạch, hoặc bổ sung bước ép kiểu lúc nạp.

</details>

---

## 1.5 Thêm "Định dạng bảng" + sửa chỗ sinh câu SQL

<details open>
<summary><b>Thêm "Định dạng bảng" + sửa chỗ sinh câu SQL</b></summary>


> **Câu hỏi cần trả lời:** *"Cụ thể FE làm gì, BE làm gì?"*
>
> Đây là hạng mục có ảnh hưởng dây chuyền rộng nhất trong GĐ 1. Chia làm 4 phần.

### 1.5.1 Hiện trạng chính xác

| | Thực tế |
|---|---|
| Trường "định dạng" | **Đã tồn tại** trong dữ liệu bảng, giá trị `parquet` / `csv` |
| Hiện trên giao diện | ❌ Không màn nào |
| Ai gán giá trị | Hệ thống tự gán `"parquet"`, cứng trong mã nguồn |
| Dùng vào đâu | Là **mảnh đầu tiên** trong chuỗi tham chiếu bảng gửi xuống TaskUtil |

### 1.5.2 🆕 Phần FE — Đưa trường ra giao diện

**(a) Màn chi tiết bảng — mục Thông tin chung**

| Control | Loại | Bắt buộc | Mặc định | Hành vi |
|---|---|---|---|---|
| **Định dạng bảng** | Dropdown | Có | `Parquet` | 4 giá trị: `Parquet` · `CSV` · `Iceberg` · `Hudi`.<br>**Giai đoạn đầu chỉ mở 3 giá trị đầu**, Hudi để sẵn nhưng khoá (xám) |

**Quy tắc hiển thị / cho sửa:**

| Tình huống | Ứng xử |
|---|---|
| Tạo bảng mới | Cho chọn tự do trong các giá trị đang mở |
| Sửa bảng đã có dữ liệu | **Khoá, chỉ đọc** — kèm dòng chú thích *"Đổi định dạng phải thực hiện qua quy trình chuyển đổi dữ liệu, liên hệ DE"* |
| Bảng chưa chuyển Catalog mà chọn Iceberg | Chặn lưu, báo *"Bảng chưa đăng ký Catalog, chưa thể dùng định dạng Iceberg"* |

> **Vì sao khoá khi đã có dữ liệu:** đổi giá trị này **không chuyển đổi dữ liệu**, nó chỉ đổi cách hệ thống sinh câu SQL. Người dùng đổi nhầm = tool đọc bảng bằng cách sai, không báo lỗi rõ ràng. Đây là loại lỗi rất khó truy.

**(b) Màn danh sách bảng**

| Bổ sung | Nội dung |
|---|---|
| Cột **Định dạng** | Nhãn màu: `Parquet` (xám) · `CSV` (xám) · `Iceberg` (xanh) |
| Bộ lọc **Định dạng** | Để theo dõi tiến độ chuyển đổi |
| Chỉ số tiến độ | *"Đã chuyển Iceberg: 48 / 11.087 bảng"* |

**(c) Import / Download**

Thêm cột `Định dạng bảng` vào template Import Table và file Download Metadata — nhưng ⚠️ **cột này ở Import nên để chỉ đọc / bỏ qua giá trị nhập**, tránh việc import hàng loạt vô tình đổi định dạng bảng đang có dữ liệu. Cần chốt → [Phụ lục B](#phụ-lục-b--điểm-cần-chốt).

### 1.5.3 🔧 Phần BE — Rẽ nhánh chỗ sinh tham chiếu bảng

Đây là **thay đổi lõi**. Hiện hệ thống ghép 3 mảnh thành một chuỗi duy nhất. Sau khi sửa, việc ghép **rẽ theo định dạng**:

| Định dạng | Tham chiếu sinh ra | Ghi chú |
|---|---|---|
| `Parquet` / `CSV` | `` parquet.`{đường dẫn Area}/{Path}` `` | **Y nguyên như hiện tại** |
| `Iceberg` | `{tên catalog}.{namespace}.{tên bảng}` | Mới — lấy từ 2 trường ở mục 1.2.2 |

**Chỗ nào gọi tới việc ghép này thì tự động đúng theo:**

| Chức năng | Ứng xử sau khi sửa |
|---|---|
| Xem dữ liệu mẫu (Sample data) | ✅ Tự đúng — vốn đã dùng bí danh `${TÊN_BẢNG}` |
| SQL Query người dùng gõ | ✅ Tự đúng — cùng cơ chế bí danh |
| Job ETL | ✅ Tự đúng nếu job viết bằng bí danh · ⚠️ **sai nếu job hardcode đường dẫn** — cần rà |
| Export / Delivery | ✅ Tự đúng |

### 1.5.4 🔴 Phần rủi ro — 3 tính năng có thể "âm thầm chết"

**Đây là phần BA phải nắm kỹ nhất**, vì các lỗi này **không báo lỗi** — hệ thống vẫn chạy, chỉ là không còn làm đúng việc.

| # | Tính năng | Đang hoạt động thế nào | Chuyện gì xảy ra khi bảng chuyển sang Iceberg |
|---|---|---|---|
| **1** | **Cảnh báo SQL ảnh hưởng** — khi ai đó chạy câu lệnh động tới bảng nào đó, hệ thống nhận diện bảng bị ảnh hưởng để cảnh báo | So khớp câu SQL với chuỗi `` parquet.`đường dẫn` `` | Bảng Iceberg trong câu SQL viết dưới dạng **tên catalog**, không khớp mẫu cũ → **không nhận ra bảng nào bị ảnh hưởng → không cảnh báo ai cả**. Hệ thống không báo lỗi |
| **2** | **Phân quyền theo mẫu đường dẫn** — quyền cấp theo đường dẫn thư mục HDFS | So khớp đường dẫn | Câu SQL không còn chứa đường dẫn → **luật phân quyền có thể không khớp**. Hoặc chặn oan, hoặc **cho qua cái đáng lẽ phải chặn** — trường hợp sau nguy hiểm hơn nhiều |
| **3** | **Data Lineage** — vẽ quan hệ bảng nguồn → bảng đích | Nhận diện bảng trong câu SQL | Bảng Iceberg không được nhận ra → **đứt mắt xích trong sơ đồ lineage** |

**Cách xử lý — phải làm cùng lúc, không để sau:**

Việc nhận diện bảng trong câu SQL phải chuyển từ *"so khớp chuỗi đường dẫn"* sang *"tra danh mục bảng"* — tức là hệ thống hỏi Catalog **"chuỗi này ứng với bảng nào"** thay vì tự đoán bằng cách so văn bản. Sau khi sửa, cả 3 tính năng trên nhận ra bảng bất kể nó được viết dưới dạng đường dẫn hay tên catalog.

> ⚠️ **Đây là lý do mục 1.2 (Catalog) phải làm TRƯỚC mục 1.5**, không làm song song.

### 1.5.5 Đầu vào — đầu ra

| | Nội dung |
|---|---|
| **Người thao tác** | BDA/DE chọn định dạng khi tạo bảng mới; các trường hợp còn lại là hệ thống tự dùng |
| **Đầu vào** | Giá trị Định dạng bảng của từng bảng |
| **Đầu ra** | Câu SQL gửi xuống TaskUtil đúng theo định dạng của bảng |
| **Nghiệm thu bằng** | (1) Bảng Parquet cũ chạy y như trước — **không hồi quy**<br>(2) Bảng Iceberg thí điểm: xem dữ liệu mẫu, chạy SQL Query, export đều ra kết quả<br>(3) **Cảnh báo SQL, phân quyền, lineage vẫn nhận ra bảng Iceberg** — phải test riêng 3 cái này |

</details>

---

## 1.6 Khối "Tình trạng dữ liệu"

<details open>
<summary><b>Khối "Tình trạng dữ liệu"</b></summary>


> Đây là **tính năng đầu tiên người dùng nhìn thấy được** từ toàn bộ GĐ 1. Quan trọng về mặt thuyết phục: chứng minh việc dọn nền có sản phẩm, không phải làm mãi không ra gì.

### 1.6.1 Hiển thị gì

**Vị trí:** Quản lý bảng → Chi tiết bảng → khối mới, đặt ngay dưới mục Thông tin chung

```
  ┌────────────────────────────────────────────────────────────────┐
  │  📊  TÌNH TRẠNG DỮ LIỆU                    [🔄 Cập nhật]        │
  ├────────────────────────────────────────────────────────────────┤
  │  Cập nhật lần cuối    06:15 hôm nay  (2 giờ trước)              │
  │  Số dòng              1.204.331                                 │
  │  Dung lượng           842 MB                                    │
  │  Số lần ghi hôm nay   3 lần                                     │
  │  Thao tác gần nhất    Ghi thêm — 12.043 dòng                    │
  ├────────────────────────────────────────────────────────────────┤
  │  Số liệu đọc lúc 08:20 · 03/08/2026                             │
  └────────────────────────────────────────────────────────────────┘
```

| Chỉ số | Ý nghĩa với người dùng | Nguồn |
|---|---|---|
| **Cập nhật lần cuối** | *"Bảng này có dữ liệu mới chưa?"* — câu hỏi số 1 người dùng hay hỏi | Nhật ký ghi của Iceberg |
| **Số dòng** | Quy mô bảng, và là căn cứ so sánh với hôm qua | Thống kê sẵn trong sổ Iceberg |
| **Dung lượng** | Theo dõi phình dữ liệu | nt |
| **Số lần ghi hôm nay** | Job chạy mấy lần rồi — phát hiện job chạy lặp | nt |
| **Thao tác gần nhất** | Ghi thêm / ghi đè / xoá, kèm số dòng thay đổi | nt |

> 🔑 **Điểm cốt lõi:** 5 chỉ số này **không phải quét dữ liệu để tính**. Iceberg đã ghi sẵn khi job ghi dữ liệu; tool chỉ đọc ra. Với bảng 1,2 triệu dòng, lấy các con số này gần như tức thì.

### 1.6.2 Cách hoạt động — bám theo cơ chế đã có sẵn

Tính năng **Xem dữ liệu mẫu (Sample data)** hiện tại đã chạy đúng mô hình cần dùng lại:

```
 Người dùng bấm Cập nhật
        ↓
 FE gọi BE → BE trả ngay "Đã tiếp nhận yêu cầu"        ← KHÔNG bắt chờ
        ↓
 BE gửi câu SQL đọc sổ Iceberg xuống TaskUtil (chạy nền)
        ↓
 Có kết quả → BE lưu vào bộ nhớ đệm
        ↓
 FE hiển thị số liệu + dòng "Số liệu đọc lúc ..."
```

| Đặc điểm | Lý do |
|---|---|
| **Không chạy đồng bộ** | Không để người dùng ngồi chờ vòng quay |
| **Có bộ nhớ đệm** | Mở lại màn bảng thì hiện ngay số liệu lần trước, không phải chạy lại |
| **Chặn bấm trùng** | Đang có yêu cầu chạy mà bấm nữa → báo *"Đã có yêu cầu trước đó"* (giống Sample data hiện tại) |
| **Luôn ghi rõ thời điểm đọc** | Người dùng biết số liệu đang xem cũ hay mới |

### 1.6.3 Điều kiện hiển thị

| Định dạng bảng | Hiển thị |
|---|---|
| **Iceberg** | Hiện đầy đủ 5 chỉ số |
| **Parquet / CSV** | ⚠️ Cần chốt → [Phụ lục B](#phụ-lục-b--điểm-cần-chốt). Hai lựa chọn: (a) ẩn hẳn khối, (b) hiện khối kèm dòng *"Bảng chưa chuyển sang định dạng có quản lý — chưa lấy được tình trạng dữ liệu"* |

> **Nghiêng về (b):** người dùng nhìn thấy sự khác biệt giữa bảng đã chuyển và chưa chuyển sẽ tạo động lực chuyển đổi. Ẩn hẳn thì không ai biết là có tính năng này.

### 1.6.4 Đầu vào — đầu ra

| | Nội dung |
|---|---|
| **Người thao tác** | Mọi người dùng có quyền xem chi tiết bảng |
| **Đầu vào** | Không có — chỉ 1 nút Cập nhật |
| **Đầu ra** | 5 chỉ số + thời điểm đọc |
| **Nghiệm thu bằng** | Mở 1 bảng thí điểm: chạy job ghi dữ liệu → bấm Cập nhật → thấy "Cập nhật lần cuối" đổi đúng thời điểm job vừa chạy, số dòng tăng đúng |

</details>

</details>

---
---

# GIAI ĐOẠN 2 — BẬT DATA QUALITY

<details open>
<summary><b>GIAI ĐOẠN 2 — BẬT DATA QUALITY</b></summary>


> GĐ 2 phần lớn nằm ở **tool DQ đứng riêng** (bản demo đã có). Phần trên SQLWF chỉ có 2 hạng mục — nhưng là 2 hạng mục người dùng cảm nhận rõ nhất.

## 2.1 🔧 Bổ sung tầng "chỉ đọc metadata" cho 8 loại kiểm tra

<details open>
<summary><b>🔧 Bổ sung tầng "chỉ đọc metadata" cho 8 loại kiểm tra</b></summary>


**Nơi làm:** tool DQ · **Người dùng thấy:** cách cấu hình kiểm tra đổi

Trong 29 loại kiểm tra của bản demo, có 8 loại vốn phải **quét cả bảng** để tính, nay chuyển sang **đọc sổ Iceberg**:

| Loại kiểm tra | Trước | Sau |
|---|---|---|
| Số dòng · Dung lượng bảng · Tỉ lệ trống theo cột · Giá trị nhỏ nhất/lớn nhất | Quét cả bảng | Đọc sổ |
| Biến động khối lượng so kỳ trước | Quét 2 kỳ | So 2 ảnh chụp |
| Độ tươi dữ liệu · Đúng giờ (SLA) | Đoán qua tên thư mục | Thời điểm ghi thật |
| Kiểu dữ liệu đúng chuẩn | Quét cả bảng | Không cần kiểm — định dạng ép kiểu ngay lúc ghi |

**🆕 Thay đổi trên giao diện cấu hình DQ:** mỗi loại kiểm tra hiện thêm nhãn **Tầng 0** (đọc sổ, nhẹ) hoặc **Tầng 1** (quét dữ liệu, nặng), kèm chú thích *"Áp dụng được cho toàn bộ bảng"* / *"Chỉ nên áp cho bảng trọng yếu"*.

> **Vì sao người dùng cần thấy nhãn này:** người cấu hình DQ phải tự biết mình đang bật thứ nặng hay nhẹ. Không có nhãn, họ bật 29 loại cho 11.000 bảng và hệ thống sập.

</details>

## 2.2 🆕 Triển khai Tầng 0 diện rộng + Tầng 1 nhóm trọng yếu

<details open>
<summary><b>🆕 Triển khai Tầng 0 diện rộng + Tầng 1 nhóm trọng yếu</b></summary>


**Đây là chỗ kết quả của mục 1.1 được dùng tới:**

| Phạm vi | Lấy từ đâu | Kiểm tra gì |
|---|---|---|
| **Tầng 0 — toàn bộ bảng đã quy hoạch** | Bảng có `Phân loại = Bảng chính thức` | 8 loại đọc sổ |
| **Tầng 1 — nhóm trọng yếu** | Bảng có `Mức độ quan trọng = Trọng yếu` | Thêm 21 loại quét dữ liệu |

> ⇒ Nếu GĐ 1 không phân loại xong, GĐ 2 **không có căn cứ để chọn bảng nào chạy gì**. Đây chính là chỗ "làm nền trước" thể hiện giá trị cụ thể.

</details>

## 2.3 🆕 Đưa điểm chất lượng về màn Quản lý bảng SQLWF

<details open>
<summary><b>🆕 Đưa điểm chất lượng về màn Quản lý bảng SQLWF</b></summary>


**Vị trí:** ngay dưới khối "Tình trạng dữ liệu" ở mục 1.6

```
  ┌────────────────────────────────────────────────────────────────┐
  │  ✅  CHẤT LƯỢNG DỮ LIỆU                                         │
  ├────────────────────────────────────────────────────────────────┤
  │  Điểm chất lượng      94 / 100        🟢                        │
  │  Kiểm tra đạt         27 / 29                                   │
  │  Sự cố đang mở        1  ⚠️  Tỉ lệ trống cột ma_tinh vượt ngưỡng│
  │  Đánh giá lúc         06:30 hôm nay                             │
  │                                        [Xem chi tiết trên DQ →] │
  └────────────────────────────────────────────────────────────────┘
```

| Yếu tố | Mô tả |
|---|---|
| **Điểm chất lượng** | 1 con số 0–100 kèm màu (🟢 ≥90 · 🟡 70–89 · 🔴 <70) |
| **Kiểm tra đạt** | Bao nhiêu trên tổng số |
| **Sự cố đang mở** | Số lượng + tiêu đề sự cố nghiêm trọng nhất |
| **Nút Xem chi tiết** | Mở sang tool DQ đúng trang của bảng này |

> ### 🔴 Đây là hạng mục quan trọng nhất GĐ 2 về mặt cảm nhận người dùng
>
> Về khối lượng code thì nhỏ — chỉ là hiển thị thêm một khối. Nhưng nó là thứ **đổi hẳn trải nghiệm**: hôm nay người dùng mở bảng ra không biết số liệu có tin được không; sau việc này thì biết ngay, **ở đúng chỗ họ vốn đã vào hằng ngày**, không phải mở thêm cổng nào.
>
> Hiện tích hợp giữa 2 hệ thống đang **một chiều** — tool DQ kéo metadata từ SQLWF sang. Việc cần làm là mở **chiều ngược lại**.

</details>

## 2.4 🆕 Màn "Lịch sử phiên bản dữ liệu"

<details open>
<summary><b>🆕 Màn "Lịch sử phiên bản dữ liệu"</b></summary>


**Vị trí:** tab mới trong chi tiết bảng, cạnh tab Schema / Sample data
**Điều kiện:** chỉ bảng định dạng Iceberg

| Vùng màn hình | Nội dung |
|---|---|
| **Danh sách phiên bản** | Mỗi dòng: thời điểm ghi · thao tác (ghi thêm/ghi đè/xoá) · số dòng thay đổi · tổng số dòng sau khi ghi · job nào ghi |
| **Bộ lọc** | Khoảng thời gian · loại thao tác |
| **Nút "Xem dữ liệu tại thời điểm này"** | Mở màn xem dữ liệu, hiển thị bảng **đúng như lúc đó** |
| **Nút "So sánh với hiện tại"** ⚠️ | Chênh lệch số dòng giữa phiên bản chọn và hiện tại. Cần chốt có làm ở GĐ 2 không |

**Kịch bản dùng thật — chính là lý do chọn nhóm đối soát làm thí điểm:**

```
 Đơn vị nghiệp vụ:  "Chiều qua tôi xem báo cáo thấy 1.204 giao dịch,
                     sáng nay mở lại chỉ còn 1.198. Ai sửa?"

 Hôm nay:            Không trả lời được. Dữ liệu đã bị job ghi đè.

 Sau tính năng này:  Mở tab Lịch sử phiên bản → chọn mốc 15:00 hôm qua
                     → bấm "Xem dữ liệu tại thời điểm này"
                     → thấy đúng 1.204 dòng
                     → nhìn nhật ký: 22:30 job X ghi đè, giảm 6 dòng
```

</details>

## 2.5 🔧 Ghi kết quả đối soát thành chỉ số chất lượng

<details open>
<summary><b>🔧 Ghi kết quả đối soát thành chỉ số chất lượng</b></summary>


**Nơi làm:** tool DQ + luồng đối soát hiện có

Kết quả đối soát hiện đang là một nghiệp vụ độc lập, **không được tính là thông tin chất lượng dữ liệu**. Việc cần làm: mỗi lần đối soát xong, ghi kết quả (khớp / lệch bao nhiêu) thành một chỉ số thuộc chiều **Tính nhất quán** — chiều hiện đang **rỗng** trên giao diện DQ.

**Người dùng thấy gì:** bảng đối soát có điểm chất lượng phản ánh cả kết quả đối soát, không chỉ các kiểm tra kỹ thuật.

</details>

## 2.6 Quy trình xử lý sau cảnh báo

<details open>
<summary><b>Quy trình xử lý sau cảnh báo</b></summary>


**Không phải tính năng — là quy trình vận hành.** Bản demo DQ đã có sẵn vòng đời sự cố (mở → đang xử lý → đóng). Việc cần làm là **ban hành quy định**: ai nhận cảnh báo, trong bao lâu phải phản hồi, đóng sự cố cần ghi gì.

> Không có quy trình này thì cảnh báo bắn ra không ai xử lý, sau vài tuần mọi người tắt thông báo — đúng vết xe đổ của DQ v1/v2.

</details>

</details>

---
---

# GIAI ĐOẠN 3 — NỐI BA TRỤ

<details open>
<summary><b>GIAI ĐOẠN 3 — NỐI BA TRỤ</b></summary>


## 3.1 🆕 Màn "Hồ sơ bảng dữ liệu"

<details open>
<summary><b>🆕 Màn "Hồ sơ bảng dữ liệu"</b></summary>


Gộp thông tin của cả 3 trụ vào **một màn duy nhất** — thay vì người dùng phải mở 4 chỗ khác nhau.

```
  ┌──────────────────────────────────────────────────────────────┐
  │  📋  HỒ SƠ BẢNG:  DOI_SOAT_DOI_TAC_A                          │
  ├──────────────────────────────────────────────────────────────┤
  │  ⏱️  Cập nhật lần cuối: 06:15 hôm nay        ← câu hỏi 1      │
  │  ✅  Chất lượng: 94/100 — 1 lỗi đang mở       ← câu hỏi 2      │
  │  🔗  Nguồn: 3 bảng  →  Dùng ở: 2 báo cáo      ← câu hỏi 3      │
  │  🕐  Xem lại số liệu tại: [chọn thời điểm]    ← câu hỏi 4      │
  │  🔒  12 người có quyền · 2 cột gắn nhãn PII   ← câu hỏi 5      │
  ├──────────────────────────────────────────────────────────────┤
  │  👤  BDA phụ trách: ...     DE phụ trách: ...                 │
  │  📖  Thuật ngữ: doanh thu thuần = ...                         │
  └──────────────────────────────────────────────────────────────┘
```

**Mỗi dòng là một điểm vào**, bấm vào mở ra màn chi tiết tương ứng. Đây không phải màn mới hoàn toàn — phần lớn là **gom các khối đã làm ở GĐ 1–2 lại một chỗ** và bổ sung 2 dòng còn thiếu (lineage, quyền).

</details>

## 3.2 🆕 Nhãn phân loại mức cột

<details open>
<summary><b>🆕 Nhãn phân loại mức cột</b></summary>


**Vị trí:** tab Schema, thêm 1 cột

| Control | Loại | Giá trị |
|---|---|---|
| **Nhãn phân loại** | Dropdown ở mỗi dòng cột | `Công khai` · `Nội bộ` · `Nhạy cảm` · `PII (dữ liệu cá nhân)` |

**Thao tác hỗ trợ:**

| Chức năng | Mô tả |
|---|---|
| Gán hàng loạt | Chọn nhiều cột → gán cùng một nhãn |
| Gợi ý tự động ⚠️ | Hệ thống gợi ý nhãn theo tên cột (`cmnd`, `so_dien_thoai`, `dia_chi`…) — người dùng xác nhận, không tự áp |
| Import / Download | Thêm cột nhãn vào template Schema |

> **Đây là nền tảng dùng chung cho cả 3 trụ:** Metadata lưu nhãn → Security dùng nhãn để che dữ liệu → Data Quality dùng nhãn để chọn bộ kiểm tra phù hợp. Gắn nhãn **một lần**, ba nơi dùng.

</details>

## 3.3 🆕 Che dữ liệu theo cột

<details open>
<summary><b>🆕 Che dữ liệu theo cột</b></summary>


**Người dùng thấy gì:** cùng một bảng, hai người mở ra thấy khác nhau.

```
  Người có quyền đầy đủ:      Người không có quyền xem PII:
  ┌──────────────────────┐    ┌──────────────────────┐
  │ ten_kh    │ cmnd     │    │ ten_kh    │ cmnd     │
  │ Nguyễn A  │ 001234567│    │ Nguyễn A  │ ****4567 │
  └──────────────────────┘    └──────────────────────┘
```

**Cấu hình ở đâu:** màn Chính sách theo nhãn (mới) — mỗi nhãn khai một quy tắc: ai được xem nguyên bản, ai thấy dạng che, che kiểu gì (ẩn hoàn toàn / giữ 4 ký tự cuối / băm).

**Áp dụng ở:** màn xem dữ liệu · SQL Query · Export. ⚠️ Cần chốt có áp cho cả đường API không.

</details>

## 3.4 🆕 Lineage mức cột

<details open>
<summary><b>🆕 Lineage mức cột</b></summary>


Hiện lineage chỉ tới **mức bảng**: biết bảng A sinh ra bảng B, nhưng không biết cột `doanh_thu` của B tính từ cột nào của A.

**Cách làm:** SQLWF đã lưu sẵn **toàn bộ câu SQL của các job** → phân tích câu SQL để suy ra quan hệ cột.

**Người dùng thấy gì:** ở tab Schema, mỗi cột có thêm biểu tượng 🔗 — bấm vào hiện *"Cột này tính từ: `A.tong_tien` − `A.chiet_khau`"* và *"Cột này được dùng ở: `C.doanh_thu_thuan`"*.

**Giá trị lớn nhất:** khi một cột lỗi, biết ngay **những báo cáo nào phía sau bị ảnh hưởng** — mối nối đang đứt số 2 trong tài liệu mẹ.

</details>

## 3.5 🆕 Màn "Quyền của người dùng"

<details open>
<summary><b>🆕 Màn "Quyền của người dùng"</b></summary>


**Trả lời câu hỏi kiểm toán số 1:** *"Người này đang xem được dữ liệu gì?"*

Hiện phải hỏi **4 nơi** (quyền chức năng · quyền bảng · quyền thư mục · kiểm soát truy vấn). Màn này gộp lại:

| Vùng | Nội dung |
|---|---|
| **Ô tìm người dùng** | Nhập tên / mã nhân viên |
| **Kết quả — tab Bảng** | Danh sách bảng người này xem được, kèm **nguồn quyền** (từ nhóm nào / cấp trực tiếp) |
| **Kết quả — tab Thư mục** | Danh sách thư mục HDFS truy cập được |
| **Kết quả — tab Cột bị che** | Những cột người này thấy dạng che |
| **Kết quả — tab Hạn chế** | Hàm SQL bị chặn · giới hạn IP |
| **Xuất Excel** | Phục vụ hồ sơ kiểm toán |

**Chiều ngược lại** cũng cần: từ màn chi tiết bảng, bấm *"12 người có quyền"* → ra danh sách ai.

</details>

## 3.6 🆕 Chặn dữ liệu xấu tại cửa nạp

<details open>
<summary><b>🆕 Chặn dữ liệu xấu tại cửa nạp</b></summary>


Hiện Data Quality **phát hiện sau khi dữ liệu đã vào**. Việc này đưa kiểm tra lên **trước** thời điểm ghi vào bảng chính.

| Cấu hình | Mô tả |
|---|---|
| Bật/tắt chặn theo bảng | Chỉ bật cho bảng trọng yếu |
| Chọn bộ kiểm tra chặn | Chọn trong các loại kiểm tra đã cấu hình |
| Hành vi khi không đạt | `Chặn hoàn toàn` · `Cho vào nhưng cảnh báo` · `Tách dòng lỗi ra file riêng` |

**Người dùng thấy gì:** luồng Upload/ETL báo *"Đã chặn 1.204 dòng không đạt kiểm tra — tải file dòng lỗi"* thay vì để dữ liệu xấu vào rồi hôm sau mới báo.

</details>

## 3.7 🆕 Gắn thuật ngữ nghiệp vụ vào cột

<details open>
<summary><b>🆕 Gắn thuật ngữ nghiệp vụ vào cột</b></summary>


Data Glossary hiện **đứng riêng**, không gắn vào cột thật. Việc này nối hai thứ lại:

| Chiều | Người dùng thấy gì |
|---|---|
| Từ cột → thuật ngữ | Ở tab Schema, cột `doanh_thu_thuan` có link tới định nghĩa chuẩn của "doanh thu thuần" |
| Từ thuật ngữ → cột | Ở màn Glossary, mỗi thuật ngữ liệt kê **những cột nào trong hệ thống đang mang nghĩa này** |

**Giá trị:** hết cảnh 3 phòng dùng 3 định nghĩa khác nhau cho cùng một chỉ tiêu mà không ai biết.

</details>

</details>

---
---

# Phụ lục A — Bảng tổng hợp tính năng

<details open>
<summary><b>Phụ lục A — Bảng tổng hợp tính năng</b></summary>


| GĐ | Mã | Tính năng | Loại | Nơi làm | Quy mô ⚠️ |
|---|---|---|---|---|---|
| 1 | 1.1-A | 2 trường Phân loại bảng + Mức độ quan trọng | 🆕 | SQLWF | Nhỏ |
| 1 | 1.1-B | Đưa 2 trường vào Import + Download | 🔧 | SQLWF | Nhỏ |
| 1 | 1.1-C | Bộ lọc + cột + chỉ số tiến độ trên danh sách bảng | 🆕 | SQLWF | Nhỏ |
| 1 | 1.1-D | Màn "Rà soát danh mục bảng" | 🆕 | SQLWF | **Vừa** |
| 1 | 1.2 | 2 trường Catalog chỉ đọc | 🆕 | SQLWF | Nhỏ |
| 1 | 1.2 | Dựng Catalog | 🏗️ | Hạ tầng | **Vừa** |
| 1 | 1.3 | Cài Iceberg vào TaskUtil | 🏗️ | Hạ tầng | Nhỏ |
| 1 | 1.4 | Chuyển nhóm bảng thí điểm | 🏗️ | Hạ tầng | **Vừa** |
| 1 | 1.5-FE | Dropdown Định dạng bảng + cột danh sách | 🆕 | SQLWF | Nhỏ |
| 1 | 1.5-BE | Rẽ nhánh sinh tham chiếu bảng | 🔧 | SQLWF | **Vừa** |
| 1 | 1.5-R | Sửa nhận diện bảng cho cảnh báo SQL / phân quyền / lineage | 🔧 | SQLWF | 🔴 **Lớn — rủi ro cao** |
| 1 | 1.6 | Khối "Tình trạng dữ liệu" | 🆕 | SQLWF | Nhỏ |
| 2 | 2.1 | Nhãn Tầng 0 / Tầng 1 cho 29 loại kiểm tra | 🔧 | Tool DQ | Nhỏ |
| 2 | 2.2 | Triển khai DQ theo phân loại bảng | 🆕 | Tool DQ | **Vừa** |
| 2 | 2.3 | Khối điểm chất lượng trên màn bảng | 🆕 | SQLWF + DQ | Nhỏ |
| 2 | 2.4 | Tab "Lịch sử phiên bản dữ liệu" | 🆕 | SQLWF | **Vừa** |
| 2 | 2.5 | Kết quả đối soát → chỉ số chất lượng | 🔧 | Tool DQ | **Vừa** |
| 2 | 2.6 | Quy trình xử lý sau cảnh báo | 📋 | Vận hành | — |
| 3 | 3.1 | Màn "Hồ sơ bảng dữ liệu" | 🆕 | SQLWF | **Vừa** |
| 3 | 3.2 | Nhãn phân loại mức cột | 🆕 | SQLWF | **Vừa** |
| 3 | 3.3 | Che dữ liệu theo cột | 🆕 | SQLWF + hạ tầng | 🔴 **Lớn** |
| 3 | 3.4 | Lineage mức cột | 🆕 | SQLWF | 🔴 **Lớn** |
| 3 | 3.5 | Màn "Quyền của người dùng" | 🆕 | SQLWF | **Vừa** |
| 3 | 3.6 | Chặn dữ liệu xấu tại cửa nạp | 🆕 | SQLWF + DQ | **Vừa** |
| 3 | 3.7 | Gắn thuật ngữ vào cột | 🆕 | SQLWF | Nhỏ |

⚠️ *Quy mô là ước lượng của BA để hình dung tương quan, chưa phải estimate của đội phát triển.*

</details>

---

# Phụ lục B — Điểm cần chốt

<details open>
<summary><b>Phụ lục B — Điểm cần chốt</b></summary>


| # | Điểm | Liên quan | Đề xuất của BA |
|---|---|---|---|
| 1 | Danh sách giá trị **Phân loại bảng** và **Mức độ quan trọng** — 4 giá trị mỗi trường như đề xuất có đủ không? | 1.1.3 | Giữ 4 giá trị. Nhiều hơn thì người điền phân vân, ít hơn thì không đủ dùng |
| 2 | Import Table với 2 trường phân loại: ô trống thì **ghi đè** hay **giữ giá trị cũ**? | 1.1.4 | **Giữ giá trị cũ** — tránh import vì việc khác làm mất kết quả phân loại |
| 3 | Cột **Định dạng bảng** trong template Import: cho sửa hay chỉ đọc? | 1.5.2 | **Chỉ đọc** — đổi định dạng phải qua quy trình chuyển đổi dữ liệu |
| 4 | Khối "Tình trạng dữ liệu" với bảng **chưa phải Iceberg**: ẩn hẳn hay hiện kèm chú thích? | 1.6.3 | **Hiện kèm chú thích** — tạo động lực chuyển đổi |
| 5 | Chuyển bảng sang Iceberg: **script ngoài tool** hay **chức năng trong tool**? | 1.4.2 | Script ngoài cho GĐ thí điểm; cân nhắc làm chức năng ở GĐ 2 |
| 6 | Nút **"So sánh với hiện tại"** ở tab Lịch sử phiên bản — làm ở GĐ 2 hay để GĐ 3? | 2.4 | GĐ 3 — GĐ 2 chỉ cần xem lại được là đủ giá trị |
| 7 | Che dữ liệu theo cột có áp cho **đường API** không? | 3.3 | Có — nếu không thì lách qua API là xem được hết |
| 8 | Hạ tầng đã có sẵn **Hive Metastore** chưa? | 1.2 | ⚠️ Cần đội hạ tầng trả lời — ảnh hưởng trực tiếp khối lượng GĐ 1 |

---

> **Tài liệu này mô tả tính năng ở mức nghiệp vụ, dựa trên khảo sát trực tiếp mã nguồn SQLWF (backend Java + frontend Angular) và SRS Metadata bảng v3.8.**
> Các con số ước lượng quy mô cần đội phát triển xác nhận lại trước khi đưa vào kế hoạch.

</details>
