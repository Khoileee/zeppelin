# -*- coding: utf-8 -*-
"""DMP — Module ⑤ Data Security: 5.1 Người dùng, 5.2 Chính sách, 5.3 Yêu cầu, 5.4 Nhật ký, 5.5 Báo cáo."""
from dmp import shell, fld, chip, AC
from s_dmp2 import _kpi
from s_dmp3 import _steps

P_TABS = ["Quyền dữ liệu", "Che dữ liệu", "Lọc theo dòng", "Chính sách theo nhãn"]
P_CRUMB = "Data Security › Chính sách truy cập"
P_TITLE = "🔐 Chính sách truy cập"
P_DESC = "Một nơi duy nhất cho mọi chính sách trên DỮ LIỆU — không phải quyền vào menu"
P_ACT = ('<span class="btn w">⬇️ Xuất chính sách</span>'
         '<span class="btn">➕ Thêm chính sách</span>')


# ============================================================ 5.1 danh sách người dùng
def user_list():
    rows = [
        ("nguyen.thi.phuong", "Nguyễn Thị Phương", "BDA — Ban Kinh doanh",
         "ban_kinh_doanh · bda_kinh_doanh", "PD_SENSITIVE", "12 bảng", "Hoạt động"),
        ("tran.van.hung", "Trần Văn Hùng", "DE — Đội Dữ liệu",
         "doi_de · van_hanh_du_lieu", "DATA_GENERAL", "148 bảng", "Hoạt động"),
        ("pham.thu.ha", "Phạm Thu Hà", "BDA — Ban Tài chính",
         "ban_tai_chinh", "PD_BASIC", "24 bảng", "Hoạt động"),
        ("le.minh.tuan", "Lê Minh Tuấn", "Chuyên viên — Ban Sản phẩm",
         "ban_san_pham", "DATA_GENERAL", "6 bảng", "Hoạt động"),
        ("ctv.nguyen.an", "Nguyễn An (thuê ngoài)", "Cộng tác viên",
         "ctv_thue_ngoai", "—", "2 bảng", "Hết hạn 30/08"),
        ("vo.thi.lan", "Võ Thị Lan", "Đã nghỉ việc 15/06/2026",
         "ban_kinh_doanh", "PD_BASIC", "18 bảng", "Chưa khoá"),
    ]
    tr = ""
    for u, nm, role, grp, tag, ntbl, st in rows:
        stc = "g" if st == "Hoạt động" else ("r" if st == "Chưa khoá" else "o")
        nmc = ('<b style="color:#B42318">' + nm + "</b>") if "nghỉ việc" in role else f"<b>{nm}</b>"
        tr += (f'<tr><td class="mono" style="color:{AC}">{u}</td><td>{nmc}</td>'
               f'<td class="muted">{role}</td><td class="mono" style="font-size:11.5px">{grp}</td>'
               f'<td>{chip(tag, "r" if tag == "PD_SENSITIVE" else "n") if tag != "—" else "—"}</td>'
               f'<td style="text-align:center">{ntbl}</td>'
               f'<td>{chip(st, stc)}</td>'
               f'<td style="white-space:nowrap"><span class="ico">👁</span>'
               f'<span class="ico">✎</span></td></tr>')

    body = _kpi([
        ("TỔNG SỐ TÀI KHOẢN", "612", "584 hoạt động · 28 hết hạn", "#101828"),
        ("NHÓM NGƯỜI DÙNG", "47", "trung bình 13 người / nhóm", "#101828"),
        ("TÀI KHOẢN ĐÃ NGHỈ VIỆC CHƯA KHOÁ", "9", "vẫn còn quyền trên 132 bảng", "#B42318"),
        ("QUYỀN KHÔNG DÙNG 90 NGÀY", "1.204", "ứng viên thu hồi tự động", "#B54708"),
        ("TÀI KHOẢN CÓ QUYỀN PD_SENSITIVE", "38", "cần rà soát định kỳ hằng quý", "#B54708"),
    ]) + f"""
<div style="display:flex;gap:10px;margin-bottom:13px;align-items:center">
  <div style="flex:1;border:1px solid #d0d7e2;border-radius:8px;padding:9px 13px;font-size:13px;
    background:#fff">🔍 <span class="muted">Tìm theo tài khoản, tên, đơn vị…</span></div>
  <span class="btn w">Nhóm: tất cả ▾</span><span class="btn w">Trạng thái ▾</span>
  <span class="btn w">Đã nghỉ việc chưa khoá ☐</span>
</div>
<div class="card"><table class="g">
  <tr><th>Tài khoản</th><th>Họ tên</th><th>Vai trò · Đơn vị</th><th>Thuộc nhóm</th>
    <th>Nhãn người dùng</th><th style="text-align:center">Số bảng có quyền</th>
    <th>Trạng thái</th><th></th></tr>{tr}</table></div>
<div style="display:flex;gap:14px;margin-top:14px">
  <div class="card" style="flex:1;padding:15px 18px">
    <div class="sec">PHÂN BIỆT HAI LOẠI QUYỀN — CHỖ HAY NHẦM NHẤT CỦA CẢ MODULE</div>
    <table class="g" style="font-size:12.5px">
      <tr><th></th><th>Quyền MENU</th><th>Quyền DỮ LIỆU</th></tr>
      <tr><td style="width:130px;color:#667085"><b>Trả lời câu hỏi</b></td>
          <td>Người này <b>mở được màn nào</b></td>
          <td>Người này <b>đọc được dòng nào, cột nào</b></td></tr>
      <tr><td style="color:#667085"><b>Khai ở đâu</b></td>
          <td><b>Menu 5.1</b> — màn này</td><td><b>Menu 5.2</b></td></tr>
      <tr><td style="color:#667085"><b>SQLWF hiện có</b></td>
          <td class="mono">acl · feature-menu-authorization · group-authorize</td>
          <td class="mono">data-authorize · file-view-group · tags</td></tr>
      <tr><td style="color:#667085"><b>Việc</b></td>
          <td>{chip("🟢 Giữ nguyên", "g")}</td><td>{chip("🔵 Nâng cấp + gộp", "b")}</td></tr>
    </table>
    <div class="note" style="background:#FFFAEB;border:1px solid #FEDF89;margin-top:11px">
      ⚠️ <b>Vì sao tách hai loại này ra:</b> mở được màn <i>Truy vấn dữ liệu</i>
      <b>không có nghĩa</b> là đọc được mọi bảng trong đó.<br>
      Hiện SQLWF trộn hai loại vào cùng một màn <span class="mono">user-managerment</span> —
      các cột <i>Phân quyền truy cập dữ liệu</i> · <i>Phân quyền File View</i> ·
      <i>Phân quyền danh mục</i> · <i>Phân quyền PYC</i> nằm cạnh nhau, người khai
      <b>rất khó biết mình đang cấp cái gì</b>.
    </div>
  </div>
  <div style="width:500px;flex-shrink:0">
    <div class="note" style="background:#ECFDF3;border:1px solid #A6F4C5;margin-bottom:13px">
      ✅ <b>Menu này SQLWF đã đủ — giữ nguyên.</b><br>
      <span class="mono">user-managerment</span> · <span class="mono">group-management</span> ·
      <span class="mono">acl</span> (ma trận Menu chức năng × Quyền) ·
      <span class="mono">feature-menu-authorization</span> ·
      <span class="mono">group-authorize</span> (nhóm quyền gắn với menu).<br><br>
      Chỉ <b>chuyển 4 cột phân quyền dữ liệu sang menu 5.2</b>, để mỗi màn làm đúng một việc.
    </div>
    <div class="note" style="background:#FEF3F2;border:1px solid #FECDCA">
      🔴 <b>Chín tài khoản đã nghỉ việc nhưng chưa khoá</b> — vẫn còn quyền trên 132 bảng.<br><br>
      Đây không phải lỗi thiết kế, mà là hệ quả của việc <b>quyền không có thời hạn</b>.
      Menu <b>5.3</b> sửa chuyện này bằng cách bắt <b>mọi quyền cấp mới phải có ngày hết hạn</b>,
      và menu <b>5.5</b> cho phép rà soát định kỳ theo người.
    </div>
  </div>
</div>"""
    return shell("dmp.vds.vn/security/users", "Data Security › Người dùng &amp; Nhóm",
                 "👥 Người dùng &amp; Nhóm",
                 "Tài khoản, nhóm, vai trò và quyền truy cập MENU",
                 body, "DMP · Menu 5.1 — NGƯỜI DÙNG &amp; NHÓM · Màn DANH SÁCH", "m51",
                 tabs=("Người dùng", ["Người dùng", "Nhóm", "Vai trò", "Quyền menu (ACL)"]),
                 actions='<span class="btn w">📥 Đồng bộ từ LDAP</span>'
                         '<span class="btn">➕ Thêm tài khoản</span>')


