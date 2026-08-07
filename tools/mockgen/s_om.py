# -*- coding: utf-8 -*-
"""Màn hình OpenMetadata."""
from common import shell, nav

AC = "#7147E8"
NAVI = lambda act: nav("OpenMetadata", AC, [
    ("🏠", "Trang chủ", act == "home"),
    ("🔍", "Khám phá dữ liệu", act == "explore"),
    ("📊", "Chất lượng dữ liệu", act == "quality"),
    ("🔗", "Nguồn gốc dữ liệu", act == "lineage"),
    ("📖", "Từ điển nghiệp vụ", act == "glossary"),
    ("🏷️", "Phân loại / Nhãn", act == "tags"),
    ("🧩", "Miền dữ liệu", act == "domain"),
    ("💡", "Thông tin chi tiết", act == "insight"),
    ("⚙️", "Cài đặt", act == "settings"),
], AC)

TAG = ('<span class="chip" style="background:{b};color:{c}">{t}</span>')


def _tabs(active):
    names = ["Cấu trúc bảng", "Hoạt động & Việc cần làm", "Dữ liệu mẫu",
             "Câu truy vấn", "Giám sát dữ liệu", "Nguồn gốc", "Thuộc tính mở rộng"]
    return '<div class="tabs">' + "".join(
        f'<div class="{"on" if n == active else ""}">{n}</div>' for n in names) + "</div>"


def _head():
    return """
<div class="crumb">Kho dữ liệu · <b>hive_prod</b> › bi › doi_soat</div>
<h1 class="t">📄 doi_soat_giao_dich_A
  <span class="chip" style="background:#FFF1D6;color:#8A5B00">🏅 Tier 1 — Dữ liệu vàng</span>
  <span class="chip" style="background:#FDE8E8;color:#B42318">🔴 Có cột nhạy cảm (PII)</span>
</h1>
<div class="sub">Bảng đối soát giao dịch với đối tác A, cập nhật hằng ngày lúc 06:00.
  &nbsp;·&nbsp; <b>BDA phụ trách:</b> Nguyễn Thị Phương &nbsp;·&nbsp; <b>DE phụ trách:</b> Trần Văn Hùng
  &nbsp;·&nbsp; <b>Miền:</b> Kinh doanh</div>
<div style="display:flex;gap:26px;margin:12px 0 2px;font-size:12.5px">
  <div><div class="muted" style="font-size:11px">ĐỘ TƯƠI</div><b style="color:#067647">🟢 4 giờ trước</b></div>
  <div><div class="muted" style="font-size:11px">SỐ DÒNG</div><b>12.480.331</b>
       <span style="color:#067647">▲ 0,8%</span></div>
  <div><div class="muted" style="font-size:11px">KẾT QUẢ TEST</div><b style="color:#B54708">5/7 Success</b></div>
  <div><div class="muted" style="font-size:11px">LƯỢT DÙNG / TUẦN</div><b>1.204</b>
       <span class="muted">· 37 người</span></div>
  <div><div class="muted" style="font-size:11px">DUNG LƯỢNG</div><b>184 GB</b></div>
</div>"""


