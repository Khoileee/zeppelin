# -*- coding: utf-8 -*-
"""DMP — Module ① Data Catalog: màn chi tiết bảng (6 tab) + 3 menu còn lại."""
from dmp import shell, fld, chip, AC

TABS = ["Tổng quan", "Cột", "Chất lượng", "Nguồn gốc", "Quyền", "Lịch sử"]
CRUMB = "Data Catalog › Bảng dữ liệu › bi.doi_soat_giao_dich_A"
TITLE = "🗂️ bi.doi_soat_giao_dich_A"
DESC = ("Đối soát giao dịch — Đối tác A &nbsp;·&nbsp; BDA: Nguyễn Thị Phương &nbsp;·&nbsp; "
        "DE: Trần Văn Hùng &nbsp;·&nbsp; Miền: Kinh doanh")
ACT = ('<span class="btn w">⬇️ Xuất metadata</span><span class="btn w">🔗 Chia sẻ</span>'
       '<span class="btn">✎ Sửa</span>')


def _kpi(items):
    return ('<div style="display:flex;gap:12px;margin-bottom:16px">' + "".join(
        f'<div class="card kpi"><div class="lb">{l}</div>'
        f'<div class="vl" style="color:{c}">{v}</div><div class="sb">{s}</div></div>'
        for l, v, s, c in items) + "</div>")


