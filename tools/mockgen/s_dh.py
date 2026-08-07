# -*- coding: utf-8 -*-
"""Màn hình DataHub — hợp đồng dữ liệu & phân tích ảnh hưởng."""
from common import shell, nav

AC = "#1B75BC"
NAVI = lambda act: nav("DataHub", AC, [
    ("🏠", "Trang chủ", act == "home"),
    ("🔍", "Tìm kiếm", act == "search"),
    ("🧊", "Miền dữ liệu", act == "domain"),
    ("📦", "Sản phẩm dữ liệu", act == "product"),
    ("📖", "Từ điển nghiệp vụ", act == "glossary"),
    ("📜", "Hợp đồng dữ liệu", act == "contract"),
    ("🔗", "Nguồn gốc & Ảnh hưởng", act == "lineage"),
    ("⚙️", "Quản trị", act == "admin"),
], AC)


def _head(tab):
    names = ["Tổng quan", "Cấu trúc", "Nguồn gốc", "Chất lượng", "Quyền truy cập", "Thuộc tính"]
    tabs = "".join(f'<div class="{"on" if n == tab else ""}">{n}</div>' for n in names)
    return f"""
<div class="crumb">Tập dữ liệu · Hive › bi › doi_soat</div>
<h1 class="t">🗄️ doi_soat_giao_dich_A
  <span class="chip" style="background:#E8F4FD;color:#1B75BC">Sản phẩm dữ liệu: Đối soát đối tác</span></h1>
<div class="sub">Miền: Kinh doanh · Người sản xuất (producer): <b>Đội Data Engineering</b> ·
  4 đơn vị tiêu thụ (consumer)</div>
<div class="tabs">{tabs}</div>"""


