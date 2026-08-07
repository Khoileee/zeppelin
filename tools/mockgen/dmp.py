# -*- coding: utf-8 -*-
"""Bộ giao diện thống nhất cho tool đề xuất: DMP — Nền tảng Quản trị Dữ liệu."""

NAVY = "#16233F"
NAVY2 = "#1E2E4F"
AC = "#2563EB"
AC2 = "#0EA5A5"

CSS = """
* { box-sizing:border-box; margin:0; padding:0; }
body { font-family:"Segoe UI",Roboto,Arial,sans-serif; background:#eef1f6; }
.win { width:1560px; background:#fff; }
.chrome { height:32px; background:#dee3ea; display:flex; align-items:center; padding:0 11px; gap:7px;
          border-bottom:1px solid #c6ccd6; }
.dot { width:10px; height:10px; border-radius:50%; }
.url { flex:1; background:#fff; border-radius:12px; height:21px; display:flex; align-items:center;
       padding:0 11px; font-size:11px; color:#5a6472; margin-left:9px; }
.body { display:flex; min-height:__H__px; }
/* ------- sidebar ------- */
.side { width:236px; background:__NAVY__; flex-shrink:0; padding-bottom:14px; }
.logo { display:flex; align-items:center; gap:9px; padding:15px 16px 13px; color:#fff;
        border-bottom:1px solid #2b3a5c; }
.logo .mk { width:30px; height:30px; border-radius:8px; background:__AC__; display:flex;
            align-items:center; justify-content:center; font-weight:800; font-size:14px; }
.logo b { font-size:15px; letter-spacing:.2px; }
.logo span { display:block; font-size:10px; color:#8fa3c8; font-weight:400; }
.grp { color:#6d81a8; font-size:10px; font-weight:700; letter-spacing:.7px; padding:13px 16px 5px; }
.side a { display:flex; align-items:center; gap:9px; padding:7px 16px; color:#c3cee2; font-size:12.5px;
          text-decoration:none; }
.side a.on { background:__AC__; color:#fff; font-weight:600; }
.side a.sub { padding-left:38px; font-size:12px; color:#9db0d1; }
.side a.sub.on { background:#2b3a5c; color:#fff; border-left:3px solid __AC2__; padding-left:35px; }
/* ------- main ------- */
.main { flex:1; padding:0; overflow:hidden; background:#f7f9fc; }
.hd { background:#fff; border-bottom:1px solid #e3e8ef; padding:13px 24px; }
.crumb { font-size:11.5px; color:#8b95a7; margin-bottom:4px; }
.hd h1 { font-size:19px; font-weight:700; color:#101828; display:flex; align-items:center; gap:9px; }
.hd .desc { font-size:12.5px; color:#667085; margin-top:3px; }
.wrap { padding:18px 24px; }
.tabs { display:flex; gap:24px; margin-top:11px; }
.tabs div { font-size:13px; color:#667085; padding-bottom:8px; }
.tabs div.on { color:__AC__; font-weight:700; border-bottom:2px solid __AC__; }
/* ------- thành phần ------- */
.card { background:#fff; border:1px solid #e3e8ef; border-radius:9px; }
.kpi { flex:1; padding:12px 15px; }
.kpi .lb { font-size:10.5px; color:#8b95a7; font-weight:600; letter-spacing:.3px; }
.kpi .vl { font-size:23px; font-weight:800; color:#101828; margin-top:2px; }
.kpi .sb { font-size:11px; color:#8b95a7; }
table.g { width:100%; border-collapse:collapse; font-size:12.5px; }
table.g th { background:#f8fafc; text-align:left; padding:9px 11px; font-size:11px; font-weight:700;
             color:#5b6779; letter-spacing:.3px; border-bottom:1px solid #e3e8ef; text-transform:uppercase; }
table.g td { padding:9px 11px; border-bottom:1px solid #eef1f6; vertical-align:middle; color:#344054; }
table.g tr:hover td { background:#f9fbff; }
.chip { display:inline-flex; align-items:center; gap:4px; font-size:10.5px; padding:2px 8px;
        border-radius:11px; font-weight:600; }
.btn { display:inline-flex; align-items:center; gap:6px; font-size:12.5px; font-weight:600;
       padding:7px 13px; border-radius:7px; background:__AC__; color:#fff; }
.btn.w { background:#fff; color:#475467; border:1px solid #d0d7e2; font-weight:500; }
.btn.sm { padding:4px 9px; font-size:11.5px; }
.ico { display:inline-flex; align-items:center; justify-content:center; width:24px; height:23px;
       border-radius:5px; font-size:11px; margin-right:3px; border:1px solid #d0d7e2; color:#5b6779; }
.mono { font-family:Consolas,"Courier New",monospace; }
.muted { color:#8b95a7; }
.req { color:#d92d20; }
.fld { margin-bottom:13px; }
.fld .lb { font-size:12px; font-weight:600; color:#344054; margin-bottom:5px; }
.fld .in { border:1px solid #d0d7e2; border-radius:7px; padding:8px 11px; font-size:12.5px;
           background:#fff; min-height:34px; color:#101828; }
.fld .in.ro { background:#f5f7fa; color:#8b95a7; }
.fld .hp { font-size:11px; color:#8b95a7; margin-top:4px; }
.sec { font-size:12.5px; font-weight:700; color:__AC__; letter-spacing:.3px; padding-bottom:6px;
       border-bottom:2px solid __AC__; display:inline-block; margin:4px 0 13px; }
.note { border-radius:8px; padding:11px 14px; font-size:12.5px; line-height:1.65; }
.wm { background:#0f1729; color:#c8d0dc; font-size:11px; padding:7px 14px;
      display:flex; justify-content:space-between; }
.wm b { color:#ffd479; }
"""

