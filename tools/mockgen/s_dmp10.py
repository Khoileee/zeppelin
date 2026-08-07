# -*- coding: utf-8 -*-
"""DMP — Module ⑥ Operations: 6.1 Sức khoẻ dữ liệu, 6.2 Cấu hình hệ thống."""
from dmp import shell, fld, chip, AC

H_TABS = ["Tổng quan", "Độ phủ quản trị", "Xu hướng", "Theo miền"]
H_CRUMB = "Operations › Sức khoẻ dữ liệu"
H_TITLE = "❤️ Sức khoẻ dữ liệu"
H_DESC = "Một màn cho lãnh đạo — dữ liệu công ty đang khoẻ hay yếu, quản trị dữ liệu tiến tới đâu"
H_ACT = ('<span class="btn w">Kỳ: Tháng 8/2026 ▾</span><span class="btn w">⬇️ Xuất báo cáo</span>')


def _bar(label, pct, target, color, note):
    return (f'<div style="margin-bottom:11px">'
            f'<div style="display:flex;justify-content:space-between;font-size:12.5px;'
            f'margin-bottom:4px"><span><b>{label}</b></span>'
            f'<span style="font-weight:700;color:{color}">{pct}%</span></div>'
            f'<div style="height:15px;background:#F2F4F7;border-radius:4px;position:relative">'
            f'<div style="width:{pct}%;height:15px;background:{color};border-radius:4px"></div>'
            f'<div style="position:absolute;left:{target}%;top:-3px;width:2px;height:21px;'
            f'background:#101828"></div></div>'
            f'<div style="font-size:11px;color:#8b95a7;margin-top:3px">{note} '
            f'<span style="color:#101828">▏mục tiêu {target}%</span></div></div>')