# ---------------------------------------------------------------- 1. Explore
def explore():
    def facet(title, rows):
        r = "".join(
            f'<div style="display:flex;justify-content:space-between;padding:5px 0;font-size:12.5px">'
            f'<span><input type="checkbox" {"checked" if ck else ""}> {n}</span>'
            f'<span class="muted">{c}</span></div>' for n, c, ck in rows)
        return (f'<div style="margin-bottom:16px"><div style="font-size:11.5px;font-weight:700;'
                f'color:#5a6472;text-transform:uppercase;margin-bottom:4px">{title}</div>{r}</div>')

    def card(name, path, desc, tags, tier, score, fresh):
        return f"""
<div class="card" style="padding:13px 15px;margin-bottom:10px">
  <div style="display:flex;justify-content:space-between">
    <div style="font-size:11.5px" class="muted">hive_prod › {path}</div>
    <div style="font-size:11.5px" class="muted">{fresh}</div>
  </div>
  <div style="font-size:14.5px;font-weight:700;color:{AC};margin:3px 0 4px">📄 {name}</div>
  <div style="font-size:12.5px;color:#48505e;margin-bottom:7px">{desc}</div>
  <div style="display:flex;gap:6px;flex-wrap:wrap">{tier}{tags}</div>
</div>"""

    left = (facet("Loại tài sản", [("Bảng", "1.284", True), ("Báo cáo", "212", False),
                                   ("Luồng job", "96", False), ("Chủ đề Kafka", "18", False)]) +
            facet("Kho / Dịch vụ", [("hive_prod", "842", True), ("mongo_meta", "310", False),
                                    ("kafka_stream", "132", False)]) +
            facet("Miền dữ liệu", [("Kinh doanh", "421", True), ("Kỹ thuật", "268", False),
                                   ("Tài chính", "155", False)]) +
            facet("Mức độ quan trọng (Tier)", [("Tier 1 — Vàng", "38", True), ("Tier 2", "146", False),
                                               ("Tier 3", "660", False)]) +
            facet("Nhãn phân loại", [("PII.Nhạy cảm", "84", False), ("PII.Không nhạy cảm", "121", False),
                                     ("Tài chính.Doanh thu", "45", False)]) +
            facet("Người phụ trách", [("Nguyễn Thị Phương", "24", False), ("Trần Văn Hùng", "31", False)]))

    cards = (
        card("doi_soat_giao_dich_A", "bi › doi_soat",
             "Bảng đối soát giao dịch với đối tác A, cập nhật hằng ngày lúc 06:00.",
             '<span class="chip" style="background:#FDE8E8;color:#B42318">PII.Nhạy cảm</span>'
             '<span class="chip" style="background:#EEF2FF;color:#3538CD">Kinh doanh</span>',
             '<span class="chip" style="background:#FFF1D6;color:#8A5B00">🏅 Tier 1</span>', "88", "🟢 4 giờ trước") +
        card("thue_bao_ngay", "dwh › thue_bao",
             "Ảnh chụp trạng thái thuê bao theo ngày, nguồn cho 12 báo cáo kinh doanh.",
             '<span class="chip" style="background:#EEF2FF;color:#3538CD">Kinh doanh</span>',
             '<span class="chip" style="background:#FFF1D6;color:#8A5B00">🏅 Tier 1</span>', "94", "🟢 2 giờ trước") +
        card("doanh_thu_thang", "bi › tai_chinh",
             "Tổng hợp doanh thu theo tháng/khu vực — đầu vào cho báo cáo Ban Tổng Giám đốc.",
             '<span class="chip" style="background:#FEF3F2;color:#B42318">Tài chính.Doanh thu</span>',
             '<span class="chip" style="background:#FFF1D6;color:#8A5B00">🏅 Tier 1</span>', "76", "🟠 31 giờ trước") +
        card("log_truy_cap_raw", "raw › log",
             "Log truy cập thô, chưa làm sạch. Không khuyến nghị dùng trực tiếp cho báo cáo.",
             '<span class="chip" style="background:#F2F4F7;color:#475467">Chưa có mô tả cột</span>',
             '<span class="chip" style="background:#F2F4F7;color:#475467">Tier 3</span>', "41", "🔴 9 ngày trước"))

    main = f"""
<div style="display:flex;gap:10px;margin-bottom:14px">
  <div style="flex:1;border:1px solid #d5dae2;border-radius:8px;padding:10px 14px;font-size:13.5px">
    🔍 <b>đối soát</b><span class="muted"> — tìm theo tên bảng, tên cột, mô tả, thuật ngữ nghiệp vụ…</span></div>
  <div class="btn ghost">⚙️ Tìm kiếm nâng cao</div>
  <div class="btn ghost">↕️ Sắp xếp: Liên quan nhất</div>
</div>
<div style="display:flex;gap:22px">
  <div style="width:250px;flex-shrink:0">{left}</div>
  <div style="flex:1">
    <div style="font-size:12.5px;margin-bottom:9px" class="muted">
      <b style="color:#101828">1.284 kết quả</b> · đang lọc: Bảng · hive_prod · Kinh doanh · Tier 1</div>
    {cards}
  </div>
</div>"""
    return shell("OpenMetadata — Khám phá dữ liệu", "sandbox.open-metadata.org/explore/tables",
                 NAVI("explore"), main, AC, "#FAFAFE",
                 note="OpenMetadata · Màn KHÁM PHÁ DỮ LIỆU (Explore)")