# ============================================================ 5.2 tab Quyền dữ liệu
def pol_data():
    rows = [
        ("👥 ban_kinh_doanh", "Nhóm", "🧩 Miền Kinh doanh", "Xem", "—", "Vô thời hạn",
         "Thủ công", "Đang áp"),
        ("👥 doi_de", "Nhóm", "📦 Nhóm bảng: Kho dữ liệu thô", "Xem · Ghi · Xoá", "—",
         "Vô thời hạn", "Thủ công", "Đang áp"),
        ("👥 ban_tai_chinh", "Nhóm", "🗂️ bi.doanh_thu_thang", "Xem", "—", "Vô thời hạn",
         "Thủ công", "Đang áp"),
        ("👤 le.minh.tuan", "Người", "🗂️ bi.doi_soat_giao_dich_A", "Xem",
         "so_dien_thoai · so_cccd", "Hết hạn 15/08/2026", "Từ yêu cầu YC-0188", "Đang áp"),
        ("👥 ctv_thue_ngoai", "Nhóm", "🗂️ raw.doi_soat_A_tho", "Xem",
         "toàn bộ cột PD_SENSITIVE", "Hết hạn 30/08/2026", "Từ yêu cầu YC-0201", "Đang áp"),
        ("👤 vo.thi.lan", "Người", "🧩 Miền Kinh doanh", "Xem", "—", "Vô thời hạn",
         "Thủ công", "Cần thu hồi"),
    ]
    tr = ""
    for who, kind, scope, perm, excl, term, src, st in rows:
        tr += (f'<tr><td><b>{who}</b></td><td class="muted">{kind}</td><td>{scope}</td>'
               f'<td>{perm}</td>'
               f'<td class="mono" style="font-size:11.5px;color:#B42318">{excl}</td>'
               f'<td>{chip(term, "n" if term.startswith("Vô") else "o")}</td>'
               f'<td class="muted" style="font-size:11.5px">{src}</td>'
               f'<td>{chip(st, "g" if st == "Đang áp" else "r")}</td>'
               f'<td style="white-space:nowrap"><span class="ico">✎</span>'
               f'<span class="ico">✕</span></td></tr>')

    body = _kpi([
        ("TỔNG SỐ CHÍNH SÁCH", "1.847", "412 theo nhóm · 1.435 theo người", "#101828"),
        ("CHÍNH SÁCH VÔ THỜI HẠN", "1.612", "87% — nguồn gốc của quyền tồn đọng", "#B42318"),
        ("CẤP THEO NGƯỜI THAY VÌ NHÓM", "1.435", "khó rà soát, khó thu hồi", "#B54708"),
        ("CẦN THU HỒI", "132", "chủ tài khoản đã nghỉ việc", "#B42318"),
    ]) + f"""
<div style="display:flex;gap:10px;margin-bottom:13px;align-items:center">
  <div style="flex:1;border:1px solid #d0d7e2;border-radius:8px;padding:9px 13px;font-size:13px;
    background:#fff">🔍 <span class="muted">Tìm theo người dùng, nhóm, bảng…</span></div>
  <span class="btn w">Phạm vi: tất cả ▾</span><span class="btn w">Nguồn: tất cả ▾</span>
  <span class="btn w">Chỉ vô thời hạn ☐</span><span class="btn w">Cần thu hồi ☐</span>
</div>
<div class="card"><table class="g">
  <tr><th>Đối tượng</th><th>Loại</th><th>Phạm vi</th><th>Quyền</th><th>Cột loại trừ</th>
    <th>Thời hạn</th><th>Nguồn</th><th>Trạng thái</th><th></th></tr>{tr}</table></div>
<div style="display:flex;gap:14px;margin-top:14px">
  <div class="card" style="flex:1;padding:15px 18px">
    <div class="sec">BỐN CẤP PHẠM VI — CẤP CÀNG RỘNG CÀNG ÍT VIỆC BẢO TRÌ</div>
    <table class="g" style="font-size:12.5px">
      <tr><th>Phạm vi</th><th>Nghĩa</th><th>Nên dùng khi</th></tr>
      <tr><td>🧩 <b>Miền dữ liệu</b></td><td>Mọi bảng thuộc miền, <b>kể cả bảng khai sau này</b></td>
          <td>Cấp cho cả một ban nghiệp vụ</td></tr>
      <tr><td>📦 <b>Nhóm bảng</b></td><td>Các bảng trong nhóm khai ở 1.2</td>
          <td>Một bộ bảng dùng chung cho một việc</td></tr>
      <tr><td>🗂️ <b>Một bảng</b></td><td>Đúng một bảng</td><td>Ngoại lệ</td></tr>
      <tr><td>📁 <b>Thư mục HDFS</b></td>
          <td>Read · Write · Execute · Encrypted · Erasure Coding · Apply all children</td>
          <td>Truy cập tệp thô, không qua SQL</td></tr>
    </table>
    <div class="note" style="background:#FFFAEB;border:1px solid #FEDF89;margin-top:11px">
      ⚠️ <b>1.435 / 1.847 chính sách đang cấp theo TỪNG NGƯỜI.</b> Đây là lý do không ai
      trả lời được câu <i>"người này đang có quyền gì"</i> mà không mở 4 màn kiểm tra tay.<br>
      Cấp theo <b>nhóm</b> và theo <b>miền</b> thì người vào / ra chỉ cần đổi nhóm — không
      phải sửa hàng trăm dòng chính sách.
    </div>
  </div>
  <div style="width:500px;flex-shrink:0">
    <div class="note" style="background:#ECFDF3;border:1px solid #A6F4C5;margin-bottom:13px">
      ✅ <b>Tab này gộp 3 màn đã có, giữ nguyên phần chạy:</b><br>
      <span class="mono">data-authorize</span> — nhóm dữ liệu gắn với thư mục<br>
      <span class="mono">file-view-group</span> — quyền thư mục HDFS đầy đủ:
      <b>Read · Write · Execute · Encrypted · Erasure Coding · Apply all children</b><br>
      <span class="mono">tags</span> — nhãn người dùng, đồng bộ sang <b>OPA</b><br><br>
      Phần thêm: <b>phạm vi theo miền và theo nhóm bảng</b> · <b>cột loại trừ</b> ·
      <b>thời hạn</b> · <b>nguồn chính sách</b>.
    </div>
    <div class="note" style="background:#EFF4FF;border:1px solid #C7D7FE">
      🔗 <b>Cột "Nguồn" trả lời câu hỏi kiểm toán quan trọng nhất:</b>
      <i>"Ai cấp quyền này, căn cứ vào đâu?"</i><br><br>
      <b>Thủ công</b> — quản trị viên tự thêm<br>
      <b>Từ yêu cầu YC-xxxx</b> — sinh ra từ menu <b>5.3</b>, có người xin và người duyệt<br>
      <b>Từ nhãn</b> — sinh tự động từ tab <b>Chính sách theo nhãn</b><br><br>
      Chính sách <b>không có nguồn rõ ràng</b> là thứ đầu tiên bị soi khi kiểm toán.
    </div>
  </div>
</div>"""
    return shell("dmp.vds.vn/security/policies/data", P_CRUMB, P_TITLE, P_DESC, body,
                 "DMP · Menu 5.2 — CHÍNH SÁCH TRUY CẬP · Tab QUYỀN DỮ LIỆU", "m52",
                 tabs=("Quyền dữ liệu", P_TABS), actions=P_ACT)


