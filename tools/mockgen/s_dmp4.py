# -*- coding: utf-8 -*-
"""DMP — Module ① menu 1.4 Danh mục tham chiếu (3 màn)."""
from dmp import shell, fld, chip, AC
from s_dmp2 import _kpi
from s_dmp3 import _steps


# ============================================================ 1.4 danh sách các danh mục
def ref_list():
    rows = [
        ("DM-001", "Danh mục Đối tác", "Đối tác", "1.284", "v12", "03/08/2026", "P.T.Hà",
         "2 chờ duyệt", "Đang dùng"),
        ("DM-002", "Danh mục Tỉnh/Thành", "Địa lý", "63", "v3", "12/01/2026", "P.T.Hà",
         "—", "Đang dùng"),
        ("DM-003", "Danh mục Trạng thái đối soát", "Đối soát", "3", "v2", "20/06/2026",
         "N.T.Phương", "—", "Đang dùng"),
        ("DM-004", "Danh mục Gói cước", "Sản phẩm", "412", "v28", "01/08/2026", "L.M.Tuấn",
         "1 chờ duyệt", "Đang dùng"),
        ("DM-005", "Danh mục Kênh bán", "Sản phẩm", "18", "v5", "15/07/2026", "L.M.Tuấn",
         "—", "Đang dùng"),
        ("DM-018", "Danh mục Ngành nghề (cũ)", "Khách hàng", "94", "v7", "02/03/2025",
         "P.T.Hà", "—", "Ngừng dùng"),
    ]
    tr = ""
    for code, nm, grp, cnt, ver, upd, own, pend, st in rows:
        tr += (f'<tr><td class="mono muted">{code}</td>'
               f'<td><b style="color:{AC}">{nm}</b></td><td>{grp}</td>'
               f'<td style="text-align:right"><b>{cnt}</b></td>'
               f'<td>{chip(ver, "t")}</td><td class="muted">{upd}</td><td>{own}</td>'
               f'<td>{chip(pend, "o") if pend != "—" else "<span class=muted>—</span>"}</td>'
               f'<td>{chip(st, "g" if st == "Đang dùng" else "r")}</td>'
               f'<td><span class="ico">👁</span><span class="ico">✎</span>'
               f'<span class="ico">⋯</span></td></tr>')

    body = _kpi([
        ("TỔNG SỐ DANH MỤC", "34", "3 danh mục ngừng dùng", "#101828"),
        ("BẢN GHI ĐANG QUẢN LÝ", "8.412", "trên toàn bộ danh mục", "#101828"),
        ("CHỜ PHÊ DUYỆT", "3", "ở 2 danh mục", "#B54708"),
        ("ĐANG ĐƯỢC LUẬT CHẤT LƯỢNG DÙNG", "6", "làm nguồn đối chiếu", "#067647"),
        ("DANH MỤC CÓ MENU RIÊNG", "12", "tự sinh menu cho người nhập liệu", "#101828"),
    ]) + f"""
<div style="display:flex;gap:10px;margin-bottom:13px;align-items:center">
  <div style="flex:1;border:1px solid #d0d7e2;border-radius:8px;padding:9px 13px;font-size:13px;
    background:#fff">🔍 <span class="muted">Tìm theo mã, tên danh mục, hoặc giá trị bên trong…</span></div>
  <span class="btn w">Nhóm danh mục: tất cả ▾</span>
  <span class="btn w">Trạng thái: Đang dùng ▾</span>
  <span class="btn w">⬇️ Xuất Excel</span>
</div>
<div class="card"><table class="g">
  <tr><th>Mã</th><th>Tên danh mục</th><th>Nhóm</th><th style="text-align:right">Số bản ghi</th>
    <th>Phiên bản</th><th>Cập nhật lần cuối</th><th>Người phụ trách</th><th>Chờ duyệt</th>
    <th>Trạng thái</th><th>Thao tác</th></tr>{tr}</table></div>
<div style="display:flex;gap:14px;margin-top:14px">
  <div class="note" style="flex:1;background:#ECFDF3;border:1px solid #A6F4C5">
    ✅ <b>Phần này SQLWF đã có gần đủ</b> — màn <span class="mono">channel-indexing-management</span>
    hiện đã có: khai định nghĩa danh mục và các trường · nhập dữ liệu · <b>phê duyệt bản ghi</b> ·
    <b>phiên bản và so sánh thay đổi</b> · nạp file hàng loạt · xuất Excel ·
    <b>tự sinh menu riêng cho từng danh mục</b>.
  </div>
  <div class="note" style="width:470px;background:#FFFAEB;border:1px solid #FEDF89">
    ⚠️ <b>Việc duy nhất cần làm thêm: mở API cho luật chất lượng gọi vào.</b><br>
    Hiện danh mục và module Chất lượng <b>không biết đến nhau</b>, nên luật
    <i>"mã đối tác phải tồn tại trong danh mục Đối tác"</i> chưa chạy được.<br>
    Thẻ <b>"Đang được luật chất lượng dùng: 6"</b> ở trên là chỉ số theo dõi việc nối này.
  </div>
</div>"""
    return shell("dmp.vds.vn/catalog/reference-data", "Data Catalog › Danh mục tham chiếu",
                 "📚 Danh mục tham chiếu",
                 "Danh mục dùng chung toàn hệ thống — và là nguồn đối chiếu cho luật chất lượng",
                 body, "DMP · Menu 1.4 — DANH MỤC THAM CHIẾU · Màn DANH SÁCH", "m14",
                 tabs=("Tất cả danh mục", ["Tất cả danh mục", "Tôi phụ trách",
                                           "Có bản ghi chờ duyệt", "Đã ngừng dùng"]),
                 actions='<span class="btn w">📤 Nhập từ Excel</span>'
                         '<span class="btn">➕ Tạo danh mục</span>')


