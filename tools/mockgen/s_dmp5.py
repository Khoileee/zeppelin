# -*- coding: utf-8 -*-
"""DMP — Module ② Governance: 2.1 Business Glossary, 2.2 Classification."""
from dmp import shell, fld, chip, AC
from s_dmp2 import _kpi
from s_dmp3 import _steps


# ============================================================ 2.1 danh sách thuật ngữ
def glo_list():
    rows = [
        ("TN-0042", "Doanh thu ghi nhận", "Kinh doanh › Doanh thu", "✔", "18", "Ban Tài chính",
         "P.T.Hà", "v1.3", "Đã duyệt"),
        ("TN-0043", "Doanh thu thực thu", "Kinh doanh › Doanh thu", "✔", "6", "Ban Tài chính",
         "P.T.Hà", "v1.0", "Chờ duyệt"),
        ("TN-0018", "Thuê bao hoạt động", "Kinh doanh › Thuê bao", "✔", "31", "Ban Kinh doanh",
         "N.T.Phương", "v2.1", "Đã duyệt"),
        ("TN-0019", "Thuê bao rời mạng", "Kinh doanh › Thuê bao", "—", "12", "Ban Kinh doanh",
         "N.T.Phương", "v1.2", "Đã duyệt"),
        ("TN-0077", "Đối soát", "Kinh doanh › Đối soát", "—", "9", "Ban Kinh doanh",
         "N.T.Phương", "v1.0", "Đã duyệt"),
        ("TN-0091", "Gói cước", "Sản phẩm › Gói cước", "—", "0", "Ban Sản phẩm",
         "L.M.Tuấn", "v1.0", "Đã duyệt"),
    ]
    tr = ""
    for code, nm, path, cde, cols, own, st_, ver, stt in rows:
        colc = "#8b95a7" if cols == "0" else "#067647"
        tr += (f'<tr><td class="mono muted">{code}</td>'
               f'<td><b style="color:{AC}">{nm}</b></td><td class="muted">{path}</td>'
               f'<td style="text-align:center">{chip("CDE", "r") if cde == "✔" else "—"}</td>'
               f'<td style="text-align:center;color:{colc};font-weight:700">{cols}</td>'
               f'<td>{own}</td><td>{st_}</td><td>{chip(ver, "t")}</td>'
               f'<td>{chip(stt, "g" if stt == "Đã duyệt" else "o")}</td>'
               f'<td><span class="ico">👁</span><span class="ico">✎</span></td></tr>')

    body = _kpi([
        ("TỔNG SỐ THUẬT NGỮ", "218", "trong 4 từ điển", "#101828"),
        ("ĐÃ GẮN VÀO CỘT THẬT", "142", "65% — 76 thuật ngữ chưa gắn", "#B54708"),
        ("ĐÁNH DẤU CDE", "38", "dữ liệu trọng yếu, ưu tiên kiểm chất lượng", "#B42318"),
        ("CHỜ DUYỆT", "5", "người duyệt: chủ sở hữu thuật ngữ", "#B54708"),
        ("SỐ CỘT ĐANG MANG THUẬT NGỮ", "1.284", "trên tổng 96.400 cột", "#101828"),
    ]) + f"""
<div style="display:flex;gap:10px;margin-bottom:13px;align-items:center">
  <div style="flex:1;border:1px solid #d0d7e2;border-radius:8px;padding:9px 13px;font-size:13px;
    background:#fff">🔍 <span class="muted">Tìm theo tên, bí danh, định nghĩa…</span></div>
  <span class="btn w">Từ điển: tất cả ▾</span><span class="btn w">Chủ sở hữu: tất cả ▾</span>
  <span class="btn w">Chỉ CDE ☐</span><span class="btn w">Chưa gắn vào cột ☐</span>
</div>
<div class="card"><table class="g">
  <tr><th>Mã</th><th>Tên thuật ngữ</th><th>Thuộc từ điển</th><th style="text-align:center">CDE</th>
    <th style="text-align:center">Số cột đã gắn</th><th>Chủ sở hữu</th><th>Người phụ trách</th>
    <th>Phiên bản</th><th>Trạng thái</th><th></th></tr>{tr}</table></div>
<div style="display:flex;gap:14px;margin-top:14px">
  <div class="note" style="flex:1;background:#FEF3F2;border:1px solid #FECDCA">
    🔴 <b>Cột "Số cột đã gắn" là chỉ số sống còn của menu này.</b> Thuật ngữ gắn <b>0 cột</b>
    (như <i>Gói cước</i> ở trên) chỉ là chữ nằm trong sổ — không giúp gì cho việc tìm dữ liệu.<br>
    Hiện <b>76/218 thuật ngữ chưa gắn vào cột nào</b>.
  </div>
  <div class="note" style="width:470px;background:#ECFDF3;border:1px solid #A6F4C5">
    ✅ <b>SQLWF đã có gần đủ.</b> `data-glossary` có bí danh · <b>cờ CDE</b> · chủ sở hữu ·
    steward · người duyệt · thuật ngữ cha · thuật ngữ liên quan · đính kèm tài liệu ·
    quy trình duyệt · nạp hàng loạt.<br>
    ❌ Thiếu <b>đúng một thứ</b>: đưa thuật ngữ vào <b>chỉ mục tìm kiếm</b> của menu 1.1.
  </div>
</div>"""
    return shell("dmp.vds.vn/governance/glossary", "Governance › Từ điển nghiệp vụ",
                 "📖 Từ điển nghiệp vụ",
                 "Thống nhất cách hiểu khái niệm trong toàn công ty — và gắn khái niệm vào cột dữ liệu thật",
                 body, "DMP · Menu 2.1 — TỪ ĐIỂN NGHIỆP VỤ · Màn DANH SÁCH", "m21",
                 tabs=("Tất cả thuật ngữ", ["Tất cả thuật ngữ", "Chỉ CDE", "Chưa gắn vào cột",
                                            "Chờ duyệt", "Tôi phụ trách"]),
                 actions='<span class="btn w">📤 Nạp từ Excel</span>'
                         '<span class="btn">➕ Thêm thuật ngữ</span>')