# ============================================================ 5.2 tab Che dữ liệu
MASK_ROWS = [
    ("Hiện 4 số cuối", "0987654321", "******4321",
     "Đối soát, chăm sóc khách hàng — đủ để nhận ra khách nhưng không lộ số"),
    ("Hiện 4 số đầu", "0987654321", "0987******", "Phân tích theo đầu số / nhà mạng"),
    ("Băm không đảo ngược (hash)", "0987654321", "a3f9c2e81b4d…",
     "⭐ Vẫn <b>đếm phân biệt</b> và <b>nối bảng</b> được, nhưng không đọc ra giá trị gốc"),
    ("Che toàn bộ", "Nguyễn Văn A", "xxxxxxxxxxx", "Chỉ cần biết ô có dữ liệu hay không"),
    ("Trả về rỗng (NULL)", "0987654321", "NULL", "Cột hoàn toàn không được phép thấy"),
    ("Chỉ hiện năm", "15/03/1989", "1989", "Phân tích theo độ tuổi, không lộ ngày sinh"),
    ("Làm tròn số", "12.480.331", "12.000.000", "Xem quy mô, không xem số chính xác"),
    ("Biểu thức tự viết", "0987654321", "CONCAT('84', SUBSTR({col},2))",
     "Trường hợp đặc thù — dùng biến {col} thay cho tên cột"),
]


