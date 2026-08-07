# DMP — Nền tảng Quản trị Dữ liệu

Bộ tài liệu đề xuất xây dựng công cụ **Quản lý dữ liệu tập trung** cho SQLWF, kèm **55 ảnh minh hoạ giao diện** và **plan dựng demo front-end**.

> ⚠️ Repo này **chỉ chứa tài liệu**. Không có mã nguồn nội bộ của SQLWF.

---

## Đọc gì trước

| # | Tài liệu | Nội dung | Độ dài |
|:---:|---|---|---|
| **1** | [**Đề xuất tool Data Management**](docs/DMP-De-xuat-tool-Data-Management.md) | ⭐ **Tài liệu chính.** 8 phần + phụ lục · 6 module · 21 menu · **55 màn hình** có ảnh · lộ trình 4 đợt · 8 rủi ro · ma trận thao tác theo vai trò | ~3.300 dòng |
| **2** | [**Plan dựng demo front-end**](docs/DMP-Plan-Dung-Demo-FE.md) | ⭐ Hướng dẫn dựng demo React chạy được — hệ thống thiết kế, 18 component, bảng 55 route, đặc tả từng màn, chia 5 đợt | ~1.090 dòng |
| 3 | [Kiểm kê màn hình SQLWF](docs/DMP-Kiem-ke-man-hinh-SQLWF.md) | Kết quả **đọc mã nguồn** SQLWF — cơ sở cho cột *"SQLWF hiện có"* trong tài liệu ① | ~430 dòng |
| 4 | [Nghiên cứu thị trường](docs/SQLWF-Nghien-cuu-thi-truong-Demo-cong-cu.md) | Demo 5 công cụ thị trường *(OpenMetadata · DataHub · Soda · Apache Ranger …)*, 22 ảnh, có bảng xác thực nguồn | ~1.310 dòng |

**Thứ tự đọc gợi ý:** ① → ③ *(hiểu vì sao thiết kế như vậy)* → ② *(nếu dựng demo)*

---

## Cấu trúc repo

```
docs/
├── DMP-De-xuat-tool-Data-Management.md     ⭐ tài liệu chính
├── DMP-Plan-Dung-Demo-FE.md                ⭐ plan dựng demo
├── DMP-Kiem-ke-man-hinh-SQLWF.md           kiểm kê mã nguồn
├── SQLWF-Nghien-cuu-thi-truong-*.md        nghiên cứu thị trường
├── SQLWF-*.md · SRS-*.md                   tài liệu giai đoạn trước
├── assets/
│   ├── dmp/        55 ảnh màn hình DMP + 1 sơ đồ tổng quan
│   └── thi-truong/ 22 ảnh công cụ thị trường
└── export/
    └── *.html      bản HTML một tệp của tài liệu nghiên cứu thị trường
tools/
└── mockgen/        bộ script Python sinh ra 55 ảnh giao diện
```

---

## 55 màn hình

| Module | Menu | Màn |
|---|:---:|:---:|
| ① Data Catalog | 4 | 1 – 15 |
| ② Governance | 2 | 16 – 20 |
| ③ Data Quality | 5 | 21 – 30 |
| ④ Ingestion & Orchestration | 3 | 31 – 39 |
| ⑤ Data Security | 5 | 40 – 52 |
| ⑥ Operations | 2 | 53 – 55 |

Ảnh nằm ở `docs/assets/dmp/dmp-NN-*.png`, số thứ tự khớp với mục *"Màn NN — …"* trong tài liệu chính.

---

## Xem tài liệu thế nào cho đúng

Tài liệu dùng thẻ `<details>` để đóng/mở từng mục và bảng Markdown.

| Cách xem | Kết quả |
|---|---|
| ✅ **Trên GitHub** *(bấm vào link ở bảng trên)* | Hiện đủ ảnh, bảng, và các mục đóng/mở được |
| ✅ **VS Code** — mở tệp rồi `Ctrl+Shift+V` | Như trên |
| ⚠️ Trình soạn thảo text thường | Thấy thẻ HTML thô, ảnh không hiện |

---

## Sinh lại ảnh giao diện

Bộ script trong `tools/mockgen/` sinh ra toàn bộ 55 ảnh. Cần **Python 3** và **Google Chrome**.

```bash
cd tools/mockgen
python run.py <thư-mục-ảnh-đích>            # sinh tất cả
python run.py <thư-mục-ảnh-đích> dmp-44     # sinh một màn
```

| Tệp | Vai trò |
|---|---|
| `dmp.py` | Khung giao diện dùng chung — bảng màu, thanh bên 21 menu, hàm `shell()` `fld()` `chip()` |
| `s_dmp1.py` … `s_dmp11.py` | Nội dung từng nhóm màn |
| `run.py` | Sinh HTML rồi chụp bằng Chrome headless. Kích thước từng màn khai trong `SIZE` |

> Sửa màu hoặc bố cục chung thì sửa `dmp.py` rồi chạy lại `run.py` — cả 55 ảnh cập nhật theo.

---

## Hai câu hỏi còn treo

| Mã | Câu hỏi | Cần ai trả lời |
|:---:|---|---|
| **H5** | Bao nhiêu % job đang bật `enableDataLineage`? | Đội vận hành |
| **Q1** | Tên chính thức của tool — đang tạm dùng **DMP** | Lãnh đạo phòng |