# ---------------------------------------------------------------- 2. Table page
def table():
    cols = [
        ("giao_dich_id", "STRING", "Mã định danh giao dịch", "Khoá chính", "", ""),
        ("so_dien_thoai", "STRING", "Số thuê bao thực hiện giao dịch",
         "PII.Nhạy cảm", "Thuê bao", "🔴 2 luật lỗi"),
        ("so_tien", "STRING ⚠️", "Số tiền giao dịch (đang lưu dạng chuỗi)",
         "Tài chính.Doanh thu", "Doanh thu ghi nhận", "🟠 1 luật cảnh báo"),
        ("ngay_ghi_nhan", "DATE", "Ngày hệ thống ghi nhận giao dịch", "", "Ngày phát sinh", ""),
        ("trang_thai", "STRING", "Trạng thái đối soát: KHOP / LECH / CHO", "", "", ""),
        ("doi_tac", "STRING", "Mã đối tác", "", "Đối tác", ""),
    ]
    rows = ""
    for n, t, d, tag, term, dq in cols:
        tagh = (f'<span class="chip" style="background:#FDE8E8;color:#B42318">{tag}</span>'
                if "PII" in tag else
                f'<span class="chip" style="background:#FEF3F2;color:#B42318">{tag}</span>' if tag else
                '<span class="muted">+ Thêm nhãn</span>')
        termh = (f'<span class="chip" style="background:#F0F4FF;color:#3538CD">📖 {term}</span>'
                 if term else '<span class="muted">+ Gắn thuật ngữ</span>')
        rows += (f'<tr><td class="mono"><b>{n}</b></td><td class="mono muted">{t}</td>'
                 f'<td>{d}</td><td>{tagh}</td><td>{termh}</td><td>{dq or "🟢 Đạt"}</td></tr>')

    main = _head() + _tabs("Cấu trúc bảng") + f"""
<div style="display:flex;gap:20px;margin-top:16px">
 <div style="flex:1">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:9px">
    <div style="font-size:13.5px;font-weight:700">6 cột</div>
    <div style="display:flex;gap:8px"><span class="btn ghost">🔍 Tìm cột</span>
      <span class="btn ghost">⬇️ Xuất CSV</span></div>
  </div>
  <div class="card">
  <table class="g"><tr><th>Tên cột</th><th>Kiểu</th><th>Mô tả</th><th>Nhãn phân loại</th>
    <th>Thuật ngữ nghiệp vụ</th><th>Chất lượng</th></tr>{rows}</table></div>
 </div>
 <div style="width:270px;flex-shrink:0">
   <div class="card" style="padding:13px 15px;margin-bottom:12px">
     <div style="font-size:12px;font-weight:700;color:#5a6472;margin-bottom:8px">BẢNG THƯỜNG ĐƯỢC JOIN CÙNG</div>
     <div style="font-size:12.5px;line-height:1.9">
       📄 dwh.thue_bao_ngay <span class="muted">— 312 lần</span><br>
       📄 dm.doi_tac <span class="muted">— 190 lần</span><br>
       📄 bi.doanh_thu_thang <span class="muted">— 88 lần</span></div>
   </div>
   <div class="card" style="padding:13px 15px;margin-bottom:12px">
     <div style="font-size:12px;font-weight:700;color:#5a6472;margin-bottom:8px">DÙNG Ở ĐÂU (hạ nguồn)</div>
     <div style="font-size:12.5px;line-height:1.9">
       📊 Báo cáo Doanh thu ngày<br>📊 Dashboard Đối soát đối tác<br>
       ⚙️ Job <span class="mono">job_tonghop_doanh_thu</span></div>
   </div>
   <div class="card" style="padding:13px 15px">
     <div style="font-size:12px;font-weight:700;color:#5a6472;margin-bottom:8px">THÔNG BÁO GẦN ĐÂY</div>
     <div style="font-size:12.5px;line-height:1.6;color:#48505e">
       🔴 <b>03/08</b> — Luật "so_dien_thoai đúng định dạng" thất bại: 1.204 dòng sai<br><br>
       🟠 <b>01/08</b> — Cấu trúc bảng thay đổi: thêm cột <span class="mono">doi_tac</span></div>
   </div>
 </div>
</div>"""
    return shell("OpenMetadata — Hồ sơ bảng", "sandbox.open-metadata.org/table/hive_prod.bi.doi_soat_giao_dich_A",
                 NAVI("explore"), main, AC, "#FAFAFE",
                 note="OpenMetadata · HỒ SƠ MỘT BẢNG — tab Cấu trúc bảng")


