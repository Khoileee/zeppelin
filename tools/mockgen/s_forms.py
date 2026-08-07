# -*- coding: utf-8 -*-
"""Các màn FORM THÊM MỚI / XEM CHI TIẾT — phần quan trọng nhất cho BA."""
from common import shell, nav

OM = "#7147E8"
DH = "#1B75BC"
RG = "#0F7B6C"

NAV_OM = lambda act: nav("OpenMetadata", OM, [
    ("🏠", "Trang chủ", act == "home"),
    ("🔍", "Khám phá dữ liệu", act == "explore"),
    ("📊", "Chất lượng dữ liệu", act == "quality"),
    ("🔗", "Nguồn gốc dữ liệu", act == "lineage"),
    ("📖", "Từ điển nghiệp vụ", act == "glossary"),
    ("🏷️", "Phân loại / Nhãn", act == "tags"),
    ("🧩", "Miền dữ liệu", act == "domain"),
    ("💡", "Thông tin chi tiết", act == "insight"),
    ("⚙️", "Cài đặt", act == "settings"),
], OM)

NAV_DH = lambda act: nav("DataHub", DH, [
    ("🏠", "Trang chủ", act == "home"),
    ("🔍", "Tìm kiếm", act == "search"),
    ("🧊", "Miền dữ liệu", act == "domain"),
    ("📦", "Sản phẩm dữ liệu", act == "product"),
    ("📖", "Từ điển nghiệp vụ", act == "glossary"),
    ("📜", "Hợp đồng dữ liệu", act == "contract"),
    ("🔗", "Nguồn gốc & Ảnh hưởng", act == "lineage"),
    ("⚙️", "Quản trị", act == "admin"),
], DH)

NAV_RG = lambda act: nav("Ranger", RG, [
    ("🛡️", "Quản lý dịch vụ", act == "svc"),
    ("📋", "Chính sách truy cập", act == "access"),
    ("🙈", "Che dữ liệu (Masking)", act == "mask"),
    ("🔎", "Lọc theo dòng", act == "row"),
    ("🏷️", "Chính sách theo nhãn", act == "tag"),
    ("📜", "Nhật ký kiểm toán", act == "audit"),
    ("👥", "Người dùng / Nhóm", act == "users"),
], RG)


def fld(label, value, req=False, hint="", mono=False, tall=False, ph=False):
    star = '<span style="color:#D92D20">*</span> ' if req else ""
    return f"""<div style="margin-bottom:13px">
  <div style="font-size:12px;font-weight:600;color:#344054;margin-bottom:5px">{star}{label}</div>
  <div style="border:1px solid #cfd6e0;border-radius:6px;padding:{'10px 11px;min-height:56px' if tall else '8px 11px'};
    font-size:13px;background:#fff;{'font-family:Consolas,monospace;' if mono else ''}
    {'color:#98A2B3' if ph else ''}">{value}</div>
  {f'<div class="muted" style="font-size:11.5px;margin-top:4px">{hint}</div>' if hint else ''}</div>"""


def chips(items, bg="#F0F4FF", fg="#3538CD"):
    return "".join(f'<span class="chip" style="background:{bg};color:{fg};margin-right:5px">{i} ✕</span>'
                   for i in items)


def steps(items, accent):
    out = []
    for i, (label, state) in enumerate(items, 1):
        c = {"done": ("#12B76A", "#fff"), "now": (accent, "#fff"), "next": ("#E4E7EC", "#98A2B3")}[state]
        out.append(f'<div style="display:flex;align-items:center;gap:8px">'
                   f'<div style="width:24px;height:24px;border-radius:50%;background:{c[0]};color:{c[1]};'
                   f'display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700">'
                   f'{"✓" if state == "done" else i}</div>'
                   f'<span style="font-size:12.5px;font-weight:{700 if state == "now" else 400};'
                   f'color:{"#101828" if state != "next" else "#98A2B3"}">{label}</span></div>')
        if i < len(items):
            out.append('<div style="width:24px;height:1px;background:#E4E7EC;margin-top:12px"></div>')
    return ('<div style="display:flex;gap:14px;margin:16px 0 20px;padding:13px 18px;background:#F9FAFB;'
            'border:1px solid #EAECF0;border-radius:8px">' + "".join(out) + "</div>")


