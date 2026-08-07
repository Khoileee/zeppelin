# -*- coding: utf-8 -*-
"""Apache Ranger — dựng lại theo đúng bố cục giao diện thật (thanh xanh ngang trên cùng,
tab Access / Masking / Row Level Filter trong trang policy của service)."""

GREEN = "#6DA544"
GREEN_D = "#5C8F38"
BTN = "#7CB342"

CSS = """
* { box-sizing:border-box; margin:0; padding:0; }
body { font-family:"Segoe UI","Open Sans",Arial,sans-serif; background:#f2f2f2; }
.win { width:1440px; background:#fff; }
.chrome { height:34px; background:#dee3ea; display:flex; align-items:center; padding:0 12px; gap:7px;
          border-bottom:1px solid #c6ccd6; }
.dot { width:10px; height:10px; border-radius:50%; }
.url { flex:1; background:#fff; border-radius:13px; height:22px; display:flex; align-items:center;
       padding:0 11px; font-size:11.5px; color:#5a6472; margin-left:9px; }
/* thanh xanh của Ranger */
.top { height:42px; background:%(G)s; display:flex; align-items:center; padding:0 14px; }
.brand { font-size:20px; font-weight:800; color:#fff; letter-spacing:.3px; margin-right:22px;
         font-style:italic; }
.top a { color:#fff; font-size:12.5px; padding:0 13px; height:42px; display:flex; align-items:center;
         gap:6px; text-decoration:none; }
.top a.on { background:%(GD)s; font-weight:600; }
.spacer { flex:1; }
.crumb { background:#fafafa; border-bottom:1px solid #e0e0e0; padding:7px 18px; font-size:11.5px;
         color:#666; }
.crumb b { color:#333; }
.page { padding:14px 18px; min-height:%(H)spx; }
.ptitle { font-size:15px; font-weight:600; color:#444; margin-bottom:10px; }
.tabs { display:flex; border-bottom:2px solid %(G)s; margin-bottom:12px; }
.tabs div { padding:7px 20px; font-size:12.5px; color:#555; border:1px solid #ddd;
            border-bottom:none; background:#f7f7f7; margin-right:2px; }
.tabs div.on { background:%(G)s; color:#fff; font-weight:600; border-color:%(G)s; }
.btn { display:inline-flex; align-items:center; gap:5px; font-size:12px; font-weight:600;
       padding:5px 12px; border-radius:3px; background:%(B)s; color:#fff; }
.btn.w { background:#fff; color:#555; border:1px solid #ccc; font-weight:400; }
.btn.sm { padding:3px 8px; font-size:11px; }
table.g { width:100%; border-collapse:collapse; font-size:11.5px; border:1px solid #ddd; }
table.g th { background:#f5f5f5; text-align:left; padding:7px 9px; font-weight:600; color:#555;
             border:1px solid #ddd; font-size:11px; }
table.g td { padding:6px 9px; border:1px solid #e8e8e8; vertical-align:middle; color:#444; }
.badge { display:inline-block; font-size:10.5px; padding:1px 8px; border-radius:2px;
         background:#8BC34A; color:#fff; font-weight:600; }
.badge.g2 { background:#4CAF50; }
.badge.b { background:#5bc0de; }
.badge.o { background:#f0ad4e; }
.ico { display:inline-flex; align-items:center; justify-content:center; width:20px; height:19px;
       border-radius:3px; color:#fff; font-size:10px; margin-right:3px; }
.ico.e { background:#5bc0de; } .ico.d { background:#d9534f; } .ico.a { background:#8BC34A; }
.sec { font-size:13px; color:#333; font-weight:600; border-bottom:1px solid #ddd;
       padding-bottom:5px; margin:16px 0 11px; }
.sec.warn { color:#8a6d3b; border-color:#faebcc; }
.fr { display:flex; align-items:center; margin-bottom:9px; }
.fl { width:130px; font-size:12px; color:#333; text-align:left; }
.fl i { color:#d9534f; font-style:normal; }
.fi { width:290px; border:1px solid #ccc; border-radius:3px; padding:5px 9px; font-size:12px;
      background:#fff; min-height:28px; color:#333; }
.fi.wide { width:520px; }
.tog { display:inline-flex; margin-left:9px; }
.tog span { font-size:10.5px; padding:3px 10px; border:1px solid #ccc; }
.tog span.on { background:%(B)s; color:#fff; border-color:%(B)s; }
.mono { font-family:Consolas,"Courier New",monospace; }
.mini { font-size:11px; color:#888; margin-left:9px; }
.wm { background:#1f2937; color:#c8d0dc; font-size:11px; padding:6px 13px;
      display:flex; justify-content:space-between; }
.wm b { color:#ffd479; }
""".replace("%(G)s", GREEN).replace("%(GD)s", GREEN_D).replace("%(B)s", BTN).replace("%(H)s", "560")


