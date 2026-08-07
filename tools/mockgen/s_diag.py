# -*- coding: utf-8 -*-
"""Hai sơ đồ của Phần A — vẽ thành ảnh để xuất được ra PDF/Word/HTML."""

CSS = """
* { box-sizing:border-box; margin:0; padding:0; }
body { font-family:"Segoe UI",Roboto,Arial,sans-serif; background:#fff; width:1280px; padding:26px 30px; }
.title { font-size:15px; font-weight:700; color:#101828; margin-bottom:3px; }
.hint { font-size:12px; color:#667085; margin-bottom:16px; }
.band { border:1.5px solid #d0d5dd; border-radius:11px; padding:14px 16px 16px; margin-bottom:15px; }
.band .cap { font-size:11.5px; font-weight:700; letter-spacing:.4px; color:#475467; margin-bottom:11px; }
.row { display:flex; align-items:stretch; gap:0; }
.bx { flex:1; border-radius:9px; padding:11px 12px; text-align:center; }
.bx .no { font-size:19px; font-weight:800; line-height:1.1; }
.bx .nm { font-size:13.5px; font-weight:700; margin-top:3px; }
.bx .ds { font-size:11.5px; margin-top:5px; line-height:1.45; }
.ar { width:34px; display:flex; align-items:center; justify-content:center;
      font-size:20px; color:#98a2b3; flex-shrink:0; }
.gap { width:12px; flex-shrink:0; }
.link { text-align:center; font-size:11.5px; color:#667085; margin:6px 0 9px;
        letter-spacing:.3px; }
.flow { background:#eef2ff; border:1.5px solid #6172f3; color:#2d31a6; }
.cross { background:#fffaeb; border:1.5px solid #f79009; color:#93370d; }
.ok   { background:#ecfdf3; border:1.5px solid #12b76a; color:#05603a; }
.warn { background:#fffaeb; border:1.5px solid #f79009; color:#93370d; }
.bad  { background:#fef3f2; border:1.5px solid #f04438; color:#912018; }
.wm { margin-top:14px; background:#1f2937; color:#c8d0dc; font-size:11px; padding:6px 12px;
      border-radius:6px; display:flex; justify-content:space-between; }
.wm b { color:#ffd479; }
"""


def _bx(cls, no, nm, ds):
    return (f'<div class="bx {cls}"><div class="no">{no}</div>'
            f'<div class="nm">{nm}</div><div class="ds">{ds}</div></div>')


def _page(title, hint, body, note):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>'
            f'<div class="title">{title}</div><div class="hint">{hint}</div>{body}'
            f'<div class="wm"><span>{note}</span>'
            f'<span><b>Sơ đồ do BA dựng</b> — dùng chung bộ số ① ② ③ ④ ⑤ và Ⓐ Ⓑ Ⓒ Ⓓ với phần mô tả bên dưới</span>'
            f'</div></body></html>')


# ------------------------------------------------------------------ Sơ đồ 1
def flow():
    arrow = '<div class="ar">▶</div>'
    chang = arrow.join([
        _bx("flow", "①", "NGUỒN", "CSDL nghiệp vụ<br>File đối tác<br>Log, sự kiện"),
        _bx("flow", "②", "NẠP", "Đưa về kho<br>giữ nguyên bản gốc"),
        _bx("flow", "③", "LƯU", "Định dạng bảng mở<br>có phiên bản, sửa/xoá được"),
        _bx("flow", "④", "BIẾN ĐỔI", "Làm sạch, ghép<br>tổng hợp bằng SQL"),
        _bx("flow", "⑤", "KHAI THÁC", "Báo cáo, dashboard<br>API, mô hình AI"),
    ])
    gap = '<div class="gap"></div>'
    lop = gap.join([
        _bx("cross", "Ⓐ", "DANH MỤC & METADATA",
            "Có bảng nào · nghĩa là gì · ai phụ trách<br>lấy từ đâu · ai đang dùng"),
        _bx("cross", "Ⓑ", "CHẤT LƯỢNG & GIÁM SÁT",
            "Dữ liệu hôm nay có đúng không<br>sai thì ai biết · ai sửa"),
        _bx("cross", "Ⓒ", "BẢO MẬT & QUYỀN",
            "Ai được xem cột nào<br>người ngoài nhìn thấy gì"),
        _bx("cross", "Ⓓ", "ĐIỀU PHỐI",
            "Job nào chạy trước<br>nguồn chưa về thì có chạy không"),
    ])
    body = (f'<div class="band"><div class="cap">5 CHẶNG — DỮ LIỆU CHẢY QUA, TỪ TRÁI SANG PHẢI</div>'
            f'<div class="row">{chang}</div></div>'
            f'<div class="link">▲ &nbsp; 4 lớp bên dưới áp lên TOÀN BỘ 5 chặng ở trên &nbsp; ▲</div>'
            f'<div class="band" style="border-color:#f79009;background:#fffdf7">'
            f'<div class="cap" style="color:#93370d">'
            f'4 LỚP XUYÊN SUỐT — ĐÂY LÀ PHẦN THỊ TRƯỜNG TẬP TRUNG 5 NĂM QUA</div>'
            f'<div class="row">{lop}</div></div>')
    return _page("Luồng dữ liệu chuẩn của thị trường",
                 "Quản trị dữ liệu KHÔNG phải một chặng — nó là lớp xuyên suốt áp lên cả 5 chặng.",
                 body, "Mục 1 — Luồng dữ liệu chuẩn của thị trường")