# ============================================================ 1. Khai báo thông tin bảng
def edit_table():
    main = f"""
<div class="crumb">Khám phá dữ liệu › hive_prod › bi › doi_soat_giao_dich_A › Sửa thông tin</div>
<h1 class="t">✏️ Khai báo thông tin bảng</h1>
<div class="sub">Màn này để <b>gán trách nhiệm và ý nghĩa nghiệp vụ cho một bảng</b> — ai chịu trách nhiệm,
  bảng dùng vào việc gì, quan trọng đến mức nào, có chứa dữ liệu nhạy cảm không.</div>
<div style="display:flex;gap:26px;margin-top:16px">
  <div style="width:470px;flex-shrink:0">
    <div style="font-size:13px;font-weight:700;margin-bottom:11px;padding-bottom:7px;
      border-bottom:2px solid #7147E8;display:inline-block">① THÔNG TIN NHẬN DẠNG</div>
    {fld("Tên bảng", "bi.doi_soat_giao_dich_A &nbsp;<span style='color:#98A2B3'>(không sửa được)</span>", mono=True)}
    {fld("Tên hiển thị cho người dùng nghiệp vụ", "Đối soát giao dịch — Đối tác A", True,
         "Tên tiếng Việt để người không biết kỹ thuật vẫn tìm được")}
    {fld("Mô tả", "Bảng đối soát giao dịch với đối tác A. Nguồn: file đối tác gửi hằng ngày qua SFTP. "
                  "Chốt số liệu lúc 06:00. Dùng cho báo cáo doanh thu ngày và dashboard đối soát.",
         True, "Trả lời 3 câu: bảng này là gì · lấy từ đâu · dùng để làm gì", tall=True)}
    <div style="font-size:13px;font-weight:700;margin:20px 0 11px;padding-bottom:7px;
      border-bottom:2px solid #7147E8;display:inline-block">② TRÁCH NHIỆM</div>
    {fld("BDA phụ trách", "👤 Nguyễn Thị Phương — Phòng Phân tích Dữ liệu ▾", True,
         "Người trả lời câu hỏi <b>nghiệp vụ</b> về bảng này")}
    {fld("DE phụ trách", "👤 Trần Văn Hùng — Đội Data Engineering ▾", True,
         "Người xử lý khi bảng lỗi / job hỏng")}
    {fld("Miền dữ liệu", "Kinh doanh ▾", True)}
  </div>
  <div style="width:470px;flex-shrink:0">
    <div style="font-size:13px;font-weight:700;margin-bottom:11px;padding-bottom:7px;
      border-bottom:2px solid #7147E8;display:inline-block">③ PHÂN LOẠI & MỨC ĐỘ QUAN TRỌNG</div>
    {fld("Mức độ quan trọng (Tier)",
         "🏅 Tier 1 — Dữ liệu vàng, phục vụ báo cáo lãnh đạo ▾", True,
         "Tier 1 = hỏng là ảnh hưởng báo cáo lãnh đạo · Tier 2 = ảnh hưởng nghiệp vụ · Tier 3 = nội bộ / thử nghiệm")}
    {fld("Nhãn phân loại của bảng",
         chips(["PII.Nhạy cảm"], "#FDE8E8", "#B42318") + chips(["TaiChinh.DoanhThu"], "#FEF3F2", "#B42318")
         + '<span class="muted">+ Thêm nhãn</span>')}
    {fld("Thuật ngữ nghiệp vụ liên quan",
         chips(["Doanh thu ghi nhận", "Đối soát"]) + '<span class="muted">+ Gắn thuật ngữ</span>')}
    <div style="font-size:13px;font-weight:700;margin:20px 0 11px;padding-bottom:7px;
      border-bottom:2px solid #7147E8;display:inline-block">④ CAM KẾT VẬN HÀNH</div>
    {fld("Chu kỳ cập nhật", "Hằng ngày — trước 07:00 ▾", True,
         "Dùng để hệ thống tự tính 'độ tươi' và cảnh báo khi trễ")}
    {fld("Thời gian lưu trữ", "36 tháng ▾")}
    {fld("Được phép chia sẻ ra ngoài đơn vị?", "Không — chỉ nội bộ Ban Kinh doanh và Ban Tài chính ▾")}
    <div style="background:#F4F0FF;border:1px solid #D9CCFF;border-radius:7px;padding:11px 13px;
      font-size:12.5px;margin-top:6px">
      💡 Ô có dấu <span style="color:#D92D20">*</span> là bắt buộc. Bảng chưa khai đủ sẽ bị đánh dấu
      <b>"Chưa hoàn thiện hồ sơ"</b> trong màn khám phá và bị trừ điểm ở báo cáo quản trị dữ liệu hằng tháng.</div>
    <div style="display:flex;gap:10px;margin-top:18px">
      <span class="btn">💾 Lưu</span><span class="btn ghost">Lưu & khai bảng tiếp theo</span>
      <span class="btn ghost">Huỷ</span></div>
  </div>
</div>"""
    return shell("OpenMetadata — Khai báo thông tin bảng",
                 "sandbox.open-metadata.org/table/…/edit", NAV_OM("explore"), main, OM, "#FAFAFE",
                 note="OpenMetadata · FORM KHAI BÁO THÔNG TIN BẢNG — 4 nhóm trường")


