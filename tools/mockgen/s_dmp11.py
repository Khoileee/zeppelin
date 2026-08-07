# -*- coding: utf-8 -*-
"""DMP — 8 màn bổ sung sau đợt rà soát: form khai báo và các tab còn thiếu."""
from dmp import shell, fld, chip, AC
from s_dmp2 import _kpi
from s_dmp3 import _steps
from s_dmp7 import J_TABS, J_CRUMB, J_TITLE, J_DESC, J_ACT
from s_dmp8 import P_TABS, P_CRUMB, P_TITLE, P_DESC, P_ACT, MASK_ROWS


# ==================================================== 3.5 tab Kênh gửi
def alert_channels():
    rows = [
        ("KENH-01", "Email — Ban Kinh doanh", "Email", "notify-manager · nhóm 12 người",
         "Đang chạy", "1.842", "0,2%"),
        ("KENH-02", "Email — Đội vận hành dữ liệu", "Email", "notify-manager · nhóm 8 người",
         "Đang chạy", "3.104", "0,1%"),
        ("KENH-03", "Telegram — Cảnh báo job hỏng", "Telegram", "chat_id: -100248…",
         "Đang chạy", "612", "1,4%"),
        ("KENH-04", "Telegram — Sự cố chất lượng", "Telegram", "chat_id: -100311…",
         "Đang chạy", "188", "0,5%"),
        ("KENH-05", "SMS — Trực lãnh đạo", "SMS", "4 số điện thoại", "Chỉ dùng mức Nghiêm trọng",
         "6", "0%"),
        ("KENH-06", "Ticket SOC", "Tạo ticket", "warning-history · isSendTicket",
         "Đang chạy", "31", "3,2%"),
    ]
    tr = ""
    for c_, nm, kind, cfg, st, sent, fail in rows:
        fc = "#B42318" if float(fail.replace("%", "").replace(",", ".")) > 1 else "#667085"
        tr += (f'<tr><td class="mono muted">{c_}</td><td><b style="color:{AC}">{nm}</b></td>'
               f'<td>{chip(kind, "t")}</td><td class="mono muted" style="font-size:11.5px">{cfg}</td>'
               f'<td>{chip(st, "g" if st == "Đang chạy" else "o")}</td>'
               f'<td style="text-align:right">{sent}</td>'
               f'<td style="text-align:right;color:{fc}">{fail}</td>'
               f'<td style="white-space:nowrap"><span class="ico">▶</span>'
               f'<span class="ico">✎</span></td></tr>')

    users = "".join(
        f'<tr><td class="mono">{a}</td><td>{b}</td><td class="muted">{c}</td></tr>'
        for a, b, c in [
            ("BDA phụ trách bảng", "Lấy từ trường businessOwner của 1.1",
             "Đổi người phụ trách ở 1.1 → cảnh báo tự đi đúng chỗ"),
            ("DE phụ trách bảng", "Lấy từ trường dataEngineerOwner của 1.1", "như trên"),
            ("Người được gán sự cố", "Lấy từ menu 3.4", "Theo từng sự cố"),
            ("Nhóm người dùng", "Chọn từ 5.1", "Dùng khi cần cả nhóm biết"),
            ("Danh sách cố định", "Gõ tay email / số điện thoại",
             "⚠️ Không khuyến khích — người nghỉ việc là cảnh báo rơi vào hư không")])

    body = _kpi([
        ("SỐ KÊNH ĐANG CHẠY", "6", "Email · Telegram · SMS · Ticket SOC", "#101828"),
        ("CẢNH BÁO GỬI TRONG THÁNG", "5.783", "trên 4 loại kênh", "#101828"),
        ("TỈ LỆ GỬI THẤT BẠI", "0,4%", "chủ yếu do email người đã nghỉ việc", "#B54708"),
        ("QUY TẮC ĐANG DÙNG KÊNH NÀY", "41", "khai ở tab Quy tắc · 4.1 · 3.4", "#101828"),
    ]) + f"""
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
  <div style="font-size:13.5px;font-weight:700">Kênh gửi dùng chung toàn hệ thống</div>
  <div style="display:flex;gap:8px"><span class="btn w">▶ Gửi thử tất cả</span>
    <span class="btn">➕ Thêm kênh</span></div></div>
<div class="card"><table class="g">
  <tr><th>Mã kênh</th><th>Tên kênh</th><th>Loại</th><th>Cấu hình</th><th>Trạng thái</th>
    <th style="text-align:right">Đã gửi / tháng</th><th style="text-align:right">Thất bại</th>
    <th></th></tr>{tr}</table></div>
<div style="display:flex;gap:16px;margin-top:14px">
  <div class="card" style="flex:1;padding:16px 19px">
    <div class="sec">KHAI NGƯỜI NHẬN THEO VAI TRÒ, KHÔNG GÕ TÊN NGƯỜI</div>
    <table class="g" style="font-size:12.5px">
      <tr><th style="width:210px">Kiểu người nhận</th><th>Lấy từ đâu</th><th>Ghi chú</th></tr>
      {users}</table>
    <div class="note" style="background:#EFF4FF;border:1px solid #C7D7FE;margin-top:11px">
      ⭐ <b>Đây là tab mà ba menu khác dùng lại — không menu nào khai kênh riêng.</b><br><br>
      <b>4.1</b> — cảnh báo job hỏng &nbsp;·&nbsp; <b>3.4</b> — thông báo sự cố &nbsp;·&nbsp;
      <b>3.5 tab Quy tắc</b> — cảnh báo chất lượng<br><br>
      Cả ba chỉ <b>chọn mã kênh</b>. Đổi nhóm nhận email thì sửa <b>một chỗ duy nhất</b>,
      không phải đi sửa 41 quy tắc.
    </div>
  </div>
  <div style="width:520px;flex-shrink:0">
    <div class="note" style="background:#ECFDF3;border:1px solid #A6F4C5;margin-bottom:13px">
      ✅ <b>Toàn bộ tab này SQLWF đã có — giữ nguyên.</b><br>
      <span class="mono">notify-manager</span> quản nhóm nhận email ·
      <span class="mono">telegram</span> đã chạy ·
      <span class="mono">warning-history</span> có <b>tạo ticket SOC</b>
      (<span class="mono">isSendTicket</span>) và <b>duyệt cảnh báo hàng loạt</b>.<br><br>
      Phần thêm duy nhất: <b>cột "Đã gửi / Thất bại"</b> và <b>nút gửi thử</b>.
    </div>
    <div class="note" style="background:#FFFAEB;border:1px solid #FEDF89">
      ⚠️ <b>Cột "Thất bại" nhỏ nhưng quan trọng.</b><br><br>
      Cảnh báo gửi vào hòm thư của người đã nghỉ việc thì <b>hệ thống vẫn báo là đã gửi</b> —
      không ai biết cảnh báo rơi vào hư không.<br><br>
      Kênh nào vượt <b>1% thất bại</b> thì hiện đỏ và nhắc người quản trị rà lại danh sách nhận.
      Hiện <span class="mono">KENH-03</span> đang 1,4% và <span class="mono">KENH-06</span> 3,2%.
    </div>
  </div>
</div>"""
    return shell("dmp.vds.vn/quality/alerts/channels", "Data Quality › Cảnh báo › Kênh gửi",
                 "🔔 Cảnh báo",
                 "Ai nhận cảnh báo gì, qua kênh nào — khai một lần, ba menu dùng lại",
                 body, "DMP · Menu 3.5 — CẢNH BÁO · Tab KÊNH GỬI", "m35",
                 tabs=("Kênh gửi", ["Quy tắc", "Lịch sử gửi", "Kênh gửi", "Mẫu nội dung"]),
                 actions='<span class="btn w">▶ Gửi thử</span><span class="btn">➕ Thêm kênh</span>')


