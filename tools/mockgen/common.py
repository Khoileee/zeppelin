# -*- coding: utf-8 -*-
"""Khung dựng ảnh màn hình mô phỏng các tool Data Management trên thị trường."""

BASE_CSS = """
* { box-sizing: border-box; margin:0; padding:0; }
body { font-family: "Segoe UI", Roboto, Arial, sans-serif; background:#e8ebf0; }
.win { width:1440px; background:#fff; }
/* thanh trình duyệt */
.bar { height:38px; background:#dee3ea; display:flex; align-items:center; padding:0 12px; gap:8px;
       border-bottom:1px solid #c6ccd6; }
.dot { width:11px; height:11px; border-radius:50%; }
.url { flex:1; background:#fff; border-radius:14px; height:24px; display:flex; align-items:center;
       padding:0 12px; font-size:12px; color:#5a6472; margin-left:10px; }
.body { display:flex; min-height:930px; }
/* nav trái */
.nav { width:196px; padding:14px 0; flex-shrink:0; }
.logo { display:flex; align-items:center; gap:8px; padding:0 16px 16px; font-weight:700; font-size:15px; }
.logo .mark { width:24px; height:24px; border-radius:6px; display:flex; align-items:center;
              justify-content:center; color:#fff; font-size:13px; font-weight:800; }
.nav a { display:flex; align-items:center; gap:9px; padding:8px 16px; font-size:13px; text-decoration:none; }
.nav a.on { font-weight:700; }
/* nội dung */
.main { flex:1; padding:20px 26px; overflow:hidden; }
.crumb { font-size:12px; color:#7b8494; margin-bottom:6px; }
h1.t { font-size:21px; font-weight:700; margin-bottom:4px; display:flex; align-items:center; gap:10px; }
.sub { font-size:12.5px; color:#6b7484; margin-bottom:14px; }
.chip { display:inline-flex; align-items:center; gap:5px; font-size:11px; padding:2px 9px;
        border-radius:11px; font-weight:600; }
.tabs { display:flex; gap:2px; border-bottom:1px solid #e2e6ec; margin:14px 0 0; }
.tabs div { padding:9px 15px; font-size:13px; color:#6b7484; cursor:pointer; }
.tabs div.on { font-weight:700; border-bottom:2px solid; }
table.g { width:100%; border-collapse:collapse; font-size:12.5px; }
table.g th { text-align:left; padding:9px 10px; background:#f6f8fa; color:#5a6472; font-weight:600;
             font-size:11.5px; text-transform:uppercase; letter-spacing:.3px; border-bottom:1px solid #e2e6ec; }
table.g td { padding:9px 10px; border-bottom:1px solid #eef1f5; vertical-align:top; }
.mono { font-family: Consolas, "Courier New", monospace; }
.muted { color:#8b94a3; }
.card { border:1px solid #e2e6ec; border-radius:8px; background:#fff; }
.btn { display:inline-flex; align-items:center; gap:6px; font-size:12.5px; font-weight:600;
       padding:7px 14px; border-radius:6px; color:#fff; }
.btn.ghost { background:#fff; border:1px solid #cfd6e0; color:#48505e; }
/* dải chú thích cuối ảnh */
.wm { background:#1f2937; color:#c8d0dc; font-size:11.5px; padding:7px 14px;
      display:flex; justify-content:space-between; letter-spacing:.2px; }
.wm b { color:#ffd479; }
"""


WM_RIGHT_DEFAULT = ("<b>Ảnh DỰNG LẠI</b> theo tài liệu chính thức của sản phẩm "
                    "— không phải ảnh chụp màn hình thật")


def shell(title, url, nav_html, main_html, accent, brandbg="#fff", extra_css="", note="",
          note_right=None):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}
.nav {{ background:{brandbg}; }}
.tabs div.on {{ color:{accent}; border-color:{accent}; }}
.btn {{ background:{accent}; }}
{extra_css}</style></head><body>
<div class="win">
  <div class="bar">
    <div class="dot" style="background:#ff5f57"></div>
    <div class="dot" style="background:#febc2e"></div>
    <div class="dot" style="background:#28c840"></div>
    <div class="url">🔒 {url}</div>
  </div>
  <div class="body">
    <div class="nav">{nav_html}</div>
    <div class="main">{main_html}</div>
  </div>
  <div class="wm"><span>{note}</span>
    <span>{note_right or WM_RIGHT_DEFAULT}</span></div>
</div></body></html>"""


def nav(brand, mark_bg, items, accent, textcol="#48505e"):
    """items: list of (icon, label, is_active)"""
    rows = "".join(
        f'<a class="{"on" if on else ""}" style="color:{accent if on else textcol};'
        f'{"background:" + accent + "14;border-right:3px solid " + accent + ";" if on else ""}">'
        f'<span style="width:16px">{ic}</span>{lb}</a>'
        for ic, lb, on in items)
    return (f'<div class="logo"><span class="mark" style="background:{mark_bg}">'
            f'{brand[0]}</span>{brand}</div>{rows}')