# ============================================================ 2.1 chi tiết thuật ngữ
def glo_detail():
    cols = [
        ("bi.doi_soat_giao_dich_A", "so_tien", "DECIMAL(18,2)", "Kinh doanh", "Tier 1", "Đã duyệt"),
        ("bi.doanh_thu_thang", "tong_tien", "DECIMAL(18,2)", "Tài chính", "Tier 1", "Đã duyệt"),
        ("dwh.thue_bao_ngay", "doanh_thu_ngay", "DECIMAL(18,2)", "Kinh doanh", "Tier 1", "Đã duyệt"),
        ("mart.kpi_kinh_doanh", "revenue", "DOUBLE", "Kinh doanh", "Tier 2", "Chờ duyệt"),
    ]
    tr = "".join(
        f'<tr><td class="mono" style="color:{AC}">{a}</td><td class="mono"><b>{b}</b></td>'
        f'<td class="mono muted">{c}</td><td>{d}</td><td>{chip(e, "o" if e == "Tier 1" else "b")}</td>'
        f'<td>{chip(f, "g" if f == "Đã duyệt" else "o")}</td>'
        f'<td><span class="ico">✕</span></td></tr>'
        for a, b, c, d, e, f in cols)

    body = f"""
<div style="display:flex;gap:16px">
  <div style="flex:1.3">
    <div class="card" style="padding:16px 19px;margin-bottom:14px">
      <div class="sec">ĐỊNH NGHĨA</div>
      <div style="font-size:13.5px;line-height:1.75;color:#344054">
        Số tiền đã được ghi nhận vào sổ kế toán trong kỳ, <b>không phụ thuộc vào việc đã thu được
        tiền hay chưa</b>. Khác với <i>Doanh thu thực thu</i> — là số tiền đã thực sự về tài khoản.</div>
      <div style="margin-top:13px;display:flex;gap:7px;flex-wrap:wrap">
        {chip("CDE — Dữ liệu trọng yếu", "r")}{chip("Đã duyệt", "g")}{chip("v1.3", "t")}
        {chip("Đơn vị: VNĐ", "n")}</div>
    </div>
    <div class="card" style="padding:16px 19px;margin-bottom:14px">
      <div class="sec">THÔNG TIN QUẢN TRỊ</div>
      <table class="g" style="font-size:12.5px">
        <tr><td style="width:190px;color:#667085">Thuộc từ điển</td>
            <td>Kinh doanh › Doanh thu</td></tr>
        <tr><td style="color:#667085">Chủ sở hữu</td><td>Ban Tài chính</td></tr>
        <tr><td style="color:#667085">Người phụ trách (steward)</td><td>Phạm Thu Hà</td></tr>
        <tr><td style="color:#667085">Người duyệt</td><td>Trưởng Ban Tài chính</td></tr>
        <tr><td style="color:#667085">Bí danh</td>
            <td>{chip("Revenue", "n")}{chip("DT ghi nhận", "n")}{chip("Recognized revenue", "n")}</td></tr>
        <tr><td style="color:#667085">Thuật ngữ liên quan</td>
            <td>{chip("Doanh thu thực thu", "b")}{chip("Công nợ phải thu", "b")}</td></tr>
        <tr><td style="color:#667085">Tài liệu đính kèm</td>
            <td>📎 QĐ-412-KTTC.pdf &nbsp; 📎 Huong-dan-ghi-nhan-DT.docx</td></tr>
      </table>
    </div>
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:9px">
      <div style="font-size:13.5px;font-weight:700">Đang gắn vào 18 cột</div>
      <span class="btn">➕ Gắn thêm cột</span></div>
    <div class="card"><table class="g">
      <tr><th>Bảng</th><th>Cột</th><th>Kiểu</th><th>Miền</th><th>Mức QT</th><th>Trạng thái gắn</th><th></th></tr>
      {tr}</table>
      <div style="padding:9px 12px;font-size:12px" class="muted">… và 14 cột khác</div></div>
  </div>
  <div style="width:440px;flex-shrink:0">
    <div class="note" style="background:#ECFDF3;border:1px solid #A6F4C5;margin-bottom:13px">
      ✅ <b>Nhờ 18 liên kết này:</b> người dùng gõ <b>"doanh thu"</b>, <b>"revenue"</b> hay
      <b>"DT ghi nhận"</b> ở ô tìm kiếm menu 1.1 đều ra đúng 18 cột —
      <b>kể cả cột tên <span class="mono">tong_tien</span> hay <span class="mono">revenue</span></b>,
      vốn không chứa chữ "doanh thu".
    </div>
    <div class="card" style="padding:15px 17px;margin-bottom:13px">
      <div class="sec">VÌ SAO CỜ CDE QUAN TRỌNG</div>
      <div style="font-size:12.5px;line-height:1.8">
        Thuật ngữ đánh dấu <b>CDE</b> (Critical Data Element) kéo theo 3 hệ quả tự động:<br><br>
        ① Mọi cột mang thuật ngữ này <b>bắt buộc phải có ≥ 1 luật chất lượng</b><br>
        ② Bảng chứa cột đó <b>không được duyệt</b> nếu thiếu luật<br>
        ③ Sự cố trên cột đó được <b>nâng mức ưu tiên</b> ở menu 3.4</div>
      <div class="muted" style="font-size:11.5px;margin-top:9px">
        SQLWF đã có trường <span class="mono">cde</span> — hiện chỉ lưu, chưa dùng để ràng buộc gì.</div>
    </div>
    <div class="card" style="padding:15px 17px">
      <div class="sec">LỊCH SỬ PHIÊN BẢN</div>
      <div style="font-size:12.5px;line-height:1.85">
        <b>v1.3</b> — 12/07/2026 · P.T.Hà<br>
        <span class="muted">Làm rõ khác biệt với "Doanh thu thực thu"</span><br><br>
        <b>v1.2</b> — 03/04/2026 · P.T.Hà<br>
        <span class="muted">Bổ sung bí danh "Recognized revenue"</span><br><br>
        <b>v1.0</b> — 15/01/2026 · P.T.Hà</div>
    </div>
  </div>
</div>"""
    return shell("dmp.vds.vn/governance/glossary/TN-0042",
                 "Governance › Từ điển nghiệp vụ › Doanh thu ghi nhận",
                 "📖 Doanh thu ghi nhận",
                 "Mã TN-0042 &nbsp;·&nbsp; Kinh doanh › Doanh thu &nbsp;·&nbsp; "
                 "Chủ sở hữu: Ban Tài chính", body,
                 "DMP · Menu 2.1 — TỪ ĐIỂN NGHIỆP VỤ · Màn CHI TIẾT", "m21",
                 tabs=("Định nghĩa", ["Định nghĩa", "Cột đã gắn", "Phiên bản", "Góp ý", "Tài liệu"]),
                 actions='<span class="btn w">📎 Đính kèm</span><span class="btn">✎ Sửa</span>')