# ============================================================ 6.1 bảng điều khiển
def health_board():
    bars = (
        _bar("Có người phụ trách (BDA + DE)", 34, 90, "#F04438",
             "3.904 / 11.482 bảng — 7.578 bảng không ai nhận") +
        _bar("Có mô tả nghiệp vụ đủ nghĩa", 28, 80, "#F04438",
             "3.215 bảng — chưa tính các mô tả kiểu 'bảng tạm'") +
        _bar("Đã gán mức quan trọng (Tier)", 0, 100, "#F04438",
             "trường Tier là mới — chưa bảng nào được gán") +
        _bar("Có ít nhất 1 luật chất lượng", 1, 60, "#F04438",
             "64 / 11.482 bảng — chỉ 0,6%") +
        _bar("Có sơ đồ nguồn gốc", 0, 70, "#F04438",
             "phụ thuộc số job bật quét nguồn gốc — chưa có số liệu (H5)") +
        _bar("Cột nhạy cảm đã gắn nhãn", 78, 95, "#F79009",
             "412 cột đã gắn — bộ dò gợi ý còn 23 cột nghi ngờ chưa xác nhận") +
        _bar("Cột nhạy cảm đã có chính sách che", 0, 100, "#F04438",
             "0 / 412 — tính năng che dữ liệu chưa tồn tại"))

    worst = "".join(
        f'<tr><td class="mono" style="color:{AC};font-size:11.5px">{a}</td>'
        f'<td style="white-space:nowrap">{chip(b, "o" if b == "Tier 1" else "b")}</td>'
        f'<td style="text-align:center;color:#B42318;font-weight:700">{c}</td>'
        f'<td class="muted" style="font-size:11.5px">{d}</td><td>{e}</td></tr>'
        for a, b, c, d, e in [
            ("mart.kpi_kinh_doanh_v2", "Tier 1", "0/5", "không người phụ trách · không mô tả · "
             "không luật · không nguồn gốc · không Tier", "6 báo cáo đang dùng"),
            ("dwh.lich_su_giao_dich", "Tier 1", "1/5", "chỉ có mô tả", "3 báo cáo"),
            ("ops.log_truy_cap", "Tier 3", "1/5", "chỉ có người phụ trách", "1 báo cáo"),
            ("raw.doi_soat_B_tho", "Tier 2", "2/5", "có người phụ trách · có mô tả", "2 job hạ nguồn"),
        ])

    body = f"""
<div style="display:flex;gap:12px;margin-bottom:16px">
  <div class="card" style="flex:1.3;padding:16px 19px;background:#0F1729;border:none">
    <div style="font-size:11px;color:#8FA3C8;font-weight:700;letter-spacing:.4px">
      ĐIỂM CHẤT LƯỢNG DỮ LIỆU TOÀN HỆ THỐNG</div>
    <div style="display:flex;align-items:baseline;gap:12px;margin-top:4px">
      <div style="font-size:44px;font-weight:800;color:#12B76A;line-height:1">87</div>
      <div style="font-size:13px;color:#C3CEE2">/ 100 &nbsp;·&nbsp; ▲ 3 điểm so với tháng trước</div>
    </div>
    <div style="margin-top:11px;padding:9px 12px;background:#3D1D1D;border-radius:7px;
      border:1px solid #7A2E2E;font-size:12px;color:#FDA29B;line-height:1.6">
      ⚠️ <b>Điểm này chỉ tính trên 64 / 11.482 bảng đang được kiểm — 0,6%.</b><br>
      Đọc con số 87 mà không đọc con số 0,6% là <b>hiểu sai tình hình</b>.
    </div>
  </div>
  <div style="flex:2.4;display:flex;flex-direction:column;gap:12px">
    <div style="display:flex;gap:12px;flex:1">
      <div class="card kpi" style="flex:1"><div class="lb">BẢNG ĐANG ĐƯỢC KIỂM</div>
        <div class="vl" style="color:#B42318">0,6%</div>
        <div class="sb">64 / 11.482 bảng — mẫu quá nhỏ để kết luận</div></div>
      <div class="card kpi" style="flex:1"><div class="lb">BẢNG CHƯA GÁN MIỀN</div>
        <div class="vl" style="color:#B42318">4.334</div>
        <div class="sb">38% — không ai chịu trách nhiệm</div></div>
      <div class="card kpi" style="flex:1"><div class="lb">SỰ CỐ ĐANG MỞ</div>
        <div class="vl" style="color:#B54708">14</div>
        <div class="sb">3 sự cố quá hạn xử lý</div></div>
    </div>
    <div style="display:flex;gap:12px;flex:1">
      <div class="card kpi" style="flex:1"><div class="lb">THỜI GIAN XỬ LÝ SỰ CỐ</div>
        <div class="vl">2,4 ngày</div><div class="sb">mục tiêu: dưới 2 ngày</div></div>
      <div class="card kpi" style="flex:1"><div class="lb">TỈ LỆ BÁO ĐỘNG GIẢ</div>
        <div class="vl" style="color:#B54708">18%</div>
        <div class="sb">⭐ trên 25% thì người dùng tắt thông báo</div></div>
      <div class="card kpi" style="flex:1"><div class="lb">JOB CHẠY ĐÚNG GIỜ CAM KẾT</div>
        <div class="vl" style="color:#067647">96%</div>
        <div class="sb">4 tác vụ trễ trong 24 giờ qua</div></div>
    </div>
  </div>
</div>
<div style="display:flex;gap:16px">
  <div style="flex:1.25">
    <div class="card" style="padding:16px 19px;margin-bottom:14px">
      <div class="sec">ĐỘ PHỦ QUẢN TRỊ — BẢY CHỈ SỐ, VẠCH ĐEN LÀ MỤC TIÊU</div>
      {bars}
      <div class="note" style="background:#FEF3F2;border:1px solid #FECDCA;margin-top:12px">
        🔴 <b>Đây là màn quan trọng nhất để báo cáo lãnh đạo — vì nó nói thật.</b><br>
        Điểm chất lượng <b>87</b> nghe rất tốt, nhưng bảy thanh ở trên cho thấy
        <b>gần như mọi chỉ số quản trị đều dưới 40%</b>.<br>
        Ba thanh đang ở <b>0%</b> là ba tính năng <b>chưa tồn tại</b>: mức quan trọng ·
        sơ đồ nguồn gốc · che dữ liệu.
      </div>
    </div>
    <div class="card" style="padding:16px 19px">
      <div class="sec">BỐN BẢNG YẾU NHẤT ĐANG ĐƯỢC DÙNG NHIỀU</div>
      <table class="g" style="font-size:12.5px">
        <tr><th>Bảng</th><th>Mức QT</th><th style="text-align:center">Đạt</th>
          <th>Thiếu gì</th><th>Hạ nguồn</th></tr>{worst}</table>
      <div class="muted" style="font-size:11.5px;margin-top:9px">
        Bảng xếp theo <b>mức độ được dùng × mức độ thiếu quản trị</b> — không phải xếp theo
        điểm chất lượng. Bảng không ai dùng thì thiếu cũng ít hại.</div>
    </div>
  </div>
  <div style="width:520px;flex-shrink:0">
    <div class="card" style="padding:15px 17px;margin-bottom:13px">
      <div class="sec">SÁU MODULE ĐÓNG GÓP GÌ VÀO MÀN NÀY</div>
      <table class="g" style="font-size:12.5px">
        <tr><th>Từ menu</th><th>Chỉ số</th></tr>
        <tr><td><b>1.1</b></td><td>% bảng có người phụ trách · có mô tả · có Tier</td></tr>
        <tr><td><b>2.1 · 2.2</b></td><td>% cột có thuật ngữ · % cột nhạy cảm đã gắn nhãn</td></tr>
        <tr><td><b>3.2 · 3.4</b></td><td>Điểm chất lượng · sự cố đang mở · <b>tỉ lệ báo động giả</b></td></tr>
        <tr><td><b>4.1 · 4.3</b></td><td>% job chạy đúng giờ · <b>độ phủ sơ đồ nguồn gốc</b></td></tr>
        <tr><td><b>5.2 · 5.5</b></td><td>% chính sách có thời hạn · % cột nhạy cảm đã che</td></tr>
      </table>
      <div class="note" style="background:#EFF4FF;border:1px solid #C7D7FE;margin-top:11px;
        font-size:12.5px">
        🔗 <b>Màn này không khai gì.</b> Toàn bộ số liệu đọc lại từ năm module kia —
        nên nó chỉ đúng khi <b>các module kia được dùng thật</b>.<br><br>
        Đây cũng là lý do đặt nó ở <b>module cuối cùng</b> trong lộ trình.
      </div>
    </div>
    <div class="card" style="padding:15px 17px;margin-bottom:13px">
      <div class="sec">TỈ LỆ BÁO ĐỘNG GIẢ — CHỈ SỐ DỄ BỊ BỎ QUA NHẤT</div>
      <div style="font-size:12.5px;line-height:1.8">
        Tính từ <b>lý do đóng sự cố</b> ở menu 3.4 — tỉ lệ sự cố đóng với lý do
        <i>"Cảnh báo sai — luật đặt chưa đúng"</i>.
      </div>
      <table class="g" style="font-size:12.5px;margin-top:9px">
        <tr><th>Tỉ lệ</th><th>Nghĩa</th></tr>
        <tr><td>{chip("Dưới 10%", "g")}</td><td>Luật đặt tốt</td></tr>
        <tr><td>{chip("10 – 25%", "o")}</td><td>Cần rà lại ngưỡng của một số luật</td></tr>
        <tr><td>{chip("Trên 25%", "r")}</td>
            <td>🔴 <b>Người dùng sẽ tắt thông báo</b> — cả module ③ thành vô dụng</td></tr>
      </table>
      <div class="muted" style="font-size:11.5px;margin-top:9px">
        Đây chính là điều đã xảy ra với tính năng chất lượng cũ của SQLWF.</div>
    </div>
    <div class="note" style="background:#FFFAEB;border:1px solid #FEDF89">
      ⚠️ <b>SQLWF hiện có <span class="mono">report-management</span></b> với các báo cáo quản trị,
      nhưng đó là <b>báo cáo vận hành</b> — không phải bảng điều khiển sức khoẻ dữ liệu.<br><br>
      Khác biệt: báo cáo vận hành trả lời <i>"hệ thống chạy thế nào"</i>;
      màn này trả lời <i>"<b>dữ liệu</b> của công ty đang ở tình trạng nào"</i>.
    </div>
  </div>
</div>"""
    return shell("dmp.vds.vn/operations/health", H_CRUMB, H_TITLE, H_DESC, body,
                 "DMP · Menu 6.1 — SỨC KHOẺ DỮ LIỆU · Màn TỔNG QUAN", "m61",
                 tabs=("Tổng quan", H_TABS), actions=H_ACT)