# ============================================================ TAB TỔNG QUAN
def tab_overview():
    body = _kpi([
        ("ĐỘ TƯƠI", "4 giờ", "cam kết: trước 07:00 hằng ngày", "#067647"),
        ("SỐ DÒNG", "12.480.331", "▲ 0,8% so với hôm qua", "#101828"),
        ("LUẬT CHẤT LƯỢNG", "5/7 đạt", "1 cảnh báo · 1 thất bại", "#B54708"),
        ("LƯỢT DÙNG / TUẦN", "1.204", "37 người · 6 báo cáo", "#101828"),
        ("DUNG LƯỢNG", "184 GB", "Iceberg · 412 snapshot", "#101828"),
    ]) + f"""
<div style="display:flex;gap:16px">
  <div style="flex:1.4">
    <div class="card" style="padding:16px 19px;margin-bottom:14px">
      <div class="sec">MÔ TẢ NGHIỆP VỤ</div>
      <div style="font-size:13px;line-height:1.7;color:#344054">
        Bảng đối soát giao dịch với đối tác A. Nguồn: file đối tác gửi qua SFTP hằng ngày 05:30.
        Chốt số liệu 06:00. Dùng cho báo cáo doanh thu ngày và dashboard đối soát.</div>
      <div style="margin-top:13px;display:flex;gap:7px;flex-wrap:wrap">
        {chip("🏅 Tier 1 — Dữ liệu vàng", "o")}{chip("Iceberg", "t")}
        {chip("PII.Nhạy cảm", "r")}{chip("Kinh doanh", "b")}{chip("Đang dùng", "g")}</div>
    </div>
    <div class="card" style="padding:16px 19px;margin-bottom:14px">
      <div class="sec">THÔNG TIN KỸ THUẬT</div>
      <table class="g" style="font-size:12.5px">
        <tr><td style="width:200px;color:#667085">Vùng lưu trữ</td>
            <td class="mono">business_zone / bi</td></tr>
        <tr><td style="color:#667085">Đường dẫn vật lý</td>
            <td class="mono">/storage/business_zone/bi/doi_soat_giao_dich_A</td></tr>
        <tr><td style="color:#667085">Định dạng bảng</td><td>Iceberg</td></tr>
        <tr><td style="color:#667085">Chế độ ghi</td><td>MERGE theo <span class="mono">giao_dich_id</span></td></tr>
        <tr><td style="color:#667085">Phân vùng</td><td class="mono">ngay_ghi_nhan</td></tr>
        <tr><td style="color:#667085">Chu kỳ cập nhật cam kết</td>
            <td><b>Hằng ngày — trước 07:00</b></td></tr>
        <tr><td style="color:#667085">Thời gian lưu trữ</td><td>36 tháng</td></tr>
      </table>
    </div>
  </div>
  <div style="width:400px;flex-shrink:0">
    <div class="card" style="padding:15px 17px;margin-bottom:13px">
      <div class="sec">AI ĐANG DÙNG BẢNG NÀY</div>
      <table class="g" style="font-size:12.5px">
        <tr><td>📊 Báo cáo Doanh thu ngày</td><td class="muted">Ban Kinh doanh</td></tr>
        <tr><td>📊 Dashboard Đối soát</td><td class="muted">Ban Kinh doanh</td></tr>
        <tr><td>🗄️ bi.doanh_thu_thang</td><td class="muted">Đội DE</td></tr>
        <tr><td>⚙️ job_tonghop_doanh_thu</td><td class="muted">Đội DE</td></tr>
      </table>
      <div class="muted" style="font-size:11.5px;margin-top:8px">
        Lấy từ tab Nguồn gốc — không phải khai tay</div>
    </div>
    <div class="card" style="padding:15px 17px;margin-bottom:13px">
      <div class="sec">HOẠT ĐỘNG GẦN ĐÂY</div>
      <div style="font-size:12.5px;line-height:1.8">
        🔴 <b>03/08 06:14</b> — luật <i>so_dien_thoai đúng định dạng</i> thất bại, 1.204 dòng sai<br>
        🟠 <b>01/08 09:22</b> — thêm cột <span class="mono">doi_tac</span><br>
        ✅ <b>28/07 15:40</b> — N.T.Phương cập nhật mô tả</div>
    </div>
    <div class="card" style="padding:15px 17px;background:#FFFAEB;border-color:#FEDF89">
      <div style="font-size:12px;font-weight:700;margin-bottom:8px">📋 ĐỘ HOÀN THIỆN HỒ SƠ — 5/6</div>
      <div style="font-size:12.5px;line-height:1.9">
        ✅ Có mô tả · ✅ Có BDA và DE · ✅ Có miền và Tier<br>
        ✅ Mọi cột có mô tả · ✅ Cột nhạy cảm đã gắn nhãn<br>
        ⬜ <b>Tier 1 cần ≥ 3 luật chất lượng đạt</b> — hiện 5/7 nhưng 1 thất bại</div>
    </div>
  </div>
</div>"""
    return shell("dmp.vds.vn/catalog/tables/BI-0142", CRUMB, TITLE, DESC, body,
                 "DMP · Menu 1.1 — CHI TIẾT BẢNG · tab TỔNG QUAN", "m11",
                 tabs=("Tổng quan", TABS), actions=ACT, height=1020)


