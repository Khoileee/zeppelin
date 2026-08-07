# -*- coding: utf-8 -*-
"""Sơ đồ tổng quan module DMP — bản chốt sau kiểm kê mã nguồn."""

CSS = """
* { box-sizing:border-box; margin:0; padding:0; }
body { font-family:"Segoe UI",Roboto,Arial,sans-serif; background:#fff; width:1560px; padding:20px 24px; }
.tt { font-size:16px; font-weight:700; color:#101828; margin-bottom:2px; }
.st { font-size:12px; color:#667085; margin-bottom:8px; }
.lg { display:flex; gap:16px; font-size:11.5px; color:#344054; margin-bottom:14px; }
.lg b { font-weight:700; }
.band { border-radius:11px; padding:10px 13px 12px; }
.bh { font-size:12px; font-weight:800; letter-spacing:.4px; margin-bottom:8px; }
.row { display:flex; gap:9px; }
.bx { flex:1; background:#fff; border-radius:8px; padding:7px 9px; text-align:center; position:relative; }
.bx .n { font-size:10.5px; font-weight:800; opacity:.7; }
.bx .t { font-size:12.5px; font-weight:700; margin-top:1px; line-height:1.22; }
.bx .d { font-size:10px; color:#667085; margin-top:3px; line-height:1.3; }
.bx .s { position:absolute; top:5px; right:6px; font-size:10px; }
.arrow { display:flex; align-items:center; justify-content:center; gap:9px; margin:8px 0 2px; }
.arrow .ln { flex:1; height:0; border-top:2px dashed #98a2b3; }
.arrow .lb { font-size:11.5px; color:#344054; background:#f2f4f7; padding:3px 12px;
             border-radius:12px; font-weight:600; white-space:nowrap; }
.tri { width:0; height:0; border-left:7px solid transparent; border-right:7px solid transparent;
       border-top:9px solid #98a2b3; margin:0 auto 7px; }
.cols { display:flex; gap:10px; }
.cols > div { flex:1; }
.wm { margin-top:13px; background:#0f1729; color:#c8d0dc; font-size:11px; padding:6px 12px;
      border-radius:6px; display:flex; justify-content:space-between; }
.wm b { color:#ffd479; }
"""

GOV = ("#fffaeb", "#f79009", "#93370d")
CAT = ("#eff4ff", "#2563eb", "#1e40af")
DQ = ("#ecfdf3", "#12b76a", "#05603a")
ING = ("#f4f0ff", "#7147e8", "#4a1fb8")
SEC = ("#fef3f2", "#f04438", "#912018")
OPS = ("#f2f4f7", "#667085", "#344054")


def bx(no, title, desc, c, st, strong=False):
    return (f'<div class="bx" style="border:{"2.5px" if strong else "1.5px"} solid {c[1]}">'
            f'<div class="s">{st}</div>'
            f'<div class="n" style="color:{c[2]}">{no}</div>'
            f'<div class="t" style="color:{c[2]}">{title}</div>'
            f'<div class="d">{desc}</div></div>')


def band(title, c, boxes, strong=False):
    return (f'<div class="band" style="background:{c[0]};border:{"2.5px" if strong else "1.5px"} '
            f'solid {c[1]}"><div class="bh" style="color:{c[2]}">{title}</div>'
            f'<div class="row">{boxes}</div></div>')


def arrow(label):
    return (f'<div class="arrow"><div class="ln"></div><div class="lb">{label}</div>'
            f'<div class="ln"></div></div><div class="tri"></div>')