# ==================================================== 4.1 tạo job
def job_create():
    steps = "".join(
        f'<tr><td style="text-align:center">{i}</td><td><b>{nm}</b></td>'
        f'<td class="muted">{par}</td><td class="mono" style="font-size:11.5px">{out}</td>'
        f'<td style="white-space:nowrap"><span class="ico">✎</span>'
        f'<span class="ico">✕</span></td></tr>'
        for i, nm, par, out in [
            (1, "Đọc file đối tác A", "—", "tmp_doi_tac_tho"),
            (2, "Chuẩn hoá số điện thoại", "Bước 1", "tmp_doi_tac_chuan"),
            (3, "Đọc giao dịch nội bộ", "—", "tmp_giao_dich_noi_bo"),
            (4, "Đối soát 2 nguồn", "Bước 2, Bước 3", "tmp_ket_qua"),
            (5, "Ghi bảng đích", "Bước 4", "bi.doi_soat_giao_dich_A")])

    body = _steps([("Thông tin chung", "done"), ("Các bước SQL", "done"),
                   ("Bảng đích & Lịch", "now"), ("Cảnh báo", "next"), ("Gửi duyệt", "next")]) + f"""
<div style="display:flex;gap:18px">
  <div style="width:490px;flex-shrink:0">
    <div class="card" style="padding:17px 19px;margin-bottom:13px">
      <div class="sec">① THÔNG TIN CHUNG</div>
      {fld("Mã job", "JOB-0412 &nbsp;<span class='muted'>(tự sinh)</span>", ro=True)}
      {fld("Tên job", "Đối soát giao dịch đối tác A", True,
           "Viết đủ nghĩa — tên này hiện trên sơ đồ pipeline ở 4.3 và trong cảnh báo")}
      {fld("Nhóm job", "Đối soát ▾", True, "Dùng để lọc ở màn danh sách")}
      {fld("Mô tả", "Đối soát file đối tác A gửi qua SFTP với giao dịch nội bộ, "
                    "chốt số chênh lệch theo ngày.", True)}
      {fld("Nhân bản từ job có sẵn?", "☐ Không &nbsp; ☑ Từ JOB-0388",
           hint="SQLWF đã có <span class='mono'>job-clone/:id</span> — giữ nguyên")}
    </div>
    <div class="card" style="padding:17px 19px">
      <div class="sec">② CÁC BƯỚC SQL</div>
      <table class="g" style="font-size:12.5px">
        <tr><th style="text-align:center">#</th><th>Tên bước</th><th>Bước cha</th>
          <th>Bảng ra</th><th></th></tr>{steps}</table>
      <div style="margin-top:10px"><span class="btn w">➕ Thêm bước</span>
        <span class="btn w">🔀 Xem sơ đồ phụ thuộc</span></div>
      <div class="muted" style="font-size:11.5px;margin-top:9px">
        Bước không có bước cha thì chạy song song. Toàn bộ phần này
        <b>SQLWF đã có</b> — <span class="mono">job-step</span> ·
        <span class="mono">step-diagram</span> · <span class="mono">sql-viewer</span>.</div>
    </div>
  </div>
  <div style="flex:1">
    <div class="card" style="padding:17px 19px;margin-bottom:13px;background:#FFFAEB;
      border-color:#FEDF89">
      <div class="sec" style="color:#B54708;border-color:#B54708">
        ③ BẢNG ĐÍCH — HAI RÀNG BUỘC MỚI NẰM Ở ĐÂY</div>
      {fld("Bảng đích", "🗂️ bi.doi_soat_giao_dich_A ▾", True,
           "⭐ <b>Bắt buộc chọn từ danh mục 1.1 — không cho gõ tay tên bảng.</b> "
           "Bảng chưa khai thì bấm <i>Khai bảng mới</i>, mở form của 1.1 ngay tại đây")}
      <div class="note" style="background:#fff;border:1px solid #d0d7e2;font-size:12.5px;
        margin-bottom:13px">
        Chọn xong hệ thống hiện ngay: bảng này <b>Tier 1</b> · BDA <b>Nguyễn Thị Phương</b> ·
        có <b>7 luật chất lượng</b> · đang được <b>6 báo cáo</b> dùng.<br>
        → Người tạo job <b>biết mình đang ghi đè cái gì</b> trước khi bấm lưu.
      </div>
      {fld("Bật quét nguồn gốc", "☑ Bật &nbsp;<span class='muted'>(mặc định MỚI: bật)</span>", True,
           "SQLWF hiện mặc định <b>TẮT</b> (<span class='mono'>enableDataLineage = false</span>) — "
           "đây là nguyên nhân gốc khiến tab Nguồn gốc của phần lớn bảng đang trống")}
      <div class="note" style="background:#FEF3F2;border:1px solid #FECDCA;font-size:12.5px">
        🔴 <b>Không cho tắt với bảng đích Tier 1.</b> Bảng vàng mà không có sơ đồ nguồn gốc thì
        khi hỏng không ai biết ảnh hưởng tới báo cáo nào.
      </div>
    </div>
    <div class="card" style="padding:17px 19px;margin-bottom:13px">
      <div class="sec">③ LỊCH CHẠY</div>
      <div style="display:flex;gap:13px">
        <div style="flex:1">
          {fld("Biểu thức lịch", "0 0 6 * * ?", True, "Diễn giải: <b>06:00 hằng ngày</b>", mono=True)}
          {fld("Mã điều phối", "COORD_DOISOAT_A", hint="Dùng bởi Pentaho — giữ nguyên", mono=True)}
        </div>
        <div style="flex:1">
          {fld("Chờ job nào xong trước", "JOB-0388 — nạp file SFTP ▾",
               hint="Tránh chạy khi file chưa về")}
          {fld("Giờ cam kết xong", "07:00", True,
               "⭐ <b>Trường mới.</b> Luật <span class='mono'>on_time</span> ở 3.2 và thẻ "
               "<b>Độ tươi</b> ở 1.1 đều lấy mốc này")}
        </div>
      </div>
      {fld("Chế độ chạy thử", "☐ Bật — chạy nhưng không ghi vào bảng đích",
           hint="SQLWF đã có <span class='mono'>updateTestMode</span>")}
    </div>
    <div style="display:flex;gap:13px">
      <div class="note" style="flex:1;background:#EFF4FF;border:1px solid #C7D7FE">
        🔗 <b>Khai ở đây, dùng ở đâu</b><br><br>
        <b>Bảng đích</b> → tab Nguồn gốc của <b>1.1</b> · sơ đồ pipeline <b>4.3</b><br>
        <b>Câu SQL các bước</b> → bộ phân tích cú pháp sinh <b>bảng nguồn</b><br>
        <b>Giờ cam kết</b> → luật <span class="mono">on_time</span> ở <b>3.2</b> · thẻ Độ tươi ở <b>1.1</b><br>
        <b>Lịch chạy</b> → màn giám sát <b>4.3</b>
      </div>
      <div class="note" style="width:330px;background:#ECFDF3;border:1px solid #A6F4C5">
        ✅ <b>Quy trình duyệt giữ nguyên.</b> Job ở trạng thái <b>Nháp</b> cho tới khi
        <b>BDA phụ trách bảng đích</b> duyệt — SQLWF đã có
        <span class="mono">job-approval</span>.
      </div>
    </div>
    <div style="display:flex;gap:10px;margin-top:15px">
      <span class="btn">Tiếp tục — Cảnh báo</span>
      <span class="btn w">▶ Chạy thử</span><span class="btn w">Lưu nháp</span></div>
  </div>
</div>"""
    return shell("dmp.vds.vn/orchestration/jobs/create",
                 "Ingestion &amp; Orchestration › Luồng xử lý › Tạo job", "➕ Tạo job",
                 "Khai chuỗi bước SQL, bảng đích và lịch chạy", body,
                 "DMP · Menu 4.1 — LUỒNG XỬ LÝ · Màn TẠO JOB (bước 3 — Bảng đích &amp; Lịch)", "m41")