# ---------------------------------------------------------------- contract
def contract():
    def asr(kind, name, detail, status, last):
        c = {"🟢": "#067647", "🔴": "#B42318", "🟠": "#B54708"}[status[0]]
        return (f'<tr><td><span class="chip" style="background:#EEF4FF;color:#3538CD">{kind}</span></td>'
                f'<td><b>{name}</b></td><td class="mono" style="font-size:11.5px">{detail}</td>'
                f'<td style="color:{c};font-weight:700">{status}</td><td class="muted">{last}</td></tr>')

    rows = (asr("Độ tươi", "Dữ liệu phải cập nhật trước 07:00 hằng ngày",
                "freshness ≤ 24h · cron 0 7 * * *", "🟢 Đạt", "07:02 hôm nay") +
            asr("Cấu trúc", "Không được xoá / đổi kiểu 6 cột đã cam kết",
                "schema hash = a91f… · chế độ: chặt", "🟢 Đạt", "07:02 hôm nay") +
            asr("Khối lượng", "Số dòng mới mỗi ngày trong khoảng cho phép",
                "row_count_delta ∈ [80.000 ; 300.000]", "🟢 Đạt", "07:02 hôm nay") +
            asr("Chất lượng", "so_dien_thoai đúng định dạng · tỉ lệ sai ≤ 0,5%",
                "custom SQL assertion", "🔴 Vi phạm", "07:02 hôm nay") +
            asr("Cột", "so_tien không âm và không rỗng",
                "so_tien ≥ 0 AND so_tien IS NOT NULL", "🟢 Đạt", "07:02 hôm nay"))

    consumers = "".join(
        f'<div style="display:flex;justify-content:space-between;font-size:12.5px;padding:6px 0;'
        f'border-bottom:1px solid #eef1f5"><span>{ic} {n}</span>'
        f'<span class="muted">{o}</span></div>'
        for ic, n, o in [("📊", "Báo cáo Doanh thu ngày", "Ban Kinh doanh"),
                         ("📊", "Dashboard Đối soát", "Ban Kinh doanh"),
                         ("🗄️", "bi.doanh_thu_thang", "Đội DE"),
                         ("🤖", "Mô hình dự báo rời mạng", "Đội Data Science")])

    main = _head("Chất lượng") + f"""
<div class="tabs" style="border:none;margin:10px 0 0">
  <div class="on" style="padding-left:0">Hợp đồng dữ liệu</div>
  <div>Các phép kiểm (assertion)</div><div>Lịch sử sự cố</div></div>
<div style="display:flex;gap:20px;margin-top:16px">
  <div style="flex:1">
    <div class="card" style="padding:15px 18px;margin-bottom:14px;border-left:4px solid #F04438">
      <div style="display:flex;justify-content:space-between;align-items:center">
        <div><div style="font-size:15px;font-weight:700">📜 Hợp đồng: Đối soát giao dịch đối tác A — v2</div>
          <div class="sub" style="margin:4px 0 0">Bên cam kết: <b>Đội Data Engineering</b> ·
            Hiệu lực từ 01/06/2026 · Rà soát lại: 01/12/2026</div></div>
        <div style="text-align:right">
          <div class="chip" style="background:#ECFDF3;color:#067647;font-size:13px;padding:5px 13px">
            State: ACTIVE</div>
          <div class="muted" style="font-size:11.5px;margin-top:5px">
            4/5 phép kiểm đạt · <span style="color:#B42318">1 đang thất bại</span></div></div>
      </div></div>
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:9px">
      <div style="font-size:13.5px;font-weight:700">Các điều khoản của hợp đồng</div>
      <span class="btn">➕ Thêm điều khoản</span></div>
    <div class="card"><table class="g">
      <tr><th>Nhóm</th><th>Điều khoản</th><th>Định nghĩa kỹ thuật</th><th>Trạng thái</th><th>Kiểm lần cuối</th></tr>
      {rows}</table></div>
    <div style="margin-top:12px;font-size:12.5px;background:#FEF3F2;border:1px solid #FECDCA;
      border-radius:7px;padding:11px 14px">
      🔴 <b>Khi một phép kiểm thất bại:</b> DataHub <b>tự sinh một Sự cố (Incident)</b> gắn vào bảng,
      với nguồn sinh ra là <span class="mono">ASSERTION_FAILURE</span>, rồi gửi thông báo theo đăng ký.<br>
      ⚠️ <b>Việc chặn job hạ nguồn KHÔNG tự động.</b> Đó là cơ chế riêng tên là
      <b>Pipeline Circuit Breaking</b>, phải <b>tự tích hợp</b>: luồng Airflow/Dagster gọi API hỏi
      "bảng đầu vào có sự cố đang mở không" rồi tự quyết định dừng. Tài liệu DataHub ghi rõ khung hợp đồng
      chỉ <b>định nghĩa và theo dõi</b>, còn <b>thực thi phải tích hợp thêm</b>.</div>
  </div>
  <div style="width:290px;flex-shrink:0">
    <div class="card" style="padding:13px 15px;margin-bottom:12px">
      <div style="font-size:12px;font-weight:700;color:#5a6472;margin-bottom:6px">
        AI ĐANG PHỤ THUỘC VÀO BẢNG NÀY</div>{consumers}</div>
    <div class="card" style="padding:13px 15px">
      <div style="font-size:12px;font-weight:700;color:#5a6472;margin-bottom:8px">SỰ CỐ ĐANG MỞ</div>
      <div style="font-size:12.5px;line-height:1.85">
        <b>Incident #4821</b><br>
        Nguồn sinh ra: <span class="mono">ASSERTION_FAILURE</span> (hệ thống tự tạo)<br>
        Trạng thái: <b>INVESTIGATION</b><br>
        <span class="muted" style="font-size:11px">Chuỗi trạng thái: TRIAGE → INVESTIGATION →
        WORK_IN_PROGRESS → FIXED / NO_ACTION_REQUIRED</span><br><br>
        <span class="muted" style="font-size:11.5px">Ở màn tìm kiếm có bộ lọc
        "Has Active Incidents" để xem mọi bảng đang có sự cố.</span>
      </div></div>
  </div>
</div>"""
    return shell("DataHub — Hợp đồng dữ liệu", "demo.datahub.com/dataset/…/Quality/Data%20Contract",
                 NAVI("contract"), main, AC, "#F7FAFC",
                 note="DataHub · HỢP ĐỒNG DỮ LIỆU (Data Contract) — cam kết giữa bên sản xuất và bên dùng")


