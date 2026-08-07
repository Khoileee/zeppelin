# -*- coding: utf-8 -*-
"""DMP — Module ⑤ (tiếp): 5.3 Yêu cầu cấp quyền, 5.4 Nhật ký kiểm toán, 5.5 Báo cáo quyền."""
from dmp import shell, fld, chip, AC
from s_dmp2 import _kpi
from s_dmp3 import _steps


# ============================================================ 5.3 danh sách yêu cầu
def req_list():
    rows = [
        ("YC-0231", "le.minh.tuan", "🗂️ bi.doi_soat_giao_dich_A", "Xem",
         "Làm báo cáo đối soát quý III", "3 tháng", "N.T.Phương (BDA)", "Chờ duyệt", "2 giờ"),
        ("YC-0230", "ctv.nguyen.an", "🗂️ crm.khach_hang", "Xem",
         "Phân tích chân dung khách hàng", "1 tháng", "N.T.Phương (BDA)", "Chờ duyệt", "6 giờ"),
        ("YC-0228", "pham.thu.ha", "📦 Nhóm bảng: Tài chính", "Xem · Ghi",
         "Xây job tổng hợp doanh thu mới", "6 tháng", "T.V.Hùng (DE)", "Đã duyệt", "—"),
        ("YC-0225", "tran.van.hung", "🗂️ fin.luong_nhan_vien", "Xem",
         "Kiểm tra chất lượng dữ liệu", "1 tháng", "Ban Nhân sự", "Từ chối", "—"),
        ("YC-0219", "le.minh.tuan", "🗂️ dwh.thue_bao_ngay", "Xem",
         "Phân tích thuê bao theo gói cước", "3 tháng", "N.T.Phương (BDA)", "Sắp hết hạn", "—"),
        ("YC-0188", "le.minh.tuan", "🗂️ bi.doi_soat_giao_dich_A", "Xem",
         "Đối soát quý II", "3 tháng", "N.T.Phương (BDA)", "Đã thu hồi", "—"),
    ]
    tr = ""
    for c_, who, scope, perm, why, term, appr, st, wait in rows:
        sc = {"Chờ duyệt": "o", "Đã duyệt": "g", "Từ chối": "r",
              "Sắp hết hạn": "o", "Đã thu hồi": "n"}[st]
        tr += (f'<tr><td class="mono muted">{c_}</td><td class="mono">{who}</td>'
               f'<td>{scope}</td><td>{perm}</td><td class="muted">{why}</td>'
               f'<td>{term}</td><td>{appr}</td><td>{chip(st, sc)}</td>'
               f'<td class="muted">{wait}</td>'
               f'<td style="white-space:nowrap"><span class="ico">👁</span></td></tr>')

    body = _kpi([
        ("YÊU CẦU CHỜ DUYỆT", "12", "cũ nhất đã chờ 6 giờ", "#B54708"),
        ("THỜI GIAN DUYỆT TRUNG BÌNH", "4 giờ", "mục tiêu: dưới 1 ngày làm việc", "#067647"),
        ("QUYỀN SẮP HẾT HẠN 7 NGÀY TỚI", "38", "hệ thống tự nhắc trước 7 ngày", "#B54708"),
        ("ĐÃ TỰ THU HỒI 30 NGÀY QUA", "94", "hết hạn mà không xin gia hạn", "#101828"),
        ("TỈ LỆ TỪ CHỐI", "8%", "chủ yếu do lý do xin không rõ ràng", "#101828"),
    ]) + f"""
<div style="display:flex;gap:10px;margin-bottom:13px;align-items:center">
  <div style="flex:1;border:1px solid #d0d7e2;border-radius:8px;padding:9px 13px;font-size:13px;
    background:#fff">🔍 <span class="muted">Tìm theo mã yêu cầu, người xin, bảng…</span></div>
  <span class="btn w">Trạng thái ▾</span><span class="btn w">Người duyệt ▾</span>
  <span class="btn w">Chỉ tôi phải duyệt ☐</span>
</div>
<div class="card"><table class="g">
  <tr><th>Mã YC</th><th>Người xin</th><th>Xin quyền trên</th><th>Loại quyền</th><th>Lý do</th>
    <th>Thời hạn xin</th><th>Người duyệt</th><th>Trạng thái</th><th>Đã chờ</th><th></th></tr>
  {tr}</table></div>
<div style="display:flex;gap:14px;margin-top:14px">
  <div class="card" style="flex:1;padding:15px 18px">
    <div class="sec">VÒNG ĐỜI MỘT YÊU CẦU — NĂM TRẠNG THÁI</div>
    <div style="display:flex;gap:9px;align-items:center;margin:6px 0 12px">
      {"".join(f'<div style="flex:1;text-align:center;padding:8px 6px;border-radius:7px;'
               f'background:{bg};color:{fg};font-size:12px;font-weight:600">{t}</div>'
               f'{"<span style=color:#98a2b3>→</span>" if i < 4 else ""}'
               for i, (t, bg, fg) in enumerate([
                   ("① Gửi", "#EFF4FF", "#2563EB"),
                   ("② Chờ duyệt", "#FFFAEB", "#B54708"),
                   ("③ Đã duyệt — quyền có hiệu lực", "#ECFDF3", "#067647"),
                   ("④ Sắp hết hạn — nhắc trước 7 ngày", "#FFFAEB", "#B54708"),
                   ("⑤ Tự thu hồi", "#F2F4F7", "#475467")]))}
    </div>
    <table class="g" style="font-size:12.5px">
      <tr><th>Trạng thái</th><th>Ai làm gì</th><th>Hệ thống làm gì</th></tr>
      <tr><td><b>① Gửi</b></td><td>Người xin điền phạm vi · loại quyền · <b>lý do</b> · thời hạn</td>
          <td>Tự tìm người duyệt = <b>BDA phụ trách bảng</b> khai ở 1.1</td></tr>
      <tr><td><b>② Chờ duyệt</b></td><td>Người duyệt xem và quyết định</td>
          <td>Nhắc sau 4 giờ · chuyển lên cấp trên sau 1 ngày làm việc</td></tr>
      <tr><td><b>③ Đã duyệt</b></td><td>—</td>
          <td>Sinh dòng chính sách ở <b>5.2</b>, cột <i>Nguồn</i> ghi <b>mã yêu cầu</b></td></tr>
      <tr><td><b>④ Sắp hết hạn</b></td><td>Người xin có thể <b>xin gia hạn</b></td>
          <td>Gửi nhắc trước <b>7 ngày</b> cho cả người xin và người duyệt</td></tr>
      <tr><td><b>⑤ Tự thu hồi</b></td><td>—</td>
          <td>Xoá dòng chính sách ở 5.2 · ghi vào nhật ký 5.4 · báo người xin</td></tr>
    </table>
  </div>
  <div style="width:500px;flex-shrink:0">
    <div class="note" style="background:#FEF3F2;border:1px solid #FECDCA;margin-bottom:13px">
      🔴 <b>Menu này chưa có trong SQLWF — hiện xin quyền qua chat và email.</b><br><br>
      Ba hệ quả đo được:<br>
      ① <b>Không biết ai cấp, căn cứ vào đâu</b> — 1.409/1.847 chính sách (76%) ghi nguồn là <b>Thủ công</b><br>
      ② <b>Quyền không có hạn</b> — 87% là vô thời hạn, nên 9 người đã nghỉ việc vẫn còn quyền<br>
      ③ <b>Không có số liệu để rà soát</b> — không biết quyền nào còn dùng, quyền nào bỏ quên
    </div>
    <div class="note" style="background:#ECFDF3;border:1px solid #A6F4C5">
      ✅ <b>Không phải xây từ con số không.</b> SQLWF đã có <b>khung duyệt</b> chạy tốt ở
      ba chỗ: <span class="mono">job-approval</span> ·
      <span class="mono">channel-indexing-management</span> (duyệt bản ghi danh mục) ·
      <span class="mono">sync-management</span> (<span class="mono">approveRecord</span> /
      <span class="mono">rejectRecord</span>).<br><br>
      Menu 5.3 <b>dùng lại đúng khung đó</b>, chỉ đổi đối tượng duyệt từ <i>job</i> sang
      <i>quyền truy cập</i>, và thêm phần <b>thời hạn + tự thu hồi</b>.
    </div>
  </div>
</div>"""
    return shell("dmp.vds.vn/security/requests", "Data Security › Yêu cầu cấp quyền",
                 "✋ Yêu cầu cấp quyền",
                 "Xin quyền có dấu vết: gửi → duyệt → quyền có thời hạn → tự thu hồi",
                 body, "DMP · Menu 5.3 — YÊU CẦU CẤP QUYỀN · Màn DANH SÁCH", "m53",
                 tabs=("Tất cả", ["Tất cả", "Tôi phải duyệt", "Tôi đã xin", "Sắp hết hạn",
                                  "Đã thu hồi"]),
                 actions='<span class="btn">➕ Xin quyền</span>')


