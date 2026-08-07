# -*- coding: utf-8 -*-
"""Màn hình Soda Cloud — luật chất lượng viết bằng ngôn ngữ gần tự nhiên."""
from common import shell, nav

AC = "#6C3DF4"
NAVI = lambda act: nav("Soda", AC, [
    ("🏠", "Trang chủ", act == "home"),
    ("✅", "Luật kiểm tra", act == "checks"),
    ("🗂️", "Tập dữ liệu", act == "datasets"),
    ("🤝", "Thoả thuận chất lượng", act == "agree"),
    ("🚨", "Sự cố", act == "incident"),
    ("🔔", "Quy tắc thông báo", act == "notify"),
    ("🔌", "Nguồn dữ liệu", act == "source"),
], AC)


def checks():
    def spark(pattern):
        return "".join(f'<div style="width:5px;height:18px;background:{c};border-radius:1px"></div>'
                       for c in pattern)

    G, R, O = "#12B76A", "#F04438", "#F79009"

    def row(name, ds, col, st, val, hist):
        c = {"🟢": "#067647", "🔴": "#B42318", "🟠": "#B54708"}[st[0]]
        return (f'<tr><td><b>{name}</b></td><td class="mono" style="font-size:11.5px">{ds}</td>'
                f'<td class="mono">{col}</td>'
                f'<td style="color:{c};font-weight:700">{st}</td><td>{val}</td>'
                f'<td><div style="display:flex;gap:2px">{spark(hist)}</div></td></tr>')

    rows = (row("row_count between 8000000 and 20000000", "bi.doi_soat_giao_dich_A", "—",
                "🟢 Đạt", "12.480.331", [G] * 14) +
            row("missing_count(so_dien_thoai) = 0", "bi.doi_soat_giao_dich_A", "so_dien_thoai",
                "🟢 Đạt", "0", [G] * 14) +
            row("invalid_percent(so_dien_thoai) < 0.5%", "bi.doi_soat_giao_dich_A", "so_dien_thoai",
                "🔴 Thất bại", "0,96%", [G] * 11 + [R, R, R]) +
            row("duplicate_count(giao_dich_id) = 0", "bi.doi_soat_giao_dich_A", "giao_dich_id",
                "🟢 Đạt", "0", [G] * 14) +
            row("freshness(ngay_ghi_nhan) < 1d", "bi.doi_soat_giao_dich_A", "ngay_ghi_nhan",
                "🟠 Cảnh báo", "26 giờ", [G] * 12 + [O, O]) +
            row("values in (doi_tac) must exist in dm.doi_tac (doi_tac_id)", "bi.doi_soat_giao_dich_A",
                "doi_tac", "🟢 Đạt", "0 mã lạ", [G] * 14) +
            row("anomaly detection for row_count", "dwh.thue_bao_ngay", "—",
                "🟢 Đạt", "trong dải học được", [G] * 9 + [R] + [G] * 4) +
            row("schema changes must not drop columns", "bi.doanh_thu_thang", "—",
                "🟠 Cảnh báo", "thêm 1 cột mới", [G] * 13 + [O]))

    main = f"""
<h1 class="t">✅ Bảng điều khiển luật kiểm tra</h1>
<div class="sub">Toàn bộ luật chất lượng đang chạy trên 3 nguồn dữ liệu · Lần quét gần nhất 06:12 hôm nay</div>
<div style="display:flex;gap:14px;margin:16px 0 14px">
  <div class="card" style="flex:1;padding:13px 15px"><div class="muted" style="font-size:11px">TỔNG SỐ LUẬT</div>
    <div style="font-size:26px;font-weight:800">148</div></div>
  <div class="card" style="flex:1;padding:13px 15px"><div class="muted" style="font-size:11px">ĐẠT</div>
    <div style="font-size:26px;font-weight:800;color:#067647">139</div></div>
  <div class="card" style="flex:1;padding:13px 15px"><div class="muted" style="font-size:11px">CẢNH BÁO</div>
    <div style="font-size:26px;font-weight:800;color:#B54708">6</div></div>
  <div class="card" style="flex:1;padding:13px 15px"><div class="muted" style="font-size:11px">THẤT BẠI</div>
    <div style="font-size:26px;font-weight:800;color:#B42318">3</div></div>
  <div class="card" style="flex:2;padding:13px 15px"><div class="muted" style="font-size:11px">
    TẬP DỮ LIỆU ĐANG ĐƯỢC KIỂM</div>
    <div style="font-size:26px;font-weight:800">64<span style="font-size:14px"> tập dữ liệu</span></div>
    <div class="muted" style="font-size:11.5px">gom theo nguồn dữ liệu đã kết nối</div></div>
</div>
<div style="display:flex;gap:10px;margin-bottom:12px">
  <span class="btn ghost">Nguồn: tất cả ▾</span><span class="btn ghost">Trạng thái: tất cả ▾</span>
  <span class="btn ghost">Chiều chất lượng: tất cả ▾</span>
  <div style="flex:1"></div><span class="btn">➕ Tạo luật mới</span></div>
<div class="card"><table class="g">
  <tr><th>Luật kiểm tra (viết bằng SodaCL)</th><th>Tập dữ liệu</th><th>Cột</th>
    <th>Kết quả</th><th>Giá trị đo được</th><th>14 lần quét gần nhất</th></tr>{rows}</table></div>
<div style="margin-top:12px;font-size:12.5px;background:#F5F1FF;border:1px solid #DDD0FF;
  border-radius:7px;padding:11px 14px">
  💡 <b>Điểm đáng chú ý cho SQLWF:</b> luật viết bằng câu gần ngôn ngữ tự nhiên —
  <span class="mono">invalid_percent(so_dien_thoai) &lt; 0.5%</span> —
  người làm nghiệp vụ <b>đọc hiểu và tự viết được</b>, không cần lập trình viên.<br>
  ⚠️ Chỉ số "bao nhiêu % bảng đã được kiểm" <b>không có sẵn</b> trong Soda —
  đó là chỉ số <b>ta tự đề xuất thêm</b> cho SQLWF.</div>"""
    return shell("Soda Cloud — Luật kiểm tra", "cloud.soda.io/checks",
                 NAVI("checks"), main, AC, "#FAF8FF",
                 note="Soda Cloud · BẢNG ĐIỀU KHIỂN LUẬT CHẤT LƯỢNG")