# ==================================================== 4.1 tab Phiên bản
def job_versions():
    vers = [
        ("v4.2", "07/08/2026 08:14", "T.V.Hùng", "Đổi ngưỡng chênh lệch từ 0,5% xuống 0,1%",
         "N.T.Phương", "Đang chạy"),
        ("v4.1", "22/07/2026 14:02", "T.V.Hùng", "Thêm Bước 3 — đọc giao dịch nội bộ",
         "N.T.Phương", "Đã thay thế"),
        ("v4.0", "10/06/2026 09:31", "L.V.Nam", "Chuyển bảng đích sang định dạng Iceberg",
         "N.T.Phương", "Đã thay thế"),
        ("v3.4", "02/04/2026 16:45", "T.V.Hùng", "Sửa lỗi múi giờ ở cột ngay_giao_dich",
         "N.T.Phương", "Đã thay thế"),
    ]
    tr = ""
    for v, d, who, note, appr, st in vers:
        tr += (f'<tr style="{"background:#EFF4FF" if st == "Đang chạy" else ""}">'
               f'<td>{chip(v, "b" if st == "Đang chạy" else "n")}</td><td>{d}</td>'
               f'<td>{who}</td><td>{note}</td><td class="muted">{appr}</td>'
               f'<td>{chip(st, "g" if st == "Đang chạy" else "n")}</td>'
               f'<td style="white-space:nowrap"><span class="ico">👁</span>'
               f'<span class="ico">⇄</span><span class="ico">↩</span></td></tr>')

    body = f"""
<div style="display:flex;gap:16px">
  <div style="flex:1.35">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
      <div style="font-size:13.5px;font-weight:700">Lịch sử phiên bản — 12 phiên bản</div>
      <div style="display:flex;gap:8px"><span class="btn w">⇄ So sánh 2 phiên bản</span></div></div>
    <div class="card" style="margin-bottom:14px"><table class="g">
      <tr><th>Phiên bản</th><th>Thời điểm</th><th>Người sửa</th><th>Nội dung thay đổi</th>
        <th>Người duyệt</th><th>Trạng thái</th><th></th></tr>{tr}</table>
      <div style="padding:9px 12px;font-size:12px" class="muted">… và 8 phiên bản cũ hơn</div></div>
    <div class="card" style="padding:16px 19px">
      <div class="sec">SO SÁNH v4.1 → v4.2 — BƯỚC 4</div>
      <pre style="background:#0F1729;border-radius:8px;padding:13px 15px;
        font-family:Consolas,monospace;font-size:12px;line-height:1.65;overflow:hidden;color:#E5E9F0">
<span style="color:#8b95a7">  SELECT ma_giao_dich, so_tien_noi_bo, so_tien_doi_tac,</span>
<span style="color:#8b95a7">         n.so_tien - d.so_tien AS chenh_lech</span>
<span style="color:#8b95a7">  FROM   ...</span>
<span style="background:#3D1D1D;color:#FDA29B">- WHERE  ABS(chenh_lech) / n.so_tien &gt; 0.005</span>
<span style="background:#123522;color:#75E0A7">+ WHERE  ABS(chenh_lech) / n.so_tien &gt; 0.001</span></pre>
      <div class="muted" style="font-size:11.5px;margin-top:9px">
        Chỉ hiện <b>phần khác nhau</b>, không bắt người duyệt đọc lại cả câu SQL 80 dòng.</div>
    </div>
  </div>
  <div style="width:520px;flex-shrink:0">
    <div class="card" style="padding:16px 19px;margin-bottom:13px;background:#FFFAEB;
      border-color:#FEDF89">
      <div class="sec" style="color:#B54708;border-color:#B54708">
        ⚠️ HAI NGƯỜI ĐANG MỞ CÙNG MỘT JOB</div>
      <table class="g" style="font-size:12.5px;background:#fff">
        <tr><td style="width:150px;color:#667085">Đang giữ khoá</td>
            <td><b>Trần Văn Hùng</b> — từ 08:02 <span class="muted">(12 phút)</span></td></tr>
        <tr><td style="color:#667085">Đang chờ</td><td>Lê Văn Nam — chỉ xem được</td></tr>
        <tr><td style="color:#667085">Khoá tự hết hạn</td><td>sau 30 phút không thao tác</td></tr>
      </table>
      <div style="font-size:12.5px;margin-top:11px;line-height:1.7">
        ✅ <b>SQLWF đã xử lý chuyện này rất tốt — giữ nguyên hoàn toàn.</b><br>
        <span class="mono">acquireLock</span> · <span class="mono">refreshLock</span> ·
        <span class="mono">releaseLock</span> và màn
        <span class="mono">job-version-conflict</span> khi hai người lỡ sửa cùng lúc.<br><br>
        Đây là thứ <b>nhiều công cụ thị trường không có</b> — người sau lưu đè mất thay đổi
        của người trước mà không ai biết.
      </div>
    </div>
    <div class="card" style="padding:15px 17px;margin-bottom:13px">
      <div class="sec">QUAY LẠI PHIÊN BẢN CŨ</div>
      <div style="font-size:12.5px;line-height:1.85">
        Bấm <b>↩</b> ở một phiên bản cũ thì hệ thống <b>không ghi đè trực tiếp</b> — nó
        <b>tạo một phiên bản mới</b> có nội dung giống bản cũ.<br><br>
        Lý do: lịch sử phải <b>chỉ thêm, không sửa</b>. Nếu ghi đè thì mất dấu vết ai đã
        quay lại và quay lại lúc nào.
      </div>
      <div class="note" style="background:#EFF4FF;border:1px solid #C7D7FE;margin-top:11px;
        font-size:12px">
        Bản quay lại vẫn phải <b>qua duyệt</b> như mọi thay đổi khác.
      </div>
    </div>
    <div class="note" style="background:#ECFDF3;border:1px solid #A6F4C5">
      ✅ <b>Tab này gần như không phải làm gì.</b> <span class="mono">job-version-history</span>
      đã có đủ.<br>
      Phần thêm: <b>khung so sánh hai phiên bản</b> hiện đúng phần khác nhau, và
      <b>cột người duyệt</b> để biết bản nào đã qua duyệt.
    </div>
  </div>
</div>"""
    return shell("dmp.vds.vn/orchestration/jobs/JOB-0412/versions", J_CRUMB, J_TITLE, J_DESC,
                 body, "DMP · Menu 4.1 — LUỒNG XỬ LÝ · Màn CHI TIẾT · Tab PHIÊN BẢN", "m41",
                 tabs=("Phiên bản", J_TABS), actions=J_ACT)


