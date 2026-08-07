# SQLWF — Hiện trạng Data Management & Nghiên cứu thị trường
### Tài liệu nền cho đề xuất hoàn thiện 3 trụ: Metadata · Data Quality · Data Security
### (kèm lý do bổ sung `type = Hudi / Iceberg` vào Quản lý bảng)

> **Đối tượng đọc:** IT BA / PO / quản lý sản phẩm. Viết ở mức nghiệp vụ, nhưng **không giấu chi tiết kỹ thuật cần thiết** — chỗ nào BA phải biết tên kho dữ liệu, tên bảng, tên trường thì ghi rõ, kèm giải nghĩa.
> **Mục tiêu:** đọc xong file này là **không cần mở source code** vẫn nắm được SQLWF đang làm gì, dữ liệu đi thế nào, đang thiếu gì, và cần nghiên cứu tool nào.
> **Nguồn:** khảo sát trực tiếp source `sqlwf-be` (Java/Spring) + `sqlwf-fe` (Angular), tháng 07/2026, cộng nghiên cứu thị trường (mục 13–14).
> **Ký hiệu:**
> - ✅ = đã có và hoạt động
> - 🟡 = có nhưng chưa đầy đủ / chưa dùng được
> - ❌ = chưa có
> - ⚠️ = **suy luận từ code, cần xác nhận với đội phát triển** trước khi đưa vào tài liệu chính thức

---

## MỤC LỤC