def rshell(url, crumb, page, note, note_right=None, active="access"):
    nav = "".join(
        f'<a class="{"on" if k == active else ""}">{ic} {lb}</a>'
        for k, ic, lb in [("access", "☰", "Access Manager ▾"), ("audit", "🕐", "Audit"),
                          ("zone", "🛡", "Security Zone"), ("set", "⚙", "Settings ▾")])
    right = ('<div class="spacer"></div>'
             '<a style="font-size:12px">👤 admin</a>')
    default_right = ("<b>Ảnh DỰNG LẠI</b> theo giao diện thật của Apache Ranger "
                     "— không phải ảnh chụp màn hình")
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="win">
  <div class="chrome"><div class="dot" style="background:#ff5f57"></div>
    <div class="dot" style="background:#febc2e"></div>
    <div class="dot" style="background:#28c840"></div><div class="url">🔒 {url}</div></div>
  <div class="top"><span class="brand">Ranger</span>{nav}{right}</div>
  <div class="crumb">{crumb}</div>
  <div class="page">{page}</div>
  <div class="wm"><span>{note}</span><span>{note_right or default_right}</span></div>
</div></body></html>"""


def _tabs(active):
    return '<div class="tabs">' + "".join(
        f'<div class="{"on" if n == active else ""}">{n}</div>'
        for n in ["Access", "Masking", "Row Level Filter"]) + "</div>"


def _field(label, value, req=False, toggles=None, wide=False, note=""):
    star = ' <i>*</i>' if req else ""
    tg = ""
    if toggles:
        tg = '<span class="tog">' + "".join(
            f'<span class="{"on" if on else ""}">{t}</span>' for t, on in toggles) + "</span>"
    return (f'<div class="fr"><div class="fl">{label}{star}</div>'
            f'<div class="fi{" wide" if wide else ""}">{value}</div>{tg}'
            f'{f"<span class=mini>{note}</span>" if note else ""}</div>')


def _cond_table(headers, rows, title, warn=False):
    th = "".join(f"<th>{h}</th>" for h in headers)
    tr = ""
    for r in rows:
        tr += "<tr>" + "".join(f"<td>{c}</td>" for c in r) + \
              '<td style="width:80px"><span class="ico d">✕</span>' \
              '<span class="ico a">+</span></td></tr>'
    return (f'<div class="sec{" warn" if warn else ""}">'
            f'{"⚠️ " if warn else ""}{title}</div>'
            f'<table class="g"><tr>{th}<th style="width:80px"></th></tr>{tr}</table>')


SEL = '<span style="color:#aaa">Select Group</span>'
SEU = '<span style="color:#aaa">Select User</span>'
PERM = '<span style="color:#d9534f;font-size:11px">Add Permissions +</span>'


# ============================================================ 1. Masking
def mask():
    rows = [
        ('<span class="badge b">ban_kinh_doanh ✕</span>', SEU,
         '<span class="badge b">select ✕</span>',
         '<span class="badge o">Partial mask: show last 4 ✕</span>'),
        ('<span class="badge b">ctv_thue_ngoai ✕</span>', SEU,
         '<span class="badge b">select ✕</span>',
         '<span class="badge o">Hash ✕</span>'),
    ]
    page = (_tabs("Masking") +
            '<div class="ptitle">Create Policy</div>' +
            '<div class="sec">Policy Details :</div>' +
            '<div style="display:flex"><div style="flex:1">' +
            _field("Policy Type", '<span class="badge g2">Masking</span>') +
            _field("Policy Name", "Che so dien thoai - doi soat doi tac A", True,
                   [("enabled", True), ("normal", True)]) +
            _field("Policy Label", '<span style="color:#aaa">Policy Label</span>') +
            _field("Hive Database", '<span class="badge b">bi ✕</span>', True,
                   [("include", True)]) +
            _field("Hive Table", '<span class="badge b">doi_soat_giao_dich_A ✕</span>', True,
                   [("include", True)]) +
            _field("Hive Column", '<span class="badge b">so_dien_thoai ✕</span>', True,
                   note="chỉ chọn được MỘT cột cho mỗi chính sách masking") +
            _field("Description", "", wide=False) +
            _field("Audit Logging", '<span class="tog"><span class="on">YES</span></span>') +
            '</div><div style="width:170px;text-align:right">'
            '<span class="btn">＋ Add Validity Period</span></div></div>' +
            _cond_table(["Select Group", "Select User", "Access Types", "Select Masking Option"],
                        rows, "Mask Conditions :") +
            '<div style="margin-top:16px"><span class="btn">Add</span> '
            '<span class="btn w" style="margin-left:7px">Cancel</span></div>')
    return rshell("ranger-admin:6080/index.html#!/service/1/policies/create",
                  'Service Manager &nbsp;›&nbsp; <b>jumanji_hive</b> Policies &nbsp;›&nbsp; Create Policy',
                  page, "Apache Ranger · TAB MASKING — form tạo chính sách che dữ liệu theo cột")


# ============================================================ 2. Row level filter
def row_filter():
    rows = [
        ('<span class="badge b">kd_mien_bac ✕</span>', SEU,
         '<span class="badge b">select ✕</span>',
         '<span class="mono" style="font-size:11px">khu_vuc IN (\'HN\',\'HP\',\'QN\')</span>'),
        ('<span class="badge b">ctv_thue_ngoai ✕</span>', SEU,
         '<span class="badge b">select ✕</span>',
         '<span class="mono" style="font-size:11px">ngay_ghi_nhan &gt;= CURRENT_DATE - 7</span>'),
    ]
    page = (_tabs("Row Level Filter") +
            '<div class="ptitle">Create Policy</div>' +
            '<div class="sec">Policy Details :</div>' +
            '<div style="display:flex"><div style="flex:1">' +
            _field("Policy Type", '<span class="badge g2">Row Level Filter</span>') +
            _field("Policy Name", "Loc giao dich theo khu vuc phu trach", True,
                   [("enabled", True), ("normal", True)]) +
            _field("Policy Label", '<span style="color:#aaa">Policy Label</span>') +
            _field("Hive Database", '<span class="badge b">bi ✕</span>', True,
                   [("include", True)]) +
            _field("Hive Table", '<span class="badge b">doi_soat_giao_dich_A ✕</span>', True,
                   note="Row Level Filter chỉ tới mức BẢNG, không có ô chọn cột") +
            _field("Description", "") +
            _field("Audit Logging", '<span class="tog"><span class="on">YES</span></span>') +
            '</div><div style="width:170px;text-align:right">'
            '<span class="btn">＋ Add Validity Period</span></div></div>' +
            _cond_table(["Select Group", "Select User", "Access Types", "Row Level Filter"],
                        rows, "Row Filter Conditions :") +
            '<div style="margin-top:16px"><span class="btn">Add</span> '
            '<span class="btn w" style="margin-left:7px">Cancel</span></div>')
    return rshell("ranger-admin:6080/index.html#!/service/1/policies/create",
                  'Service Manager &nbsp;›&nbsp; <b>jumanji_hive</b> Policies &nbsp;›&nbsp; Create Policy',
                  page, "Apache Ranger · TAB ROW LEVEL FILTER — form tạo chính sách lọc theo dòng")


# ============================================================ 3. Danh sách policy
def policy_list():
    rows = [
        ("26", "all - hiveservice", "--", "", ""),
        ("27", "all - global", "--", "", ""),
        ("28", "all - url", "--", "", ""),
        ("24", "all - database, table, column", "--", "public", ""),
        ("25", "all - database, udf", "--", "public", ""),
        ("31", "jmxcache portal hive rights", "--", "public", "jumanji"),
    ]
    tr = ""
    for pid, name, lbl, grp, usr in rows:
        tr += (f'<tr><td>{pid}</td><td>{name}</td><td>{lbl}</td>'
               f'<td><span class="badge">Enabled</span></td>'
               f'<td><span class="badge">Enabled</span></td>'
               f'<td>{f"<span class=badge-b style=background:#5bc0de;color:#fff;padding:1px 7px;border-radius:2px;font-size:10.5px>{grp}</span>" if grp else ""}</td>'
               f'<td>{f"<span style=background:#f0ad4e;color:#fff;padding:1px 7px;border-radius:2px;font-size:10.5px>{usr}</span>" if usr else ""}</td>'
               f'<td><span class="ico e">✎</span><span class="ico d">🗑</span></td></tr>')
    page = (_tabs("Access") +
            '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:9px">'
            '<div class="ptitle" style="margin:0">List of Policies : jumanji_hive</div>'
            '<span class="btn">Add New Policy</span></div>'
            '<div style="border:1px solid #ccc;border-radius:3px;padding:6px 11px;font-size:12px;'
            'color:#aaa;margin-bottom:10px">🔍 Search for your policy...</div>'
            '<table class="g"><tr><th>Policy ID</th><th>Policy Name</th><th>Policy Labels</th>'
            '<th>Status</th><th>Audit Logging</th><th>Groups</th><th>Users</th><th>Action</th></tr>'
            + tr + "</table>")
    return rshell("ranger-admin:6080/index.html#!/service/1/policies/Access",
                  'Service Manager &nbsp;›&nbsp; <b>jumanji_hive</b> Policies',
                  page, "Apache Ranger · DANH SÁCH CHÍNH SÁCH của một service, 3 tab tách riêng")


# ============================================================ 4. Audit
def audit():
    rows = [
        ("131", "12", "03/01/2026 10:44:36 AM", "hdfs", "jumanji", "jumanji_hdfs", "/data/bi/doi_soat",
         "READ", "Allowed", "hadoop-acl", "10.21.2.108"),
        ("131", "12", "03/01/2026 10:44:36 AM", "hdfs", "jumanji", "jumanji_hdfs", "/data/bi/doi_soat",
         "READ", "Allowed", "hadoop-acl", "10.21.2.108"),
        ("--", "--", "03/01/2026 10:41:02 AM", "hiveServer2", "ctv_nam", "jumanji_hive",
         "bi/doi_soat_giao_dich_A/so_dien_thoai", "SELECT", "Denied", "ranger-acl", "10.21.2.77"),
        ("131", "12", "03/01/2026 10:38:55 AM", "hdfs", "jumanji", "jumanji_hdfs", "/data/bi/doi_soat",
         "WRITE", "Allowed", "hadoop-acl", "10.21.2.108"),
        ("28", "3", "03/01/2026 10:35:19 AM", "hiveServer2", "phuong", "jumanji_hive",
         "bi/doi_soat_giao_dich_A", "SELECT", "Allowed", "ranger-acl", "10.21.2.51"),
    ]
    tr = ""
    for pid, pv, t, app, user, svc, res, at, rs, enf, ip in rows:
        col = "#4CAF50" if rs == "Allowed" else "#d9534f"
        tr += (f'<tr><td>{pid}</td><td>{pv}</td><td>{t}</td><td>{app}</td><td>{user}</td>'
               f'<td>{svc}</td><td class="mono" style="font-size:10.5px">{res}</td><td>{at}</td>'
               f'<td><span class="badge" style="background:{col}">{rs}</span></td>'
               f'<td>{enf}</td><td>{ip}</td><td>1</td></tr>')
    tabs = '<div class="tabs">' + "".join(
        f'<div class="{"on" if n == "Access" else ""}">{n}</div>'
        for n in ["Access", "Admin", "Login Sessions", "Plugins", "Plugin Status", "User Sync"]) + "</div>"
    page = (tabs +
            '<div style="display:flex;align-items:center;gap:10px;margin-bottom:10px">'
            '<div style="flex:1;border:1px solid #ccc;border-radius:3px;padding:6px 11px;font-size:12px">'
            '🔍 <span style="background:#eee;padding:1px 7px;border-radius:2px;font-size:11px">'
            'Start Date: 01/03/2026 ✕</span></div>'
            '<span style="font-size:11.5px;color:#666">Entries: 1 to 25 of 1000+</span></div>'
            '<table class="g"><tr><th>Policy ID</th><th>Policy Version</th><th>Event Time ▲</th>'
            '<th>Application</th><th>User</th><th>Service Name</th><th>Resource Name</th>'
            '<th>Access Type</th><th>Result</th><th>Access Enforcer</th><th>Client IP</th>'
            '<th>Event Count</th></tr>' + tr + "</table>"
            '<div style="margin-top:11px;font-size:11.5px;color:#666">'
            '☐ Exclude Service Users &nbsp;·&nbsp; mỗi dòng là một lần truy cập thật đã bị '
            'chính sách nào chặn hoặc cho qua</div>')
    return rshell("ranger-admin:6080/index.html#!/reports/audit/bigData",
                  "Audit &nbsp;›&nbsp; Access", page,
                  "Apache Ranger · NHẬT KÝ KIỂM TOÁN — ghi lại từng lần truy cập, kèm chính sách nào quyết định",
                  active="audit")


# ============================================================ 5. User access report
def report():
    rows = [
        ("18", "all - path", "--", "path:/*", "Access", "Enabled", "--"),
        ("22", "kms hdfs rights", "--", "path:/ranger/audit/hdfs/*", "Access", "Enabled", "--"),
        ("31", "jmxcache policy", "jmxcache-policy", "path:/jmxcache/*", "Access", "Enabled", "--"),
    ]
    tr = "".join(
        f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td class="mono" style="font-size:10.5px">{d}</td>'
        f'<td>{e}</td><td><span class="badge">{f}</span></td><td>{g}</td>'
        f'<td>✚</td><td>✚</td><td>✚</td><td>✚</td></tr>'
        for a, b, c, d, e, f, g in rows)
    crit = "".join(
        f'<div style="display:flex;align-items:center;margin-bottom:8px">'
        f'<div style="width:120px;font-size:12px;color:#333">{lb}</div>'
        f'<div class="fi" style="width:240px;color:#aaa">{ph}</div></div>'
        for lb, ph in [("Policy Name", "Enter Policy Name"), ("Component", "Select Component"),
                       ("Policy Label", "Select Policy Label"), ("Search By", "Group ▾ · Select Group")])
    crit2 = "".join(
        f'<div style="display:flex;align-items:center;margin-bottom:8px">'
        f'<div style="width:110px;font-size:12px;color:#333">{lb}</div>'
        f'<div class="fi" style="width:240px;color:#aaa">{ph}</div></div>'
        for lb, ph in [("Policy Type", "Access ▾"), ("Resource", "Select Resource Name"),
                       ("Zone Name", "Select Zone Name")])
    page = ('<div class="ptitle">User Access Report</div>'
            '<div class="sec">Search Criteria</div>'
            f'<div style="display:flex;gap:40px">{crit}{crit2}</div>'
            '<span class="btn">🔍 Search</span>'
            '<div class="sec" style="margin-top:18px">HDFS</div>'
            '<table class="g"><tr><th>Policy ID</th><th>Policy Name</th><th>Policy Labels</th>'
            '<th>Resources</th><th>Policy Type</th><th>Status</th><th>Zone Name</th>'
            '<th>Allow Conditions</th><th>Allow Exclude</th><th>Deny Conditions</th>'
            '<th>Deny Exclude</th></tr>' + tr + "</table>"
            '<div style="margin-top:10px;font-size:11.5px;color:#666">'
            'Kết quả gom theo từng thành phần (HDFS · HBASE · HIVE · KAFKA…) — '
            'trả lời câu hỏi "một người/nhóm đang có những quyền gì trên toàn hệ thống".</div>')
    return rshell("ranger-admin:6080/index.html#!/reports/userAccess",
                  "Access Manager &nbsp;›&nbsp; Reports", page,
                  "Apache Ranger · BÁO CÁO QUYỀN TRUY CẬP — xem toàn bộ quyền của một người/nhóm ở một chỗ")


SCREENS = {
    "rg-01-policy-list": policy_list,
    "rg-02-mask": mask,
    "rg-03-rowfilter": row_filter,
    "rg-04-audit": audit,
    "rg-05-report": report,
}


# ============================================================ 6. Tag Based Policies
def tag_policy():
    rows = [
        ("41", "PII so dien thoai - che 4 so cuoi", "--", "PII.SoDienThoai", "Masking", "ban_kinh_doanh"),
        ("42", "PII so dien thoai - bam", "--", "PII.SoDienThoai", "Masking", "ctv_thue_ngoai"),
        ("43", "PII CCCD - tra ve NULL", "--", "PII.CCCD", "Masking", "public"),
        ("44", "Tai chinh - chan truy cap", "--", "TaiChinh.DoanhThu", "Access", "ctv_thue_ngoai"),
    ]
    tr = "".join(
        f'<tr><td>{a}</td><td>{b}</td><td>{c}</td>'
        f'<td><span class="badge o">{d}</span></td><td>{e}</td>'
        f'<td><span class="badge b">{f}</span></td>'
        f'<td><span class="badge">Enabled</span></td>'
        f'<td><span class="ico e">✎</span><span class="ico d">🗑</span></td></tr>'
        for a, b, c, d, e, f in rows)
    page = ('<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:9px">'
            '<div class="ptitle" style="margin:0">List of Policies : vds_tag_service</div>'
            '<span class="btn">Add New Policy</span></div>'
            '<div style="border:1px solid #ccc;border-radius:3px;padding:6px 11px;font-size:12px;'
            'color:#aaa;margin-bottom:10px">🔍 Search for your policy...</div>'
            '<table class="g"><tr><th>Policy ID</th><th>Policy Name</th><th>Policy Labels</th>'
            '<th>TAG</th><th>Policy Type</th><th>Áp cho nhóm</th><th>Status</th><th>Action</th></tr>'
            + tr + "</table>"
            '<div style="margin-top:12px;font-size:11.5px;color:#666;background:#fcf8e3;'
            'border:1px solid #faebcc;padding:9px 12px;border-radius:3px">'
            '⚠️ <b>Ranger chỉ THỰC THI theo nhãn, không tự gắn nhãn.</b> Nhãn (TAG) phải được gắn cho '
            'cột ở một công cụ danh mục dữ liệu bên ngoài — thường là Apache Atlas — rồi đồng bộ sang '
            'Ranger qua Tag Sync. Đây chính là chỗ trụ Metadata nối vào trụ Bảo mật.</div>')
    return rshell("ranger-admin:6080/index.html#!/policymanager/tag",
                  "Access Manager &nbsp;›&nbsp; Tag Based Policies &nbsp;›&nbsp; <b>vds_tag_service</b>",
                  page, "Apache Ranger · CHÍNH SÁCH THEO NHÃN — khai một lần, áp cho mọi bảng có nhãn đó")


SCREENS["rg-06-tagpolicy"] = tag_policy