# ============================================================ 1.4 thêm mới — khai định nghĩa
def ref_create():
    flds = [
        ("doi_tac_id", "Chuỗi", "—", "3", "20", "✔", "✔", "Mã đối tác", "Khoá đối chiếu với bảng giao dịch"),
        ("ten_doi_tac", "Chuỗi", "—", "1", "200", "✔", "—", "Tên đối tác", "Hiển thị trên báo cáo"),
        ("loai_doi_tac", "Chuỗi", "NOI_BO / NGOAI", "—", "—", "✔", "—", "Loại", "Phân nhóm khi thống kê"),
        ("ngay_hieu_luc", "Ngày", "dd/MM/yyyy", "—", "—", "✔", "—", "Hiệu lực từ", "Lọc đối tác còn hiệu lực"),
        ("trang_thai", "Chuỗi", "HOAT_DONG / DUNG", "—", "—", "✔", "—", "Trạng thái", "Chỉ đối chiếu bản ghi đang hoạt động"),
    ]
    tr = "".join(
        f'<tr><td class="mono"><b>{a}</b></td><td>{b}</td>'
        f'<td class="mono" style="font-size:11.5px">{c}</td><td style="text-align:center">{d}</td>'
        f'<td style="text-align:center">{e}</td><td style="text-align:center">{f}</td>'
        f'<td style="text-align:center">{g}</td><td>{h}</td>'
        f'<td style="font-size:11.5px" class="muted">{i}</td>'
        f'<td><span class="ico">✎</span><span class="ico">✕</span></td></tr>'
        for a, b, c, d, e, f, g, h, i in flds)

    body = _steps([("Thông tin danh mục", "done"), ("Khai các trường", "now"),
                   ("Quy tắc phê duyệt", "next"), ("Nhập dữ liệu", "next")]) + f"""
<div style="display:flex;gap:18px">
  <div style="width:420px;flex-shrink:0">
    <div class="card" style="padding:17px 19px">
      <div class="sec">① THÔNG TIN DANH MỤC</div>
      {fld("Mã danh mục", "DM-035 &nbsp;<span class='muted'>(tự sinh)</span>", ro=True)}
      {fld("Tên danh mục", "Danh mục Đối tác", True,
           "Tên hiển thị ở ô chọn khi khai luật chất lượng")}
      {fld("Tên kỹ thuật", "dm_doi_tac", True,
           "Dùng khi luật chất lượng tham chiếu tới, ví dụ <span class='mono'>→ dm_doi_tac</span>",
           mono=True)}
      {fld("Nhóm danh mục", "Đối tác ▾", hint="Dùng để gom nhóm ở màn danh sách")}
      {fld("Mô tả", "Danh sách toàn bộ đối tác đang và đã hợp tác, dùng đối chiếu mã đối tác "
                    "trên các bảng giao dịch.", True)}
      {fld("Người phụ trách", "👤 Phạm Thu Hà ▾", True,
           "Người <b>duyệt bản ghi mới</b> và chịu trách nhiệm về nội dung danh mục")}
      {fld("Tự sinh menu riêng cho danh mục này?", "☑ Có — menu \"Danh mục Đối tác\"",
           hint="Bật thì người nhập liệu vào thẳng menu riêng, không phải đi qua màn này")}
    </div>
  </div>
  <div style="flex:1">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:9px">
      <div class="sec" style="margin:0">② KHAI CÁC TRƯỜNG CỦA DANH MỤC</div>
      <span class="btn" style="padding:5px 11px">➕ Thêm trường</span></div>
    <div class="card"><table class="g">
      <tr><th>Tên trường</th><th>Kiểu</th><th>Định dạng / Tập giá trị</th>
        <th style="text-align:center">Min</th><th style="text-align:center">Max</th>
        <th style="text-align:center">Bắt buộc</th><th style="text-align:center">Khoá chính</th>
        <th>Tên hiển thị</th><th>Mục đích sử dụng</th><th></th></tr>{tr}</table></div>
    <div class="note" style="background:#EFF4FF;border:1px solid #C7D7FE;margin-top:14px">
      🔗 <b>Khai ở đây, dùng ở đâu</b><br><br>
      <b>Trường khoá chính</b> <span class="mono">doi_tac_id</span> → là <b>cột được đối chiếu</b>
      khi khai luật <i>"giá trị phải tồn tại trong danh mục"</i> ở <b>3.2</b><br>
      <b>Tập giá trị</b> <span class="mono">NOI_BO / NGOAI</span> → sinh thẳng thành
      <b>luật kiểm tập giá trị</b> cho chính danh mục này<br>
      <b>Bắt buộc / Min / Max</b> → kiểm ngay khi người dùng nhập bản ghi, không cho lưu nếu sai
    </div>
    <div class="note" style="background:#FFFAEB;border:1px solid #FEDF89;margin-top:12px">
      ⚠️ <b>Chỉ được sửa định nghĩa trường khi danh mục chưa có dữ liệu.</b>
      Sau khi đã có bản ghi, việc thêm trường mới sẽ tạo <b>phiên bản mới</b> và
      các bản ghi cũ để trống trường đó.
    </div>
    <div style="display:flex;gap:10px;margin-top:16px">
      <span class="btn">Tiếp tục ▶</span><span class="btn w">Lưu nháp</span>
      <span class="btn w">Huỷ</span></div>
  </div>
</div>"""
    return shell("dmp.vds.vn/catalog/reference-data/create",
                 "Data Catalog › Danh mục tham chiếu › Tạo danh mục", "➕ Tạo danh mục tham chiếu",
                 "Khai định nghĩa một danh mục mới — gồm thông tin chung và cấu trúc các trường",
                 body, "DMP · Menu 1.4 — DANH MỤC THAM CHIẾU · Màn THÊM MỚI (bước 1 và 2)", "m14")


