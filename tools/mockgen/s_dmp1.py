# -*- coding: utf-8 -*-
"""DMP — Module 1: Danh mục bảng (màn danh sách + màn thêm mới)."""
from dmp import shell, fld, chip, AC


# ============================================================ Màn danh sách
def table_list():
    rows = [
        ("BI-0142", "bi.doi_soat_giao_dich_A", "Đối soát giao dịch — Đối tác A", "Kinh doanh",
         "Tier 1", "Iceberg", "N.T.Phương", "T.V.Hùng", "🟢 4h trước", "5/7", "✅ Đang dùng"),
        ("DWH-0031", "dwh.thue_bao_ngay", "Thuê bao theo ngày", "Kinh doanh",
         "Tier 1", "Iceberg", "N.T.Phương", "L.M.Tuấn", "🟢 2h trước", "9/9", "✅ Đang dùng"),
        ("BI-0177", "bi.doanh_thu_thang", "Doanh thu theo tháng", "Tài chính",
         "Tier 1", "Parquet", "P.T.Hà", "T.V.Hùng", "🟠 31h trước", "6/8", "✅ Đang dùng"),
        ("DM-0009", "dm.doi_tac", "Danh mục đối tác", "Kinh doanh",
         "Tier 2", "Parquet", "P.T.Hà", "L.M.Tuấn", "🟢 1h trước", "3/3", "✅ Đang dùng"),
        ("RAW-0455", "raw.gd_doi_tac_A", "Giao dịch thô từ đối tác A", "Kinh doanh",
         "Tier 3", "Parquet", "—", "T.V.Hùng", "🟢 5h trước", "1/1", "✅ Đang dùng"),
        ("RAW-0512", "raw.log_truy_cap", "Log truy cập thô", "Kỹ thuật",
         "Tier 3", "Parquet", "—", "—", "🔴 9 ngày", "0/0", "⚠️ Chưa hoàn thiện"),
        ("TMP-0098", "tmp.test_thang_7", "(chưa có mô tả)", "—",
         "—", "Parquet", "—", "—", "🔴 42 ngày", "0/0", "⛔ Ngừng dùng"),
    ]
    tr = ""
    for code, name, disp, dom, tier, fmt, bda, de, fresh, dq, st in rows:
        tier_c = {"Tier 1": chip("Tier 1", "o"), "Tier 2": chip("Tier 2", "b"),
                  "Tier 3": chip("Tier 3", "n"), "—": '<span class="muted">—</span>'}[tier]
        fmt_c = chip(fmt, "t") if fmt == "Iceberg" else chip(fmt, "n")
        st_c = {"✅ Đang dùng": chip("Đang dùng", "g"),
                "⚠️ Chưa hoàn thiện": chip("Chưa hoàn thiện hồ sơ", "o"),
                "⛔ Ngừng dùng": chip("Ngừng dùng", "r")}[st]
        dqc = "#067647" if dq.split("/")[0] == dq.split("/")[1] and dq != "0/0" else (
            "#8b95a7" if dq == "0/0" else "#B42318")
        tr += (f'<tr><td class="mono muted">{code}</td>'
               f'<td><b class="mono" style="color:{AC}">{name}</b>'
               f'<div class="muted" style="font-size:11.5px">{disp}</div></td>'
               f'<td>{dom}</td><td>{tier_c}</td><td>{fmt_c}</td>'
               f'<td>{bda}</td><td>{de}</td><td>{fresh}</td>'
               f'<td style="color:{dqc};font-weight:700">{dq}</td><td>{st_c}</td>'
               f'<td><span class="ico">👁</span><span class="ico">✎</span><span class="ico">⋯</span></td></tr>')

    filters = "".join(
        f'<div style="border:1px solid #d0d7e2;border-radius:7px;padding:7px 11px;font-size:12px;'
        f'background:#fff;color:#475467">{f} ▾</div>'
        for f in ["Miền dữ liệu: tất cả", "Mức quan trọng: tất cả", "Định dạng: tất cả",
                  "Người phụ trách: tất cả", "Trạng thái: Đang dùng", "Độ tươi: tất cả"])

    body = f"""
<div style="display:flex;gap:12px;margin-bottom:16px">
  <div class="card kpi"><div class="lb">TỔNG SỐ BẢNG</div><div class="vl">11.482</div>
    <div class="sb">+18 trong 30 ngày</div></div>
  <div class="card kpi"><div class="lb">ĐÃ HOÀN THIỆN HỒ SƠ</div>
    <div class="vl" style="color:#067647">3.104</div><div class="sb">27,0% — mục tiêu quý IV: 100% Tier 1</div></div>
  <div class="card kpi"><div class="lb">CÓ ÍT NHẤT 1 LUẬT CHẤT LƯỢNG</div>
    <div class="vl" style="color:#B54708">64</div><div class="sb">0,6%</div></div>
  <div class="card kpi"><div class="lb">CÓ CỘT GẮN NHÃN NHẠY CẢM</div>
    <div class="vl">412</div><div class="sb">3,6%</div></div>
  <div class="card kpi"><div class="lb">DỮ LIỆU TRỄ SO VỚI CAM KẾT</div>
    <div class="vl" style="color:#B42318">23</div><div class="sb">đang cảnh báo</div></div>
</div>

<div style="display:flex;gap:10px;margin-bottom:12px;align-items:center">
  <div style="flex:1;border:1px solid #d0d7e2;border-radius:8px;padding:9px 13px;font-size:13px;background:#fff">
    🔍 <span class="muted">Tìm theo mã bảng, tên bảng, tên cột, mô tả, thuật ngữ nghiệp vụ…</span></div>
  <div class="btn w">⚙️ Bộ lọc nâng cao</div>
  <div class="btn w">⬇️ Xuất Excel</div>
</div>
<div style="display:flex;gap:8px;margin-bottom:14px;flex-wrap:wrap">{filters}</div>

<div class="card">
  <div style="display:flex;justify-content:space-between;align-items:center;padding:11px 14px;
    border-bottom:1px solid #eef1f6">
    <div style="font-size:13px"><b>11.482 bảng</b>
      <span class="muted">· đang lọc: Trạng thái = Đang dùng</span></div>
    <div class="muted" style="font-size:12px">Hiển thị 1–7 / 11.482</div></div>
  <table class="g">
    <tr><th>Mã bảng</th><th>Tên bảng / Tên hiển thị</th><th>Miền</th><th>Mức QT</th><th>Định dạng</th>
      <th>BDA</th><th>DE</th><th>Độ tươi</th><th>Luật đạt</th><th>Trạng thái</th><th>Thao tác</th></tr>
    {tr}</table>
</div>

<div class="note" style="background:#EFF4FF;border:1px solid #C7D7FE;margin-top:14px">
  💡 <b>Vì sao màn này là gốc của cả hệ thống:</b> một bảng <b>chưa có trong danh mục</b> thì
  <b>không gán được luật chất lượng</b> (module 3), <b>không phân quyền được</b> (module 5),
  <b>không xuất hiện trên sơ đồ nguồn gốc</b> (tab Nguồn gốc) và <b>job không được phép ghi vào</b> (module 4).
  Mọi module khác đều đọc mã bảng từ đây.</div>"""

    actions = ('<span class="btn w">📤 Nhập từ Excel</span>'
               '<span class="btn">➕ Thêm bảng mới</span>')
    return shell("dmp.vds.vn/catalog/tables",
                 "Data Catalog › Bảng dữ liệu",
                 "🗂️ Bảng dữ liệu",
                 "Nơi khai báo và tra cứu mọi bảng dữ liệu của công ty — nguồn sự thật duy nhất "
                 "cho toàn bộ các module còn lại",
                 body, "DMP · Menu 1.1 — BẢNG DỮ LIỆU · Màn DANH SÁCH", "m11",
                 tabs=("Tất cả bảng", ["Tất cả bảng", "Bảng tôi phụ trách", "Chưa hoàn thiện hồ sơ",
                                       "Chờ duyệt", "Đã ngừng dùng"]),
                 actions=actions)