# ==================================================== 4.2 tab Vùng chờ
def ingest_quarantine():
    lots = [
        ("LO-4412", "NAP-012 · File đối soát A", "07/08 05:31", "🛑 Chặn cả lô",
         "Số dòng 218.440 — dưới ngưỡng 300.000", "218.440", "SC-0242", "Chờ xử lý"),
        ("LO-4408", "NAP-101 · HDFS đối tác B", "07/08 04:00", "⚠️ Tách dòng lỗi",
         "1.204 dòng sai định dạng số điện thoại", "1.204 / 88.310", "—", "Chờ xử lý"),
        ("LO-4391", "NAP-012 · File đối soát A", "06/08 05:30", "⚠️ Tách dòng lỗi",
         "88 dòng mã đối tác không có trong danh mục 1.4", "88 / 412.808", "—",
         "Đã cho qua"),
        ("LO-4377", "NAP-034 · Đồng bộ CRM", "05/08 09:30", "🛑 Chặn cả lô",
         "Cột ma_giao_dich rỗng ở 100% dòng", "12.044", "SC-0238", "Đã huỷ lô"),
    ]
    tr = ""
    for lid, src, t, lvl, why, n, sc, st in lots:
        lc = "r" if "Chặn" in lvl else "o"
        stc = {"Chờ xử lý": "o", "Đã cho qua": "g", "Đã huỷ lô": "n"}[st]
        tr += (f'<tr><td class="mono muted">{lid}</td><td><b>{src}</b></td><td>{t}</td>'
               f'<td style="white-space:nowrap">{chip(lvl, lc)}</td>'
               f'<td class="muted">{why}</td><td style="text-align:right">{n}</td>'
               f'<td class="mono" style="color:{AC}">{sc}</td><td>{chip(st, stc)}</td>'
               f'<td style="white-space:nowrap"><span class="ico">👁</span></td></tr>')

    bad = "".join(
        f'<tr><td style="text-align:right" class="muted">{a}</td>'
        f'<td class="mono" style="font-size:11.5px">{b}</td>'
        f'<td class="mono" style="font-size:11.5px;color:#B42318">{c}</td>'
        f'<td class="muted">{d}</td></tr>'
        for a, b, c, d in [
            ("dòng 412", "GD20260807000412", "098765432", "Thiếu 1 chữ số"),
            ("dòng 1.088", "GD20260807001088", "84987654321", "Có mã quốc gia — cần chuẩn hoá"),
            ("dòng 2.331", "GD20260807002331", "(rỗng)", "Không có số điện thoại"),
            ("dòng 3.907", "GD20260807003907", "0987-654-321", "Có dấu gạch nối")])

    body = _kpi([
        ("LÔ ĐANG CHỜ XỬ LÝ", "2", "cũ nhất chờ 2 giờ", "#B54708"),
        ("DÒNG LỖI ĐANG GIỮ", "219.644", "chưa vào bảng đích", "#B42318"),
        ("LÔ BỊ CHẶN 30 NGÀY", "9", "so với 0 trước khi có cổng chất lượng", "#101828"),
        ("THỜI GIAN XỬ LÝ TRUNG BÌNH", "3,1 giờ", "mục tiêu: dưới 4 giờ", "#067647"),
        ("DUNG LƯỢNG VÙNG CHỜ", "4,2 GB", "tự xoá lô đã xử lý sau 30 ngày", "#101828"),
    ]) + f"""
<div class="card" style="margin-bottom:14px"><table class="g">
  <tr><th>Mã lô</th><th>Đến từ mẫu nạp</th><th>Thời điểm</th><th>Mức chặn</th>
    <th>Vì sao bị giữ</th><th style="text-align:right">Dòng bị giữ</th><th>Sự cố</th>
    <th>Trạng thái</th><th></th></tr>{tr}</table></div>
<div style="display:flex;gap:16px">
  <div style="flex:1.2">
    <div class="card" style="padding:16px 19px;margin-bottom:14px">
      <div class="sec">LÔ LO-4408 — 1.204 DÒNG SAI ĐỊNH DẠNG SỐ ĐIỆN THOẠI</div>
      <table class="g" style="font-size:12.5px">
        <tr><th style="width:90px;text-align:right">Vị trí</th><th>Mã giao dịch</th>
          <th>Giá trị sai</th><th>Sai chỗ nào</th></tr>{bad}</table>
      <div style="padding:8px 0;font-size:12px" class="muted">… và 1.200 dòng khác</div>
      <div style="margin-top:6px;display:flex;gap:9px">
        <span class="btn w">⬇️ Tải 1.204 dòng lỗi về Excel</span>
        <span class="btn w">📤 Nạp lại file đã sửa</span></div>
    </div>
    <div class="card" style="padding:16px 19px">
      <div class="sec">BỐN HÀNH ĐỘNG TRÊN MỘT LÔ</div>
      <table class="g" style="font-size:12.5px">
        <tr><th>Hành động</th><th>Hệ thống làm gì</th><th>Ai được làm</th></tr>
        <tr><td><b>✔ Cho qua</b></td>
            <td>Ghi hết vào bảng đích, <b>kể cả dòng lỗi</b>. Ghi nhật ký 5.4 kèm lý do</td>
            <td>BDA phụ trách bảng đích</td></tr>
        <tr><td><b>✂️ Chỉ ghi dòng đúng</b></td>
            <td>Ghi phần đạt, <b>giữ lại dòng lỗi</b> chờ nạp bổ sung</td>
            <td>DE phụ trách</td></tr>
        <tr><td><b>📤 Nạp lại file đã sửa</b></td>
            <td>Thay lô cũ bằng lô mới, <b>chạy lại cổng chất lượng</b> từ đầu</td>
            <td>DE phụ trách</td></tr>
        <tr><td><b>✕ Huỷ lô</b></td>
            <td>Xoá khỏi vùng chờ, <b>không ghi gì</b>. Đóng sự cố liên quan ở 3.4</td>
            <td>BDA phụ trách bảng đích</td></tr>
      </table>
      <div class="note" style="background:#FFFAEB;border:1px solid #FEDF89;margin-top:11px;
        font-size:12.5px">
        ⚠️ <b>"Cho qua" bắt buộc điền lý do và luôn để lại dấu vết.</b><br>
        Nếu một mẫu nạp bị cho qua nhiều lần thì đó là dấu hiệu <b>luật ở cổng đặt sai</b> —
        thống kê này hiện ở màn 53 Sức khoẻ dữ liệu, cùng chỗ với tỉ lệ báo động giả.
      </div>
    </div>
  </div>
  <div style="width:520px;flex-shrink:0">
    <div class="note" style="background:#FEF3F2;border:1px solid #FECDCA;margin-bottom:13px">
      🔴 <b>Không có tab này thì cổng chất lượng ở màn 37 chỉ mới làm được nửa việc.</b><br><br>
      Chặn dữ liệu xấu là một chuyện. Nhưng <b>lô bị chặn phải đi đâu, ai xử lý, xử lý thế nào</b>
      mới là phần quyết định người dùng có chịu bật cổng hay không.<br><br>
      Không có nơi xử lý rõ ràng thì lần đầu bị chặn giữa đêm, đội vận hành sẽ
      <b>tắt luôn cổng chất lượng</b> — và mọi thứ quay về như cũ.
    </div>
    <div class="card" style="padding:15px 17px;margin-bottom:13px">
      <div class="sec">LÔ BỊ CHẶN TỰ MỞ SỰ CỐ</div>
      <div style="font-size:12.5px;line-height:1.85">
        Mức <b>🛑 Chặn cả lô</b> tự mở sự cố ở <b>menu 3.4</b>:<br><br>
        <b>Gán cho</b> — DE phụ trách bảng đích<br>
        <b>Mức ưu tiên</b> — theo Tier của bảng đích<br>
        <b>Hạn xử lý</b> — Tier 1: 4 giờ · Tier 2: 1 ngày<br>
        <b>Đóng sự cố</b> — tự đóng khi lô được cho qua, nạp lại thành công, hoặc huỷ
      </div>
      <div class="muted" style="font-size:11.5px;margin-top:9px">
        Mức <b>⚠️ Tách dòng lỗi</b> <b>không</b> mở sự cố — chỉ gửi cảnh báo, vì dữ liệu
        đúng vẫn vào bảng bình thường.</div>
    </div>
    <div class="note" style="background:#EFF4FF;border:1px solid #C7D7FE">
      🔗 <b>Vùng chờ nằm ở đâu về mặt kỹ thuật</b><br><br>
      Là một thư mục riêng trên HDFS, <b>chỉ tài khoản dịch vụ đọc được</b> — quyền khai ở
      <b>5.2 tab Quyền dữ liệu</b>.<br><br>
      Người dùng thường <b>không truy vấn được</b> dữ liệu trong vùng chờ, chỉ xem được
      mẫu dòng lỗi qua màn này. Nếu không siết chỗ này thì cổng chất lượng bị vòng qua dễ dàng.
    </div>
  </div>
</div>"""
    return shell("dmp.vds.vn/ingestion/quarantine",
                 "Ingestion &amp; Orchestration › Cửa nạp dữ liệu › Vùng chờ",
                 "📥 Cửa nạp dữ liệu",
                 "Lô dữ liệu bị cổng chất lượng giữ lại — chờ người quyết định",
                 body, "DMP · Menu 4.2 — CỬA NẠP DỮ LIỆU · Tab VÙNG CHỜ", "m42",
                 tabs=("Vùng chờ", ["Mẫu nạp", "Lịch sử nạp", "Cổng chất lượng", "Vùng chờ"]),
                 actions='<span class="btn w">⬇️ Tải dòng lỗi</span>')


