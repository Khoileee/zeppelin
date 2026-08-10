# Plan dựng demo Front-end — DMP

### Tài liệu hướng dẫn cho phiên làm việc mới (máy khác)


> 🔴 **TÀI LIỆU NÀY CHƯA CẬP NHẬT THEO KIẾN TRÚC CHỐT.**
> Con số menu và màn hình bên dưới **không còn hiệu lực**. Kiến trúc chốt là **8 module · 27 menu** —
> xem [**DMP-Kien-truc-CHOT.md**](DMP-Kien-truc-CHOT.md). Phần **nghiệp vụ** trong tài liệu này **vẫn đúng**,
> chỉ số hiệu menu là sai.

| | |
|---|---|
| **Mục đích** | Dựng **demo FE chạy được** của DMP — bấm được, điều hướng được, mở popup, chuyển tab, sát giao diện thật |
| **Không cần** | Back-end · API · database · đăng nhập thật |
| **Đầu ra** | Một ứng dụng web chạy bằng `npm run dev`, mở trình duyệt là dùng được |
| **Người đọc** | Một phiên Claude Code mới trên máy khác — **đọc tài liệu này là đủ để bắt tay làm** |
| **Ngày** | 07/08/2026 |

---

## 0. ĐỌC GÌ TRƯỚC KHI BẮT ĐẦU

<details open>
<summary><b>Ba đầu vào bắt buộc — đọc theo đúng thứ tự này</b></summary>

| # | Tệp | Đọc để làm gì | Bắt buộc |
|:---:|---|---|:---:|
| **1** | **`DMP-De-xuat-tool-Data-Management.md`** *(cùng thư mục)* | ⭐ **Nguồn sự thật về NGHIỆP VỤ.** Mọi trường thông tin, mọi luồng, mọi ràng buộc đều đã mô tả ở đây. Plan này **không chép lại**, chỉ trỏ tới | ✔ |
| **2** | **`assets/dmp/dmp-01…55-*.png`** *(55 ảnh)* | ⭐ **Nguồn sự thật về GIAO DIỆN.** Mỗi màn có một ảnh. Bố cục, màu, khoảng cách, thứ tự cột — nhìn ảnh mà dựng | ✔ |
| 3 | `DMP-Kiem-ke-man-hinh-SQLWF.md` | Bối cảnh: SQLWF hiện có gì. Chỉ đọc khi cần hiểu vì sao một màn được thiết kế như vậy | — |

**Cách dùng hai nguồn trên khi dựng một màn:**

```
① Mở ảnh assets/dmp/dmp-NN-*.png          → biết bố cục, cột, màu, thứ tự
② Mở mục "Màn NN — ..." trong tài liệu ①  → biết ý nghĩa từng trường, ràng buộc, luồng
③ Đọc mục tương ứng trong plan này        → biết dùng component nào, bấm ra cái gì
```

> ⚠️ **Nếu ảnh và tài liệu lệch nhau thì tin ẢNH** về bố cục, tin **TÀI LIỆU** về nghiệp vụ.

</details>

<details open>
<summary><b>Bốn quyết định đã chốt — không cần hỏi lại</b></summary>

| Quyết định | Đã chốt |
|---|---|
| **Công nghệ** | React + Vite + TypeScript + Tailwind CSS. Máy dựng **có npm và internet bình thường** |
| **Dữ liệu** | ⭐ **Chỉ điều hướng — dữ liệu CỐ ĐỊNH, không lưu.** Form gõ được, wizard chuyển bước được, bấm Lưu thì hiện thông báo thành công rồi quay lại; **danh sách không đổi** |
| **Phạm vi** | Đủ **21 menu / 55 màn**, chia **5 đợt** |
| **Tên tool** | **DMP** — đặt trong một tệp cấu hình duy nhất để đổi được sau |

</details>

---

## 1. MỤC TIÊU VÀ PHI MỤC TIÊU

<details open>
<summary><b>Demo này để làm gì và KHÔNG làm gì</b></summary>

**Mục tiêu**

| # | Mục tiêu | Đo bằng |
|:---:|---|---|
| 1 | Người xem **tự bấm khám phá** được toàn bộ 21 menu mà không cần ai hướng dẫn | Mở bất kỳ menu nào cũng ra màn có nội dung, không có màn trống |
| 2 | Thấy được **quan hệ giữa các module** | Bấm tên bảng ở màn Job → nhảy sang chi tiết bảng. Bấm mã sự cố → nhảy sang chi tiết sự cố |
| 3 | Thấy được **hình dáng thật của form khai báo** | Mở form tạo bảng / gán luật / thêm chính sách che → thấy đủ trường, đủ ô gợi ý, đủ cảnh báo |
| 4 | Thuyết phục được lãnh đạo về **ba tính năng mới** | Che dữ liệu · Lọc theo dòng · Cổng chất lượng — có màn bấm vào xem được |

**Phi mục tiêu — làm là lãng phí**

| Không làm | Vì sao |
|---|---|
| ❌ Back-end, API, database | Đã chốt: demo FE thuần |
| ❌ Đăng nhập, phân quyền thật | Người dùng hiện tại là **cố định**, hiện ở góc trên |
| ❌ Lưu dữ liệu | Đã chốt. Bấm Lưu → thông báo → quay lại, danh sách không đổi |
| ❌ Biểu đồ động, thư viện chart nặng | Mọi biểu đồ trong ảnh đều là **thanh ngang bằng div** hoặc **SVG tĩnh** — không cần Recharts/D3 |
| ❌ Responsive điện thoại | Demo chiếu máy chiếu / màn hình lớn. Chỉ cần **tối thiểu 1440px** |
| ❌ Dải watermark đen ở đáy ảnh | Đó là chú thích **chỉ dùng cho tài liệu**, **KHÔNG dựng vào demo** |
| ❌ Đa ngôn ngữ | Chỉ tiếng Việt |

</details>

---

## 2. KHỞI TẠO DỰ ÁN

<details open>
<summary><b>Lệnh khởi tạo và danh sách thư viện</b></summary>

```bash
npm create vite@latest dmp-demo -- --template react-ts
cd dmp-demo
npm install
npm install react-router-dom
npm install -D tailwindcss @tailwindcss/vite
npm run dev
```

**Danh sách thư viện — chỉ đúng ba thứ, không thêm**

| Thư viện | Dùng để | Vì sao không dùng cái khác |
|---|---|---|
| `react` + `react-dom` | Khung | |
| `react-router-dom` | Điều hướng 55 route | Cần URL thật để chia sẻ link từng màn khi trình bày |
| `tailwindcss` | Kiểu dáng | Ảnh mẫu dùng toàn inline style — Tailwind ánh xạ gần như 1-1 |

> 🔴 **Không cài thêm thư viện UI** (MUI, Ant Design, shadcn…). Giao diện trong ảnh là **thiết kế riêng**; dùng thư viện có sẵn sẽ ra một bộ mặt khác hẳn và mất công đè kiểu.
>
> 🔴 **Không cài thư viện biểu đồ.** Mọi biểu đồ đều dựng bằng `div` và `svg` thuần — xem mục 7.

**`vite.config.ts`**

```ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: { port: 5173, open: true },
})
```

**`src/index.css`**

```css
@import "tailwindcss";

@theme {
  --color-navy:      #16233F;
  --color-navy-2:    #1E2E4F;
  --color-navy-3:    #2B3A5C;
  --color-ac:        #2563EB;
  --color-ac-2:      #0EA5A5;
  --color-page:      #F7F9FC;
  --color-line:      #E3E8EF;
  --color-line-2:    #EEF1F6;
  --color-input:     #D0D7E2;
  --color-ink:       #101828;
  --color-ink-2:     #344054;
  --color-ink-3:     #475467;
  --color-muted:     #667085;
  --color-muted-2:   #8B95A7;
  --color-muted-3:   #98A2B3;
  --color-ok:        #12B76A;
  --color-ok-ink:    #067647;
  --color-warn:      #F79009;
  --color-warn-ink:  #B54708;
  --color-bad:       #F04438;
  --color-bad-ink:   #B42318;
  --color-panel:     #0F1729;
}

body {
  font-family: "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  background: var(--color-page);
  color: var(--color-ink);
  min-width: 1440px;
}
.mono { font-family: Consolas, "Courier New", monospace; }
```

> 💡 Dùng **font hệ thống**, không tải font ngoài — ảnh mẫu render bằng Segoe UI, dùng font khác sẽ lệch bố cục.

</details>

---

## 3. HỆ THỐNG THIẾT KẾ — LẤY ĐÚNG TỪ ẢNH MẪU

<details open>
<summary><b>Bảng màu — dùng đúng mã, không tự chọn</b></summary>

| Nhóm | Vai trò | Mã màu |
|---|---|---|
| **Thanh bên** | Nền | `#16233F` |
| | Nền mục đang chọn | `#2563EB` |
| | Nền mục con đang chọn | `#2B3A5C` + viền trái `#0EA5A5` 3px |
| | Chữ mục thường | `#C3CEE2` |
| | Chữ nhóm menu | `#6D81A8` — 10px, đậm, giãn chữ 0.7px, VIẾT HOA |
| | Đường kẻ dưới logo | `#2B3A5C` |
| **Nền** | Ngoài cùng | `#EEF1F6` |
| | Vùng nội dung | `#F7F9FC` |
| | Thẻ, đầu trang | `#FFFFFF` |
| **Viền** | Thẻ, đầu trang | `#E3E8EF` |
| | Dòng bảng | `#EEF1F6` |
| | Ô nhập | `#D0D7E2` |
| **Chữ** | Tiêu đề | `#101828` |
| | Nội dung | `#344054` |
| | Mờ | `#667085` · `#8B95A7` |
| **Nhấn** | Chính | `#2563EB` |
| | Phụ | `#0EA5A5` |

**Sáu kiểu nhãn tròn (chip)** — nền / chữ