# ============================================================ 2. Gắn nhãn cho cột
def tag_column():
    tree = "".join(
        f'<div style="padding:6px 10px;font-size:12.5px;border-radius:6px;margin-bottom:2px;'
        f'{"background:#F4F0FF;font-weight:700;color:#7147E8" if on else ""}">{ind}{t}'
        f'{f"<span class=muted style=float:right>{c}</span>" if c else ""}</div>'
        for ind, t, c, on in [
            ("", "🗂️ PII — Thông tin cá nhân", "", False),
            ("&nbsp;&nbsp;", "🏷️ PII.SoDienThoai", "12 cột", True),
            ("&nbsp;&nbsp;", "🏷️ PII.CCCD", "4 cột", False),
            ("&nbsp;&nbsp;", "🏷️ PII.DiaChi", "9 cột", False),
            ("&nbsp;&nbsp;", "🏷️ PII.HoTen", "15 cột", False),
            ("", "🗂️ TaiChinh — Dữ liệu tài chính", "", False),
            ("&nbsp;&nbsp;", "🏷️ TaiChinh.DoanhThu", "18 cột", False),
            ("&nbsp;&nbsp;", "🏷️ TaiChinh.ChiPhi", "7 cột", False),
            ("", "🗂️ NoiBo — Dữ liệu nội bộ", "", False),
        ])

    main = f"""
<div class="crumb">bi.doi_soat_giao_dich_A › Cấu trúc bảng › Cột <b>so_dien_thoai</b></div>
<h1 class="t">🏷️ Gắn nhãn phân loại cho cột</h1>
<div class="sub">Màn này để <b>đánh dấu cột nào chứa dữ liệu nhạy cảm</b>.
  Gắn nhãn một lần ở đây, mọi chính sách bảo mật gắn với nhãn đó sẽ <b>tự động áp lên cột</b> —
  không phải khai lại ở màn phân quyền.</div>
<div style="display:flex;gap:22px;margin-top:18px">
  <div style="width:340px;flex-shrink:0">
    <div style="border:1px solid #d5dae2;border-radius:8px;padding:9px 12px;font-size:13px;margin-bottom:12px">
      🔍 <span class="muted">Tìm nhãn…</span></div>
    <div style="font-size:12px;font-weight:700;color:#5a6472;margin-bottom:7px">CÂY NHÃN PHÂN LOẠI</div>
    <div class="card" style="padding:8px">{tree}</div>
  </div>
  <div style="flex:1">
    <div class="card" style="padding:16px 18px;margin-bottom:14px">
      <div style="font-size:12px;font-weight:700;color:#5a6472;margin-bottom:9px">CỘT ĐANG GẮN</div>
      <div style="font-size:15px;font-weight:700" class="mono">so_dien_thoai</div>
      <div class="muted" style="font-size:12.5px;margin:3px 0 10px">
        Kiểu STRING · Bảng bi.doi_soat_giao_dich_A · 12.480.331 giá trị</div>
      <div style="font-size:12px;font-weight:600;color:#344054;margin-bottom:6px">Nhãn đã chọn</div>
      <div style="border:1px solid #cfd6e0;border-radius:6px;padding:9px 11px;min-height:42px">
        {chips(["PII.SoDienThoai"], "#FDE8E8", "#B42318")}</div>
      <div style="font-size:12px;font-weight:600;color:#344054;margin:13px 0 6px">Mức độ nhạy cảm</div>
      <div style="border:1px solid #cfd6e0;border-radius:6px;padding:8px 11px;font-size:13px">
        🔴 Cao — không được hiển thị nguyên bản cho người ngoài đơn vị ▾</div>
      <div style="display:flex;gap:10px;margin-top:16px">
        <span class="btn">💾 Lưu nhãn</span><span class="btn ghost">Huỷ</span></div>
    </div>
    <div style="background:#FFFAEB;border:1px solid #FEDF89;border-radius:8px;padding:13px 16px">
      <div style="font-size:12.5px;font-weight:700;margin-bottom:7px">
        ⚡ KHI LƯU NHÃN NÀY, HỆ THỐNG TỰ ÁP 3 CHÍNH SÁCH — KHÔNG CẦN KHAI THÊM</div>
      <div style="font-size:12.5px;line-height:1.9">
        1. Nhóm <b>ban_kinh_doanh</b> → chỉ nhìn thấy <span class="mono">xxxxxx5678</span><br>
        2. Nhóm <b>ctv_thue_ngoai</b> → chỉ nhìn thấy chuỗi băm <span class="mono">a91f3e7b…</span><br>
        3. Mọi truy vấn vào cột này đều bị <b>ghi nhật ký kiểm toán</b></div>
    </div>
  </div>
  <div style="width:330px;flex-shrink:0">
    <div class="card" style="padding:14px 16px;margin-bottom:12px">
      <div style="font-size:12px;font-weight:700;color:#5a6472;margin-bottom:9px">
        🤖 HỆ THỐNG ĐỀ XUẤT NHÃN</div>
      <div style="font-size:12.5px;line-height:1.7;margin-bottom:10px">
        Bộ dò đã quét 1.000 dòng mẫu và tên cột:</div>
      <div style="background:#ECFDF3;border:1px solid #A6F4C5;border-radius:7px;padding:10px 12px;font-size:12.5px">
        <b>PII.SoDienThoai</b> — độ tin cậy <b>98%</b><br>
        <span class="muted">Căn cứ: 98,2% giá trị khớp mẫu đầu số di động Việt Nam; tên cột chứa
        "so_dien_thoai"</span>
        <div style="margin-top:9px;display:flex;gap:7px">
          <span class="btn" style="padding:5px 11px">✓ Chấp nhận</span>
          <span class="btn ghost" style="padding:5px 11px">✕ Từ chối</span></div></div>
      <div class="muted" style="font-size:11.5px;margin-top:9px">
        Máy chỉ <b>gợi ý</b> — người quản trị dữ liệu là người quyết định cuối cùng.</div>
    </div>
    <div class="card" style="padding:14px 16px">
      <div style="font-size:12px;font-weight:700;color:#5a6472;margin-bottom:8px">
        📋 12 CỘT KHÁC ĐANG MANG NHÃN NÀY</div>
      <div class="mono" style="font-size:11.5px;line-height:1.85;color:#48505e">
        raw.gd_doi_tac_A.msisdn<br>dwh.thue_bao_ngay.so_tb<br>crm.khach_hang.dien_thoai<br>
        crm.lien_he.sdt<br><span class="muted">… và 8 cột khác</span></div>
    </div>
  </div>
</div>"""
    return shell("OpenMetadata — Gắn nhãn cho cột",
                 "sandbox.open-metadata.org/table/…/columns/so_dien_thoai/tags",
                 NAV_OM("tags"), main, OM, "#FAFAFE",
                 note="OpenMetadata · FORM GẮN NHÃN PHÂN LOẠI CHO MỘT CỘT")