# ============================================================ 5.3 màn duyệt
def req_approve():
    body = _steps([("Người xin gửi", "done"), ("Người duyệt xem xét", "now"),
                   ("Quyền có hiệu lực", "next"), ("Tự thu hồi", "next")]) + f"""
<div style="display:flex;gap:18px">
  <div style="width:520px;flex-shrink:0">
    <div class="card" style="padding:17px 19px;margin-bottom:13px">
      <div class="sec">NỘI DUNG YÊU CẦU — YC-0231</div>
      {fld("Người xin", "👤 Lê Minh Tuấn · Chuyên viên — Ban Sản phẩm", ro=True)}
      {fld("Xin quyền trên", "🗂️ bi.doi_soat_giao_dich_A", ro=True,
           hint="Tier 1 · Miền Kinh doanh · BDA: Nguyễn Thị Phương")}
      {fld("Loại quyền", "Xem", ro=True)}
      {fld("Lý do cần dùng", "Làm báo cáo đối soát quý III theo yêu cầu của Ban Sản phẩm. "
                             "Cần số liệu giao dịch của 3 tháng 7, 8, 9.", ro=True,
           hint="⭐ <b>Bắt buộc điền, tối thiểu 30 ký tự.</b> Đây là thứ người duyệt đọc để quyết định, "
           "và là thứ kiểm toán đọc lại về sau")}
      {fld("Thời hạn xin", "3 tháng — đến 07/11/2026", ro=True,
           hint="Chọn từ danh sách: 1 tháng · 3 tháng · 6 tháng · 1 năm. "
           "<b>Không có tuỳ chọn vô thời hạn</b>")}
    </div>
    <div class="card" style="padding:17px 19px">
      <div class="sec">QUYẾT ĐỊNH CỦA NGƯỜI DUYỆT</div>
      {fld("Cấp quyền ở mức", "☑ Xem có che &nbsp; ☐ Xem đầy đủ &nbsp; ☐ Từ chối", True,
           "⭐ <b>Người duyệt được hạ mức, không chỉ có Đồng ý / Từ chối</b>")}
      {fld("Cột loại trừ", chip("so_dien_thoai", "r") + chip("so_cccd", "r") +
           '<span class="muted">+ Thêm cột</span>',
           hint="Cột chọn ở đây sẽ <b>trả về NULL</b> cho riêng người này")}
      {fld("Thời hạn cấp", "3 tháng — đến 07/11/2026 ▾", True,
           "Người duyệt <b>rút ngắn được</b> so với thời hạn xin")}
      {fld("Ghi chú cho người xin", "Đồng ý ở mức xem có che. Số điện thoại và CCCD không cần "
                                    "cho việc đối soát — nếu cần thì xin riêng và nêu rõ lý do.")}
      <div style="display:flex;gap:10px;margin-top:6px">
        <span class="btn">✔ Duyệt</span><span class="btn w">✕ Từ chối</span>
        <span class="btn w">↗ Chuyển người khác duyệt</span></div>
    </div>
  </div>
  <div style="flex:1">
    <div class="card" style="padding:16px 19px;margin-bottom:13px">
      <div class="sec">HỆ THỐNG CHUẨN BỊ SẴN CHO NGƯỜI DUYỆT</div>
      <table class="g" style="font-size:12.5px">
        <tr><th style="width:250px">Thông tin</th><th>Giá trị</th><th>Vì sao cần biết</th></tr>
        <tr><td><b>Người này đã có quyền gì trên bảng</b></td>
            <td>{chip("Chưa có", "n")}</td><td>Tránh cấp trùng</td></tr>
        <tr><td><b>Đã từng xin bảng này chưa</b></td>
            <td>{chip("YC-0188 — đã hết hạn", "o")}</td>
            <td>Xin lại nhiều lần → nên cấp theo nhóm thay vì theo người</td></tr>
        <tr><td><b>Lần trước có dùng không</b></td>
            <td>{chip("Có — 47 truy vấn", "g")}</td>
            <td>⭐ Xin rồi không dùng là dấu hiệu xin thừa</td></tr>
        <tr><td><b>Bảng có cột nhạy cảm không</b></td>
            <td>{chip("Có — 2 cột PD_SENSITIVE", "r")}</td>
            <td>Gợi ý người duyệt <b>loại trừ cột</b> thay vì từ chối cả yêu cầu</td></tr>
        <tr><td><b>Đồng nghiệp cùng nhóm có quyền chưa</b></td>
            <td>{chip("4/9 người đã có", "o")}</td>
            <td>Quá nửa nhóm có quyền → nên <b>cấp cho cả nhóm</b></td></tr>
      </table>
      <div class="note" style="background:#EFF4FF;border:1px solid #C7D7FE;margin-top:11px">
        ⭐ <b>Năm dòng này là phần quan trọng nhất của màn.</b> Người duyệt hiện phải mở
        <b>4 màn khác nhau</b> mới kiểm tra được từng ấy thứ — nên phần lớn <b>duyệt luôn cho nhanh</b>.<br>
        Đưa sẵn thông tin lên đây thì việc duyệt <b>vừa nhanh hơn vừa chặt hơn</b>.
      </div>
    </div>
    <div style="display:flex;gap:13px">
      <div class="card" style="flex:1;padding:15px 17px">
        <div class="sec">DUYỆT XONG THÌ ĐIỀU GÌ XẢY RA</div>
        <div style="font-size:12.5px;line-height:1.9">
          ① Sinh một dòng ở <b>5.2 › tab Quyền dữ liệu</b><br>
          &nbsp;&nbsp;&nbsp;cột <i>Nguồn</i> ghi <b>YC-0231</b><br>
          ② Cột loại trừ sinh dòng ở <b>5.2 › tab Che dữ liệu</b><br>
          ③ Ghi vào <b>nhật ký 5.4</b>: ai duyệt, lúc nào, IP nào<br>
          ④ Hẹn nhắc trước <b>7 ngày</b> khi sắp hết hạn<br>
          ⑤ Hết hạn → <b>tự thu hồi</b>, không cần ai nhớ
        </div>
      </div>
      <div class="note" style="width:390px;background:#FFFAEB;border:1px solid #FEDF89">
        ⚠️ <b>Bỏ hẳn tuỳ chọn "vô thời hạn" là quyết định có chủ ý.</b><br><br>
        87% chính sách hiện nay vô thời hạn — và đó chính là lý do có <b>1.204 quyền
        không ai dùng suốt 90 ngày</b> và <b>9 tài khoản đã nghỉ việc vẫn còn quyền</b>.<br><br>
        Quyền hết hạn mà còn cần thì <b>xin gia hạn một cú bấm</b>. Đổi lại,
        <b>quyền bỏ quên tự biến mất</b> — không cần ai đi dọn.
      </div>
    </div>
  </div>
</div>"""
    return shell("dmp.vds.vn/security/requests/YC-0231",
                 "Data Security › Yêu cầu cấp quyền › YC-0231",
                 "✋ YC-0231 — Lê Minh Tuấn xin quyền xem bi.doi_soat_giao_dich_A",
                 "Gửi lúc 07/08/2026 08:14 &nbsp;·&nbsp; Đã chờ 2 giờ &nbsp;·&nbsp; "
                 "Người duyệt: Nguyễn Thị Phương (BDA phụ trách bảng)", body,
                 "DMP · Menu 5.3 — YÊU CẦU CẤP QUYỀN · Màn DUYỆT", "m53")