# ---------------------------------------------------------------- impact
def impact():
    def row(ic, name, kind, level, owner, usage, risk):
        return (f'<tr><td>{ic} <b>{name}</b></td><td>{kind}</td><td class="mono">{level}</td>'
                f'<td>{owner}</td><td>{usage}</td><td>{risk}</td></tr>')

    rows = (row("🗄️", "bi.doanh_thu_thang", "Tập dữ liệu", "1", "Đội DE", "Kinh doanh", "Hive") +
            row("📊", "Báo cáo Doanh thu ngày", "Báo cáo", "2", "Ban Kinh doanh", "Kinh doanh", "PowerBI") +
            row("📊", "Dashboard Đối soát", "Báo cáo", "2", "Ban Kinh doanh", "Kinh doanh", "PowerBI") +
            row("🤖", "Mô hình dự báo rời mạng", "Mô hình", "2", "Data Science", "Kỹ thuật", "MLflow") +
            row("🗄️", "mart.kpi_kinh_doanh", "Tập dữ liệu", "3", "Đội DE", "Kinh doanh", "Hive") +
            row("📊", "BC Tổng Giám đốc hằng tháng", "Báo cáo", "3", "Văn phòng", "Kinh doanh", "PowerBI") +
            row("📄", "File xuất cho đối tác A", "Tập dữ liệu", "3", "Ban Kinh doanh", "Kinh doanh", "S3"))

    main = _head("Nguồn gốc") + f"""
<div style="display:flex;gap:10px;margin:16px 0 14px">
  <span class="btn">📉 Phân tích ảnh hưởng hạ nguồn</span>
  <span class="btn ghost">Số cấp phụ thuộc: 3 ▾</span>
  <span class="btn ghost">Loại: Tất cả ▾</span>
  <span class="btn ghost">Người phụ trách ▾</span><span class="btn ghost">Nền tảng ▾</span>
  <span class="btn ghost">⬇️ Xuất danh sách (CSV)</span>
</div>
<div style="background:#FFFAEB;border:1px solid #FEDF89;border-radius:8px;padding:13px 16px;margin-bottom:16px">
  <div style="font-size:13.5px"><b>Câu hỏi:</b> "Nếu tôi đổi kiểu cột
    <span class="mono">so_tien</span> từ chuỗi sang số thì cái gì gãy?"</div>
  <div style="font-size:13.5px;margin-top:5px"><b>Trả lời của hệ thống:</b>
    <b style="color:#B42318">7 tài sản</b> ở 3 cấp hạ nguồn bị ảnh hưởng,
    thuộc <b>4 đơn vị</b>. Bấm <b>Xuất CSV</b> để tải danh sách — file kèm sẵn
    <b>người phụ trách, miền dữ liệu, nhãn, thuật ngữ</b> và link quay lại từng tài sản.<br>
    <span style="color:#B54708">⚠️ Mặc định hệ thống chỉ tra <b>1 cấp phụ thuộc</b> cho nhẹ máy —
    muốn xem sâu hơn phải tự chỉnh.</span></div>
</div>
<div class="card"><table class="g">
  <tr><th>Tài sản bị ảnh hưởng</th><th>Loại</th><th>Cấp</th><th>Đơn vị phụ trách</th>
    <th>Miền dữ liệu</th><th>Nền tảng</th></tr>{rows}</table></div>
<div style="display:flex;gap:14px;margin-top:16px">
  <div class="card" style="flex:1;padding:13px 15px">
    <div class="muted" style="font-size:11px">TỔNG TÀI SẢN HẠ NGUỒN</div>
    <div style="font-size:26px;font-weight:800">7</div></div>
  <div class="card" style="flex:1;padding:13px 15px">
    <div class="muted" style="font-size:11px">SỐ CẤP PHỤ THUỘC ĐÃ TRA</div>
    <div style="font-size:26px;font-weight:800">3</div></div>
  <div class="card" style="flex:1;padding:13px 15px">
    <div class="muted" style="font-size:11px">SỐ ĐƠN VỊ CẦN THÔNG BÁO</div>
    <div style="font-size:26px;font-weight:800">4</div></div>
  <div class="card" style="flex:2;padding:13px 15px;background:#F0F9FF">
    <div class="muted" style="font-size:11px">GHI CHÚ</div>
    <div style="font-size:12.5px;line-height:1.7;margin-top:4px">
      Phần "gợi ý hành động" <b>không phải tính năng của DataHub</b> — đó là quy trình
      <b>ta tự đặt ra</b> dựa trên danh sách này.</div></div>
</div>"""
    return shell("DataHub — Phân tích ảnh hưởng", "demo.datahub.com/dataset/…/Lineage/Impact%20Analysis",
                 NAVI("lineage"), main, AC, "#F7FAFC",
                 note="DataHub · PHÂN TÍCH ẢNH HƯỞNG (Impact Analysis) — trả lời 'đổi cái này thì gãy cái gì'")


SCREENS = {"dh-01-contract": contract, "dh-02-impact": impact}