| Kiểu | Nền | Chữ | Dùng cho |
|---|---|---|---|
| `b` xanh dương | `#EFF4FF` | `#2563EB` | Thông tin trung tính, phiên bản |
| `g` xanh lá | `#ECFDF3` | `#067647` | Đạt · Thành công · Đang chạy |
| `r` đỏ | `#FEF3F2` | `#B42318` | Hỏng · Từ chối · Chặn · Nhạy cảm |
| `o` cam | `#FFFAEB` | `#B54708` | Cảnh báo · Chờ duyệt · Sắp hết hạn |
| `n` xám | `#F2F4F7` | `#475467` | Không xác định · Đã ngừng |
| `t` ngọc | `#E6FAF8` | `#0E7C7B` | Phân loại, loại hình |

**Bốn kiểu hộp ghi chú** — nền / viền / biểu tượng mở đầu

| Kiểu | Nền | Viền | Mở đầu bằng | Dùng cho |
|---|---|---|---|---|
| Tốt | `#ECFDF3` | `#A6F4C5` | ✅ | SQLWF đã có — giữ nguyên |
| Xấu | `#FEF3F2` | `#FECDCA` | 🔴 | Vấn đề nghiêm trọng, tính năng chưa có |
| Cảnh báo | `#FFFAEB` | `#FEDF89` | ⚠️ | Cần cẩn thận |
| Liên kết | `#EFF4FF` | `#C7D7FE` | 🔗 hoặc 💡 | Khai ở đây dùng ở đâu |

**Bảng mã tối** *(dùng cho khối SQL và thẻ điểm chất lượng)*

| Vai trò | Mã |
|---|---|
| Nền | `#0F1729` |
| Chữ | `#E5E9F0` |
| Chú thích | `#8B95A7` |
| Từ khoá SQL | `#7C3AED` *(nền sáng)* · `#93B4FF` *(nền tối)* |
| Giá trị nhấn | `#FFD479` |
| Thêm vào | `#75E0A7` · nền `#123522` |
| Bỏ đi | `#FDA29B` · nền `#3D1D1D` |

</details>

<details open>
<summary><b>Kích thước, bo góc, cỡ chữ</b></summary>

| Thành phần | Giá trị |
|---|---|
| Thanh bên | rộng `236px`, không co |
| Đầu trang | đệm `13px 24px`, viền dưới 1px |
| Vùng nội dung | đệm `18px 24px` |
| Bo góc thẻ | `9px` · ô nhập `7px` · nút `7px` · chip `11px` · nút biểu tượng `5px` |
| Khoảng cách giữa thẻ | `12–16px` |
| Chiều rộng tối thiểu trang | `1440px` |

| Chữ | Cỡ / đậm |
|---|---|
| Tiêu đề trang `h1` | `19px / 700` |
| Mô tả dưới tiêu đề | `12.5px`, màu `#667085` |
| Đường dẫn (breadcrumb) | `11.5px`, màu `#8B95A7` |
| Nhãn tab | `13px`; tab đang chọn `700` + gạch chân 2px `#2563EB` |
| Tiêu đề khối trong thẻ | `12.5px / 700`, màu `#2563EB`, gạch chân 2px, `display:inline-block` |
| Nội dung bảng | `12.5px` |
| Đầu cột bảng | `11px / 700`, VIẾT HOA, giãn chữ `0.3px`, màu `#5B6779`, nền `#F8FAFC` |
| Nhãn chip | `10.5px / 600` |
| Nút | `12.5px / 600` |
| Thẻ số liệu — nhãn | `10.5px / 600`, VIẾT HOA, màu `#8B95A7` |
| Thẻ số liệu — số | `23px / 800` |
| Thẻ số liệu — chú thích | `11px`, màu `#8B95A7` |
| Nhãn trường form | `12px / 600`, màu `#344054` |
| Gợi ý dưới trường | `11px`, màu `#8B95A7` |

</details>

---

## 4. KHUNG GIAO DIỆN

<details open>
<summary><b>Bố cục chung mọi màn</b></summary>

```
┌──────────────────────────────────────────────────────────────┐
│ ┌──────────┐ ┌──────────────────────────────────────────────┐│
│ │          │ │ ĐẦU TRANG (nền trắng, viền dưới)             ││
│ │ THANH    │ │  đường dẫn ›  ›                              ││
│ │ BÊN      │ │  H1 tiêu đề                    [nút] [nút]   ││
│ │ 236px    │ │  mô tả một dòng                              ││
│ │          │ │  Tab1  Tab2  Tab3                            ││
│ │ nền navy │ ├──────────────────────────────────────────────┤│
│ │          │ │ NỘI DUNG (nền #F7F9FC, đệm 18px 24px)        ││
│ │          │ │  [thẻ số liệu] [thẻ] [thẻ] [thẻ]             ││
│ │          │ │  [thanh lọc + ô tìm kiếm]                    ││
│ │          │ │  [bảng trong thẻ trắng]                      ││
│ │          │ │  [hộp ghi chú trái]      [hộp ghi chú phải]  ││
│ └──────────┘ └──────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────┘
```

> 🔴 **Không dựng dải watermark đen ở đáy ảnh.** Đó là chú thích của tài liệu.

**Đầu trang có thêm — không có trong ảnh, thêm cho demo**

Góc phải trên cùng của thanh bên hoặc đầu trang: chip người dùng hiện tại

```
👤 Nguyễn Thị Phương · BDA — Ban Kinh doanh   ▾
```

Bấm vào mở danh sách 5 người, **chỉ đổi tên hiển thị**, không đổi dữ liệu. Dùng khi trình bày để nói *"nếu tôi là DE thì màn này sẽ…"*.

</details>

<details open>
<summary><b>Thanh bên — 21 mục, chép đúng nhãn và biểu tượng</b></summary>

| Nhóm | Biểu tượng | Nhãn | Mã | Route |
|---|:---:|---|---|---|
| **① DATA CATALOG** | | | | |
| | 🗂️ | Bảng dữ liệu | `m11` | `/catalog/tables` |
| | 📦 | Nhóm bảng | `m12` | `/catalog/groups` |
| | 🧩 | Miền dữ liệu | `m13` | `/catalog/domains` |
| | 📚 | Danh mục tham chiếu | `m14` | `/catalog/refdata` |
| **② GOVERNANCE** | | | | |
| | 📖 | Từ điển nghiệp vụ | `m21` | `/governance/glossary` |
| | 🏷️ | Phân loại & Nhãn | `m22` | `/governance/classification` |
| **③ DATA QUALITY** | | | | |
| | 📐 | Thư viện luật | `m31` | `/quality/rules` |
| | 🎯 | Luật & Kết quả | `m32` | `/quality/board` |
| | 🔬 | Phân tích dữ liệu | `m33` | `/quality/profiling` |
| | 🚨 | Sự cố chất lượng | `m34` | `/quality/incidents` |
| | 🔔 | Cảnh báo | `m35` | `/quality/alerts` |
| **④ INGESTION & ORCHESTRATION** | | | | |
| | ⚙️ | Luồng xử lý (Job) | `m41` | `/orchestration/jobs` |
| | 📥 | Cửa nạp dữ liệu | `m42` | `/ingestion/templates` |
| | 🖥️ | Theo dõi & Pipeline | `m43` | `/orchestration/monitor` |
| **⑤ DATA SECURITY** | | | | |
| | 👥 | Người dùng & Nhóm | `m51` | `/security/users` |
| | 🔐 | Chính sách truy cập | `m52` | `/security/policies/data` |
| | ✋ | Yêu cầu cấp quyền | `m53` | `/security/requests` |
| | 📜 | Nhật ký kiểm toán | `m54` | `/security/audit` |
| | 📋 | Báo cáo quyền | `m55` | `/security/report` |
| **⑥ OPERATIONS** | | | | |
| | ❤️ | Sức khoẻ dữ liệu | `m61` | `/operations/health` |
| | ⚙️ | Cấu hình hệ thống | `m62` | `/operations/settings` |

**Khối logo trên cùng thanh bên**

```
┌──┐
│D │  DMP
└──┘  Nền tảng Quản trị Dữ liệu
```
Ô vuông `30×30`, bo `8px`, nền `#2563EB`, chữ `D` trắng đậm `14px`.
Chữ `DMP` `15px/800` trắng · dòng dưới `10px` màu `#8FA3C8`.

> ⭐ **Quy tắc tô sáng:** một mục sáng khi route hiện tại **bắt đầu bằng** route của mục đó. Ví dụ `/catalog/tables/bi.doi_soat/columns` vẫn tô sáng mục *Bảng dữ liệu*.

</details>

---

## 5. BẢNG ROUTE ĐẦY ĐỦ — 55 MÀN

<details open>
<summary><b>Ánh xạ Màn ↔ Route ↔ Ảnh ↔ Tệp mã nguồn</b></summary>