# ============================================================ TAB CỘT
def tab_columns():
    cols = [
        ("giao_dich_id", "STRING", "Mã định danh giao dịch", "—", "DATA_GENERAL",
         "Không trùng, không rỗng", "—", "PK", "Không", "0%", "—", "2 luật"),
        ("so_dien_thoai", "STRING", "Số thuê bao thực hiện giao dịch", "Thuê bao", "PD_SENSITIVE",
         "Đúng đầu số di động VN", "^(84|0)(3|5|7|8|9)…", "—", "Không", "0,02%", "—", "🔴 2 luật"),
        ("so_tien", "DECIMAL(18,2)", "Số tiền giao dịch", "Doanh thu ghi nhận", "TaiChinh.DoanhThu",
         "Không âm", "0 – 500.000.000", "—", "Không", "0%", "1.000 / 48.500.000", "2 luật"),
        ("ngay_ghi_nhan", "DATE", "Ngày hệ thống ghi nhận", "Ngày phát sinh", "DATA_GENERAL",
         "Không muộn hơn hôm nay", "—", "Phân vùng", "Không", "0%", "01/01/24 – 03/08/26", "1 luật"),
        ("trang_thai", "STRING", "Trạng thái đối soát", "—", "DATA_GENERAL",
         "Chỉ nhận 3 giá trị", "KHOP · LECH · CHO", "—", "Không", "0%", "—", "1 luật"),
        ("doi_tac", "STRING", "Mã đối tác", "Đối tác", "DATA_GENERAL",
         "Phải có trong danh mục Đối tác", "→ dm.doi_tac", "FK", "Không", "0%", "—", "🟠 1 luật"),
    ]
    tr = ""
    for nm, ty, de, gl, tg, br, vr, ky, nu, nl, mm, rl in cols:
        tgc = ("r" if tg == "PD_SENSITIVE" else "o" if "TaiChinh" in tg else "n")
        rlc = "#B42318" if "🔴" in rl else "#B54708" if "🟠" in rl else "#067647"
        tr += (f'<tr><td class="mono"><b>{nm}</b></td><td class="mono muted">{ty}</td><td>{de}</td>'
               f'<td>{chip(gl, "b") if gl != "—" else "<span class=muted>+ gắn</span>"}</td>'
               f'<td>{chip(tg, tgc)}</td><td style="font-size:12px">{br}</td>'
               f'<td class="mono" style="font-size:11.5px">{vr}</td><td>{ky}</td><td>{nu}</td>'
               f'<td>{nl}</td><td class="mono" style="font-size:11.5px">{mm}</td>'
               f'<td style="color:{rlc};font-weight:700">{rl}</td></tr>')

    body = f"""
<div style="display:flex;gap:10px;margin-bottom:13px;align-items:center">
  <div style="flex:1;border:1px solid #d0d7e2;border-radius:8px;padding:8px 12px;font-size:12.5px;
    background:#fff">🔍 <span class="muted">Tìm cột theo tên, mô tả, thuật ngữ…</span></div>
  <span class="btn w">🏷️ Gắn nhãn hàng loạt</span>
  <span class="btn w">📖 Gắn thuật ngữ hàng loạt</span>
  <span class="btn w">⬇️ Xuất Excel</span>
  <span class="btn">✎ Sửa cấu trúc</span>
</div>
<div class="card">
  <div style="display:flex;justify-content:space-between;align-items:center;padding:10px 14px;
    border-bottom:1px solid #eef1f6">
    <div style="font-size:13px"><b>6 cột</b> <span class="muted">· 1 cột nhạy cảm · 6/6 đã có mô tả</span></div>
    <div class="muted" style="font-size:11.5px">
      Cột <b>% rỗng</b> và <b>Min / Max</b> lấy từ <b>3.3 Phân tích dữ liệu</b> — quét lúc 06:12 hôm nay</div>
  </div>
  <table class="g">
    <tr><th>Tên cột</th><th>Kiểu</th><th>Mô tả</th><th>Thuật ngữ</th><th>Nhãn phân loại</th>
      <th>Quy tắc nghiệp vụ</th><th>Tập giá trị / Khoảng</th><th>Khoá</th><th>Cho rỗng</th>
      <th>% rỗng</th><th>Min / Max</th><th>Luật đang gán</th></tr>
    {tr}</table>
</div>
<div style="display:flex;gap:14px;margin-top:14px">
  <div class="note" style="flex:1;background:#EFF4FF;border:1px solid #C7D7FE">
    ⭐ <b>Đây là màn quan trọng nhất của cả tool.</b> Ba cột <b>Thuật ngữ</b>, <b>Nhãn phân loại</b> và
    <b>Quy tắc nghiệp vụ</b> là nơi <b>khai một lần, dùng ở nhiều nơi</b>:<br>
    • Thuật ngữ → người dùng gõ "doanh thu" ở ô tìm kiếm sẽ ra cột <span class="mono">so_tien</span><br>
    • Nhãn <span class="mono">PD_SENSITIVE</span> → chính sách che dữ liệu ở <b>5.2</b> tự áp lên cột
      <span class="mono">so_dien_thoai</span><br>
    • Tập giá trị <span class="mono">KHOP · LECH · CHO</span> → sinh thẳng thành luật chất lượng ở <b>3.2</b>
  </div>
  <div class="note" style="width:420px;background:#FFFAEB;border:1px solid #FEDF89">
    ⚠️ <b>So với SQLWF hiện tại:</b> bảng khai trường đã có sẵn <b>Glossary term</b>,
    <b>Phân loại dữ liệu</b>, <b>Quy tắc nghiệp vụ</b>, <b>Tập giá trị</b>.<br>
    Ba cột <b>mới thêm</b> là <b>% rỗng</b>, <b>Min / Max</b> và <b>Luật đang gán</b> —
    đọc từ module Chất lượng, <b>không khai lại</b>.
  </div>
</div>"""
    return shell("dmp.vds.vn/catalog/tables/BI-0142/columns", CRUMB, TITLE, DESC, body,
                 "DMP · Menu 1.1 — CHI TIẾT BẢNG · tab CỘT", "m11",
                 tabs=("Cột", TABS), actions=ACT, height=1000)