# ---------------------------------------------------------------- 3. Lineage
def lineage():
    def node(x, y, title, sub, color, w=210, badge=""):
        return f"""<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;
  border:1.5px solid {color};border-radius:9px;background:#fff;box-shadow:0 1px 4px #0001">
  <div style="background:{color}12;padding:6px 10px;border-bottom:1px solid {color}44;
    font-size:12.5px;font-weight:700;color:{color}">{title} {badge}</div>
  <div style="padding:7px 10px;font-size:11.5px;line-height:1.75;color:#48505e" class="mono">{sub}</div></div>"""

    def line(x, y, w, label=""):
        lab = (f'<div style="position:absolute;left:{x + 6}px;top:{y - 17}px;font-size:10.5px;'
               f'color:#7147E8;background:#fff;padding:0 4px">{label}</div>' if label else "")
        return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:2px;'
                f'background:#7147E8"></div>'
                f'<div style="position:absolute;left:{x + w - 7}px;top:{y - 4}px;width:0;height:0;'
                f'border-left:8px solid #7147E8;border-top:5px solid transparent;'
                f'border-bottom:5px solid transparent"></div>{lab}')

    canvas = (
        node(0, 60, "📄 raw.gd_doi_tac_A", "giao_dich_id<br><b style='color:#B42318'>msisdn</b><br>amount<br>txn_date",
             "#98A2B3") +
        node(0, 300, "📄 dm.doi_tac", "doi_tac_id<br>ten_doi_tac", "#98A2B3") +
        node(300, 150, "⚙️ job_doi_soat_A", "Câu SQL: SELECT … <br>JOIN … GROUP BY<br>Chạy 06:00 hằng ngày",
             "#7147E8", 190) +
        node(560, 60, "📄 bi.doi_soat_giao_dich_A",
             "giao_dich_id<br><b style='color:#B42318'>so_dien_thoai</b><br>so_tien<br>ngay_ghi_nhan<br>doi_tac",
             "#7147E8", 220, '<span class="chip" style="background:#FFF1D6;color:#8A5B00">Tier 1</span>') +
        node(880, 40, "📄 bi.doanh_thu_thang", "thang<br>khu_vuc<br>tong_tien", "#12B76A") +
        node(880, 190, "📊 BC Doanh thu ngày", "Báo cáo Power BI<br>37 người xem/tuần", "#F79009") +
        node(880, 330, "📊 Dashboard Đối soát", "Báo cáo Power BI<br>12 người xem/tuần", "#F79009") +
        line(210, 200, 88) + line(492, 200, 66) +
        # nhánh dm.doi_tac đi ngang rồi gập lên vào job
        '<div style="position:absolute;left:210px;top:330px;width:185px;height:2px;background:#7147E8"></div>'
        '<div style="position:absolute;left:393px;top:258px;width:2px;height:74px;background:#7147E8"></div>'
        '<div style="position:absolute;left:389px;top:250px;width:0;height:0;border-bottom:8px solid #7147E8;'
        'border-left:5px solid transparent;border-right:5px solid transparent"></div>' +
        line(782, 120, 96, "so_tien → tong_tien") + line(782, 240, 96) + line(782, 370, 96))

    main = _head() + _tabs("Nguồn gốc") + f"""
<div style="display:flex;gap:10px;margin:14px 0 10px">
  <span class="btn ghost">◀ Thượng nguồn: 2 cấp</span>
  <span class="btn ghost">Hạ nguồn: 3 cấp ▶</span>
  <span class="btn" style="background:#7147E8">🔵 Đang bật: Nguồn gốc mức CỘT</span>
  <span class="btn ghost">✏️ Sửa nguồn gốc thủ công</span>
  <span class="btn ghost">📅 Xem theo mốc thời gian</span>
</div>
<div class="card" style="height:470px;position:relative;background:
  linear-gradient(#f8f9fb 1px,transparent 1px),linear-gradient(90deg,#f8f9fb 1px,transparent 1px);
  background-size:22px 22px;padding:10px;overflow:hidden">{canvas}</div>
<div style="margin-top:11px;font-size:12.5px;background:#F4F0FF;border:1px solid #D9CCFF;
  border-radius:7px;padding:10px 13px">
  💡 <b>Phân tích ảnh hưởng:</b> nếu đổi kiểu cột <span class="mono">so_tien</span> thì
  <b>1 bảng hạ nguồn</b> và <b>2 báo cáo</b> bị ảnh hưởng — hệ thống tự gửi thông báo cho
  3 người phụ trách tương ứng.</div>"""
    return shell("OpenMetadata — Nguồn gốc dữ liệu", "sandbox.open-metadata.org/table/…/lineage",
                 NAVI("lineage"), main, AC, "#FAFAFE",
                 note="OpenMetadata · NGUỒN GỐC DỮ LIỆU mức CỘT (column-level lineage)")