| Màn | Route | Ảnh `assets/dmp/` | Tệp `src/pages/` |
|:---:|---|---|---|
| 1 | `/catalog/tables` | `dmp-01-table-list.png` | `catalog/TableList.tsx` |
| 2 | `/catalog/tables/create` | `dmp-02-table-create.png` | `catalog/TableCreate.tsx` |
| 3 | `/catalog/tables/:id` | `dmp-03-table-overview.png` | `catalog/table/TabOverview.tsx` |
| 4 | `/catalog/tables/:id/columns` | `dmp-04-table-columns.png` | `catalog/table/TabColumns.tsx` |
| 5 | `/catalog/tables/:id/quality` | `dmp-05-table-quality.png` | `catalog/table/TabQuality.tsx` |
| 6 | `/catalog/tables/:id/lineage` | `dmp-06-table-lineage.png` | `catalog/table/TabLineage.tsx` |
| 7 | `/catalog/tables/:id/permissions` | `dmp-07-table-perm.png` | `catalog/table/TabPerm.tsx` |
| 8 | `/catalog/tables/:id/history` | `dmp-08-table-history.png` | `catalog/table/TabHistory.tsx` |
| 9 | `/catalog/groups` | `dmp-09-group-list.png` | `catalog/GroupList.tsx` |
| 10 | `/catalog/groups/create` | `dmp-10-group-create.png` | `catalog/GroupCreate.tsx` |
| 11 | `/catalog/domains` | `dmp-11-domain-list.png` | `catalog/DomainList.tsx` |
| 12 | `/catalog/domains/create` | `dmp-12-domain-create.png` | `catalog/DomainCreate.tsx` |
| 13 | `/catalog/refdata` | `dmp-13-refdata-list.png` | `catalog/RefdataList.tsx` |
| 14 | `/catalog/refdata/create` | `dmp-14-refdata-create.png` | `catalog/RefdataCreate.tsx` |
| 15 | `/catalog/refdata/:id` | `dmp-15-refdata-detail.png` | `catalog/RefdataDetail.tsx` |
| 16 | `/governance/glossary` | `dmp-16-glossary-list.png` | `governance/GlossaryList.tsx` |
| 17 | `/governance/glossary/:id` | `dmp-17-glossary-detail.png` | `governance/GlossaryDetail.tsx` |
| 18 | `/governance/glossary/create` | `dmp-18-glossary-create.png` | `governance/GlossaryCreate.tsx` |
| 19 | `/governance/classification` | `dmp-19-classification-tree.png` | `governance/ClassificationTree.tsx` |
| 20 | `/governance/classification/create` | `dmp-20-classification-create.png` | `governance/ClassificationCreate.tsx` |
| 21 | `/quality/rules` | `dmp-21-rule-library.png` | `quality/RuleLibrary.tsx` |
| 22 | `/quality/rules/create` | `dmp-22-rule-create.png` | `quality/RuleCreate.tsx` |
| 23 | `/quality/board` | `dmp-23-quality-board.png` | `quality/QualityBoard.tsx` |
| 24 | `/quality/assign` | `dmp-24-rule-assign.png` | `quality/RuleAssign.tsx` |
| 25 | `/quality/profiling` | `dmp-25-profiling.png` | `quality/Profiling.tsx` |
| 26 | `/quality/incidents` | `dmp-26-incident-list.png` | `quality/IncidentList.tsx` |
| 27 | `/quality/incidents/:id` | `dmp-27-incident-detail.png` | `quality/IncidentDetail.tsx` |
| 28 | `/quality/alerts` | `dmp-28-alert-list.png` | `quality/AlertList.tsx` |
| 29 | `/quality/alerts/create` | `dmp-29-alert-create.png` | `quality/AlertCreate.tsx` |
| 30 | `/quality/alerts/channels` | `dmp-30-alert-channels.png` | `quality/AlertChannels.tsx` |
| 31 | `/orchestration/jobs` | `dmp-31-job-list.png` | `orchestration/JobList.tsx` |
| 32 | `/orchestration/jobs/create` | `dmp-32-job-create.png` | `orchestration/JobCreate.tsx` |
| 33 | `/orchestration/jobs/:id` | `dmp-33-job-steps.png` | `orchestration/job/TabSteps.tsx` |
| 34 | `/orchestration/jobs/:id/runs` | `dmp-34-job-runs.png` | `orchestration/job/TabRuns.tsx` |
| 35 | `/orchestration/jobs/:id/versions` | `dmp-35-job-versions.png` | `orchestration/job/TabVersions.tsx` |
| 36 | `/ingestion/templates` | `dmp-36-ingest-list.png` | `ingestion/TemplateList.tsx` |
| 37 | `/ingestion/templates/create` | `dmp-37-ingest-create.png` | `ingestion/TemplateCreate.tsx` |
| 38 | `/ingestion/quarantine` | `dmp-38-ingest-quarantine.png` | `ingestion/Quarantine.tsx` |
| 39 | `/orchestration/monitor` | `dmp-39-pipeline-monitor.png` | `orchestration/PipelineMonitor.tsx` |
| 40 | `/security/users` | `dmp-40-user-list.png` | `security/UserList.tsx` |
| 41 | `/security/users/groups` | `dmp-41-group-acl.png` | `security/GroupAcl.tsx` |
| 42 | `/security/policies/data` | `dmp-42-policy-data.png` | `security/policy/TabData.tsx` |
| 43 | `/security/policies/mask` | `dmp-43-policy-mask.png` | `security/policy/TabMask.tsx` |
| 44 | `/security/policies/mask/create` | `dmp-44-mask-create.png` | `security/MaskCreate.tsx` |
| 45 | `/security/policies/rowfilter` | `dmp-45-policy-rowfilter.png` | `security/policy/TabRowFilter.tsx` |
| 46 | `/security/policies/rowfilter/create` | `dmp-46-rowfilter-create.png` | `security/RowFilterCreate.tsx` |
| 47 | `/security/policies/by-tag` | `dmp-47-policy-bytag.png` | `security/policy/TabByTag.tsx` |
| 48 | `/security/requests` | `dmp-48-request-list.png` | `security/RequestList.tsx` |
| 49 | `/security/requests/create` | `dmp-49-request-create.png` | `security/RequestCreate.tsx` |
| 50 | `/security/requests/:id` | `dmp-50-request-approve.png` | `security/RequestApprove.tsx` |
| 51 | `/security/audit` | `dmp-51-audit-log.png` | `security/AuditLog.tsx` |
| 52 | `/security/report` | `dmp-52-perm-report.png` | `security/PermReport.tsx` |
| 53 | `/operations/health` | `dmp-53-health-board.png` | `operations/HealthBoard.tsx` |
| 54 | `/operations/health/by-domain` | `dmp-54-health-domain.png` | `operations/HealthDomain.tsx` |
| 55 | `/operations/settings` | `dmp-55-system-config.png` | `operations/SystemConfig.tsx` |

**Route mặc định:** `/` chuyển hướng sang `/operations/health` *(màn 53 — bảng điều khiển, mở ra là thấy toàn cảnh ngay)*.

**Định danh mẫu dùng trong route:**
`:id` bảng = `bi.doi_soat_giao_dich_A` · job = `JOB-0412` · sự cố = `SC-0231` · yêu cầu = `YC-0231` · danh mục = `DM-004`.

</details>

---

## 6. CẤU TRÚC THƯ MỤC

<details open>
<summary><b>Sơ đồ thư mục và nguyên tắc đặt tệp</b></summary>

```
src/
├── main.tsx                 khởi động + router
├── index.css                Tailwind + biến màu
├── config.ts                ⭐ TÊN TOOL, khẩu hiệu, người dùng hiện tại
│
├── layout/
│   ├── AppShell.tsx         khung: thanh bên + đầu trang + nội dung
│   ├── Sidebar.tsx          21 mục, tô sáng theo route
│   ├── PageHeader.tsx       đường dẫn + H1 + mô tả + nút + tab
│   └── menu.ts              ⭐ mảng 21 mục (nhóm, biểu tượng, nhãn, route)
│
├── ui/                      thư viện dùng chung — xem mục 7
│   ├── Card.tsx      KpiRow.tsx    DataTable.tsx   Chip.tsx
│   ├── Button.tsx    IconButton.tsx Field.tsx      Note.tsx
│   ├── SectionTitle.tsx  Tabs.tsx  FilterBar.tsx   Steps.tsx
│   ├── Modal.tsx     Drawer.tsx    Toast.tsx       Dropdown.tsx
│   ├── ProgressBar.tsx  Timeline.tsx  CodeBlock.tsx  TreeView.tsx
│   ├── FlowDiagram.tsx   StatusBar.tsx  EmptyState.tsx
│   └── index.ts             xuất tất cả
│
├── data/                    ⭐ toàn bộ dữ liệu mẫu — tệp .ts, gõ kiểu đầy đủ
│   ├── types.ts             định nghĩa kiểu
│   ├── tables.ts    columns.ts    domains.ts    groups.ts   refdata.ts
│   ├── glossary.ts  tags.ts
│   ├── rules.ts     ruleInstances.ts  incidents.ts  alerts.ts  profiling.ts
│   ├── jobs.ts      jobRuns.ts    ingestTemplates.ts  quarantine.ts
│   ├── users.ts     groupsAcl.ts  policies.ts   requests.ts  auditLog.ts
│   └── health.ts    settings.ts
│
└── pages/                   55 màn — theo bảng route mục 5
    ├── catalog/  governance/  quality/  orchestration/  ingestion/
    ├── security/  operations/
```

**Ba nguyên tắc**

| # | Nguyên tắc |
|:---:|---|
| **1** | ⭐ **Mọi dữ liệu nằm trong `src/data/`.** Không viết dữ liệu cứng trong tệp màn. Lý do: khi cần sửa một con số cho khớp tài liệu thì sửa một chỗ |
| **2** | ⭐ **Mọi màn chỉ được dùng component trong `src/ui/`.** Không viết `<div className="bg-white rounded-lg border …">` lặp lại ở 55 chỗ |
| **3** | **Tên tool và người dùng hiện tại nằm trong `src/config.ts`** — đổi một chỗ là đổi toàn bộ |

**`src/config.ts`**

```ts
export const APP = {
  name: 'DMP',
  tagline: 'Nền tảng Quản trị Dữ liệu',
  domain: 'dmp.vds.vn',
}

export const CURRENT_USER = {
  id: 'nguyen.thi.phuong',
  name: 'Nguyễn Thị Phương',
  role: 'BDA — Ban Kinh doanh',
}

// danh sách để đổi vai khi trình bày (chỉ đổi tên hiển thị)
export const DEMO_USERS = [
  { id: 'nguyen.thi.phuong', name: 'Nguyễn Thị Phương', role: 'BDA — Ban Kinh doanh' },
  { id: 'tran.van.hung',     name: 'Trần Văn Hùng',     role: 'DE — Đội Dữ liệu' },
  { id: 'pham.thu.ha',       name: 'Phạm Thu Hà',       role: 'BDA — Ban Tài chính' },
  { id: 'le.minh.tuan',      name: 'Lê Minh Tuấn',      role: 'Chuyên viên — Ban Sản phẩm' },
  { id: 'admin.he.thong',    name: 'Quản trị hệ thống', role: 'QTHT' },
]
```