# ==================================================== 5.1 tab Nhóm & Quyền menu
def group_acl():
    grps = [
        ("ban_kinh_doanh", "Ban Kinh doanh", "184", "Miền Kinh doanh", "4 chính sách", "LDAP"),
        ("bda_kinh_doanh", "BDA Ban Kinh doanh", "12", "Miền Kinh doanh", "9 chính sách", "Thủ công"),
        ("doi_de", "Đội Data Engineer", "18", "Toàn bộ vùng thô", "12 chính sách", "Thủ công"),
        ("ban_tai_chinh", "Ban Tài chính", "96", "Miền Tài chính", "3 chính sách", "LDAP"),
        ("ctv_thue_ngoai", "Cộng tác viên thuê ngoài", "24", "2 bảng cụ thể", "6 chính sách",
         "Thủ công"),
        ("truong_don_vi", "Trưởng đơn vị", "31", "—", "1 chính sách", "Thủ công"),
    ]
    tr = ""
    for c_, nm, n, scope, npol, src in grps:
        tr += (f'<tr><td class="mono" style="color:{AC}">{c_}</td><td><b>{nm}</b></td>'
               f'<td style="text-align:center">{n}</td><td class="muted">{scope}</td>'
               f'<td>{npol}</td><td>{chip(src, "b" if src == "LDAP" else "n")}</td>'
               f'<td style="white-space:nowrap"><span class="ico">👁</span>'
               f'<span class="ico">✎</span></td></tr>')

    MENUS = ["1.1 Bảng dữ liệu", "1.4 Danh mục tham chiếu", "3.1 Thư viện luật",
             "3.2 Luật & Kết quả", "3.4 Sự cố chất lượng", "4.1 Luồng xử lý",
             "5.2 Chính sách truy cập", "5.4 Nhật ký kiểm toán", "6.2 Cấu hình hệ thống"]
    MTX = {
        "1.1 Bảng dữ liệu":          ["XS", "XS", "XS", "X", "X"],
        "1.4 Danh mục tham chiếu":   ["XS", "XSD", "X", "X", "—"],
        "3.1 Thư viện luật":         ["XSD", "X", "X", "X", "—"],
        "3.2 Luật & Kết quả":        ["XS", "XS", "XS", "X", "—"],
        "3.4 Sự cố chất lượng":      ["XS", "XSD", "XS", "X", "—"],
        "4.1 Luồng xử lý":           ["X", "XD", "XS", "X", "—"],
        "5.2 Chính sách truy cập":   ["XS", "XS", "—", "—", "XSD"],
        "5.4 Nhật ký kiểm toán":     ["X", "X", "—", "—", "X"],
        "6.2 Cấu hình hệ thống":     ["XS", "—", "—", "—", "XS"],
    }
    COLS = ["QTDL", "BDA", "DE", "ND", "QTHT"]

    def cell(v):
        if v == "—":
            return '<td style="text-align:center;color:#d0d7e2">—</td>'
        m = {"X": ("Xem", "b"), "XS": ("Xem·Sửa", "o"), "XD": ("Xem·Duyệt", "t"),
             "XSD": ("Xem·Sửa·Duyệt", "g")}[v]
        return f'<td style="text-align:center;white-space:nowrap">{chip(*m)}</td>'

    mtx = "".join(
        f'<tr><td><b>{m}</b></td>' + "".join(cell(v) for v in MTX[m]) + "</tr>"
        for m in MENUS)

    body = f"""
<div style="display:flex;gap:16px">
  <div style="flex:1">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
      <div style="font-size:13.5px;font-weight:700">47 nhóm người dùng</div>
      <div style="display:flex;gap:8px"><span class="btn w">📥 Đồng bộ LDAP</span>
        <span class="btn">➕ Tạo nhóm</span></div></div>
    <div class="card" style="margin-bottom:14px"><table class="g">
      <tr><th>Mã nhóm</th><th>Tên nhóm</th><th style="text-align:center">Số người</th>
        <th>Phạm vi dữ liệu</th><th>Chính sách ở 5.2</th><th>Nguồn</th><th></th></tr>{tr}</table>
      <div style="padding:9px 12px;font-size:12px" class="muted">… và 41 nhóm khác</div></div>
    <div class="card" style="padding:16px 19px">
      <div class="sec">MA TRẬN QUYỀN MENU × VAI TRÒ &nbsp;<span class="muted"
        style="font-weight:400;font-size:11px">(trích 9/21 menu)</span></div>
      <table class="g" style="font-size:12.5px">
        <tr><th>Menu</th>{"".join(f'<th style="text-align:center">{c}</th>' for c in COLS)}</tr>
        {mtx}</table>
      <div style="display:flex;gap:16px;font-size:11.5px;color:#667085;margin-top:10px">
        <span><b>QTDL</b> Quản trị dữ liệu</span><span><b>BDA</b> BDA phụ trách bảng</span>
        <span><b>DE</b> DE phụ trách bảng</span><span><b>ND</b> Người dùng thường</span>
        <span><b>QTHT</b> Quản trị hệ thống</span></div>
    </div>
  </div>
  <div style="width:520px;flex-shrink:0">
    <div class="note" style="background:#ECFDF3;border:1px solid #A6F4C5;margin-bottom:13px">
      ✅ <b>Toàn bộ tab này SQLWF đã có — giữ nguyên.</b><br>
      <span class="mono">group-management</span> quản nhóm ·
      <span class="mono">acl</span> chính là <b>ma trận Menu chức năng × Quyền</b> ·
      <span class="mono">feature-menu-authorization</span> ·
      <span class="mono">group-authorize</span> gắn nhóm quyền với menu.<br><br>
      Phần thêm: <b>cột "Phạm vi dữ liệu"</b> và <b>cột "Chính sách ở 5.2"</b> — để nhìn một chỗ
      thấy được nhóm này ngoài quyền menu còn có quyền dữ liệu gì.
    </div>
    <div class="card" style="padding:16px 19px;margin-bottom:13px;background:#FFFAEB;
      border-color:#FEDF89">
      <div class="sec" style="color:#B54708;border-color:#B54708">
        ⚠️ HAI CỘT NÀY LÀ HAI THẾ GIỚI KHÁC NHAU</div>
      <table class="g" style="font-size:12.5px;background:#fff">
        <tr><th></th><th>Ma trận ở đây</th><th>Chính sách ở 5.2</th></tr>
        <tr><td style="width:110px;color:#667085">Quản cái gì</td>
            <td><b>Mở được MÀN nào</b></td><td><b>Đọc được DỮ LIỆU nào</b></td></tr>
        <tr><td style="color:#667085">Ví dụ</td>
            <td>Mở được màn <i>Bảng dữ liệu</i></td>
            <td>Nhưng chỉ thấy <b>412 / 11.482 bảng</b></td></tr>
        <tr><td style="color:#667085">Ai khai</td><td>QTHT</td><td>QTHT · BDA phụ trách bảng</td></tr>
      </table>
      <div style="font-size:12.5px;margin-top:11px;line-height:1.7">
        🔴 <b>Đây là chỗ SQLWF đang trộn lẫn.</b> Màn
        <span class="mono">user-managerment</span> để các cột
        <i>Phân quyền truy cập dữ liệu</i> · <i>Phân quyền File View</i> ·
        <i>Phân quyền danh mục</i> · <i>Phân quyền PYC</i> <b>nằm cạnh quyền menu</b> —
        người khai rất khó biết mình đang cấp cái gì.
      </div>
    </div>
    <div class="note" style="background:#EFF4FF;border:1px solid #C7D7FE">
      💡 <b>Nhóm đồng bộ từ LDAP thì không sửa thành viên ở đây.</b><br><br>
      Nhóm nguồn <b>LDAP</b> chỉ đọc — thêm/bớt người làm ở hệ thống nhân sự, DMP đồng bộ về.
      Nhóm nguồn <b>Thủ công</b> mới sửa được ở màn này.<br><br>
      Cách này giúp <b>người nghỉ việc tự rời khỏi mọi nhóm LDAP</b> mà không cần ai nhớ — bịt
      đúng lỗ hổng 9 tài khoản đã nghỉ vẫn còn quyền.
    </div>
  </div>
</div>"""
    return shell("dmp.vds.vn/security/users/groups", "Data Security › Người dùng &amp; Nhóm › Nhóm",
                 "👥 Người dùng &amp; Nhóm",
                 "Nhóm người dùng và ma trận quyền truy cập MENU",
                 body, "DMP · Menu 5.1 — NGƯỜI DÙNG &amp; NHÓM · Tab NHÓM + QUYỀN MENU", "m51",
                 tabs=("Nhóm", ["Người dùng", "Nhóm", "Vai trò", "Quyền menu (ACL)"]),
                 actions='<span class="btn w">📥 Đồng bộ LDAP</span>'
                         '<span class="btn">➕ Tạo nhóm</span>')


