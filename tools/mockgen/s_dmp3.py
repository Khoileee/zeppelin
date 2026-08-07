# -*- coding: utf-8 -*-
"""DMP — Module ① Data Catalog: 2 tab còn lại + menu 1.2, 1.3, 1.4."""
from dmp import shell, fld, chip, AC
from s_dmp2 import TABS, CRUMB, TITLE, DESC, ACT, _kpi


def _steps(items):
    out = []
    for i, (lb, st) in enumerate(items, 1):
        c = {"done": ("#12B76A", "#fff"), "now": (AC, "#fff"), "next": ("#E4E7EC", "#98A2B3")}[st]
        out.append(f'<div style="display:flex;align-items:center;gap:7px">'
                   f'<div style="width:22px;height:22px;border-radius:50%;background:{c[0]};'
                   f'color:{c[1]};display:flex;align-items:center;justify-content:center;'
                   f'font-size:11px;font-weight:700">{"✓" if st == "done" else i}</div>'
                   f'<span style="font-size:12px;font-weight:{700 if st == "now" else 400};'
                   f'color:{"#101828" if st != "next" else "#98A2B3"}">{lb}</span></div>')
    return ('<div style="display:flex;gap:11px;align-items:center;margin-bottom:17px;'
            'padding:12px 16px;background:#fff;border:1px solid #e3e8ef;border-radius:9px">' +
            '<div style="width:20px;height:1px;background:#e3e8ef"></div>'.join(out) + "</div>")


# ============================================================ 1.1 tab QUYỀN
def tab_perm():
    rows = [
        ("👥 ban_kinh_doanh", "Nhóm", "Toàn bảng", "Xem", "so_dien_thoai → hiện 4 số cuối",
         "Vô thời hạn", "5.2 · theo nhãn PD_SENSITIVE"),
        ("👥 doi_de", "Nhóm", "Toàn bảng", "Xem · Ghi", "—", "Vô thời hạn", "5.2 · quyền dữ liệu"),
        ("👥 ctv_thue_ngoai", "Nhóm", "Toàn bảng", "Xem", "so_dien_thoai → băm (hash)",
         "Vô thời hạn", "5.2 · theo nhãn PD_SENSITIVE"),
        ("👤 le.minh.tuan", "Người", "Toàn bảng", "Xem", "—", "Hết hạn 15/08/2026",
         "5.3 · yêu cầu #218 đã duyệt"),
        ("👥 ban_tai_chinh", "Nhóm", "Chỉ 3 cột", "Xem", "—", "Vô thời hạn", "5.2 · quyền mức cột"),
    ]
    tr = ""
    for who, kind, scope, act, mask, exp, src in rows:
        expc = "#B54708" if "Hết hạn" in exp else "#667085"
        tr += (f'<tr><td><b>{who}</b></td><td>{kind}</td><td>{scope}</td>'
               f'<td>{chip(act, "b")}</td>'
               f'<td>{chip(mask, "r") if mask != "—" else "<span class=muted>không che</span>"}</td>'
               f'<td style="color:{expc}">{exp}</td>'
               f'<td class="muted" style="font-size:11.5px">{src}</td>'
               f'<td><span class="ico">👁</span></td></tr>')

    body = _kpi([
        ("NHÓM ĐƯỢC CẤP QUYỀN", "4", "trên tổng 18 nhóm", "#101828"),
        ("NGƯỜI ĐƯỢC CẤP RIÊNG", "1", "1 quyền sắp hết hạn", "#B54708"),
        ("CỘT ĐANG BỊ CHE", "1", "so_dien_thoai — nhãn PD_SENSITIVE", "#B42318"),
        ("YÊU CẦU ĐANG CHỜ DUYỆT", "2", "chờ BDA phụ trách xử lý", "#B54708"),
    ]) + f"""
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
  <div style="font-size:13.5px;font-weight:700">Ai đang được truy cập bảng này</div>
  <div style="display:flex;gap:8px"><span class="btn w">📋 Xem 2 yêu cầu đang chờ</span>
    <span class="btn">➕ Cấp quyền</span></div>
</div>
<div class="card"><table class="g">
  <tr><th>Đối tượng</th><th>Loại</th><th>Phạm vi</th><th>Được làm gì</th><th>Che dữ liệu</th>
    <th>Thời hạn</th><th>Nguồn chính sách</th><th></th></tr>{tr}</table></div>

<div style="display:flex;gap:14px;margin-top:14px">
  <div class="note" style="flex:1;background:#EFF4FF;border:1px solid #C7D7FE">
    💡 <b>Màn này chỉ ĐỌC, không cấp quyền tại đây.</b> Nó tổng hợp lại kết quả từ
    <b>5.2 Chính sách truy cập</b> để trả lời nhanh câu <i>"ai đang xem được bảng này"</i> mà
    không phải mở 3 màn khác nhau.<br>
    Cột <b>Nguồn chính sách</b> cho biết quyền đó đến từ đâu — bấm vào sẽ nhảy sang đúng chính sách.
  </div>
  <div class="note" style="width:440px;background:#FEF3F2;border:1px solid #FECDCA">
    🔴 <b>Cột <span class="mono">so_dien_thoai</span> mang nhãn <span class="mono">PD_SENSITIVE</span></b>
    nên hai nhóm bị che tự động — <b>không ai phải khai riêng cho bảng này</b>.<br>
    Đây chính là kết quả của việc gắn nhãn ở <b>tab Cột</b>.
  </div>
</div>"""
    return shell("dmp.vds.vn/catalog/tables/BI-0142/permissions", CRUMB, TITLE, DESC, body,
                 "DMP · Menu 1.1 — CHI TIẾT BẢNG · tab QUYỀN", "m11",
                 tabs=("Quyền", TABS), actions=ACT)


