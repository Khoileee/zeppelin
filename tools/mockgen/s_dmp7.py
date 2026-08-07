# -*- coding: utf-8 -*-
"""DMP — Module ④ Ingestion & Orchestration: 4.1 Job, 4.2 Cửa nạp, 4.3 Theo dõi & Pipeline."""
from dmp import shell, fld, chip, AC
from s_dmp2 import _kpi
from s_dmp3 import _steps

# ------------------------------------------------------------------ tiện ích sơ đồ
AH = ('<defs><marker id="ah" markerWidth="9" markerHeight="8" refX="8" refY="3" '
      'orient="auto"><path d="M0,0 L8,3 L0,6 z" fill="#98a2b3"/></marker>'
      '<marker id="ahr" markerWidth="9" markerHeight="8" refX="8" refY="3" '
      'orient="auto"><path d="M0,0 L8,3 L0,6 z" fill="#F04438"/></marker></defs>')


def _svg(w, h, paths):
    return (f'<svg width="{w}" height="{h}" style="position:absolute;left:0;top:0">'
            + AH + "".join(paths) + "</svg>")


def _pl(pts, color="#98a2b3", mk="ah", dash=None):
    d = " ".join(f"{x},{y}" for x, y in pts)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<polyline points="{d}" fill="none" stroke="{color}" stroke-width="1.8"'
            f'{da} marker-end="url(#{mk})"/>')


def _node(x, y, w, h, title, sub, border, bg="#fff", badge="", tcol="#101828"):
    bd = (f'<div style="position:absolute;top:-9px;right:-7px;font-size:10px;font-weight:700;'
          f'padding:1px 7px;border-radius:9px;{badge[1]}">{badge[0]}</div>') if badge else ""
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
            f'border:1.8px solid {border};background:{bg};border-radius:8px;padding:6px 8px;'
            f'font-size:11.5px;line-height:1.3">{bd}'
            f'<div style="font-weight:700;color:{tcol}">{title}</div>'
            f'<div style="color:#667085;font-size:10.5px;margin-top:2px">{sub}</div></div>')


# ============================================================ 4.1 danh sách job
def job_list():
    rows = [
        ("JOB-0412", "Đối soát giao dịch đối tác A", "Đối soát", "bi.doi_soat_giao_dich_A", "5",
         "06:00 hằng ngày", "Hôm nay 06:02 · 2 ph 14 gy", "ok", "Bật", "Đã duyệt"),
        ("JOB-0119", "Tổng hợp doanh thu ngày", "Tài chính", "bi.doanh_thu_thang", "8",
         "07:00 hằng ngày", "Hôm nay 07:11 · 6 ph 03 gy", "ok", "Bật", "Đã duyệt"),
        ("JOB-0087", "Thuê bao hoạt động theo ngày", "Kinh doanh", "dwh.thue_bao_ngay", "4",
         "05:30 hằng ngày", "Hôm nay 05:33 · 1 ph 47 gy", "ok", "Tắt", "Đã duyệt"),
        ("JOB-0233", "Làm sạch danh bạ khách hàng", "CRM", "crm.khach_hang", "6",
         "02:00 Chủ nhật", "04/08 02:00 · 11 ph", "ok", "Tắt", "Đã duyệt"),
        ("JOB-0501", "KPI kinh doanh tháng", "Kinh doanh", "mart.kpi_kinh_doanh_v2", "12",
         "03:00 ngày 1", "01/08 03:00 · 24 ph", "err", "Tắt", "Đã duyệt"),
        ("JOB-0644", "Nạp log truy cập cổng dịch vụ", "Vận hành", "ops.log_truy_cap", "3",
         "mỗi 15 phút", "Hôm nay 09:45 · 38 gy", "ok", "Tắt", "Chờ duyệt"),
    ]
    tr = ""
    for code, nm, grp, tbl, nstep, sched, last, st, lin, appr in rows:
        warn = tbl in ("mart.kpi_kinh_doanh_v2", "ops.log_truy_cap")
        tcell = (f'<span class="mono">{tbl}</span>' +
                 ('<br><span style="font-size:10.5px;color:#B42318">⚠ không có trong danh mục 1.1</span>'
                  if warn else ""))
        tr += (f'<tr><td class="mono muted">{code}</td>'
               f'<td><b style="color:{AC}">{nm}</b></td><td>{grp}</td>'
               f'<td>{tcell}</td><td style="text-align:center">{nstep}</td>'
               f'<td class="muted">{sched}</td>'
               f'<td>{last}</td>'
               f'<td>{chip("Thành công", "g") if st == "ok" else chip("Hỏng bước 7", "r")}</td>'
               f'<td>{chip(lin, "g" if lin == "Bật" else "n")}</td>'
               f'<td>{chip(appr, "g" if appr == "Đã duyệt" else "o")}</td>'
               f'<td style="white-space:nowrap"><span class="ico">👁</span>'
               f'<span class="ico">✎</span><span class="ico">▶</span></td></tr>')

    body = _kpi([
        ("TỔNG SỐ JOB", "1.842", "1.514 đang bật · 328 tắt", "#101828"),
        ("HỎNG TRONG 24 GIỜ", "17", "5 job đã hỏng 3 ngày liên tiếp", "#B42318"),
        ("BẬT QUÉT NGUỒN GỐC", "?", "chưa có số liệu — cần đội vận hành trả lời (H5)", "#B54708"),
        ("BẢNG ĐÍCH KHÔNG CÓ TRONG DANH MỤC", "214", "job ghi ra bảng chưa ai khai ở 1.1", "#B42318"),
        ("JOB KHÔNG AI CHẠY 90 NGÀY", "186", "ứng viên rà soát để tắt", "#B54708"),
    ]) + f"""
<div style="display:flex;gap:10px;margin-bottom:13px;align-items:center">
  <div style="flex:1;border:1px solid #d0d7e2;border-radius:8px;padding:9px 13px;font-size:13px;
    background:#fff">🔍 <span class="muted">Tìm theo mã job, tên job, bảng đích, câu SQL…</span></div>
  <span class="btn w">Nhóm: tất cả ▾</span><span class="btn w">Trạng thái chạy: tất cả ▾</span>
  <span class="btn w">Chỉ job đang hỏng ☐</span><span class="btn w">Bảng đích chưa khai ☐</span>
</div>
<div class="card"><table class="g">
  <tr><th>Mã job</th><th>Tên job</th><th>Nhóm</th><th>Bảng đích</th>
    <th style="text-align:center">Bước</th><th>Lịch chạy</th><th>Lần chạy gần nhất</th>
    <th>Kết quả</th><th>Quét nguồn gốc</th><th>Duyệt</th><th></th></tr>{tr}</table></div>
<div style="display:flex;gap:14px;margin-top:14px">
  <div class="note" style="flex:1;background:#ECFDF3;border:1px solid #A6F4C5">
    ✅ <b>SQLWF <span class="mono">job-management</span> đã rất mạnh — giữ gần như nguyên.</b><br>
    Chuỗi bước có phụ thuộc (DAG) · sơ đồ bước · trình xem SQL · quy trình xin duyệt / duyệt / từ chối ·
    <b>lịch sử phiên bản</b> · <b>xử lý xung đột khi 2 người sửa cùng lúc</b> ·
    <b>khoá phiên chỉnh sửa</b> · nhân bản job · chế độ chạy thử.<br>
    Đây là một trong những màn <b>hoàn thiện nhất của SQLWF</b> — không có lý do gì làm lại.<br><br>
    Phần lịch chạy do <span class="mono">pentaho-job-management</span> đảm nhiệm, cũng giữ nguyên.
    DMP chỉ <b>hiển thị lịch chung một chỗ</b> với job, thay vì bắt người dùng mở hai màn khác nhau
    để biết một job chạy lúc mấy giờ.<br><br>
    <b>Kết luận cho menu 4.1: giữ toàn bộ phần chạy, chỉ thêm hai ràng buộc ở phần khai báo.</b>
  </div>
  <div class="note" style="width:520px;background:#FEF3F2;border:1px solid #FECDCA">
    🔴 <b>Chỉ thiếu đúng hai thứ — nhưng cả hai đều làm hỏng module khác:</b><br><br>
    ① <b>Bảng đích không bị ép phải có trong danh mục 1.1.</b> 214 job đang ghi ra bảng
    chưa ai khai → những bảng đó <b>không có người phụ trách, không có luật chất lượng,
    không lên được sơ đồ nguồn gốc</b>.<br><br>
    ② <b>Cờ quét nguồn gốc mặc định TẮT.</b> Job nào không bật thì tab Nguồn gốc của 1.1
    trống — đây là <b>nguyên nhân gốc</b> khiến lineage hiện phủ rất ít bảng.
  </div>
</div>"""
    return shell("dmp.vds.vn/orchestration/jobs", "Ingestion &amp; Orchestration › Luồng xử lý",
                 "⚙️ Luồng xử lý (Job)",
                 "Chuỗi bước SQL có phụ thuộc, chạy theo lịch, ghi kết quả ra bảng đích",
                 body, "DMP · Menu 4.1 — LUỒNG XỬ LÝ · Màn DANH SÁCH", "m41",
                 tabs=("Tất cả job", ["Tất cả job", "Đang hỏng", "Chờ duyệt", "Tôi phụ trách",
                                      "Bảng đích chưa khai"]),
                 actions='<span class="btn w">⧉ Nhân bản</span>'
                         '<span class="btn">➕ Tạo job</span>')