# ============================================================ 3. Chi tiết luật thất bại
def test_detail():
    vals = [0.02, 0.03, 0.02, 0.04, 0.03, 0.02, 0.03, 0.02, 0.05, 0.03,
            0.02, 0.04, 0.03, 0.02, 0.03, 0.02, 0.04, 0.03, 0.02, 0.03,
            0.02, 0.03, 0.04, 0.61, 0.78, 0.84, 0.91, 0.96]
    W, H = 940, 190
    n = len(vals)
    sx = lambda i: 8 + i * (W - 16) / (n - 1)
    sy = lambda v: H - (v / 1.1) * H
    line = "M " + " L ".join(f"{sx(i):.1f},{sy(v):.1f}" for i, v in enumerate(vals))
    dots = "".join(f'<circle cx="{sx(i):.1f}" cy="{sy(v):.1f}" r="{4.5 if v > 0.5 else 2.4}" '
                   f'fill="{"#F04438" if v > 0.5 else "#12B76A"}"/>' for i, v in enumerate(vals))
    thr = sy(0.5)
    chart = f"""<svg width="{W}" height="{H + 22}" viewBox="0 0 {W} {H + 22}">
  <line x1="0" y1="{thr:.1f}" x2="{W}" y2="{thr:.1f}" stroke="#F04438" stroke-width="1.5"
        stroke-dasharray="6 4"/>
  <text x="{W - 190}" y="{thr - 7:.1f}" fill="#B42318" font-size="11.5" font-family="Segoe UI"
        font-weight="600">Ngưỡng cho phép 0,5%</text>
  <path d="{line}" fill="none" stroke="#667085" stroke-width="1.8"/>{dots}
  <text x="4" y="{H + 17}" fill="#98A2B3" font-size="11" font-family="Segoe UI">07/07</text>
  <text x="{W - 190}" y="{H + 17}" fill="#B42318" font-size="11" font-family="Segoe UI"
        font-weight="600">31/07 — bắt đầu vượt ngưỡng</text>
</svg>"""

    bad = "".join(
        f'<tr><td class="mono">{gid}</td><td class="mono" style="color:#B42318"><b>{v}</b></td>'
        f'<td>{why}</td><td class="mono">{d}</td><td>{p}</td></tr>'
        for gid, v, why, d, p in [
            ("GD20260803001204", "+84-912-345-678", "Có dấu gạch nối và dấu +", "2026-08-03", "Đối tác A"),
            ("GD20260803001881", "0912345", "Chỉ có 7 chữ số", "2026-08-03", "Đối tác A"),
            ("GD20260803002140", "N/A", "Không phải số", "2026-08-03", "Đối tác A"),
            ("GD20260803002377", "0212345678", "Đầu số cố định, không phải di động", "2026-08-03", "Đối tác A"),
            ("GD20260803002903", "(trống)", "Giá trị rỗng", "2026-08-03", "Đối tác A"),
        ])

    main = f"""
<div class="crumb">Chất lượng dữ liệu › bi.doi_soat_giao_dich_A › Chi tiết luật kiểm tra</div>
<h1 class="t">🔴 so_dien_thoai đúng định dạng đầu số VN
  <span class="chip" style="background:#FEF3F2;color:#B42318">Thất bại 5 ngày liên tiếp</span></h1>
<div class="sub">Màn này để <b>xem một luật đang hỏng ra sao và hỏng từ bao giờ</b> —
  kèm danh sách dòng dữ liệu sai cụ thể để gửi cho bên tạo dữ liệu đi sửa.</div>
<div style="display:flex;gap:14px;margin:16px 0 14px">
  <div class="card" style="flex:1;padding:12px 15px"><div class="muted" style="font-size:11px">TỈ LỆ SAI HÔM NAY</div>
    <div style="font-size:24px;font-weight:800;color:#B42318">0,96%</div>
    <div style="font-size:11.5px" class="muted">ngưỡng cho phép 0,5%</div></div>
  <div class="card" style="flex:1;padding:12px 15px"><div class="muted" style="font-size:11px">SỐ DÒNG SAI</div>
    <div style="font-size:24px;font-weight:800">1.204</div>
    <div style="font-size:11.5px" class="muted">trên 12.480.331 dòng</div></div>
  <div class="card" style="flex:1;padding:12px 15px"><div class="muted" style="font-size:11px">BẮT ĐẦU HỎNG</div>
    <div style="font-size:24px;font-weight:800">31/07</div>
    <div style="font-size:11.5px" class="muted">5 ngày trước</div></div>
  <div class="card" style="flex:1;padding:12px 15px"><div class="muted" style="font-size:11px">NGUỒN GÂY LỖI</div>
    <div style="font-size:18px;font-weight:800;margin-top:5px">Đối tác A</div>
    <div style="font-size:11.5px" class="muted">100% dòng sai đến từ nguồn này</div></div>
  <div class="card" style="flex:1.3;padding:12px 15px;background:#FEF3F2;border-color:#FECDCA">
    <div class="muted" style="font-size:11px">TRẠNG THÁI XỬ LÝ</div>
    <div style="font-size:15px;font-weight:800;color:#B42318;margin-top:4px">Đã ghi nhận</div>
    <div style="font-size:11.5px" class="muted">Người xử lý: Trần Văn Hùng</div></div>
</div>
<div class="card" style="padding:16px 18px;margin-bottom:14px">
  <div style="font-size:13.5px;font-weight:700;margin-bottom:9px">
    Tỉ lệ sai định dạng theo ngày — 28 ngày gần nhất</div>{chart}</div>
<div style="display:flex;gap:18px">
  <div style="flex:1.6">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:9px">
      <div style="font-size:13.5px;font-weight:700">5 dòng sai đầu tiên (mẫu)</div>
      <div style="display:flex;gap:8px"><span class="btn ghost">⬇️ Tải toàn bộ 1.204 dòng (CSV)</span>
        <span class="btn ghost">📧 Gửi cho đối tác A</span></div></div>
    <div class="card"><table class="g">
      <tr><th>Mã giao dịch</th><th>Giá trị sai</th><th>Sai ở chỗ nào</th><th>Ngày</th><th>Nguồn</th></tr>
      {bad}</table></div>
  </div>
  <div style="width:400px;flex-shrink:0">
    <div class="card" style="padding:14px 16px;margin-bottom:12px">
      <div style="font-size:12px;font-weight:700;color:#5a6472;margin-bottom:9px">QUY TRÌNH XỬ LÝ SỰ CỐ</div>
      <div style="display:flex;align-items:center;gap:6px;margin-bottom:11px">
        <span class="chip" style="background:#F2F4F7;color:#475467">✓ Mới</span>→
        <span class="chip" style="background:#FEF3F2;color:#B42318;font-weight:700">● Đã ghi nhận</span>→
        <span class="chip" style="background:#F2F4F7;color:#98A2B3">Đã xử lý</span></div>
      <div style="font-size:12.5px;line-height:1.8">
        <b>Người xử lý:</b> Trần Văn Hùng (DE)<br>
        <b>Hạn xử lý:</b> 06/08/2026<br>
        <b>Nguyên nhân đã ghi nhận:</b> Đối tác A đổi định dạng file từ 31/07</div>
      <div style="display:flex;gap:8px;margin-top:12px">
        <span class="btn">✓ Đánh dấu đã xử lý</span>
        <span class="btn ghost">Đổi người xử lý</span></div>
    </div>
    <div class="card" style="padding:14px 16px">
      <div style="font-size:12px;font-weight:700;color:#5a6472;margin-bottom:9px">TRAO ĐỔI</div>
      <div style="font-size:12.5px;line-height:1.6;padding-bottom:9px;border-bottom:1px solid #eef1f5">
        <b>Nguyễn Thị Phương</b> <span class="muted">— 03/08 08:20</span><br>
        Đã báo đối tác A. Họ xác nhận đổi hệ thống từ 31/07, sẽ gửi lại file chuẩn trong tuần.</div>
      <div style="font-size:12.5px;line-height:1.6;padding:9px 0">
        <b>Trần Văn Hùng</b> <span class="muted">— 03/08 09:05</span><br>
        Tạm thời đã chặn 1.204 dòng này không cho chảy xuống báo cáo.</div>
    </div>
  </div>
</div>"""
    return shell("OpenMetadata — Chi tiết luật thất bại",
                 "sandbox.open-metadata.org/test-case/…/details", NAV_OM("quality"), main, OM, "#FAFAFE",
                 note="OpenMetadata · MÀN XEM CHI TIẾT MỘT LUẬT ĐANG HỎNG + quy trình xử lý sự cố")