# ============================================================ TAB CHẤT LƯỢNG
def tab_quality():
    rules = [
        ("Số dòng trong khoảng cho phép", "Bảng", "Đầy đủ", "8.000.000 – 20.000.000",
         "✅ Đạt", "12.480.331", "06:12"),
        ("giao_dich_id không trùng", "giao_dich_id", "Duy nhất", "—", "✅ Đạt", "0 bản trùng", "06:12"),
        ("so_dien_thoai không rỗng", "so_dien_thoai", "Đầy đủ", "≤ 0,1%", "✅ Đạt", "0,02%", "06:12"),
        ("so_dien_thoai đúng đầu số VN", "so_dien_thoai", "Hợp lệ", "sai ≤ 0,5%",
         "❌ Thất bại", "0,96% — 1.204 dòng", "06:12"),
        ("trang_thai thuộc danh mục", "trang_thai", "Hợp lệ", "KHOP · LECH · CHO",
         "✅ Đạt", "0 giá trị lạ", "06:12"),
        ("doi_tac tồn tại trong danh mục Đối tác", "doi_tac", "Nhất quán", "→ dm.doi_tac",
         "⚠️ Cảnh báo", "3 mã lạ", "06:12"),
        ("Dữ liệu về đúng giờ cam kết", "Bảng", "Kịp thời", "trước 07:00", "✅ Đạt", "06:02", "07:00"),
    ]
    tr = ""
    for nm, sc, dim, par, st, val, at in rules:
        c = "#067647" if "✅" in st else "#B42318" if "❌" in st else "#B54708"
        tr += (f'<tr><td><b>{nm}</b></td><td class="mono">{sc}</td><td>{chip(dim, "b")}</td>'
               f'<td class="mono" style="font-size:11.5px">{par}</td>'
               f'<td style="color:{c};font-weight:700">{st}</td><td>{val}</td>'
               f'<td class="muted">{at}</td>'
               f'<td><span class="ico">👁</span><span class="ico">✎</span></td></tr>')

    dims = "".join(
        f'<div style="flex:1;text-align:center;padding:9px 6px;border-radius:8px;background:{bg}">'
        f'<div style="font-size:11px;color:#667085">{d}</div>'
        f'<div style="font-size:19px;font-weight:800;color:{c}">{v}</div></div>'
        for d, v, c, bg in [("Đầy đủ", "100", "#067647", "#ECFDF3"),
                            ("Hợp lệ", "50", "#B42318", "#FEF3F2"),
                            ("Nhất quán", "67", "#B54708", "#FFFAEB"),
                            ("Duy nhất", "100", "#067647", "#ECFDF3"),
                            ("Chính xác", "—", "#8b95a7", "#F2F4F7"),
                            ("Kịp thời", "100", "#067647", "#ECFDF3")])

    body = _kpi([
        ("ĐIỂM CHẤT LƯỢNG", "83", "▼ 12 điểm so với tuần trước", "#B54708"),
        ("LUẬT ĐANG ÁP DỤNG", "7", "5 đạt · 1 cảnh báo · 1 thất bại", "#101828"),
        ("SỰ CỐ ĐANG MỞ", "1", "Đã gán cho Trần Văn Hùng", "#B42318"),
        ("LẦN QUÉT GẦN NHẤT", "06:12", "hôm nay · theo lịch 06:00", "#101828"),
    ]) + f"""
<div class="card" style="padding:15px 18px;margin-bottom:14px">
  <div class="sec">ĐIỂM THEO 6 CHIỀU CHẤT LƯỢNG</div>
  <div style="display:flex;gap:10px">{dims}</div>
  <div class="muted" style="font-size:11.5px;margin-top:9px">
    Điểm mỗi chiều = trung bình % dòng đạt của các luật thuộc chiều đó.
    Điểm bảng = trung bình 6 chiều. Chiều <b>Chính xác</b> chưa có luật nào nên không tính.</div>
</div>
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
  <div style="font-size:13.5px;font-weight:700">Luật đang áp dụng cho bảng này</div>
  <div style="display:flex;gap:8px"><span class="btn w">⏱ Lịch quét: 06:00 hằng ngày</span>
    <span class="btn">➕ Gán luật từ thư viện</span></div>
</div>
<div class="card"><table class="g">
  <tr><th>Tên luật</th><th>Phạm vi</th><th>Chiều</th><th>Tham số</th><th>Kết quả</th>
    <th>Giá trị đo được</th><th>Lúc</th><th></th></tr>{tr}</table></div>
<div class="note" style="background:#FEF3F2;border:1px solid #FECDCA;margin-top:14px">
  🔴 <b>Sự cố #4821 đang mở</b> — luật <i>so_dien_thoai đúng đầu số VN</i> thất bại từ 31/07.
  Người xử lý: <b>Trần Văn Hùng (DE phụ trách)</b> — <b>hệ thống tự gán</b> dựa trên trường DE khai ở tab Tổng quan.
  Trạng thái: <b>Đang xử lý</b> · Hạn: 06/08.
  <span style="color:#B42318">Bấm vào luật để xem 1.204 dòng sai và tải về gửi đối tác.</span>
</div>"""
    return shell("dmp.vds.vn/catalog/tables/BI-0142/quality", CRUMB, TITLE, DESC, body,
                 "DMP · Menu 1.1 — CHI TIẾT BẢNG · tab CHẤT LƯỢNG", "m11",
                 tabs=("Chất lượng", TABS), actions=ACT, height=1020)