# ============================================================ 1.1 tab LỊCH SỬ
def tab_history():
    rows = [
        ("03/08 06:14", "Hệ thống", "Chất lượng", "Sự cố #4821 mở",
         "—", "Luật so_dien_thoai thất bại", "—"),
        ("01/08 09:22", "Trần Văn Hùng", "Cấu trúc", "Thêm cột",
         "5 cột", "6 cột — thêm doi_tac", "10.21.2.108"),
        ("01/08 09:20", "Trần Văn Hùng", "Cấu trúc", "Đổi kiểu cột so_tien",
         "STRING", "DECIMAL(18,2)", "10.21.2.108"),
        ("28/07 15:40", "Nguyễn Thị Phương", "Mô tả", "Sửa mô tả bảng",
         "Bảng đối soát giao dịch.", "Bảng đối soát giao dịch với đối tác A. Nguồn: file…",
         "10.21.2.51"),
        ("28/07 15:38", "Nguyễn Thị Phương", "Phân loại", "Gắn nhãn cột so_dien_thoai",
         "DATA_GENERAL", "PD_SENSITIVE", "10.21.2.51"),
        ("20/07 11:05", "Nguyễn Thị Phương", "Trách nhiệm", "Đổi BDA phụ trách",
         "Phạm Thu Hà", "Nguyễn Thị Phương", "10.21.2.51"),
        ("15/07 08:12", "Trần Văn Hùng", "Vận hành", "Đổi chu kỳ cập nhật",
         "Hằng tuần", "Hằng ngày — trước 07:00", "10.21.2.108"),
    ]
    tr = ""
    for tm, who, kind, act, old, new, ip in rows:
        kc = {"Chất lượng": "r", "Cấu trúc": "o", "Mô tả": "n",
              "Phân loại": "b", "Trách nhiệm": "t", "Vận hành": "g"}[kind]
        tr += (f'<tr><td class="mono" style="font-size:11.5px">{tm}</td><td>{who}</td>'
               f'<td>{chip(kind, kc)}</td><td><b>{act}</b></td>'
               f'<td class="muted" style="font-size:11.5px">{old}</td>'
               f'<td style="font-size:11.5px">{new}</td>'
               f'<td class="mono muted" style="font-size:11px">{ip}</td></tr>')

    body = f"""
<div style="display:flex;gap:9px;margin-bottom:13px;align-items:center">
  <div style="flex:1;border:1px solid #d0d7e2;border-radius:8px;padding:8px 12px;font-size:12.5px;
    background:#fff">🔍 <span class="muted">Tìm theo người thay đổi, trường bị đổi…</span></div>
  <span class="btn w">Loại thay đổi: tất cả ▾</span>
  <span class="btn w">Người thực hiện: tất cả ▾</span>
  <span class="btn w">Khoảng thời gian: 90 ngày ▾</span>
  <span class="btn w">⬇️ Xuất Excel</span>
</div>
<div class="card">
  <div style="padding:10px 14px;border-bottom:1px solid #eef1f6;font-size:13px">
    <b>32 thay đổi</b> <span class="muted">trong 90 ngày · hiển thị 7 gần nhất</span></div>
  <table class="g">
    <tr><th>Thời điểm</th><th>Người thực hiện</th><th>Loại</th><th>Hành động</th>
      <th>Giá trị cũ</th><th>Giá trị mới</th><th>Địa chỉ IP</th></tr>{tr}</table>
</div>
<div style="display:flex;gap:14px;margin-top:14px">
  <div class="note" style="flex:1;background:#ECFDF3;border:1px solid #A6F4C5">
    ✅ <b>Phần này SQLWF đã có sẵn</b> — màn <span class="mono">history-data</span> ghi đầy đủ
    <b>giá trị cũ → giá trị mới</b> và <b>địa chỉ IP</b>. Việc cần làm chỉ là
    <b>đưa nó vào thành một tab của bảng</b> thay vì để ở màn riêng, để xem lịch sử của
    đúng bảng đang mở.
  </div>
  <div class="note" style="width:440px;background:#EFF4FF;border:1px solid #C7D7FE">
    💡 <b>Vì sao đáng để ở đây:</b> khi số liệu báo cáo đột nhiên lệch, câu hỏi đầu tiên luôn là
    <i>"hôm qua ai sửa gì bảng này?"</i>. Dòng <b>01/08 đổi kiểu cột <span class="mono">so_tien</span></b>
    ở trên là ví dụ điển hình.
  </div>
</div>"""
    return shell("dmp.vds.vn/catalog/tables/BI-0142/history", CRUMB, TITLE, DESC, body,
                 "DMP · Menu 1.1 — CHI TIẾT BẢNG · tab LỊCH SỬ", "m11",
                 tabs=("Lịch sử", TABS), actions=ACT)