# ============================================================ 5.4 nhật ký kiểm toán
def audit_log():
    rows = [
        ("07/08 09:42:11", "le.minh.tuan", "Truy vấn", "🗂️ bi.doi_soat_giao_dich_A",
         "SELECT … WHERE ngay_giao_dich = …", "412 dòng", "Che: so_dien_thoai → 4 số cuối",
         "10.58.12.44", "ok"),
        ("07/08 09:31:07", "ctv.nguyen.an", "Truy vấn", "🗂️ crm.khach_hang",
         "SELECT so_cccd, ho_ten FROM …", "0 dòng",
         "Chặn: không có quyền trên cột so_cccd", "10.58.201.9", "deny"),
        ("07/08 08:55:23", "nguyen.thi.phuong", "Duyệt quyền", "YC-0228",
         "Duyệt YC-0228 cho pham.thu.ha", "—", "—", "10.58.12.31", "ok"),
        ("07/08 08:14:02", "tran.van.hung", "Sửa cấu hình", "🗂️ bi.doi_soat_giao_dich_A",
         "Đổi chu kỳ cập nhật: Ngày → Giờ", "—", "Giá trị cũ: DAILY · mới: HOURLY",
         "10.58.12.77", "ok"),
        ("07/08 07:20:44", "le.minh.tuan", "Xuất dữ liệu", "🗂️ dwh.thue_bao_ngay",
         "Xuất Excel 50.000 dòng", "50.000 dòng", "⚠️ Vượt ngưỡng cảnh báo 10.000 dòng",
         "10.58.12.44", "warn"),
        ("07/08 06:05:18", "svc_dq_runner", "Chạy luật", "🗂️ bi.doi_soat_giao_dich_A",
         "Chạy 7 luật chất lượng", "—", "5 đạt · 2 hỏng", "10.58.244.12", "ok"),
    ]
    tr = ""
    for t, who, act, obj, detail, nrow, note, ip, st in rows:
        sc = {"ok": ("Cho phép", "g"), "deny": ("Từ chối", "r"), "warn": ("Cảnh báo", "o")}[st]
        nc = "#B42318" if st in ("deny", "warn") else "#667085"
        tr += (f'<tr><td class="mono" style="font-size:11.5px;white-space:nowrap">{t}</td>'
               f'<td class="mono">{who}</td><td>{chip(act, "n")}</td><td>{obj}</td>'
               f'<td class="mono" style="font-size:11px">{detail}</td>'
               f'<td style="text-align:right">{nrow}</td>'
               f'<td style="font-size:11.5px;color:{nc}">{note}</td>'
               f'<td class="mono muted" style="font-size:11.5px">{ip}</td>'
               f'<td>{chip(*sc)}</td></tr>')

    body = _kpi([
        ("SỰ KIỆN HÔM NAY", "48.211", "truy vấn · xuất · sửa cấu hình · duyệt quyền", "#101828"),
        ("BỊ TỪ CHỐI TRUY CẬP", "127", "chủ yếu do thiếu quyền trên cột nhạy cảm", "#B54708"),
        ("XUẤT DỮ LIỆU VƯỢT NGƯỠNG", "9", "trên 10.000 dòng — cần rà soát", "#B42318"),
        ("TRUY CẬP CỘT PD_SENSITIVE", "1.844", "trong ngày · 38 người", "#B54708"),
        ("THỜI GIAN LƯU NHẬT KÝ", "24 tháng", "theo yêu cầu kiểm toán nội bộ", "#101828"),
    ]) + f"""
<div style="display:flex;gap:10px;margin-bottom:13px;align-items:center">
  <div style="flex:1;border:1px solid #d0d7e2;border-radius:8px;padding:9px 13px;font-size:13px;
    background:#fff">🔍 <span class="muted">Tìm theo người dùng, bảng, cột, địa chỉ IP…</span></div>
  <span class="btn w">Loại sự kiện ▾</span><span class="btn w">Khoảng thời gian ▾</span>
  <span class="btn w">Chỉ cột nhạy cảm ☐</span><span class="btn w">Chỉ bị từ chối ☐</span>
</div>
<div class="card"><table class="g">
  <tr><th>Thời điểm</th><th>Người dùng</th><th>Hành động</th><th>Đối tượng</th><th>Chi tiết</th>
    <th style="text-align:right">Số dòng</th><th>Chính sách nào quyết định</th>
    <th>Địa chỉ IP</th><th>Kết quả</th></tr>{tr}</table></div>
<div style="display:flex;gap:14px;margin-top:14px">
  <div class="card" style="flex:1;padding:15px 18px">
    <div class="sec">GỘP NĂM MÀN NHẬT KÝ ĐANG RẢI RÁC</div>
    <table class="g" style="font-size:12.5px">
      <tr><th>Màn SQLWF hiện tại</th><th>Ghi cái gì</th><th>Đã có trường gì</th></tr>
      <tr><td class="mono">history-data</td><td>Thay đổi cấu hình</td>
          <td>✅ <b>Giá trị cũ · Giá trị mới · Người thay đổi · IP Address</b> — rất đầy đủ</td></tr>
      <tr><td class="mono">sql-history</td><td>Lịch sử câu lệnh SQL</td><td>Câu lệnh · người chạy</td></tr>
      <tr><td class="mono">query-history</td><td>Lịch sử truy vấn</td><td>Truy vấn · thời điểm</td></tr>
      <tr><td class="mono">sql-query-report</td><td>Báo cáo truy vấn</td><td>Thống kê theo kỳ</td></tr>
      <tr><td class="mono">detail-log-configuration</td><td>Nhật ký cấu hình tác vụ</td>
          <td>Thay đổi theo <span class="mono">taskCode</span></td></tr>
    </table>
    <div class="note" style="background:#ECFDF3;border:1px solid #A6F4C5;margin-top:11px">
      ✅ <b>Phần khó nhất SQLWF đã làm rồi.</b> <span class="mono">history-data</span> ghi cả
      <b>giá trị cũ</b>, <b>giá trị mới</b> và <b>địa chỉ IP</b> — nhiều công cụ thị trường
      cũng chỉ ghi được đến mức này.<br>
      Việc còn lại chủ yếu là <b>gộp 5 màn về một chỗ tra cứu</b>, không phải xây mới.
    </div>
  </div>
  <div style="width:520px;flex-shrink:0">
    <div class="note" style="background:#FEF3F2;border:1px solid #FECDCA;margin-bottom:13px">
      🔴 <b>Cột thêm mới quan trọng nhất: "Chính sách nào quyết định".</b><br><br>
      Nhật ký hiện chỉ trả lời <i>ai làm gì</i>. Khi kiểm toán hỏi
      <i>"vì sao người này xem được cột này"</i> hoặc <i>"vì sao người kia bị chặn"</i>
      thì <b>không có câu trả lời</b> — phải mở 4 màn quyền ra dò tay.<br><br>
      Ghi thẳng <b>chính sách nào đã áp</b> vào từng dòng nhật ký thì mỗi dòng
      <b>tự giải thích được chính nó</b>.
    </div>
    <div class="card" style="padding:15px 17px">
      <div class="sec">BỐN CÂU HỎI KIỂM TOÁN THƯỜNG HỎI</div>
      <table class="g" style="font-size:12.5px">
        <tr><th>Câu hỏi</th><th>Trả lời bằng</th></tr>
        <tr><td>Ai đã xem cột CCCD trong quý vừa rồi</td>
            <td>Lọc <i>Chỉ cột nhạy cảm</i> + khoảng thời gian</td></tr>
        <tr><td>Người đã nghỉ việc còn truy cập sau ngày nghỉ không</td>
            <td>Lọc theo tài khoản + so với ngày nghỉ ở 5.1</td></tr>
        <tr><td>Có ai xuất lượng dữ liệu bất thường không</td>
            <td>Thẻ <b>Xuất dữ liệu vượt ngưỡng</b></td></tr>
        <tr><td>Quyền này ai cấp, căn cứ vào đâu</td>
            <td>Cột <i>Nguồn</i> ở 5.2 → mã yêu cầu ở <b>5.3</b></td></tr>
      </table>
      <div class="muted" style="font-size:11.5px;margin-top:9px">
        Cả bốn câu hiện đều <b>không trả lời được trong một lần tra</b>.</div>
    </div>
  </div>
</div>"""
    return shell("dmp.vds.vn/security/audit", "Data Security › Nhật ký kiểm toán",
                 "📜 Nhật ký kiểm toán",
                 "Ai truy cập gì, lúc nào, từ đâu — và chính sách nào đã quyết định",
                 body, "DMP · Menu 5.4 — NHẬT KÝ KIỂM TOÁN · Màn TRA CỨU", "m54",
                 tabs=("Tất cả sự kiện", ["Tất cả sự kiện", "Truy vấn dữ liệu", "Xuất dữ liệu",
                                          "Thay đổi cấu hình", "Thay đổi quyền"]),
                 actions='<span class="btn w">⬇️ Xuất nhật ký</span>')