# ============================================================ 4.1 chi tiết job — tab Bước
J_TABS = ["Bước", "Lịch chạy", "Lần chạy", "Phiên bản", "Cảnh báo"]
J_CRUMB = "Ingestion &amp; Orchestration › Luồng xử lý › JOB-0412"
J_TITLE = "⚙️ JOB-0412 — Đối soát giao dịch đối tác A"
J_DESC = ("Nhóm: Đối soát &nbsp;·&nbsp; Bảng đích: <span class='mono'>bi.doi_soat_giao_dich_A</span> "
          "&nbsp;·&nbsp; DE: Trần Văn Hùng &nbsp;·&nbsp; Đã duyệt v4.2")
J_ACT = ('<span class="btn w">▶ Chạy thử</span><span class="btn w">⧉ Nhân bản</span>'
         '<span class="btn">✎ Sửa</span>')

SQL_B4 = """<span style="color:#7C3AED">SELECT</span>
    n.ma_giao_dich,
    n.so_tien       <span style="color:#7C3AED">AS</span> so_tien_noi_bo,
    d.so_tien       <span style="color:#7C3AED">AS</span> so_tien_doi_tac,
    n.so_tien - d.so_tien <span style="color:#7C3AED">AS</span> chenh_lech,
    n.so_dien_thoai
<span style="color:#7C3AED">FROM</span>   ${buoc_3_giao_dich_noi_bo} n
<span style="color:#7C3AED">LEFT JOIN</span> ${buoc_2_doi_tac_chuan} d
       <span style="color:#7C3AED">ON</span> n.ma_giao_dich = d.ma_giao_dich
<span style="color:#7C3AED">WHERE</span>  n.ngay_giao_dich = '${ngay_du_lieu}'"""