# ============================================================ 4. Tạo thuật ngữ nghiệp vụ
def glossary_form():
    main = f"""
<div class="crumb">Từ điển nghiệp vụ › Từ điển Kinh doanh › Doanh thu › Thêm thuật ngữ</div>
<h1 class="t">📖 Thêm thuật ngữ nghiệp vụ</h1>
<div class="sub">Màn này để <b>thống nhất cách hiểu một khái niệm trong toàn công ty</b> —
  và quan trọng hơn: <b>gắn khái niệm đó vào đúng các cột dữ liệu thật</b>,
  để người dùng tìm bằng ngôn ngữ nghiệp vụ vẫn ra đúng bảng.</div>
{steps([("Định nghĩa", "now"), ("Gắn vào dữ liệu", "next"), ("Chọn người duyệt", "next")], OM)}
<div style="display:flex;gap:26px">
  <div style="width:490px;flex-shrink:0">
    {fld("Tên thuật ngữ", "Doanh thu thực thu", True)}
    {fld("Thuộc từ điển / nhóm", "Từ điển Kinh doanh › Doanh thu ▾", True)}
    {fld("Định nghĩa", "Số tiền đã thực sự về tài khoản của công ty trong kỳ. "
                       "Khác với <b>Doanh thu ghi nhận</b> — là số đã vào sổ kế toán nhưng có thể chưa thu được tiền.",
         True, "Viết cho người không làm kế toán vẫn hiểu. Nếu dễ nhầm với thuật ngữ khác thì nói rõ khác ở đâu.",
         tall=True)}
    {fld("Đơn vị tính", "VNĐ ▾")}
    {fld("Từ đồng nghĩa / cách gọi khác",
         chips(["Cash collected", "DT thực thu", "Tiền về"]) + '<span class="muted">+ Thêm</span>',
         hint="Người dùng gõ bất kỳ từ nào trong danh sách này đều tìm ra thuật ngữ")}
    {fld("Thuật ngữ liên quan",
         chips(["Doanh thu ghi nhận", "Công nợ phải thu"]) + '<span class="muted">+ Thêm</span>')}
  </div>
  <div style="width:490px;flex-shrink:0">
    {fld("Chủ sở hữu thuật ngữ", "👥 Ban Tài chính ▾", True,
         "Đơn vị có quyền quyết định định nghĩa này đúng hay sai")}
    {fld("Người phê duyệt", "👤 Trưởng Ban Tài chính ▾", True,
         "Thuật ngữ ở trạng thái <b>Nháp</b> cho tới khi được duyệt")}
    {fld("Trạng thái", "📝 Nháp — chờ duyệt ▾")}
    <div style="font-size:13px;font-weight:700;margin:6px 0 9px;padding-bottom:7px;
      border-bottom:2px solid #7147E8;display:inline-block">GẮN VÀO DỮ LIỆU THẬT (bước 2)</div>
    <div class="card" style="padding:13px 15px;margin-bottom:12px">
      <div style="border:1px solid #d5dae2;border-radius:6px;padding:8px 11px;font-size:13px;margin-bottom:10px">
        🔍 <span class="muted">Tìm bảng hoặc cột để gắn…</span></div>
      <table class="g" style="font-size:12px">
        <tr><th>Tài sản dữ liệu</th><th>Cột</th><th></th></tr>
        <tr><td class="mono">bi.doanh_thu_thang</td><td class="mono">tien_da_thu</td>
          <td><span style="color:#B42318">✕ Bỏ</span></td></tr>
        <tr><td class="mono">fin.cong_no</td><td class="mono">so_da_thanh_toan</td>
          <td><span style="color:#B42318">✕ Bỏ</span></td></tr>
      </table>
      <div class="muted" style="font-size:11.5px;margin-top:9px">
        💡 Đây là bước <b>quan trọng nhất</b>. Không gắn thì từ điển chỉ là một quyển sách nằm riêng,
        không giúp gì cho việc tìm dữ liệu.</div>
    </div>
    <div style="background:#ECFDF3;border:1px solid #A6F4C5;border-radius:7px;padding:11px 13px;font-size:12.5px">
      ✅ <b>Sau khi lưu:</b> người dùng gõ "tiền về" hay "cash collected" ở ô tìm kiếm sẽ ra
      đúng 2 cột trên — <b>dù tên cột không hề chứa các chữ đó</b>.</div>
    <div style="display:flex;gap:10px;margin-top:18px">
      <span class="btn">Tiếp tục ▶</span><span class="btn ghost">Lưu nháp</span>
      <span class="btn ghost">Huỷ</span></div>
  </div>
</div>"""
    return shell("OpenMetadata — Thêm thuật ngữ", "sandbox.open-metadata.org/glossary/add-term",
                 NAV_OM("glossary"), main, OM, "#FAFAFE",
                 note="OpenMetadata · FORM THÊM THUẬT NGỮ NGHIỆP VỤ + gắn vào cột dữ liệu")