# ============================================================ 5.5 báo cáo quyền
def perm_report():
    perms = [
        ("🧩 Miền Kinh doanh", "Xem", "Nhóm ban_kinh_doanh", "Vô thời hạn", "Có — 214 truy vấn",
         "Giữ"),
        ("📦 Nhóm bảng: Báo cáo tuần", "Xem", "Nhóm ban_kinh_doanh", "Vô thời hạn",
         "Có — 88 truy vấn", "Giữ"),
        ("🗂️ bi.doi_soat_giao_dich_A", "Xem", "YC-0231 — cấp riêng", "Hết hạn 07/11/2026",
         "Có — 47 truy vấn", "Giữ"),
        ("🗂️ fin.luong_nhan_vien", "Xem", "Cấp thủ công 2024", "Vô thời hạn",
         "Không — 0 truy vấn 18 tháng", "Thu hồi"),
        ("🗂️ crm.khach_hang", "Xem · Ghi", "Nhóm bda_kinh_doanh", "Vô thời hạn",
         "Không — 0 truy vấn 90 ngày", "Rà soát"),
        ("📁 /data/raw/doi_soat/", "Read · Write", "file-view-group", "Vô thời hạn",
         "Không xác định", "Rà soát"),
    ]
    tr = ""
    for scope, perm, src, term, used, act in perms:
        uc = "#067647" if used.startswith("Có") else "#B42318"
        ac = {"Giữ": "g", "Thu hồi": "r", "Rà soát": "o"}[act]
        tr += (f'<tr><td>{scope}</td><td>{perm}</td><td class="muted">{src}</td>'
               f'<td>{chip(term, "n" if term.startswith("Vô") else "o")}</td>'
               f'<td style="color:{uc};font-size:12px">{used}</td>'
               f'<td>{chip(act, ac)}</td>'
               f'<td><span class="ico">✕</span></td></tr>')

    masks = "".join(
        f'<tr><td class="mono" style="font-size:11.5px">{a}</td><td class="mono">{b}</td>'
        f'<td>{chip(c, "r")}</td><td>{chip(d, "o" if d != "Không che" else "g")}</td></tr>'
        for a, b, c, d in [
            ("bi.doi_soat_giao_dich_A", "so_dien_thoai", "PD_SENSITIVE", "Hiện 4 số cuối"),
            ("crm.khach_hang", "so_cccd", "PD_SENSITIVE", "Trả về NULL"),
            ("crm.khach_hang", "ngay_sinh", "PD_BASIC", "Chỉ hiện năm")])

    body = f"""
<div style="display:flex;gap:10px;margin-bottom:14px;align-items:center">
  <div style="flex:1;border:1px solid #d0d7e2;border-radius:8px;padding:9px 13px;font-size:13px;
    background:#fff">🔍 <b>le.minh.tuan</b> — Lê Minh Tuấn ·
    <span class="muted">Chuyên viên, Ban Sản phẩm</span></div>
  <span class="btn w">Tra theo BẢNG thay vì theo người</span>
  <span class="btn w">⬇️ Xuất báo cáo rà soát</span>
</div>
{_kpi([("TỔNG SỐ QUYỀN ĐANG CÓ", "6", "3 qua nhóm · 2 cấp riêng · 1 thư mục", "#101828"),
       ("QUYỀN KHÔNG DÙNG 90 NGÀY", "3", "ứng viên thu hồi", "#B42318"),
       ("BẢNG THỰC SỰ ĐỌC ĐƯỢC", "412", "sau khi tính cả quyền theo miền", "#101828"),
       ("CỘT BỊ CHE", "3", "trên 2 bảng", "#B54708"),
       ("QUYỀN VÔ THỜI HẠN", "5 / 6", "chỉ 1 quyền có ngày hết hạn", "#B42318")])}
<div style="display:flex;gap:16px">
  <div style="flex:1.4">
    <div style="font-size:13.5px;font-weight:700;margin-bottom:9px">
      Toàn bộ quyền của le.minh.tuan — gộp từ 4 nguồn</div>
    <div class="card" style="margin-bottom:14px"><table class="g">
      <tr><th>Phạm vi</th><th>Quyền</th><th>Có được nhờ đâu</th><th>Thời hạn</th>
        <th>90 ngày qua có dùng không</th><th>Đề xuất</th><th></th></tr>{tr}</table></div>
    <div class="card" style="padding:16px 19px">
      <div class="sec">CỘT BỊ CHE ĐỐI VỚI NGƯỜI NÀY</div>
      <table class="g" style="font-size:12.5px">
        <tr><th>Bảng</th><th>Cột</th><th>Nhãn</th><th>Người này thấy</th></tr>{masks}</table>
      <div class="muted" style="font-size:11.5px;margin-top:9px">
        Bảng này trả lời câu <i>"người này có đọc được số CCCD không"</i> —
        hiện phải mở từng bảng ra kiểm tra tay.</div>
    </div>
  </div>
  <div style="width:520px;flex-shrink:0">
    <div class="note" style="background:#FEF3F2;border:1px solid #FECDCA;margin-bottom:13px">
      🔴 <b>Menu này chưa có trong SQLWF.</b> Quyền hiện rải ở <b>4 màn</b>
      (<span class="mono">user-managerment</span> · <span class="mono">data-authorize</span> ·
      <span class="mono">file-view-group</span> · <span class="mono">group-authorize</span>),
      phải mở từng cái kiểm tra tay.<br><br>
      Hệ quả thực tế: khi có người nghỉ việc, <b>không ai chắc đã thu hồi hết quyền chưa</b> —
      và đó là lý do <b>9 tài khoản đã nghỉ vẫn còn quyền trên 132 bảng</b>.
    </div>
    <div class="card" style="padding:15px 17px;margin-bottom:13px">
      <div class="sec">HAI CHIỀU TRA CỨU</div>
      <table class="g" style="font-size:12.5px">
        <tr><th>Chiều</th><th>Câu hỏi trả lời được</th></tr>
        <tr><td><b>Theo NGƯỜI</b><br><span class="muted">màn này</span></td>
            <td>Người này đang có quyền gì trên toàn hệ thống · quyền nào không dùng ·
              cột nào bị che</td></tr>
        <tr><td><b>Theo BẢNG</b><br><span class="muted">nút ở góc trên</span></td>
            <td>Bảng này ai đang xem được · ai có quyền ghi · ai xem được cột nhạy cảm</td></tr>
      </table>
      <div class="muted" style="font-size:11.5px;margin-top:9px">
        Chiều <b>theo bảng</b> cũng chính là nội dung <b>tab Quyền</b> trong chi tiết bảng 1.1 —
        cùng một dữ liệu, hai lối vào.</div>
    </div>
    <div class="card" style="padding:15px 17px">
      <div class="sec">RÀ SOÁT QUYỀN ĐỊNH KỲ</div>
      <div style="font-size:12.5px;line-height:1.85">
        Mỗi <b>quý</b>, hệ thống gửi cho từng <b>trưởng đơn vị</b> danh sách quyền của
        nhân viên mình, kèm cột <b>90 ngày qua có dùng không</b>.<br><br>
        Trưởng đơn vị chỉ cần bấm <b>Giữ</b> hoặc <b>Thu hồi</b> từng dòng.
        Quá <b>14 ngày</b> không phản hồi thì các quyền <b>không dùng</b> tự thu hồi.
      </div>
      <div class="note" style="background:#FFFAEB;border:1px solid #FEDF89;margin-top:11px;
        font-size:12px">
        ⚠️ <b>Cột "có dùng không" là thứ làm cho việc rà soát khả thi.</b><br>
        Đưa một danh sách 600 dòng quyền cho trưởng đơn vị mà không kèm số liệu sử dụng thì
        họ sẽ <b>bấm Giữ tất</b> — rà soát thành hình thức.<br>
        Có cột này thì <b>chỉ còn 3 dòng đáng phải nghĩ</b>.
      </div>
    </div>
  </div>
</div>"""
    return shell("dmp.vds.vn/security/report?user=le.minh.tuan",
                 "Data Security › Báo cáo quyền › le.minh.tuan",
                 "📋 Báo cáo quyền truy cập",
                 "Một người đang có quyền gì trên toàn hệ thống — trả lời trong một màn",
                 body, "DMP · Menu 5.5 — BÁO CÁO QUYỀN · Màn TRA THEO NGƯỜI", "m55")


SCREENS = {
    "dmp-48-request-list": req_list,
    "dmp-50-request-approve": req_approve,
    "dmp-51-audit-log": audit_log,
    "dmp-52-perm-report": perm_report,
}