# ============================================================ 1.2 NHÓM BẢNG — danh sách
def group_list():
    rows = [
        ("NB-001", "Đối soát đối tác", "Toàn bộ bảng phục vụ đối soát với đối tác ngoài",
         "12", "3", "N.T.Phương", "Đang dùng"),
        ("NB-002", "Báo cáo kinh doanh", "Bảng nguồn cho hệ báo cáo Ban Kinh doanh",
         "28", "5", "P.T.Hà", "Đang dùng"),
        ("NB-003", "Dữ liệu thuê bao", "Nhóm bảng thuê bao dùng chung",
         "41", "7", "N.T.Phương", "Đang dùng"),
        ("NB-004", "Tài chính — hạn chế", "Chỉ Ban Tài chính được truy cập",
         "9", "1", "P.T.Hà", "Đang dùng"),
        ("NB-011", "Thử nghiệm Q2/2026", "Nhóm tạm cho đợt thử nghiệm",
         "6", "0", "T.V.Hùng", "Ngừng dùng"),
    ]
    tr = ""
    for code, nm, de, nt, ng, own, st in rows:
        tr += (f'<tr><td class="mono muted">{code}</td>'
               f'<td><b style="color:{AC}">{nm}</b></td><td>{de}</td>'
               f'<td style="text-align:center"><b>{nt}</b></td>'
               f'<td style="text-align:center">{ng}</td><td>{own}</td>'
               f'<td>{chip(st, "g" if st == "Đang dùng" else "r")}</td>'
               f'<td><span class="ico">👁</span><span class="ico">✎</span>'
               f'<span class="ico">⋯</span></td></tr>')

    body = _kpi([
        ("TỔNG SỐ NHÓM", "24", "5 nhóm ngừng dùng", "#101828"),
        ("BẢNG ĐÃ VÀO NHÓM", "1.842", "16% trên 11.482 bảng", "#B54708"),
        ("BẢNG CHƯA VÀO NHÓM NÀO", "9.640", "chỉ phân quyền được từng bảng một", "#B42318"),
        ("NHÓM NGƯỜI DÙNG ĐANG GẮN", "18", "trung bình 3,2 nhóm/bảng", "#101828"),
    ]) + f"""
<div style="display:flex;gap:10px;margin-bottom:13px;align-items:center">
  <div style="flex:1;border:1px solid #d0d7e2;border-radius:8px;padding:9px 13px;font-size:13px;
    background:#fff">🔍 <span class="muted">Tìm theo mã nhóm, tên nhóm, tên bảng bên trong…</span></div>
  <span class="btn w">Trạng thái: Đang dùng ▾</span>
  <span class="btn w">Người tạo: tất cả ▾</span>
</div>
<div class="card"><table class="g">
  <tr><th>Mã nhóm</th><th>Tên nhóm bảng</th><th>Mô tả</th><th style="text-align:center">Số bảng</th>
    <th style="text-align:center">Nhóm người dùng</th><th>Người phụ trách</th><th>Trạng thái</th>
    <th>Thao tác</th></tr>{tr}</table></div>
<div class="note" style="background:#EFF4FF;border:1px solid #C7D7FE;margin-top:14px">
  💡 <b>Nhóm bảng để làm gì:</b> phân quyền cho <b>một nhóm 41 bảng</b> bằng một thao tác, thay vì
  cấp quyền 41 lần. Khi thêm bảng mới vào nhóm, mọi người đang có quyền trên nhóm
  <b>tự động thấy bảng mới</b> — không phải cấp lại.<br>
  ⚠️ Con số <b>9.640 bảng chưa vào nhóm nào</b> là chỉ số đáng chú ý: những bảng này hiện chỉ
  phân quyền được từng cái một.
</div>"""
    return shell("dmp.vds.vn/catalog/table-groups", "Data Catalog › Nhóm bảng",
                 "📦 Nhóm bảng", "Gom nhiều bảng thành một bộ để phân quyền và theo dõi chung",
                 body, "DMP · Menu 1.2 — NHÓM BẢNG · Màn DANH SÁCH", "m12",
                 tabs=("Tất cả nhóm", ["Tất cả nhóm", "Nhóm tôi phụ trách", "Đã ngừng dùng"]),
                 actions='<span class="btn">➕ Tạo nhóm bảng</span>')