**PHẦN A — HIỂU SQLWF ĐANG LÀ GÌ**
- [1. SQLWF trong 1 trang](#1-sqlwf-trong-1-trang)
- [2. Bản đồ hệ thống — ai giữ dữ liệu gì](#2-bản-đồ-hệ-thống--ai-giữ-dữ-liệu-gì)
- [3. Bản đồ chức năng — 60+ màn hình chia thành 8 nhóm](#3-bản-đồ-chức-năng)
- [4. "Bảng" trong SQLWF thực chất là gì](#4-bảng-trong-sqlwf-thực-chất-là-gì)
- [5. Vòng đời một bảng — từ khai báo tới khai thác](#5-vòng-đời-một-bảng)
- [6. Dữ liệu VÀO bằng những cửa nào (5 cửa)](#6-dữ-liệu-vào-bằng-những-cửa-nào)
- [7. Dữ liệu RA bằng những kênh nào (6 kênh)](#7-dữ-liệu-ra-bằng-những-kênh-nào)
- [8. Ai thực sự chạy job — Pentaho, TaskUtil, Hadoop Adapter](#8-ai-thực-sự-chạy-job)

**PHẦN B — BA TRỤ DATA MANAGEMENT: HIỆN TRẠNG CHI TIẾT**
- [9. Trụ 1 — METADATA](#9-trụ-1--metadata)
- [10. Trụ 2 — DATA QUALITY](#10-trụ-2--data-quality)
- [11. Trụ 3 — DATA SECURITY](#11-trụ-3--data-security)
- [12. Ba trụ đang RỜI RẠC ở đâu — phân tích mối nối](#12-ba-trụ-đang-rời-rạc-ở-đâu)

**PHẦN C — HUDI / ICEBERG**
- [13. Vì sao cần thêm type = Hudi / Iceberg](#13-vì-sao-cần-thêm-type--hudi--iceberg)

**PHẦN D — THỊ TRƯỜNG & ĐỀ XUẤT**
- [14. Nghiên cứu thị trường — tool nào cần xem, tool nào dùng thử được ngay](#14-nghiên-cứu-thị-trường)
- [15. So khớp SQLWF ↔ thị trường — bảng thừa/thiếu](#15-so-khớp-sqlwf--thị-trường)
- [16. Đề xuất](#16-đề-xuất)
- [17. Kế hoạch nghiên cứu cuối tuần — checklist thực hành](#17-kế-hoạch-nghiên-cứu-cuối-tuần)

**PHỤ LỤC**
- [P1. Từ điển thuật ngữ](#p1-từ-điển-thuật-ngữ)
- [P2. Danh mục kho dữ liệu & bảng quan trọng](#p2-danh-mục-kho-dữ-liệu--bảng-quan-trọng)
- [P3. Danh sách 22 vùng lưu trữ (zone)](#p3-danh-sách-22-vùng-lưu-trữ)
- [P4. Câu hỏi cần xác nhận với đội phát triển](#p4-câu-hỏi-cần-xác-nhận)

---
---

# PHẦN A — HIỂU SQLWF ĐANG LÀ GÌ

## 1. SQLWF trong 1 trang

**SQLWF (SQL Workflow)** là một **web app quản trị kho dữ liệu lớn (data lake)** chạy trên nền Hadoop.

Nói theo ngôn ngữ nghiệp vụ, SQLWF làm 4 việc:

| # | Việc | Nghĩa là |
|---|---|---|
| 1 | **Khai báo & quản lý "bảng"** | Người dùng khai: bảng tên gì, có cột nào, thuộc lĩnh vực (domain) nào, ai sở hữu, đồng bộ mấy lần/ngày, có phải bảng phục vụ báo cáo (datamart) không |
| 2 | **Đưa dữ liệu vào bảng** | Qua 5 cửa: Upload file, Job ETL (SQL theo lịch), Quản lý danh mục, Đồng bộ từ DB nguồn, Nạp file tài chính |
| 3 | **Cho phép khai thác dữ liệu** | Qua 6 kênh: màn hình dữ liệu, SQL query, HDFS Explorer, Export/Delivery, Zeppelin, API |
| 4 | **Kiểm soát: chất lượng + quyền + vết** | DQ theo chu kỳ, phân quyền theo nhóm bảng/thư mục/IP, ghi audit log |

**Điều quan trọng nhất cần nhớ:**

> Dữ liệu **thật** (số liệu doanh thu, thuê bao, giao dịch…) nằm trên **HDFS dưới dạng file Parquet/CSV**.
> Còn **mọi thứ mô tả về dữ liệu** (bảng tên gì, cột gì, ai được xem, chất lượng ra sao) nằm rải ở **4 kho khác nhau**: MongoDB, MariaDB, Neo4j, và một phần trong file cấu hình.
>
> **Chính việc "mô tả dữ liệu bị chia ở 4 nơi, không nối với nhau" là gốc rễ của cảm giác "3 trụ đang rời rạc".** Đây là luận điểm trung tâm của cả tài liệu này.

---

## 2. Bản đồ hệ thống — ai giữ dữ liệu gì

### 2.1. Sơ đồ tổng thể

```
                    ┌────────────────────────────────────────────┐
                    │              NGƯỜI DÙNG                     │
                    │   BA · Data Engineer · Vận hành · Lãnh đạo  │
                    └──────────────────┬─────────────────────────┘
                                       │ trình duyệt
                    ┌──────────────────▼─────────────────────────┐
                    │        SQLWF FRONTEND (Angular)             │
                    │        ~60 màn hình quản trị                │
                    └──────────────────┬─────────────────────────┘
                                       │ REST API
                    ┌──────────────────▼─────────────────────────┐
                    │     SQLWF BACKEND (Java / Spring Boot)      │
                    │  — không tự xử lý dữ liệu lớn —              │
                    │  chỉ: quản metadata, phân quyền, điều phối   │
                    └───┬──────┬──────┬──────┬──────┬──────┬─────┘
                        │      │      │      │      │      │
        ┌───────────────┘      │      │      │      │      └──────────────┐
        │        ┌─────────────┘      │      │      └────────┐            │
        ▼        ▼                    ▼      ▼               ▼            ▼
  ┌──────────┐ ┌──────────┐   ┌───────────┐ ┌─────────┐ ┌─────────┐ ┌──────────┐
  │ MongoDB  │ │ MariaDB  │   │  Neo4j    │ │ClickHouse│ │  MinIO  │ │ RabbitMQ │
  │          │ │          │   │           │ │         │ │         │ │  Kafka   │
  │ Metadata │ │ Người    │   │ Lineage   │ │ Truy vấn│ │ File    │ │ Hàng đợi │
  │ bảng,job,│ │ dùng,    │   │ (quan hệ  │ │ nhanh   │ │ tài     │ │ + thông  │
  │ DQ config│ │ quyền,   │   │ bảng↔job) │ │ (feature│ │ chính,  │ │ báo      │
  │ danh mục │ │ menu,    │   │           │ │ selec-  │ │ chatbot │ │          │
  │          │ │ audit    │   │           │ │ tion)   │ │         │ │          │
  └──────────┘ └──────────┘   └───────────┘ └─────────┘ └─────────┘ └──────────┘
        │
        │  SQLWF Backend KHÔNG tự đọc/ghi dữ liệu lớn. Nó nhờ 3 "cánh tay" bên ngoài:
        │
  ┌─────▼──────────────┬─────────────────────┬──────────────────────────┐
  ▼                    ▼                     ▼                          ▼
┌────────────┐  ┌──────────────┐   ┌──────────────────┐      ┌──────────────┐
│  TaskUtil  │  │   Pentaho    │   │  Hadoop Adapter  │      │ OPA Collector│
│ (ws:9503)  │  │ (Coordinator)│   │   (http:8080)    │      │  (chính sách)│
│            │  │              │   │                  │      │              │
│ CHẠY SQL   │  │ ĐẶT LỊCH job │   │ THAO TÁC FILE    │      │ ĐỒNG BỘ      │
│ (Spark SQL)│  │ chạy định kỳ │   │ trên HDFS        │      │ blacklist    │
│ trên lake  │  │              │   │ (list/up/down/   │      │ bảng + hàm   │
│            │  │              │   │  rename/xóa)     │      │ + user       │
└─────┬──────┘  └──────┬───────┘   └────────┬─────────┘      └──────────────┘
      │                │                     │
      └────────────────┴─────────────────────┘
                       │
                       ▼
        ┌──────────────────────────────────────┐
        │   HDFS — DATA LAKE (dữ liệu thật)     │
        │   /storage/<zone>/<domain>/<path>/    │
        │   file Parquet & CSV                  │
        │   Bảo mật tầng hạ tầng: Kerberos      │
        └──────────────────────────────────────┘
```

### 2.2. Giải thích từng thành phần (ngôn ngữ nghiệp vụ)

| Thành phần | Ví von | Giữ cái gì | BA cần biết gì |
|---|---|---|---|
| **HDFS** | Nhà kho hàng khổng lồ | Dữ liệu thật, dạng file Parquet/CSV | Đây là nơi duy nhất chứa số liệu. Mọi thứ khác chỉ là "sổ sách" |
| **MongoDB** | Sổ cái mô tả nghiệp vụ | Khai báo bảng, job, DQ config, danh mục, template upload | **Kho metadata chính.** Bảng quan trọng nhất: `tbl_table_info` |
| **MariaDB** | Sổ đăng ký người & quyền | Tài khoản, vai trò, menu, phân quyền thư mục, **audit log**, IP whitelist, tag chặn hàm SQL | Trụ Data Security nằm chủ yếu ở đây |
| **Neo4j** | Sơ đồ quan hệ | Data Lineage: bảng nào sinh ra từ bảng nào, qua job/step nào | Chỉ dùng cho 1 màn: **Data Lineage** |
| **ClickHouse** | Kho phụ tra cứu nhanh | Dữ liệu phục vụ "Chọn tập theo điều kiện" (feature selection) | Kho phụ, không phải data lake chính |
| **MinIO** | Tủ hồ sơ | File tài chính, file chatbot | Kho file phụ trợ, không phải bảng |
| **RabbitMQ / Kafka** | Băng chuyền + loa | Chuyển việc bất đồng bộ, gửi thông báo | Cơ chế nền, BA ít chạm |
| **TaskUtil** | Người thợ chạy SQL | Không giữ gì — nhận câu SQL, chạy trên lake, trả kết quả | **Toàn bộ SQL của SQLWF chạy ở đây.** Là dịch vụ riêng, không thuộc SQLWF |
| **Pentaho** | Người bấm đồng hồ | Lịch chạy job (cron), trạng thái job | Đây chính là cái tài liệu cũ gọi là **"Coordinator"** — **không phải Oozie** ⚠️ |
| **Hadoop Adapter** | Người bốc xếp kho | Không giữ gì — tạo thư mục, upload/download/đổi tên file HDFS | Backend của màn **HDFS Explorer** |
| **OPA Collector** | Bảng nội quy | Nhận danh sách cấm (bảng cấm, hàm cấm, user cấm) từ SQLWF | Lớp thực thi chính sách bảo mật ⚠️ |
| **Kerberos** | Thẻ ra vào kho | Xác thực ở tầng Hadoop | Có cấu hình `keytab`/`principal` trong hệ thống |

> **Điểm cần nhấn mạnh cho báo cáo:** SQLWF **không phải** là engine xử lý dữ liệu. Nó là **lớp quản trị + điều phối**. Sức mạnh xử lý nằm ở TaskUtil (Spark) và Hadoop. Điều này quan trọng vì: mọi đề xuất bổ sung tính năng (Hudi/Iceberg, DQ nâng cao, masking) đều **phụ thuộc vào việc TaskUtil/Hadoop có hỗ trợ hay không**, không phải chỉ sửa SQLWF là xong.

---

## 3. Bản đồ chức năng

SQLWF hiện có khoảng **60+ màn hình**. Gom lại thành **8 nhóm**:

### Nhóm 1 — Quản trị dữ liệu (lõi Data Management)
| Màn hình | Làm gì |
|---|---|
| **Quản lý bảng** (`table-management`) | Khai báo bảng: tên, kiểu file, vùng lưu trữ, cột, chủ sở hữu, domain, tần suất đồng bộ, cấu hình ghi |
| **Quản lý nhóm bảng** (`table-monitor` / create-group-table) | Gom bảng thành nhóm để phân quyền |
| **Data Quality** (`data-quality`) | Bật/tắt DQ, khai chỉ số DQ cho bảng và cho từng trường, cấu hình chu kỳ & nhóm nhận cảnh báo |
| **Data Lineage** (`data-linage`) | Xem sơ đồ bảng này sinh ra từ đâu, đi đến đâu |
| **Data Dictionary** (`data-dictionary`) | Từ điển đặc trưng dữ liệu (feature metadata), có versioning + feedback |
| **Data Glossary** (`data-glossary`) | Từ điển thuật ngữ nghiệp vụ, gắn phòng ban, đính kèm tài liệu |
| **Quản lý Domain** (`domain-management`) | Khai báo lĩnh vực nghiệp vụ (domain / sub-domain) |
| **Lịch sử thay đổi** (`history-data`) | Xem lịch sử chỉnh sửa cấu hình bảng |

### Nhóm 2 — Đưa dữ liệu vào
| Màn hình | Làm gì |
|---|---|
| **Import Data / Upload** (`import-data`) | Tải file Excel/CSV theo template đã khai sẵn |
| **Quản lý Job** (`job-management`) | Tạo job ETL: chuỗi bước SQL có phụ thuộc nhau (DAG), ghi ra bảng đích |
| **Pentaho Job Management** (v1, v2) | Quản lý lịch chạy job trên Pentaho |
| **Data Transform** (`data-transform`) | Cấu hình biến đổi dữ liệu, chọn đích ghi: Parquet / Hive / Kafka / ClickHouse / Mongo / HBase |
| **Sync Management** (`sync-management`) | Đồng bộ dữ liệu từ CSDL nguồn |
| **Data Migration** (`data-migration-management`) | Di chuyển dữ liệu giữa các vùng |
| **Quản lý danh mục** ⚠️ | Nhập/duyệt dữ liệu tham chiếu (có versioning) |
| **Invoice Uploader / Financial** | Nạp file hóa đơn, dữ liệu tài chính (qua MinIO) |

### Nhóm 3 — Khai thác dữ liệu
| Màn hình | Làm gì |
|---|---|
| **SQL Query** + `sql-editor` | Gõ SQL truy vấn trực tiếp lên lake |
| **SQL History / Query History** | Lịch sử câu truy vấn đã chạy |
| **HDFS Explorer** (`hdfs-explorer`) | Duyệt cây thư mục HDFS, xem/tải/đổi tên/tạo thư mục |
| **File Management / File View** | Quản lý file + phân quyền file |
| **IO Download / Data Delivery** | Xuất dữ liệu ra ngoài (file, email, SMS) |
| **Zeppelin** | Notebook phân tích |
| **Feature Selection** | Chọn tập dữ liệu theo điều kiện (chạy trên ClickHouse) |

### Nhóm 4 — Bảo mật & phân quyền
| Màn hình | Làm gì |
|---|---|
| **Quản lý người dùng** (`user-managerment`) | Tài khoản, vai trò |
| **ACL** (`acl`) | Danh sách kiểm soát truy cập |
| **Data Authorize** (`data-authorize`) | Phân quyền dữ liệu |
| **Group Authorize** (`group-authorize`) | Phân quyền theo nhóm |
| **Feature Menu Authorization** | Phân quyền menu/chức năng |
| **File View Group** (`file-view-group`) | Phân quyền thư mục HDFS theo user/nhóm |
| **Tags** (`tags`) | Gán nhãn user → chặn hàm SQL nguy hiểm (query guard) |
| **KDC Management** | Quản lý Kerberos ⚠️ |

### Nhóm 5 — Giám sát & cảnh báo
| Màn hình | Làm gì |
|---|---|
| **Table Monitor** | Giám sát bảng |
| **Warning History** | Lịch sử cảnh báo |
| **Task Management** | Theo dõi tác vụ đang chạy |
| **Report Management** | Báo cáo quản trị |

### Nhóm 6 — Đối soát (Reconciliation)
`reconcile-ads`, `reconciliation-reports`, `partner-reconciliation-data`, `support-data-compare`, `renewal-report` — nhóm nghiệp vụ đối soát số liệu giữa các nguồn.

### Nhóm 7 — Nghiệp vụ chuyên biệt
`blacklist-management`, `leadgen`, `lead-marketing`, `look-a-like`, `remarketing`, `chatbot-kpp`, `news-management`, `backtest-management`, `brand-management`, `partner-management`, `pyc-management`, `channel-indexing-management`, `in-dept-analysis-management`…

### Nhóm 8 — Cấu hình hệ thống
`configuration-management`, `connection-management`, `menu-items`, `processing-guidance`, `telegram`, `fsync`.

> **Nhận xét cho báo cáo:** SQLWF **không phải** một công cụ Data Management thuần túy. Nó là **nền tảng đa mục đích**: ~30% màn hình là Data Management, ~70% là nghiệp vụ chuyên biệt (đối soát, marketing, chatbot, tài chính). Điều này giải thích vì sao 3 trụ DM "rời rạc" — chúng được xây **theo từng yêu cầu nghiệp vụ riêng lẻ**, không theo một khung Data Governance thống nhất từ đầu.

---

## 4. "Bảng" trong SQLWF thực chất là gì

Đây là phần **quan trọng nhất** để hiểu mọi thứ còn lại.

### 4.1. Ba tầng chồng nhau

```
   Cái người dùng thấy:   "Bảng REVENUE_MERCHANT"
              │
              ▼   thực chất chỉ là 1 BẢN GHI mô tả trong MongoDB
   Bản ghi trong MongoDB (collection: tbl_table_info)
      { name: "REVENUE_MERCHANT",
        type: "parquet",                  ← chỉ có 2 lựa chọn: parquet | csv
        area: "bi_business_zone",         ← vùng lưu trữ (1 trong 22 zone)
        path: "reports/revenue_merchant", ← đường dẫn con
        schema: [ {name, type, description}, ... ],
        createdInfo: { mode, partitionBy, mergeBy, ... },
        tableQuality: { ...cấu hình DQ... },
        domainIds, businessOwner, dataEngineerOwner, jobName, syncFrequency, dataMart }
              │
              ▼   trỏ tới một THƯ MỤC trên HDFS
   /storage/business_zone/bi/reports/revenue_merchant/
              │
              ▼   bên trong là các FILE
   PARTITION_DATE=20260724/part-00000.parquet
   PARTITION_DATE=20260725/part-00000.parquet
```

### 4.2. Điều gây bất ngờ nhất: **SQLWF không có "danh mục bảng" (catalog) thật**

Khi bạn viết SQL trong SQLWF, hệ thống **không** dịch tên bảng thành `database.table` như CSDL thông thường. Nó dịch thành **đường dẫn file**:

```
Người dùng chọn bảng REVENUE_MERCHANT
                 ↓  SQLWF tự sinh ra:
SELECT * FROM parquet.`/storage/business_zone/bi/reports/revenue_merchant`
                      └────────── đây là ĐƯỜNG DẪN, không phải TÊN BẢNG ──────────┘
```

**Hệ quả nghiệp vụ của việc này — rất quan trọng cho phần đề xuất:**

| Hệ quả | Nghĩa là |
|---|---|
| Không có Hive Metastore / catalog trung tâm | Không công cụ nào bên ngoài (Trino, Power BI, tool catalog thị trường) "nhìn thấy" danh sách bảng của SQLWF một cách tự nhiên. Muốn tích hợp phải viết connector riêng ⚠️ |
| Metadata và dữ liệu **không gắn cứng với nhau** | Có thể xoá file trên HDFS mà bản ghi mô tả trong Mongo vẫn còn (bảng "ma"), và ngược lại — file tồn tại mà không ai khai báo (dữ liệu "mồ côi") |
| Phân quyền phải làm theo **đường dẫn**, không phải theo tên bảng | Đây là lý do trong hệ thống có `pathPatterns` (mẫu đường dẫn) khi phân quyền nhóm bảng |
| Muốn dùng Hudi/Iceberg → **bắt buộc phải dựng catalog trước** | Xem mục 13 |

### 4.3. Cấu hình ghi dữ liệu — phần `createdInfo`

Khi khai báo bảng, người dùng khai thêm 1 khối cấu hình về **cách ghi dữ liệu vào bảng**:

| Trường | Nghĩa nghiệp vụ | Tình trạng |
|---|---|---|
| `mode` | Ghi thêm (`append`) hay ghi đè (`overwrite`) | ✅ đang dùng |
| `partitionBy` | Chia bảng theo cột nào (thường theo ngày) | ✅ đang dùng |
| `partition` | Số file đầu ra mong muốn | ✅ đang dùng |
| **`mergeBy`** | **Khóa để hợp nhất dữ liệu (khóa chính nghiệp vụ)** | 🟡 **Người dùng khai được trên UI, lưu vào Mongo, nhưng backend SQLWF không đọc trường này ở bất kỳ đâu** |
| `groupBy`, `orderBy` | Gom nhóm / sắp xếp khi ghi | 🟡 tương tự |
| `recordNumber` | Số bản ghi giới hạn | ✅ |

> **Phát hiện đáng giá:** trường **`mergeBy` — "khóa hợp nhất" — đã tồn tại sẵn trong màn Quản lý bảng và trong cơ sở dữ liệu, nhưng chưa được khai thác.** Đây chính xác là thông tin mà Hudi/Iceberg cần để làm "cập nhật đúng dòng" (upsert). Nghĩa là: **về mặt metadata, SQLWF đã sẵn sàng 70% cho Hudi/Iceberg mà chưa ai để ý.**

---

## 5. Vòng đời một bảng

```
 GIAI ĐOẠN 1: KHAI BÁO              GIAI ĐOẠN 2: NẠP DỮ LIỆU        GIAI ĐOẠN 3: KHAI THÁC
 ┌───────────────────────┐          ┌────────────────────────┐      ┌──────────────────────┐
 │ Màn "Quản lý bảng"     │          │ 5 cửa nạp (mục 6)      │      │ 6 kênh xem (mục 7)   │
 │                        │          │                        │      │                      │
 │ • Tên bảng             │          │ • Upload file          │      │ • Màn dữ liệu        │
 │ • Kiểu: parquet|csv    │  tạo     │ • Job ETL (SQL+lịch)   │ ghi  │ • SQL Query          │
 │ • Vùng (zone)          │ ────────►│ • Quản lý danh mục     │─────►│ • HDFS Explorer      │
 │ • Đường dẫn            │  thư mục │ • Đồng bộ từ DB nguồn  │ file │ • Export / Delivery  │
 │ • Danh sách cột        │  HDFS    │ • File tài chính       │      │ • Zeppelin           │
 │ • Domain, chủ sở hữu   │          │                        │      │ • API                │
 │ • Tần suất đồng bộ     │          └────────────────────────┘      └──────────────────────┘
 │ • Cấu hình DQ          │                     │
 │ • Cấu hình ghi         │                     │
 └───────────────────────┘                     ▼
            │                        ┌────────────────────────┐
            │                        │ GIAI ĐOẠN 4: KIỂM SOÁT │
            └───────────────────────►│ • DQ chạy theo chu kỳ  │
                                     │ • Cảnh báo khi vi phạm │
                                     │ • Audit log mọi thao tác│
                                     │ • Lineage cập nhật     │
                                     └────────────────────────┘
```

**Điểm gãy trong vòng đời (sẽ phân tích kỹ ở mục 12):**
- Giai đoạn 1 sinh ra metadata, nhưng **metadata này không tự động kiểm chứng với dữ liệu thật** ở giai đoạn 2.
- Giai đoạn 4 (DQ) chạy **độc lập**, kết quả không phản hồi ngược lại giai đoạn 1 và 3.

---

## 6. Dữ liệu VÀO bằng những cửa nào

### Cửa 1 — Upload theo template (`import-data`)

**Dùng khi:** đơn vị nghiệp vụ có file Excel/CSV cần đưa vào định kỳ (VD: file doanh thu hằng ngày).

**Luồng chi tiết:**

```
 ① Admin tạo TEMPLATE trước
    (khai: file có cột nào, cột nào là partition, cột nào bắt buộc)
              │
              │ Khi tạo template, hệ thống tự sinh RA 2 BẢNG:
              ├──────► Bảng chính:  REVENUE_MERCHANT
              └──────► Bảng tạm:    REVENUE_MERCHANT_TMP   ← "khu vực chờ"
              │
 ② Người dùng tải file Excel lên
              │
 ③ Hệ thống ĐỌC file Excel, CHUYỂN sang định dạng Parquet
              │        ⚠️ Lưu ý quan trọng: xem hộp cảnh báo bên dưới
              │
 ④ Đẩy file Parquet lên HDFS, nạp vào BẢNG TẠM (_TMP)
              │        Bảng tạm được chia thư mục theo TỪNG FILE tải lên
              │
 ⑤ Hợp nhất (merge) từ bảng tạm → BẢNG CHÍNH
              │        Cách làm hiện tại: GHI ĐÈ cả phân vùng của ngày đó
              ▼
        Bảng chính sẵn sàng khai thác
```

> ⚠️ **PHÁT HIỆN QUAN TRỌNG — cần đưa vào báo cáo Data Quality:**
> Khi chuyển Excel → Parquet, **hệ thống ghi TẤT CẢ các cột dưới dạng chữ (text)**, bất kể trong template khai cột đó là số hay ngày tháng.
>
> Nghĩa là: **kiểu dữ liệu khai trong Quản lý bảng chỉ là "khai báo trên giấy", không được ép buộc ở tầng lưu trữ.**
>
> Hệ quả nghiệp vụ:
> - Một cột khai là "số tiền" vẫn có thể chứa "abc" mà tầng lưu trữ không phản đối
> - Việc kiểm tra kiểu hoàn toàn phụ thuộc vào tầng validate phía trước
> - Khi so sánh / tính toán, phải ép kiểu — dễ sai lệch âm thầm
> - **Đây là một lỗ hổng chất lượng dữ liệu ở tầng nền, không phải tầng rule**

**Điểm yếu khác của cửa này:**
- Bảng tạm chia thư mục theo từng file tải lên → tải nhiều file nhỏ sẽ sinh **rất nhiều thư mục và file nhỏ** trên HDFS, làm chậm truy vấn về sau (vấn đề "small files" kinh điển của Hadoop).
- Cơ chế `_TMP` → ghi đè phân vùng tồn tại **chỉ vì Parquet không cho sửa từng dòng** (xem mục 13).

---

### Cửa 2 — Job ETL (`job-management`)

**Dùng khi:** cần tự động lấy dữ liệu từ bảng khác, biến đổi, ghi vào bảng đích, theo lịch.

**Cấu trúc một job:**

```
   JOB (có mã điều phối, lịch cron, chủ sở hữu, cấu hình thông báo)
     │
     ├── BƯỚC 1: câu SQL ──► ghi ra "bảng tạm trong bộ nhớ" (tempView) hoặc bảng thật
     ├── BƯỚC 2: câu SQL (phụ thuộc bước 1) ──► ...
     └── BƯỚC 3: câu SQL (phụ thuộc bước 1,2) ──► ghi ra BẢNG ĐÍCH
                                                    + kiểu ghi: append / overwrite
```

- Các bước nối với nhau thành **sơ đồ phụ thuộc (DAG)** — có trường "bước cha" và có toạ độ để vẽ diagram trên UI.
- Job có **trạng thái phê duyệt**: Nháp → Chờ duyệt → Đã duyệt / Từ chối.
- Lịch chạy được đăng ký sang **Pentaho**.
- Câu SQL được gửi sang **TaskUtil** để chạy thật.

**Điểm mạnh:** đây là nơi sinh ra **Data Lineage tự động** — vì SQLWF biết bước nào đọc bảng nào, ghi bảng nào.

**Điểm yếu:** lineage chỉ ở **mức bảng**, không biết **cột nào sinh ra cột nào** (xem mục 9).

---

### Cửa 3 — Quản lý danh mục ⚠️

**Dùng khi:** dữ liệu tham chiếu (danh mục tỉnh/thành, loại dịch vụ, mã sản phẩm…) cần nhập tay hoặc upload, có quy trình duyệt.

- Lưu trong MongoDB với cơ chế **bản ghi + phiên bản** (`CategoryRecord`, `CategoryVersion`) → tức là danh mục **đã có lịch sử phiên bản**.
- Có schema động (định nghĩa cấu trúc danh mục lúc chạy).

> **Đáng chú ý:** danh mục là loại dữ liệu **thay đổi thường xuyên theo từng dòng** — đúng loại mà Hudi/Iceberg giải quyết tốt nhất. Hiện SQLWF đang tự xây cơ chế versioning riêng cho việc này.

---

### Cửa 4 — Đồng bộ từ CSDL nguồn (`sync-management`, `databasesyncinfo`)

Kết nối tới CSDL nguồn, kéo dữ liệu về lake theo cấu hình. ⚠️ Cần xác nhận chi tiết cơ chế (full load hay incremental).

---

### Cửa 5 — Nạp file chuyên biệt

File tài chính, hóa đơn — đi qua **MinIO** trước, rồi mới xử lý và chuyển thành bảng.

---

### Bảng tổng hợp 5 cửa nạp

| Cửa | Người dùng chính | Tần suất | Có duyệt? | Có DQ tự động? |
|---|---|---|---|---|
| Upload template | BA / nghiệp vụ | Hằng ngày | ⚠️ | 🟡 chỉ validate cấu trúc |
| Job ETL | Data Engineer | Theo lịch | ✅ có duyệt | 🟡 DQ chạy riêng, không chặn job |
| Quản lý danh mục | Nghiệp vụ | Khi có thay đổi | ✅ có duyệt | ❌ |
| Đồng bộ DB nguồn | Data Engineer | Theo lịch | ⚠️ | ❌ |
| File tài chính | Nghiệp vụ | Theo lô | ⚠️ | ⚠️ |

> **Khoảng trống lộ rõ:** **không có cửa nạp nào bị DQ chặn lại.** DQ chạy sau, theo chu kỳ riêng. Nghĩa là dữ liệu xấu **vẫn vào bảng chính**, rồi mới bị phát hiện — đôi khi hôm sau. Đây là điểm khác biệt lớn nhất so với các tool thị trường (xem mục 15).

---

## 7. Dữ liệu RA bằng những kênh nào

| # | Kênh | Đặc điểm | Kiểm soát quyền |
|---|---|---|---|
| 1 | **Màn hình dữ liệu trong app** | Xem dạng bảng, phân trang, tìm kiếm | Theo nhóm bảng |
| 2 | **SQL Query** | Gõ SQL tự do, chạy qua TaskUtil | Theo nhóm bảng + **giới hạn số truy vấn đồng thời** + **chặn hàm SQL theo nhãn user** |
| 3 | **HDFS Explorer** | Duyệt cây thư mục HDFS, tải file thô về | Theo **phân quyền thư mục** riêng (user + nhóm) |
| 4 | **Export / Data Delivery** | Xuất Excel/CSV, gửi qua email/SMS/FTP | Có lịch sử giao nhận (`IoHistoryInfo`) |
| 5 | **Zeppelin** | Notebook phân tích | ⚠️ |
| 6 | **API / tích hợp** | Bên thứ ba gọi vào | Qua `SysUserApi` |

> **Rủi ro bảo mật cần nêu trong báo cáo:** kênh 1–2 kiểm soát theo **bảng**, kênh 3 kiểm soát theo **thư mục**. Hai hệ thống phân quyền này **độc lập nhau**. Về lý thuyết, một người bị chặn xem bảng qua SQL vẫn có thể mở đúng thư mục đó trên HDFS Explorer nếu quyền thư mục cấu hình lỏng — vì **không có một nơi duy nhất định nghĩa "ai được xem dữ liệu gì"**. ⚠️ Cần kiểm chứng thực tế trên môi trường.

---

## 8. Ai thực sự chạy job

Đây là điểm mà tài liệu cũ để dấu hỏi ("Coordinator là Oozie hay nền tự viết?"). Câu trả lời từ khảo sát code:

```
   Người dùng bấm "Chạy job" / đến giờ theo lịch
                 │
                 ▼
   ┌─────────────────────────────┐
   │  PENTAHO  (= "Coordinator")  │   ← ĐẶT LỊCH & KÍCH HOẠT
   │  giữ: mã điều phối, cron,    │      (KHÔNG phải Oozie)
   │  trạng thái Y/W/N             │
   └──────────────┬──────────────┘
                  │ đến giờ → kích hoạt
                  ▼
   ┌─────────────────────────────┐
   │  TASKUTIL  (dịch vụ riêng)   │   ← CHẠY SQL THẬT
   │  nhận: câu SQL + tham số     │      qua kết nối websocket
   │  chạy: Spark SQL trên lake   │
   │  trả: kết quả / lỗi          │
   └──────────────┬──────────────┘
                  │
                  ▼
   ┌─────────────────────────────┐
   │  HDFS  — ghi file Parquet     │
   └─────────────────────────────┘
```

**Tham số thời gian tự động:** SQLWF cung cấp sẵn ~30 biến ngày tháng cho câu SQL (`PARTITION_DATE`, `PREVIOUS_DATE`, `PARTITION_MONTH`, `YYYYMMDD`…). Đây là lý do job có thể viết SQL kiểu "lấy dữ liệu ngày hôm qua" mà không cần sửa tay.

**Ngôn ngữ SQL:** SQLWF nhúng sẵn bộ phân tích cú pháp **Spark SQL phiên bản 3.x**.

> **Tin tốt cho đề xuất Hudi/Iceberg:** bộ phân tích cú pháp này **đã hiểu sẵn** hai loại câu lệnh mà Hudi/Iceberg cần:
> - `MERGE INTO ...` (cập nhật đúng dòng — thay cho cơ chế `_TMP` + ghi đè)
> - `FOR TIMESTAMP AS OF ...` / `FOR VERSION AS OF ...` (xem lại dữ liệu quá khứ — time travel)
>
> Nghĩa là **tầng kiểm tra SQL của SQLWF sẽ không báo lỗi** khi người dùng viết cú pháp Iceberg. Rào cản kỹ thuật thấp hơn nhiều so với dự đoán ban đầu.

**Tầng cảnh báo SQL (`SQL Warning`)** — một tính năng hay mà ít người biết: trước khi chạy, SQLWF phân tích câu SQL và cảnh báo:
- `SELECT *` sẽ lấy bao nhiêu cột (gợi ý chỉ lấy cột cần)
- Tên cột không tồn tại trong schema đã khai
- Truy vấn không lọc theo partition → sẽ quét toàn bộ bảng
- Đọc file CSV/JSON thay vì Parquet → không tối ưu

> **Nhận xét:** đây là mầm mống rất tốt của một "Query Governance". Nhưng nó **hoạt động dựa trên đường dẫn HDFS** — tức là nếu sau này chuyển sang gọi bảng bằng tên catalog, **tính năng này sẽ âm thầm ngừng hoạt động** (không báo lỗi, chỉ là không còn cảnh báo nữa). Cần lưu ý khi lập kế hoạch.

---
---

# PHẦN B — BA TRỤ DATA MANAGEMENT: HIỆN TRẠNG CHI TIẾT

## 9. Trụ 1 — METADATA

### 9.1. SQLWF đang có gì

#### (a) Metadata kỹ thuật — trong "Quản lý bảng"

| Thông tin | Có? | Ghi chú |
|---|---|---|
| Tên bảng, mô tả | ✅ | |
| Kiểu lưu trữ (`parquet` / `csv`) | ✅ | **Chỉ có 2 lựa chọn** — đây là chỗ sẽ bổ sung Hudi/Iceberg |
| Vùng lưu trữ (zone) | ✅ | 22 vùng, xem Phụ lục P3 |
| Đường dẫn HDFS | ✅ | |
| Danh sách cột + kiểu + mô tả | ✅ | Nhưng **không được ép buộc ở tầng file** (mục 6) |
| Kích thước bảng | ✅ | `totalSize` |
| Cách chia phân vùng | ✅ | `partitionBy` |
| Cấu hình ghi (append/overwrite) | ✅ | |
| **Khóa hợp nhất (`mergeBy`)** | 🟡 | Khai được nhưng chưa dùng |
| Trạng thái active | ✅ | |

#### (b) Metadata nghiệp vụ

| Thông tin | Có? | Ghi chú |
|---|---|---|
| Domain / Sub-domain | ✅ | Có màn quản lý riêng |
| **Chủ sở hữu nghiệp vụ** (`businessOwner`) | ✅ | Danh sách người |
| **Chủ sở hữu kỹ thuật** (`dataEngineerOwner`) | ✅ | Danh sách người |
| Job sinh ra bảng (`jobName`) | ✅ | |
| Tần suất đồng bộ (`syncFrequency`) | ✅ | Có cả lựa chọn "khác" |
| Có phải datamart không (`dataMart`) | ✅ | |
| Use case sử dụng bảng | ✅ | `useCases` |
| Link tài liệu nghiệp vụ | ✅ | `businessLink` + file đính kèm |
| Người tạo / sửa / duyệt + thời gian | ✅ | |

> **Đánh giá:** metadata nghiệp vụ của SQLWF **khá đầy đủ so với mặt bằng chung** — nhiều tool thị trường cũng chỉ có bấy nhiêu trường. Đây là điểm mạnh nên nêu rõ trong báo cáo.

#### (c) Data Lineage — sơ đồ dòng chảy dữ liệu

Lưu trong **Neo4j** (cơ sở dữ liệu đồ thị), gồm:

```
   ┌─────────┐   HAS_STEP    ┌──────────┐   NEXT_STEP   ┌──────────┐
   │   JOB   │──────────────►│  BƯỚC 1  │──────────────►│  BƯỚC 2  │
   └─────────┘               └────┬─────┘               └────┬─────┘
                       SOURCE_OF_STEP│              TARGET_OF_STEP│
                            ┌───────▼──────┐            ┌────────▼─────┐
                            │ BẢNG NGUỒN A │            │ BẢNG ĐÍCH B  │
                            └──────┬───────┘            └──────────────┘
                                   │      CREATES_TABLE
                                   └────────────────────────►
```

| Loại nút | Thông tin lưu |
|---|---|
| **Bảng** | Mã bảng, tên, vùng, đường dẫn, mô tả, trạng thái, người tạo/sửa, **cờ "còn tồn tại"** |
| **Job** | Mã job, tên, mô tả, trạng thái |
| **Bước (step)** | Mã job, tên bước, mô tả |

| Loại quan hệ | Nghĩa |
|---|---|
| `CREATES_TABLE` | Bảng A sinh ra bảng B |
| `HAS_STEP` | Job có bước |
| `SOURCE_OF_STEP` | Bảng là **đầu vào** của bước |
| `TARGET_OF_STEP` | Bảng là **đầu ra** của bước |
| `NEXT_STEP` | Bước này chạy sau bước kia |

#### (d) Các từ điển

| Màn hình | Nội dung | Điểm mạnh |
|---|---|---|
| **Data Dictionary** | Từ điển đặc trưng dữ liệu | Có **phiên bản** + **feedback của người dùng** + thông báo |
| **Data Glossary** | Từ điển thuật ngữ nghiệp vụ | Gắn **phòng ban**, đính kèm tài liệu, có import Excel |
| **Metadata Information Upload** | Nạp hàng loạt metadata từ Excel | 3 loại: thông tin bảng, thông tin schema, thông tin use case |

#### (e) Lịch sử thay đổi

- Màn **History Data**: xem lịch sử chỉnh sửa cấu hình bảng, có so sánh trước/sau.
- **Audit log** trong MariaDB: ghi lại giá trị cũ / giá trị mới / người thực hiện / thời gian / **địa chỉ IP** — cho ~20 loại đối tượng (tài khoản, bảng, job, quyền, SQL, domain, nhóm bảng…).

### 9.2. Trụ Metadata đang THIẾU gì

| # | Thiếu | Vì sao quan trọng | Mức độ |
|---|---|---|---|
| M1 | **Lineage ở mức CỘT** | Hiện chỉ biết "bảng A sinh ra bảng B". Không trả lời được: *"Cột `doanh_thu` trong báo cáo này lấy từ cột nào, qua phép tính gì?"* — đây là câu hỏi số 1 khi có tranh cãi số liệu | 🔴 Cao |
| M2 | **Lineage không nối tới nơi tiêu thụ cuối** | Không biết bảng này đang được dùng ở báo cáo/dashboard/API nào → **không đánh giá được ảnh hưởng khi sửa bảng** | 🔴 Cao |
| M3 | **Không có "độ tươi" (freshness) của dữ liệu** | Không có chỗ nào trả lời *"Bảng này cập nhật lần cuối lúc mấy giờ?"* một cách đáng tin. Người dùng phải đoán qua tên thư mục partition | 🔴 Cao |
| M4 | **Không có lịch sử thay đổi cấu trúc bảng (schema history)** | Thêm/xoá/đổi cột lúc nào, ai làm, ảnh hưởng gì — chỉ có trong audit log dạng văn bản thô, không có màn hình chuyên biệt | 🟠 Trung bình |
| M5 | **Không có nhãn phân loại dữ liệu (classification/tag)** | Không đánh dấu được "cột này là PII / dữ liệu nhạy cảm / dữ liệu tài chính". Hiện chỉ có cờ `isSensitivity` ở **mức nhóm bảng**, không tới mức cột | 🔴 Cao — đây là mối nối giữa Metadata và Security |
| M6 | **Không có chỉ số sử dụng (popularity/usage)** | Không biết bảng nào hay được dùng, bảng nào bỏ hoang → không biết ưu tiên chăm sóc bảng nào, không biết bảng nào xoá được | 🟠 Trung bình |
| M7 | **Metadata không tự động đối chiếu với thực tế** | Khai 10 cột nhưng file thật có 12 cột → không ai phát hiện. Bảng khai còn active nhưng thư mục đã bị xoá → không ai biết | 🔴 Cao |
| M8 | **Không có tìm kiếm/khám phá dữ liệu kiểu "Google cho dữ liệu"** | Người dùng mới không tự tìm được bảng cần dùng, phải hỏi người cũ | 🟠 Trung bình |
| M9 | **Data Dictionary / Glossary không gắn với bảng thật** | Từ điển tồn tại như một danh sách riêng, ⚠️ chưa thấy cơ chế "thuật ngữ X ↔ cột Y của bảng Z" | 🔴 Cao — đây là mối nối bị đứt rõ nhất trong trụ Metadata |

---

## 10. Trụ 2 — DATA QUALITY

> Đây là phần chị đã nhận xét *"prototype lần trước chưa ok, nhiều nội dung chưa trả lời được vì sao cần thông tin đó"*. Mục này giải thích **vì sao cảm giác đó là đúng, và gốc rễ nằm ở đâu**.

### 10.1. SQLWF đang có gì

#### (a) Khung 6 chiều chất lượng (đúng chuẩn quốc tế DAMA)

SQLWF khai báo **6 chiều chất lượng dữ liệu**:

| # | Chiều | Tên tiếng Việt trong hệ thống | Áp dụng ở mức | Có chỉ số thực tế? |
|---|---|---|---|---|
| 1 | ACCURACY | Tính chính xác | Trường | ✅ 10 chỉ số |
| 2 | TIMELINESS | Tính kịp thời | Bảng | ✅ 1 chỉ số |
| 3 | COMPLETENESS | Tính đầy đủ | Bảng | ✅ 2 chỉ số |
| 4 | CONSISTENCY | Tính nhất quán | Bảng | ❌ **RỖNG — không có chỉ số nào** |
| 5 | UNIQUENESS | Tính duy nhất | Trường | ✅ 1 chỉ số |
| 6 | VALIDITY | Tính hợp lệ | Trường | ❌ **RỖNG — không có chỉ số nào** |

> 🔴 **PHÁT HIỆN SỐ 1 — trả lời trực tiếp cho nhận xét của chị:**
> **2 trong 6 chiều chất lượng (Tính nhất quán và Tính hợp lệ) được hiển thị trên giao diện nhưng KHÔNG có bất kỳ chỉ số nào phía sau.** Người dùng chọn được chiều đó, nhưng không có gì để cấu hình và không có gì để đo.
>
> Đây chính là lý do prototype trước "có nội dung mà không trả lời được vì sao cần" — vì **một phần khung DQ là vỏ rỗng**.

#### (b) Danh mục chỉ số DQ thực tế đang có

**Chỉ số mức BẢNG (3 chỉ số):**

| Chỉ số | Đo cái gì | Cấu hình | Câu hỏi nghiệp vụ nó trả lời |
|---|---|---|---|
| **On Time** | Bảng có được cập nhật đúng giờ không | Biểu thức lịch (cron) | *"Dữ liệu hôm nay đã về chưa?"* |
| **File Size** | Kích thước dữ liệu | Ngưỡng min – max | *"Hôm nay dữ liệu có bị hụt bất thường không?"* |
| **Record Count** | Số bản ghi | Ngưỡng min – max | *"Số dòng hôm nay có bất thường không?"* |

**Chỉ số mức TRƯỜNG (11 chỉ số):**

| Chỉ số | Đo cái gì | Cấu hình |
|---|---|---|
| **Duplicate** | Có trùng lặp không | – |
| **Count** | Số giá trị | min – max |
| **Mean** | Giá trị trung bình | min – max |
| **Stddev** | Độ lệch chuẩn | min – max |
| **Min / Max** | Giá trị nhỏ nhất / lớn nhất | min – max |
| **25% / 50% / 75%** | Phân vị (giá trị ở mốc 25%, 50%, 75%) | min – max |
| **In** | Giá trị phải nằm trong danh sách cho trước | danh sách |
| **Is** | Giá trị phải bằng đúng một giá trị | giá trị |

> 🔴 **PHÁT HIỆN SỐ 2 — gốc rễ của vấn đề "không biết vì sao cần thông tin này":**
>
> Nhìn kỹ danh sách trên: **9/11 chỉ số mức trường là chỉ số THỐNG KÊ MÔ TẢ** (trung bình, độ lệch chuẩn, phân vị…).
>
> Đây là các chỉ số của **hoạt động "mô tả dữ liệu" (data profiling)** — trả lời câu hỏi *"dữ liệu trông như thế nào?"*.
>
> Chúng **KHÔNG phải** là **luật nghiệp vụ (business rule)** — thứ trả lời câu hỏi *"dữ liệu này có đúng theo quy định nghiệp vụ không?"*.
>
> **Ví dụ minh hoạ sự khác nhau:**
>
> | Loại | Câu hỏi | SQLWF làm được? |
> |---|---|---|
> | Thống kê mô tả | "Trung bình doanh thu là 5 triệu, có nằm trong khoảng 3–8 triệu không?" | ✅ Có |
> | Luật nghiệp vụ | "Số điện thoại có đúng định dạng 10 số bắt đầu bằng 0 không?" | ❌ Không |
> | Luật nghiệp vụ | "Mã tỉnh trong bảng này có tồn tại trong danh mục tỉnh không?" | ❌ Không |
> | Luật nghiệp vụ | "Ngày kết thúc có luôn lớn hơn ngày bắt đầu không?" | ❌ Không |
> | Luật nghiệp vụ | "Tổng doanh thu của bảng A có bằng tổng của bảng B không?" | ❌ Không |
> | Luật nghiệp vụ | "Cột bắt buộc có bị trống quá 5% không?" | ❌ Không (chỉ có Count, không có tỉ lệ null) |
>
> **Khi người dùng nhìn màn hình DQ hiện tại, họ thấy "độ lệch chuẩn của cột doanh thu" và hỏi "tôi cần thông tin này để làm gì?" — và họ ĐÚNG.** Con số thống kê chỉ có ý nghĩa khi gắn với một câu hỏi nghiệp vụ. Hiện tại không có tầng nào làm việc gắn kết đó.

#### (c) Cấu hình chu kỳ chạy DQ

| Cấu hình | Nghĩa |
|---|---|
| `dqEnable` | Bật/tắt DQ cho bảng |
| `dqCycleType` | Chu kỳ: Ngày / Tuần / Tháng / Quý |
| `dqOffset` | Lệch bao nhiêu so với mốc |
| `dqDelay` | Chờ bao lâu mới đo (đợi dữ liệu về) |
| `dqComparedCycle` | So sánh với bao nhiêu chu kỳ trước (mặc định 7) |
| `clusters` | Chạy trên cụm máy nào |

> **Điểm mạnh đáng ghi nhận:** `dqComparedCycle` cho phép **so sánh với các chu kỳ trước** — đây là mầm mống của **phát hiện bất thường theo xu hướng (anomaly detection)**, tính năng mà nhiều tool thị trường bán rất đắt. ⚠️ Cần xác nhận cơ chế này đang được dùng thực tế đến đâu.

#### (d) Kết quả DQ được lưu ở đâu

Trong MongoDB, mỗi lần đo sinh ra một bản ghi:

| Trường | Nghĩa |
|---|---|
| `tableName`, `fieldName` | Đo bảng nào, trường nào |
| `dqType`, `dqValue` | Loại chỉ số, giá trị đo được |
| `refMin`, `refMax`, `refEnum` | Ngưỡng tham chiếu |
| **`violationStatus`** | **Có vi phạm hay không** |
| `activeCycle`, `cycleTime`, `activeDate` | Thuộc chu kỳ nào |
| `updatedTime` | Thời điểm đo |

#### (e) Cảnh báo

- Có **nhóm nhận thông báo DQ** riêng.
- Kênh: Email, SMS, Telegram ⚠️.
- Có màn **Lịch sử cảnh báo**.

#### (f) Các tính năng chất lượng "ẩn" — không nằm trong màn DQ

| Tính năng | Nằm ở đâu | Làm gì |
|---|---|---|
| **Cảnh báo câu SQL** | Màn SQL Query | Báo cột không tồn tại, `SELECT *` lấy quá nhiều cột, quên lọc partition |
| **So sánh 2 bảng** | `support-data-compare` | Đối chiếu dữ liệu giữa 2 bảng |
| **Đối soát** | `reconcile-ads`, `reconciliation-reports` | Đối soát số liệu với đối tác |
| **Validate lúc upload** | Cửa nạp Upload | Kiểm tra cấu trúc file trước khi nạp |

> 🔴 **PHÁT HIỆN SỐ 3:** SQLWF thực ra có **4 cơ chế kiểm tra chất lượng nằm rải rác ở 4 chỗ khác nhau**, và **không cái nào biết cái nào tồn tại**. Kết quả đối soát không ghi vào DQ; DQ không biết bảng nào đang được đối soát; cảnh báo SQL không lưu thành chỉ số chất lượng.
>
> Đây là ví dụ điển hình nhất cho nhận xét *"đã có rồi nhưng đang bị rời rạc"*.

### 10.2. Trụ Data Quality đang THIẾU gì

| # | Thiếu | Vì sao quan trọng | Mức độ |
|---|---|---|---|
| Q1 | **Luật nghiệp vụ (business rule)**: định dạng, biểu thức điều kiện, tỉ lệ trống, quan hệ giữa các cột | Đây là thứ người dùng nghiệp vụ thực sự cần. Thống kê mô tả không thay thế được | 🔴 Rất cao |
| Q2 | **Kiểm tra tham chiếu (mã có tồn tại trong danh mục không)** | Lỗi phổ biến nhất trong thực tế. SQLWF **có sẵn module Quản lý danh mục** nhưng DQ không dùng được nó | 🔴 Rất cao — mối nối bị đứt |
| Q3 | **Kiểm tra nhất quán giữa các bảng** (chiều CONSISTENCY đang rỗng) | Đối soát A vs B là nghiệp vụ SQLWF làm rất nhiều, nhưng không được tính là DQ | 🔴 Rất cao |
| Q4 | **DQ không chặn được dữ liệu xấu** | DQ chạy sau, theo chu kỳ. Dữ liệu xấu đã vào bảng và có thể đã được dùng để ra quyết định | 🔴 Rất cao |
| Q5 | **Không có điểm chất lượng tổng hợp (DQ score)** | Không trả lời được: *"Bảng này đáng tin đến mức nào?"* bằng một con số/nhãn duy nhất | 🔴 Cao |
| Q6 | **Không có mức độ nghiêm trọng của lỗi** | Mọi vi phạm như nhau. Không phân biệt "cảnh báo nhẹ" với "dừng ngay" | 🟠 Trung bình |
| Q7 | **Không có quy trình xử lý sau cảnh báo** | Cảnh báo bắn ra rồi thôi. Không có: ai nhận, đã xử lý chưa, xử lý thế nào, bao lâu | 🔴 Cao |
| Q8 | **Kết quả DQ không hiện ở nơi người dùng đọc dữ liệu** | Người xem bảng không biết bảng này đang có lỗi chất lượng | 🔴 Rất cao — mối nối bị đứt |
| Q9 | **Không có DQ theo phân vùng/ngày** | Chỉ đo theo chu kỳ. Không trả lời: *"ngày 24/07 có vấn đề gì không?"* ⚠️ | 🟠 Trung bình |
| Q10 | **Kiểu dữ liệu không được ép ở tầng lưu trữ** | Xem mục 6 — cột khai là số vẫn lưu chữ | 🔴 Cao |

---

## 11. Trụ 3 — DATA SECURITY

### 11.1. SQLWF đang có gì — 7 tầng kiểm soát

SQLWF có hệ thống bảo mật **nhiều tầng, khá đầy đủ so với mặt bằng chung**. Vấn đề không phải thiếu, mà là **rời rạc**.

```
 TẦNG 1: ĐĂNG NHẬP            ── OAuth2 + SSO
 TẦNG 2: QUYỀN CHỨC NĂNG      ── Vai trò → Menu nào được thấy → API nào được gọi
 TẦNG 3: QUYỀN DỮ LIỆU (bảng) ── Nhóm bảng → User nào xem được nhóm nào
 TẦNG 4: QUYỀN THƯ MỤC (HDFS) ── Phân quyền riêng cho HDFS Explorer
 TẦNG 5: KIỂM SOÁT TRUY VẤN   ── Chặn hàm SQL nguy hiểm theo nhãn user + giới hạn số truy vấn
 TẦNG 6: KIỂM SOÁT MẠNG       ── Danh sách IP cho phép (riêng cho dữ liệu nhạy cảm)
 TẦNG 7: GHI VẾT              ── Audit log toàn hệ thống
                              ── Kerberos ở tầng Hadoop
```

#### Tầng 2 — Quyền chức năng

| Đối tượng | Lưu ở | Nội dung |
|---|---|---|
| Vai trò (Roles) | MariaDB | Admin / User / Approver |
| Menu items | MariaDB | Danh sách menu, phân cấp |
| Phân quyền menu theo nhóm | MariaDB | Nhóm nào thấy menu nào |
| Phân quyền API | MariaDB | `SysUserApi` — user hệ thống nào gọi được API nào |

#### Tầng 3 — Quyền dữ liệu theo NHÓM BẢNG

| Khái niệm | Nội dung | Ghi chú |
|---|---|---|
| **Nhóm bảng** (`tbl_table_group`) | Tên nhóm, **danh sách bảng thuộc nhóm**, **mẫu đường dẫn** (`pathPatterns`), **cờ nhạy cảm** (`isSensitivity`) | Cờ nhạy cảm ở **mức nhóm**, không tới mức cột |
| **Gán nhóm cho user** (`tbl_user_table_group`) | User → các nhóm bảng, **danh sách IP cho phép**, **danh sách IP cho dữ liệu nhạy cảm** (riêng), **số truy vấn đồng thời tối đa** | Thiết kế khá tinh tế |

> **Điểm mạnh đáng ghi nhận:** việc tách riêng "IP thường" và "IP cho dữ liệu nhạy cảm" là một thiết kế bảo mật **tốt hơn nhiều tool phổ thông**. Nên nêu như một điểm mạnh trong báo cáo.

#### Tầng 4 — Quyền thư mục HDFS (cho HDFS Explorer)

Một hệ thống phân quyền **hoàn toàn riêng biệt**:

| Bảng (MariaDB) | Nội dung |
|---|---|
| `folders` / `folder_data` | Danh sách thư mục được quản lý |
| `folder_data_authorize` | Thư mục nào cần phân quyền |
| `user_folder_data` | User nào được vào thư mục nào |
| `data_authorize` | Mã/tên nhóm quyền dữ liệu |

Ngoài ra có **File View Permission** riêng: phân quyền theo user và theo nhóm cho từng thư mục, có ghi audit riêng cho 3 loại thao tác (quyền user, quyền nhóm, thư mục).

#### Tầng 5 — Kiểm soát truy vấn (Query Guard)

Đây là tính năng ít người biết nhưng rất đáng chú ý:

```
   USER  ──gán──►  NHÃN (Tag)  ──cấm──►  DANH SÁCH HÀM SQL BỊ CHẶN
                       │
                       └──cho phép──►  DANH SÁCH HÀNH ĐỘNG
```

| Bảng (MariaDB) | Nội dung |
|---|---|
| `tag` | Nhãn (VD: "nhân viên ngoài", "phân tích viên cấp 1") |
| `user_tag` | Gán nhãn cho user |
| `function` | Danh sách hàm SQL, có phân loại |
| `tag_function_blacklist` | **Nhãn này bị cấm dùng hàm nào** |
| `tag_action` | Nhãn này được làm hành động nào |

**Ý nghĩa nghiệp vụ:** có thể cấm một nhóm người dùng gọi các hàm nhạy cảm (VD: hàm giải mã số điện thoại), trong khi vẫn cho họ truy vấn bảng đó.

> **Đây là hình thức kiểm soát gần nhất với "phân quyền mức cột" mà SQLWF đang có** — nhưng gián tiếp (qua hàm), không phải trực tiếp (qua cột).

#### Tầng 6 — Đồng bộ chính sách sang OPA ⚠️

SQLWF đẩy 3 loại danh sách cấm sang một dịch vụ chính sách bên ngoài (**OPA Collector**):
- Danh sách bảng bị cấm
- Danh sách hàm bị cấm theo nhãn
- Danh sách theo tên người dùng

> ⚠️ **Cần xác nhận:** OPA là điểm thực thi chính sách thật sự (chặn tại engine) hay chỉ là nơi lưu trữ đồng bộ. Điều này quyết định mức độ tin cậy của toàn bộ trụ Security.

#### Tầng 7 — Ghi vết (Audit)

| Thông tin ghi lại | Có? |
|---|---|
| Ai làm | ✅ |
| Làm gì (hành động) | ✅ |
| Trên đối tượng nào (~20 loại) | ✅ |
| Giá trị cũ → giá trị mới | ✅ |
| Thời điểm | ✅ |
| **Địa chỉ IP** | ✅ |
| Mã câu SQL liên quan | ✅ |

Ngoài ra có: Lịch sử SQL, Lịch sử truy vấn, Lịch sử cảnh báo, Lịch sử giao nhận dữ liệu.

#### Tầng nền — Vùng lưu trữ phân theo độ nhạy cảm

Trong 22 vùng lưu trữ, có các vùng chuyên biệt:
- `*_encrypted_zone` (bi / tel / prd / common) — **vùng mã hoá**
- `sensitive_zone` — **vùng nhạy cảm**
- `raw_zone`, `working_zone`, `temporary_zone`, `business_zone`, `share_zone`, `external_zone`

> **Cách tiếp cận bảo mật hiện tại:** bảo vệ **theo vùng lưu trữ**, không phải theo cột. Dữ liệu nhạy cảm được đặt vào vùng riêng đã mã hoá.

### 11.2. Trụ Data Security đang THIẾU gì

| # | Thiếu | Vì sao quan trọng | Mức độ |
|---|---|---|---|
| S1 | **Không có phân quyền / che giấu ở mức CỘT** | Không thể cho một người xem bảng nhưng che cột "số CMND". Hiện phải: hoặc cho xem cả bảng, hoặc tách bảng khác | 🔴 Rất cao |
| S2 | **Không có che dữ liệu động (dynamic masking)** | Không thể hiển thị `098****321` cho người này và số đầy đủ cho người kia trên **cùng một bảng** | 🔴 Rất cao |
| S3 | **Không có lọc theo dòng (row-level filter)** | Không thể tự động chỉ cho chi nhánh A xem dữ liệu chi nhánh A. Phải tách bảng thủ công | 🔴 Cao |
| S4 | **Không có nhãn phân loại dữ liệu (PII / Confidential / Public)** | Không biết cột nào nhạy cảm → không thể áp chính sách tự động. Cờ `isSensitivity` chỉ ở mức nhóm bảng | 🔴 Rất cao — nối với M5 |
| S5 | **Không tự động phát hiện dữ liệu nhạy cảm** | Phải khai tay. Bảng mới có cột CMND → không ai biết cho tới khi có sự cố | 🔴 Cao |
| S6 | **Hai hệ thống phân quyền song song, không nối nhau** | Quyền bảng (Mongo) và quyền thư mục (MariaDB) độc lập → **rủi ro rò rỉ qua HDFS Explorer** ⚠️ | 🔴 Rất cao |
| S7 | **Chính sách phân tán ở 5 nơi** | Nhóm bảng, thư mục, nhãn hàm SQL, menu, OPA — **không có một màn hình trả lời được: "Người X hiện đang xem được những dữ liệu gì?"** | 🔴 Rất cao |
| S8 | **Không có quy trình xin/cấp quyền** | Không có luồng: user xin quyền → chủ sở hữu duyệt → tự động cấp → tự động thu hồi khi hết hạn | 🟠 Trung bình |
| S9 | **Không có quyền có thời hạn** | Cấp rồi là vĩnh viễn cho đến khi ai đó nhớ ra để thu | 🟠 Trung bình |
| S10 | **Audit không có màn hình phân tích hành vi** | Có dữ liệu log nhưng không có báo cáo kiểu "ai tải nhiều dữ liệu bất thường tuần này" | 🟠 Trung bình |

---

## 12. Ba trụ đang RỜI RẠC ở đâu

Đây là phần trả lời trực tiếp cho nhận xét *"đã có rồi nhưng đang bị rời rạc, chưa thể hiện được sự liên kết chặt chẽ"*.

### 12.1. Hình dung: cái đang có vs cái nên có

```
   ═══════════ HIỆN TẠI: 3 HÒN ĐẢO ═══════════

   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
   │   METADATA   │   │ DATA QUALITY │   │   SECURITY   │
   │              │   │              │   │              │
   │ • Quản lý bảng│   │ • 6 chiều    │   │ • Nhóm bảng  │
   │ • Lineage     │   │ • 14 chỉ số  │   │ • Thư mục    │
   │ • Dictionary  │   │ • Cảnh báo   │   │ • Nhãn hàm   │
   │ • Glossary    │   │              │   │ • IP, Audit  │
   │              │   │              │   │              │
   │  (MongoDB +   │   │  (MongoDB)   │   │  (MariaDB +  │
   │   Neo4j)      │   │              │   │   OPA)       │
   └──────────────┘   └──────────────┘   └──────────────┘
         ╳ không nối        ╳ không nối        ╳

   ═══════════ NÊN CÓ: 1 LỤC ĐỊA ═══════════

              ┌────────────────────────────────┐
              │   HỒ SƠ BẢNG DỮ LIỆU (1 màn)    │
              │  ────────────────────────────  │
              │  📋 Mô tả · chủ sở hữu · domain │
              │  🔗 Nguồn gốc (lineage cột)     │
              │  ⏱️ Cập nhật lần cuối            │
              │  ✅ Điểm chất lượng: 92/100     │
              │  ⚠️ 2 lỗi đang mở               │
              │  🔒 Nhãn: có 3 cột PII          │
              │  👥 12 người đang có quyền      │
              │  📊 Được dùng ở 4 báo cáo       │
              └────────────────────────────────┘
```

### 12.2. 10 mối nối đang bị ĐỨT — liệt kê cụ thể

| # | Mối nối bị đứt | Hiện tượng người dùng gặp | Nối lại thì được gì |
|---|---|---|---|
| **N1** | **Metadata ↔ Data Quality** | Xem thông tin bảng không thấy bảng đó chất lượng thế nào; xem DQ không thấy ai là chủ sở hữu để báo | Màn Quản lý bảng hiện điểm DQ + số lỗi đang mở |
| **N2** | **Data Quality ↔ Lineage** | Bảng A lỗi, không biết những bảng nào phía sau bị ảnh hưởng | Cảnh báo kèm "ảnh hưởng tới N bảng, M báo cáo" |
| **N3** | **Metadata ↔ Security** | Không đánh nhãn PII ở mức cột → không áp được chính sách tự động | Gắn nhãn 1 lần, chính sách tự áp cho mọi cột cùng nhãn |
| **N4** | **Quyền bảng ↔ Quyền thư mục HDFS** | Hai hệ thống độc lập, có thể lệch nhau → rủi ro rò rỉ | Một nguồn sự thật duy nhất về quyền |
| **N5** | **Đối soát ↔ Data Quality** | Đối soát lệch số không được ghi nhận là lỗi chất lượng | Chiều CONSISTENCY (đang rỗng) được lấp đầy bằng chính kết quả đối soát |
| **N6** | **Quản lý danh mục ↔ Data Quality** | Có sẵn danh mục chuẩn nhưng DQ không dùng để kiểm tra mã hợp lệ | Chiều VALIDITY (đang rỗng) được lấp đầy |
| **N7** | **Cảnh báo SQL ↔ Data Quality** | Cảnh báo "cột không tồn tại" không được ghi nhận ở đâu | Phát hiện lệch giữa schema khai báo và dữ liệu thật |
| **N8** | **Data Glossary ↔ Cột của bảng** | Từ điển thuật ngữ tồn tại riêng, không gắn với cột thật ⚠️ | Người xem bảng hiểu ngay cột này nghĩa là gì |
| **N9** | **DQ ↔ Cửa nạp dữ liệu** | DQ chạy sau, không chặn được dữ liệu xấu | Dữ liệu xấu bị chặn ở cửa, không vào bảng chính |
| **N10** | **Audit ↔ Metadata/Lineage** | Có log nhưng không trả lời được "ai đang dùng bảng này nhiều nhất" | Biết bảng nào quan trọng để ưu tiên chăm sóc |

### 12.3. Ba nguyên nhân gốc

Không nên chỉ liệt kê triệu chứng. Ba nguyên nhân gốc là:

> **Nguyên nhân 1 — Không có "danh mục bảng" (catalog) trung tâm.**
> Bảng được định danh bằng **đường dẫn file**, không phải bằng tên trong một danh mục. Vì vậy mỗi module tự giữ cách tham chiếu riêng: DQ giữ `tableName` (chuỗi), Security giữ `pathPatterns` (mẫu đường dẫn), Lineage giữ `tableId` (mã Neo4j), Quản lý bảng giữ `_id` (mã Mongo). **Bốn cách gọi tên cho cùng một bảng ⇒ không thể nối chúng lại một cách đáng tin.**

> **Nguyên nhân 2 — Metadata chia ở 4 kho vật lý khác nhau.**
> MongoDB (mô tả bảng, DQ) + MariaDB (quyền, audit) + Neo4j (lineage) + file cấu hình (danh sách vùng lưu trữ). Muốn trả lời một câu hỏi tổng hợp phải ghép dữ liệu từ 4 kho — không có sẵn chỗ nào làm việc đó.

> **Nguyên nhân 3 — Đơn vị quản trị nhỏ nhất là BẢNG, không phải CỘT.**
> DQ có chỉ số mức trường, nhưng Security, Lineage, và nhãn phân loại đều **dừng ở mức bảng**. Trong khi mọi nhu cầu nâng cao (che số CMND, truy vết cột doanh thu, đánh dấu PII) đều **cần tới mức cột**.

---
---

# PHẦN C — HUDI / ICEBERG

## 13. Vì sao cần thêm `type = Hudi / Iceberg`

### 13.1. Nhắc lại: `type` hiện tại là gì

Trong màn **Quản lý bảng**, trường "Kiểu" hiện có đúng **2 lựa chọn**: `parquet` và `csv`.

Đây không phải "kiểu bảng" theo nghĩa nghiệp vụ, mà là **định dạng file**. Việc bổ sung `hudi` / `iceberg` vào đây thực chất là bổ sung một khái niệm **cao hơn một bậc**: không phải "file kiểu gì" mà là **"bảng được quản lý theo chuẩn nào"**.

### 13.2. Vấn đề của cách làm hiện tại — 5 vấn đề, minh hoạ bằng tình huống thật

#### Vấn đề 1 — Sửa 1 dòng phải ghi lại cả ngày dữ liệu

> **Tình huống:** merchant `CP001` báo sai tên. Cần sửa **1 dòng** trong dữ liệu ngày 24/07.

```
   Cách hiện tại (Parquet thuần):
   ┌──────────────────────────────┐
   │ Phân vùng ngày 24/07          │
   │ 10 triệu dòng                 │  ──► ĐỌC HẾT ──► SỬA 1 DÒNG ──► GHI ĐÈ LẠI CẢ 10 TRIỆU DÒNG
   └──────────────────────────────┘
   Tốn: thời gian, tài nguyên máy, và trong lúc ghi đè thì ai đọc bảng sẽ thấy dữ liệu không đầy đủ
```

**Đây chính là lý do tồn tại của cơ chế `_TMP` + ghi đè phân vùng.** Nó không phải là thiết kế mong muốn — nó là **giải pháp chữa cháy cho việc Parquet không cho sửa từng dòng**.

#### Vấn đề 2 — Không xem lại được quá khứ

> **Tình huống đối soát:** *"Chiều qua lúc 15h tôi lấy số liệu là 8,2 tỷ. Sáng nay lấy lại là 8,5 tỷ. Ai đúng?"*

Với cách làm hiện tại: **không trả lời được**. Job chạy đè lên dữ liệu cũ, bản cũ đã mất.

Đây là vấn đề **nghiêm trọng nhất về mặt nghiệp vụ**, vì SQLWF có cả một nhóm chức năng đối soát.

#### Vấn đề 3 — Không có "bản ghi thay đổi" nào

Không biết: dữ liệu ngày 24/07 đã bị ghi đè mấy lần? Lần cuối lúc nào? Ai/job nào ghi? Ghi bao nhiêu dòng?

→ Đây cũng chính là lý do **thiếu "độ tươi dữ liệu" (M3)** ở trụ Metadata.

#### Vấn đề 4 — Đổi cấu trúc bảng dễ vỡ

> **Tình huống:** thêm cột `discount` vào bảng đã có 2 năm dữ liệu.

Với Parquet thuần: các file cũ không có cột đó. Tuỳ cách đọc, có thể lỗi hoặc đọc sai. Không có cơ chế đảm bảo an toàn.

#### Vấn đề 5 — Ghi hỏng giữa chừng để lại dữ liệu dở dang

Nếu job ghi đè phân vùng bị lỗi giữa chừng: dữ liệu cũ đã xoá, dữ liệu mới chưa xong → **bảng ở trạng thái hỏng**. Không có cơ chế tự động quay lui.

### 13.3. Hudi / Iceberg giải quyết thế nào

**Điểm cần hiểu đúng ngay từ đầu:**

> **Hudi và Iceberg KHÔNG thay thế Parquet.** Chúng là **một lớp "sổ quản lý" đặt TRÊN các file Parquet đang có.**

```
   ┌──────────────────────────────────────────────────────┐
   │  CÔNG CỤ XỬ LÝ: Spark (qua TaskUtil), Trino, ...      │
   ├──────────────────────────────────────────────────────┤
   │  ★ LỚP MỚI — "SỔ QUẢN LÝ": Hudi hoặc Iceberg          │
   │    • Biết file nào là mới nhất, file nào đã bỏ         │
   │    • Ghi nhật ký từng lần thay đổi (ai, khi nào, gì)  │
   │    • Cho phép xem lại trạng thái bảng ở quá khứ        │
   │    • Quản lý thay đổi cấu trúc an toàn                 │
   ├──────────────────────────────────────────────────────┤
   │  ĐỊNH DẠNG FILE: Parquet   (GIỮ NGUYÊN)               │
   ├──────────────────────────────────────────────────────┤
   │  LƯU TRỮ: HDFS             (GIỮ NGUYÊN)               │
   └──────────────────────────────────────────────────────┘
```

**Ví von:** Parquet là **những trang giấy rời** ghi số liệu. Hudi/Iceberg là **quyển sổ mục lục + nhật ký chỉnh sửa** kẹp cùng xấp giấy. Nhờ quyển sổ đó mà biết được: trang nào mới nhất, trang nào bỏ, hôm qua xấp giấy trông thế nào, và sửa 1 dòng thì kẹp thêm 1 trang nhỏ thay vì chép lại cả xấp.

### 13.4. Bảng đối chiếu: vấn đề → giải pháp → lợi ích nghiệp vụ

| Vấn đề hiện tại | Hudi/Iceberg giải quyết bằng | Lợi ích nghiệp vụ cụ thể cho SQLWF |
|---|---|---|
| Sửa 1 dòng → ghi lại cả phân vùng | **Cập nhật đúng dòng (upsert)** theo khoá | Bỏ được cơ chế `_TMP` + ghi đè. Job chạy nhanh hơn, ít rủi ro hơn |
| Không xem lại được quá khứ | **Xem lại theo thời điểm (time travel)** | **Trả lời được câu hỏi đối soát: "số liệu lúc 15h chiều qua là bao nhiêu"**. Sai thì quay lui được |
| Không biết dữ liệu cập nhật lúc nào | **Nhật ký thay đổi (commit log)** | Có ngay **"độ tươi dữ liệu"** cho trụ Metadata — không phải xây riêng |
| Đổi cấu trúc dễ vỡ | **Thay đổi cấu trúc an toàn** | Thêm cột không phá query cũ. Có **lịch sử thay đổi cấu trúc** cho trụ Metadata |
| Ghi hỏng để lại dữ liệu dở | **Giao dịch trọn vẹn (ACID)** | Ghi hoặc thành công hoàn toàn, hoặc không thay đổi gì. Không còn trạng thái hỏng |

### 13.5. Hudi khác Iceberg thế nào — và nên chọn cái nào

| Tiêu chí | **Hudi** | **Iceberg** |
|---|---|---|
| Thế mạnh | Cập nhật **liên tục, gần thời gian thực**, bắt thay đổi từ CSDL nguồn (CDC) | **Phân tích quy mô lớn**, ổn định lâu dài, nhiều công cụ cùng đọc |
| Cập nhật từng dòng | ✅ Rất mạnh — cơ chế lõi | ✅ Được, qua câu lệnh `MERGE INTO` |
| Xem lại quá khứ | ✅ | ✅ |
| Đổi cấu trúc an toàn | ✅ | ✅ **Mạnh nhất** |
| Nhiều công cụ cùng đọc | 🟡 Khá | ✅ **Tốt nhất — chuẩn mở, đã thành chuẩn thị trường 2026** |
| Chi phí vận hành | Cao hơn — cần tinh chỉnh cơ chế gộp file (compaction), dọn dẹp | Thấp hơn |

**Đề xuất chọn:** xem mục 16.

### 13.6. ⚠️ Điều kiện tiên quyết — không được bỏ qua

> **Muốn dùng Iceberg/Hudi, BẮT BUỘC phải có "danh mục bảng" (catalog) trước.**
>
> Lý do: các tính năng chính (xem lại quá khứ, `MERGE INTO`, đổi cấu trúc) đều được gọi qua **tên bảng** trong một danh mục — không gọi được qua đường dẫn file như SQLWF đang làm.
>
> Nghĩa là công việc thực chất **không phải** "thêm 2 lựa chọn vào ô dropdown", mà là:
> 1. Dựng một danh mục bảng (catalog)
> 2. Thay đổi cách SQLWF gọi tên bảng trong câu SQL
> 3. Bổ sung trường "định dạng bảng" vào metadata
> 4. Rà lại các tính năng đang dựa vào đường dẫn (cảnh báo SQL, phân quyền theo `pathPatterns`, lineage)
>
> **Đây là thông tin quan trọng nhất cần đưa vào báo cáo** để tránh ước lượng sai công sức.

### 13.7. ⚠️ Câu hỏi chặn — cần hỏi đội TaskUtil TRƯỚC KHI làm gì khác

> **TaskUtil (dịch vụ chạy SQL) có nạp được thư viện Iceberg/Hudi không? Đang chạy Spark phiên bản mấy?**
>
> Nếu câu trả lời là "không", **toàn bộ kế hoạch dừng lại ở đây** — vì SQLWF không tự chạy SQL, nó chỉ gửi SQL đi.
>
> Đây là câu hỏi cần trả lời **đầu tiên**, trước cả việc chọn Hudi hay Iceberg.

---
---

# PHẦN D — THỊ TRƯỜNG & ĐỀ XUẤT

## 14. Nghiên cứu thị trường

### 14.1. Cách phân loại thị trường (để không bị rối)

Thị trường Data Management chia thành **4 nhóm sản phẩm khác nhau** — nhiều người nhầm lẫn giữa chúng:

| Nhóm | Giải quyết việc gì | Tương ứng trụ nào của ta |
|---|---|---|
| **1. Data Catalog / Governance** | Danh mục dữ liệu, tìm kiếm, từ điển, nguồn gốc, chủ sở hữu, nhãn phân loại | **Metadata** |
| **2. Data Quality / Observability** | Luật kiểm tra, phát hiện bất thường, cảnh báo, điểm chất lượng | **Data Quality** |
| **3. Data Access Control** | Phân quyền cột/dòng, che dữ liệu, chính sách theo nhãn | **Data Security** |
| **4. Lakehouse Catalog** | Danh mục bảng cho Iceberg/Hudi + quyền ở tầng catalog | **Nền tảng cho cả 3** |

### 14.2. NHÓM 1 — Data Catalog / Metadata

#### ⭐ OpenMetadata — **ưu tiên nghiên cứu số 1**

| Mục | Nội dung |
|---|---|
| **Loại** | Mã nguồn mở, miễn phí hoàn toàn |
| **Dùng thử** | ✅ **Có 2 cách, không cần liên hệ sales**: (1) bản demo trực tuyến sẵn có; (2) chạy bằng Docker — tài liệu ghi khoảng 5 phút, giao diện ở `localhost:8585` |
| **Vì sao hợp SQLWF** | Là tool duy nhất gộp **cả 3 trụ trong 1 sản phẩm**: catalog + lineage mức cột + data quality + phân loại/nhãn PII. Chính là mô hình "1 lục địa" mà ta muốn hướng tới |
| **Cần xem cụ thể** | • Màn "hồ sơ một bảng" — cách họ gộp mô tả + chất lượng + nguồn gốc + quyền vào 1 chỗ<br>• Lineage **mức cột** trông thế nào<br>• Cách khai luật chất lượng không cần code<br>• Cách gắn nhãn PII và áp chính sách theo nhãn<br>• Cách gắn thuật ngữ nghiệp vụ vào cột thật (giải quyết N8) |
| **Cần cảnh giác** | Kết nối tới nguồn dữ liệu qua các "connector" có sẵn — **SQLWF không nằm trong danh sách** ⚠️. Cần xem họ có API để đẩy metadata vào không |
| **Nguồn** | [Quickstart](https://docs.open-metadata.org/v1.12.x/quick-start) · [GitHub](https://github.com/open-metadata/OpenMetadata) · [Lineage view](https://docs.open-metadata.org/v1.12.x/how-to-guides/data-lineage/explore) |

#### DataHub — **ưu tiên số 2**

| Mục | Nội dung |
|---|---|
| **Loại** | Mã nguồn mở (bản Core miễn phí), có bản Cloud trả phí |
| **Dùng thử** | ✅ Cài bằng lệnh `datahub docker quickstart`, giao diện ở `localhost:9002`, tài khoản mặc định `datahub/datahub`. Có sẵn dữ liệu mẫu kèm lineage |
| **Vì sao đáng xem** | Mạnh nhất về **lineage mức cột tự động bằng cách phân tích câu SQL** — đúng thứ SQLWF cần, vì SQLWF **đã có sẵn toàn bộ câu SQL của mọi job**. Có khái niệm **"hợp đồng dữ liệu" (data contract)** |
| **Cần xem cụ thể** | • Bộ phân tích SQL sinh lineage cột hoạt động ra sao<br>• Data contract là gì, dùng thế nào |
| **Cần cảnh giác** | Nặng hơn OpenMetadata đáng kể (cần Kafka, Elasticsearch…). Tài liệu so sánh ước tính ~10 dịch vụ so với ~4 của OpenMetadata. Không phù hợp nếu chỉ muốn thử nhanh |
| **Nguồn** | [Quickstart](https://docs.datahub.com/docs/quickstart) · [Column-level lineage](https://datahub.com/blog/column-level-lineage-comes-to-datahub/) · [SQL parser](https://datahub.com/blog/extracting-column-level-lineage-from-sql/) |

#### Apache Atlas — **xem để tham khảo, không khuyến nghị triển khai**

Sinh ra cho hệ sinh thái Hadoop (Hive, HBase, Kafka, Spark), tích hợp sẵn với Apache Ranger. **Về lý thuyết là tool "gần SQLWF nhất" về công nghệ nền.** Nhưng cộng đồng đã chậm lại nhiều so với 2 tool trên.
→ **Nên xem** vì mô hình phân loại (classification) + tích hợp Ranger là chính xác thứ SQLWF thiếu (S4).

#### Amundsen — chỉ để tham khảo giao diện tìm kiếm

Nhẹ, dễ cài, tập trung vào tìm kiếm/khám phá dữ liệu. Dùng Neo4j làm nền — **giống SQLWF**. Nhưng lộ trình phát triển đã chững lại, ít tính năng quản trị.

#### Marquez / OpenLineage — **chỉ giải quyết lineage, nhưng rất đáng xem**

| Mục | Nội dung |
|---|---|
| **Loại** | Mã nguồn mở, miễn phí |
| **Dùng thử** | ✅ Có sẵn docker-compose |
| **Vì sao rất hợp SQLWF** | **OpenLineage là chuẩn mở về nguồn gốc dữ liệu.** Với Spark, lineage mức cột được bật **mặc định, không cần cấu hình thêm**. Vì TaskUtil chạy Spark → về lý thuyết chỉ cần bật listener là có lineage cột tự động ⚠️ |
| **Cần xem cụ thể** | • Cách bật OpenLineage trên Spark<br>• Dữ liệu lineage cột trả về trông thế nào<br>• Có ghép được vào Neo4j hiện có không, hay phải thay |
| **Nguồn** | [OpenLineage Spark](https://openlineage.io/docs/guides/spark/) · [Column lineage](https://openlineage.io/docs/integrations/spark/spark_column_lineage/) · [Marquez](https://marquezproject.ai/blog/column-lineage-demo/) |

#### Tool thương mại có bản miễn phí (dùng thử nhanh, không cần demo)

| Tool | Bản miễn phí | Ghi chú |
|---|---|---|
| **Secoda** | ✅ Có gói **miễn phí vĩnh viễn** | Giao diện rất gọn, hợp để **lấy cảm hứng thiết kế UI**. ⚠️ Trang đăng ký vẫn có hướng đặt lịch gặp — nên vào thẳng trang pricing |
| **Select Star** | ✅ Có gói Light miễn phí + dùng thử 14 ngày | Quảng cáo **cài trong ~15 phút**, có lineage mức cột và sơ đồ quan hệ. Tốt để xem "trải nghiệm chuẩn" trông ra sao |
| **Atlan, Collibra, Alation** | ❌ Phải liên hệ sales | **Không nên mất thời gian** cho mục tiêu cuối tuần. Chỉ đọc blog của họ để lấy khung tư duy |

**Nguồn:** [Secoda pricing](https://www.secoda.co/pricing) · [Select Star](https://www.getapp.com/business-intelligence-analytics-software/a/select-star/)

---

### 14.3. NHÓM 2 — Data Quality / Observability

> Đây là nhóm **quan trọng nhất** cần nghiên cứu, vì đúng điểm yếu lớn nhất của SQLWF (mục 10).

#### ⭐ Soda Core / Soda Cloud — **ưu tiên nghiên cứu số 1 cho DQ**

| Mục | Nội dung |
|---|---|
| **Dùng thử** | ✅ **Gói Free $0/tháng, không cần thẻ tín dụng** |
| **Vì sao hợp nhất** | Luật viết bằng cú pháp **khai báo, gần với ngôn ngữ tự nhiên**, người làm nghiệp vụ đọc hiểu được — không cần lập trình. Đây **chính xác là thứ SQLWF thiếu** |
| **Ví dụ luật của Soda** (để so với SQLWF) | `missing_count(customer_id) = 0`<br>`invalid_percent(phone) < 1% với định dạng ...`<br>`duplicate_count(order_id) = 0`<br>`row_count between 1000 and 5000`<br>`freshness(created_at) < 1d` |
| **Cần xem cụ thể** | • **Danh mục đầy đủ các loại luật** → dùng làm danh sách yêu cầu bổ sung cho SQLWF<br>• Cách khai luật tham chiếu (mã có trong danh mục không)<br>• Cách phát hiện bất thường tự động<br>• Cách hiển thị kết quả & điểm chất lượng |
| **Lưu ý** | Soda Core dùng giấy phép Elastic License 2.0 (mã nguồn mở có điều kiện), ⚠️ cần đọc kỹ nếu định dùng lại mã |
| **Nguồn** | [Soda pricing](https://datastackindex.com/data-observability/tools/soda/) |

#### Great Expectations — **xem để lấy danh mục luật**

| Mục | Nội dung |
|---|---|
| **Dùng thử** | ✅ Mã nguồn mở, có bản Cloud với gói miễn phí |
| **Vì sao đáng xem** | Bộ luật kiểm tra **phong phú nhất thị trường** (hàng trăm loại "expectation"). Tạo ra **tài liệu chất lượng dạng web tự động** — mỗi lần chạy sinh ra một trang báo cáo đọc được |
| **Cần xem cụ thể** | • **Danh sách các "expectation"** → đây là danh mục yêu cầu tốt nhất để đối chiếu với 14 chỉ số của SQLWF<br>• Cách trình bày báo cáo chất lượng |
| **Cảnh giác** | Cài đặt và cấu hình phức tạp, cần lập trình Python. **Không phù hợp để bắt chước cách triển khai** — chỉ nên học **danh mục luật** và **cách trình bày** |

#### Amazon Deequ — **rất đáng xem vì cùng nền Spark**

| Mục | Nội dung |
|---|---|
| **Vì sao hợp SQLWF** | Chạy **trên Spark** — cùng nền với TaskUtil. Thiết kế để đo chất lượng trên **dữ liệu rất lớn mà không cần lấy mẫu**. Có sẵn cơ chế **phát hiện bất thường theo lịch sử** |
| **Cần xem cụ thể** | Danh mục "constraint" của Deequ và cách nó tính toán hiệu quả trên Spark — vì nếu bổ sung DQ cho SQLWF, khả năng cao sẽ chạy trên chính Spark của TaskUtil |

#### Metaplane (Datadog) — xem để lấy ý tưởng về phát hiện bất thường

| Mục | Nội dung |
|---|---|
| **Dùng thử** | ✅ **Miễn phí, không cần thẻ**, cài dưới 15 phút. Gói miễn phí giám sát ~10 bảng, có lineage mức cột |
| **Vì sao đáng xem** | Tự động phát hiện bất thường về **độ tươi, khối lượng, cấu trúc, tỉ lệ trống, tính duy nhất, phân bố** — bằng máy học, **không cần khai ngưỡng bằng tay**.<br>**Đối chiếu:** SQLWF hiện bắt người dùng **khai tay từng ngưỡng min/max** — đó chính là lý do người dùng hỏi "tôi cần thông tin này để làm gì". Cách làm hiện đại là **hệ thống tự học ngưỡng** |
| **Nguồn** | [Metaplane pricing](https://www.metaplane.dev/pricing) |

#### Elementary — chỉ xem nếu có thời gian

Miễn phí ở dạng gói mã nguồn mở (gắn với dbt). Ít liên quan trực tiếp vì SQLWF không dùng dbt.

---

### 14.4. NHÓM 3 — Data Access Control (Security)

#### ⭐ Apache Ranger — **ưu tiên nghiên cứu số 1 cho Security**

| Mục | Nội dung |
|---|---|
| **Loại** | Mã nguồn mở, miễn phí |
| **Dùng thử** | 🟡 Cài đặt phức tạp hơn (cần môi trường Hadoop). **Khuyến nghị: đọc tài liệu + xem ảnh màn hình thay vì cố cài** |
| **Vì sao PHẢI xem** | Ranger có sẵn **đúng 3 thứ SQLWF thiếu nhất**:<br>1. **Che dữ liệu theo cột (column masking)** — VD chỉ hiện 4 ký tự cuối<br>2. **Lọc theo dòng (row-level filter)** — VD chỉ thấy dữ liệu tỉnh mình<br>3. **Chính sách theo NHÃN (tag-based policy)** — gắn nhãn "PII" một lần, chính sách tự áp cho mọi cột có nhãn đó |
| **Cơ chế hay cần hiểu** | Ranger thực thi bằng cách **viết lại câu truy vấn trước khi chạy** — người dùng không hề biết có dòng/cột bị ẩn. Dữ liệu gốc **không bị sao chép hay chỉnh sửa** |
| **Cần xem cụ thể** | • Màn tạo chính sách masking trông thế nào (để thiết kế màn tương tự cho SQLWF)<br>• Cách gắn nhãn + chính sách theo nhãn<br>• Cách phân biệt "cho phép / từ chối / ngoại lệ" |
| **Cảnh giác** | Tài liệu ghi rõ: chính sách dùng ký tự đại diện (`*`) dễ gây xung đột khó lường; user có quyền `ALTER` bảng có thể vượt qua chính sách masking |
| **Nguồn** | [Ranger policy model](https://ranger.apache.org/blogs/policy_model.html) · [Row filter & column masking](https://cwiki.apache.org/confluence/display/RANGER/Row-level+filtering+and+column-masking+using+Apache+Ranger+policies+in+Apache+Hive) |

#### Open Policy Agent (OPA) — **SQLWF ĐÃ DÙNG rồi, cần làm rõ đang dùng tới đâu**

SQLWF đã có tích hợp gửi danh sách cấm sang OPA Collector.
→ **Việc cần làm không phải "nghiên cứu OPA có tốt không", mà là "OPA trong SQLWF hiện đang thực sự làm gì"** ⚠️ — đây là câu hỏi cho đội phát triển, không phải cho Google.

#### Immuta / Privacera — chỉ đọc tài liệu marketing

Cả hai đều **phải liên hệ sales**, không dùng thử được. Nhưng blog của họ giải thích rất tốt các khái niệm: chính sách theo thuộc tính, che dữ liệu động, tự động phát hiện dữ liệu nhạy cảm.
→ **Chỉ đọc để lấy khung khái niệm và từ vựng cho báo cáo.**

---

### 14.5. NHÓM 4 — Lakehouse Catalog (nền tảng cho Hudi/Iceberg)

> Nhóm này quan trọng vì như mục 13.6 đã nêu: **muốn có Iceberg thì phải có catalog trước**.

Bối cảnh thị trường 2026: **câu chuyện định dạng bảng đã ngã ngũ — Iceberg thắng.** Câu hỏi còn lại của thị trường là **chọn catalog nào**.

| Tool | Đặc điểm | Có đáng xem cho SQLWF? |
|---|---|---|
| **Hive Metastore** | Cách truyền thống, có sẵn trong hệ sinh thái Hadoop | ✅ Đáng xem — **có thể môi trường Hadoop của công ty đã có sẵn** ⚠️ cần hỏi |
| **Apache Polaris** | Đã thành dự án cấp cao của Apache (02/2026). Có **phân quyền chi tiết** + **cấp chứng chỉ truy cập tạm thời** thay vì đưa khoá dài hạn | ✅ Đáng xem — hướng đi chuẩn của thị trường |
| **Lakekeeper** | Nhẹ (1 file chạy, không cần Java), **tích hợp sẵn với OPA** | ⭐ **Đáng xem nhất** — vì **SQLWF đã dùng OPA rồi**. Đây là điểm khớp kiến trúc hiếm có |
| **Nessie** | Cho phép "phân nhánh" dữ liệu kiểu Git | 🟡 Chỉ xem nếu quan tâm kiểm thử dữ liệu |

**Xu hướng quan trọng cần đưa vào báo cáo:**
> Thị trường 2026 đang thống nhất rằng **"quản trị nên nằm ở tầng catalog"** — tức là định nghĩa quyền, nguồn gốc, kiểm toán **một lần ở catalog**, rồi mọi công cụ truy vấn (Spark, Trino…) đều tuân theo. Thay vì mỗi công cụ tự quản một kiểu.
>
> **Điều này khớp chính xác với vấn đề "3 trụ rời rạc" của SQLWF** — và gợi ý rằng lời giải dài hạn không phải là "nối 3 module lại", mà là **"dựng một tầng catalog để cả 3 trụ cùng dựa vào"**.

**Nguồn:** [Iceberg catalogs 2026](https://amdatalakehouse.substack.com/p/the-state-of-apache-iceberg-catalogs) · [Lakekeeper docs](https://docs.lakekeeper.io/) · [Catalog comparison](https://risingwave.com/blog/iceberg-catalog-comparison-guide/)

---

### 14.6. Bảng tổng hợp: tool nào dùng thử được ngay, không cần request demo

| Tool | Nhóm | Miễn phí? | Cần liên hệ sales? | Thời gian cài | Ưu tiên |
|---|---|---|---|---|---|
| **OpenMetadata** | Catalog + DQ + Security | ✅ Hoàn toàn | ❌ Không | ~5–30 phút (Docker) hoặc dùng bản demo online | ⭐⭐⭐ **Số 1** |
| **Soda Cloud** | Data Quality | ✅ Gói Free, không cần thẻ | ❌ Không | ~15 phút | ⭐⭐⭐ **Số 1 cho DQ** |
| **Metaplane** | Observability | ✅ Miễn phí, không cần thẻ | ❌ Không | <15 phút | ⭐⭐ |
| **Select Star** | Catalog | ✅ Gói Light + thử 14 ngày | 🟡 Có hướng demo | ~15 phút | ⭐⭐ |
| **Secoda** | Catalog | ✅ Miễn phí vĩnh viễn | 🟡 Có hướng demo | ~15 phút | ⭐⭐ |
| **DataHub** | Catalog + Lineage | ✅ Bản Core | ❌ Không | ~30–60 phút, máy cần ≥8GB RAM | ⭐⭐ |
| **Marquez/OpenLineage** | Lineage | ✅ | ❌ Không | ~30 phút | ⭐⭐ |
| **Great Expectations** | Data Quality | ✅ | ❌ Không | Vài giờ | ⭐ (chỉ đọc tài liệu) |
| **Apache Ranger** | Security | ✅ | ❌ Không | Khó cài | ⭐⭐⭐ **đọc tài liệu, không cần cài** |
| **Apache Atlas** | Catalog | ✅ | ❌ Không | Khó cài | ⭐ (chỉ đọc) |
| **Lakekeeper** | Iceberg catalog | ✅ | ❌ Không | ~15 phút | ⭐⭐ |
| Atlan / Collibra / Alation / Immuta | Đủ loại | ❌ | ✅ Bắt buộc | – | ⭐ (chỉ đọc blog) |

---

## 15. So khớp SQLWF ↔ thị trường

### 15.1. Trụ METADATA

| Tính năng | SQLWF | Thị trường | Kết luận |
|---|---|---|---|
| Mô tả bảng, chủ sở hữu, domain | ✅ Đầy đủ | ✅ | **Ngang bằng** |
| Từ điển nghiệp vụ | ✅ Có | ✅ | **Ngang bằng** — nhưng ta chưa gắn vào cột thật ⚠️ |
| Lineage mức **bảng** | ✅ Có (Neo4j) | ✅ | **Ngang bằng** |
| Lineage mức **cột** | ❌ | ✅ Chuẩn mực | 🔴 **Thiếu** |
| Lineage tới báo cáo/dashboard | ❌ | ✅ | 🔴 **Thiếu** |
| Độ tươi dữ liệu | ❌ | ✅ | 🔴 **Thiếu** |
| Lịch sử thay đổi cấu trúc | 🟡 Chỉ trong audit thô | ✅ Có màn riêng | 🟠 **Yếu** |
| Nhãn phân loại (PII…) | ❌ (chỉ có cờ nhạy cảm mức nhóm bảng) | ✅ Cốt lõi | 🔴 **Thiếu** |
| Tự phát hiện dữ liệu nhạy cảm | ❌ | ✅ | 🔴 **Thiếu** |
| Tìm kiếm/khám phá dữ liệu | 🟡 Chỉ có tìm theo tên | ✅ Tìm kiếm ngữ nghĩa | 🟠 **Yếu** |
| Chỉ số mức độ sử dụng | ❌ | ✅ | 🟠 **Thiếu** |
| Đối chiếu metadata với thực tế | ❌ | ✅ Tự động | 🔴 **Thiếu** |
| Phiên bản + feedback cho từ điển | ✅ **Có** | 🟡 Không phải tool nào cũng có | 🟢 **SQLWF nhỉnh hơn** |

### 15.2. Trụ DATA QUALITY

| Tính năng | SQLWF | Thị trường | Kết luận |
|---|---|---|---|
| Khung 6 chiều chất lượng | ✅ Có khai báo | ✅ | **Ngang** — nhưng 2/6 chiều rỗng |
| Chỉ số thống kê (profiling) | ✅ 11 chỉ số | ✅ | 🟢 **Ngang bằng** |
| Kiểm tra độ tươi / đúng giờ | ✅ | ✅ | **Ngang bằng** |
| Kiểm tra số dòng / kích thước | ✅ | ✅ | **Ngang bằng** |
| **Luật định dạng (regex)** | ❌ | ✅ Cơ bản | 🔴 **Thiếu** |
| **Tỉ lệ giá trị trống (%)** | ❌ | ✅ Cơ bản | 🔴 **Thiếu** |
| **Luật biểu thức tuỳ ý (SQL)** | ❌ ⚠️ có trường `dqExpr` nhưng chưa rõ dùng được chưa | ✅ Cơ bản | 🔴 **Thiếu** |
| **Kiểm tra tham chiếu danh mục** | ❌ | ✅ | 🔴 **Thiếu** |
| **Kiểm tra nhất quán giữa bảng** | ❌ (chiều CONSISTENCY rỗng) | ✅ | 🔴 **Thiếu** |
| **Tự học ngưỡng / phát hiện bất thường** | 🟡 Có `dqComparedCycle`, chưa rõ dùng đến đâu ⚠️ | ✅ Đã thành chuẩn | 🟠 **Yếu** |
| **Điểm chất lượng tổng hợp** | ❌ | ✅ | 🔴 **Thiếu** |
| **Mức độ nghiêm trọng của lỗi** | ❌ | ✅ | 🟠 **Thiếu** |
| **Chặn dữ liệu xấu tại cửa nạp** | ❌ | ✅ | 🔴 **Thiếu** |
| **Quy trình xử lý sau cảnh báo** | ❌ | ✅ | 🔴 **Thiếu** |
| **Hiện chất lượng ngay chỗ xem dữ liệu** | ❌ | ✅ | 🔴 **Thiếu** |
| Cảnh báo đa kênh (email/SMS/Telegram) | ✅ | 🟡 Thường chỉ email/Slack | 🟢 **SQLWF nhỉnh hơn** |
| Cấu hình chu kỳ chi tiết (offset, delay) | ✅ **Rất chi tiết** | 🟡 | 🟢 **SQLWF nhỉnh hơn** |

### 15.3. Trụ DATA SECURITY

| Tính năng | SQLWF | Thị trường | Kết luận |
|---|---|---|---|
| Phân quyền mức bảng | ✅ | ✅ | **Ngang bằng** |
| Phân quyền theo nhóm | ✅ | ✅ | **Ngang bằng** |
| **Phân quyền mức cột** | ❌ | ✅ | 🔴 **Thiếu** |
| **Che dữ liệu động (masking)** | ❌ | ✅ | 🔴 **Thiếu** |
| **Lọc theo dòng** | ❌ | ✅ | 🔴 **Thiếu** |
| **Chính sách theo nhãn** | ❌ | ✅ | 🔴 **Thiếu** |
| Kiểm soát theo IP | ✅ **có IP riêng cho dữ liệu nhạy cảm** | 🟡 Ít tool có | 🟢 **SQLWF nhỉnh hơn** |
| Giới hạn số truy vấn đồng thời | ✅ | 🟡 | 🟢 **SQLWF nhỉnh hơn** |
| Chặn hàm SQL theo nhãn user | ✅ **Query Guard** | 🟡 Hiếm tool có | 🟢 **SQLWF nhỉnh hơn** |
| Audit log chi tiết (cũ→mới, IP) | ✅ | ✅ | **Ngang bằng** |
| Phân tích hành vi từ audit | ❌ | ✅ | 🟠 **Thiếu** |
| Quy trình xin/cấp quyền | ❌ | ✅ | 🟠 **Thiếu** |
| Quyền có thời hạn | ❌ | ✅ | 🟠 **Thiếu** |
| **Một nơi duy nhất xem toàn bộ quyền của 1 người** | ❌ | ✅ | 🔴 **Thiếu** |
| Vùng lưu trữ mã hoá riêng | ✅ | 🟡 | 🟢 **SQLWF nhỉnh hơn** |

### 15.4. Kết luận so khớp — 4 câu

1. **SQLWF không hề yếu.** Ở nhiều điểm (kiểm soát IP theo độ nhạy cảm, chặn hàm SQL, cấu hình chu kỳ DQ, đa kênh cảnh báo, vùng mã hoá) SQLWF **nhỉnh hơn** mặt bằng tool phổ thông.

2. **Khoảng cách lớn nhất nằm ở MỨC ĐỘ CHI TIẾT: thị trường làm việc ở mức CỘT, SQLWF dừng ở mức BẢNG.** Lineage cột, quyền cột, nhãn cột, che dữ liệu cột — đây là 4 thiếu sót cùng một gốc.

3. **Khoảng cách lớn thứ hai là TÍNH LIÊN KẾT.** Thị trường bán "một hồ sơ dữ liệu duy nhất"; SQLWF có đủ nguyên liệu nhưng để rời ở 4 kho.

4. **Khoảng cách lớn thứ ba, riêng ở DQ, là BẢN CHẤT CHỈ SỐ.** SQLWF đo *"dữ liệu trông như thế nào"* (thống kê); thị trường kiểm *"dữ liệu có đúng quy định nghiệp vụ không"* (luật). **Đây chính là lý do prototype trước bị đánh giá "chưa trả lời được vì sao cần thông tin đó".**

---

## 16. Đề xuất

### 16.1. Ba nguyên tắc đề xuất

> **Nguyên tắc 1 — Không thay thế SQLWF bằng tool thị trường.**
> SQLWF gắn chặt với nghiệp vụ nội bộ (đối soát, leadgen, tài chính…), tool thị trường không thay được. **Học cách làm, không mua đứt.**

> **Nguyên tắc 2 — Ưu tiên NỐI cái đang có, trước khi XÂY cái mới.**
> Nhiều thiếu sót có thể lấp bằng nguyên liệu đã có: chiều CONSISTENCY lấp bằng kết quả đối soát; chiều VALIDITY lấp bằng danh mục sẵn có; độ tươi dữ liệu lấy từ nhật ký Iceberg. **Nối rẻ hơn xây rất nhiều.**

> **Nguyên tắc 3 — Mọi thứ nâng cao đều cần xuống tới mức CỘT.**
> Nếu chỉ được chọn một hướng đầu tư dài hạn: **đưa đơn vị quản trị từ BẢNG xuống CỘT.**

### 16.2. Đề xuất theo 4 làn

#### LÀN 1 — Việc "nối", làm được ngay, không cần hạ tầng mới

| # | Việc | Nối mối nào | Giá trị |
|---|---|---|---|
| 1.1 | Đưa **điểm chất lượng + số lỗi đang mở** lên màn Quản lý bảng và màn danh sách bảng | N1 | Cao — người dùng thấy ngay bảng nào đáng tin |
| 1.2 | Ghi **kết quả đối soát** thành chỉ số DQ thuộc chiều CONSISTENCY | N5 | Cao — lấp chiều rỗng bằng thứ đã có |
| 1.3 | Thêm loại luật **"giá trị phải có trong danh mục X"**, lấy từ module Quản lý danh mục | N6 | Rất cao — lấp chiều VALIDITY, đúng nhu cầu thực tế |
| 1.4 | Bổ sung 4 loại luật cơ bản: **tỉ lệ trống (%)**, **định dạng (regex)**, **biểu thức SQL tuỳ ý**, **so sánh giữa 2 cột** | Q1 | Rất cao — đây là thứ người dùng thực sự hỏi |
| 1.5 | Gắn **thuật ngữ Glossary vào cột** của bảng | N8 | Cao — Glossary hết "mồ côi" |
| 1.6 | Thêm **mức độ nghiêm trọng** cho luật DQ (Cảnh báo / Nghiêm trọng / Chặn) | Q6 | Trung bình |
| 1.7 | Màn **"Người này đang xem được gì"** — gộp quyền từ cả 4 nguồn | S7, N4 | Rất cao — trả lời câu hỏi kiểm toán số 1 |
| 1.8 | Job đối chiếu **metadata khai báo vs dữ liệu thật** (cột, kích thước, tồn tại) | M7 | Cao — phát hiện bảng "ma" và dữ liệu "mồ côi" |

#### LÀN 2 — Xuống mức CỘT

| # | Việc | Ghi chú |
|---|---|---|
| 2.1 | Thêm **nhãn phân loại ở mức cột** (PII / Nhạy cảm / Nội bộ / Công khai) vào schema của bảng | Nền tảng cho mọi thứ sau. Học mô hình classification của Apache Atlas |
| 2.2 | **Quét tự động gợi ý cột nhạy cảm** (theo tên cột + mẫu dữ liệu) | Học từ tool thị trường |
| 2.3 | **Lineage mức cột** | Ưu tiên: thử OpenLineage trên Spark trước (có thể gần như miễn phí công sức), phương án 2 là tự phân tích SQL job đã có |
| 2.4 | **Che dữ liệu theo cột** dựa trên nhãn | Học mô hình Ranger. ⚠️ Phụ thuộc TaskUtil có hỗ trợ viết lại truy vấn không |
| 2.5 | **Lọc theo dòng** | Tương tự 2.4 |

#### LÀN 3 — Nền tảng Lakehouse (Iceberg)

| # | Việc | Ghi chú |
|---|---|---|
| 3.0 | **Hỏi đội TaskUtil: Spark phiên bản mấy, nạp được thư viện Iceberg không?** | ⚠️ **Cửa chặn. Làm trước tiên.** |
| 3.1 | Chọn & dựng **catalog** | Ưu tiên xem: Hive Metastore (nếu hạ tầng đã có), Lakekeeper (vì khớp OPA sẵn có) |
| 3.2 | Thêm trường **`format`** vào metadata bảng: `parquet` / `csv` / `iceberg` | Đây là "thêm type" mà chị nhắc — nhưng phải kèm 3.1 mới có ý nghĩa |
| 3.3 | Thử nghiệm **1 bảng đối soát** chuyển sang Iceberg | Đo: tốc độ nạp, số file sinh ra, có xem lại được quá khứ không |
| 3.4 | Dùng **`mergeBy` đã có sẵn** làm khoá cho câu lệnh `MERGE INTO`, thay cơ chế `_TMP` + ghi đè | Ít công sửa nhất, lợi ích lớn nhất |
| 3.5 | Lấy **độ tươi dữ liệu + lịch sử thay đổi cấu trúc** từ nhật ký Iceberg, đổ vào trụ Metadata | Lấp M3 và M4 gần như miễn phí |

**Về việc chọn Hudi hay Iceberg — đề xuất rõ ràng:**

> **Chọn Iceberg làm mặc định. Chưa triển khai Hudi.**
>
> Lý do:
> 1. Nút thắt thật của SQLWF là **đối soát/xem lại quá khứ + đa công cụ + metadata**, không phải cập nhật thời gian thực. Đây đúng thế mạnh Iceberg.
> 2. Trong hệ thống hiện tại **chưa thấy luồng bắt thay đổi liên tục (CDC)** — là chỗ Hudi thắng rõ. Hudi giải quyết một vấn đề SQLWF **chưa có**.
> 3. Hudi cần tinh chỉnh vận hành liên tục (gộp file, dọn dẹp), trong khi SQLWF chỉ có **một đường ghi duy nhất là "gửi câu SQL cho TaskUtil"** — không có chỗ đặt cơ chế ghi chuyên dụng.
> 4. Chạy song song 2 định dạng = 2 bộ vận hành, 2 bộ kiến thức, 2 nhánh code — **chi phí gấp đôi, lợi ích cận biên**.
>
> **Về mặt màn hình:** vẫn nên thiết kế ô "Định dạng bảng" cho phép **4 giá trị** (`parquet`, `csv`, `iceberg`, `hudi`) để không phải sửa lại sau, nhưng **giai đoạn 1 chỉ mở `iceberg`**, `hudi` để trạng thái chưa kích hoạt.

#### LÀN 4 — Quy trình & con người (không cần code nhiều)

| # | Việc |
|---|---|
| 4.1 | Quy định: bảng mới **bắt buộc** khai chủ sở hữu + domain + phân loại độ nhạy cảm mới được duyệt |
| 4.2 | Quy trình xử lý sau cảnh báo DQ: ai nhận, bao lâu phải phản hồi, đóng lỗi thế nào |
| 4.3 | Rà soát quyền định kỳ (quý), thu hồi quyền không dùng |
| 4.4 | Thống nhất **1 bộ từ vựng chung** cho 3 trụ (tránh mỗi module gọi một kiểu) |

### 16.3. Nếu chỉ được chọn 3 việc

| Thứ tự | Việc | Vì sao |
|---|---|---|
| **1** | **Bổ sung luật nghiệp vụ cho DQ** (tỉ lệ trống, định dạng, tham chiếu danh mục, biểu thức tuỳ ý) + đưa **điểm chất lượng** lên màn Quản lý bảng | Trả lời trực tiếp nhận xét *"chưa biết vì sao cần thông tin đó"*. Không cần hạ tầng mới. Thấy kết quả ngay |
| **2** | **Nhãn phân loại mức cột** (PII/Nhạy cảm/…) | Là nền tảng chung cho **cả 3 trụ**: Metadata có phân loại, Security áp chính sách theo nhãn, DQ ưu tiên kiểm cột quan trọng. **Một việc, ba trụ cùng hưởng** |
| **3** | **Hỏi TaskUtil về Iceberg, rồi thử nghiệm 1 bảng đối soát** | Mở đường cho time-travel (đối soát) + độ tươi dữ liệu + lịch sử schema. Nhưng phải xác nhận khả thi trước |

---

## 17. Kế hoạch nghiên cứu cuối tuần

> Thiết kế để **không cần source code SQLWF**. Tổng ~6–8 giờ, chia 4 buổi.

### Buổi 1 (~2h) — Xem tool "3 trong 1" hoạt động thế nào
**Tool:** OpenMetadata (bản demo online, hoặc Docker nếu tiện)

- [ ] Mở **hồ sơ một bảng** — chụp màn hình. Ghi lại: họ hiển thị bao nhiêu khối thông tin trên 1 màn?
- [ ] Xem **lineage mức cột** — so với lineage mức bảng của ta, khác biệt ở đâu?
- [ ] Xem cách khai **luật chất lượng** — có cần code không? Có bao nhiêu loại luật?
- [ ] Xem cách gắn **nhãn phân loại** và chính sách theo nhãn
- [ ] Xem cách **thuật ngữ nghiệp vụ gắn vào cột**
- 📝 **Đầu ra:** 5–8 ảnh chụp màn hình + ghi chú "SQLWF nên học điều gì"

### Buổi 2 (~2h) — Lấy danh mục luật chất lượng
**Tool:** Soda (tài liệu + gói Free) và Great Expectations (chỉ tài liệu)

- [ ] Liệt kê **toàn bộ loại luật** Soda hỗ trợ → lập bảng đối chiếu với **14 chỉ số** của SQLWF
- [ ] Tìm cách họ khai luật **tham chiếu danh mục** và luật **so sánh giữa 2 bảng**
- [ ] Xem cách **phát hiện bất thường tự động** (không cần khai ngưỡng tay)
- [ ] Xem cách hiển thị **điểm chất lượng** và báo cáo
- 📝 **Đầu ra:** **Bảng "Danh mục luật DQ đề xuất cho SQLWF"** — đây là sản phẩm quan trọng nhất của cuối tuần, dùng trực tiếp làm yêu cầu phần mềm

### Buổi 3 (~1,5h) — Học mô hình bảo mật mức cột
**Tool:** Apache Ranger (chỉ đọc tài liệu + ảnh màn hình, **không cần cài**)

- [ ] Xem màn tạo chính sách **che dữ liệu theo cột** — có những kiểu che nào?
- [ ] Xem chính sách **lọc theo dòng** — khai điều kiện thế nào?
- [ ] Hiểu **chính sách theo nhãn** — gắn nhãn 1 lần, áp cho nhiều cột
- [ ] Ghi lại các bẫy đã biết (xung đột ký tự đại diện, lỗ hổng quyền ALTER)
- 📝 **Đầu ra:** phác thảo màn hình "Chính sách dữ liệu" cho SQLWF

### Buổi 4 (~1,5h) — Lakehouse & catalog
- [ ] Đọc tổng quan về Iceberg catalog 2026 — hiểu vì sao "catalog quan trọng hơn định dạng bảng"
- [ ] Xem **Lakekeeper** — đặc biệt phần tích hợp OPA (vì SQLWF đã dùng OPA)
- [ ] Đọc về **OpenLineage cho Spark** — xác nhận lineage cột có thực sự "bật là có"
- [ ] (Nếu còn thời gian) Đăng ký **Metaplane** hoặc **Select Star** miễn phí để xem trải nghiệm chuẩn
- 📝 **Đầu ra:** kết luận "SQLWF nên dựng catalog nào" + đánh giá độ khả thi lineage cột

### Sản phẩm cuối tuần
1. ✅ Bảng **danh mục luật DQ đề xuất** (quan trọng nhất)
2. ✅ Bộ ảnh chụp màn hình tham chiếu cho thiết kế UI
3. ✅ Phác thảo màn "Hồ sơ bảng dữ liệu" gộp 3 trụ
4. ✅ Kết luận về catalog + tính khả thi của lineage cột
5. ✅ Danh sách câu hỏi cho đội phát triển (xem P4)

---
---

# PHỤ LỤC

## P1. Từ điển thuật ngữ

| Thuật ngữ | Giải thích 1 câu |
|---|---|
| **HDFS** | "Ổ cứng khổng lồ" ghép từ nhiều máy, chứa được file rất lớn |
| **Parquet** | Định dạng file lưu bảng theo cột, nén tốt, đọc nhanh khi chỉ cần vài cột |
| **Partition (phân vùng)** | Chia bảng thành thư mục con theo một cột (thường theo ngày) để tìm nhanh |
| **Zone (vùng lưu trữ)** | Cách SQLWF chia HDFS theo mục đích: thô / làm việc / nghiệp vụ / mã hoá / nhạy cảm |
| **Data Lake** | Kho chứa dữ liệu thô và lớn (ở đây = HDFS + Parquet) |
| **Table format (định dạng bảng)** | Lớp "sổ quản lý" đặt trên file, thêm khả năng như cơ sở dữ liệu (Hudi/Iceberg) |
| **Lakehouse** | Data Lake + tính năng của kho dữ liệu (nhờ table format) |
| **Catalog (danh mục bảng)** | Nơi lưu "bảng nào tên gì, ở đâu, cấu trúc ra sao" — SQLWF hiện **chưa có** |
| **Metastore** | Một dạng catalog truyền thống của hệ sinh thái Hadoop |
| **ACID** | Ghi dữ liệu trọn vẹn: hoặc xong hết, hoặc không thay đổi gì |
| **Upsert** | Cập nhật nếu đã có + thêm mới nếu chưa có (theo khoá) |
| **Merge key / `mergeBy`** | Khoá dùng để xác định "dòng này đã tồn tại chưa" |
| **Time travel** | Xem lại bảng đúng như ở một thời điểm trong quá khứ |
| **Snapshot** | "Ảnh chụp" trạng thái bảng tại một thời điểm |
| **Schema evolution** | Thêm/đổi cột an toàn, không phá dữ liệu và truy vấn cũ |
| **CDC** | Bắt thay đổi (thêm/sửa/xoá) từ nguồn để đồng bộ tiếp |
| **Staging / `_TMP`** | Bảng tạm giữ dữ liệu chờ, trước khi hợp nhất vào bảng chính |
| **Coordinator** | Nền đặt lịch chạy job — trong SQLWF là **Pentaho** ⚠️ |
| **DAG** | Sơ đồ các bước phụ thuộc nhau, không có vòng lặp |
| **Data Lineage** | Sơ đồ nguồn gốc: dữ liệu này từ đâu tới, đi đâu |
| **Column-level lineage** | Lineage chi tiết tới từng cột |
| **Data Profiling** | Mô tả dữ liệu bằng thống kê ("dữ liệu trông thế nào") |
| **Business rule** | Luật nghiệp vụ ("dữ liệu có đúng quy định không") |
| **DQ Score** | Điểm chất lượng tổng hợp của một bảng |
| **PII** | Thông tin định danh cá nhân (tên, CMND, số điện thoại…) |
| **Data Classification** | Gắn nhãn phân loại độ nhạy cảm cho dữ liệu |
| **Dynamic masking** | Che dữ liệu **khi hiển thị**, tuỳ người xem — dữ liệu gốc không đổi |
| **Row-level filter** | Tự động lọc bớt dòng tuỳ theo người xem |
| **Tag-based policy** | Chính sách áp theo nhãn, không phải theo từng cột cụ thể |
| **OPA** | Công cụ quản lý & thực thi chính sách tập trung |
| **Kerberos** | Cơ chế xác thực của hệ sinh thái Hadoop |
| **Audit log** | Nhật ký ghi lại ai làm gì, khi nào, từ đâu |

---

## P2. Danh mục kho dữ liệu & bảng quan trọng

| Kho | Bảng / Collection | Chứa gì | Liên quan trụ nào |
|---|---|---|---|
| **MongoDB** | `tbl_table_info` | **Khai báo bảng** — trung tâm của cả hệ thống | Metadata (+ DQ, Security) |
| MongoDB | `tbl_data_quality` | Kết quả đo DQ từng chu kỳ | Data Quality |
| MongoDB | `tbl_table_group` | Nhóm bảng + mẫu đường dẫn + cờ nhạy cảm | Security |
| MongoDB | `tbl_user_table_group` | User → nhóm bảng, IP, giới hạn truy vấn | Security |
| MongoDB | `tbl_tmp_workflow_info` | Cấu hình job/workflow | Metadata |
| MongoDB | (danh mục) `CategoryRecord`, `CategoryVersion` | Danh mục + phiên bản | Metadata |
| **MariaDB** | `user`, `roles`, `menu_items` | Tài khoản, vai trò, menu | Security |
| MariaDB | `folders`, `folder_data`, `folder_data_authorize`, `user_folder_data` | Phân quyền thư mục HDFS | Security |
| MariaDB | `data_authorize`, `group_authorize`, `menu_items_group` | Phân quyền dữ liệu & nhóm | Security |
| MariaDB | `tag`, `user_tag`, `function`, `tag_function_blacklist`, `tag_action` | Query Guard — chặn hàm SQL theo nhãn | Security |
| MariaDB | `audit_log`, `audit_log_v2` | Nhật ký thao tác (có IP, giá trị cũ/mới) | Security |
| MariaDB | `ip_whitelist`, `ip` | Danh sách IP cho phép | Security |
| **Neo4j** | Nút: Bảng / Job / Bước<br>Quan hệ: `CREATES_TABLE`, `HAS_STEP`, `SOURCE_OF_STEP`, `TARGET_OF_STEP`, `NEXT_STEP` | Data Lineage mức bảng | Metadata |
| **HDFS** | `/storage/<zone>/<domain>/<path>/` | **Dữ liệu thật** (Parquet/CSV) | Tất cả |

---

## P3. Danh sách 22 vùng lưu trữ

| Nhóm | Vùng | Đường dẫn HDFS | Ý nghĩa nghiệp vụ |
|---|---|---|---|
| **Thô** | `raw_zone`, `bi_raw_zone`, `tel_raw_zone`, `common_raw_zone` | `/storage/raw_zone/...` | Dữ liệu vừa nạp, chưa xử lý |
| **Làm việc** | `working_zone`, `bi_working_zone`, `tel_working_zone` | `/storage/working_zone/...` | Đang xử lý dở |
| **Tạm** | `bi_temporary_zone`, `tel_temporary_zone` | `/storage/temporary_zone/...` | Trung gian, có thể xoá |
| **Nghiệp vụ** | `business_zone`, `bi_business_zone`, `tel_business_zone`, `prd_business_zone`, `exp_business_zone` | `/storage/business_zone/...` | **Dữ liệu sẵn sàng dùng** |
| **Chia sẻ** | `tel_share_zone` | `/storage/share_zone/tel/` | Chia sẻ giữa các đơn vị |
| **Bên ngoài** | `tel_external_zone` | `/storage/external_zone/tel/` | Từ nguồn ngoài |
| **🔒 Mã hoá** | `bi_encrypted_zone`, `tel_encrypted_zone`, `prd_encrypted_zone`, `common_encrypted_zone` | `/storage/encrypted_zone/...` | **Dữ liệu đã mã hoá** |
| **🔒 Nhạy cảm** | `sensitive_zone` | `/storage/sensitive_zone/` | **Dữ liệu nhạy cảm nhất** |

*(Ký hiệu: `bi` = Business Intelligence, `tel` = Telecom, `prd` = Products, `exp` = Export/Delivery, `common` = dùng chung)*

---

## P4. Câu hỏi cần xác nhận

### Nhóm A — Chặn kế hoạch (hỏi TRƯỚC TIÊN)
1. **TaskUtil chạy Spark phiên bản mấy? Có nạp thêm được thư viện (Iceberg/Hudi) không?** — *nếu không, toàn bộ phần Hudi/Iceberg dừng lại*
2. **Hạ tầng Hadoop của công ty đã có sẵn Hive Metastore chưa?** — *nếu có, tiết kiệm được cả một hạng mục dựng catalog*
3. **OPA đang thực sự chặn truy cập ở đâu, hay chỉ là nơi đồng bộ danh sách?** — *quyết định độ tin cậy của cả trụ Security*

### Nhóm B — Làm rõ hiện trạng
4. Trường **`dqExpr`** trong cấu hình DQ đã dùng được chưa? Nếu rồi thì khai biểu thức kiểu gì? — *nếu đã dùng được, một phần thiếu sót Q1 tự động biến mất*
5. **`dqComparedCycle`** (so sánh N chu kỳ trước) hiện đang được dùng để làm gì? Có phát hiện bất thường tự động không?
6. Hai chiều **CONSISTENCY** và **VALIDITY** để rỗng là **có chủ đích** (dành cho sau) hay **bị bỏ quên**?
7. **`mergeBy`, `groupBy`, `orderBy`** trong cấu hình ghi — TaskUtil có đọc và dùng không?
8. Cơ chế hợp nhất `_TMP` → bảng chính hiện do **ai** thực hiện: Pentaho, TaskUtil, hay job riêng?
9. **Quản lý danh mục** hiện dùng cho những nghiệp vụ nào? Danh mục có được dùng để kiểm tra dữ liệu ở đâu chưa?
10. **HDFS Explorer** và **quyền bảng** có được đồng bộ ở đâu không, hay hoàn toàn độc lập?
11. **Zeppelin** truy cập dữ liệu qua đường nào, có chịu phân quyền của SQLWF không?
12. Đồng bộ từ CSDL nguồn (`sync-management`) là **tải lại toàn bộ** hay **chỉ phần thay đổi**?

### Nhóm C — Định hướng cần lãnh đạo quyết
13. Hudi/Iceberg áp cho **bảng tạo mới**, hay **chuyển đổi cả bảng cũ**?
14. Nhóm bảng nào ưu tiên thử nghiệm trước? *(đề xuất: nhóm đối soát — vì time-travel có giá trị nghiệp vụ ngay)*
15. Có chấp nhận **dựng thêm một thành phần hạ tầng mới (catalog)** không? Nếu không, phạm vi Iceberg phải thu hẹp lại rất nhiều.

---

## Nguồn tham khảo (mục 14)

**Data Catalog / Metadata**
- [OpenMetadata Quickstart](https://docs.open-metadata.org/v1.12.x/quick-start) · [OpenMetadata GitHub](https://github.com/open-metadata/OpenMetadata) · [OpenMetadata Lineage](https://docs.open-metadata.org/v1.12.x/how-to-guides/data-lineage/explore)
- [DataHub Quickstart](https://docs.datahub.com/docs/quickstart) · [DataHub Column-Level Lineage](https://datahub.com/blog/column-level-lineage-comes-to-datahub/) · [DataHub SQL Parser](https://datahub.com/blog/extracting-column-level-lineage-from-sql/)
- [So sánh OpenMetadata vs DataHub](https://atlan.com/openmetadata-vs-datahub/) · [Top open source data catalogs 2026](https://atlan.com/open-source-data-catalog-tools/)
- [OpenLineage với Spark](https://openlineage.io/docs/guides/spark/) · [Column-Level Lineage (OpenLineage)](https://openlineage.io/docs/integrations/spark/spark_column_lineage/) · [Marquez column lineage](https://marquezproject.ai/blog/column-lineage-demo/)
- [Secoda pricing](https://www.secoda.co/pricing) · [Select Star](https://www.getapp.com/business-intelligence-analytics-software/a/select-star/)

**Data Quality / Observability**
- [Open-source data quality landscape 2026 (DataKitchen)](https://datakitchen.io/blog/the-2026-open-source-data-quality-and-data-observability-landscape/)
- [Great Expectations vs dbt Tests vs Soda Core](https://pipecode.ai/blogs/data-quality-frameworks-great-expectations-vs-dbt-tests-vs-soda-core) · [GX vs Deequ vs Soda](https://branchboston.com/great-expectations-vs-deequ-vs-soda-data-quality-testing-tools-compared/)
- [Soda pricing & features](https://datastackindex.com/data-observability/tools/soda/) · [Metaplane pricing](https://www.metaplane.dev/pricing) · [Elementary pricing](https://docs.elementary-data.com/resources/pricing)

**Data Security**
- [Apache Ranger Policy Model](https://ranger.apache.org/blogs/policy_model.html) · [Row-level filtering & column masking](https://cwiki.apache.org/confluence/display/RANGER/Row-level+filtering+and+column-masking+using+Apache+Ranger+policies+in+Apache+Hive) · [Ranger masking trên CDP](https://docs.cloudera.com/runtime/7.3.1/security-ranger-authorization/topics/security-ranger-row-level-filtering-and-column-masking-in-hive.html)

**Lakehouse Catalog**
- [The State of Apache Iceberg Catalogs (06/2026)](https://amdatalakehouse.substack.com/p/the-state-of-apache-iceberg-catalogs) · [Lakekeeper Docs](https://docs.lakekeeper.io/) · [Iceberg Catalog Comparison](https://risingwave.com/blog/iceberg-catalog-comparison-guide/) · [Securing Iceberg with FGAC](https://iceberglakehouse.com/posts/iceberg-row-column-access-control/)

---

> **Tài liệu này được xây dựng từ khảo sát trực tiếp source code SQLWF (backend Java + frontend Angular), tháng 07/2026.**
> Mọi mục đánh ⚠️ là suy luận cần xác nhận — xem danh sách câu hỏi ở [P4](#p4-câu-hỏi-cần-xác-nhận).