def pol_mask():
    mk = "".join(
        f'<tr><td><b>{a}</b></td><td class="mono" style="font-size:11.5px">{b}</td>'
        f'<td class="mono" style="font-size:11.5px;color:#B54708">{c}</td>'
        f'<td class="muted">{d}</td></tr>' for a, b, c, d in MASK_ROWS)

    pol = "".join(
        f'<tr><td class="mono" style="color:{AC};font-size:11.5px">{a}</td>'
        f'<td class="mono" style="font-size:11.5px"><b>{b}</b></td>'
        f'<td>{chip(c, "r" if c == "PD_SENSITIVE" else "n")}</td><td>{d}</td>'
        f'<td style="white-space:nowrap">{chip(e, f)}</td>'
        f'<td class="mono" style="font-size:11px;color:#B54708">{g}</td>'
        f'<td class="muted" style="font-size:11.5px">{h}</td></tr>'
        for a, b, c, d, e, f, g, h in [
            ("bi.doi_soat_giao_dich_A", "so_dien_thoai", "PD_SENSITIVE", "👥 ban_kinh_doanh",
             "Hiện 4 số cuối", "o", "******4321", "Từ nhãn"),
            ("bi.doi_soat_giao_dich_A", "so_dien_thoai", "PD_SENSITIVE", "👥 ctv_thue_ngoai",
             "Băm (hash)", "o", "a3f9c2e8…", "Từ nhãn"),
            ("bi.doi_soat_giao_dich_A", "so_dien_thoai", "PD_SENSITIVE", "👥 doi_de",
             "Không che", "g", "0987654321", "Ngoại lệ thủ công"),
            ("crm.khach_hang", "so_cccd", "PD_SENSITIVE", "👥 ban_kinh_doanh",
             "Trả về NULL", "r", "NULL", "Từ nhãn"),
            ("crm.khach_hang", "ngay_sinh", "PD_BASIC", "👥 ban_kinh_doanh",
             "Chỉ hiện năm", "o", "1989", "Từ nhãn"),
            ("fin.luong_nhan_vien", "muc_luong", "PD_SENSITIVE", "Mọi nhóm trừ ban_nhan_su",
             "Trả về NULL", "r", "NULL", "Thủ công")])

    body = _kpi([
        ("CỘT ĐANG ĐƯỢC CHE", "0", "⭐ chưa có tính năng này trong SQLWF", "#B42318"),
        ("CỘT MANG NHÃN PD_SENSITIVE", "144", "đều đang hiện nguyên giá trị cho mọi người có quyền xem",
         "#B42318"),
        ("CỘT MANG NHÃN PD_BASIC", "268", "cần rà soát mức che phù hợp", "#B54708"),
        ("SỐ CHÍNH SÁCH CHE SẼ SINH TỰ ĐỘNG", "412", "từ nhãn, không phải khai tay từng cột",
         "#067647"),
    ]) + f"""
<div class="card" style="padding:16px 19px;margin-bottom:14px;background:#FEF3F2;
  border-color:#FECDCA">
  <div class="sec" style="color:#B42318;border-color:#B42318">
    ⚠️ TÍNH NĂNG CHƯA TỒN TẠI TRONG SQLWF — ĐÃ KIỂM TRA MÃ NGUỒN</div>
  <div style="font-size:12.5px;line-height:1.75;color:#344054">
    Mã nguồn <b>không có trường <span class="mono">maskType</span> nào</b>, ở bất kỳ thực thể nào.
    Cơ chế bảo mật hiện tại qua OPA là <b>chặn HÀM SQL theo nhãn</b>
    (<span class="mono">TagFunctionBlacklist</span>) — tức là cấm dùng một số hàm trên cột nhạy cảm,
    <b>không phải che giá trị</b>.<br>
    Kết quả: <b>144 cột PD_SENSITIVE hiện vẫn trả về số điện thoại và CCCD nguyên vẹn</b>
    cho mọi người có quyền xem bảng.
  </div>
</div>
<div style="display:flex;gap:16px">
  <div style="flex:1.35">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:9px">
      <div style="font-size:13.5px;font-weight:700">Chính sách che đang áp</div>
      <span class="btn">➕ Thêm chính sách che</span></div>
    <div class="card" style="margin-bottom:14px"><table class="g">
      <tr><th>Bảng</th><th>Cột</th><th>Nhãn</th><th>Áp cho</th><th>Kiểu che</th>
        <th>Người dùng thấy</th><th>Nguồn</th></tr>{pol}</table></div>
    <div class="card" style="padding:16px 19px">
      <div class="sec">TÁM KIỂU CHE — CHỌN THEO VIỆC NGƯỜI DÙNG CẦN LÀM</div>
      <table class="g" style="font-size:12.5px">
        <tr><th>Kiểu che</th><th>Giá trị gốc</th><th>Người dùng thấy</th>
          <th>Chọn khi</th></tr>{mk}</table>
      <div class="muted" style="font-size:11.5px;margin-top:9px">
        Danh sách này đối chiếu với <b>Apache Ranger</b> — công cụ phân quyền dữ liệu phổ biến nhất
        trong hệ sinh thái Hadoop, và là thứ đội hạ tầng đã quen. Xem tài liệu nghiên cứu thị trường.</div>
    </div>
  </div>
  <div style="width:520px;flex-shrink:0">
    <div class="card" style="padding:15px 17px;margin-bottom:13px">
      <div class="sec">CHE Ở ĐÂU TRONG ĐƯỜNG ĐI CỦA CÂU TRUY VẤN</div>
      <div style="font-size:12.5px;line-height:1.9;background:#F8FAFC;border-radius:8px;
        padding:12px 14px;font-family:Consolas,monospace">
        ① Người dùng gõ &nbsp;<span style="color:#7C3AED">SELECT</span> so_dien_thoai …<br>
        ② DMP <b>viết lại câu SQL</b> trước khi gửi xuống engine<br>
        &nbsp;&nbsp;&nbsp;→ <span style="color:#B54708">CONCAT('******', RIGHT(so_dien_thoai,4))</span><br>
        ③ Engine chạy câu <b>đã viết lại</b><br>
        ④ Kết quả trả về <b>đã bị che sẵn</b>
      </div>
      <div class="note" style="background:#ECFDF3;border:1px solid #A6F4C5;margin-top:11px;
        font-size:12.5px">
        ⭐ <b>Điểm mấu chốt: che ở tầng viết lại câu truy vấn, không phải ở tầng giao diện.</b><br>
        Nếu chỉ che trên màn hình thì người dùng <b>xuất Excel</b> hoặc <b>gọi API</b> là ra
        giá trị gốc. Che bằng viết lại SQL thì <b>mọi đường ra đều đã bị che</b>.
      </div>
    </div>
    <div class="note" style="background:#FFFAEB;border:1px solid #FEDF89;margin-bottom:13px">
      ⚠️ <b>Hai lỗ hổng phải bịt cùng lúc, nếu không che chỉ là hình thức</b><br><br>
      ① <b>Quyền ghi có thể lách che.</b> Ai có quyền sửa cấu trúc bảng thì có thể tạo bảng mới
      từ dữ liệu gốc rồi đọc thoải mái. Đây là hạn chế <b>đã ghi nhận trong tài liệu Apache Ranger</b>
      — người có quyền <span class="mono">ALTER</span> bỏ qua được che.<br>
      → <b>Cách bịt:</b> tách quyền ghi khỏi quyền đọc trên cột nhạy cảm, và ghi nhật ký mọi lệnh
      tạo bảng từ bảng có cột được che.<br><br>
      ② <b>Đường vào thẳng HDFS.</b> Che chỉ áp cho truy vấn SQL. Ai đọc được tệp Parquet gốc
      thì thấy nguyên dữ liệu.<br>
      → <b>Cách bịt:</b> siết quyền thư mục ở tab <i>Quyền dữ liệu</i> — chỉ tài khoản dịch vụ
      được đọc thư mục thô.
    </div>
    <div class="note" style="background:#EFF4FF;border:1px solid #C7D7FE">
      💡 <b>Kiểu "Băm (hash)" đáng chú ý nhất về mặt nghiệp vụ.</b><br><br>
      Cùng một số điện thoại luôn cho ra cùng một chuỗi băm → vẫn <b>đếm được số thuê bao
      phân biệt</b> và vẫn <b>nối được hai bảng theo số điện thoại</b>, mà <b>không ai đọc
      ra số thật</b>.<br><br>
      Đây là kiểu che nên dùng mặc định cho <b>cộng tác viên thuê ngoài</b> — họ vẫn làm được
      phân tích, chỉ không lấy được dữ liệu khách hàng ra ngoài.
    </div>
  </div>
</div>"""
    return shell("dmp.vds.vn/security/policies/mask", P_CRUMB, P_TITLE, P_DESC, body,
                 "DMP · Menu 5.2 — CHÍNH SÁCH TRUY CẬP · Tab CHE DỮ LIỆU (mới hoàn toàn)", "m52",
                 tabs=("Che dữ liệu", P_TABS), actions=P_ACT)