def job_steps():
    nodes = (
        _node(10, 15, 170, 64, "Bước 1", "Đọc file đối tác A<br>→ tmp_doi_tac_tho", "#98A2B3") +
        _node(200, 15, 170, 64, "Bước 2", "Chuẩn hoá số điện thoại<br>→ tmp_doi_tac_chuan", "#98A2B3") +
        _node(10, 105, 170, 64, "Bước 3", "Đọc giao dịch nội bộ<br>→ tmp_giao_dich_noi_bo", "#98A2B3") +
        _node(390, 60, 170, 64, "Bước 4 ◀ đang xem", "Đối soát 2 nguồn<br>→ tmp_ket_qua", AC,
              "#EFF4FF", tcol=AC) +
        _node(580, 60, 170, 64, "Bước 5", "GHI BẢNG ĐÍCH<br>bi.doi_soat_giao_dich_A", "#12B76A",
              "#ECFDF3", badge=("ĐÍCH", "background:#12B76A;color:#fff"), tcol="#05603A"))
    edges = _svg(760, 200, [
        _pl([(180, 47), (200, 47)]),
        _pl([(370, 47), (382, 47), (382, 92), (390, 92)]),
        _pl([(180, 137), (376, 137), (376, 92), (390, 92)]),
        _pl([(560, 92), (580, 92)]),
    ])

    stp = "".join(
        f'<tr style="{"background:#EFF4FF" if on else ""}"><td style="text-align:center">{i}</td>'
        f'<td><b>{nm}</b></td><td class="muted">{par}</td>'
        f'<td class="mono" style="font-size:11.5px">{out}</td>'
        f'<td style="text-align:right">{rows}</td><td style="text-align:right">{sec}</td></tr>'
        for i, nm, par, out, rows, sec, on in [
            (1, "Đọc file đối tác A", "—", "tmp_doi_tac_tho", "412.808", "18 gy", False),
            (2, "Chuẩn hoá số điện thoại", "Bước 1", "tmp_doi_tac_chuan", "412.808", "26 gy", False),
            (3, "Đọc giao dịch nội bộ", "—", "tmp_giao_dich_noi_bo", "418.112", "31 gy", False),
            (4, "Đối soát 2 nguồn", "Bước 2, Bước 3", "tmp_ket_qua", "418.112", "47 gy", True),
            (5, "Ghi bảng đích", "Bước 4", "bi.doi_soat_giao_dich_A", "418.112", "12 gy", False),
        ])

    body = f"""
<div style="display:flex;gap:16px">
  <div style="flex:1.45">
    <div class="card" style="padding:16px 19px;margin-bottom:14px">
      <div class="sec">SƠ ĐỒ PHỤ THUỘC GIỮA CÁC BƯỚC</div>
      <div style="position:relative;height:190px;width:760px">{edges}{nodes}</div>
      <div class="muted" style="font-size:11.5px;margin-top:4px">
        Bước không có bước cha thì chạy song song. Bước 4 chờ cả Bước 2 và Bước 3 xong mới chạy.</div>
    </div>
    <div class="card" style="padding:16px 19px;margin-bottom:14px">
      <div class="sec">DANH SÁCH BƯỚC</div>
      <table class="g" style="font-size:12.5px">
        <tr><th style="text-align:center">#</th><th>Tên bước</th><th>Bước cha</th>
          <th>Bảng ra</th><th style="text-align:right">Số dòng</th>
          <th style="text-align:right">Thời gian</th></tr>{stp}</table>
    </div>
    <div class="card" style="padding:16px 19px">
      <div class="sec">CÂU SQL — BƯỚC 4</div>
      <pre style="background:#0F1729;color:#E5E9F0;border-radius:8px;padding:13px 15px;
        font-family:Consolas,monospace;font-size:12px;line-height:1.6;overflow:hidden">{SQL_B4}</pre>
    </div>
  </div>
  <div style="width:470px;flex-shrink:0">
    <div class="card" style="padding:15px 17px;margin-bottom:13px">
      <div class="sec">BẢNG ĐÍCH</div>
      {fld("Bảng đích", "🗂️ bi.doi_soat_giao_dich_A ▾", True,
           "⭐ <b>Bắt buộc chọn từ danh mục 1.1</b> — không cho gõ tay tên bảng. "
           "Đây là ràng buộc mới, và là thứ giữ cho hai module không lệch nhau")}
      <div class="note" style="background:#ECFDF3;border:1px solid #A6F4C5;font-size:12px">
        Chọn xong, hệ thống hiện ngay: bảng này <b>Tier 1</b> ·
        BDA <b>Nguyễn Thị Phương</b> · có <b>7 luật chất lượng</b> ·
        đang được <b>6 báo cáo</b> dùng.<br>
        → Người tạo job <b>biết mình đang động vào cái gì</b> trước khi bấm lưu.
      </div>
    </div>
    <div class="card" style="padding:15px 17px;margin-bottom:13px">
      <div class="sec">NGUỒN GỐC SINH RA TỪ JOB NÀY</div>
      <table class="g" style="font-size:12px">
        <tr><th>Bảng nguồn</th><th>Dò bằng cách nào</th></tr>
        <tr><td class="mono">raw.doi_soat_A_tho</td><td>{chip("Từ biến ${…}", "g")}</td></tr>
        <tr><td class="mono">dwh.giao_dich_ngay</td><td>{chip("Từ biến ${…}", "g")}</td></tr>
        <tr><td class="mono">ref.doi_tac</td><td>{chip("Viết thẳng tên — BỎ SÓT", "r")}</td></tr>
      </table>
      <div class="note" style="background:#FEF3F2;border:1px solid #FECDCA;margin-top:11px;
        font-size:12px">
        🔴 <b>Lỗi gốc của lineage hiện tại.</b> SQLWF dò bảng nguồn bằng cách
        <b>tìm chuỗi <span class="mono">${{…}}</span> trong câu SQL</b> — không phải phân tích cú pháp SQL thật.<br>
        Bảng nào viết thẳng tên trong câu <span class="mono">FROM</span> / <span class="mono">JOIN</span>
        đều <b>bị bỏ sót</b>.<br><br>
        <b>DMP thay bằng bộ phân tích cú pháp SQL</b> — đọc đúng mọi bảng trong
        <span class="mono">FROM</span>, <span class="mono">JOIN</span>,
        <span class="mono">WITH</span>, truy vấn con.
      </div>
    </div>
    <div class="card" style="padding:15px 17px">
      <div class="sec">QUÉT NGUỒN GỐC</div>
      {fld("Bật quét nguồn gốc cho job này", "☑ Bật &nbsp;<span class='muted'>(mặc định MỚI: bật)</span>",
           hint="SQLWF hiện mặc định <b>TẮT</b> (<span class='mono'>enableDataLineage = false</span>). "
                "Đây là lý do tab Nguồn gốc của phần lớn bảng đang trống")}
      <div class="note" style="background:#FFFAEB;border:1px solid #FEDF89;font-size:12px">
        ⚠️ <b>Việc phải làm khi chuyển sang DMP:</b> bật cờ này cho <b>toàn bộ job cũ</b> bằng một
        lệnh cập nhật hàng loạt, rồi chạy lại bộ quét một lượt.<br>
        Không làm bước này thì tab Nguồn gốc của 1.1 <b>vẫn trống như hiện nay</b>.
      </div>
    </div>
  </div>
</div>"""
    return shell("dmp.vds.vn/orchestration/jobs/JOB-0412", J_CRUMB, J_TITLE, J_DESC, body,
                 "DMP · Menu 4.1 — LUỒNG XỬ LÝ · Màn CHI TIẾT · Tab BƯỚC", "m41",
                 tabs=("Bước", J_TABS), actions=J_ACT)