MENU = [
    ("grp", "① DATA CATALOG", None),
    ("a", "🗂️ Bảng dữ liệu", "m11"),
    ("a", "📦 Nhóm bảng", "m12"),
    ("a", "🧩 Miền dữ liệu", "m13"),
    ("a", "📚 Danh mục tham chiếu", "m14"),
    ("grp", "② GOVERNANCE", None),
    ("a", "📖 Từ điển nghiệp vụ", "m21"),
    ("a", "🏷️ Phân loại & Nhãn", "m22"),
    ("grp", "③ DATA QUALITY", None),
    ("a", "📐 Thư viện luật", "m31"),
    ("a", "🎯 Luật & Kết quả", "m32"),
    ("a", "🔬 Phân tích dữ liệu", "m33"),
    ("a", "🚨 Sự cố chất lượng", "m34"),
    ("a", "🔔 Cảnh báo", "m35"),
    ("grp", "④ INGESTION & ORCHESTRATION", None),
    ("a", "⚙️ Luồng xử lý (Job)", "m41"),
    ("a", "📥 Cửa nạp dữ liệu", "m42"),
    ("a", "🖥️ Theo dõi & Pipeline", "m43"),
    ("grp", "⑤ DATA SECURITY", None),
    ("a", "👥 Người dùng & Nhóm", "m51"),
    ("a", "🔐 Chính sách truy cập", "m52"),
    ("a", "✋ Yêu cầu cấp quyền", "m53"),
    ("a", "📜 Nhật ký kiểm toán", "m54"),
    ("a", "📋 Báo cáo quyền", "m55"),
    ("grp", "⑥ OPERATIONS", None),
    ("a", "❤️ Sức khoẻ dữ liệu", "m61"),
    ("a", "⚙️ Cấu hình hệ thống", "m62"),
]


def side(active):
    out = ['<div class="logo"><span class="mk">D</span><div><b>DMP</b>'
           '<span>Nền tảng Quản trị Dữ liệu</span></div></div>']
    for kind, label, key in MENU:
        if kind == "grp":
            out.append(f'<div class="grp">{label}</div>')
        else:
            out.append(f'<a class="{"on" if key == active else ""}">{label}</a>')
    return "".join(out)


def shell(url, crumb, title, desc, body, note, active, tabs=None, height=980, actions=""):
    tabs_html = ""
    if tabs:
        tabs_html = '<div class="tabs">' + "".join(
            f'<div class="{"on" if t == tabs[0] else ""}">{t}</div>' for t in tabs[1]) + "</div>"
    css = CSS.replace("__NAVY__", NAVY).replace("__AC__", AC).replace("__AC2__", AC2) \
             .replace("__H__", str(height))
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>
<div class="win">
  <div class="chrome"><div class="dot" style="background:#ff5f57"></div>
    <div class="dot" style="background:#febc2e"></div>
    <div class="dot" style="background:#28c840"></div><div class="url">🔒 {url}</div></div>
  <div class="body">
    <div class="side">{side(active)}</div>
    <div class="main">
      <div class="hd"><div class="crumb">{crumb}</div>
        <div style="display:flex;justify-content:space-between;align-items:flex-start">
          <div><h1>{title}</h1><div class="desc">{desc}</div></div>
          <div style="display:flex;gap:8px">{actions}</div></div>
        {tabs_html}</div>
      <div class="wrap">{body}</div>
    </div>
  </div>
  <div class="wm"><span>{note}</span>
    <span><b>Ảnh MINH HOẠ ĐỀ XUẤT</b> — màn hình chưa tồn tại, dựng để mô tả tính năng</span></div>
</div></body></html>"""


def fld(label, value, req=False, hint="", ro=False, mono=False):
    return (f'<div class="fld"><div class="lb">{"<span class=req>*</span> " if req else ""}{label}</div>'
            f'<div class="in{" ro" if ro else ""}"{" style=font-family:Consolas,monospace" if mono else ""}>'
            f'{value}</div>{f"<div class=hp>{hint}</div>" if hint else ""}</div>')


def chip(text, kind="b"):
    c = {"b": ("#EFF4FF", "#2563EB"), "g": ("#ECFDF3", "#067647"), "r": ("#FEF3F2", "#B42318"),
         "o": ("#FFFAEB", "#B54708"), "n": ("#F2F4F7", "#475467"), "t": ("#E6FAF8", "#0E7C7B")}[kind]
    return f'<span class="chip" style="background:{c[0]};color:{c[1]}">{text}</span>'