# ---------------------------------------------------------------- 4. Data quality
def quality():
    tests = [
        ("Số dòng nằm trong khoảng cho phép", "Bảng", "tableRowCountToBeBetween",
         "min 8.000.000 · max 20.000.000", "🟢 Đạt", "12.480.331", "06:12 hôm nay"),
        ("Cột giao_dich_id không được trùng", "giao_dich_id", "columnValuesToBeUnique",
         "—", "🟢 Đạt", "0 giá trị trùng", "06:12 hôm nay"),
        ("Cột so_dien_thoai không được rỗng", "so_dien_thoai", "columnValuesToBeNotNull",
         "cho phép ≤ 0,1%", "🟢 Đạt", "0,02% rỗng", "06:12 hôm nay"),
        ("so_dien_thoai đúng định dạng đầu số VN", "so_dien_thoai", "columnValuesToMatchRegex",
         "^(84|0)(3|5|7|8|9)[0-9]{8}$", "🔴 Thất bại", "1.204 / 12.480.331 sai", "06:12 hôm nay"),
        ("trang_thai chỉ nhận giá trị trong danh mục", "trang_thai", "columnValuesToBeInSet",
         "KHOP, LECH, CHO", "🟢 Đạt", "0 giá trị lạ", "06:12 hôm nay"),
        ("Dữ liệu phải đủ tươi", "Bảng", "tableDataToBeFresh",
         "≤ 24 giờ", "🟠 Cảnh báo", "trễ 26 giờ", "06:12 hôm nay"),
        ("Tổng so_tien khớp với bảng nguồn", "Bảng", "tableCustomSQLQuery",
         "SQL tự viết · lệch ≤ 0,01%", "🟢 Đạt", "lệch 0,002%", "06:14 hôm nay"),
    ]
    rows = ""
    for name, scope, kind, param, st, res, at in tests:
        col = {"🟢": "#067647", "🔴": "#B42318", "🟠": "#B54708"}[st[0]]
        rows += (f'<tr><td><b>{name}</b><div class="muted mono" style="font-size:11px">{kind}</div></td>'
                 f'<td class="mono">{scope}</td><td class="mono" style="font-size:11.5px">{param}</td>'
                 f'<td style="color:{col};font-weight:700">{st}</td><td>{res}</td>'
                 f'<td class="muted">{at}</td></tr>')

    spark = "".join(
        f'<div style="width:9px;height:{h}px;background:{c};border-radius:2px"></div>'
        for h, c in [(26, "#12B76A")] * 9 + [(26, "#F79009"), (26, "#12B76A"), (26, "#12B76A"),
                                             (26, "#F04438"), (26, "#12B76A"), (26, "#12B76A"),
                                             (26, "#F04438"), (26, "#12B76A"), (26, "#12B76A"),
                                             (26, "#12B76A"), (26, "#12B76A")])

    main = _head() + _tabs("Giám sát dữ liệu") + f"""
<div style="display:flex;gap:14px;margin:16px 0 14px">
  <div class="card" style="flex:1;padding:13px 15px">
    <div class="muted" style="font-size:11px">TỔNG SỐ TEST ĐÃ CHẠY</div>
    <div style="font-size:26px;font-weight:800">7</div>
    <div style="font-size:11.5px" class="muted">lần chạy 06:12 hôm nay</div></div>
  <div class="card" style="flex:1;padding:13px 15px">
    <div class="muted" style="font-size:11px">KẾT QUẢ</div>
    <div style="font-size:26px;font-weight:800;color:#067647">5</div>
    <div style="font-size:11.5px"><span style="color:#067647">5 Success</span> ·
      <span style="color:#B54708">1 Aborted</span> · <span style="color:#B42318">1 Failed</span></div></div>
  <div class="card" style="flex:1;padding:13px 15px">
    <div class="muted" style="font-size:11px">SỰ CỐ CHƯA XỬ LÝ</div>
    <div style="font-size:26px;font-weight:800;color:#B42318">1</div>
    <div style="font-size:11.5px" class="muted">Trạng thái: Ack</div></div>
  <div class="card" style="flex:2;padding:13px 15px">
    <div class="muted" style="font-size:11px">20 LẦN CHẠY GẦN NHẤT</div>
    <div style="display:flex;gap:4px;align-items:flex-end;margin-top:10px">{spark}</div>
    <div style="font-size:11.5px;margin-top:6px" class="muted">🟩 đạt &nbsp;🟧 cảnh báo &nbsp;🟥 thất bại</div></div>
</div>
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:9px">
  <div style="font-size:13.5px;font-weight:700">Danh sách luật kiểm tra</div>
  <div style="display:flex;gap:8px"><span class="btn ghost">⏱ Lịch chạy: 06:00 hằng ngày</span>
    <span class="btn">➕ Thêm luật kiểm tra</span></div>
</div>
<div class="card"><table class="g">
  <tr><th>Tên luật</th><th>Phạm vi</th><th>Tham số</th><th>Kết quả</th><th>Chi tiết</th><th>Lần chạy cuối</th></tr>
  {rows}</table></div>
<div style="margin-top:11px;font-size:12.5px;background:#FEF3F2;border:1px solid #FECDCA;
  border-radius:7px;padding:10px 13px">
  🔴 <b>Sự cố đang mở:</b> luật "so_dien_thoai đúng định dạng đầu số VN" thất bại từ 03/08.
  Người xử lý: <b>Trần Văn Hùng</b> · Trạng thái: <b>Ack</b> ·
  <span class="mono">New → Ack → Assigned → Resolved</span></div>"""
    return shell("OpenMetadata — Chất lượng dữ liệu", "sandbox.open-metadata.org/table/…/profiler",
                 NAVI("quality"), main, AC, "#FAFAFE",
                 note="OpenMetadata · TAB GIÁM SÁT DỮ LIỆU — danh mục luật chất lượng và kết quả")