# ============================================================ 4.1 tab Lần chạy
def job_runs():
    runs = [
        ("R-88214", "07/08 06:00", "06:02:14", "2 ph 14 gy", "ok", "—", "418.112", "7/7 đạt"),
        ("R-88102", "06/08 06:00", "06:02:31", "2 ph 31 gy", "ok", "—", "417.904", "6/7 đạt"),
        ("R-87990", "05/08 06:00", "06:09:47", "9 ph 47 gy", "warn", "Bước 4 chạy lại lần 2",
         "418.331", "5/7 đạt"),
        ("R-87877", "04/08 06:00", "—", "1 ph 02 gy", "err", "Bước 1 — file đối tác chưa về",
         "0", "không chạy"),
        ("R-87765", "03/08 06:00", "06:02:08", "2 ph 08 gy", "ok", "—", "416.220", "7/7 đạt"),
    ]
    tr = ""
    for rid, st, en, dur, res, err, nrow, dq in runs:
        rc = {"ok": ("Thành công", "g"), "warn": ("Có cảnh báo", "o"), "err": ("Thất bại", "r")}[res]
        dqc = "g" if dq.startswith("7/7") else ("r" if dq == "không chạy" else "o")
        tr += (f'<tr><td class="mono muted">{rid}</td><td>{st}</td><td>{en}</td><td>{dur}</td>'
               f'<td>{chip(*rc)}</td><td class="muted">{err}</td>'
               f'<td style="text-align:right">{nrow}</td><td>{chip(dq, dqc)}</td>'
               f'<td><span class="ico">📄</span></td></tr>')

    bars = "".join(
        f'<div style="display:flex;align-items:center;gap:9px;margin-bottom:6px">'
        f'<div style="width:170px;font-size:12px">{nm}</div>'
        f'<div style="flex:1;height:17px;background:#F2F4F7;border-radius:4px;position:relative">'
        f'<div style="position:absolute;left:{off}%;width:{w}%;height:17px;background:{c};'
        f'border-radius:4px"></div></div>'
        f'<div style="width:52px;text-align:right;font-size:11.5px" class="muted">{s}</div></div>'
        for nm, off, w, c, s in [
            ("Bước 1 — Đọc file", 0, 13, "#98A2B3", "18 gy"),
            ("Bước 3 — Đọc nội bộ", 0, 23, "#98A2B3", "31 gy"),
            ("Bước 2 — Chuẩn hoá", 13, 19, "#98A2B3", "26 gy"),
            ("Bước 4 — Đối soát", 32, 35, AC, "47 gy"),
            ("Bước 5 — Ghi đích", 67, 9, "#12B76A", "12 gy"),
            ("Chạy luật chất lượng 3.2", 76, 24, "#0EA5A5", "32 gy"),
        ])

    body = _kpi([
        ("SỐ LẦN CHẠY 30 NGÀY", "30", "27 thành công · 2 cảnh báo · 1 thất bại", "#101828"),
        ("TỈ LỆ THÀNH CÔNG", "90%", "cam kết nội bộ: ≥ 98%", "#B42318"),
        ("THỜI GIAN TRUNG BÌNH", "2 ph 41 gy", "chậm nhất 9 ph 47 gy ngày 05/08", "#101828"),
        ("XONG TRƯỚC GIỜ CAM KẾT", "29/30", "cam kết: xong trước 07:00", "#B54708"),
    ]) + f"""
<div style="display:flex;gap:16px">
  <div style="flex:1.5">
    <div class="card" style="margin-bottom:14px"><table class="g">
      <tr><th>Mã lần chạy</th><th>Bắt đầu</th><th>Kết thúc</th><th>Thời lượng</th>
        <th>Kết quả</th><th>Hỏng ở đâu</th><th style="text-align:right">Dòng ghi</th>
        <th>Chất lượng sau chạy</th><th></th></tr>{tr}</table></div>
    <div class="card" style="padding:16px 19px">
      <div class="sec">DÒNG THỜI GIAN CỦA LẦN CHẠY R-88214</div>
      {bars}
      <div class="muted" style="font-size:11.5px;margin-top:8px">
        Bước 1 và Bước 3 chạy <b>song song</b> vì không phụ thuộc nhau.
        Sau khi ghi bảng đích, hệ thống <b>tự chạy luật chất lượng</b> của bảng đó — đây là chỗ
        module ④ nối vào module ③.</div>
    </div>
    <div class="card" style="padding:16px 19px;margin-top:14px">
      <div class="sec">BẤM VÀO MỘT LẦN CHẠY HỎNG THÌ THẤY GÌ</div>
      <table class="g" style="font-size:12.5px">
        <tr><th style="width:230px">Thông tin</th><th>Vì sao cần</th></tr>
        <tr><td><b>Nhật ký của đúng bước hỏng</b></td>
            <td>Không phải cuộn cả nghìn dòng log của 5 bước để tìm chỗ hỏng</td></tr>
        <tr><td><b>Câu SQL đã chạy — sau khi thay biến</b></td>
            <td>Thấy đúng câu máy đã chạy, không phải câu có <span class="mono">${{…}}</span>.
              Phần lớn lỗi nằm ở <b>giá trị biến sai</b>, không phải câu SQL sai</td></tr>
        <tr><td><b>Số dòng vào / ra của từng bước</b></td>
            <td>Bước nào làm mất dòng thì thấy ngay</td></tr>
        <tr><td><b>Nút "Chạy lại từ bước hỏng"</b></td>
            <td>Không chạy lại từ đầu — tiết kiệm thời gian và không ghi đè phần đã đúng</td></tr>
      </table>
      <div class="muted" style="font-size:11.5px;margin-top:9px">
        SQLWF đã có <b>trình xem SQL</b> và <b>sơ đồ bước</b>. Phần thêm là
        <b>gắn nhật ký lần chạy vào đúng bước</b> và <b>thay biến trước khi hiện</b>.</div>
    </div>
  </div>
  <div style="width:460px;flex-shrink:0">
    <div class="card" style="padding:15px 17px;margin-bottom:13px">
      <div class="sec">LỊCH CHẠY</div>
      <table class="g" style="font-size:12.5px">
        <tr><td style="width:165px;color:#667085">Biểu thức lịch</td>
            <td class="mono">0 0 6 * * ?</td></tr>
        <tr><td style="color:#667085">Diễn giải</td><td>06:00 hằng ngày</td></tr>
        <tr><td style="color:#667085">Mã điều phối</td><td class="mono">COORD_DOISOAT_A</td></tr>
        <tr><td style="color:#667085">Chờ job nào xong trước</td>
            <td>JOB-0388 <span class="muted">(nạp file SFTP)</span></td></tr>
        <tr><td style="color:#667085">Giờ cam kết xong</td><td><b>07:00</b></td></tr>
        <tr><td style="color:#667085">Chế độ chạy thử</td><td>{chip("Tắt", "n")}</td></tr>
      </table>
      <div class="muted" style="font-size:11.5px;margin-top:8px">
        Toàn bộ mục này SQLWF đã có — <span class="mono">cronExpression</span> ·
        <span class="mono">coordinatorCode</span> · <span class="mono">updateTestMode</span>.</div>
    </div>
    <div class="card" style="padding:15px 17px;margin-bottom:13px">
      <div class="sec">GIỜ CAM KẾT — TRƯỜNG MỚI</div>
      <div class="note" style="background:#EFF4FF;border:1px solid #C7D7FE;font-size:12.5px">
        SQLWF hiện chỉ biết job <b>chạy xong hay chưa</b>, không biết
        <b>xong có kịp giờ không</b>.<br><br>
        Khai <b>giờ cam kết</b> ở đây thì hai chỗ dùng lại được ngay:<br>
        ① Luật <span class="mono">on_time</span> ở <b>3.2</b> có mốc để so<br>
        ② Thẻ <b>Độ tươi</b> ở tab Tổng quan của <b>1.1</b> biết thế nào là trễ
      </div>
    </div>
    <div class="card" style="padding:15px 17px">
      <div class="sec">GỬI CẢNH BÁO CHO AI</div>
      {fld("Người nhận khi job hỏng", "👤 DE phụ trách bảng đích &nbsp; 👥 Đội vận hành dữ liệu",
           hint="Khai theo <b>vai trò</b>, không gõ tên người — đổi người phụ trách ở 1.1 thì "
                "cảnh báo tự đi đúng chỗ")}
      {fld("Kênh gửi", "Email · Telegram", ro=True,
           hint="Dùng lại cấu hình kênh ở <b>menu 3.5</b> — không khai lại ở đây")}
      {fld("Hỏng mấy lần liên tiếp thì tạo sự cố", "2 lần",
           hint="Đủ số lần thì tự mở sự cố ở <b>menu 3.4</b>, có người xử lý và có hạn")}
    </div>
  </div>
</div>"""
    return shell("dmp.vds.vn/orchestration/jobs/JOB-0412/runs", J_CRUMB, J_TITLE, J_DESC, body,
                 "DMP · Menu 4.1 — LUỒNG XỬ LÝ · Màn CHI TIẾT · Tab LẦN CHẠY + LỊCH", "m41",
                 tabs=("Lần chạy", J_TABS), actions=J_ACT)