</details>

---

## 7. THƯ VIỆN COMPONENT DÙNG CHUNG

<details open>
<summary><b>Mười tám component — dựng TRƯỚC khi dựng màn nào</b></summary>

> ⭐ **Đây là phần quan trọng nhất của cả plan.** Dựng đủ 18 component này thì 55 màn còn lại chỉ là lắp ghép. Bỏ qua bước này thì sẽ viết lại cùng một đoạn HTML 55 lần và giao diện sẽ lệch nhau.

### Nhóm bố cục

| Component | Props | Hành vi |
|---|---|---|
| **`Card`** | `title?` `actions?` `tone?: 'default'\|'warn'\|'bad'\|'dark'` `children` | Thẻ trắng bo `9px` viền `#E3E8EF` đệm `16px 19px`. `tone` đổi nền/viền theo bảng màu hộp ghi chú |
| **`SectionTitle`** | `children` | Chữ `12.5px/700` màu `#2563EB`, gạch chân 2px, `inline-block`, `margin: 4px 0 13px` |
| **`Tabs`** | `items: {label, to}[]` `active` | Hàng tab, khoảng cách `24px`. Tab đang chọn: xanh + đậm + gạch chân 2px. **Dùng `<Link>`, mỗi tab là một route thật** |
| **`FilterBar`** | `placeholder` `filters: string[]` | Ô tìm kiếm chiếm hết chiều rộng còn lại + các nút lọc kiểu `btn w` có mũi tên ▾. **Không cần lọc thật** — bấm mở dropdown trang trí |

### Nhóm hiển thị dữ liệu

| Component | Props | Hành vi |
|---|---|---|
| **`KpiRow`** | `items: {label, value, sub, color?}[]` | Hàng thẻ số liệu, `flex`, khoảng cách `12px`, mỗi thẻ `flex:1`. Xem cỡ chữ ở mục 3 |
| **`DataTable`** | `columns: {key,label,align?,width?,nowrap?}[]` `rows: any[]` `onRowClick?` `renderCell?` | Bảng chuẩn. Đầu cột VIẾT HOA nền `#F8FAFC`. Dòng có `hover:bg-[#F9FBFF]`. Nếu có `onRowClick` thì thêm `cursor-pointer` |
| **`Chip`** | `tone: 'b'\|'g'\|'r'\|'o'\|'n'\|'t'` `children` | Nhãn tròn. **Luôn bọc trong `<span class="whitespace-nowrap">`** — nhãn xuống dòng làm hỏng bảng |
| **`ProgressBar`** | `pct` `target?` `color` `label` `note` | Thanh ngang nền `#F2F4F7` cao `15px` bo `4px`. Nếu có `target` thì vẽ vạch đen 2px cao `21px` tại `left: target%` |
| **`Timeline`** | `items: {time, who, text, tone?}[]` | Dọc, chấm tròn bên trái + đường nối. Dùng ở màn 27 và 35 |
| **`CodeBlock`** | `lang?` `dark?: boolean` `children` | Khối mã. `dark` → nền `#0F1729` chữ `#E5E9F0`. Tô màu **bằng tay qua `<span>`**, không cần thư viện tô sáng cú pháp |
| **`TreeView`** | `nodes: {label, count?, children?}[]` `activeId` | Cây phân cấp. Nút đang chọn: nền `#EFF4FF`, chữ xanh đậm. Dùng ở màn 19 và 47 |
| **`StatusBar`** | `steps: {label, count?, tone}[]` | Dải trạng thái ngang có mũi tên `→` giữa các bước. Dùng ở màn 26 (6 trạng thái sự cố) và 48 (5 trạng thái yêu cầu) |

### Nhóm nhập liệu

| Component | Props | Hành vi |
|---|---|---|
| **`Field`** | `label` `required?` `hint?` `readOnly?` `mono?` `children` | Bọc một ô nhập. Có dấu `*` đỏ nếu bắt buộc, gợi ý `11px` màu mờ bên dưới. `readOnly` → nền `#F5F7FA` chữ mờ |
| **`Steps`** | `items: {label, state:'done'\|'now'\|'next'}[]` | Dải bước của wizard. `done` = tròn xanh lá có ✓ · `now` = tròn xanh dương có số · `next` = tròn xám. Có đường nối `20px` giữa các bước |
| **`Button`** | `variant: 'primary'\|'ghost'` `size?: 'sm'` `icon?` `onClick` | `primary` nền `#2563EB` chữ trắng · `ghost` nền trắng viền `#D0D7E2` chữ `#475467` |
| **`IconButton`** | `icon` `title` `onClick` | Ô vuông `24×23` bo `5px` viền `#D0D7E2`. Dùng cho 👁 ✎ ✕ ▶ ⇄ ↩ trong bảng |

### Nhóm tương tác

| Component | Props | Hành vi |
|---|---|---|
| **`Modal`** | `open` `title` `size?: 'sm'\|'md'\|'lg'` `footer?` `onClose` | Lớp phủ đen `rgba(16,24,40,.45)`. Hộp trắng giữa màn, bo `12px`, bóng đổ. Đóng bằng nút ✕, phím `Esc`, hoặc bấm nền |
| **`Drawer`** | `open` `title` `width?` `onClose` | Trượt từ phải, rộng mặc định `520px`. Dùng cho *xem nhanh chi tiết* mà không rời màn danh sách |
| **`Toast`** | gọi qua `toast.success(msg)` / `toast.info(msg)` | Hiện góc phải trên, tự tắt sau `3s`. ⭐ **Đây là cách demo phản hồi mọi thao tác lưu** |
| **`Dropdown`** | `label` `items: {label, onClick}[]` | Menu thả xuống. Dùng cho nút lọc và bộ chọn người dùng |

### Component đặc biệt

**`FlowDiagram`** — dùng ở màn 6 *(nguồn gốc)*, 33 *(sơ đồ bước job)*, 39 *(pipeline)*

```ts
type Node = {
  id: string; x: number; y: number; w: number; h: number
  title: string; sub: string
  tone: 'neutral' | 'ok' | 'warn' | 'bad' | 'active'
  badge?: { text: string; tone: string }
}
type Edge = { points: [number, number][]; tone?: 'neutral' | 'bad' | 'warn'; dashed?: boolean }
```

**Cách dựng:** một `<div style="position:relative">` chứa
① một `<svg>` phủ toàn bộ vẽ các `<polyline>` cạnh, có `<marker>` mũi tên
② các `<div style="position:absolute; left:x; top:y">` là nút

> 🔴 **Không dùng thư viện vẽ đồ thị.** Toạ độ đã cố định sẵn trong dữ liệu mẫu — chép từ ảnh ra. Nút bấm được → điều hướng sang màn tương ứng.

</details>

---

## 8. QUY ƯỚC TƯƠNG TÁC — ÁP CHO CẢ 55 MÀN

<details open>
<summary><b>Bấm vào gì thì xảy ra gì</b></summary>

| Thao tác | Kết quả | Ghi chú |
|---|---|---|
| Bấm **mã / tên** trong bảng *(mã bảng, mã job, mã sự cố, mã yêu cầu…)* | Điều hướng sang màn chi tiết tương ứng | ⭐ **Quan trọng nhất** — đây là thứ làm demo có cảm giác thật |
| Bấm 👁 | Mở **`Drawer`** xem nhanh, không rời màn | |
| Bấm ✎ | Điều hướng sang màn sửa *(dùng lại màn tạo, tiêu đề đổi thành "Sửa …")* | |
| Bấm ✕ | Mở **`Modal`** xác nhận xoá → bấm Đồng ý → `toast.success('Đã xoá (demo)')` → đóng, **danh sách không đổi** | |
| Bấm ➕ *(nút chính góc phải)* | Điều hướng sang màn tạo | |
| Bấm **Lưu / Gửi duyệt / Duyệt** trong form | `toast.success('Đã lưu (demo)')` → quay lại màn danh sách sau `600ms` | ⭐ Không lưu dữ liệu |
| Bấm **Tiếp tục** trong wizard | Chuyển bước — `Steps` cập nhật, nội dung đổi | Bước lùi được |
| Bấm **Huỷ** | Quay lại màn trước | |
| Bấm **tab** | Điều hướng route con, thanh bên vẫn tô sáng menu cha | |
| Bấm nút **lọc** ▾ | Mở `Dropdown` — chọn mục thì đóng và `toast.info('Bộ lọc chỉ minh hoạ')` | Không lọc thật |
| Gõ vào **ô tìm kiếm** | Không lọc, chỉ nhận chữ | Có thể để `readOnly` cũng được |
| Bấm nút **▶ Chạy thử / Gửi thử / Chạy đối chiếu** | `Modal` hiện kết quả mẫu | Nội dung kết quả lấy từ ảnh |
| Bấm nút **⬇️ Xuất** | `toast.info('Chức năng xuất — minh hoạ')` | |
| Bấm **nút trong sơ đồ** | Điều hướng sang màn của thực thể đó | |
| Trỏ chuột lên **chip cắt chữ** | Hiện `title` gốc | |

**Ba trạng thái phải có ở mọi bảng**

| Trạng thái | Khi nào | Hiện gì |
|---|---|---|
| Bình thường | Có dữ liệu | Bảng |
| **Rỗng** | Bộ lọc không ra gì *(nếu về sau có lọc thật)* | `EmptyState` — biểu tượng + *"Không có dữ liệu phù hợp"* + nút xoá lọc |
| **Đang tải** | Chỉ dùng cho các màn nặng | Khung xám nhấp nháy `1.2s` rồi hiện dữ liệu — **tuỳ chọn**, làm nếu còn thời gian |