# ============================================================ 1.2 NHÓM BẢNG — thêm mới
def group_create():
    avail = "".join(
        f'<div style="display:flex;justify-content:space-between;padding:6px 9px;font-size:12px;'
        f'border-bottom:1px solid #f2f4f7"><span class="mono">{n}</span>'
        f'<span class="muted" style="font-size:11px">{d}</span></div>'
        for n, d in [("bi.doanh_thu_thang", "Tài chính"), ("dwh.thue_bao_ngay", "Kinh doanh"),
                     ("raw.log_truy_cap", "Kỹ thuật"), ("mart.kpi_kinh_doanh", "Kinh doanh"),
                     ("dm.tinh_thanh", "Dùng chung"), ("crm.khach_hang", "Kinh doanh")])
    chosen = "".join(
        f'<div style="display:flex;justify-content:space-between;align-items:center;padding:6px 9px;'
        f'font-size:12px;border-bottom:1px solid #f2f4f7;background:#f9fbff">'
        f'<span class="mono">{n}</span>'
        f'<span>{chip("Bật", "g") if on else chip("Tắt", "n")}'
        f'<span style="color:#B42318;margin-left:6px">✕</span></span></div>'
        for n, on in [("bi.doi_soat_giao_dich_A", True), ("raw.gd_doi_tac_A", True),
                      ("dm.doi_tac", True), ("bi.doi_soat_giao_dich_B", False)])

    body = _steps([("Thông tin nhóm", "now"), ("Chọn bảng", "next"),
                   ("Gán nhóm người dùng", "next")]) + f"""
<div style="display:flex;gap:18px">
  <div style="width:430px;flex-shrink:0">
    <div class="card" style="padding:17px 19px">
      <div class="sec">① THÔNG TIN NHÓM</div>
      {fld("Mã nhóm", "NB-025 &nbsp;<span class='muted'>(hệ thống tự sinh)</span>", ro=True)}
      {fld("Tên nhóm bảng", "Đối soát đối tác B", True,
           "Tên hiển thị khi cấp quyền — nên nói rõ nhóm này gồm dữ liệu gì")}
      {fld("Mô tả", "Toàn bộ bảng phục vụ đối soát với đối tác B, gồm bảng thô, bảng đối soát và danh mục.",
           True, "Người duyệt quyền đọc dòng này để quyết định có cấp hay không")}
      {fld("Người phụ trách nhóm", "👤 Nguyễn Thị Phương ▾", True,
           "Là người <b>duyệt các yêu cầu xin quyền</b> vào nhóm này ở menu 5.3")}
      {fld("Trạng thái", "🟢 Đang dùng ▾", True,
           "Chuyển sang <b>Ngừng dùng</b> thì mọi quyền trên nhóm bị thu hồi, "
           "nhưng quyền cấp trực tiếp cho từng bảng vẫn giữ")}
    </div>
  </div>
  <div style="flex:1">
    <div class="sec">② CHỌN BẢNG ĐƯA VÀO NHÓM</div>
    <div style="display:flex;gap:14px;align-items:flex-start">
      <div style="flex:1">
        <div style="font-size:12px;font-weight:600;color:#344054;margin-bottom:6px">
          Bảng sẵn có <span class="muted">(11.478)</span></div>
        <div style="border:1px solid #d0d7e2;border-radius:8px;padding:7px 10px;font-size:12px;
          margin-bottom:7px;background:#fff">🔍 <span class="muted">Tìm bảng…</span></div>
        <div class="card" style="height:250px;overflow:hidden">{avail}</div>
      </div>
      <div style="padding-top:90px;display:flex;flex-direction:column;gap:7px">
        <span class="btn" style="padding:5px 11px">▶</span>
        <span class="btn w" style="padding:5px 11px">◀</span>
      </div>
      <div style="flex:1">
        <div style="font-size:12px;font-weight:600;color:#344054;margin-bottom:6px">
          Bảng đã chọn <span class="muted">(4)</span></div>
        <div style="font-size:11.5px;color:#8b95a7;margin-bottom:7px">
          Công tắc <b>Bật/Tắt</b> cho phép tạm khoá một bảng trong nhóm mà không cần gỡ ra</div>
        <div class="card" style="height:250px;overflow:hidden">{chosen}</div>
      </div>
    </div>
    <div class="note" style="background:#FFFAEB;border:1px solid #FEDF89;margin-top:14px">
      ⚠️ <b>Một bảng có thể thuộc nhiều nhóm.</b> Khi đó người dùng được quyền nếu
      <b>có quyền ở ít nhất một nhóm</b> chứa bảng đó. Đây là điểm dễ nhầm khi rà soát quyền —
      màn <b>5.5 Báo cáo quyền</b> sẽ hiển thị đầy đủ mọi đường dẫn tới quyền.
    </div>
    <div style="display:flex;gap:10px;margin-top:16px">
      <span class="btn">Tiếp tục ▶</span><span class="btn w">Lưu nháp</span>
      <span class="btn w">Huỷ</span></div>
  </div>
</div>"""
    return shell("dmp.vds.vn/catalog/table-groups/create",
                 "Data Catalog › Nhóm bảng › Tạo nhóm bảng", "➕ Tạo nhóm bảng",
                 "Gom bảng thành bộ để cấp quyền một lần cho cả nhóm", body,
                 "DMP · Menu 1.2 — NHÓM BẢNG · Màn THÊM MỚI", "m12")