# ============================================================ 2.1 thêm thuật ngữ
def glo_create():
    body = _steps([("Định nghĩa", "now"), ("Gắn vào cột", "next"), ("Gửi duyệt", "next")]) + f"""
<div style="display:flex;gap:18px">
  <div style="width:480px;flex-shrink:0">
    <div class="card" style="padding:17px 19px">
      <div class="sec">① ĐỊNH NGHĨA THUẬT NGỮ</div>
      {fld("Mã thuật ngữ", "TN-0219 &nbsp;<span class='muted'>(tự sinh)</span>", ro=True)}
      {fld("Tên thuật ngữ", "Doanh thu thực thu", True)}
      {fld("Thuộc từ điển", "Kinh doanh › Doanh thu ▾", True,
           "Cây từ điển tối đa 3 cấp")}
      {fld("Định nghĩa", "Số tiền đã thực sự về tài khoản của công ty trong kỳ. Khác với "
                         "Doanh thu ghi nhận — là số đã vào sổ nhưng có thể chưa thu được tiền.",
           True, "Viết cho người không làm kế toán vẫn hiểu. "
                 "<b>Nếu dễ nhầm với thuật ngữ khác thì phải nói rõ khác ở đâu</b>")}
      {fld("Đơn vị tính", "VNĐ ▾")}
      {fld("Bí danh / cách gọi khác",
           chip("Cash collected", "n") + chip("DT thực thu", "n") + chip("Tiền về", "n") +
           '<span class="muted">+ Thêm</span>',
           hint="Người dùng gõ <b>bất kỳ từ nào</b> trong danh sách này đều tìm ra thuật ngữ")}
      {fld("Thuật ngữ liên quan", chip("Doanh thu ghi nhận", "b") + chip("Công nợ phải thu", "b"),
           hint="Nối các khái niệm dễ nhầm với nhau")}
      {fld("Đánh dấu CDE?", "☑ Có — dữ liệu trọng yếu",
           hint="Bật thì <b>mọi cột mang thuật ngữ này bắt buộc phải có luật chất lượng</b>, "
                "và bảng chứa nó không được duyệt nếu thiếu")}
    </div>
  </div>
  <div style="flex:1">
    <div class="card" style="padding:17px 19px;margin-bottom:13px">
      <div class="sec">② GẮN VÀO CỘT THẬT &nbsp;<span class="muted"
        style="font-weight:400;font-size:11px">(bước 2 — quan trọng nhất)</span></div>
      <div style="border:1px solid #d0d7e2;border-radius:8px;padding:8px 11px;font-size:12.5px;
        margin-bottom:10px;background:#fff">
        🔍 <span class="muted">Tìm bảng hoặc cột để gắn…</span></div>
      <table class="g" style="font-size:12px">
        <tr><th>Bảng</th><th>Cột</th><th>Kiểu</th><th></th></tr>
        <tr><td class="mono">bi.doanh_thu_thang</td><td class="mono">tien_da_thu</td>
            <td class="muted">DECIMAL</td><td style="color:#B42318">✕</td></tr>
        <tr><td class="mono">fin.cong_no</td><td class="mono">so_da_thanh_toan</td>
            <td class="muted">DECIMAL</td><td style="color:#B42318">✕</td></tr>
      </table>
      <div style="margin-top:11px;padding:9px 11px;background:#FEF3F2;border:1px solid #FECDCA;
        border-radius:7px;font-size:12.5px">
        🔴 <b>Không gắn cột nào thì thuật ngữ vô dụng.</b> Nó sẽ không xuất hiện trong kết quả
        tìm kiếm, và tab Cột của bảng cũng không hiện gì.<br>
        Hệ thống <b>cho lưu</b> nhưng đánh dấu <b>"Chưa gắn vào cột"</b> và đếm vào thẻ cảnh báo
        ở màn danh sách.</div>
    </div>
    <div class="card" style="padding:17px 19px;margin-bottom:13px">
      <div class="sec">③ QUẢN TRỊ &nbsp;<span class="muted"
        style="font-weight:400;font-size:11px">(bước 3)</span></div>
      {fld("Chủ sở hữu", "👥 Ban Tài chính ▾", True,
           "Đơn vị có quyền quyết định định nghĩa này đúng hay sai")}
      {fld("Người phụ trách (steward)", "👤 Phạm Thu Hà ▾", True,
           "Người trực tiếp bảo trì nội dung — <b>khác với chủ sở hữu</b>")}
      {fld("Người duyệt", "👤 Trưởng Ban Tài chính ▾", True,
           "Thuật ngữ ở trạng thái <b>Nháp</b> cho tới khi được duyệt")}
    </div>
    <div style="display:flex;gap:10px">
      <span class="btn">Gửi duyệt</span><span class="btn w">Lưu nháp</span>
      <span class="btn w">Huỷ</span></div>
  </div>
</div>"""
    return shell("dmp.vds.vn/governance/glossary/create",
                 "Governance › Từ điển nghiệp vụ › Thêm thuật ngữ", "➕ Thêm thuật ngữ",
                 "Định nghĩa một khái niệm nghiệp vụ và gắn nó vào các cột dữ liệu thật", body,
                 "DMP · Menu 2.1 — TỪ ĐIỂN NGHIỆP VỤ · Màn THÊM MỚI", "m21")