> 💡 **Mẹo làm demo có cảm giác thật:** thêm độ trễ giả `400–800ms` khi chuyển sang màn chi tiết, kèm khung xám. Không có độ trễ thì mọi thứ hiện tức thì, người xem lại thấy *"giả"*.

</details>

---

## 9. DỮ LIỆU MẪU

<details open>
<summary><b>Nguyên tắc và các con số phải giữ đúng</b></summary>

**Ba nguyên tắc**

| # | Nguyên tắc |
|:---:|---|
| **1** | ⭐ **Chép số liệu từ ảnh, không tự bịa.** Toàn bộ số trong 55 ảnh đã được đối chiếu chéo với tài liệu — tự đổi sẽ gây mâu thuẫn |
| **2** | **Danh sách trong ảnh chỉ hiện 4–6 dòng, dữ liệu mẫu nên có 12–20 dòng** để cuộn được và trông thật hơn. Dòng thêm phải **cùng phong cách** — tên bảng tiếng Việt không dấu, mã có tiền tố |
| **3** | **Mọi khoá ngoại phải khớp.** `JOB-0412` ghi ra `bi.doi_soat_giao_dich_A` thì bảng đó **phải tồn tại** trong `tables.ts`, và tab Nguồn gốc của nó **phải trỏ ngược lại** `JOB-0412` |

**Bảng số liệu chủ chốt — phải giữ nguyên trên mọi màn**

| Con số | Giá trị | Xuất hiện ở màn |
|---|---|---|
| Tổng số bảng | **11.482** | 1 · 21 · 23 · 53 |
| Bảng đang được kiểm chất lượng | **64** — tức **0,6%** | 23 · 53 |
| Điểm chất lượng toàn hệ thống | **87 / 100** | 23 · 53 |
| Bảng chưa gán miền | **4.334** — **38%** | 53 · 54 |
| Bảng chưa có người phụ trách | **7.578** *(có 3.904 = 34%)* | 53 |
| Tổng số job | **1.842** | 31 · 39 |
| Bảng đích của job chưa khai ở 1.1 | **214** | 31 |
| Số mẫu nạp | **168** — cổng chất lượng **0/168** | 36 |
| Số cột nhạy cảm | **412** = 268 `PD_BASIC` + 144 `PD_SENSITIVE` | 19 · 43 · 47 · 53 |
| Cột đã có chính sách che | **0 / 412** | 43 · 53 |
| Bảng trùng lặp do phân quyền chi nhánh | **41** | 45 |
| Tổng số chính sách quyền | **1.847** — 412 theo nhóm · 1.435 theo người | 42 |
| Chính sách vô thời hạn | **1.612** — **87%** | 42 |
| Chính sách nguồn "Thủ công" | **1.409** — **76%** | 42 · 48 |
| Tài khoản đã nghỉ việc chưa khoá | **9** — còn quyền trên **132 bảng** | 40 · 52 |
| Số loại kiểm tra trong thư viện luật | **28** | 21 |
| Số luật đang chạy | **795** | 21 · 23 |
| Tỉ lệ báo động giả | **18%** — ngưỡng đỏ **25%** | 53 |
| Số thuật ngữ | **218** — 142 đã gắn cột (65%) · 38 CDE | 16 |

**Bảng mẫu chính — dùng xuyên suốt mọi màn**

| Thực thể | Mã | Ghi chú |
|---|---|---|
| Bảng chính | `bi.doi_soat_giao_dich_A` | Tier 1 · Miền Kinh doanh · BDA Nguyễn Thị Phương · DE Trần Văn Hùng · 12.480.331 dòng · 2 cột `PD_SENSITIVE` · 7 luật chất lượng · 6 báo cáo dùng |
| Job sinh ra bảng đó | `JOB-0412` | 5 bước · lịch `0 0 6 * * ?` · giờ cam kết 07:00 |
| Mẫu nạp nguồn | `NAP-012` | SFTP đối tác A · 05:30 hằng ngày |
| Sự cố mẫu | `SC-0231` | Trên bảng chính |
| Yêu cầu quyền mẫu | `YC-0231` | Lê Minh Tuấn xin xem bảng chính |
| Thuật ngữ mẫu | `TN-0042` | Doanh thu ghi nhận · CDE · 18 cột đã gắn |
| Nhãn mẫu | `PD_SENSITIVE` | 144 cột |

> ⭐ **Chuỗi liên kết phải bấm được xuyên suốt:**
> `NAP-012` → `raw.doi_soat_A_tho` → `JOB-0412` → `bi.doi_soat_giao_dich_A` → `SC-0231` → `YC-0231`
> Đây là **kịch bản trình bày chính**. Dựng xong đợt nào cũng phải kiểm chuỗi này.

**`src/data/types.ts` — bộ kiểu tối thiểu**

```ts
export type Tier = 'Tier 1' | 'Tier 2' | 'Tier 3'
export type Tone = 'b' | 'g' | 'r' | 'o' | 'n' | 't'

export type TableRow = {
  id: string                 // 'bi.doi_soat_giao_dich_A'
  name: string
  description: string
  domain: string
  tier: Tier | null
  bda: string | null
  de: string | null
  rows: number
  format: 'Iceberg' | 'Hudi' | 'Parquet'
  zone: 'raw' | 'dwh' | 'bi' | 'mart' | 'ops' | 'crm' | 'fin' | 'ref'
  syncFrequency: string
  lifecycle: 'Nháp' | 'Đang dùng' | 'Sắp ngừng' | 'Đã ngừng'
  qualityScore: number | null
  ruleCount: number
  sensitiveColumnCount: number
  producedByJob: string | null    // 'JOB-0412'
  consumers: string[]             // tên báo cáo / job hạ nguồn
}

export type ColumnRow = {
  tableId: string; name: string; type: string; description: string
  glossaryTerm: string | null; tags: string[]
  businessRule: string | null; valueSet: string[] | null
  isKey: boolean; nullable: boolean
  nullPct: number; distinctCount: number; min: string | null; max: string | null
}
// … các kiểu còn lại khai tương tự, bám đúng cột hiện trong ảnh
```

</details>

---

## 10. ĐẶC TẢ TỪNG MÀN

> **Cách đọc mục này.** Mỗi màn có một khối ngắn: bố cục · cột hoặc trường · tương tác · dữ liệu cần.
> **Ý nghĩa nghiệp vụ của từng trường KHÔNG chép lại ở đây** — đọc mục *"Màn NN — …"* tương ứng trong `DMP-De-xuat-tool-Data-Management.md`.

<details open>
<summary><b>MODULE ① DATA CATALOG — màn 1 → 15</b></summary>

### Màn 1 — Danh sách bảng dữ liệu · `/catalog/tables`
- **Bố cục:** `KpiRow` 5 thẻ → `FilterBar` → `DataTable` → 2 hộp ghi chú
- **Cột:** Tên bảng *(có mô tả 1 dòng bên dưới, chữ mờ)* · Miền · Mức QT *(chip)* · BDA · DE · Số dòng *(phải)* · Độ tươi · Chất lượng · Trạng thái · thao tác
- **Tab:** Tất cả bảng · Bảng tôi phụ trách · **Chưa hoàn thiện hồ sơ** · Chờ duyệt · Đã ngừng dùng
- **Tương tác:** bấm tên bảng → màn 3 · ➕ Thêm bảng mới → màn 2
- **Dữ liệu:** `tables.ts` — 18 dòng, trong đó ≥ 4 dòng thiếu BDA/Tier để tab *Chưa hoàn thiện hồ sơ* có nghĩa

### Màn 2 — Thêm bảng mới · `/catalog/tables/create`
- **Bố cục:** `Steps` 4 bước → 2 cột: trái form, phải hộp ghi chú + xem trước
- **Trường:** Tên bảng · Mô tả nghiệp vụ · Miền · **Mức quan trọng (Tier)** · Vùng lưu trữ · Định dạng · **BDA phụ trách** · **DE phụ trách** · Chu kỳ cập nhật · Trạng thái vòng đời
- **Tương tác đặc biệt:** ⭐ gõ tên bảng sai chuẩn → hiện lỗi đỏ ngay dưới ô *(kiểm bằng regex `^[a-z][a-z0-9_]{2,62}$`)* · chọn **Tier 1** → khối *Điều kiện bắt buộc* đổi màu đỏ và liệt kê 5 điều kiện · nút Lưu **bị mờ** cho tới khi đủ trường bắt buộc
- **Dữ liệu:** danh sách miền, danh sách người dùng để chọn BDA/DE

### Màn 3 → 8 — Chi tiết bảng, 6 tab · `/catalog/tables/:id[/...]`
- **Khung chung:** `PageHeader` có tiêu đề = mã bảng, mô tả = *tên nghiệp vụ · BDA · DE · Miền*, nút `⬇️ Xuất metadata` `🔗 Chia sẻ` `✎ Sửa`, `Tabs` 6 mục
- **Màn 3 Tổng quan:** `KpiRow` 5 thẻ *(Độ tươi · Số dòng · Luật chất lượng · Lượt dùng/tuần · Dung lượng)* → 2 cột: trái mô tả nghiệp vụ + chip + bảng thông tin kỹ thuật; phải người phụ trách + hệ thống tiêu thụ + hoạt động gần đây
- **Màn 4 Cột:** bảng cột — Tên cột · Kiểu · Mô tả · **Thuật ngữ** · **Nhãn** · Khoá · Cho rỗng · **% rỗng** · **Số giá trị phân biệt** · Min/Max. ⭐ Bấm thuật ngữ → màn 17 · bấm nhãn → màn 19
- **Màn 5 Chất lượng:** danh sách luật đang chạy + kết quả + xu hướng 7 ngày *(thanh nhỏ)*. Bấm ➕ Gán luật → màn 24 · bấm luật hỏng → mở `Drawer` chi tiết
- **Màn 6 Nguồn gốc:** ⭐ **`FlowDiagram`** — cột trái nguồn, giữa bảng hiện tại, phải hạ nguồn. Nút bấm được → điều hướng. Có nút *Phân tích ảnh hưởng* → `Modal` liệt kê 6 báo cáo + nút xuất danh sách người cần báo
- **Màn 7 Quyền:** bảng ai có quyền gì, cột **Che dữ liệu** và **Nguồn chính sách**. Bấm ➕ Cấp quyền → màn 44
- **Màn 8 Lịch sử:** dòng thời gian thay đổi cấu hình — Giá trị cũ → Giá trị mới · Người thay đổi · IP