# ============================================================ 1.3 MIỀN DỮ LIỆU
def domain_list():
    tree = "".join(
        f'<div style="padding:6px 10px;font-size:12.5px;border-radius:6px;margin-bottom:2px;'
        f'{"background:#EFF4FF;font-weight:700;color:" + AC if on else ""}">{ind}{t}'
        f'<span class="muted" style="float:right;font-weight:400">{c}</span></div>'
        for ind, t, c, on in [
            ("", "🧩 Kinh doanh", "4.218", False),
            ("&nbsp;&nbsp;", "📁 Đối soát", "312", True),
            ("&nbsp;&nbsp;", "📁 Thuê bao", "1.104", False),
            ("&nbsp;&nbsp;", "📁 Bán hàng", "886", False),
            ("", "🧩 Tài chính", "1.552", False),
            ("&nbsp;&nbsp;", "📁 Doanh thu", "621", False),
            ("&nbsp;&nbsp;", "📁 Công nợ", "294", False),
            ("", "🧩 Kỹ thuật", "2.680", False),
            ("", "🧩 Dùng chung", "418", False),
            ("", "⚠️ Chưa gán miền", "2.614", False),
        ])
    tables = "".join(
        f'<tr><td class="mono" style="color:{AC}">{n}</td><td>{tier}</td><td>{bda}</td>'
        f'<td>{de}</td><td>{st}</td></tr>'
        for n, tier, bda, de, st in [
            ("bi.doi_soat_giao_dich_A", chip("Tier 1", "o"), "N.T.Phương", "T.V.Hùng",
             chip("Đang dùng", "g")),
            ("bi.doi_soat_giao_dich_B", chip("Tier 2", "b"), "N.T.Phương", "T.V.Hùng",
             chip("Đang dùng", "g")),
            ("raw.gd_doi_tac_A", chip("Tier 3", "n"), "—", "T.V.Hùng", chip("Đang dùng", "g")),
            ("dm.doi_tac", chip("Tier 2", "b"), "P.T.Hà", "L.M.Tuấn", chip("Đang dùng", "g")),
        ])

    body = f"""
<div style="display:flex;gap:18px">
  <div style="width:330px;flex-shrink:0">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
      <div style="font-size:12.5px;font-weight:700">CÂY MIỀN DỮ LIỆU</div>
      <span class="btn" style="padding:4px 10px;font-size:11.5px">➕ Thêm miền</span></div>
    <div class="card" style="padding:9px">{tree}</div>
    <div class="note" style="background:#FEF3F2;border:1px solid #FECDCA;margin-top:12px">
      🔴 <b>2.614 bảng chưa gán miền</b> — không lọc được theo miền, không phân quyền theo miền,
      và không xuất hiện đúng chỗ khi người dùng duyệt danh mục.
    </div>
  </div>
  <div style="flex:1">
    <div class="card" style="padding:16px 19px;margin-bottom:14px">
      <div class="sec">MIỀN ĐANG CHỌN — Kinh doanh › Đối soát</div>
      <table class="g" style="font-size:12.5px">
        <tr><td style="width:180px;color:#667085">Mã miền</td><td class="mono">DOM-KD-04</td></tr>
        <tr><td style="color:#667085">Miền cha</td><td>Kinh doanh</td></tr>
        <tr><td style="color:#667085">Mô tả</td>
            <td>Dữ liệu phục vụ đối soát số liệu với các đối tác ngoài</td></tr>
        <tr><td style="color:#667085">Đơn vị chủ quản</td><td>Ban Kinh doanh</td></tr>
        <tr><td style="color:#667085">BDA mặc định</td><td>Nguyễn Thị Phương</td></tr>
        <tr><td style="color:#667085">DE mặc định</td><td>Trần Văn Hùng</td></tr>
      </table>
    </div>
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:9px">
      <div style="font-size:13.5px;font-weight:700">312 bảng thuộc miền này</div>
      <span class="btn w">⬇️ Xuất danh sách</span></div>
    <div class="card"><table class="g">
      <tr><th>Tên bảng</th><th>Mức quan trọng</th><th>BDA</th><th>DE</th><th>Trạng thái</th></tr>
      {tables}</table>
      <div style="padding:9px 12px;font-size:12px" class="muted">… và 308 bảng khác</div></div>
    <div class="note" style="background:#EFF4FF;border:1px solid #C7D7FE;margin-top:14px">
      💡 <b>BDA / DE mặc định của miền</b> được <b>điền sẵn</b> khi tạo bảng mới trong miền này —
      giảm việc khai lặp và tránh bảng vô chủ.
    </div>
  </div>
</div>"""
    return shell("dmp.vds.vn/catalog/domains", "Data Catalog › Miền dữ liệu",
                 "🧩 Miền dữ liệu",
                 "Khai lĩnh vực nghiệp vụ theo cây phân cấp — dùng để gom nhóm, tìm kiếm và phân quyền",
                 body, "DMP · Menu 1.3 — MIỀN DỮ LIỆU · Màn DANH SÁCH + CHI TIẾT", "m13")