# ============================================================ 2.2 cây nhãn
def cls_tree():
    tree = "".join(
        f'<div style="padding:6px 10px;font-size:12.5px;border-radius:6px;margin-bottom:2px;'
        f'{"background:#EFF4FF;font-weight:700;color:" + AC if on else ""}">{ind}{t}'
        f'<span class="muted" style="float:right;font-weight:400">{c}</span></div>'
        for ind, t, c, on in [
            ("", "🗂️ PII — Thông tin cá nhân", "412 cột", False),
            ("&nbsp;&nbsp;", "🏷️ PD_BASIC — cá nhân cơ bản", "268", False),
            ("&nbsp;&nbsp;", "🏷️ PD_SENSITIVE — cá nhân nhạy cảm", "144", True),
            ("", "🗂️ TaiChinh — Dữ liệu tài chính", "186 cột", False),
            ("&nbsp;&nbsp;", "🏷️ TaiChinh.DoanhThu", "118", False),
            ("&nbsp;&nbsp;", "🏷️ TaiChinh.ChiPhi", "68", False),
            ("", "🗂️ NoiBo — Dữ liệu nội bộ", "94 cột", False),
            ("", "🏷️ DATA_GENERAL — thông thường", "95.708", False),
        ])
    pol = "".join(
        f'<tr><td>{a}</td><td>{chip(b, c)}</td><td>{d}</td></tr>'
        for a, b, c, d in [
            ("👥 ban_kinh_doanh", "Hiện 4 số cuối", "o", "5.2 › tab Che dữ liệu"),
            ("👥 ctv_thue_ngoai", "Băm (hash)", "o", "5.2 › tab Che dữ liệu"),
            ("👥 doi_de", "Không che", "g", "5.2 › tab Quyền dữ liệu"),
            ("Mọi truy vấn", "Ghi nhật ký", "b", "5.4 › Nhật ký kiểm toán")])
    cols = "".join(
        f'<tr><td class="mono" style="color:{AC}">{a}</td><td class="mono">{b}</td>'
        f'<td>{c}</td><td>{d}</td></tr>'
        for a, b, c, d in [
            ("bi.doi_soat_giao_dich_A", "so_dien_thoai", "Kinh doanh", chip("Tier 1", "o")),
            ("dwh.thue_bao_ngay", "so_tb", "Kinh doanh", chip("Tier 1", "o")),
            ("crm.khach_hang", "dien_thoai", "Kinh doanh", chip("Tier 2", "b")),
            ("crm.khach_hang", "so_cccd", "Kinh doanh", chip("Tier 2", "b"))])

    body = f"""
<div style="display:flex;gap:18px">
  <div style="width:340px;flex-shrink:0">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
      <div style="font-size:12.5px;font-weight:700">CÂY NHÃN PHÂN LOẠI</div>
      <span class="btn" style="padding:4px 10px;font-size:11.5px">➕ Thêm nhãn</span></div>
    <div class="card" style="padding:9px">{tree}</div>
    <div class="note" style="background:#FFFAEB;border:1px solid #FEDF89;margin-top:12px">
      ⚠️ <b>SQLWF hiện chỉ có 3 nhãn phẳng</b> — `PD_BASIC`, `PD_SENSITIVE`, `DATA_GENERAL`.<br>
      Cần thêm <b>phân cấp</b> để chính sách viết ở nhánh cha tự áp cho mọi nhánh con.
    </div>
  </div>
  <div style="flex:1">
    <div class="card" style="padding:16px 19px;margin-bottom:14px">
      <div class="sec">NHÃN ĐANG CHỌN — PD_SENSITIVE</div>
      <table class="g" style="font-size:12.5px">
        <tr><td style="width:190px;color:#667085">Mã nhãn</td>
            <td class="mono"><b>PD_SENSITIVE</b></td></tr>
        <tr><td style="color:#667085">Tên hiển thị</td><td>Dữ liệu cá nhân nhạy cảm</td></tr>
        <tr><td style="color:#667085">Nhãn cha</td><td>PII — Thông tin cá nhân</td></tr>
        <tr><td style="color:#667085">Mức nhạy cảm</td><td>{chip("🔴 Cao", "r")}</td></tr>
        <tr><td style="color:#667085">Mô tả</td>
            <td>Số điện thoại, CCCD, sinh trắc học, thông tin sức khoẻ và tài chính cá nhân</td></tr>
        <tr><td style="color:#667085">Căn cứ pháp lý</td>
            <td>Nghị định 13/2023/NĐ-CP về bảo vệ dữ liệu cá nhân</td></tr>
      </table>
    </div>
    <div class="card" style="padding:16px 19px;margin-bottom:14px;background:#FEF3F2;
      border-color:#FECDCA">
      <div class="sec" style="color:#B42318;border-color:#B42318">
        ⚡ 4 CHÍNH SÁCH TỰ ÁP CHO MỌI CỘT MANG NHÃN NÀY</div>
      <table class="g" style="font-size:12.5px;background:#fff">
        <tr><th>Áp cho ai</th><th>Hành động</th><th>Khai ở đâu</th></tr>{pol}</table>
      <div style="font-size:12.5px;margin-top:10px">
        ⭐ <b>Đây là giá trị lớn nhất của việc gắn nhãn:</b> khai 4 chính sách một lần,
        áp cho <b>144 cột</b> hiện tại và <b>mọi cột gắn nhãn sau này</b> — không phải khai lại.</div>
    </div>
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:9px">
      <div style="font-size:13.5px;font-weight:700">144 cột đang mang nhãn này</div>
      <div style="display:flex;gap:8px"><span class="btn w">🤖 Xem 23 cột hệ thống nghi ngờ</span>
        <span class="btn w">⬇️ Xuất danh sách</span></div></div>
    <div class="card"><table class="g">
      <tr><th>Bảng</th><th>Cột</th><th>Miền</th><th>Mức QT</th></tr>{cols}</table>
      <div style="padding:9px 12px;font-size:12px" class="muted">… và 140 cột khác</div></div>
  </div>
</div>"""
    return shell("dmp.vds.vn/governance/classification", "Governance › Phân loại & Nhãn",
                 "🏷️ Phân loại & Nhãn",
                 "Đánh dấu dữ liệu nhạy cảm một lần — chính sách bảo mật tự áp theo nhãn",
                 body, "DMP · Menu 2.2 — PHÂN LOẠI & NHÃN · Màn CÂY NHÃN + CHI TIẾT", "m22")