### Màn 9–10 — Nhóm bảng · `/catalog/groups[/create]`
- Danh sách nhóm: Tên · Mô tả · Số bảng · Người tạo · Trạng thái. Màn tạo có ô chọn hai cột *Bảng sẵn có → Bảng được truy cập*

### Màn 11–12 — Miền dữ liệu · `/catalog/domains[/create]`
- Danh sách dạng **cây 3 cấp** + bảng bên phải. Màn tạo: Tên miền · Miền cha · Mô tả · Người chịu trách nhiệm

### Màn 13–15 — Danh mục tham chiếu · `/catalog/refdata[/create|/:id]`
- **Màn 15** có 5 tab: **Dữ liệu** · Định nghĩa trường · Phiên bản · Chờ duyệt · Nhật ký
- ⭐ Tab *Chờ duyệt* có nút **Duyệt / Từ chối** → `Modal` xác nhận → `toast`
- ⭐ Tab *Phiên bản* có nút **So sánh** → `Modal` hiện khác biệt kiểu thêm/bớt dòng

</details>

<details open>
<summary><b>MODULE ② GOVERNANCE — màn 16 → 20</b></summary>

### Màn 16 — Danh sách thuật ngữ · `/governance/glossary`
- **Cột:** Mã · Tên thuật ngữ · Thuộc từ điển · **CDE** · **Số cột đã gắn** · Chủ sở hữu · Người phụ trách · Phiên bản · Trạng thái
- ⭐ Cột *Số cột đã gắn* bằng `0` → tô đỏ. Đây là điểm nhấn của màn

### Màn 17 — Chi tiết thuật ngữ · `/governance/glossary/:id`
- 2 cột. Trái: định nghĩa + thông tin quản trị + **bảng 18 cột đang gắn**. Phải: hộp giải thích tác dụng + ý nghĩa cờ CDE + lịch sử phiên bản
- Bấm tên bảng trong danh sách cột → màn 4

### Màn 18 — Thêm thuật ngữ · `/governance/glossary/create`
- `Steps` 3 bước. Trường: Mã *(tự sinh)* · Tên · Thuộc từ điển · Định nghĩa · Đơn vị tính · **Bí danh** *(chip nhập nhiều)* · Thuật ngữ liên quan · **Đánh dấu CDE**
- ⭐ Bước 2 *Gắn vào cột* — nếu để trống, hiện cảnh báo đỏ *"Không gắn cột nào thì thuật ngữ vô dụng"*, vẫn cho lưu

### Màn 19 — Cây nhãn phân loại · `/governance/classification`
- 3 cột: `TreeView` trái · giữa chi tiết nhãn + **bảng 4 chính sách tự áp** · phải danh sách 144 cột mang nhãn
- Bấm nút *🤖 Xem 23 cột hệ thống nghi ngờ* → `Modal` bảng gợi ý có nút Xác nhận / Bỏ qua từng dòng

### Màn 20 — Thêm nhãn · `/governance/classification/create`
- Trường: Mã nhãn *(mono, có ghi chú "đồng bộ sang OPA nên không đổi được")* · Tên hiển thị · Nhãn cha · Mức nhạy cảm · Mô tả · Căn cứ pháp lý + bảng **chính sách mặc định** theo nhóm

</details>

<details open>
<summary><b>MODULE ③ DATA QUALITY — màn 21 → 30</b></summary>

### Màn 21 — Thư viện 28 loại kiểm tra · `/quality/rules`
- **Cột:** Mã · **Mã kỹ thuật** *(mono)* · Tên loại · **Chiều chất lượng** · Áp cho · Tham số phải khai · Nguồn · **Lượt dùng**
- ⭐ Hai dòng `referential_integrity` và `cross_table_sum` có **Lượt dùng = 0** → tô đỏ + có chú thích riêng bên dưới
- **Dữ liệu:** đủ **28 dòng** — danh sách đầy đủ ở tài liệu đề xuất, mục 3.1

### Màn 22 — Tạo loại kiểm tra · `/quality/rules/create`
- `Steps` 3 bước: Thông tin loại → Tham số → **Ngưỡng mặc định**
- ⭐ Bước 3 có bảng giải thích **ngưỡng 3 cấp** (loại → bảng → lần gán)
- Có khối `CodeBlock` hiện câu SQL mẫu dùng biến `{bang_dich}` `{bang_nguon}`

### Màn 23 — Bảng điều khiển chất lượng · `/quality/board`
- `KpiRow` → dải **6 chiều chất lượng** *(6 thanh `ProgressBar`)* → bảng điểm theo bảng
- ⭐ Thẻ *Bảng đang được kiểm — 64/11.482 (0,6%)* phải nằm **ngay cạnh** thẻ Điểm chất lượng

### Màn 24 — Gán luật cho bảng · `/quality/assign`
- `Steps` 5 bước. ⭐ Màn cao nhất hệ thống — cuộn dài
- Có khối **nguồn gợi ý luật** *(từ quy tắc nghiệp vụ · tập giá trị · kết quả Profiling)*, **bảng ngưỡng 3 cấp**, và **5 ô chọn hành động khi luật hỏng**

### Màn 25 — Phân tích dữ liệu (Profiling) · `/quality/profiling`
- Bảng chỉ số theo cột + nút *Gợi ý luật* trên từng dòng → `Modal` đề xuất luật nên gán
- Tab: Theo cột · Phân bố giá trị · Lịch sử quét *(hai tab sau dùng lại cùng bảng, đổi tiêu đề)*

### Màn 26 — Danh sách sự cố · `/quality/incidents`
- ⭐ `StatusBar` **6 trạng thái** có số đếm: Mới → Đã gán → Đang xử lý → Chờ duyệt → Đã giải quyết → Đóng
- **Cột:** Mã · Bảng/cột · Luật hỏng · Mức ưu tiên · Người xử lý · Hạn xử lý · Trạng thái · Đã mở bao lâu

### Màn 27 — Chi tiết sự cố · `/quality/incidents/:id`
- 2 cột. Trái: thông tin + **dòng lỗi mẫu** + `Timeline` diễn biến + ô bình luận. Phải: người xử lý + hạn + **khối 4 mắt** + nút hành động
- ⭐ **Nút *Đóng sự cố* mở `Modal` bắt buộc chọn 1 trong 6 lý do** — trong đó có *"Cảnh báo sai — luật đặt chưa đúng"*
- ⭐ Nếu người dùng hiện tại **là người xử lý** thì nút *Đóng* bị **vô hiệu hoá** kèm chú thích *"Nguyên tắc 4 mắt — chuyển sang Chờ duyệt để người khác đóng"*

### Màn 28–29 — Cảnh báo · `/quality/alerts[/create]`
- Danh sách quy tắc cảnh báo + màn tạo có **4 chế độ gửi** *(ngay · gom lô · tổng hợp ngày · tổng hợp tuần)* và ô **chống trùng**

### Màn 30 — Kênh gửi · `/quality/alerts/channels`
- **Cột:** Mã kênh · Tên · Loại · Cấu hình · Trạng thái · **Đã gửi/tháng** · **Thất bại**
- ⭐ Kênh có tỉ lệ thất bại `> 1%` → tô đỏ · nút **▶ Gửi thử** → `Modal` kết quả

</details>

<details open>
<summary><b>MODULE ④ INGESTION & ORCHESTRATION — màn 31 → 39</b></summary>

### Màn 31 — Danh sách job · `/orchestration/jobs`
- **Cột:** Mã job · Tên · Nhóm · **Bảng đích** · Bước · Lịch chạy · Lần chạy gần nhất · Kết quả · **Quét nguồn gốc** · Duyệt
- ⭐ Bảng đích không có trong danh mục → hiện dòng cảnh báo đỏ nhỏ ngay dưới tên bảng
- ⭐ Thẻ *Bật quét nguồn gốc* để giá trị **`?`** kèm chú thích *"chưa có số liệu — H5"* — **giữ nguyên, đây là chủ ý**

### Màn 32 — Tạo job · `/orchestration/jobs/create`
- `Steps` 5 bước, đang ở bước ③. Bố cục 2 cột
- ⭐ Ô **Bảng đích** là `Dropdown` chọn từ danh mục — chọn xong hiện ngay hộp thông tin bảng (Tier, BDA, số luật, số báo cáo)
- ⭐ Ô **Bật quét nguồn gốc** mặc định **bật**; nếu bảng đích là Tier 1 thì **không tắt được**, hiện chú thích đỏ

### Màn 33 — Chi tiết job › tab Bước · `/orchestration/jobs/:id`
- ⭐ **`FlowDiagram`** 5 nút bước, có nhánh song song → hội tụ. Nút *Bước 4* đang chọn tô xanh, nút *Bước 5* viền xanh lá + nhãn `ĐÍCH`
- Dưới sơ đồ: bảng danh sách bước + `CodeBlock` câu SQL của bước đang chọn
- Cột phải: bảng đích · **bảng nguồn dò được** *(có dòng ghi `Viết thẳng tên — BỎ SÓT` màu đỏ)* · ô bật quét nguồn gốc

### Màn 34 — tab Lần chạy + Lịch · `/orchestration/jobs/:id/runs`
- Bảng lịch sử chạy + **biểu đồ dòng thời gian các bước** *(thanh ngang lệch nhau, dựng bằng div có `left` và `width` theo %)*
- Cột phải: cấu hình lịch · **giờ cam kết** · người nhận cảnh báo

