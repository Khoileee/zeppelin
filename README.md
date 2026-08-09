# DMP — Nền tảng Quản trị Dữ liệu

Bộ tài liệu đề xuất xây dựng công cụ **Quản lý dữ liệu tập trung** cho SQLWF, kèm **55 ảnh minh hoạ giao diện** và **plan dựng demo front-end**.

> ⚠️ Repo này **chỉ chứa tài liệu**. Không có mã nguồn nội bộ của SQLWF.

---

## Đọc gì trước

| # | Tài liệu | Nội dung | Độ dài |
|:---:|---|---|---|
| **0** | [**Hướng dẫn sử dụng — Walkthrough**](docs/DMP-Huong-dan-su-dung-Walkthrough.md) | ⭐ **Đọc nếu chưa từng dùng DMP.** Đi từ *"hệ thống này là gì"* tới *"vào đâu khai gì, khai xong nó chạy đi đâu"* — thứ tự khai báo 4 đợt, walkthrough 12 bước theo một bảng thật, bảng **máy tự làm vs người làm tay**, tra nhanh 35 menu, **8 phép thử tự rà soát logic** | ~700 dòng |
| **1** | [**Review đối chiếu yêu cầu BDA**](docs/DMP-Review-Doi-chieu-Yeu-cau-BDA.md) | ⭐ **Đọc trước tiên.** Rà soát 6 tài liệu yêu cầu BDA *(Phương án + GĐ1→GĐ5)* với thiết kế DMP — mức phủ từng nhóm chức năng, 3 gap cấp kiến trúc, 10 gap chi tiết, kiến trúc đề xuất **8 module · 34 menu**, 12 việc phải làm | ~450 dòng |
| **2** | [**Đề xuất tool Data Management**](docs/DMP-De-xuat-tool-Data-Management.md) | ⭐ **Tài liệu chính** *(bản 3.0)*. 8 phần + phụ lục · **8 module · 34 menu** · **55 màn hình** có ảnh · **mục 4B** giải thích 13 menu bổ sung · lộ trình · rủi ro · ma trận thao tác theo vai trò | ~3.400 dòng |
| **3** | [**Plan dựng demo front-end**](docs/DMP-Plan-Dung-Demo-FE.md) | Hướng dẫn dựng demo React — hệ thống thiết kế, 18 component, bảng route, đặc tả từng màn | ~1.090 dòng |
| 4 | [Kiểm kê màn hình SQLWF](docs/DMP-Kiem-ke-man-hinh-SQLWF.md) | Kết quả **đọc mã nguồn** SQLWF — cơ sở cho cột *"SQLWF hiện có"* trong tài liệu ② | ~430 dòng |
| 5 | [Nghiên cứu thị trường](docs/SQLWF-Nghien-cuu-thi-truong-Demo-cong-cu.md) | Demo 5 công cụ thị trường *(OpenMetadata · DataHub · Soda · Apache Ranger …)*, 22 ảnh, có bảng xác thực nguồn | ~1.310 dòng |

**Thứ tự đọc gợi ý:** ⓪ *(hiểu cách dùng)* → ① *(biết thiếu gì)* → ② *(tool sẽ có gì)* → ④ *(vì sao thiết kế như vậy)* → ③ *(nếu dựng demo)*

---

## Demo chạy được

Kiến trúc sau review đã được dựng thành **demo front-end chạy được**: React + Vite + TypeScript,
**8 module · 34 menu · 96 màn hình**, bấm được, mở popup được, có wizard nhiều bước và các ràng buộc nghiệp vụ thật.

```bash
npm install && npm run dev      # trong repo dmp
```

Kịch bản trình bày 12 phút và bảng số liệu chủ chốt nằm trong `README.md` của repo demo.

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