# ============================================================ 2.2 thêm nhãn
def cls_create():
    body = f"""
<div style="display:flex;gap:18px">
  <div style="width:500px;flex-shrink:0">
    <div class="card" style="padding:17px 19px">
      <div class="sec">THÔNG TIN NHÃN</div>
      {fld("Mã nhãn", "PD_BIOMETRIC", True,
           "Viết HOA, không dấu, dùng gạch dưới. Đây là mã <b>đồng bộ sang OPA</b> "
           "nên không đổi được sau khi tạo", mono=True)}
      {fld("Tên hiển thị", "Dữ liệu sinh trắc học", True)}
      {fld("Nhãn cha", "PII — Thông tin cá nhân ▾",
           hint="Chính sách khai ở nhãn cha <b>tự áp xuống mọi nhãn con</b>")}
      {fld("Mức nhạy cảm", "🔴 Cao ▾", True,
           "Cao / Trung bình / Thấp — quyết định <b>kiểu che mặc định</b> khi gắn nhãn cho cột mới")}
      {fld("Mô tả", "Vân tay, khuôn mặt, giọng nói và các dữ liệu sinh trắc học khác.", True)}
      {fld("Căn cứ pháp lý", "Nghị định 13/2023/NĐ-CP — Điều 2 khoản 4",
           hint="Ghi để phục vụ kiểm toán tuân thủ")}
    </div>
  </div>
  <div style="flex:1">
    <div class="card" style="padding:17px 19px;margin-bottom:13px">
      <div class="sec">CHÍNH SÁCH MẶC ĐỊNH KHI GẮN NHÃN NÀY</div>
      <table class="g" style="font-size:12.5px">
        <tr><th>Nhóm người dùng</th><th>Hành động mặc định</th><th></th></tr>
        <tr><td>👥 ctv_thue_ngoai</td><td>{chip("Trả về NULL", "r")}</td>
            <td style="color:#B42318">✕</td></tr>
        <tr><td>👥 ban_kinh_doanh</td><td>{chip("Băm (hash)", "o")}</td>
            <td style="color:#B42318">✕</td></tr>
        <tr><td>👥 doi_de</td><td>{chip("Không che", "g")}</td>
            <td style="color:#B42318">✕</td></tr>
        <tr><td colspan="3" style="color:#8b95a7">+ Thêm nhóm</td></tr>
      </table>
      <div class="muted" style="font-size:11.5px;margin-top:9px">
        Đây là <b>mặc định</b> — vẫn sửa được cho từng cột cụ thể ở menu 5.2 nếu có ngoại lệ.</div>
    </div>
    <div class="note" style="background:#EFF4FF;border:1px solid #C7D7FE;margin-bottom:13px">
      🔗 <b>Khai ở đây, dùng ở đâu</b><br><br>
      <b>Mã nhãn</b> → ô chọn nhãn ở <b>tab Cột của 1.1</b> · đồng bộ sang <b>OPA</b><br>
      <b>Chính sách mặc định</b> → tự sinh chính sách ở <b>5.2 › tab Theo nhãn</b><br>
      <b>Mức nhạy cảm</b> → quyết định kiểu che gợi ý khi gắn nhãn cho cột mới<br>
      <b>Số cột mang nhãn</b> → thẻ số liệu ở <b>1.1</b> và <b>6.1 Sức khoẻ dữ liệu</b>
    </div>
    <div class="note" style="background:#FFFAEB;border:1px solid #FEDF89">
      ⚠️ <b>Không xoá được nhãn đang gắn cho cột.</b> Phải gỡ nhãn khỏi toàn bộ cột trước —
      hệ thống chặn và hiện danh sách cột còn lại.<br>
      Lý do: xoá nhãn đồng nghĩa <b>gỡ bỏ chính sách bảo mật</b> trên các cột đó mà không ai hay.
    </div>
    <div style="display:flex;gap:10px;margin-top:16px">
      <span class="btn">💾 Lưu nhãn</span><span class="btn w">Huỷ</span></div>
  </div>
</div>"""
    return shell("dmp.vds.vn/governance/classification/create",
                 "Governance › Phân loại & Nhãn › Thêm nhãn", "➕ Thêm nhãn phân loại",
                 "Khai một nhãn mới vào cây phân loại, kèm chính sách bảo mật mặc định", body,
                 "DMP · Menu 2.2 — PHÂN LOẠI & NHÃN · Màn THÊM MỚI", "m22")


SCREENS = {
    "dmp-16-glossary-list": glo_list,
    "dmp-17-glossary-detail": glo_detail,
    "dmp-18-glossary-create": glo_create,
    "dmp-19-classification-tree": cls_tree,
    "dmp-20-classification-create": cls_create,
}