# ============================================================ 4.2 danh sách mẫu nạp
def ing_list():
    rows = [
        ("NAP-012", "File đối soát đối tác A", "Tải file lên", "SFTP · /doi_soat/A/",
         "raw.doi_soat_A_tho", "CSV · UTF-8 · dấu ;", "05:30 hằng ngày", "3 luật", "import-data"),
        ("NAP-034", "Đồng bộ khách hàng từ CRM", "Đồng bộ CSDL", "MariaDB · crm_prod",
         "raw.khach_hang", "—", "mỗi 30 phút", "2 luật", "sync-management"),
        ("NAP-057", "Hoá đơn điện tử", "Nạp hoá đơn", "Người dùng tải lên",
         "raw.hoa_don", "XML · UTF-8", "thủ công", "chưa có", "invoice-uploader"),
        ("NAP-088", "Di trú dữ liệu cũ 2019-2022", "Di trú một lần", "OracleDB · legacy",
         "dwh.lich_su_giao_dich", "—", "một lần", "chưa có", "data-migration-management"),
        ("NAP-101", "Đồng bộ thư mục HDFS đối tác B", "Đồng bộ tệp", "HDFS · /partner/B/",
         "raw.doi_soat_B_tho", "Parquet", "mỗi giờ", "1 luật", "fsync"),
        ("NAP-140", "Bàn giao số liệu cho Ban Tài chính", "Bàn giao ra ngoài",
         "bi.doanh_thu_thang", "SFTP · Ban TC", "CSV · UTF-8", "08:00 hằng ngày", "2 luật",
         "clean-delivery"),
    ]
    tr = ""
    for code, nm, kind, src, dst, fmt, sched, gate, old in rows:
        gc = "n" if gate == "chưa có" else "g"
        tr += (f'<tr><td class="mono muted">{code}</td>'
               f'<td><b style="color:{AC}">{nm}</b></td><td>{chip(kind, "t")}</td>'
               f'<td class="mono" style="font-size:11.5px">{src}</td>'
               f'<td class="mono" style="font-size:11.5px">{dst}</td>'
               f'<td class="muted">{fmt}</td><td class="muted">{sched}</td>'
               f'<td>{chip(gate, gc)}</td>'
               f'<td class="mono muted" style="font-size:11px">{old}</td>'
               f'<td style="white-space:nowrap"><span class="ico">👁</span>'
               f'<span class="ico">✎</span></td></tr>')

    body = _kpi([
        ("TỔNG SỐ MẪU NẠP", "168", "gộp từ 6 màn rời rạc của SQLWF", "#101828"),
        ("LẦN NẠP HÔM NAY", "412", "398 thành công · 14 lỗi định dạng", "#101828"),
        ("CÓ CỔNG CHẤT LƯỢNG", "0 / 168", "chưa mẫu nào chặn được dữ liệu xấu", "#B42318"),
        ("DỮ LIỆU XẤU ĐÃ LỌT VÀO 30 NGÀY", "9 lần", "phát hiện sau khi đã ghi — phải xoá và nạp lại",
         "#B42318"),
        ("BẢNG ĐÍCH CHƯA KHAI Ở 1.1", "31", "nạp vào bảng không ai quản", "#B54708"),
    ]) + f"""
<div style="display:flex;gap:10px;margin-bottom:13px;align-items:center">
  <div style="flex:1;border:1px solid #d0d7e2;border-radius:8px;padding:9px 13px;font-size:13px;
    background:#fff">🔍 <span class="muted">Tìm theo tên mẫu, nguồn, bảng đích…</span></div>
  <span class="btn w">Loại cửa nạp: tất cả ▾</span><span class="btn w">Bảng đích ▾</span>
  <span class="btn w">Chưa có cổng chất lượng ☐</span>
</div>
<div class="card"><table class="g">
  <tr><th>Mã mẫu</th><th>Tên mẫu nạp</th><th>Loại cửa nạp</th><th>Nguồn</th><th>Bảng đích</th>
    <th>Định dạng</th><th>Lịch</th><th>Cổng chất lượng</th><th>Màn SQLWF cũ</th><th></th></tr>
  {tr}</table></div>
<div style="display:flex;gap:14px;margin-top:14px">
  <div class="card" style="flex:1;padding:15px 18px">
    <div class="sec">SÁU MÀN CŨ GỘP VỀ MỘT MENU</div>
    <table class="g" style="font-size:12.5px">
      <tr><th>Màn SQLWF hiện tại</th><th>Việc nó làm</th><th>Về đâu trong DMP</th></tr>
      <tr><td class="mono">import-data</td><td>Tải file lên, <b>đã có quản lý mẫu đầy đủ</b></td>
          <td>Loại <b>Tải file lên</b></td></tr>
      <tr><td class="mono">sync-management</td><td>Đồng bộ MariaDB · MongoDB · OracleDB, có duyệt</td>
          <td>Loại <b>Đồng bộ CSDL</b></td></tr>
      <tr><td class="mono">invoice-uploader</td><td>Nạp hoá đơn, có kết quả xử lý của đội AI</td>
          <td>Loại <b>Nạp hoá đơn</b></td></tr>
      <tr><td class="mono">data-migration-management</td><td>Chuyển dữ liệu hệ thống cũ</td>
          <td>Loại <b>Di trú một lần</b></td></tr>
      <tr><td class="mono">fsync</td><td>Đồng bộ thư mục tệp</td>
          <td>Loại <b>Đồng bộ tệp</b></td></tr>
      <tr><td class="mono">clean-delivery</td><td>Bàn giao số liệu ra ngoài</td>
          <td>Loại <b>Bàn giao ra ngoài</b></td></tr>
    </table>
    <div class="note" style="background:#EFF4FF;border:1px solid #C7D7FE;margin-top:11px">
      💡 <b>Gộp không có nghĩa là viết lại.</b> Phần chạy của 6 màn giữ nguyên — chỉ thống nhất
      <b>một khuôn khai báo</b>, <b>một chỗ xem lịch sử nạp</b>, và <b>một cổng chất lượng dùng chung</b>.
    </div>
  </div>
  <div style="width:500px;flex-shrink:0">
    <div class="note" style="background:#ECFDF3;border:1px solid #A6F4C5;margin-bottom:13px">
      ✅ <b>SQLWF đã có sẵn hai thứ quý:</b><br>
      ① <span class="mono">import-data/template</span> — quản lý mẫu nạp đầy đủ: tạo · sửa · bật/tắt ·
      tải file mẫu · gắn vào menu chức năng.<br>
      ② <span class="mono">sync-management</span> <b>đã dùng lại <span class="mono">dqService</span></b> —
      tức là cấu hình đồng bộ <b>đã kèm cấu hình chất lượng</b>. Đây chính là mầm của cổng chất lượng,
      chỉ chưa có phần <b>chặn</b>.
    </div>
    <div class="note" style="background:#FEF3F2;border:1px solid #FECDCA">
      🔴 <b>Cột "Cổng chất lượng" đang 0/168 là con số đáng lo nhất màn này.</b><br><br>
      Hiện dữ liệu xấu <b>vẫn được ghi vào bảng</b>, luật chất lượng chạy <b>sau đó</b> mới phát hiện.
      Lúc ấy báo cáo đã đọc phải số sai, và phải xoá dữ liệu rồi nạp lại — 9 lần trong 30 ngày.<br><br>
      <b>Chặn tại cửa rẻ hơn dọn dẹp phía sau.</b>
    </div>
  </div>
</div>"""
    return shell("dmp.vds.vn/ingestion/templates", "Ingestion &amp; Orchestration › Cửa nạp dữ liệu",
                 "📥 Cửa nạp dữ liệu",
                 "Mọi đường dữ liệu đi vào hệ thống — một khuôn khai báo, một cổng kiểm tra",
                 body, "DMP · Menu 4.2 — CỬA NẠP DỮ LIỆU · Màn DANH SÁCH MẪU NẠP", "m42",
                 tabs=("Mẫu nạp", ["Mẫu nạp", "Lịch sử nạp", "Cổng chất lượng", "Vùng chờ"]),
                 actions='<span class="btn w">⬇️ Tải file mẫu</span>'
                         '<span class="btn">➕ Tạo mẫu nạp</span>')