# ============================================================ 5. Tạo hợp đồng dữ liệu
def create_contract():
    def pick(kind, name, detail, on):
        return (f'<tr style="{"background:#F0F9FF" if on else ""}">'
                f'<td><input type="checkbox" {"checked" if on else ""}></td>'
                f'<td><span class="chip" style="background:#EEF4FF;color:#3538CD">{kind}</span></td>'
                f'<td><b>{name}</b><div class="muted mono" style="font-size:11px">{detail}</div></td></tr>')

    rows = (pick("Độ tươi", "Dữ liệu phải cập nhật trước 07:00 hằng ngày", "freshness ≤ 24h", True) +
            pick("Cấu trúc", "Không được xoá / đổi kiểu 6 cột đã cam kết", "schema strict mode", True) +
            pick("Khối lượng", "Số dòng mới mỗi ngày trong khoảng cho phép", "delta ∈ [80.000 ; 300.000]", True) +
            pick("Chất lượng", "so_dien_thoai đúng định dạng · sai ≤ 0,5%", "custom SQL assertion", True) +
            pick("Cột", "so_tien không âm và không rỗng", "so_tien ≥ 0 AND NOT NULL", True) +
            pick("Chất lượng", "trang_thai chỉ nhận KHOP / LECH / CHO", "values in set", False) +
            pick("Khối lượng", "Không có ngày nào thiếu dữ liệu", "no missing partition", False))

    main = f"""
<div class="crumb">Tập dữ liệu › bi.doi_soat_giao_dich_A › Chất lượng › Hợp đồng dữ liệu › Tạo mới</div>
<h1 class="t">📜 Tạo hợp đồng dữ liệu</h1>
<div class="sub">Màn này để <b>bên tạo bảng cam kết bằng văn bản với các bên đang dùng bảng</b>:
  dữ liệu về đúng giờ, cấu trúc không đổi bất ngờ, chất lượng đạt mức nào.
  Cam kết này được <b>máy kiểm tự động mỗi ngày</b>, không phải văn bản để trong tủ.</div>
{steps([("Chọn điều khoản", "now"), ("Cam kết vận hành", "next"),
        ("Bên nhận thông báo", "next"), ("Hành động khi vi phạm", "next")], DH)}
<div style="display:flex;gap:24px">
  <div style="flex:1.3">
    <div style="font-size:13px;font-weight:700;margin-bottom:9px">
      Chọn các phép kiểm đưa vào hợp đồng <span class="muted">(đã chọn 5/7)</span></div>
    <div class="card"><table class="g">
      <tr><th style="width:34px"></th><th style="width:100px">Nhóm</th><th>Điều khoản</th></tr>{rows}</table></div>
    <div style="margin-top:12px;font-size:12.5px;background:#FFFAEB;border:1px solid #FEDF89;
      border-radius:7px;padding:11px 13px">
      ⚠️ Chỉ chọn được các phép kiểm <b>đã tạo sẵn</b> ở màn Chất lượng dữ liệu.
      Muốn thêm điều khoản mới thì phải tạo phép kiểm trước.</div>
  </div>
  <div style="width:470px;flex-shrink:0">
    {fld("Tên hợp đồng", "Đối soát giao dịch đối tác A — v2", True)}
    {fld("Bên cam kết (bên tạo dữ liệu)", "👥 Đội Data Engineering ▾", True)}
    {fld("Hiệu lực từ", "01/06/2026", True)}
    {fld("Ngày rà soát lại", "01/12/2026", hint="Hệ thống sẽ nhắc trước 2 tuần")}
    <div style="font-size:13px;font-weight:700;margin:6px 0 9px;padding-bottom:7px;
      border-bottom:2px solid #1B75BC;display:inline-block">HÀNH ĐỘNG KHI VI PHẠM (bước 4)</div>
    <div class="card" style="padding:13px 15px;font-size:12.5px;line-height:2.1">
      <div><input type="checkbox" checked> Gắn nhãn cảnh báo lên bảng cho <b>mọi người dùng đều thấy</b></div>
      <div><input type="checkbox" checked> Gửi thông báo cho <b>toàn bộ bên đang dùng bảng</b> (4 đơn vị)</div>
      <div><input type="checkbox" checked> <b>Tạm dừng các job hạ nguồn</b> — không cho số sai chảy tiếp</div>
      <div><input type="checkbox"> Chặn luôn quyền truy vấn vào bảng</div>
      <div><input type="checkbox" checked> Tạo sự cố và gán người xử lý</div>
    </div>
    <div style="background:#F0F9FF;border:1px solid #B9E6FE;border-radius:7px;padding:11px 13px;
      font-size:12.5px;margin-top:12px">
      💡 Ô thứ 3 là ô <b>đắt giá nhất</b>: hiện nay khi bảng lỗi, các đội hạ nguồn vẫn dùng số sai
      vì không ai báo. Bật ô này là chặn được ngay từ gốc.</div>
    <div style="display:flex;gap:10px;margin-top:18px">
      <span class="btn">Tiếp tục ▶</span><span class="btn ghost">Lưu nháp</span></div>
  </div>
</div>"""
    return shell("DataHub — Tạo hợp đồng dữ liệu",
                 "demo.datahub.com/dataset/…/Quality/Data%20Contract/create", NAV_DH("contract"), main,
                 DH, "#F7FAFC",
                 note="DataHub · FORM TẠO HỢP ĐỒNG DỮ LIỆU — chọn điều khoản và hành động khi vi phạm")