# ============================================================ 6.1 tab theo miền
def health_domain():
    doms = [
        ("Kinh doanh", "1.842", 92, 41, 12, 4, "N.T.Phương", "#12B76A"),
        ("Tài chính", "684", 88, 62, 18, 2, "P.T.Hà", "#12B76A"),
        ("Sản phẩm", "1.204", 71, 22, 6, 5, "L.M.Tuấn", "#F79009"),
        ("Vận hành", "3.418", 64, 9, 2, 3, "Đội DE", "#F79009"),
        ("Chưa gán miền", "4.334", 0, 0, 0, 0, "— không ai", "#F04438"),
    ]
    tr = ""
    for nm, ntbl, score, cov, nrule, ninc, own, col in doms:
        sc = f'<b style="color:{col};font-size:15px">{score}</b>' if score else \
             '<span class="muted">chưa đo</span>'
        tr += (f'<tr><td><b>{nm}</b></td><td style="text-align:right">{ntbl}</td>'
               f'<td style="text-align:center">{sc}</td>'
               f'<td><div style="height:13px;background:#F2F4F7;border-radius:3px;width:130px">'
               f'<div style="width:{cov}%;height:13px;background:{col};border-radius:3px"></div>'
               f'</div><span style="font-size:11px;color:#8b95a7">{cov}% có người phụ trách</span></td>'
               f'<td style="text-align:center">{nrule}</td>'
               f'<td style="text-align:center;color:{"#B42318" if ninc > 3 else "#344054"}">{ninc}</td>'
               f'<td class="{"muted" if "không ai" in own else ""}">{own}</td></tr>')

    body = f"""
<div class="card" style="margin-bottom:14px"><table class="g">
  <tr><th>Miền dữ liệu</th><th style="text-align:right">Số bảng</th>
    <th style="text-align:center">Điểm chất lượng</th><th>Độ phủ quản trị</th>
    <th style="text-align:center">Số luật đang chạy</th>
    <th style="text-align:center">Sự cố đang mở</th><th>Người chịu trách nhiệm</th></tr>{tr}</table></div>
<div style="display:flex;gap:14px">
  <div class="note" style="flex:1;background:#FEF3F2;border:1px solid #FECDCA">
    🔴 <b>Dòng đáng chú ý nhất là dòng cuối: 4.334 bảng chưa gán miền — 38% toàn bộ.</b><br><br>
    Bảng không thuộc miền nào thì <b>không ai chịu trách nhiệm</b>, và mọi chỉ số quản trị
    trên nó đều bằng 0. Đây cũng là nhóm bảng mà <b>chính sách theo miền ở 5.2 không với tới</b>.<br><br>
    <b>Việc đầu tiên phải làm khi triển khai:</b> gán miền cho 4.334 bảng này —
    và đó là việc <b>không cần lập trình</b>, chỉ cần tổ chức.
  </div>
  <div class="note" style="width:520px;background:#EFF4FF;border:1px solid #C7D7FE">
    💡 <b>Vì sao chia theo miền chứ không chia theo phòng ban</b><br><br>
    Phòng ban <b>thay đổi theo cơ cấu tổ chức</b>; miền dữ liệu thì không.
    Bảng doanh thu vẫn thuộc miền Kinh doanh dù ban nào quản.<br><br>
    Cột <b>Người chịu trách nhiệm</b> mới là chỗ gắn với con người — và nó
    <b>đổi được mà không phải sắp xếp lại toàn bộ danh mục</b>.
  </div>
</div>"""
    return shell("dmp.vds.vn/operations/health/by-domain", H_CRUMB, H_TITLE, H_DESC, body,
                 "DMP · Menu 6.1 — SỨC KHOẺ DỮ LIỆU · Tab THEO MIỀN", "m61",
                 tabs=("Theo miền", H_TABS), actions=H_ACT)