# ==================================================== 5.2 form thêm chính sách che
def mask_create():
    mk = "".join(
        f'<tr style="{"background:#EFF4FF" if a == "Hiện 4 số cuối" else ""}">'
        f'<td style="text-align:center">{"◉" if a == "Hiện 4 số cuối" else "○"}</td>'
        f'<td><b>{a}</b></td><td class="mono" style="font-size:11.5px">{b}</td>'
        f'<td class="mono" style="font-size:11.5px;color:#B54708">{c}</td></tr>'
        for a, b, c, d in MASK_ROWS)

    body = _steps([("Chọn cột", "done"), ("Chọn kiểu che", "now"),
                   ("Áp cho ai", "next"), ("Xem thử & lưu", "next")]) + f"""
<div style="display:flex;gap:18px">
  <div style="width:480px;flex-shrink:0">
    <div class="card" style="padding:17px 19px;margin-bottom:13px">
      <div class="sec">① CHỌN CỘT CẦN CHE</div>
      {fld("Phạm vi áp dụng", "🏷️ Theo NHÃN ▾", True,
           "⭐ <b>Ba lựa chọn:</b> theo <b>nhãn</b> (áp cho mọi cột mang nhãn, kể cả cột gắn "
           "nhãn sau này) · theo <b>một cột cụ thể</b> · theo <b>tên cột</b> (biểu thức)")}
      {fld("Nhãn", "PD_SENSITIVE — Dữ liệu cá nhân nhạy cảm ▾", True,
           "Cây nhãn khai ở <b>menu 2.2</b>. Chính sách sẽ áp cho <b>144 cột</b> đang mang nhãn này")}
      <div class="note" style="background:#ECFDF3;border:1px solid #A6F4C5;font-size:12.5px">
        ⭐ <b>Chọn theo nhãn thay vì theo cột là điểm quan trọng nhất của màn này.</b><br>
        Khai <b>một dòng</b> áp cho <b>144 cột</b> hiện tại — và <b>mọi cột gắn nhãn
        PD_SENSITIVE sau này tự động được che</b>, không ai phải nhớ quay lại khai.
      </div>
      {fld("Loại trừ cột nào không?",
           chip("doi_de → so_dien_thoai (bảng đối soát)", "n") +
           '<span class="muted">+ Thêm ngoại lệ</span>',
           hint="Ngoại lệ <b>nới lỏng</b> phải có người duyệt — xem quy tắc ở tab "
                "<i>Chính sách theo nhãn</i>")}
    </div>
    <div class="card" style="padding:17px 19px">
      <div class="sec">③ ÁP CHO AI</div>
      {fld("Nhóm người dùng", "👥 ban_kinh_doanh ▾", True,
           "Khai theo <b>nhóm</b>, không khai theo từng người — nếu không sẽ có 1.435 dòng "
           "chính sách như hiện nay")}
      {fld("Thời hạn", "Vô thời hạn ▾",
           hint="Chính sách <b>che</b> nên vô thời hạn — nó là ràng buộc thường trực. "
                "Khác với chính sách <b>cấp quyền</b> ở 5.3 luôn phải có hạn")}
      {fld("Mức ưu tiên", "Cấp 2 — chính sách theo nhãn con", ro=True,
           hint="Thứ tự ưu tiên do phạm vi quyết định, không tự đặt được")}
    </div>
  </div>
  <div style="flex:1">
    <div class="card" style="padding:17px 19px;margin-bottom:13px">
      <div class="sec">② CHỌN KIỂU CHE — 8 KIỂU</div>
      <table class="g" style="font-size:12.5px">
        <tr><th style="width:36px"></th><th>Kiểu che</th><th>Giá trị gốc</th>
          <th>Người dùng thấy</th></tr>{mk}</table>
    </div>
    <div class="card" style="padding:17px 19px;margin-bottom:13px;background:#0F1729;border:none">
      <div style="font-size:12.5px;font-weight:700;color:#8FA3C8;letter-spacing:.3px;
        margin-bottom:9px">④ XEM THỬ — CÂU SQL HỆ THỐNG SẼ VIẾT LẠI</div>
      <pre style="font-family:Consolas,monospace;font-size:12px;line-height:1.7;color:#E5E9F0;
        overflow:hidden"><span style="color:#8b95a7">-- người dùng ban_kinh_doanh gõ</span>
<span style="color:#93B4FF">SELECT</span> ma_giao_dich, so_dien_thoai
<span style="color:#93B4FF">FROM</span>   bi.doi_soat_giao_dich_A

<span style="color:#8b95a7">-- DMP viết lại trước khi gửi xuống engine</span>
<span style="color:#93B4FF">SELECT</span> ma_giao_dich,
       <span style="color:#FFD479">CONCAT('******', RIGHT(so_dien_thoai, 4))</span>
         <span style="color:#93B4FF">AS</span> so_dien_thoai
<span style="color:#93B4FF">FROM</span>   bi.doi_soat_giao_dich_A</pre>
    </div>
    <div style="display:flex;gap:13px;margin-bottom:13px">
      <div class="card" style="flex:1;padding:15px 17px">
        <div class="sec">CHÍNH SÁCH NÀY SẼ ĐỘNG TỚI</div>
        <table class="g" style="font-size:12.5px">
          <tr><td style="width:180px;color:#667085">Số cột bị che</td>
              <td><b style="color:#B54708">144 cột</b> trên 38 bảng</td></tr>
          <tr><td style="color:#667085">Số người bị ảnh hưởng</td><td><b>184 người</b></td></tr>
          <tr><td style="color:#667085">Số báo cáo đang đọc các cột này</td>
              <td><b style="color:#B42318">11 báo cáo</b></td></tr>
          <tr><td style="color:#667085">Có hiệu lực từ</td><td>Ngay khi lưu</td></tr>
        </table>
      </div>
      <div class="note" style="width:340px;background:#FEF3F2;border:1px solid #FECDCA">
        🔴 <b>11 báo cáo đang đọc các cột này.</b><br><br>
        Bật che ngay lập tức thì 11 báo cáo <b>đổi kết quả trong một đêm</b> mà người làm
        báo cáo không biết.<br><br>
        <b>Nên chọn "Có hiệu lực sau 7 ngày"</b> và gửi thông báo trước cho chủ sở hữu
        11 báo cáo đó.
      </div>
    </div>
    <div style="display:flex;gap:10px">
      <span class="btn">💾 Lưu chính sách</span>
      <span class="btn w">▶ Chạy thử với tài khoản khác</span>
      <span class="btn w">Huỷ</span></div>
  </div>
</div>"""
    return shell("dmp.vds.vn/security/policies/mask/create",
                 "Data Security › Chính sách truy cập › Che dữ liệu › Thêm",
                 "➕ Thêm chính sách che dữ liệu",
                 "Chọn cột · chọn kiểu che · chọn áp cho ai — hệ thống viết lại câu truy vấn",
                 body, "DMP · Menu 5.2 — CHÍNH SÁCH TRUY CẬP · Màn THÊM CHÍNH SÁCH CHE", "m52")