# ============================================================ 6. Lọc theo dòng
def row_filter():
    rows = "".join(
        f'<tr><td>{g}</td><td class="mono" style="font-size:11.5px">{expr}</td><td>{res}</td></tr>'
        for g, expr, res in [
            ("Nhóm <b>kd_mien_bac</b>", "khu_vuc IN ('HN','HP','QN')", "412.033 / 12.480.331 dòng"),
            ("Nhóm <b>kd_mien_nam</b>", "khu_vuc IN ('HCM','CT','BD')", "689.114 / 12.480.331 dòng"),
            ("Nhóm <b>kd_toan_quoc</b>", "(không lọc)", "12.480.331 / 12.480.331 dòng"),
            ("Nhóm <b>ctv_thue_ngoai</b>", "ngay_ghi_nhan &gt;= CURRENT_DATE - 7", "84.201 / 12.480.331 dòng"),
        ])

    main = f"""
<div class="crumb">Chính sách › hive_prod › Lọc theo dòng › Tạo chính sách</div>
<h1 class="t">🔎 Tạo chính sách lọc theo dòng</h1>
<div class="sub">Màn này để <b>cùng một bảng nhưng mỗi người chỉ thấy phần dữ liệu thuộc phạm vi của mình</b> —
  ví dụ cán bộ kinh doanh miền Bắc chỉ thấy giao dịch miền Bắc.
  Không phải tạo 3 bảng riêng cho 3 miền.</div>
<div style="display:flex;gap:26px;margin-top:18px">
  <div style="width:450px;flex-shrink:0">
    {fld("Tên chính sách", "Lọc giao dịch theo khu vực phụ trách", True)}
    {fld("Kho dữ liệu", "hive_prod ▾", True)}
    {fld("Cơ sở dữ liệu / Bảng", "bi &nbsp;/&nbsp; doi_soat_giao_dich_A ▾", True, mono=True)}
    {fld("Áp dụng cho", "Nhóm: kd_mien_bac ▾", True,
         "Có thể chọn theo người dùng, nhóm, hoặc vai trò")}
    {fld("Điều kiện lọc", "khu_vuc IN ('HN','HP','QN')", True,
         "Viết như mệnh đề WHERE. Hệ thống tự chèn vào mọi câu truy vấn của nhóm này.", mono=True)}
    <div style="background:#E6F6F3;border:1px solid #A6E0D5;border-radius:7px;padding:11px 13px;
      font-size:12.5px;margin-bottom:14px">
      💡 Có thể dùng <b>biến động</b> thay vì viết cứng:
      <span class="mono">khu_vuc = '${{user.khu_vuc}}'</span> — hệ thống tự thay bằng khu vực
      của người đang đăng nhập. Một chính sách dùng chung cho mọi khu vực.</div>
    <div style="display:flex;gap:10px">
      <span class="btn">💾 Lưu chính sách</span>
      <span class="btn ghost">▶️ Chạy thử</span><span class="btn ghost">Huỷ</span></div>
  </div>
  <div style="flex:1">
    <div style="font-size:13px;font-weight:700;margin-bottom:9px">
      Các chính sách lọc dòng đang áp trên bảng này</div>
    <div class="card" style="margin-bottom:18px"><table class="g">
      <tr><th>Đối tượng</th><th>Điều kiện lọc</th><th>Số dòng nhìn thấy</th></tr>{rows}</table></div>
    <div style="font-size:13px;font-weight:700;margin-bottom:9px">
      Cùng câu lệnh <span class="mono">SELECT COUNT(*) FROM bi.doi_soat_giao_dich_A</span></div>
    <div style="display:flex;gap:12px">
      <div class="card" style="flex:1;padding:13px 15px">
        <div style="font-size:12px;font-weight:700;color:#0F7B6C;margin-bottom:7px">
          👤 Chị Lan — kd_mien_bac</div>
        <div class="mono" style="font-size:19px;font-weight:800">412.033</div>
        <div class="muted" style="font-size:11.5px;margin-top:4px">
          Câu lệnh thật sự chạy:<br>
          <span class="mono" style="font-size:11px">… WHERE khu_vuc IN ('HN','HP','QN')</span></div></div>
      <div class="card" style="flex:1;padding:13px 15px">
        <div style="font-size:12px;font-weight:700;color:#B54708;margin-bottom:7px">
          👤 Anh Nam — ctv_thue_ngoai</div>
        <div class="mono" style="font-size:19px;font-weight:800">84.201</div>
        <div class="muted" style="font-size:11.5px;margin-top:4px">
          Câu lệnh thật sự chạy:<br>
          <span class="mono" style="font-size:11px">… WHERE ngay_ghi_nhan &gt;= CURRENT_DATE - 7</span></div></div>
      <div class="card" style="flex:1;padding:13px 15px">
        <div style="font-size:12px;font-weight:700;color:#3538CD;margin-bottom:7px">
          👤 Anh Hùng — kd_toan_quoc</div>
        <div class="mono" style="font-size:19px;font-weight:800">12.480.331</div>
        <div class="muted" style="font-size:11.5px;margin-top:4px">
          Câu lệnh thật sự chạy:<br>
          <span class="mono" style="font-size:11px">… (không thêm điều kiện)</span></div></div>
    </div>
    <div style="margin-top:16px;font-size:12.5px;background:#E6F6F3;border:1px solid #A6E0D5;
      border-radius:7px;padding:11px 14px">
      ✅ <b>Điểm quan trọng:</b> ba người viết <b>y hệt một câu lệnh</b>, hệ thống tự chèn điều kiện lọc
      trước khi chạy. Người dùng không cần biết có luật lọc, và <b>không thể bỏ qua nó</b>.</div>
  </div>
</div>"""
    return shell("Apache Ranger — Lọc theo dòng", "ranger.internal:6080/policymanager/rowfilter/create",
                 NAV_RG("row"), main, RG, "#F4FBFA",
                 note="Apache Ranger · FORM TẠO CHÍNH SÁCH LỌC THEO DÒNG (row-level filter)")


SCREENS = {
    "om-07-edit-table": edit_table,
    "om-08-tag-column": tag_column,
    "om-09-test-detail": test_detail,
    "om-10-glossary-form": glossary_form,
    "dh-03-create-contract": create_contract,
    "rg-03-rowfilter": row_filter,
}