# ---------------------------------------------------------------- 5. Add test wizard
def addtest():
    """Theo tài liệu chính thức: tab Data Observability > nút Add Test > chọn Table/Column test,
    điền Name + Description + Test type + Column + Parameters > Submit > trang đặt lịch."""

    def fld(label, value, hint="", mono=False, ph=False):
        return f"""<div style="margin-bottom:14px">
  <div style="font-size:12px;font-weight:600;color:#344054;margin-bottom:5px">{label}</div>
  <div style="border:1px solid #cfd6e0;border-radius:6px;padding:8px 11px;font-size:13px;background:#fff;
    {'font-family:Consolas,monospace;' if mono else ''}{'color:#98A2B3' if ph else ''}">{value}</div>
  {f'<div class="muted" style="font-size:11.5px;margin-top:4px">{hint}</div>' if hint else ''}</div>"""

    defs = "".join(
        f'<div style="border:1px solid {"#7147E8" if on else "#E4E7EC"};border-radius:7px;'
        f'padding:8px 11px;margin-bottom:6px;background:{"#F4F0FF" if on else "#fff"}">'
        f'<div class="mono" style="font-size:12px;font-weight:{700 if on else 400}">{n}</div>'
        f'<div class="muted" style="font-size:11px">{d}</div></div>'
        for n, d, on in [
            ("columnValuesToBeNotNull", "Cột không được có giá trị rỗng", False),
            ("columnValuesToBeUnique", "Mọi giá trị trong cột phải khác nhau", False),
            ("columnValuesToMatchRegex", "Giá trị phải khớp một mẫu định dạng", True),
            ("columnValuesToBeInSet", "Giá trị chỉ được thuộc một tập cho trước", False),
            ("columnValuesToBeBetween", "Giá trị số nằm giữa min và max", False),
            ("tableRowCountToBeBetween", "Số dòng của bảng nằm trong khoảng", False),
            ("tableDataToBeFresh", "Dữ liệu của bảng phải đủ tươi", False),
            ("tableCustomSQLQuery", "Tự viết câu SQL kiểm tra bất kỳ", False),
        ])

    main = f"""
<div class="crumb">bi.doi_soat_giao_dich_A › Data Observability › Add Test</div>
<h1 class="t">➕ Add Test — tạo luật kiểm tra không cần viết code</h1>
<div class="sub">Vào tab <b>Data Observability</b> của bảng → bấm nút <b>Add Test</b> ở góc trên bên phải
  → chọn <b>Table Test</b> hoặc <b>Column Test</b> → điền form → <b>Submit</b>.</div>
<div style="display:flex;gap:24px;margin-top:18px">
  <div style="width:330px;flex-shrink:0">
    <div style="font-size:13px;font-weight:700;margin-bottom:9px">Test type
      <span class="muted" style="font-weight:400">— chọn từ danh mục có sẵn</span></div>{defs}
    <div class="muted" style="font-size:11.5px;margin-top:8px">
      Danh sách đầy đủ lấy được từ API <span class="mono">GET /api/v1/dataQuality/testDefinitions</span></div>
  </div>
  <div style="flex:1">
    <div style="font-size:13px;font-weight:700;margin-bottom:12px">Form tạo test case</div>
    {fld("Name", "so_dien_thoai_dung_dinh_dang_VN", "Tên định danh cho test case")}
    {fld("Description", "Số điện thoại phải đúng mẫu đầu số di động Việt Nam")}
    {fld("Column", "so_dien_thoai ▾", "Chỉ hiện khi chọn Column Test")}
    {fld("Parameter — regex", "^(84|0)(3|5|7|8|9)[0-9]{8}$",
         "Tham số thay đổi theo từng test definition", mono=True)}
    <div style="border:1px solid #cfd6e0;border-radius:6px;padding:9px 11px;font-size:12.5px;
      background:#F9FAFB;margin-bottom:14px">
      ☑ <b>Compute passed/failed row count</b>
      <div class="muted" style="font-size:11.5px;margin-top:3px">
        Bật thì hệ thống mới đếm số dòng đạt/không đạt và lưu <b>mẫu dòng lỗi</b>.
        Mặc định <b>tắt</b> — không bật thì màn chi tiết lỗi sẽ trống.</div></div>
    <div style="display:flex;gap:10px"><span class="btn">Submit</span>
      <span class="btn ghost">Cancel</span></div>
  </div>
  <div style="width:310px;flex-shrink:0">
    <div class="card" style="padding:14px 16px;margin-bottom:12px;background:#F9FAFB">
      <div style="font-size:12px;font-weight:700;margin-bottom:8px">BƯỚC TIẾP THEO — SCHEDULE FOR INGESTION</div>
      <div style="font-size:12.5px;line-height:1.8">
        Sau khi Submit, hệ thống chuyển sang trang đặt lịch chạy:<br><br>
        <b>Frequency:</b> Day ▾ &nbsp; <b>Time:</b> 06:00<br>
        <span class="muted">Múi giờ mặc định là <b>UTC</b></span><br><br>
        Chọn <b>None</b> nếu muốn tự kích hoạt từ pipeline bên ngoài thay vì chạy theo lịch.</div>
    </div>
    <div class="card" style="padding:14px 16px;background:#FEF3F2;border-color:#FECDCA">
      <div style="font-size:12px;font-weight:700;margin-bottom:7px">⚠️ KHÔNG CÓ TRONG FORM NÀY</div>
      <div style="font-size:12.5px;line-height:1.75">
        • <b>Không có nút chạy thử / xem trước kết quả</b> trước khi lưu<br>
        • <b>Không có trường mức độ nghiêm trọng</b> — severity được hệ thống
          <b>tự gán cho SỰ CỐ</b> sau khi test thất bại, người dùng có thể sửa lại</div>
    </div>
  </div>
</div>"""
    return shell("OpenMetadata — Add Test", "sandbox.open-metadata.org/…/add-data-quality-test",
                 NAVI("quality"), main, AC, "#FAFAFE",
                 note="OpenMetadata · FORM ADD TEST — theo đúng các bước trong tài liệu chính thức")