def agreement():
    code = """<span style="color:#7C8798"># Luật áp dụng cho bảng đối soát giao dịch đối tác A</span>
<span style="color:#C084FC">checks for</span> bi.doi_soat_giao_dich_A:

  <span style="color:#7C8798"># 1 — Đủ dữ liệu</span>
  - <span style="color:#7DD3FC">row_count</span> between 8000000 and 20000000

  <span style="color:#7C8798"># 2 — Không rỗng ở cột bắt buộc</span>
  - <span style="color:#7DD3FC">missing_count</span>(so_dien_thoai) = 0
  - <span style="color:#7DD3FC">missing_percent</span>(so_tien) &lt; 0.1%

  <span style="color:#7C8798"># 3 — Đúng định dạng</span>
  - <span style="color:#7DD3FC">invalid_percent</span>(so_dien_thoai) &lt; 0.5%:
      valid regex: <span style="color:#FCD34D">'^(84|0)(3|5|7|8|9)[0-9]{8}$'</span>

  <span style="color:#7C8798"># 4 — Không trùng khoá</span>
  - <span style="color:#7DD3FC">duplicate_count</span>(giao_dich_id) = 0

  <span style="color:#7C8798"># 5 — Giá trị nằm trong danh mục</span>
  - <span style="color:#7DD3FC">invalid_count</span>(trang_thai) = 0:
      valid values: [KHOP, LECH, CHO]

  <span style="color:#7C8798"># 6 — Tham chiếu sang bảng danh mục</span>
  - <span style="color:#7DD3FC">values</span> in (doi_tac) must exist in dm.doi_tac (doi_tac_id)

  <span style="color:#7C8798"># 7 — Dữ liệu phải mới</span>
  - <span style="color:#7DD3FC">freshness</span>(ngay_ghi_nhan) &lt; 24h

  <span style="color:#7C8798"># 8 — Tự học ngưỡng, không cần khai tay</span>
  - <span style="color:#7DD3FC">anomaly detection</span> for row_count

  <span style="color:#7C8798"># 9 — Luật nghiệp vụ tự viết bằng SQL</span>
  - <span style="color:#7DD3FC">tong_tien_khop_nguon</span> = 0:
      <span style="color:#C084FC">tong_tien_khop_nguon query</span>: |
        SELECT ABS(SUM(a.so_tien) - SUM(b.amount))
        FROM bi.doi_soat_giao_dich_A a, raw.gd_doi_tac_A b"""

    def step(n, label, state):
        c = {"done": ("#12B76A", "#fff"), "now": (AC, "#fff"), "next": ("#E4E7EC", "#98A2B3")}[state]
        return (f'<div style="display:flex;align-items:center;gap:8px">'
                f'<div style="width:24px;height:24px;border-radius:50%;background:{c[0]};color:{c[1]};'
                f'display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700">'
                f'{"✓" if state == "done" else n}</div>'
                f'<span style="font-size:12.5px;font-weight:{700 if state == "now" else 400}">{label}</span></div>')

    main = f"""
<div class="crumb">Thoả thuận chất lượng › Tạo mới</div>
<h1 class="t">🤝 Thoả thuận chất lượng dữ liệu — Đối soát đối tác A</h1>
<div class="sub">Văn bản cam kết giữa <b>bên tạo dữ liệu</b> và <b>bên dùng dữ liệu</b> về mức chất lượng tối thiểu</div>
<div style="display:flex;gap:30px;margin:18px 0;padding:14px 18px;background:#F9FAFB;
  border:1px solid #EAECF0;border-radius:8px">
  {step(1, "Đặt tên & chọn nguồn", "done")}<div style="width:26px;height:1px;background:#E4E7EC;margin-top:12px"></div>
  {step(2, "Viết luật kiểm tra", "now")}<div style="width:26px;height:1px;background:#E4E7EC;margin-top:12px"></div>
  {step(3, "Đặt lịch quét", "next")}<div style="width:26px;height:1px;background:#E4E7EC;margin-top:12px"></div>
  {step(4, "Người nhận thông báo", "next")}<div style="width:26px;height:1px;background:#E4E7EC;margin-top:12px"></div>
  {step(5, "Người phê duyệt", "next")}
</div>
<div style="display:flex;gap:20px">
  <div style="flex:1.5">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
      <div style="font-size:13px;font-weight:700">Trình soạn luật (SodaCL)</div>
      <div style="display:flex;gap:8px"><span class="btn ghost">📋 Chèn từ mẫu có sẵn</span>
        <span class="btn ghost">▶️ Chạy thử</span></div></div>
    <div style="background:#0F172A;border-radius:9px;padding:16px 18px;font-family:Consolas,monospace;
      font-size:12.5px;line-height:1.72;color:#E2E8F0;white-space:pre">{code}</div>
  </div>
  <div style="width:340px;flex-shrink:0">
    <div class="card" style="padding:14px 16px;margin-bottom:12px">
      <div style="font-size:12px;font-weight:700;color:#5a6472;margin-bottom:9px">▶️ KẾT QUẢ CHẠY THỬ</div>
      <table class="g" style="font-size:12px">
        <tr><td>row_count</td><td style="color:#067647;font-weight:700">Đạt</td></tr>
        <tr><td>missing_count(so_dien_thoai)</td><td style="color:#067647;font-weight:700">Đạt</td></tr>
        <tr><td>invalid_percent(so_dien_thoai)</td><td style="color:#B42318;font-weight:700">0,96% ✗</td></tr>
        <tr><td>duplicate_count(giao_dich_id)</td><td style="color:#067647;font-weight:700">Đạt</td></tr>
        <tr><td>trang_thai in danh mục</td><td style="color:#067647;font-weight:700">Đạt</td></tr>
        <tr><td>doi_tac tồn tại ở dm.doi_tac</td><td style="color:#067647;font-weight:700">Đạt</td></tr>
        <tr><td>freshness(ngay_ghi_nhan)</td><td style="color:#B54708;font-weight:700">26h ⚠</td></tr>
        <tr><td>anomaly detection row_count</td><td style="color:#067647;font-weight:700">Đạt</td></tr>
        <tr><td>tong_tien_khop_nguon</td><td style="color:#067647;font-weight:700">Đạt</td></tr>
      </table>
      <div style="margin-top:10px;font-size:12px" class="muted">Thời gian quét: 47 giây ·
        Soda chỉ đọc, <b>không sao chép dữ liệu ra ngoài</b></div></div>
    <div class="card" style="padding:14px 16px;background:#F5F1FF">
      <div style="font-size:12px;font-weight:700;margin-bottom:7px">🎯 9 LUẬT TRÊN PHỦ ĐỦ 6 CHIỀU CHẤT LƯỢNG</div>
      <div style="font-size:12.5px;line-height:1.85">
        Đầy đủ (completeness) — luật 1, 2<br>
        Hợp lệ (validity) — luật 3, 5<br>
        Duy nhất (uniqueness) — luật 4<br>
        Nhất quán (consistency) — luật 6, 9<br>
        Kịp thời (timeliness) — luật 7<br>
        Chính xác (accuracy) — luật 8, 9</div></div>
  </div>
</div>"""
    return shell("Soda Cloud — Thoả thuận chất lượng", "cloud.soda.io/agreements/new",
                 NAVI("agree"), main, AC, "#FAF8FF",
                 note="Soda Cloud · TẠO THOẢ THUẬN CHẤT LƯỢNG — bước 2: viết luật")


SCREENS = {"soda-01-checks": checks, "soda-02-agreement": agreement}