# ------------------------------------------------------------------ Sơ đồ 2
def sqlwf():
    arrow = '<div class="ar">▶</div>'
    chang = arrow.join([
        _bx("ok", "①", "NGUỒN", "✅ <b>Đủ</b>"),
        _bx("ok", "②", "NẠP", "✅ <b>Đủ</b><br>5 cửa nạp"),
        _bx("warn", "③", "LƯU", "🟠 <b>Hở</b><br>Parquet thuần<br>chưa có Iceberg"),
        _bx("ok", "④", "BIẾN ĐỔI", "✅ <b>Đủ</b><br>TaskUtil / Spark"),
        _bx("ok", "⑤", "KHAI THÁC", "✅ <b>Đủ</b><br>Query + API"),
    ])
    gap = '<div class="gap"></div>'
    lop = gap.join([
        _bx("warn", "Ⓐ", "DANH MỤC & METADATA",
            "🟠 <b>Hở</b><br>chưa có danh mục thật · tìm kiếm yếu<br>"
            "nguồn gốc dừng ở mức bảng · chưa có nhãn cột"),
        _bx("bad", "Ⓑ", "CHẤT LƯỢNG & GIÁM SÁT",
            "🔴 <b>Hở nhiều</b><br>mới có 11 chỉ số thống kê<br>"
            "chưa có luật kiểm tra nào"),
        _bx("warn", "Ⓒ", "BẢO MẬT & QUYỀN",
            "🟠 <b>Hở</b><br>mạnh ở mức bảng<br>chưa có quyền/che dữ liệu mức cột"),
        _bx("ok", "Ⓓ", "ĐIỀU PHỐI",
            "✅ <b>Đủ</b><br>Pentaho lo lịch chạy<br>và phụ thuộc job"),
    ])
    body = (f'<div class="band"><div class="cap">5 CHẶNG — SQLWF PHỦ TỐT, CHỈ HỞ CHẶNG ③</div>'
            f'<div class="row">{chang}</div></div>'
            f'<div class="link">▲ &nbsp; nhưng 4 lớp xuyên suốt thì hở nhiều &nbsp; ▲</div>'
            f'<div class="band" style="border-color:#f04438;background:#fffbfa">'
            f'<div class="cap" style="color:#912018">'
            f'4 LỚP XUYÊN SUỐT — ĐÂY LÀ TOÀN BỘ KHOẢNG CÁCH VỚI THỊ TRƯỜNG</div>'
            f'<div class="row">{lop}</div></div>')
    return _page("SQLWF đang đứng ở đâu trên luồng đó",
                 "SQLWF gộp cả 5 chặng vào một nền tảng — đó là điểm mạnh. Khoảng cách nằm ở 4 lớp xuyên suốt.",
                 body, "Mục 3 — SQLWF đang đứng ở đâu trên luồng đó")


SCREENS = {"diag-01-luong-thi-truong": flow, "diag-02-sqlwf-tren-luong": sqlwf}