# ============================================================ TAB NGUỒN GỐC
def tab_lineage():
    def node(x, y, ic, title, sub, color, w=190, badge="", dashed=False):
        return f"""<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;
  border:1.5px {'dashed' if dashed else 'solid'} {color};border-radius:9px;background:#fff;
  box-shadow:0 1px 4px #0001">
  <div style="background:{color}12;padding:5px 9px;border-bottom:1px solid {color}33;
    font-size:11.5px;font-weight:700;color:{color}">{ic} {title} {badge}</div>
  <div style="padding:5px 9px;font-size:10.5px;line-height:1.6;color:#475467">{sub}</div></div>"""

    def more(x, y, txt, w=190):
        return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;'
                f'border:1.5px dashed #98a2b3;border-radius:9px;background:#f8fafc;'
                f'padding:8px 9px;text-align:center;font-size:11.5px;color:#475467;'
                f'font-weight:600">{txt}</div>')

    def elbow(x1, y1, x2, y2, lb="", col=None):
        col = col or AC
        mid = x1 + (x2 - x1) // 2
        s = (f'<div style="position:absolute;left:{x1}px;top:{y1}px;width:{mid - x1}px;height:2px;'
             f'background:{col}"></div>')
        if y1 != y2:
            top, h = min(y1, y2), abs(y2 - y1)
            s += (f'<div style="position:absolute;left:{mid}px;top:{top}px;width:2px;height:{h}px;'
                  f'background:{col}"></div>')
        s += (f'<div style="position:absolute;left:{mid}px;top:{y2}px;width:{x2 - mid - 8}px;'
              f'height:2px;background:{col}"></div>'
              f'<div style="position:absolute;left:{x2 - 8}px;top:{y2 - 4}px;width:0;height:0;'
              f'border-left:8px solid {col};border-top:5px solid transparent;'
              f'border-bottom:5px solid transparent"></div>')
        if lb:
            s += (f'<div style="position:absolute;left:{x1 + 10}px;top:{y1 - 19}px;font-size:10.5px;'
                  f'color:{col};background:#fff;padding:0 4px;white-space:nowrap">{lb}</div>')
        return s

    canvas = (
        # ---- 3 nguồn ghi vào CÙNG một bảng
        node(0, 20, "⚙️", "job_doi_soat_A", "bước 3 · chạy 06:00<br>ghi 8/6 cột", "#7147e8") +
        node(0, 105, "⚙️", "job_bu_du_lieu_A", "bước 1 · chạy khi cần<br>nạp lại lịch sử", "#7147e8") +
        node(0, 190, "📥", "Cửa nạp SFTP", "sửa tay khi đối tác<br>gửi file bổ sung", "#7147e8") +
        more(0, 275, "▾ còn 1 nguồn nữa") +
        # ---- bảng đang xem
        node(300, 90, "🗄️", "bi.doi_soat_giao_dich_A", "<b>BẢNG ĐANG XEM</b><br>6 cột · Tier 1 · Iceberg",
             AC, 230, chip("Tier 1", "o")) +
        # ---- hạ nguồn
        node(640, 15, "🗄️", "bi.doanh_thu_thang", "Tier 1 · Đội DE", "#12b76a") +
        node(640, 100, "🗄️", "mart.kpi_kinh_doanh", "Tier 2 · Đội DE", "#12b76a") +
        node(640, 185, "📊", "8 báo cáo Power BI", "<b>gộp nhóm</b> · 2.140 lượt/tuần<br>"
                                                   "3 đơn vị · bấm để xoè", "#f79009") +
        node(640, 275, "🤖", "Mô hình dự báo rời mạng", "Data Science", "#12b76a") +
        more(640, 355, "▾ còn 4 nút ở cấp 3"),
        )[0] if False else (
        node(0, 20, "⚙️", "job_doi_soat_A", "bước 3 · chạy 06:00<br>ghi 8/6 cột", "#7147e8") +
        node(0, 105, "⚙️", "job_bu_du_lieu_A", "bước 1 · chạy khi cần<br>nạp lại lịch sử", "#7147e8") +
        node(0, 190, "📥", "Cửa nạp SFTP", "sửa tay khi đối tác<br>gửi file bổ sung", "#7147e8") +
        more(0, 275, "▾ còn 1 nguồn nữa") +
        node(300, 90, "🗄️", "bi.doi_soat_giao_dich_A", "<b>BẢNG ĐANG XEM</b><br>6 cột · Tier 1 · Iceberg",
             AC, 230, chip("Tier 1", "o")) +
        node(640, 15, "🗄️", "bi.doanh_thu_thang", "Tier 1 · Đội DE", "#12b76a") +
        node(640, 100, "🗄️", "mart.kpi_kinh_doanh", "Tier 2 · Đội DE", "#12b76a") +
        node(640, 185, "📊", "8 báo cáo Power BI", "<b>gộp nhóm</b> · 2.140 lượt/tuần<br>"
                                                   "3 đơn vị · bấm để xoè", "#f79009") +
        node(640, 275, "🤖", "Mô hình dự báo rời mạng", "Data Science", "#12b76a") +
        more(640, 355, "▾ còn 4 nút ở cấp 3") +
        elbow(191, 50, 300, 135) +
        elbow(191, 135, 300, 135) +
        elbow(191, 220, 300, 135) +
        elbow(531, 135, 640, 45, "so_tien → tong_tien") +
        elbow(531, 135, 640, 130) +
        elbow(531, 135, 640, 215) +
        elbow(531, 135, 640, 305))

    body = f"""
<div style="display:flex;gap:9px;margin-bottom:13px">
  <span class="btn w">◀ Thượng nguồn: 2 cấp</span>
  <span class="btn w">Hạ nguồn: 3 cấp ▶</span>
  <span class="btn">🔵 Đang bật: mức CỘT</span>
  <span class="btn w">🔀 Gộp nút cùng loại: Bật</span>
  <span class="btn w">✎ Vẽ tay bổ sung</span>
  <div style="flex:1"></div>
  <span class="btn w">📉 Phân tích ảnh hưởng</span>
  <span class="btn w">⬇️ Xuất danh sách (CSV)</span>
</div>
<div class="card" style="height:445px;position:relative;padding:12px;overflow:hidden;background:
  linear-gradient(#f7f9fc 1px,transparent 1px),linear-gradient(90deg,#f7f9fc 1px,transparent 1px);
  background-size:22px 22px">{canvas}
  <div style="position:absolute;left:12px;bottom:10px;font-size:11px;color:#8b95a7">
    Thượng nguồn: <b>4 nguồn</b> &nbsp;·&nbsp; Hạ nguồn: <b>15 tài sản</b> qua 3 cấp
    &nbsp;·&nbsp; đang hiện 3 + 4 nút, phần còn lại gộp lại</div>
</div>
<div style="display:flex;gap:14px;margin-top:14px">
  <div class="note" style="flex:1.2;background:#EFF4FF;border:1px solid #C7D7FE">
    ⚠️ <b>Một bảng KHÔNG chỉ do một job sinh ra.</b> Ví dụ trên có <b>4 nguồn cùng ghi</b>:
    job chính · job nạp bù lịch sử · sửa tay qua cửa nạp · và một nguồn nữa.<br>
    Vì vậy giao diện phải chịu được cả hai chiều đều nhiều — xem 4 quy tắc hiển thị bên phải.
  </div>
  <div class="note" style="width:520px;background:#FFFAEB;border:1px solid #FEDF89">
    <b>4 quy tắc để sơ đồ không vỡ</b><br>
    ① Mỗi cột hiện tối đa <b>5 nút</b>, còn lại gom vào nút <i>"▾ còn N nút nữa"</i><br>
    ② Nút cùng loại và cùng đơn vị thì <b>gộp thành một</b> — ví dụ <i>"8 báo cáo Power BI"</i><br>
    ③ Bố cục <b>tự tính theo số nút</b>, không dùng toạ độ cố định<br>
    ④ Quá <b>60 nút</b> thì chuyển sang <b>chế độ bảng</b> thay vì vẽ sơ đồ
  </div>
</div>"""
    return shell("dmp.vds.vn/catalog/tables/BI-0142/lineage", CRUMB, TITLE, DESC, body,
                 "DMP · Menu 1.1 — CHI TIẾT BẢNG · tab NGUỒN GỐC (nhiều nguồn, nhiều đích)", "m11",
                 tabs=("Nguồn gốc", TABS), actions=ACT)


SCREENS = {
    "dmp-03-table-overview": tab_overview,
    "dmp-04-table-columns": tab_columns,
    "dmp-05-table-quality": tab_quality,
    "dmp-06-table-lineage": tab_lineage,
}