### Màn 35 — tab Phiên bản · `/orchestration/jobs/:id/versions`
- Bảng 12 phiên bản + `CodeBlock` **so sánh** kiểu thêm/bớt dòng *(dòng bỏ nền `#3D1D1D`, dòng thêm nền `#123522`)*
- Cột phải: khối **hai người đang mở cùng job** + giải thích quay lại phiên bản cũ

### Màn 36 — Danh sách mẫu nạp · `/ingestion/templates`
- **Cột:** Mã mẫu · Tên · **Loại cửa nạp** *(6 loại, chip ngọc)* · Nguồn · Bảng đích · Định dạng · Lịch · **Cổng chất lượng** · Màn SQLWF cũ
- Dưới bảng: khối **6 màn cũ gộp về một menu**

### Màn 37 — Tạo mẫu nạp · `/ingestion/templates/create`
- `Steps` 5 bước, đang ở bước ④ **Cổng chất lượng**
- ⭐ Bảng luật kiểm tại cửa + bảng **3 mức xử lý** (Chặn cả lô / Tách dòng lỗi / Chỉ cảnh báo)

### Màn 38 — Vùng chờ · `/ingestion/quarantine`
- **Cột:** Mã lô · Đến từ mẫu nạp · Thời điểm · **Mức chặn** · Vì sao bị giữ · Dòng bị giữ · Sự cố · Trạng thái
- Dưới: bảng **dòng lỗi mẫu** + bảng **4 hành động trên một lô**
- ⭐ Bấm **✔ Cho qua** → `Modal` **bắt buộc điền lý do**, nút Đồng ý mờ tới khi có ≥ 20 ký tự
- Bấm mã sự cố → màn 27

### Màn 39 — Giám sát pipeline · `/orchestration/monitor`
- ⭐ **`FlowDiagram`** lớn nhất: 2 hàng, 9 nút, có cạnh **nét đứt đỏ/cam** thể hiện lan lỗi
- Dưới: bảng tác vụ + bảng **4 tổ hợp trạng thái chạy × chất lượng**
- Cột phải: giải thích lan lỗi + bảng **chặn lan lỗi**

</details>

<details open>
<summary><b>MODULE ⑤ DATA SECURITY — màn 40 → 52</b></summary>

### Màn 40 — Danh sách người dùng · `/security/users`
- **Cột:** Tài khoản · Họ tên · Vai trò · Thuộc nhóm · Nhãn người dùng · Số bảng có quyền · Trạng thái
- ⭐ Dòng người đã nghỉ việc: tên tô **đỏ**, trạng thái `Chưa khoá` chip đỏ
- Dưới: bảng **phân biệt quyền MENU và quyền DỮ LIỆU**

### Màn 41 — Nhóm & Quyền menu · `/security/users/groups`
- Bảng nhóm + ⭐ **ma trận Menu × Vai trò** *(9 menu × 5 vai trò, ô là chip: Xem / Xem·Sửa / Xem·Duyệt / Xem·Sửa·Duyệt / —)*
- Cột phải: bảng so sánh *ma trận ở đây* vs *chính sách ở 5.2*

### Màn 42 — Chính sách › tab Quyền dữ liệu · `/security/policies/data`
- `Tabs` 4 mục dùng chung cho màn 42–47 *(43+44 cùng tab Che, 45+46 cùng tab Lọc)*
- **Cột:** Đối tượng · Loại · **Phạm vi** *(4 cấp có biểu tượng)* · Quyền · Cột loại trừ · **Thời hạn** · **Nguồn** · Trạng thái
- Bấm mã yêu cầu ở cột Nguồn → màn 50

### Màn 43 — tab Che dữ liệu · `/security/policies/mask`
- ⭐ Trên cùng: hộp đỏ *"Tính năng chưa tồn tại trong SQLWF — đã kiểm tra mã nguồn"*
- Bảng chính sách che + bảng **8 kiểu che** có cột *Giá trị gốc* → *Người dùng thấy*
- Cột phải: khối **đường đi của câu truy vấn** *(`CodeBlock` tối)* + khối **hai lỗ hổng phải bịt**

### Màn 44 — Thêm chính sách che · `/security/policies/mask/create`
- `Steps` 4 bước. Trái: chọn phạm vi *(theo nhãn / theo cột / theo tên cột)* + chọn nhãn + ngoại lệ; và khối *Áp cho ai*
- Phải: ⭐ **bảng 8 kiểu che dạng nút chọn (radio)** — chọn kiểu nào thì khối `CodeBlock` bên dưới **đổi câu SQL viết lại tương ứng**
- ⭐ Khối *Chính sách này sẽ động tới*: 144 cột · 184 người · **11 báo cáo** — kèm cảnh báo đỏ

### Màn 45 — tab Lọc theo dòng · `/security/policies/rowfilter`
- Bảng điều kiện lọc + `CodeBlock` cơ chế nối `AND` + bảng **hai kiểu điều kiện** + bảng **bỏ được 41 bảng trùng lặp**

### Màn 46 — Thêm điều kiện lọc · `/security/policies/rowfilter/create`
- `Steps` 4 bước. ⭐ Ô **Biểu thức điều kiện** là khối nền tối, gõ được, có tô màu biến `${…}` màu vàng
- Bảng **5 biến dùng được** · khối **xem thử** hiện số dòng trước/sau lọc
- ⭐ Nút **Lưu bị khoá** cho tới khi bấm *Chạy đối chiếu 5 tài khoản* → `Modal` kết quả đạt → nút Lưu mở

### Màn 47 — tab Chính sách theo nhãn · `/security/policies/by-tag`
- `TreeView` trái + bảng **5 dòng chính sách áp cho 144 cột** + bảng **thứ tự ưu tiên 4 cấp**

### Màn 48 — Danh sách yêu cầu · `/security/requests`
- ⭐ `StatusBar` **5 trạng thái** · **Cột:** Mã YC · Người xin · Xin quyền trên · Loại quyền · **Lý do** · Thời hạn xin · Người duyệt · Trạng thái · **Đã chờ**

### Màn 49 — Xin quyền · `/security/requests/create`
- `Steps` 3 bước. Chọn bảng xong → hiện hộp hồ sơ bảng
- ⭐ Ô **Lý do** đếm ký tự, dưới `30` thì viền đỏ + chữ *"còn thiếu N ký tự"*
- ⭐ Ô **Thời hạn** là `Dropdown` **không có** mục *Vô thời hạn*
- ⭐ Khối gợi ý *"Đã có 4/9 người trong nhóm xin bảng này — nên xin theo nhóm"* có nút chuyển

### Màn 50 — Duyệt yêu cầu · `/security/requests/:id`
- Trái: nội dung yêu cầu *(các ô `readOnly`)* + khối **quyết định** có 3 lựa chọn mức + cột loại trừ + thời hạn + ghi chú
- Phải: ⭐ **bảng 5 thông tin hệ thống chuẩn bị sẵn** + khối *duyệt xong thì gì xảy ra*
- Bấm **✔ Duyệt** → `Modal` xác nhận tóm tắt → `toast.success` → về màn 48

### Màn 51 — Nhật ký kiểm toán · `/security/audit`
- **Cột:** Thời điểm · Người dùng · Hành động · Đối tượng · Chi tiết · Số dòng · ⭐ **Chính sách nào quyết định** · Địa chỉ IP · Kết quả
- Dòng *Từ chối* và *Cảnh báo* tô màu tương ứng ở cột ghi chú

### Màn 52 — Báo cáo quyền · `/security/report`
- Ô chọn người dùng ở trên + `KpiRow` + bảng quyền có cột **90 ngày qua có dùng không** và **Đề xuất** *(Giữ / Thu hồi / Rà soát)*
- Dưới: bảng **cột bị che đối với người này**
- ⭐ Nút *Tra theo BẢNG thay vì theo người* → điều hướng sang màn 7

</details>

<details open>
<summary><b>MODULE ⑥ OPERATIONS — màn 53 → 55</b></summary>

### Màn 53 — Sức khoẻ dữ liệu · `/operations/health`
- ⭐ Hàng trên: **thẻ tối** *(điểm 87/100 + hộp cảnh báo đỏ "chỉ tính trên 0,6% số bảng")* chiếm `flex:1.3`, bên phải là **lưới 2×3 thẻ số liệu** chiếm `flex:2.4`
- Giữa trái: **7 thanh `ProgressBar`** có vạch mục tiêu · dưới: bảng **4 bảng yếu nhất đang được dùng nhiều**
- Phải: bảng *6 module đóng góp gì* + khối **tỉ lệ báo động giả** + ghi chú `report-management`

### Màn 54 — Sức khoẻ theo miền · `/operations/health/by-domain`
- Bảng 5 miền có cột **thanh độ phủ nhỏ** trong ô
- ⭐ Dòng cuối *Chưa gán miền — 4.334 bảng* tô đỏ, cột người chịu trách nhiệm ghi *"— không ai"*

### Màn 55 — Cấu hình hệ thống · `/operations/settings`
- `Tabs` 5 mục — nhưng **tất cả nội dung hiện trên cùng một màn** *(bảng kết nối · bảng định nghĩa Tier · bảng chuẩn đặt tên · các ô tham số)*
- ⭐ Dòng kết nối `HDFS_PARTNER_B` trạng thái **Lỗi xác thực** chip đỏ · có nút **▶ Kiểm tra kết nối** → `Modal` kết quả

</details>

---

## 11. CHIA ĐỢT VÀ ĐIỀU KIỆN HOÀN THÀNH

<details open>
<summary><b>Năm đợt — mỗi đợt chạy được, không chờ đợt sau</b></summary>

### ĐỢT 1 — Khung + Module ① · **15 màn**