# ============================================================ 1.4 chi tiết — dữ liệu + phiên bản
def ref_detail():
    recs = [
        ("1284", "DT_VNPAY", "Công ty CP Giải pháp Thanh toán Việt Nam", "NGOAI",
         "01/08/2026", "HOAT_DONG", "Chờ duyệt", "v12"),
        ("1283", "DT_MOMO", "Công ty CP Dịch vụ Di động Trực tuyến", "NGOAI",
         "01/08/2026", "HOAT_DONG", "Chờ duyệt", "v12"),
        ("1201", "DT_VDS_BI", "Trung tâm Phân tích Dữ liệu", "NOI_BO",
         "15/03/2025", "HOAT_DONG", "Đã duyệt", "v11"),
        ("1180", "DT_ZALOPAY", "Công ty CP Zion", "NGOAI",
         "20/01/2025", "HOAT_DONG", "Đã duyệt", "v9"),
        ("0994", "DT_OLD_A", "Đối tác A (cũ)", "NGOAI",
         "01/01/2023", "DUNG", "Đã duyệt", "v4"),
    ]
    tr = ""
    for rid, code, nm, lo, dt, st, ap, ver in recs:
        apc = "o" if ap == "Chờ duyệt" else "g"
        tr += (f'<tr><td class="mono muted">{rid}</td><td class="mono"><b>{code}</b></td>'
               f'<td>{nm}</td><td>{chip(lo, "b")}</td><td class="muted">{dt}</td>'
               f'<td>{chip(st, "g" if st == "HOAT_DONG" else "n")}</td>'
               f'<td>{chip(ap, apc)}</td><td>{chip(ver, "t")}</td>'
               f'<td><span class="ico">👁</span><span class="ico">✎</span></td></tr>')

    diff = "".join(
        f'<tr><td class="mono">{a}</td><td>{b}</td>'
        f'<td class="muted" style="font-size:11.5px">{c}</td>'
        f'<td style="font-size:11.5px;color:#067647">{d}</td><td class="muted">{e}</td></tr>'
        for a, b, c, d, e in [
            ("DT_VNPAY", "Thêm mới", "—", "Công ty CP Giải pháp Thanh toán VN", "P.T.Hà"),
            ("DT_MOMO", "Thêm mới", "—", "Công ty CP Dịch vụ Di động Trực tuyến", "P.T.Hà"),
            ("DT_OLD_A", "Sửa", "HOAT_DONG", "DUNG", "P.T.Hà")])

    body = _kpi([
        ("SỐ BẢN GHI", "1.284", "1.281 đang hoạt động", "#101828"),
        ("PHIÊN BẢN HIỆN TẠI", "v12", "tạo 03/08/2026", "#101828"),
        ("CHỜ PHÊ DUYỆT", "2", "người duyệt: Phạm Thu Hà", "#B54708"),
        ("LUẬT ĐANG THAM CHIẾU", "3", "trên 3 bảng khác nhau", "#067647"),
    ]) + f"""
<div class="card" style="padding:14px 17px;margin-bottom:14px;background:#F9FAFB">
  <div class="sec">3 LUẬT CHẤT LƯỢNG ĐANG DÙNG DANH MỤC NÀY LÀM NGUỒN ĐỐI CHIẾU</div>
  <table class="g" style="font-size:12.5px">
    <tr><td style="width:290px" class="mono">bi.doi_soat_giao_dich_A.doi_tac</td>
        <td>→ đối chiếu với <span class="mono">dm_doi_tac.doi_tac_id</span></td>
        <td>{chip("⚠️ 3 mã lạ", "o")}</td></tr>
    <tr><td class="mono">bi.doi_soat_giao_dich_B.doi_tac</td>
        <td>→ đối chiếu với <span class="mono">dm_doi_tac.doi_tac_id</span></td>
        <td>{chip("Đạt", "g")}</td></tr>
    <tr><td class="mono">dwh.giao_dich_ngay.ma_dt</td>
        <td>→ đối chiếu với <span class="mono">dm_doi_tac.doi_tac_id</span></td>
        <td>{chip("Đạt", "g")}</td></tr>
  </table>
  <div class="muted" style="font-size:11.5px;margin-top:8px">
    ⭐ Đây là mối nối mà SQLWF hiện <b>chưa có</b> — danh mục và luật chất lượng đang không biết đến nhau.</div>
</div>

<div style="display:flex;gap:16px">
  <div style="flex:1.5">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:9px">
      <div style="font-size:13.5px;font-weight:700">Dữ liệu trong danh mục</div>
      <div style="display:flex;gap:8px"><span class="btn w">📤 Nạp từ file</span>
        <span class="btn w">⬇️ Xuất Excel</span><span class="btn">➕ Thêm bản ghi</span></div></div>
    <div class="card"><table class="g">
      <tr><th>ID</th><th>Mã đối tác</th><th>Tên đối tác</th><th>Loại</th><th>Hiệu lực từ</th>
        <th>Trạng thái</th><th>Phê duyệt</th><th>Phiên bản</th><th></th></tr>{tr}</table>
      <div style="padding:9px 12px;font-size:12px" class="muted">… và 1.279 bản ghi khác</div></div>
  </div>
  <div style="width:520px;flex-shrink:0">
    <div class="card" style="padding:15px 17px;margin-bottom:13px">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:9px">
        <div class="sec" style="margin:0">SO SÁNH PHIÊN BẢN</div>
        <span class="btn w" style="padding:4px 10px;font-size:11.5px">v11 ↔ v12 ▾</span></div>
      <table class="g" style="font-size:12px">
        <tr><th>Mã</th><th>Loại thay đổi</th><th>Giá trị cũ</th><th>Giá trị mới</th><th>Người sửa</th></tr>
        {diff}</table>
      <div class="muted" style="font-size:11.5px;margin-top:8px">
        Lý do thay đổi: <i>"Bổ sung 2 đối tác thanh toán mới theo công văn 412/KD"</i></div>
    </div>
    <div class="note" style="background:#FFFAEB;border:1px solid #FEDF89">
      ⚠️ <b>2 bản ghi đang chờ duyệt</b> — chưa được luật chất lượng dùng để đối chiếu.<br>
      Nghĩa là nếu bảng giao dịch đã có mã <span class="mono">DT_VNPAY</span> thì
      luật vẫn báo <b>"mã lạ"</b> cho tới khi bản ghi được duyệt.<br>
      <span style="color:#B54708">Đây là hành vi cố ý — để danh mục không bị nhiễm dữ liệu chưa kiểm.</span>
    </div>
  </div>
</div>"""
    return shell("dmp.vds.vn/catalog/reference-data/DM-001",
                 "Data Catalog › Danh mục tham chiếu › Danh mục Đối tác",
                 "📚 Danh mục Đối tác",
                 "Mã danh mục DM-001 &nbsp;·&nbsp; Người phụ trách: Phạm Thu Hà "
                 "&nbsp;·&nbsp; Tên kỹ thuật: dm_doi_tac",
                 body, "DMP · Menu 1.4 — DANH MỤC THAM CHIẾU · Màn CHI TIẾT (dữ liệu + phiên bản)",
                 "m14", tabs=("Dữ liệu", ["Dữ liệu", "Định nghĩa trường", "Phiên bản",
                                          "Chờ duyệt", "Nhật ký"]))


SCREENS = {
    "dmp-13-refdata-list": ref_list,
    "dmp-14-refdata-create": ref_create,
    "dmp-15-refdata-detail": ref_detail,
}