# ---------------------------------------------------------------- 6. Glossary
def glossary():
    tree = "".join(
        f'<div style="padding:6px 10px;font-size:12.5px;border-radius:6px;margin-bottom:2px;'
        f'{"background:#F4F0FF;font-weight:700;color:#7147E8" if on else ""}">{ind}{t}</div>'
        for ind, t, on in [
            ("", "📚 Từ điển Kinh doanh", False),
            ("&nbsp;&nbsp;", "📁 Thuê bao", False),
            ("&nbsp;&nbsp;&nbsp;&nbsp;", "📄 Thuê bao hoạt động", False),
            ("&nbsp;&nbsp;&nbsp;&nbsp;", "📄 Thuê bao rời mạng", False),
            ("&nbsp;&nbsp;", "📁 Doanh thu", False),
            ("&nbsp;&nbsp;&nbsp;&nbsp;", "📄 Doanh thu ghi nhận", True),
            ("&nbsp;&nbsp;&nbsp;&nbsp;", "📄 Doanh thu thực thu", False),
            ("&nbsp;&nbsp;", "📁 Đối soát", False),
            ("", "📚 Từ điển Kỹ thuật", False),
        ])

    assets = "".join(
        f'<tr><td>{ic} <b>{n}</b></td><td class="mono muted">{c}</td><td>{k}</td></tr>'
        for ic, n, c, k in [
            ("📄", "bi.doi_soat_giao_dich_A", "so_tien", "Cột"),
            ("📄", "bi.doanh_thu_thang", "tong_tien", "Cột"),
            ("📄", "dwh.thue_bao_ngay", "doanh_thu_ngay", "Cột"),
            ("📊", "Báo cáo Doanh thu ngày", "—", "Báo cáo"),
        ])

    main = f"""
<div class="crumb">Từ điển nghiệp vụ › Từ điển Kinh doanh › Doanh thu</div>
<h1 class="t">📖 Doanh thu ghi nhận
  <span class="chip" style="background:#ECFDF3;color:#067647">Đã phê duyệt</span>
  <span class="chip" style="background:#F2F4F7;color:#475467">Phiên bản 1.3</span></h1>
<div class="sub">Chủ sở hữu thuật ngữ: <b>Ban Tài chính</b> · Cập nhật 12/07/2026 bởi Nguyễn Thị Phương</div>
<div style="display:flex;gap:24px;margin-top:16px">
  <div style="width:250px;flex-shrink:0">
    <div style="font-size:12px;font-weight:700;color:#5a6472;margin-bottom:8px">CÂY THUẬT NGỮ</div>
    <div class="card" style="padding:8px">{tree}</div></div>
  <div style="flex:1">
    <div class="card" style="padding:15px 18px;margin-bottom:14px">
      <div style="font-size:12px;font-weight:700;color:#5a6472;margin-bottom:6px">ĐỊNH NGHĨA</div>
      <div style="font-size:13.5px;line-height:1.75">Doanh thu đã được ghi nhận vào sổ kế toán trong kỳ,
        <b>không phụ thuộc vào việc đã thu được tiền hay chưa</b>. Khác với "Doanh thu thực thu" —
        là số tiền đã thực sự về tài khoản.</div>
      <div style="margin-top:12px;display:flex;gap:26px;font-size:12.5px">
        <div><span class="muted">Đơn vị:</span> <b>VNĐ</b></div>
        <div><span class="muted">Từ đồng nghĩa:</span> <b>Revenue, DT ghi nhận</b></div>
        <div><span class="muted">Thuật ngữ liên quan:</span>
          <span class="chip" style="background:#F0F4FF;color:#3538CD">Doanh thu thực thu</span></div>
      </div></div>
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:9px">
      <div style="font-size:13px;font-weight:700">Đang được gắn vào 4 tài sản dữ liệu</div>
      <span class="btn ghost">➕ Gắn thêm cột / bảng</span></div>
    <div class="card"><table class="g">
      <tr><th>Tài sản dữ liệu</th><th>Cột</th><th>Loại</th></tr>{assets}</table></div>
    <div style="margin-top:12px;font-size:12.5px;background:#F4F0FF;border:1px solid #D9CCFF;
      border-radius:7px;padding:10px 13px">
      💡 Nhờ liên kết này, khi người dùng gõ <b>"doanh thu"</b> ở ô tìm kiếm, hệ thống trả về
      <b>đúng 4 tài sản</b> ở trên — kể cả khi tên cột là <span class="mono">tong_tien</span>,
      không hề chứa chữ "doanh thu".</div>
  </div>
</div>"""
    return shell("OpenMetadata — Từ điển nghiệp vụ", "sandbox.open-metadata.org/glossary/Kinh-doanh.Doanh-thu",
                 NAVI("glossary"), main, AC, "#FAFAFE",
                 note="OpenMetadata · TỪ ĐIỂN NGHIỆP VỤ gắn trực tiếp vào cột dữ liệu thật")


SCREENS = {
    "om-01-explore": explore, "om-02-table": table, "om-03-lineage": lineage,
    "om-04-quality": quality, "om-05-add-test": addtest, "om-06-glossary": glossary,
}