def overview():
    gov = band("② GOVERNANCE — TỪ VỰNG &amp; QUY ƯỚC DÙNG CHUNG", GOV,
               bx("2.1", "Business Glossary", "data-glossary — đã có CDE,<br>steward, duyệt, phân cấp",
                  GOV, "🔵") +
               bx("2.2", "Classification", "tagIds mức cột đã có<br>PD_BASIC · PD_SENSITIVE · DATA_GENERAL",
                  GOV, "🔵"))

    cat = band("① DATA CATALOG — NGUỒN SỰ THẬT DUY NHẤT", CAT,
               bx("1.1", "Bảng dữ liệu", "table-management + gộp data-dictionary<br>"
                                         "<b>6 tab: Tổng quan · Cột · Chất lượng<br>"
                                         "<u>Nguồn gốc</u> · Quyền · Lịch sử</b>", CAT, "🔵🟣", True) +
               bx("1.2", "Nhóm bảng", "table-monitor", CAT, "🟢") +
               bx("1.3", "Domain", "domain-management", CAT, "🟢") +
               bx("1.4", "Danh mục tham chiếu", "channel-indexing-management<br>"
                                                "đã có duyệt + phiên bản", CAT, "🟢"),
               strong=True)

    dq = band("③ DATA QUALITY — phần chạy đã hỏng, làm lại theo thiết kế DQ Tool", DQ,
              bx("3.1", "Rule Library", "28 loại kiểm tra", DQ, "🔴") +
              bx("3.2", "Luật &amp; Kết quả", "gán luật · chấm điểm", DQ, "🔴") +
              bx("3.3", "Profiling", "đo chỉ số cột", DQ, "🔴") +
              bx("3.4", "Incidents", "sự cố có vòng đời", DQ, "🔴") +
              bx("3.5", "Alerts", "warning-history · telegram<br>notify-manager", DQ, "🟢"))

    ing = band("④ INGESTION &amp; ORCHESTRATION", ING,
               bx("4.1", "Luồng xử lý", "job-management — đã có<br>duyệt, phiên bản, khoá phiên",
                  ING, "🔵") +
               bx("4.2", "Cửa nạp dữ liệu", "gộp 6 màn nạp<br>+ cổng chặn dữ liệu xấu", ING, "🟣") +
               bx("4.3", "Theo dõi &amp; Giám sát pipeline", "task-management + sơ đồ job→bảng<br>phủ badge chất lượng", ING, "🔵"))

    sec = band("⑤ DATA SECURITY", SEC,
               bx("5.1", "Người dùng &amp; Nhóm", "user · group · acl", SEC, "🟢") +
               bx("5.2", "Chính sách truy cập", "gộp 4 màn quyền<br><b>+ tab Che dữ liệu (mới)</b>",
                  SEC, "🔵", True) +
               bx("5.3", "Yêu cầu cấp quyền", "xin → duyệt → có hạn", SEC, "🔴") +
               bx("5.4", "Nhật ký kiểm toán", "history-data + lịch sử<br>truy vấn", SEC, "🔵") +
               bx("5.5", "Báo cáo quyền", "một người có quyền gì", SEC, "🔴"))

    ops = band("⑥ OPERATIONS", OPS,
               bx("6.1", "Sức khoẻ dữ liệu", "bảng điều khiển cho lãnh đạo + độ phủ quản trị",
                  OPS, "🔴") +
               bx("6.2", "Cấu hình hệ thống", "configuration · connection · chuẩn đặt tên · định nghĩa Tier",
                  OPS, "🟢"))

    body = (gov + arrow("từ vựng và nhãn dùng chung — khai một lần, mọi bảng dùng lại") +
            cat +
            arrow("mọi module bên dưới tham chiếu MÃ BẢNG và MÃ CỘT từ Data Catalog") +
            f'<div class="cols"><div>{dq}</div></div>'
            '<div style="height:9px"></div>'
            f'<div class="cols"><div>{ing}</div><div>{sec}</div></div>' +
            arrow("kết quả từ ③ ④ ⑤ đổ về báo cáo") + ops)

    legend = ('<div class="lg">'
              '<span><b>🟢 Giữ nguyên</b> — 6 menu</span>'
              '<span><b>🔵 Nâng cấp cái đã có</b> — 7 menu</span>'
              '<span><b>🟣 Gộp cái đang rải rác</b> — 1 menu</span>'
              '<span><b>🔴 Xây mới</b> — 7 menu</span>'
              '<span style="color:#667085">→ <b>14/21 menu (67%) là kế thừa</b></span></div>')

    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>'
            f'<div class="tt">Mô hình tổng quan DMP — 6 module cha, 21 menu con</div>'
            f'<div class="st">Trạng thái từng menu lấy từ kết quả kiểm kê mã nguồn SQLWF, '
            f'không phải suy đoán.</div>{legend}{body}'
            f'<div class="wm"><span>DMP · Mô hình tổng quan (bản chốt sau kiểm kê)</span>'
            f'<span><b>Số hiệu menu</b> khớp với bảng phân rã chức năng ở mục 4</span></div>'
            f'</body></html>')


SCREENS = {"diag-03-mo-hinh-dmp": overview}