# ============================================================ 6.2 cấu hình hệ thống
def sys_config():
    conns = "".join(
        f'<tr><td class="mono" style="color:{AC};font-size:11.5px">{a}</td><td>{chip(b, "t")}</td>'
        f'<td class="mono muted" style="font-size:11px">{c}</td>'
        f'<td>{chip(d, "g" if d == "Kết nối được" else "r")}</td>'
        f'<td class="muted" style="font-size:11.5px">{e}</td></tr>'
        for a, b, c, d, e in [
            ("MARIA_CRM_PROD", "JDBC", "jdbc:mariadb://10.58.20.11:3306/crm_prod",
             "Kết nối được", "NAP-034"),
            ("ORACLE_LEGACY", "JDBC", "jdbc:oracle:thin:@10.58.30.4:1521:LEGACY",
             "Kết nối được", "NAP-088"),
            ("SFTP_DOITAC_A", "FTP", "sftp://10.58.44.9:22/doi_soat/A/",
             "Kết nối được", "NAP-012"),
            ("KAFKA_EVENTS", "Kafka", "10.58.50.1:9092 · topic: user_events",
             "Kết nối được", "4 luồng"),
            ("HDFS_PARTNER_B", "HDFS + Kerberos", "principal: svc_dmp@VDS.LOCAL · keytab: ✔",
             "Lỗi xác thực", "NAP-101")])

    tiers = "".join(
        f'<tr><td>{chip(a, b)}</td><td class="muted">{c}</td><td>{d}</td><td>{e}</td></tr>'
        for a, b, c, d, e in [
            ("Tier 1 — Dữ liệu vàng", "o", "Sai là ảnh hưởng báo cáo lãnh đạo hoặc đối tác",
             "✔ BDA + DE · ✔ mô tả · ✔ ≥ 3 luật · ✔ luật freshness · ✔ giờ cam kết",
             "Không duyệt được nếu thiếu"),
            ("Tier 2 — Dữ liệu nghiệp vụ", "b", "Dùng cho phân tích nội bộ",
             "✔ BDA + DE · ✔ mô tả · ✔ ≥ 1 luật", "Cảnh báo, vẫn duyệt được"),
            ("Tier 3 — Dữ liệu thô / tạm", "n", "Vùng thô, bảng trung gian",
             "✔ DE phụ trách", "Không ràng buộc")])

    body = f"""
<div style="display:flex;gap:16px">
  <div style="flex:1.3">
    <div class="card" style="padding:16px 19px;margin-bottom:14px">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
        <div class="sec" style="margin:0">① KẾT NỐI NGUỒN</div>
        <span class="btn" style="padding:4px 10px;font-size:11.5px">➕ Thêm kết nối</span></div>
      <table class="g" style="font-size:12.5px">
        <tr><th>Mã kết nối</th><th>Loại</th><th>Chuỗi kết nối</th><th>Trạng thái</th>
          <th>Đang dùng ở</th></tr>{conns}</table>
      <div class="note" style="background:#ECFDF3;border:1px solid #A6F4C5;margin-top:11px">
        ✅ <b>SQLWF <span class="mono">connection-management</span> đã rất đầy đủ — giữ nguyên.</b>
        Có <span class="mono">connectionType</span> · <span class="mono">databaseType</span> ·
        <span class="mono">databaseConnectionURL</span> ·
        <span class="mono">databaseConnectionIpList</span> ·
        <span class="mono">ftpIpAddress</span> · <span class="mono">kafkaBrokers</span> ·
        <span class="mono">topics</span> · <b><span class="mono">kerberos</span> ·
        <span class="mono">keytab</span> · <span class="mono">principal</span></b> ·
        <span class="mono">protocol</span> · <span class="mono">portCLI</span> ·
        <span class="mono">portData</span>.<br>
        Chỉ thêm <b>cột "Đang dùng ở"</b> — để biết xoá kết nối này thì hỏng cái gì.
      </div>
    </div>
    <div class="card" style="padding:16px 19px;margin-bottom:14px;background:#FFFAEB;
      border-color:#FEDF89">
      <div class="sec" style="color:#B54708;border-color:#B54708">
        ② ĐỊNH NGHĨA MỨC QUAN TRỌNG (TIER) — MỤC MỚI</div>
      <table class="g" style="font-size:12.5px;background:#fff">
        <tr><th>Mức</th><th>Nghĩa</th><th>Điều kiện bắt buộc</th><th>Nếu thiếu</th></tr>
        {tiers}</table>
      <div style="font-size:12.5px;margin-top:11px;line-height:1.7">
        ⭐ <b>Đây là chỗ biến Tier từ một cái nhãn thành một ràng buộc thật.</b>
        Khai ở đây một lần, <b>menu 1.1 dùng để chặn khi duyệt bảng</b>.<br>
        Không có mục này thì Tier chỉ là chữ ghi cho đẹp — giống như cờ
        <span class="mono">cde</span> hiện nay của SQLWF, có lưu nhưng không ràng buộc gì.
      </div>
    </div>
    <div class="card" style="padding:16px 19px">
      <div class="sec">③ CHUẨN ĐẶT TÊN — KIỂM KHI TẠO BẢNG</div>
      <table class="g" style="font-size:12.5px">
        <tr><th style="width:150px">Đối tượng</th><th>Biểu thức kiểm</th><th>Ví dụ hợp lệ</th>
          <th>Mức</th></tr>
        <tr><td>Tên bảng</td><td class="mono" style="font-size:11px">^[a-z][a-z0-9_]{{2,62}}$</td>
            <td class="mono" style="font-size:11px">doi_soat_giao_dich_a</td>
            <td>{chip("Chặn", "r")}</td></tr>
        <tr><td>Tiền tố theo vùng</td>
            <td class="mono" style="font-size:11px">raw_ · dwh_ · bi_ · mart_ · tmp_</td>
            <td class="mono" style="font-size:11px">bi_doanh_thu_thang</td>
            <td>{chip("Cảnh báo", "o")}</td></tr>
        <tr><td>Tên cột</td><td class="mono" style="font-size:11px">^[a-z][a-z0-9_]{{1,62}}$</td>
            <td class="mono" style="font-size:11px">ngay_giao_dich</td>
            <td>{chip("Chặn", "r")}</td></tr>
        <tr><td>Tên job</td><td class="mono" style="font-size:11px">^JOB-[0-9]{{4}}$</td>
            <td class="mono" style="font-size:11px">JOB-0412</td>
            <td>{chip("Chặn", "r")}</td></tr>
      </table>
      <div class="note" style="background:#EFF4FF;border:1px solid #C7D7FE;margin-top:11px">
        💡 <b>Chuẩn đặt tên là một MỤC CẤU HÌNH, không phải một menu riêng.</b><br>
        Nó không có gì để quản lý theo vòng đời — chỉ là vài biểu thức, khai một lần,
        dùng để <b>kiểm ngay lúc tạo bảng ở 1.1</b>. Dựng hẳn một menu cho việc này là thừa.
      </div>
    </div>
  </div>
  <div style="width:520px;flex-shrink:0">
    <div class="card" style="padding:15px 17px;margin-bottom:13px">
      <div class="sec">④ THAM SỐ HỆ THỐNG</div>
      {fld("Ngưỡng cảnh báo xuất dữ liệu", "10.000 dòng",
           hint="Xuất vượt ngưỡng thì ghi cờ cảnh báo ở <b>nhật ký 5.4</b>")}
      {fld("Thời gian lưu nhật ký kiểm toán", "24 tháng",
           hint="Theo yêu cầu kiểm toán nội bộ")}
      {fld("Chu kỳ rà soát quyền", "Hằng quý &nbsp;·&nbsp; hạn phản hồi 14 ngày",
           hint="Quá hạn thì quyền <b>không dùng</b> tự thu hồi — menu <b>5.5</b>")}
      {fld("Nhắc trước khi quyền hết hạn", "7 ngày", hint="Menu <b>5.3</b>")}
      {fld("Số lần job hỏng liên tiếp thì mở sự cố", "2 lần", hint="Menu <b>4.1</b> → <b>3.4</b>")}
      {fld("Ngưỡng tỉ lệ báo động giả gây cảnh báo", "25%",
           hint="Vượt ngưỡng thì gửi cảnh báo cho quản trị dữ liệu — menu <b>6.1</b>")}
    </div>
    <div class="note" style="background:#ECFDF3;border:1px solid #A6F4C5;margin-bottom:13px">
      ✅ <b>SQLWF đã có <span class="mono">configuration-management</span></b> — cấu hình theo
      <span class="mono">taskCode</span>, có <b>Source name → Target name → Target type → Order</b>
      và <b>nhật ký cấu hình</b> (<span class="mono">detail-log-configuration</span>).<br><br>
      Menu 6.2 <b>giữ nguyên</b> và thêm hai mục: <b>định nghĩa Tier</b> và <b>chuẩn đặt tên</b>.
    </div>
    <div class="note" style="background:#FFFAEB;border:1px solid #FEDF89">
      ⚠️ <b>Mọi thay đổi ở menu này đều phải vào nhật ký 5.4.</b><br><br>
      Đổi ngưỡng cảnh báo hay điều kiện Tier là <b>thay đổi luật chơi của cả hệ thống</b> —
      phải biết ai đổi, đổi lúc nào, giá trị cũ là bao nhiêu.<br>
      SQLWF đã có sẵn cơ chế này qua <span class="mono">history-data</span> —
      chỉ cần <b>đăng ký các tham số mới vào đó</b>.
    </div>
  </div>
</div>"""
    return shell("dmp.vds.vn/operations/settings", "Operations › Cấu hình hệ thống",
                 "⚙️ Cấu hình hệ thống",
                 "Kết nối nguồn · tham số · định nghĩa Tier · chuẩn đặt tên",
                 body, "DMP · Menu 6.2 — CẤU HÌNH HỆ THỐNG · Màn CẤU HÌNH", "m62",
                 tabs=("Kết nối nguồn", ["Kết nối nguồn", "Định nghĩa Tier", "Chuẩn đặt tên",
                                         "Tham số hệ thống", "Nhật ký cấu hình"]))


SCREENS = {
    "dmp-53-health-board": health_board,
    "dmp-54-health-domain": health_domain,
    "dmp-55-system-config": sys_config,
}