# ============================================================ 5.2 tab Lọc theo dòng
def pol_rowfilter():
    rows = [
        ("🗂️ bi.doi_soat_giao_dich_A", "👥 ban_kinh_doanh_mien_bac",
         "ma_chi_nhanh IN ('HN','HP','QN','TB')", "Chỉ thấy giao dịch của chi nhánh miền Bắc"),
        ("🗂️ bi.doi_soat_giao_dich_A", "👥 ctv_thue_ngoai",
         "ngay_giao_dich &gt;= CURRENT_DATE - 30", "Chỉ thấy 30 ngày gần nhất"),
        ("🗂️ crm.khach_hang", "👥 ban_kinh_doanh",
         "ma_chi_nhanh = ${chi_nhanh_cua_nguoi_dung}",
         "⭐ Biến động — mỗi người thấy đúng chi nhánh của mình"),
        ("🗂️ dwh.thue_bao_ngay", "👥 ban_san_pham",
         "loai_thue_bao = 'TRA_TRUOC'", "Chỉ phụ trách nhóm trả trước"),
        ("🗂️ fin.luong_nhan_vien", "👥 truong_phong",
         "ma_don_vi = ${don_vi_cua_nguoi_dung}", "Chỉ thấy nhân sự đơn vị mình"),
    ]
    tr = "".join(
        f'<tr><td class="mono" style="color:{AC};font-size:11.5px">{a}</td><td>{b}</td>'
        f'<td class="mono" style="font-size:11.5px;background:#F8FAFC">{c}</td>'
        f'<td class="muted">{d}</td>'
        f'<td style="white-space:nowrap"><span class="ico">✎</span>'
        f'<span class="ico">✕</span></td></tr>' for a, b, c, d in rows)

    body = _kpi([
        ("BẢNG ĐANG CÓ LỌC THEO DÒNG", "0", "⭐ chưa có tính năng này trong SQLWF", "#B42318"),
        ("BẢNG NÊN CÓ LỌC", "34", "bảng có cột chi nhánh / đơn vị / vùng", "#B54708"),
        ("CÁCH LÀM HIỆN TẠI", "Tạo bảng riêng", "mỗi chi nhánh một bảng sao chép — 41 bảng trùng lặp",
         "#B42318"),
        ("BẢNG TRÙNG LẶP SẼ BỎ ĐƯỢC", "41", "thay bằng 1 bảng gốc + 1 điều kiện lọc", "#067647"),
    ]) + f"""
<div class="card" style="padding:16px 19px;margin-bottom:14px;background:#FEF3F2;
  border-color:#FECDCA">
  <div class="sec" style="color:#B42318;border-color:#B42318">
    ⚠️ TÍNH NĂNG CHƯA TỒN TẠI TRONG SQLWF — VÀ ĐANG ĐƯỢC LÀM VÒNG BẰNG CÁCH RẤT TỐN KÉM</div>
  <div style="font-size:12.5px;line-height:1.75;color:#344054">
    Mã nguồn <b>không có trường <span class="mono">rowFilter</span> nào</b>.
    Cách đang làm hiện nay: <b>tạo hẳn một bảng riêng cho mỗi chi nhánh / mỗi đơn vị</b>, rồi
    phân quyền theo bảng.<br>
    Hệ quả: <b>41 bảng là bản sao lọc sẵn của bảng gốc</b> — tốn dung lượng, tốn job chạy,
    và mỗi lần bảng gốc đổi cấu trúc thì <b>phải sửa 41 chỗ</b>.
  </div>
</div>
<div style="display:flex;gap:16px">
  <div style="flex:1.3">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:9px">
      <div style="font-size:13.5px;font-weight:700">Điều kiện lọc đang áp</div>
      <span class="btn">➕ Thêm điều kiện lọc</span></div>
    <div class="card" style="margin-bottom:14px"><table class="g">
      <tr><th>Bảng</th><th>Áp cho</th><th>Điều kiện lọc</th><th>Nghĩa</th><th></th></tr>
      {tr}</table></div>
    <div class="card" style="padding:16px 19px">
      <div class="sec">CƠ CHẾ — ĐIỀU KIỆN ĐƯỢC NỐI THÊM VÀO CÂU TRUY VẤN</div>
      <div style="font-size:12.5px;line-height:1.9;background:#F8FAFC;border-radius:8px;
        padding:12px 14px;font-family:Consolas,monospace">
        <span class="muted">-- người dùng gõ</span><br>
        <span style="color:#7C3AED">SELECT</span> * <span style="color:#7C3AED">FROM</span>
        bi.doi_soat_giao_dich_A<br>
        <span style="color:#7C3AED">WHERE</span> ngay_giao_dich = '2026-08-07'<br><br>
        <span class="muted">-- DMP viết lại trước khi chạy</span><br>
        <span style="color:#7C3AED">SELECT</span> * <span style="color:#7C3AED">FROM</span>
        bi.doi_soat_giao_dich_A<br>
        <span style="color:#7C3AED">WHERE</span> ngay_giao_dich = '2026-08-07'<br>
        &nbsp;&nbsp;<span style="color:#B54708"><b>AND</b> ma_chi_nhanh
        <b>IN</b> ('HN','HP','QN','TB')</span> &nbsp;<span class="muted">← thêm tự động</span>
      </div>
      <div class="note" style="background:#FFFAEB;border:1px solid #FEDF89;margin-top:11px;
        font-size:12.5px">
        ⚠️ <b>Người dùng không thấy điều kiện này và không gỡ được.</b> Đó là điểm mạnh —
        nhưng cũng là điểm phải cẩn thận:<br><br>
        Người dùng đếm ra <b>412.808 dòng</b> trong khi đồng nghiệp đếm ra <b>1.204.331 dòng</b>
        trên <b>cùng một câu SQL</b> → nếu không được báo trước sẽ tưởng dữ liệu hỏng.<br><br>
        <b>Cách xử lý:</b> hiện một dòng nhắc ngay dưới kết quả —
        <i>"Kết quả đã được lọc theo phạm vi dữ liệu của bạn: chi nhánh miền Bắc"</i>.
      </div>
    </div>
  </div>
  <div style="width:520px;flex-shrink:0">
    <div class="card" style="padding:15px 17px;margin-bottom:13px">
      <div class="sec">HAI KIỂU ĐIỀU KIỆN</div>
      <table class="g" style="font-size:12.5px">
        <tr><th>Kiểu</th><th>Ví dụ</th><th>Bảo trì</th></tr>
        <tr><td><b>Cố định</b></td>
            <td class="mono" style="font-size:11px">ma_chi_nhanh IN ('HN','HP')</td>
            <td>Thêm chi nhánh phải <b>sửa chính sách</b></td></tr>
        <tr><td><b>Biến động</b> ⭐</td>
            <td class="mono" style="font-size:11px">ma_chi_nhanh = ${{chi_nhanh_cua_nguoi_dung}}</td>
            <td>Không phải sửa gì — <b>lấy từ hồ sơ người dùng ở 5.1</b></td></tr>
      </table>
      <div class="note" style="background:#ECFDF3;border:1px solid #A6F4C5;margin-top:11px;
        font-size:12.5px">
        ⭐ <b>Kiểu biến động là thứ đáng đầu tư.</b> Một dòng chính sách duy nhất phục vụ
        <b>toàn bộ 63 chi nhánh</b>. Người chuyển công tác sang chi nhánh khác thì
        <b>phạm vi dữ liệu tự đổi theo</b> — không ai phải nhớ sửa quyền.
      </div>
    </div>
    <div class="card" style="padding:15px 17px;margin-bottom:13px">
      <div class="sec">BỎ ĐƯỢC 41 BẢNG TRÙNG LẶP</div>
      <table class="g" style="font-size:12.5px">
        <tr><th></th><th>Cách hiện tại</th><th>Sau khi có lọc dòng</th></tr>
        <tr><td style="color:#667085">Số bảng</td><td>1 gốc + <b>41 bản sao</b></td>
            <td><b>1 bảng gốc</b></td></tr>
        <tr><td style="color:#667085">Số job chạy</td><td>1 + <b>41 job sao chép</b></td>
            <td><b>1 job</b></td></tr>
        <tr><td style="color:#667085">Đổi cấu trúc bảng</td><td>Sửa <b>41 chỗ</b></td>
            <td>Sửa <b>1 chỗ</b></td></tr>
        <tr><td style="color:#667085">Dung lượng</td><td><b>×42</b></td><td><b>×1</b></td></tr>
      </table>
      <div class="muted" style="font-size:11.5px;margin-top:9px">
        Đây là <b>lý do dễ thuyết phục nhất</b> để ưu tiên tính năng này: nó vừa là bảo mật,
        vừa là tiết kiệm hạ tầng và công bảo trì.</div>
    </div>
    <div class="note" style="background:#EFF4FF;border:1px solid #C7D7FE">
      🔗 <b>Che dữ liệu và lọc theo dòng giải hai bài toán khác nhau — thường phải dùng cùng lúc</b><br><br>
      <b>Che dữ liệu</b> trả lời: <i>người này thấy được CỘT nào</i><br>
      <b>Lọc theo dòng</b> trả lời: <i>người này thấy được DÒNG nào</i><br><br>
      Ví dụ cộng tác viên thuê ngoài: <b>lọc dòng</b> chỉ cho thấy 30 ngày gần nhất,
      <b>đồng thời che</b> số điện thoại thành chuỗi băm.
    </div>
  </div>
</div>"""
    return shell("dmp.vds.vn/security/policies/rowfilter", P_CRUMB, P_TITLE, P_DESC, body,
                 "DMP · Menu 5.2 — CHÍNH SÁCH TRUY CẬP · Tab LỌC THEO DÒNG (mới hoàn toàn)", "m52",
                 tabs=("Lọc theo dòng", P_TABS), actions=P_ACT)