| Việc | Ghi chú |
|---|---|
| Khởi tạo dự án, cấu hình Tailwind, biến màu | Mục 2 |
| Dựng **18 component** ở `src/ui/` | ⭐ **Làm đủ, đừng làm tắt** |
| `AppShell` + `Sidebar` 21 mục + `PageHeader` | Mục 4 |
| Router 55 route — **54 route trỏ tạm sang trang "Đang dựng"** | Để bấm menu nào cũng không lỗi |
| Dựng màn **1 → 15** | |
| `data/tables.ts` `columns.ts` `domains.ts` `groups.ts` `refdata.ts` | |

**Hoàn thành khi:**
- ✔ Bấm được cả 21 mục thanh bên, không mục nào lỗi trắng
- ✔ Màn 1 → bấm tên bảng → màn 3 → chuyển đủ 6 tab
- ✔ Màn 6 sơ đồ nguồn gốc: bấm nút → điều hướng sang bảng khác
- ✔ Màn 2: gõ tên sai chuẩn ra lỗi đỏ; chọn Tier 1 đổi khối điều kiện

---

### ĐỢT 2 — Module ② + ③ · **15 màn** *(16 → 30)*

**Hoàn thành khi:**
- ✔ Màn 4 bấm thuật ngữ → màn 17, bấm nhãn → màn 19
- ✔ Màn 27: nút *Đóng sự cố* mở `Modal` bắt buộc chọn lý do; nếu người dùng là người xử lý thì nút bị vô hiệu hoá
- ✔ Màn 21 có đủ **28 dòng**

---

### ĐỢT 3 — Module ④ · **9 màn** *(31 → 39)*

**Hoàn thành khi:**
- ✔ `FlowDiagram` chạy đúng ở màn 33 *(nhánh song song)* và 39 *(2 hàng, cạnh nét đứt)*
- ✔ Chuỗi bấm `NAP-012` → `raw.doi_soat_A_tho` → `JOB-0412` → `bi.doi_soat_giao_dich_A` thông suốt
- ✔ Màn 38: nút *Cho qua* bắt buộc điền lý do mới bấm được

---

### ĐỢT 4 — Module ⑤ · **13 màn** *(40 → 52)*

**Hoàn thành khi:**
- ✔ Màn 44: đổi kiểu che → câu SQL bên dưới đổi theo
- ✔ Màn 46: nút Lưu khoá cho tới khi chạy đối chiếu
- ✔ Màn 49: ô Lý do đếm ký tự, dưới 30 thì báo lỗi
- ✔ Màn 50: bấm Duyệt → `Modal` → `toast` → về màn 48

---

### ĐỢT 5 — Module ⑥ + hoàn thiện · **3 màn** *(53 → 55)* + rà soát

| Việc |
|---|
| Dựng màn 53 → 55 |
| **Rà soát toàn bộ**: mở lần lượt 55 route, đối chiếu với 55 ảnh |
| Bộ chọn người dùng ở đầu trang |
| Độ trễ giả + khung xám khi chuyển màn chi tiết |
| Kiểm mọi liên kết chéo giữa các module |
| Viết `README.md`: cách chạy + **kịch bản trình bày 10 phút** |

**Kịch bản trình bày gợi ý — viết vào README**

| Bước | Màn | Nói gì |
|:---:|:---:|---|
| 1 | 53 | *"Điểm chất lượng 87 — nhưng chỉ tính trên 0,6% số bảng"* |
| 2 | 1 → 3 | *"Đây là nguồn sự thật. 11.482 bảng, nhưng 7.578 bảng không ai nhận"* |
| 3 | 6 | *"Bảng này hỏng thì ảnh hưởng tới đâu — hiện không ai trả lời được"* |
| 4 | 39 | *"Job chạy thành công vẫn có thể sinh ra số sai"* |
| 5 | 43 → 44 | *"144 cột CCCD và số điện thoại hiện trả về nguyên giá trị"* |
| 6 | 46 | *"41 bảng sao chép chỉ để phân quyền theo chi nhánh — bỏ được hết"* |
| 7 | 48 → 50 | *"Xin quyền hiện qua chat. 87% quyền không có hạn"* |

</details>

---

## 12. NHỮNG CHỖ DỄ LÀM SAI

<details open>
<summary><b>Mười lỗi đã thấy khi dựng bộ ảnh — tránh lặp lại</b></summary>

| # | Lỗi | Cách tránh |
|:---:|---|---|
| 1 | **Chip bị xuống dòng** làm vỡ chiều cao dòng bảng | Luôn `whitespace-nowrap` cho ô chứa chip |
| 2 | **Cột thao tác 👁 ✎ ▶ xuống 2 dòng** | `whitespace-nowrap` cho ô cuối |
| 3 | **Biểu thức chính quy hiện sai** — `{8}` thành `{{8}}` | Trong JSX viết `{'^(84|0)(3|5|7|8|9)[0-9]{8}$'}` |
| 4 | **Mũi tên sơ đồ không chạm nút** | Toạ độ cạnh phải khớp mép nút; vẽ theo đoạn ngang→dọc→ngang, không vẽ đường xiên |
| 5 | **Hai hộp ghi chú cạnh nhau cao lệch** | Đặt `items-stretch` cho hàng, hoặc bổ sung nội dung cho hộp ngắn |
| 6 | **Số liệu mâu thuẫn giữa các màn** | Mọi con số lấy từ `src/data/`, không gõ thẳng trong màn. Xem bảng số liệu chủ chốt mục 9 |
| 7 | **Menu con không tô sáng khi ở route con** | Tô sáng theo `pathname.startsWith(route)` |
| 8 | **Emoji trong chip cỡ nhỏ hiện thành ô vuông** | Không đặt emoji trong chip; emoji chỉ dùng ở nhãn menu và tiêu đề |
| 9 | **Bảng quá nhiều cột bị tràn ngang** | Đặt `width` cho cột chữ dài, cho phép xuống dòng ở cột mô tả, `nowrap` ở cột ngắn |
| 10 | **Dựng lại watermark đen ở đáy** | Không có trong demo |

</details>

---

## 13. NGHIỆM THU

<details open>
<summary><b>Bảng kiểm trước khi báo cáo xong</b></summary>

| # | Hạng mục | Đạt |
|:---:|---|:---:|
| 1 | `npm run dev` chạy, không lỗi trong console | ☐ |
| 2 | 55 route mở được, không route nào trắng hoặc lỗi | ☐ |
| 3 | 21 mục thanh bên bấm được, tô sáng đúng kể cả ở route con | ☐ |
| 4 | Mọi màn có tab thì tab chuyển được và là route thật | ☐ |
| 5 | Mọi mã trong bảng *(bảng, job, sự cố, yêu cầu, thuật ngữ)* bấm được và tới đúng chỗ | ☐ |
| 6 | Chuỗi `NAP-012 → raw.doi_soat_A_tho → JOB-0412 → bi.doi_soat_giao_dich_A → SC-0231 → YC-0231` thông suốt | ☐ |
| 7 | Mọi nút ➕ mở được màn tạo tương ứng | ☐ |
| 8 | Mọi nút Lưu hiện `toast` rồi quay lại | ☐ |
| 9 | Ba sơ đồ *(màn 6, 33, 39)* vẽ đúng, nút bấm được | ☐ |
| 10 | Sáu ràng buộc đặc biệt chạy đúng: **màn 2** kiểm tên · **màn 27** 4 mắt · **màn 38** bắt buộc lý do · **màn 44** đổi kiểu che đổi SQL · **màn 46** khoá Lưu tới khi đối chiếu · **màn 49** đếm ký tự lý do | ☐ |
| 11 | Đối chiếu từng màn với ảnh trong `assets/dmp/` — bố cục, thứ tự cột, màu chip khớp | ☐ |
| 12 | Không màn nào có số liệu mâu thuẫn với bảng mục 9 | ☐ |
| 13 | `README.md` có hướng dẫn chạy + kịch bản trình bày | ☐ |

</details>

---

## 14. CÂU HỎI CÓ THỂ PHÁT SINH — TRẢ LỜI SẴN

<details open>
<summary><b>Bảy câu hay gặp</b></summary>

| Câu hỏi | Trả lời |
|---|---|
| *"Không tìm thấy thư mục ảnh `assets/dmp/`?"* | Ảnh nằm cạnh tài liệu đề xuất, đường dẫn `docs/assets/dmp/` trong repo. **Không có ảnh thì không dựng** — hỏi lại người giao việc |
| *"Có nên thêm biểu đồ đẹp hơn không?"* | ❌ Không. Mọi biểu đồ trong ảnh đều là thanh ngang hoặc SVG tĩnh. Thêm thư viện chart làm demo lệch khỏi thiết kế |
| *"Có nên làm responsive không?"* | ❌ Không. `min-width: 1440px` |
| *"Dữ liệu ít quá trông giả — có được thêm không?"* | ✔ Được, thêm tới 12–20 dòng mỗi bảng. Nhưng **giữ nguyên các con số ở mục 9** và giữ đúng phong cách đặt tên |
| *"Form nên lưu được cho thật hơn không?"* | Đã chốt **không lưu**. Nếu về sau muốn nâng: thêm một `Context` giữ dữ liệu trong bộ nhớ *(khoảng 60 dòng)*, các màn đọc từ đó thay vì đọc thẳng `src/data/`. **Chỉ làm khi được yêu cầu** |
| *"Tên tool đổi thì sửa ở đâu?"* | `src/config.ts` — một chỗ duy nhất |
| *"Thấy tài liệu và ảnh lệch nhau thì theo cái nào?"* | **Ảnh** cho bố cục · **Tài liệu** cho nghiệp vụ. Nếu lệch về số liệu thì theo **bảng mục 9** của plan này |

</details>

---

<div align="center">

**HẾT PLAN**

*Đầu vào bắt buộc: `DMP-De-xuat-tool-Data-Management.md` + 55 ảnh trong `assets/dmp/`*
*Đầu ra: ứng dụng React chạy bằng `npm run dev`, 21 menu · 55 màn*

</div>