# ==================================================== 5.2 form thêm điều kiện lọc
def rowfilter_create():
    vars_ = "".join(
        f'<tr><td class="mono" style="font-size:11.5px;color:{AC}">{a}</td>'
        f'<td class="muted">{b}</td><td class="mono" style="font-size:11.5px">{c}</td></tr>'
        for a, b, c in [
            ("${chi_nhanh_cua_nguoi_dung}", "Mã chi nhánh trong hồ sơ người dùng ở 5.1", "'HN'"),
            ("${don_vi_cua_nguoi_dung}", "Mã đơn vị trong hồ sơ người dùng", "'KD-01'"),
            ("${nhom_cua_nguoi_dung}", "Danh sách nhóm người dùng thuộc về",
             "('ban_kinh_doanh')"),
            ("${tai_khoan}", "Tên tài khoản đăng nhập", "'le.minh.tuan'"),
            ("CURRENT_DATE", "Ngày hệ thống", "2026-08-07")])

    body = _steps([("Chọn bảng", "done"), ("Viết điều kiện", "now"),
                   ("Áp cho ai", "next"), ("Đối chiếu & lưu", "next")]) + f"""
<div style="display:flex;gap:18px">
  <div style="width:490px;flex-shrink:0">
    <div class="card" style="padding:17px 19px;margin-bottom:13px">
      <div class="sec">① CHỌN BẢNG</div>
      {fld("Bảng", "🗂️ bi.doi_soat_giao_dich_A ▾", True,
           "Chọn từ danh mục 1.1. <b>Chỉ lọc được bảng, không lọc được nhóm bảng hay miền</b> — "
           "vì mỗi bảng có cột lọc khác nhau")}
      {fld("Cột dùng để lọc", "ma_chi_nhanh ▾", True,
           "Hệ thống chỉ gợi ý các cột <b>đã có trong bảng</b> và có <b>ít giá trị phân biệt</b> "
           "— chi nhánh, đơn vị, vùng, loại thuê bao")}
      <div class="note" style="background:#EFF4FF;border:1px solid #C7D7FE;font-size:12.5px">
        💡 Cột <span class="mono">ma_chi_nhanh</span> có <b>63 giá trị phân biệt</b> trên
        12,4 triệu dòng — <b>phù hợp để lọc</b>.<br>
        Cột như <span class="mono">ma_giao_dich</span> (12,4 triệu giá trị) thì
        <b>không dùng lọc được</b>, hệ thống sẽ cảnh báo.
      </div>
    </div>
    <div class="card" style="padding:17px 19px">
      <div class="sec">③ ÁP CHO AI</div>
      {fld("Nhóm người dùng", "👥 ban_kinh_doanh ▾", True)}
      {fld("Nhóm được MIỄN lọc",
           chip("doi_de", "g") + chip("ban_tai_chinh", "g") +
           '<span class="muted">+ Thêm</span>',
           hint="Nhóm cần nhìn <b>toàn quốc</b> — đội vận hành và ban đối soát")}
      <div class="note" style="background:#FFFAEB;border:1px solid #FEDF89;font-size:12.5px">
        ⚠️ <b>Nhóm nào không nằm ở cả hai danh sách thì mặc định KHÔNG thấy dòng nào.</b><br>
        Đây là lựa chọn có chủ ý: quên khai còn hơn lộ dữ liệu. Người dùng gặp bảng trống
        sẽ đi hỏi ngay — còn dữ liệu lộ thì không ai biết.
      </div>
    </div>
  </div>
  <div style="flex:1">
    <div class="card" style="padding:17px 19px;margin-bottom:13px;background:#FFFAEB;
      border-color:#FEDF89">
      <div class="sec" style="color:#B54708;border-color:#B54708">② VIẾT ĐIỀU KIỆN LỌC</div>
      {fld("Kiểu điều kiện", "◉ Biến động &nbsp;&nbsp; ○ Cố định", True,
           "⭐ <b>Biến động</b> lấy giá trị từ hồ sơ người dùng — một dòng chính sách phục vụ "
           "cả 63 chi nhánh. <b>Cố định</b> phải sửa mỗi khi thêm chi nhánh")}
      <div class="fld"><div class="lb"><span class="req">*</span> Biểu thức điều kiện</div>
        <div style="background:#0F1729;border-radius:7px;padding:11px 13px;
          font-family:Consolas,monospace;font-size:12.5px;color:#E5E9F0">
          ma_chi_nhanh = <span style="color:#FFD479">${{chi_nhanh_cua_nguoi_dung}}</span></div>
        <div class="hp">Viết như mệnh đề <span class="mono">WHERE</span> —
          hệ thống nối thêm bằng <span class="mono">AND</span></div></div>
      <div style="font-size:12.5px;font-weight:700;margin:13px 0 7px">
        Biến dùng được trong biểu thức</div>
      <table class="g" style="font-size:12px;background:#fff">
        <tr><th>Biến</th><th>Lấy từ đâu</th><th>Giá trị mẫu</th></tr>{vars_}</table>
    </div>
    <div class="card" style="padding:17px 19px;margin-bottom:13px;background:#0F1729;border:none">
      <div style="font-size:12.5px;font-weight:700;color:#8FA3C8;letter-spacing:.3px;
        margin-bottom:9px">④ XEM THỬ VỚI TÀI KHOẢN le.minh.tuan (chi nhánh HN)</div>
      <pre style="font-family:Consolas,monospace;font-size:12px;line-height:1.7;color:#E5E9F0;
        overflow:hidden"><span style="color:#8b95a7">-- người dùng gõ</span>
<span style="color:#93B4FF">SELECT COUNT</span>(*) <span style="color:#93B4FF">FROM</span> bi.doi_soat_giao_dich_A

<span style="color:#8b95a7">-- DMP viết lại</span>
<span style="color:#93B4FF">SELECT COUNT</span>(*) <span style="color:#93B4FF">FROM</span> bi.doi_soat_giao_dich_A
<span style="color:#93B4FF">WHERE</span>  <span style="color:#FFD479">ma_chi_nhanh = 'HN'</span>

<span style="color:#8b95a7">-- kết quả</span>
<span style="color:#75E0A7">không lọc: 12.480.331 dòng  →  sau lọc: 1.842.104 dòng (14,8%)</span></pre>
    </div>
    <div style="display:flex;gap:13px">
      <div class="note" style="flex:1;background:#FEF3F2;border:1px solid #FECDCA">
        🔴 <b>Bắt buộc chạy đối chiếu trước khi lưu.</b><br><br>
        Hệ thống chạy thử với <b>5 tài khoản mẫu ở 5 chi nhánh khác nhau</b> và kiểm:
        tổng số dòng của 5 tài khoản có <b>bằng đúng số dòng gốc</b> không.<br><br>
        Lệch nghĩa là có dòng <b>không ai thấy được</b> — thường do cột lọc bị rỗng
        ở một số dòng. Đây là lỗi <b>im lặng</b>, không đối chiếu thì không phát hiện ra.
      </div>
      <div class="note" style="width:330px;background:#EFF4FF;border:1px solid #C7D7FE">
        💡 <b>Nhắc người dùng là bắt buộc.</b><br><br>
        Mọi kết quả truy vấn trên bảng có lọc đều hiện dòng:<br><br>
        <i>"Kết quả đã lọc theo phạm vi dữ liệu của bạn: <b>chi nhánh HN</b>"</i><br><br>
        Không có dòng này thì người dùng đếm ra số khác đồng nghiệp và tưởng dữ liệu hỏng.
      </div>
    </div>
    <div style="display:flex;gap:10px;margin-top:15px">
      <span class="btn">▶ Chạy đối chiếu 5 tài khoản</span>
      <span class="btn w">💾 Lưu (khoá tới khi đối chiếu đạt)</span>
      <span class="btn w">Huỷ</span></div>
  </div>
</div>"""
    return shell("dmp.vds.vn/security/policies/rowfilter/create",
                 "Data Security › Chính sách truy cập › Lọc theo dòng › Thêm",
                 "➕ Thêm điều kiện lọc theo dòng",
                 "Điều kiện được nối vào câu truy vấn — người dùng không thấy và không gỡ được",
                 body, "DMP · Menu 5.2 — CHÍNH SÁCH TRUY CẬP · Màn THÊM ĐIỀU KIỆN LỌC", "m52")