# ============================================================ 4.2 tạo mẫu nạp + cổng chất lượng
def ing_create():
    gate = "".join(
        f'<tr><td>{a}</td><td class="mono" style="font-size:11.5px">{b}</td>'
        f'<td>{chip(c, d)}</td><td class="muted">{e}</td>'
        f'<td style="color:#B42318">✕</td></tr>'
        for a, b, c, d, e in [
            ("Số dòng trong khoảng", "row_count_range · 300.000 – 500.000",
             "🛑 Chặn cả lô", "r", "File thiếu dòng = đối tác gửi thiếu"),
            ("Cột khoá không rỗng", "not_null · ma_giao_dich",
             "🛑 Chặn cả lô", "r", "Thiếu khoá thì không đối soát được"),
            ("Đúng định dạng số điện thoại", "format_regex · so_dien_thoai",
             "⚠️ Tách dòng lỗi", "o", "Dòng sai để riêng, dòng đúng vẫn nạp"),
            ("Mã đối tác có trong danh mục", "referential_integrity · ref.doi_tac",
             "⚠️ Tách dòng lỗi", "o", "Đối chiếu danh mục ở menu 1.4"),
            ("Ngày dữ liệu không phải tương lai", "value_range · ngay_giao_dich",
             "🔔 Chỉ cảnh báo", "b", "Vẫn nạp, nhưng gửi cảnh báo"),
        ])

    body = _steps([("Nguồn", "done"), ("Bảng đích", "done"), ("Ánh xạ trường", "done"),
                   ("Cổng chất lượng", "now"), ("Lịch & cảnh báo", "next")]) + f"""
<div style="display:flex;gap:18px">
  <div style="width:470px;flex-shrink:0">
    <div class="card" style="padding:17px 19px;margin-bottom:13px">
      <div class="sec">① NGUỒN</div>
      {fld("Loại cửa nạp", "📄 Tải file lên ▾", True,
           "6 loại: Tải file lên · Đồng bộ CSDL · Nạp hoá đơn · Di trú một lần · "
           "Đồng bộ tệp · Bàn giao ra ngoài. <b>Chọn loại nào thì hiện đúng nhóm trường của loại đó</b>")}
      {fld("Kết nối nguồn", "🔌 SFTP_DOITAC_A ▾", True,
           "Lấy từ <b>menu 6.2 — Cấu hình hệ thống</b>. Không khai lại máy chủ / tài khoản ở đây")}
      {fld("Đường dẫn / thư mục", "/doi_soat/A/", True, mono=True)}
      {fld("Mẫu tên tệp", "DOISOAT_A_yyyyMMdd.csv", True,
           "Hệ thống dùng mẫu này để <b>biết tệp nào thuộc ngày nào</b>", mono=True)}
      {fld("Định dạng · Bảng mã · Dấu phân cách", "CSV &nbsp;·&nbsp; UTF-8 &nbsp;·&nbsp; ;", True,
           "SQLWF đã có đủ 3 trường này ở <span class='mono'>import-data/template</span>")}
    </div>
    <div class="card" style="padding:17px 19px">
      <div class="sec">② BẢNG ĐÍCH</div>
      {fld("Bảng đích", "🗂️ raw.doi_soat_A_tho ▾", True,
           "⭐ <b>Bắt buộc chọn từ danh mục 1.1</b>. Bảng chưa khai thì bấm "
           "<i>Khai bảng mới</i> ngay tại đây — không cho gõ tay tên bảng")}
      {fld("Cách ghi", "Ghi thêm theo phân vùng ngày ▾", True,
           "Ghi thêm · Ghi đè cả bảng · Ghi đè phân vùng")}
      {fld("Cột phân vùng", "ngay_du_lieu", True, mono=True)}
      {fld("Khoảng dữ liệu", "Ngày ▾", hint="Ngày · Tháng · Quý — dùng cho báo cáo theo kỳ")}
    </div>
  </div>
  <div style="flex:1">
    <div class="card" style="padding:17px 19px;margin-bottom:13px;background:#FFFAEB;
      border-color:#FEDF89">
      <div class="sec" style="color:#B54708;border-color:#B54708">
        ④ CỔNG CHẤT LƯỢNG — PHẦN MỚI HOÀN TOÀN</div>
      <div style="font-size:12.5px;line-height:1.7;margin-bottom:11px;color:#344054">
        Luật chạy <b>trên dữ liệu trong vùng chờ, trước khi ghi vào bảng đích</b>.
        Khác với luật ở <b>menu 3.2</b> — luật 3.2 chạy <b>sau khi đã ghi</b>.
      </div>
      <table class="g" style="font-size:12.5px;background:#fff">
        <tr><th>Luật kiểm tại cửa</th><th>Cấu hình</th><th>Không đạt thì</th><th>Vì sao đặt luật này</th><th></th></tr>
        {gate}
        <tr><td colspan="5" style="color:#8b95a7">+ Thêm luật &nbsp;·&nbsp;
          <span style="color:#2563EB">Chọn từ thư viện luật 3.1</span></td></tr>
      </table>
      <div style="margin-top:11px;font-size:12.5px">
        <b>Ba mức xử lý — chọn theo mức độ nghiêm trọng:</b>
      </div>
      <table class="g" style="font-size:12.5px;background:#fff;margin-top:7px">
        <tr><th>Mức</th><th>Hệ thống làm gì</th><th>Dùng khi</th></tr>
        <tr><td>{chip("🛑 Chặn cả lô", "r")}</td>
            <td>Không ghi dòng nào. Cả lô nằm ở <b>vùng chờ</b>, gửi cảnh báo, mở sự cố ở 3.4</td>
            <td>Lỗi cho thấy <b>cả tệp sai</b> — thiếu dòng, sai cấu trúc, mất cột khoá</td></tr>
        <tr><td>{chip("⚠️ Tách dòng lỗi", "o")}</td>
            <td>Dòng đúng ghi vào bảng đích, dòng sai để riêng ở <b>vùng chờ</b> chờ xử lý</td>
            <td>Lỗi <b>rải rác vài dòng</b> — sai định dạng, mã lạ</td></tr>
        <tr><td>{chip("🔔 Chỉ cảnh báo", "b")}</td>
            <td>Ghi hết, gửi cảnh báo cho người phụ trách</td>
            <td>Nghi ngờ nhưng <b>chưa chắc sai</b> — số liệu bất thường</td></tr>
      </table>
    </div>
    <div style="display:flex;gap:13px">
      <div class="note" style="flex:1;background:#EFF4FF;border:1px solid #C7D7FE">
        🔗 <b>Khai ở đây, dùng ở đâu</b><br><br>
        <b>Bảng đích</b> → tab Nguồn gốc của <b>1.1</b> hiện cửa nạp này là nút gốc<br>
        <b>Luật cổng</b> → dùng lại <b>loại kiểm tra</b> khai ở <b>3.1</b>, không khai kiểu luật mới<br>
        <b>Lô bị chặn</b> → tự mở sự cố ở <b>3.4</b>, gán cho DE phụ trách bảng đích<br>
        <b>Lịch sử nạp</b> → thẻ <b>Độ tươi</b> ở tab Tổng quan của <b>1.1</b>
      </div>
      <div class="note" style="width:340px;background:#FEF3F2;border:1px solid #FECDCA">
        🔴 <b>Vì sao không dùng luôn luật 3.2 cho việc này</b><br><br>
        Luật 3.2 chạy <b>trên bảng đã ghi</b> — lúc phát hiện thì báo cáo đã đọc phải số sai.<br><br>
        Cổng chất lượng chạy <b>trên vùng chờ</b>, chưa ai đọc được. Chặn ở đây thì
        <b>không ai phải xoá dữ liệu và nạp lại</b>.
      </div>
    </div>
    <div style="display:flex;gap:10px;margin-top:15px">
      <span class="btn">Tiếp tục — Lịch &amp; cảnh báo</span>
      <span class="btn w">▶ Chạy thử trên tệp mẫu</span>
      <span class="btn w">Lưu nháp</span></div>
  </div>
</div>"""
    return shell("dmp.vds.vn/ingestion/templates/create",
                 "Ingestion &amp; Orchestration › Cửa nạp dữ liệu › Tạo mẫu nạp",
                 "➕ Tạo mẫu nạp dữ liệu",
                 "Khai một đường dữ liệu vào hệ thống — kèm luật chặn dữ liệu xấu ngay tại cửa",
                 body, "DMP · Menu 4.2 — CỬA NẠP DỮ LIỆU · Màn TẠO MẪU (bước 4 — Cổng chất lượng)",
                 "m42")