# ============================================================ Màn thêm mới
def table_create():
    def step(n, label, state):
        c = {"done": ("#12B76A", "#fff"), "now": (AC, "#fff"), "next": ("#E4E7EC", "#98A2B3")}[state]
        return (f'<div style="display:flex;align-items:center;gap:7px">'
                f'<div style="width:22px;height:22px;border-radius:50%;background:{c[0]};color:{c[1]};'
                f'display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700">'
                f'{"✓" if state == "done" else n}</div>'
                f'<span style="font-size:12px;font-weight:{700 if state == "now" else 400};'
                f'color:{"#101828" if state != "next" else "#98A2B3"}">{label}</span></div>')

    steps = ('<div style="display:flex;gap:12px;align-items:center;margin-bottom:18px;padding:12px 16px;'
             'background:#fff;border:1px solid #e3e8ef;border-radius:9px">' +
             '<div style="width:22px;height:1px;background:#e3e8ef"></div>'.join([
                 step(1, "Thông tin nhận dạng", "now"), step(2, "Trách nhiệm & Phân loại", "next"),
                 step(3, "Cấu trúc cột", "next"), step(4, "Cam kết vận hành", "next"),
                 step(5, "Xem lại & Gửi duyệt", "next")]) + "</div>")

    body = steps + f"""
<div style="display:flex;gap:20px">
  <div style="flex:1.1">
    <div class="card" style="padding:18px 20px;margin-bottom:16px">
      <div class="sec">① ĐỊNH DANH BẢNG</div>
      {fld("Mã bảng", "BI-0143 &nbsp;<span class='muted'>(hệ thống tự sinh)</span>", ro=True)}
      {fld("Tên bảng vật lý", "bi.doi_soat_giao_dich_B", True,
           "Bắt buộc theo <b>Chuẩn đặt tên</b> đang áp dụng: "
           "<code>&lt;miền&gt;.&lt;nghiệp_vụ&gt;_&lt;đối_tượng&gt;</code> — chữ thường, "
           "không dấu, phân cách bằng gạch dưới", mono=True)}
      <div class="note" style="background:#ECFDF3;border:1px solid #A6F4C5;margin:-6px 0 13px">
        ✅ Tên hợp lệ theo chuẩn <b>CHUAN-BANG-01</b> — kiểm tự động ngay khi gõ</div>
      {fld("Tên hiển thị", "Đối soát giao dịch — Đối tác B", True,
           "Tên tiếng Việt để người không biết kỹ thuật vẫn tìm ra bảng")}
      {fld("Mô tả", "Bảng đối soát giao dịch với đối tác B. Nguồn: file đối tác gửi qua SFTP "
                    "hằng ngày 05:30. Chốt số liệu 06:00. Dùng cho báo cáo doanh thu ngày.", True,
           "Trả lời 3 câu: bảng này là gì · lấy từ đâu · dùng để làm gì. Tối thiểu 50 ký tự")}
      {fld("Vùng lưu trữ", "business_zone / bi ▾", True,
           "Quyết định đường dẫn vật lý trên HDFS và chính sách mã hoá áp dụng")}
      {fld("Định dạng bảng", "Iceberg ▾", True,
           "Parquet = chỉ ghi thêm · <b>Iceberg = sửa/xoá từng dòng, xem lại trạng thái quá khứ</b>")}
    </div>
  </div>
  <div style="flex:1">
    <div class="card" style="padding:18px 20px;margin-bottom:16px">
      <div class="sec">② TRÁCH NHIỆM & PHÂN LOẠI &nbsp;<span class="muted"
        style="font-weight:400;font-size:11px">(bước 2)</span></div>
      {fld("BDA phụ trách", "👤 Nguyễn Thị Phương — Phòng PTDL ▾", True,
           "Người trả lời câu hỏi <b>nghiệp vụ</b>. Nhận cảnh báo chất lượng và yêu cầu cấp quyền")}
      {fld("DE phụ trách", "👤 Trần Văn Hùng — Đội DE ▾", True,
           "Người xử lý khi job hỏng / dữ liệu trễ. Là người mặc định được gán sự cố")}
      {fld("Miền dữ liệu", "Kinh doanh ▾", True,
           "Lấy từ menu <b>1.3 Miền dữ liệu</b>. Dùng để gom nhóm tìm kiếm và phân quyền theo miền")}
      {fld("Mức độ quan trọng", "🏅 Tier 1 — phục vụ báo cáo lãnh đạo ▾", True,
           "Tier 1 bắt buộc phải có ≥ 3 luật chất lượng và người phụ trách trước khi được duyệt")}
      {fld("Nhãn phân loại", chip("Chưa gắn nhãn", "n") + ' <span class="muted">+ Thêm nhãn</span>',
           hint="Lấy từ menu <b>2.3 Phân loại & Nhãn</b>. Gắn ở đây thì "
                "<b>chính sách bảo mật theo nhãn tự áp</b> ở menu 5.2 — không phải khai lại")}
    </div>
    <div class="card" style="padding:18px 20px">
      <div class="sec">④ CAM KẾT VẬN HÀNH &nbsp;<span class="muted"
        style="font-weight:400;font-size:11px">(bước 4)</span></div>
      {fld("Chu kỳ cập nhật", "Hằng ngày — trước 07:00 ▾", True,
           "Là <b>lời khai</b>. Hệ thống lấy mốc này so với thời điểm cập nhật thật để tính "
           "<b>độ tươi</b> và cảnh báo khi trễ")}
      {fld("Thời gian lưu trữ", "36 tháng ▾", hint="Cơ sở để job dọn dữ liệu cũ")}
      {fld("Trạng thái", "🟡 Nháp ▾", True,
           "<b>Nháp</b> = chưa ai dùng được · <b>Đang dùng</b> = mở cho toàn hệ thống · "
           "<b>Ngừng dùng</b> = ẩn khỏi tìm kiếm, job ghi vào sẽ bị chặn")}
    </div>
  </div>
  <div style="width:330px;flex-shrink:0">
    <div class="card" style="padding:15px 17px;margin-bottom:14px;background:#FFFAEB;border-color:#FEDF89">
      <div style="font-size:12px;font-weight:700;margin-bottom:8px">🔒 ĐIỀU KIỆN ĐỂ ĐƯỢC DUYỆT</div>
      <div style="font-size:12.5px;line-height:2">
        ✅ Tên bảng đúng chuẩn đặt tên<br>
        ✅ Có mô tả ≥ 50 ký tự<br>
        ✅ Có BDA và DE phụ trách<br>
        ⬜ Đã khai đủ cột và mô tả cột<br>
        ⬜ <b>Tier 1 → phải có ≥ 3 luật chất lượng</b><br>
        ⬜ Cột nghi nhạy cảm đã được gắn nhãn</div>
      <div class="muted" style="font-size:11px;margin-top:9px">
        Chưa đủ điều kiện thì chỉ lưu được ở trạng thái <b>Nháp</b>.</div>
    </div>
    <div class="card" style="padding:15px 17px">
      <div style="font-size:12px;font-weight:700;margin-bottom:8px">🔗 KHAI Ở ĐÂY, DÙNG Ở ĐÂU</div>
      <div style="font-size:12.5px;line-height:1.85">
        <b>Mã bảng</b> → menu 3.2 gán luật · menu 4.1 chọn bảng đích cho job · menu 5.2 phân quyền<br><br>
        <b>Chu kỳ cập nhật</b> → cảnh báo độ tươi ở menu 3.2<br><br>
        <b>Nhãn phân loại</b> → chính sách che dữ liệu ở menu 5.2<br><br>
        <b>Mức quan trọng</b> → thứ tự ưu tiên xử lý sự cố ở menu 3.4</div>
    </div>
    <div style="display:flex;gap:9px;margin-top:16px">
      <span class="btn">Tiếp tục ▶</span>
      <span class="btn w">Lưu nháp</span>
      <span class="btn w">Huỷ</span></div>
  </div>
</div>"""
    return shell("dmp.vds.vn/catalog/tables/create",
                 "Data Catalog › Bảng dữ liệu › Thêm bảng mới",
                 "➕ Thêm bảng mới",
                 "Khai báo một bảng vào danh mục — 5 bước. Bảng chỉ được đưa vào sử dụng "
                 "sau khi đủ điều kiện duyệt.",
                 body, "DMP · Menu 1.1 — BẢNG DỮ LIỆU · Màn THÊM MỚI (bước 1, 2 và 4)", "m11",
                 height=1080)


SCREENS = {"dmp-01-table-list": table_list, "dmp-02-table-create": table_create}