# ==================================================== 5.3 form xin quyền
def request_create():
    body = _steps([("Chọn dữ liệu cần xin", "done"), ("Điền lý do & thời hạn", "now"),
                   ("Gửi duyệt", "next")]) + f"""
<div style="display:flex;gap:18px">
  <div style="width:520px;flex-shrink:0">
    <div class="card" style="padding:17px 19px;margin-bottom:13px">
      <div class="sec">① XIN QUYỀN TRÊN</div>
      {fld("Phạm vi", "🗂️ Một bảng ▾", True,
           "Một bảng · Nhóm bảng · Miền dữ liệu · Thư mục HDFS")}
      {fld("Bảng", "🗂️ bi.doi_soat_giao_dich_A ▾", True,
           "Gõ tên hoặc mô tả nghiệp vụ — dùng chung ô tìm kiếm với menu 1.1")}
      <div class="note" style="background:#F8FAFC;border:1px solid #e3e8ef;font-size:12.5px;
        margin-bottom:13px">
        <b>Đối soát giao dịch — Đối tác A</b><br>
        {chip("Tier 1", "o")}{chip("Miền Kinh doanh", "b")}{chip("2 cột PD_SENSITIVE", "r")}<br>
        <span class="muted">BDA: Nguyễn Thị Phương · DE: Trần Văn Hùng · 12,4 triệu dòng ·
        cập nhật hằng ngày 06:00</span>
      </div>
      {fld("Loại quyền", "◉ Xem &nbsp;&nbsp; ○ Xem · Ghi &nbsp;&nbsp; ○ Xem · Ghi · Xoá", True,
           "Xin quyền <b>Ghi</b> thì người duyệt là DE phụ trách, không phải BDA")}
      {fld("Có cần xem cột nhạy cảm không?",
           "☐ Có — cần xem <span class='mono'>so_dien_thoai</span> và "
           "<span class='mono'>so_cccd</span> nguyên giá trị",
           hint="⚠️ Bỏ trống thì mặc định <b>xin quyền xem có che</b>. "
                "Tích vào thì <b>phải nêu rõ lý do vì sao cần giá trị gốc</b> ở ô dưới")}
    </div>
    <div class="note" style="background:#EFF4FF;border:1px solid #C7D7FE">
      💡 <b>Hệ thống tự tìm người duyệt — người xin không phải hỏi ai duyệt.</b><br><br>
      Người duyệt = <b>BDA phụ trách bảng</b> khai ở 1.1 → <b>Nguyễn Thị Phương</b>.<br>
      Nếu bảng chưa có BDA thì yêu cầu chuyển lên <b>trưởng miền</b>, và bảng được đưa vào
      danh sách <i>thiếu người phụ trách</i> ở màn 53.
    </div>
  </div>
  <div style="flex:1">
    <div class="card" style="padding:17px 19px;margin-bottom:13px;background:#FFFAEB;
      border-color:#FEDF89">
      <div class="sec" style="color:#B54708;border-color:#B54708">
        ② LÝ DO VÀ THỜI HẠN — HAI TRƯỜNG QUYẾT ĐỊNH</div>
      {fld("Lý do cần dùng", "Làm báo cáo đối soát quý III theo yêu cầu của Ban Sản phẩm. "
                             "Cần số liệu giao dịch của 3 tháng 7, 8, 9 để đối chiếu với "
                             "số liệu đối tác gửi.", True,
           "⭐ <b>Tối thiểu 30 ký tự.</b> Đây là thứ người duyệt đọc để quyết định, và là thứ "
           "kiểm toán đọc lại về sau. Lý do kiểu <i>&laquo;cần cho công việc&raquo;</i> sẽ bị từ chối")}
      {fld("Thời hạn cần dùng", "3 tháng — đến 07/11/2026 ▾", True,
           "1 tháng · 3 tháng · 6 tháng · 1 năm. <b>Không có tuỳ chọn vô thời hạn</b> — "
           "hết hạn mà còn cần thì xin gia hạn một cú bấm")}
      {fld("Người cùng cần quyền này?",
           chip("nguyen.van.b", "n") + '<span class="muted">+ Thêm người</span>',
           hint="Xin cho nhiều người trong <b>một yêu cầu</b> thay vì mỗi người gửi một cái — "
                "người duyệt xử lý một lần")}
      <div class="note" style="background:#fff;border:1px solid #d0d7e2;font-size:12.5px">
        ⚠️ <b>Đã có 4/9 người trong nhóm <span class="mono">ban_san_pham</span> xin bảng này.</b>
        Quá nửa nhóm cần thì nên <b>xin cấp cho cả nhóm</b> — bấm
        <i>Chuyển sang xin theo nhóm</i>, người duyệt chỉ phải duyệt một lần và về sau
        người mới vào nhóm có quyền luôn.
      </div>
    </div>
    <div style="display:flex;gap:13px;margin-bottom:13px">
      <div class="card" style="flex:1;padding:15px 17px">
        <div class="sec">GỬI XONG THÌ ĐIỀU GÌ XẢY RA</div>
        <div style="font-size:12.5px;line-height:1.9">
          ① Yêu cầu vào hàng chờ của <b>N.T.Phương</b><br>
          ② Nhắc người duyệt sau <b>4 giờ</b><br>
          ③ Quá <b>1 ngày làm việc</b> → chuyển lên trưởng miền<br>
          ④ Duyệt xong → quyền có hiệu lực <b>ngay</b><br>
          ⑤ Nhắc trước <b>7 ngày</b> khi sắp hết hạn<br>
          ⑥ Hết hạn → <b>tự thu hồi</b>
        </div>
      </div>
      <div class="note" style="width:350px;background:#ECFDF3;border:1px solid #A6F4C5">
        ✅ <b>Người duyệt được hạ mức, không chỉ Đồng ý / Từ chối.</b><br><br>
        Yêu cầu này nhiều khả năng được duyệt ở mức <b>Xem có che</b> — vẫn dùng được
        cho việc đối soát, mà <span class="mono">so_dien_thoai</span> và
        <span class="mono">so_cccd</span> trả về NULL.<br><br>
        Nên <b>không cần tích ô "cần xem cột nhạy cảm"</b> nếu thật sự không dùng tới.
      </div>
    </div>
    <div style="display:flex;gap:10px">
      <span class="btn">Gửi yêu cầu</span>
      <span class="btn w">👥 Chuyển sang xin theo nhóm</span>
      <span class="btn w">Lưu nháp</span></div>
  </div>
</div>"""
    return shell("dmp.vds.vn/security/requests/create",
                 "Data Security › Yêu cầu cấp quyền › Xin quyền", "✋ Xin quyền truy cập",
                 "Chọn dữ liệu · nêu lý do · chọn thời hạn — hệ thống tự tìm người duyệt",
                 body, "DMP · Menu 5.3 — YÊU CẦU CẤP QUYỀN · Màn XIN QUYỀN", "m53")


SCREENS = {
    "dmp-30-alert-channels": alert_channels,
    "dmp-32-job-create": job_create,
    "dmp-35-job-versions": job_versions,
    "dmp-38-ingest-quarantine": ingest_quarantine,
    "dmp-41-group-acl": group_acl,
    "dmp-44-mask-create": mask_create,
    "dmp-46-rowfilter-create": rowfilter_create,
    "dmp-49-request-create": request_create,
}