# ============================================================ 4.3 theo dõi + sơ đồ pipeline
def pipe_monitor():
    OKB = ("#12B76A", "#ECFDF3", "#05603A")
    ERB = ("#F04438", "#FEF3F2", "#912018")
    WNB = ("#F79009", "#FFFAEB", "#93370D")
    NEU = ("#98A2B3", "#fff", "#101828")

    def nd(x, y, t, s, c, badge=None):
        return _node(x, y, 152, 64, t, s, c[0], c[1], badge=badge or "", tcol=c[2])

    nodes = (
        nd(14, 26, "📥 NAP-012", "SFTP đối tác A<br>05:30 · 412.808 dòng", NEU,
           ("✓ 05:31", "background:#ECFDF3;color:#05603A;border:1px solid #A6F4C5")) +
        nd(196, 26, "🗂️ raw.doi_soat_A_tho", "vùng thô", OKB,
           ("94", "background:#12B76A;color:#fff")) +
        nd(378, 26, "⚙️ JOB-0412", "Đối soát giao dịch<br>06:00 · 5 bước", NEU,
           ("✓ 06:02", "background:#ECFDF3;color:#05603A;border:1px solid #A6F4C5")) +
        nd(560, 26, "🗂️ bi.doi_soat_giao_dich_A", "Tier 1 · vùng nghiệp vụ", ERB,
           ("72", "background:#F04438;color:#fff")) +
        nd(742, 26, "⚙️ JOB-0119", "Tổng hợp doanh thu<br>07:00 · 8 bước", NEU,
           ("✓ 07:11", "background:#ECFDF3;color:#05603A;border:1px solid #A6F4C5")) +
        nd(924, 26, "🗂️ bi.doanh_thu_thang", "Tier 1 · vùng nghiệp vụ", WNB,
           ("?", "background:#F79009;color:#fff")) +
        nd(1106, 26, "📊 Dashboard doanh thu", "37 người xem / tuần", WNB,
           ("?", "background:#F79009;color:#fff")) +
        nd(14, 150, "📥 NAP-034", "MariaDB · crm_prod<br>mỗi 30 phút", NEU,
           ("✓ 09:30", "background:#ECFDF3;color:#05603A;border:1px solid #A6F4C5")) +
        nd(196, 150, "🗂️ raw.khach_hang", "vùng thô", OKB,
           ("91", "background:#12B76A;color:#fff")))

    edges = _svg(1270, 240, [
        _pl([(166, 58), (196, 58)]),
        _pl([(348, 58), (378, 58)]),
        _pl([(530, 58), (560, 58)]),
        _pl([(712, 58), (742, 58)], "#F04438", "ahr", "5,3"),
        _pl([(894, 58), (924, 58)], "#F79009", "ahr", "5,3"),
        _pl([(1076, 58), (1106, 58)], "#F79009", "ahr", "5,3"),
        _pl([(166, 182), (196, 182)]),
        _pl([(348, 182), (363, 182), (363, 58), (378, 58)]),
    ])

    tasks = "".join(
        f'<tr><td class="mono muted">{a}</td><td><b>{b}</b></td>'
        f'<td class="mono muted" style="white-space:nowrap;font-size:11.5px">{c}</td>'
        f'<td style="white-space:nowrap">{d}</td><td>{chip(e, f)}</td><td class="muted">{g}</td></tr>'
        for a, b, c, d, e, f, g in [
            ("TSK-1120", "JOB-0412 — Đối soát đối tác A", "0 0 6 * * ?", "Hôm nay 06:02",
             "Thành công", "g", "418.112 dòng · 2 ph 14 gy"),
            ("TSK-1121", "Luật chất lượng bi.doi_soat_giao_dich_A", "sau JOB-0412", "Hôm nay 06:05",
             "5/7 đạt", "r", "2 luật hỏng → đã mở sự cố SC-0231"),
            ("TSK-1088", "JOB-0119 — Tổng hợp doanh thu", "0 0 7 * * ?", "Hôm nay 07:11",
             "Thành công", "g", "nhưng đọc từ bảng đang có sự cố"),
            ("TSK-0904", "NAP-034 — Đồng bộ CRM", "0 */30 * * * ?", "Hôm nay 09:30",
             "Thành công", "g", "12.044 dòng"),
            ("TSK-1533", "JOB-0501 — KPI kinh doanh tháng", "0 0 3 1 * ?", "01/08 03:24",
             "Thất bại", "r", "hỏng bước 7 — hết bộ nhớ"),
        ])

    body = _kpi([
        ("TÁC VỤ ĐANG CHẠY", "23", "trên tổng 1.842 tác vụ đã khai", "#101828"),
        ("HỎNG TRONG 24 GIỜ", "17", "5 tác vụ hỏng 3 ngày liên tiếp", "#B42318"),
        ("TRỄ GIỜ CAM KẾT", "4", "xong sau mốc đã cam kết ở 4.1", "#B54708"),
        ("BẢNG BỊ ẢNH HƯỞNG DÂY CHUYỀN", "9", "hạ nguồn của bảng đang có sự cố", "#B54708"),
        ("ĐỘ PHỦ SƠ ĐỒ", "?", "phụ thuộc số job bật quét nguồn gốc (H5)", "#B54708"),
    ]) + f"""
<div class="card" style="padding:16px 19px;margin-bottom:14px">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:11px">
    <div class="sec" style="margin:0">SƠ ĐỒ PIPELINE — CỬA NẠP → BẢNG → JOB → BÁO CÁO</div>
    <div style="display:flex;gap:8px"><span class="btn w">Lọc theo miền ▾</span>
      <span class="btn w">Chỉ nhánh đang có sự cố ☑</span></div>
  </div>
  <div style="position:relative;height:225px;width:1270px">{edges}{nodes}</div>
  <div style="display:flex;gap:18px;font-size:11.5px;color:#344054;margin-top:2px">
    <span><b style="color:#12B76A">●</b> Điểm chất lượng ≥ 90 — đạt</span>
    <span><b style="color:#F04438">●</b> Có luật hỏng — nguồn gây sự cố</span>
    <span><b style="color:#F79009">●</b> Chưa chắc sai, nhưng <b>ăn dữ liệu từ nút đỏ</b></span>
    <span style="color:#667085">Đường nét đứt = nhánh đang lan lỗi xuống hạ nguồn</span>
  </div>
</div>
<div style="display:flex;gap:16px">
  <div style="flex:1.5">
    <div class="card" style="margin-bottom:14px"><table class="g">
      <tr><th>Mã tác vụ</th><th>Tác vụ</th><th>Lịch</th><th>Lần chạy gần nhất</th>
        <th>Kết quả</th><th>Ghi chú</th></tr>{tasks}</table></div>
    <div class="card" style="padding:16px 19px">
      <div class="sec">CHẠY XONG ≠ SỐ ĐÚNG — BỐN TỔ HỢP PHẢI ĐỌC ĐƯỢC TRÊN MỘT MÀN</div>
      <table class="g" style="font-size:12.5px">
        <tr><th>Job chạy</th><th>Luật chất lượng</th><th>Thực tế đang xảy ra</th><th>Ai xử lý</th></tr>
        <tr><td>{chip("Thành công", "g")}</td><td>{chip("Đạt", "g")}</td>
            <td>Bình thường</td><td class="muted">—</td></tr>
        <tr><td>{chip("Thành công", "g")}</td><td>{chip("Hỏng", "r")}</td>
            <td><b>Job chạy trơn tru nhưng số sai.</b> Đây là ca hay gặp nhất và
              hiện <b>không màn nào của SQLWF hiện ra được</b></td><td>BDA phụ trách bảng</td></tr>
        <tr><td>{chip("Thất bại", "r")}</td><td>{chip("Chưa chạy", "n")}</td>
            <td>Bảng chưa được cập nhật — báo cáo đang đọc số của hôm qua</td>
            <td>DE phụ trách job</td></tr>
        <tr style="background:#FEF3F2"><td>{chip("Thất bại", "r")}</td><td>{chip("Đạt", "g")}</td>
            <td>🔴 <b>Nguy hiểm nhất.</b> Luật báo "đạt" vì đang kiểm <b>dữ liệu cũ còn nguyên
              trong bảng</b> — không ai biết dữ liệu hôm nay chưa về</td>
            <td>DE <b>và</b> BDA</td></tr>
      </table>
      <div class="muted" style="font-size:11.5px;margin-top:9px">
        Dòng cuối là lý do luật <span class="mono">freshness</span> và
        <span class="mono">on_time</span> ở menu 3.1 <b>bắt buộc phải có</b> cho mọi bảng Tier 1 —
        không có chúng thì bảng đứng im vẫn được chấm điểm cao.</div>
    </div>
  </div>
  <div style="width:520px;flex-shrink:0">
    <div class="note" style="background:#FEF3F2;border:1px solid #FECDCA;margin-bottom:13px">
      🔴 <b>Đây là màn trả lời câu hỏi mà hiện không ai trả lời được:</b>
      <i>"Bảng này hỏng thì báo cáo nào đang đọc phải số sai?"</i><br><br>
      Nút đỏ <span class="mono">bi.doi_soat_giao_dich_A</span> có 2 luật hỏng.
      Sơ đồ chỉ ngay: <b>JOB-0119 đã chạy xong lúc 07:11</b> và đã đổ số vào
      <span class="mono">bi.doanh_thu_thang</span> → <b>Dashboard doanh thu</b> mà
      <b>37 người xem mỗi tuần</b> đang hiển thị số nghi ngờ.<br><br>
      Job chạy <b>thành công</b> vẫn có thể sinh ra <b>số sai</b> — đó là lý do
      trạng thái chạy và trạng thái chất lượng phải nằm <b>trên cùng một sơ đồ</b>.
    </div>
    <div class="card" style="padding:15px 17px;margin-bottom:13px">
      <div class="sec">CHẶN LAN LỖI — TUỲ CHỌN</div>
      <table class="g" style="font-size:12.5px">
        <tr><td style="width:210px">Bảng nguồn có luật hỏng mức chặn</td>
            <td>{chip("Dừng job hạ nguồn", "r")}</td></tr>
        <tr><td>Bảng nguồn có luật hỏng mức cảnh báo</td>
            <td>{chip("Vẫn chạy, gắn cờ nghi ngờ", "o")}</td></tr>
        <tr><td>Bảng nguồn chưa có luật nào</td>
            <td>{chip("Vẫn chạy bình thường", "n")}</td></tr>
      </table>
      <div class="note" style="background:#FFFAEB;border:1px solid #FEDF89;margin-top:10px;
        font-size:12px">
        ⚠️ <b>Bật thận trọng.</b> Dừng job hạ nguồn là hành động mạnh — chỉ nên bật cho
        nhánh <b>Tier 1</b> và chỉ với luật đã chạy ổn định ít nhất một tháng.<br>
        Bật sớm khi luật còn hay báo động giả sẽ làm <b>dừng nhầm cả dây chuyền</b>.
      </div>
    </div>
    <div class="note" style="background:#ECFDF3;border:1px solid #A6F4C5">
      ✅ <b>Nửa dưới màn này SQLWF đã có.</b> <span class="mono">task-management</span> có
      <span class="mono">taskCode</span> · <span class="mono">cronExpression</span> ·
      <span class="mono">cyclePattern</span> và <b>kết quả lần chạy gần nhất</b>.<br>
      ❌ Thiếu <b>sơ đồ</b>, và thiếu việc <b>nối kết quả chạy với kết quả chất lượng</b>.<br>
      💡 Thiết kế sơ đồ lấy từ <b>bản DQ Tool demo của đội</b> — đúng chủ trương đã ghi trong repo:
      <i>hiển thị pipeline chỉ-đọc kèm chỉ số chất lượng, còn tạo job vẫn ở SQLWF</i>.
    </div>
  </div>
</div>"""
    return shell("dmp.vds.vn/orchestration/monitor",
                 "Ingestion &amp; Orchestration › Theo dõi &amp; Giám sát pipeline",
                 "🖥️ Theo dõi &amp; Giám sát pipeline",
                 "Cái gì đang chạy, hỏng ở đâu — và hỏng đó lan tới báo cáo nào",
                 body, "DMP · Menu 4.3 — THEO DÕI &amp; PIPELINE · Màn GIÁM SÁT", "m43",
                 tabs=("Sơ đồ pipeline", ["Sơ đồ pipeline", "Danh sách tác vụ", "Đang hỏng",
                                          "Trễ giờ cam kết"]),
                 actions='<span class="btn w">⬇️ Xuất sơ đồ</span>'
                         '<span class="btn w">🔄 Làm mới</span>')


SCREENS = {
    "dmp-31-job-list": job_list,
    "dmp-33-job-steps": job_steps,
    "dmp-34-job-runs": job_runs,
    "dmp-36-ingest-list": ing_list,
    "dmp-37-ingest-create": ing_create,
    "dmp-39-pipeline-monitor": pipe_monitor,
}