# ============================================================ 5.2 tab Chính sách theo nhãn
def pol_bytag():
    tree = "".join(
        f'<div style="padding:6px 10px;font-size:12.5px;border-radius:6px;margin-bottom:2px;'
        f'{"background:#EFF4FF;font-weight:700;color:" + AC if on else ""}">{ind}{t}'
        f'<span class="muted" style="float:right;font-weight:400">{c}</span></div>'
        for ind, t, c, on in [
            ("", "🗂️ PII — Thông tin cá nhân", "412 cột", False),
            ("&nbsp;&nbsp;", "🏷️ PD_BASIC", "268", False),
            ("&nbsp;&nbsp;", "🏷️ PD_SENSITIVE", "144", True),
            ("", "🗂️ TaiChinh", "186 cột", False),
            ("&nbsp;&nbsp;", "🏷️ TaiChinh.DoanhThu", "118", False),
            ("&nbsp;&nbsp;", "🏷️ TaiChinh.ChiPhi", "68", False),
            ("", "🏷️ DATA_GENERAL", "95.708", False),
        ])
    pol = "".join(
        f'<tr><td>{a}</td><td>{chip(b, c)}</td><td>{chip(d, e)}</td><td class="muted">{f}</td></tr>'
        for a, b, c, d, e, f in [
            ("👥 doi_de", "Không che", "g", "Không lọc", "g", "Đội vận hành cần dữ liệu gốc"),
            ("👥 ban_kinh_doanh", "Hiện 4 số cuối", "o", "Theo chi nhánh", "o",
             "Đủ để nhận ra khách hàng"),
            ("👥 ban_tai_chinh", "Hiện 4 số cuối", "o", "Không lọc", "g", "Cần đối soát toàn quốc"),
            ("👥 ctv_thue_ngoai", "Băm (hash)", "o", "30 ngày gần nhất", "o",
             "Phân tích được, không lấy được dữ liệu ra"),
            ("Nhóm khác", "Trả về NULL", "r", "—", "n", "Mặc định: không thấy gì")])

    body = f"""
<div style="display:flex;gap:18px">
  <div style="width:330px;flex-shrink:0">
    <div style="font-size:12.5px;font-weight:700;margin-bottom:8px">CÂY NHÃN — KHAI Ở MENU 2.2</div>
    <div class="card" style="padding:9px">{tree}</div>
    <div class="note" style="background:#EFF4FF;border:1px solid #C7D7FE;margin-top:12px">
      🔗 Cây này <b>không sửa được ở đây</b> — nó thuộc menu <b>2.2 Phân loại &amp; Nhãn</b>.
      Màn này chỉ <b>gắn chính sách vào nhãn</b>.
    </div>
    <div class="note" style="background:#FFFAEB;border:1px solid #FEDF89;margin-top:12px">
      ⚠️ <b>Chính sách khai ở nhãn cha tự áp xuống nhãn con.</b><br>
      Viết ở <span class="mono">PII</span> thì cả <span class="mono">PD_BASIC</span> và
      <span class="mono">PD_SENSITIVE</span> đều nhận.<br>
      Nhãn con <b>ghi đè được</b> nếu cần chặt hơn.
    </div>
  </div>
  <div style="flex:1">
    <div class="card" style="padding:16px 19px;margin-bottom:14px;background:#FEF3F2;
      border-color:#FECDCA">
      <div class="sec" style="color:#B42318;border-color:#B42318">
        ⚡ CHÍNH SÁCH CHO NHÃN PD_SENSITIVE — ÁP CHO 144 CỘT</div>
      <table class="g" style="font-size:12.5px;background:#fff">
        <tr><th>Nhóm người dùng</th><th>Che dữ liệu</th><th>Lọc theo dòng</th><th>Lý do</th></tr>
        {pol}</table>
      <div style="margin-top:12px;font-size:13px;line-height:1.7">
        ⭐ <b>Đây là giá trị lớn nhất của cả module ⑤:</b> khai <b>5 dòng chính sách một lần</b>,
        áp cho <b>144 cột</b> hiện tại và <b>mọi cột gắn nhãn PD_SENSITIVE sau này</b>.<br>
        Không có nó thì phải khai tay <b>144 × 5 = 720 chính sách</b>, và mỗi bảng mới lại
        khai thêm — <b>chắc chắn sẽ có chỗ bị quên</b>.
      </div>
    </div>
    <div style="display:flex;gap:14px;margin-bottom:14px">
      <div class="card" style="flex:1;padding:15px 17px">
        <div class="sec">THỨ TỰ ƯU TIÊN KHI CÓ NHIỀU CHÍNH SÁCH CHỒNG NHAU</div>
        <table class="g" style="font-size:12.5px">
          <tr><th style="width:40px">Cấp</th><th>Loại chính sách</th><th>Ví dụ</th></tr>
          <tr><td><b>1</b></td><td><b>Ngoại lệ theo cột cụ thể</b></td>
              <td>doi_de không che <span class="mono">so_dien_thoai</span>
                của đúng bảng đối soát</td></tr>
          <tr><td><b>2</b></td><td>Chính sách theo nhãn con</td>
              <td><span class="mono">PD_SENSITIVE</span></td></tr>
          <tr><td><b>3</b></td><td>Chính sách theo nhãn cha</td>
              <td><span class="mono">PII</span></td></tr>
          <tr><td><b>4</b></td><td>Mặc định của hệ thống</td>
              <td>Trả về NULL</td></tr>
        </table>
        <div class="note" style="background:#FFFAEB;border:1px solid #FEDF89;margin-top:10px;
          font-size:12px">
          ⚠️ <b>Quy tắc bắt buộc: cấp trên chỉ được che CHẶT HƠN, không được nới lỏng hơn.</b><br>
          Ngoại lệ nới lỏng (như dòng <span class="mono">doi_de</span> ở trên) phải
          <b>khai riêng và có người duyệt</b>, không tự động.
        </div>
      </div>
      <div style="width:430px;flex-shrink:0">
        <div class="card" style="padding:15px 17px;margin-bottom:13px">
          <div class="sec">GẮN NHÃN CHO CỘT MỚI — ĐIỀU GÌ XẢY RA</div>
          <div style="font-size:12.5px;line-height:1.85">
            BDA gắn nhãn <span class="mono">PD_SENSITIVE</span> cho một cột mới ở
            <b>tab Cột của 1.1</b>:<br><br>
            ① Chính sách che <b>áp ngay</b>, không cần ai duyệt<br>
            ② Cột vào danh sách <b>rà soát định kỳ</b> ở 5.5<br>
            ③ Mọi truy vấn lên cột đó <b>bị ghi nhật ký</b> ở 5.4<br>
            ④ Nhãn <b>đồng bộ sang OPA</b> qua
            <span class="mono" style="font-size:11px">/api/function/sync/tag/</span>
          </div>
        </div>
        <div class="note" style="background:#ECFDF3;border:1px solid #A6F4C5">
          ✅ <b>SQLWF đã có nền cho việc này.</b> <span class="mono">tagIds</span> ở mức cột
          với 3 nhãn <span class="mono">PD_BASIC</span> ·
          <span class="mono">PD_SENSITIVE</span> · <span class="mono">DATA_GENERAL</span>,
          và <b>đã có sẵn đường đồng bộ sang OPA</b>.<br><br>
          Phần thêm: <b>gắn chính sách che và lọc vào nhãn</b> — hiện nhãn mới chỉ dùng để
          <b>chặn hàm SQL</b>, chưa dùng để che giá trị.
        </div>
      </div>
    </div>
  </div>
</div>"""
    return shell("dmp.vds.vn/security/policies/by-tag", P_CRUMB, P_TITLE, P_DESC, body,
                 "DMP · Menu 5.2 — CHÍNH SÁCH TRUY CẬP · Tab CHÍNH SÁCH THEO NHÃN", "m52",
                 tabs=("Chính sách theo nhãn", P_TABS), actions=P_ACT)


SCREENS = {
    "dmp-40-user-list": user_list,
    "dmp-42-policy-data": pol_data,
    "dmp-43-policy-mask": pol_mask,
    "dmp-45-policy-rowfilter": pol_rowfilter,
    "dmp-47-policy-bytag": pol_bytag,
}