def domain_create():
    body = f"""
<div style="display:flex;gap:18px">
  <div style="width:520px;flex-shrink:0">
    <div class="card" style="padding:18px 20px">
      <div class="sec">THÔNG TIN MIỀN DỮ LIỆU</div>
      {fld("Mã miền", "DOM-KD-07 &nbsp;<span class='muted'>(hệ thống tự sinh theo miền cha)</span>",
           ro=True)}
      {fld("Tên miền", "Chăm sóc khách hàng", True,
           "Tên nghiệp vụ, không dùng viết tắt kỹ thuật")}
      {fld("Miền cha", "Kinh doanh ▾",
           hint="Để trống nếu đây là miền cấp 1. Cây miền tối đa <b>3 cấp</b>")}
      {fld("Mô tả", "Dữ liệu liên quan tới hoạt động chăm sóc, khiếu nại và giữ chân khách hàng.",
           True, "Hiện ở màn khám phá để người dùng biết miền này chứa gì")}
      {fld("Đơn vị chủ quản", "Ban Kinh doanh ▾", True,
           "Đơn vị chịu trách nhiệm về dữ liệu trong miền này")}
      {fld("BDA mặc định", "👤 Nguyễn Thị Phương ▾",
           hint="Sẽ được <b>điền sẵn</b> khi ai đó tạo bảng mới thuộc miền này")}
      {fld("DE mặc định", "👤 Trần Văn Hùng ▾", hint="Tương tự trường trên")}
      <div style="display:flex;gap:10px;margin-top:18px">
        <span class="btn">💾 Lưu</span><span class="btn w">Huỷ</span></div>
    </div>
  </div>
  <div style="flex:1">
    <div class="card" style="padding:16px 19px;margin-bottom:14px;background:#F9FAFB">
      <div class="sec">XEM TRƯỚC VỊ TRÍ TRONG CÂY</div>
      <div style="font-size:13px;line-height:2;font-family:Consolas,monospace">
        🧩 Kinh doanh<br>
        &nbsp;&nbsp;📁 Đối soát<br>
        &nbsp;&nbsp;📁 Thuê bao<br>
        &nbsp;&nbsp;📁 Bán hàng<br>
        &nbsp;&nbsp;<b style="color:{AC}">📁 Chăm sóc khách hàng &nbsp;← miền mới</b></div>
    </div>
    <div class="note" style="background:#EFF4FF;border:1px solid #C7D7FE;margin-bottom:12px">
      🔗 <b>Khai ở đây, dùng ở đâu</b><br><br>
      <b>Tên miền</b> → ô lọc "Miền dữ liệu" ở màn <b>1.1 Bảng dữ liệu</b><br>
      <b>Tên miền</b> → phân quyền theo miền ở <b>5.2 Chính sách truy cập</b><br>
      <b>BDA / DE mặc định</b> → điền sẵn khi tạo bảng mới ở <b>1.1</b><br>
      <b>Đơn vị chủ quản</b> → gom số liệu theo đơn vị ở <b>6.1 Sức khoẻ dữ liệu</b>
    </div>
    <div class="note" style="background:#FFFAEB;border:1px solid #FEDF89">
      ⚠️ <b>Không xoá được miền đang có bảng.</b> Muốn bỏ thì phải chuyển hết bảng sang miền khác
      trước — hệ thống sẽ chặn và hiện danh sách bảng còn lại.
    </div>
  </div>
</div>"""
    return shell("dmp.vds.vn/catalog/domains/create",
                 "Data Catalog › Miền dữ liệu › Thêm miền", "➕ Thêm miền dữ liệu",
                 "Khai một lĩnh vực nghiệp vụ mới vào cây miền", body,
                 "DMP · Menu 1.3 — MIỀN DỮ LIỆU · Màn THÊM MỚI", "m13")


SCREENS = {
    "dmp-07-table-perm": tab_perm,
    "dmp-08-table-history": tab_history,
    "dmp-09-group-list": group_list,
    "dmp-10-group-create": group_create,
    "dmp-11-domain-list": domain_list,
    "dmp-12-domain-create": domain_create,
}
