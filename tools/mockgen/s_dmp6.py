# -*- coding: utf-8 -*-
"""DMP — Module ③ Data Quality: 3.1 Rule Library · 3.2 Luật & Kết quả · 3.3 Profiling
· 3.4 Incidents · 3.5 Alerts. Thiết kế bám theo bản DQ Tool demo của đội."""
from dmp import shell, fld, chip, AC
from s_dmp2 import _kpi
from s_dmp3 import _steps

DIM = {"Đầy đủ": "b", "Hợp lệ": "o", "Nhất quán": "t", "Duy nhất": "n",
       "Chính xác": "r", "Kịp thời": "g"}


# ============================================================ 3.1 Thư viện luật
def rule_lib():
    rows = [
        ("M-01", "not_null", "Không được rỗng", "Đầy đủ", "Cột", "ngưỡng % rỗng tối đa",
         "Dựng sẵn", "184"),
        ("M-04", "missing_percent", "Tỉ lệ rỗng dưới ngưỡng", "Đầy đủ", "Cột", "% tối đa",
         "Dựng sẵn", "62"),
        ("M-07", "format_regex", "Đúng định dạng", "Hợp lệ", "Cột", "biểu thức + % sai tối đa",
         "Dựng sẵn", "41"),
        ("M-08", "value_in_set", "Thuộc tập giá trị", "Hợp lệ", "Cột", "danh sách giá trị hợp lệ",
         "Dựng sẵn", "58"),
        ("M-09", "value_range", "Nằm trong khoảng", "Hợp lệ", "Cột", "min · max",
         "Dựng sẵn", "37"),
        ("M-12", "unique", "Không trùng", "Duy nhất", "Cột", "—", "Dựng sẵn", "96"),
        ("M-15", "referential_integrity", "Tồn tại trong danh mục", "Nhất quán", "Cột",
         "danh mục + cột đối chiếu", "Dựng sẵn", "0"),
        ("M-18", "cross_table_sum", "Tổng khớp với bảng nguồn", "Nhất quán", "Bảng",
         "bảng đối chiếu + % lệch", "Dựng sẵn", "0"),
        ("M-21", "row_count_range", "Số dòng trong khoảng", "Đầy đủ", "Bảng", "min · max",
         "Dựng sẵn", "128"),
        ("M-24", "freshness", "Dữ liệu đủ tươi", "Kịp thời", "Bảng", "khoảng thời gian tối đa",
         "Dựng sẵn", "74"),
        ("M-26", "on_time", "Về đúng giờ cam kết", "Kịp thời", "Bảng", "mốc giờ",
         "Dựng sẵn", "31"),
        ("M-31", "doi_soat_doanh_thu", "Đối soát doanh thu theo ngày", "Chính xác", "Bảng",
         "SQL tự viết", "Tự tạo", "4"),
    ]
    tr = ""
    for code, tech, nm, dim, lv, par, kind, used in rows:
        uc = "#8b95a7" if used == "0" else "#067647"
        tr += (f'<tr><td class="mono muted">{code}</td><td class="mono">{tech}</td>'
               f'<td><b>{nm}</b></td><td>{chip(dim, DIM[dim])}</td>'
               f'<td>{chip(lv, "n")}</td><td style="font-size:11.5px">{par}</td>'
               f'<td>{chip(kind, "b" if kind == "Dựng sẵn" else "o")}</td>'
               f'<td style="text-align:right;color:{uc};font-weight:700">{used}</td>'
               f'<td><span class="ico">👁</span><span class="ico">✎</span></td></tr>')

    body = _kpi([
        ("LOẠI KIỂM TRA", "28", "10 mức bảng · 18 mức cột", "#101828"),
        ("DỰNG SẴN / TỰ TẠO", "24 / 4", "tự tạo là SQL do đội viết", "#101828"),
        ("ĐANG ĐƯỢC DÙNG", "22", "6 loại chưa ai dùng lần nào", "#B54708"),
        ("LƯỢT GÁN VÀO BẢNG/CỘT", "715", "trên 64 bảng", "#101828"),
        ("PHỦ ĐỦ 6 CHIỀU?", "5/6", "chiều Chính xác chỉ có 1 loại", "#B42318"),
    ]) + f"""
<div style="display:flex;gap:10px;margin-bottom:13px;align-items:center">
  <div style="flex:1;border:1px solid #d0d7e2;border-radius:8px;padding:9px 13px;font-size:13px;
    background:#fff">🔍 <span class="muted">Tìm theo tên, mã kỹ thuật…</span></div>
  <span class="btn w">Chiều chất lượng: tất cả ▾</span>
  <span class="btn w">Mức áp dụng: tất cả ▾</span>
  <span class="btn w">Chưa dùng lần nào ☐</span>
</div>
<div class="card"><table class="g">
  <tr><th>Mã</th><th>Mã kỹ thuật</th><th>Tên loại kiểm tra</th><th>Chiều</th><th>Áp cho</th>
    <th>Tham số phải khai</th><th>Nguồn</th><th style="text-align:right">Lượt dùng</th><th></th></tr>
  {tr}</table>
  <div style="padding:9px 12px;font-size:12px" class="muted">… và 16 loại khác</div></div>
<div style="display:flex;gap:14px;margin-top:14px">
  <div class="note" style="flex:1;background:#EFF4FF;border:1px solid #C7D7FE">
    💡 <b>Thư viện luật khác gì với luật đang chạy:</b> đây là <b>danh mục các LOẠI kiểm tra</b> —
    khai một lần, dùng cho mọi bảng. Việc gán loại nào cho bảng nào nằm ở <b>menu 3.2</b>.<br>
    Ví dụ: loại <span class="mono">format_regex</span> khai ở đây một lần, rồi gán 41 lần
    cho 41 cột khác nhau với biểu thức khác nhau.
  </div>
  <div class="note" style="width:520px;background:#FEF3F2;border:1px solid #FECDCA">
    🔴 <b>Hai loại đang có 0 lượt dùng lại là hai loại quan trọng nhất:</b><br>
    • <span class="mono">referential_integrity</span> — <i>tồn tại trong danh mục</i>,
      cần <b>1.4 mở API</b> mới chạy được<br>
    • <span class="mono">cross_table_sum</span> — <i>tổng khớp với bảng nguồn</i>,
      chính là <b>bài toán đối soát</b> đội đang làm thủ công
  </div>
</div>"""
    return shell("dmp.vds.vn/quality/rule-library", "Data Quality › Thư viện luật",
                 "📐 Thư viện luật",
                 "Danh mục 28 loại kiểm tra dùng chung — khai một lần, gán cho mọi bảng",
                 body, "DMP · Menu 3.1 — THƯ VIỆN LUẬT · Màn DANH SÁCH", "m31",
                 tabs=("Tất cả loại", ["Tất cả loại", "Mức bảng", "Mức cột", "Tự tạo",
                                       "Chưa dùng lần nào"]),
                 actions='<span class="btn">➕ Tạo loại kiểm tra</span>')


# ============================================================ 3.1 tạo loại kiểm tra
def rule_create():
    body = _steps([("Thông tin loại", "now"), ("Tham số", "next"),
                   ("Ngưỡng mặc định", "next"), ("Chạy thử", "next")]) + f"""
<div style="display:flex;gap:18px">
  <div style="width:470px;flex-shrink:0">
    <div class="card" style="padding:17px 19px">
      <div class="sec">① THÔNG TIN LOẠI KIỂM TRA</div>
      {fld("Mã", "M-32 &nbsp;<span class='muted'>(tự sinh)</span>", ro=True)}
      {fld("Mã kỹ thuật", "doi_soat_so_luong_gd", True,
           "Chữ thường, gạch dưới. Dùng khi gọi qua API và hiện trong nhật ký chạy", mono=True)}
      {fld("Tên loại kiểm tra", "Đối soát số lượng giao dịch với nguồn", True,
           "Viết bằng tiếng Việt để người nghiệp vụ chọn được")}
      {fld("Chiều chất lượng", "Nhất quán ▾", True,
           "Quyết định luật này đóng góp vào <b>chiều nào khi chấm điểm bảng</b> ở 3.2")}
      {fld("Áp cho", "Bảng ▾", True, "Bảng — kiểm cả bảng · Cột — kiểm một cột cụ thể")}
      {fld("Mô tả nghiệp vụ", "So tổng số giao dịch trong bảng đích với bảng nguồn thô. "
                              "Lệch quá ngưỡng nghĩa là job xử lý bị mất dòng.", True,
           "Hiện ở ô chọn luật để người khai biết loại này dùng khi nào")}
      {fld("Nguồn", "Tự tạo — SQL do đội viết ▾",
           hint="<b>Dựng sẵn</b> = hệ thống cung cấp, không sửa được<br>"
                "<b>Tự tạo</b> = đội viết SQL riêng")}
    </div>
  </div>
  <div style="flex:1">
    <div class="card" style="padding:17px 19px;margin-bottom:13px">
      <div class="sec">② THAM SỐ NGƯỜI KHAI PHẢI ĐIỀN KHI GÁN</div>
      <table class="g" style="font-size:12.5px">
        <tr><th>Tên tham số</th><th>Kiểu</th><th>Bắt buộc</th><th>Mô tả</th><th></th></tr>
        <tr><td class="mono">bang_nguon</td><td>Chọn bảng</td><td>✔</td>
            <td>Bảng dùng để đối chiếu</td><td style="color:#B42318">✕</td></tr>
        <tr><td class="mono">phan_tram_lech</td><td>Số thực</td><td>✔</td>
            <td>Lệch quá bao nhiêu % thì coi là sai</td><td style="color:#B42318">✕</td></tr>
        <tr><td colspan="5" style="color:#8b95a7">+ Thêm tham số</td></tr>
      </table>
      <div style="margin-top:12px">
        <div style="font-size:12px;font-weight:600;color:#344054;margin-bottom:5px">
          Câu SQL sinh ra <span class="muted">(dùng biến của tham số ở trên)</span></div>
        <div style="background:#0f172a;border-radius:8px;padding:12px 14px;
          font-family:Consolas,monospace;font-size:12px;line-height:1.7;color:#e2e8f0">
<span style="color:#7C8798">-- {'{'}bang_dich{'}'} và {'{'}bang_nguon{'}'} do hệ thống thay khi chạy</span><br>
<span style="color:#C084FC">SELECT</span> ABS(<br>
&nbsp;&nbsp;(<span style="color:#C084FC">SELECT COUNT</span>(*) <span style="color:#C084FC">FROM</span> {'{'}bang_dich{'}'}) -<br>
&nbsp;&nbsp;(<span style="color:#C084FC">SELECT COUNT</span>(*) <span style="color:#C084FC">FROM</span> {'{'}bang_nguon{'}'})<br>
) * 100.0 / (<span style="color:#C084FC">SELECT COUNT</span>(*) <span style="color:#C084FC">FROM</span> {'{'}bang_nguon{'}'})</div>
      </div>
    </div>
    <div class="card" style="padding:17px 19px;margin-bottom:13px">
      <div class="sec">③ NGƯỠNG MẶC ĐỊNH &nbsp;<span class="muted"
        style="font-weight:400;font-size:11px">(cấp 1 trong 3 cấp)</span></div>
      <table class="g" style="font-size:12.5px">
        <tr><td style="width:200px;color:#667085">Cảnh báo khi</td>
            <td>lệch &gt; <b>0,5%</b></td></tr>
        <tr><td style="color:#667085">Thất bại khi</td><td>lệch &gt; <b>2%</b></td></tr>
      </table>
      <div class="note" style="background:#EFF4FF;border:1px solid #C7D7FE;margin-top:11px">
        📐 <b>Ngưỡng có 3 cấp, cấp dưới đè cấp trên:</b><br>
        ① <b>Ngưỡng mặc định của loại luật</b> — khai ở đây<br>
        ② <b>Ngưỡng của bảng</b> — khai ở 3.2, đè lên ①<br>
        ③ <b>Ngưỡng của từng lần gán</b> — đè lên cả ① và ②<br>
        Người khai chỉ cần điền khi muốn khác mặc định.
      </div>
    </div>
    <div style="display:flex;gap:10px">
      <span class="btn">▶️ Chạy thử trên 1 bảng</span><span class="btn w">Lưu nháp</span>
      <span class="btn w">Huỷ</span></div>
  </div>
</div>"""
    return shell("dmp.vds.vn/quality/rule-library/create",
                 "Data Quality › Thư viện luật › Tạo loại kiểm tra", "➕ Tạo loại kiểm tra",
                 "Khai một loại kiểm tra mới vào thư viện — gồm tham số, câu SQL và ngưỡng mặc định",
                 body, "DMP · Menu 3.1 — THƯ VIỆN LUẬT · Màn THÊM MỚI", "m31")


# ============================================================ 3.2 bảng điều khiển
def rule_board():
    rows = [
        ("bi.doi_soat_giao_dich_A", "Tier 1", "7", "83", "5", "1", "1", "🔴 1 sự cố", "06:12"),
        ("dwh.thue_bao_ngay", "Tier 1", "9", "100", "9", "0", "0", "—", "06:08"),
        ("bi.doanh_thu_thang", "Tier 1", "8", "88", "6", "2", "0", "—", "06:20"),
        ("dm.doi_tac", "Tier 2", "3", "100", "3", "0", "0", "—", "05:40"),
        ("mart.kpi_kinh_doanh", "Tier 2", "4", "62", "2", "1", "1", "🔴 1 sự cố", "06:30"),
        ("raw.gd_doi_tac_A", "Tier 3", "1", "100", "1", "0", "0", "—", "05:35"),
    ]
    tr = ""
    for nm, tier, tot, sc, ok, wn, fa, inc, at in rows:
        scc = "#067647" if int(sc) >= 90 else "#B54708" if int(sc) >= 70 else "#B42318"
        tr += (f'<tr><td class="mono" style="color:{AC}">{nm}</td>'
               f'<td>{chip(tier, "o" if tier == "Tier 1" else "b" if tier == "Tier 2" else "n")}</td>'
               f'<td style="text-align:center">{tot}</td>'
               f'<td style="text-align:center;color:{scc};font-weight:800;font-size:14px">{sc}</td>'
               f'<td style="text-align:center;color:#067647">{ok}</td>'
               f'<td style="text-align:center;color:#B54708">{wn}</td>'
               f'<td style="text-align:center;color:#B42318">{fa}</td>'
               f'<td>{inc}</td><td class="muted">{at}</td>'
               f'<td><span class="ico">👁</span></td></tr>')

    dims = "".join(
        f'<div style="flex:1;text-align:center;padding:10px 6px;border-radius:8px;background:{bg}">'
        f'<div style="font-size:11px;color:#667085">{d}</div>'
        f'<div style="font-size:20px;font-weight:800;color:{c}">{v}</div>'
        f'<div style="font-size:10.5px;color:#8b95a7">{n} luật</div></div>'
        for d, v, c, bg, n in [("Đầy đủ", "96", "#067647", "#ECFDF3", "312"),
                               ("Hợp lệ", "71", "#B54708", "#FFFAEB", "196"),
                               ("Nhất quán", "84", "#B54708", "#FFFAEB", "42"),
                               ("Duy nhất", "99", "#067647", "#ECFDF3", "128"),
                               ("Chính xác", "78", "#B54708", "#FFFAEB", "12"),
                               ("Kịp thời", "92", "#067647", "#ECFDF3", "105")])

    body = _kpi([
        ("ĐIỂM CHẤT LƯỢNG HỆ THỐNG", "87", "▼ 3 điểm so với tuần trước", "#B54708"),
        ("BẢNG ĐANG ĐƯỢC KIỂM", "64 / 11.482", "0,6% — mục tiêu quý IV: 100% Tier 1", "#B42318"),
        ("LUẬT ĐANG CHẠY", "795", "trên 64 bảng", "#101828"),
        ("LUẬT THẤT BẠI HÔM NAY", "9", "sinh ra 4 sự cố", "#B42318"),
        ("LẦN QUÉT GẦN NHẤT", "06:30", "hôm nay", "#101828"),
    ]) + f"""
<div class="card" style="padding:15px 18px;margin-bottom:14px">
  <div class="sec">ĐIỂM TOÀN HỆ THỐNG THEO 6 CHIỀU</div>
  <div style="display:flex;gap:10px">{dims}</div>
  <div class="muted" style="font-size:11.5px;margin-top:9px">
    Chiều <b>Chính xác</b> chỉ có 12 luật trên toàn hệ thống — thấp nhất.
    Đây là chiều khó nhất vì phải đối chiếu với nguồn ngoài.</div>
</div>
<div style="display:flex;gap:10px;margin-bottom:12px;align-items:center">
  <div style="flex:1;border:1px solid #d0d7e2;border-radius:8px;padding:9px 13px;font-size:13px;
    background:#fff">🔍 <span class="muted">Tìm bảng…</span></div>
  <span class="btn w">Mức QT: tất cả ▾</span><span class="btn w">Chiều: tất cả ▾</span>
  <span class="btn w">Chỉ bảng có luật hỏng ☐</span>
  <span class="btn">➕ Gán luật cho bảng</span>
</div>
<div class="card"><table class="g">
  <tr><th>Bảng</th><th>Mức QT</th><th style="text-align:center">Số luật</th>
    <th style="text-align:center">Điểm</th><th style="text-align:center">Đạt</th>
    <th style="text-align:center">Cảnh báo</th><th style="text-align:center">Thất bại</th>
    <th>Sự cố</th><th>Quét lúc</th><th></th></tr>{tr}</table></div>
<div class="note" style="background:#FEF3F2;border:1px solid #FECDCA;margin-top:14px">
  🔴 <b>Con số đáng báo cáo lãnh đạo nhất: 64 / 11.482 bảng đang được kiểm — 0,6%.</b><br>
  Điểm chất lượng 87 chỉ tính trên 64 bảng đó. <b>Với 99,4% bảng còn lại, hệ thống không biết
  dữ liệu đúng hay sai.</b> Vì vậy thẻ "Bảng đang được kiểm" phải luôn đứng cạnh thẻ "Điểm chất lượng",
  không được tách ra.
</div>"""
    return shell("dmp.vds.vn/quality/rules", "Data Quality › Luật & Kết quả",
                 "🎯 Luật & Kết quả",
                 "Toàn cảnh chất lượng dữ liệu — bảng nào đang được kiểm, điểm bao nhiêu, hỏng ở đâu",
                 body, "DMP · Menu 3.2 — LUẬT & KẾT QUẢ · Màn BẢNG ĐIỀU KHIỂN", "m32",
                 tabs=("Theo bảng", ["Theo bảng", "Theo luật", "Theo chiều chất lượng",
                                     "Bảng chưa có luật"]))


# ============================================================ 3.2 gán luật
def rule_assign():
    lib = "".join(
        f'<div style="border:1px solid {"#2563EB" if on else "#E4E7EC"};border-radius:7px;'
        f'padding:8px 11px;margin-bottom:6px;background:{"#EFF4FF" if on else "#fff"}">'
        f'<div style="font-size:12.5px;font-weight:{700 if on else 600}">{n}</div>'
        f'<div class="muted" style="font-size:11px">{d}</div></div>'
        for n, d, on in [
            ("format_regex — Đúng định dạng", "Hợp lệ · mức cột", True),
            ("value_in_set — Thuộc tập giá trị", "Hợp lệ · mức cột", False),
            ("referential_integrity — Tồn tại trong danh mục", "Nhất quán · mức cột", False),
            ("not_null — Không được rỗng", "Đầy đủ · mức cột", False),
            ("unique — Không trùng", "Duy nhất · mức cột", False),
            ("row_count_range — Số dòng trong khoảng", "Đầy đủ · mức bảng", False)])

    body = _steps([("Chọn bảng / cột", "done"), ("Chọn loại kiểm tra", "done"),
                   ("Điền tham số", "now"), ("Ngưỡng & lịch", "next"),
                   ("Hành động khi hỏng", "next")]) + f"""
<div style="display:flex;gap:18px">
  <div style="width:330px;flex-shrink:0">
    <div style="font-size:12.5px;font-weight:700;margin-bottom:8px">
      CHỌN LOẠI TỪ THƯ VIỆN <span class="muted" style="font-weight:400">(28 loại)</span></div>
    <div style="border:1px solid #d0d7e2;border-radius:7px;padding:7px 10px;font-size:12px;
      margin-bottom:8px;background:#fff">🔍 <span class="muted">Tìm loại kiểm tra…</span></div>
    {lib}
    <div class="note" style="background:#ECFDF3;border:1px solid #A6F4C5;margin-top:10px">
      💡 <b>Hệ thống gợi ý 3 loại</b> dựa trên dữ liệu đã có ở tab Cột:
      cột <span class="mono">so_dien_thoai</span> đã khai <i>"Đúng đầu số di động VN"</i> ở
      ô Quy tắc nghiệp vụ → gợi ý <span class="mono">format_regex</span>.
    </div>
  </div>
  <div style="flex:1">
    <div class="card" style="padding:17px 19px;margin-bottom:13px">
      <div class="sec">③ THAM SỐ CỦA LUẬT</div>
      {fld("Áp cho", "bi.doi_soat_giao_dich_A › cột so_dien_thoai", ro=True)}
      {fld("Tên luật hiển thị", "so_dien_thoai đúng đầu số di động VN", True,
           "Tên này hiện trong cảnh báo và sự cố — <b>viết để người nhận đọc là hiểu ngay</b>")}
      {fld("Biểu thức định dạng", "^(84|0)(3|5|7|8|9)[0-9]{8}$", True,
           "Lấy sẵn từ ô <b>Tập giá trị</b> đã khai ở tab Cột, sửa được", mono=True)}
      {fld("Chiều chất lượng", "Hợp lệ &nbsp;<span class='muted'>(theo loại kiểm tra)</span>", ro=True)}
    </div>
    <div class="card" style="padding:17px 19px;margin-bottom:13px">
      <div class="sec">④ NGƯỠNG & LỊCH CHẠY</div>
      <table class="g" style="font-size:12.5px;margin-bottom:11px">
        <tr><th>Cấp ngưỡng</th><th>Cảnh báo</th><th>Thất bại</th><th>Đang dùng</th></tr>
        <tr><td>① Mặc định của loại luật</td><td>&gt; 0,1%</td><td>&gt; 1%</td>
            <td class="muted">—</td></tr>
        <tr><td>② Ngưỡng của bảng</td><td>—</td><td>—</td><td class="muted">chưa đặt</td></tr>
        <tr style="background:#EFF4FF"><td><b>③ Ngưỡng riêng cho luật này</b></td>
            <td><b>&gt; 0,2%</b></td><td><b>&gt; 0,5%</b></td>
            <td>{chip("Đang áp dụng", "b")}</td></tr>
      </table>
      {fld("Lịch chạy", "Hằng ngày — 06:00 ▾", True,
           "Nên chạy <b>sau khi job ghi dữ liệu xong</b>. Hệ thống cảnh báo nếu đặt trước giờ job chạy")}
    </div>
    <div class="card" style="padding:17px 19px">
      <div class="sec">⑤ HÀNH ĐỘNG KHI LUẬT HỎNG</div>
      <div style="font-size:12.5px;line-height:2.1">
        <div><input type="checkbox" checked> <b>Sinh sự cố</b> và gán cho
          <b>DE phụ trách của bảng</b> — lấy từ tab Tổng quan</div>
        <div><input type="checkbox" checked> Gửi cảnh báo theo quy tắc ở <b>3.5</b></div>
        <div><input type="checkbox" checked> <b>Lưu mẫu 100 dòng lỗi</b> để tải về gửi bên tạo dữ liệu</div>
        <div><input type="checkbox"> <b>Chặn job hạ nguồn</b> — không cho dữ liệu sai chảy tiếp</div>
        <div><input type="checkbox"> Gắn nhãn cảnh báo lên bảng cho mọi người dùng thấy</div>
      </div>
      <div class="note" style="background:#FFFAEB;border:1px solid #FEDF89;margin-top:11px">
        ⚠️ <b>Ô "Lưu mẫu dòng lỗi" là ô quan trọng nhất.</b> Không bật thì cảnh báo chỉ nói
        <i>"có 1.204 dòng sai"</i> mà không nói sai ở đâu — người nhận không làm gì được.<br>
        Bù lại nó <b>tốn tài nguyên</b>: mỗi lần chạy phải quét lại lấy mẫu.
        Nên bật cho bảng Tier 1, cân nhắc với Tier 3.
      </div>
    </div>
    <div style="display:flex;gap:10px;margin-top:15px">
      <span class="btn">▶️ Chạy thử ngay</span><span class="btn w">Lưu</span>
      <span class="btn w">Huỷ</span></div>
  </div>
</div>"""
    return shell("dmp.vds.vn/quality/rules/assign",
                 "Data Quality › Luật & Kết quả › Gán luật", "➕ Gán luật cho bảng / cột",
                 "Chọn loại kiểm tra từ thư viện, điền tham số, đặt ngưỡng và hành động khi hỏng",
                 body, "DMP · Menu 3.2 — LUẬT & KẾT QUẢ · Màn GÁN LUẬT", "m32")


# ============================================================ 3.3 Profiling
def profiling():
    cols = [
        ("giao_dich_id", "STRING", "12.480.331", "0%", "12.480.331", "100%", "—", "—", "—",
         "GD20260803001204"),
        ("so_dien_thoai", "STRING", "12.480.331", "0,02%", "11.203.004", "89,8%", "—", "—", "10",
         "0912345678"),
        ("so_tien", "DECIMAL", "12.480.331", "0%", "884.120", "7,1%", "1.000", "48.500.000",
         "—", "1.250.000"),
        ("ngay_ghi_nhan", "DATE", "12.480.331", "0%", "947", "0,008%", "01/01/2024", "03/08/2026",
         "—", "2026-08-03"),
        ("trang_thai", "STRING", "12.480.331", "0%", "3", "0,00002%", "—", "—", "4", "KHOP"),
        ("doi_tac", "STRING", "12.480.331", "0%", "12", "0,0001%", "—", "—", "8", "DT_VNPAY"),
    ]
    tr = ""
    for nm, ty, tot, nul, dis, disp, mn, mx, ln, sample in cols:
        nulc = "#B42318" if nul != "0%" else "#067647"
        tr += (f'<tr><td class="mono"><b>{nm}</b></td><td class="mono muted">{ty}</td>'
               f'<td style="text-align:right">{tot}</td>'
               f'<td style="text-align:right;color:{nulc}">{nul}</td>'
               f'<td style="text-align:right">{dis}</td>'
               f'<td style="text-align:right" class="muted">{disp}</td>'
               f'<td style="text-align:right" class="mono">{mn}</td>'
               f'<td style="text-align:right" class="mono">{mx}</td>'
               f'<td style="text-align:center">{ln}</td>'
               f'<td class="mono" style="font-size:11px">{sample}</td></tr>')

    body = _kpi([
        ("BẢNG ĐÃ PHÂN TÍCH", "1.842", "16% trên 11.482 bảng", "#B54708"),
        ("LẦN QUÉT GẦN NHẤT", "06:12", "bảng đang xem", "#101828"),
        ("SỐ CỘT ĐO ĐƯỢC", "6 / 6", "không có cột nào lỗi", "#067647"),
        ("THỜI GIAN QUÉT", "47 giây", "trên 12,4 triệu dòng", "#101828"),
    ]) + f"""
<div style="display:flex;gap:10px;margin-bottom:13px;align-items:center">
  <div style="flex:1;border:1px solid #d0d7e2;border-radius:8px;padding:9px 13px;font-size:13px;
    background:#fff">🗂️ Bảng: <b>bi.doi_soat_giao_dich_A</b> ▾</div>
  <span class="btn w">Lịch quét: Hằng tuần — CN 02:00 ▾</span>
  <span class="btn w">⬇️ Xuất Excel</span>
  <span class="btn">▶️ Quét lại ngay</span>
</div>
<div class="card"><table class="g">
  <tr><th>Cột</th><th>Kiểu</th><th style="text-align:right">Số dòng</th>
    <th style="text-align:right">% rỗng</th><th style="text-align:right">Giá trị phân biệt</th>
    <th style="text-align:right">% phân biệt</th><th style="text-align:right">Min</th>
    <th style="text-align:right">Max</th><th style="text-align:center">Độ dài</th>
    <th>Mẫu giá trị</th></tr>{tr}</table></div>
<div style="display:flex;gap:14px;margin-top:14px">
  <div class="note" style="flex:1;background:#EFF4FF;border:1px solid #C7D7FE">
    ⭐ <b>Menu này là NƠI DUY NHẤT đo chỉ số thống kê cột.</b> Tab Cột của 1.1 chỉ
    <b>đọc lại để hiển thị</b>, không tự đo. Đây là cách giải vấn đề <b>V1</b> —
    hiện SQLWF đang đo ở hai nơi: <span class="mono">data-dictionary</span> và
    <span class="mono">data-quality</span>.
  </div>
  <div class="note" style="width:520px;background:#ECFDF3;border:1px solid #A6F4C5">
    💡 <b>Kết quả phân tích dùng để gợi ý luật ở 3.2:</b><br>
    • <span class="mono">trang_thai</span> chỉ có <b>3 giá trị phân biệt</b>
      → gợi ý luật <i>thuộc tập giá trị</i><br>
    • <span class="mono">giao_dich_id</span> có <b>100% giá trị phân biệt</b>
      → gợi ý luật <i>không trùng</i><br>
    • <span class="mono">so_dien_thoai</span> <b>độ dài luôn là 10</b>
      → gợi ý luật <i>đúng định dạng</i>
  </div>
</div>"""
    return shell("dmp.vds.vn/quality/profiling", "Data Quality › Phân tích dữ liệu",
                 "🔬 Phân tích dữ liệu (Profiling)",
                 "Đo chỉ số thống kê của từng cột — nơi duy nhất đo, các màn khác đọc lại",
                 body, "DMP · Menu 3.3 — PHÂN TÍCH DỮ LIỆU · Màn KẾT QUẢ", "m33",
                 tabs=("Theo cột", ["Theo cột", "Phân bố giá trị", "Lịch sử quét"]))


# ============================================================ 3.4 danh sách sự cố
def inc_list():
    rows = [
        ("#4821", "so_dien_thoai đúng đầu số VN", "bi.doi_soat_giao_dich_A", "Tier 1", "Cao",
         "Đang xử lý", "T.V.Hùng", "31/07", "06/08", "7 ngày"),
        ("#4835", "Tổng doanh thu khớp nguồn", "mart.kpi_kinh_doanh", "Tier 2", "Trung bình",
         "Chờ duyệt", "L.M.Tuấn", "05/08", "08/08", "2 ngày"),
        ("#4840", "Dữ liệu về đúng giờ cam kết", "bi.doanh_thu_thang", "Tier 1", "Cao",
         "Đã gán", "T.V.Hùng", "06/08", "07/08", "1 ngày"),
        ("#4841", "doi_tac tồn tại trong danh mục", "bi.doi_soat_giao_dich_A", "Tier 1", "Thấp",
         "Mới", "—", "07/08", "—", "0 ngày"),
        ("#4802", "Số dòng trong khoảng cho phép", "dwh.thue_bao_ngay", "Tier 1", "Cao",
         "Đã giải quyết", "L.M.Tuấn", "28/07", "30/07", "đã đóng"),
    ]
    tr = ""
    for cid, nm, tb, tier, sev, st, who, op, due, age in rows:
        stc = {"Mới": "r", "Đã gán": "o", "Đang xử lý": "o", "Chờ duyệt": "b",
               "Đã giải quyết": "g"}[st]
        sevc = {"Cao": "r", "Trung bình": "o", "Thấp": "n"}[sev]
        tr += (f'<tr><td class="mono"><b>{cid}</b></td><td>{nm}</td>'
               f'<td class="mono" style="font-size:11.5px;color:{AC}">{tb}</td>'
               f'<td>{chip(tier, "o" if tier == "Tier 1" else "b")}</td>'
               f'<td>{chip(sev, sevc)}</td><td>{chip(st, stc)}</td>'
               f'<td>{who}</td><td class="muted">{op}</td><td class="muted">{due}</td>'
               f'<td>{age}</td><td><span class="ico">👁</span></td></tr>')

    flow = "".join(
        f'<div style="flex:1;text-align:center;padding:8px 4px;border-radius:7px;background:{bg};'
        f'border:1px solid {bd}"><div style="font-size:11.5px;font-weight:700;color:{fg}">{s}</div>'
        f'<div style="font-size:16px;font-weight:800;color:{fg}">{n}</div></div>'
        for s, n, fg, bg, bd in [
            ("Mới", "3", "#B42318", "#FEF3F2", "#FECDCA"),
            ("Đã gán", "2", "#B54708", "#FFFAEB", "#FEDF89"),
            ("Đang xử lý", "4", "#B54708", "#FFFAEB", "#FEDF89"),
            ("Chờ duyệt", "1", "#2563EB", "#EFF4FF", "#C7D7FE"),
            ("Đã giải quyết", "12", "#067647", "#ECFDF3", "#A6F4C5"),
            ("Đóng", "148", "#475467", "#F2F4F7", "#E4E7EC")])

    body = _kpi([
        ("SỰ CỐ ĐANG MỞ", "10", "3 chưa ai nhận", "#B42318"),
        ("QUÁ HẠN XỬ LÝ", "2", "sự cố #4821 quá 1 ngày", "#B42318"),
        ("THỜI GIAN XỬ LÝ TRUNG BÌNH", "2,4 ngày", "mục tiêu: dưới 2 ngày", "#B54708"),
        ("SỰ CỐ LẶP LẠI", "4", "cùng một luật hỏng nhiều lần", "#B54708"),
    ]) + f"""
<div class="card" style="padding:14px 17px;margin-bottom:14px">
  <div class="sec">VÒNG ĐỜI SỰ CỐ — 6 TRẠNG THÁI</div>
  <div style="display:flex;gap:8px;align-items:center">{flow}</div>
  <div class="muted" style="font-size:11.5px;margin-top:9px">
    Chuyển từ <b>Chờ duyệt</b> sang <b>Đã giải quyết</b> áp dụng nguyên tắc <b>4 mắt</b> —
    người xử lý và người duyệt <b>phải là hai người khác nhau</b>.</div>
</div>
<div style="display:flex;gap:10px;margin-bottom:12px;align-items:center">
  <div style="flex:1;border:1px solid #d0d7e2;border-radius:8px;padding:9px 13px;font-size:13px;
    background:#fff">🔍 <span class="muted">Tìm theo mã sự cố, tên luật, tên bảng…</span></div>
  <span class="btn w">Trạng thái: đang mở ▾</span><span class="btn w">Mức nghiêm trọng ▾</span>
  <span class="btn w">Người xử lý ▾</span><span class="btn w">Chỉ quá hạn ☐</span>
</div>
<div class="card"><table class="g">
  <tr><th>Mã</th><th>Luật bị hỏng</th><th>Bảng</th><th>Mức QT</th><th>Nghiêm trọng</th>
    <th>Trạng thái</th><th>Người xử lý</th><th>Mở lúc</th><th>Hạn</th><th>Tuổi</th><th></th></tr>
  {tr}</table></div>
<div class="note" style="background:#EFF4FF;border:1px solid #C7D7FE;margin-top:14px">
  💡 <b>Sự cố khác cảnh báo ở chỗ nào:</b> cảnh báo là <b>tin nhắn gửi đi rồi thôi</b>.
  Sự cố là <b>một việc có người chịu trách nhiệm, có hạn, có trạng thái, và phải được đóng lại</b>.<br>
  Đây chính là thứ SQLWF chưa có — hiện `warning-history` chỉ lưu lịch sử gửi cảnh báo,
  không ai biết cảnh báo đó đã được xử lý hay chưa.
</div>"""
    return shell("dmp.vds.vn/quality/incidents", "Data Quality › Sự cố chất lượng",
                 "🚨 Sự cố chất lượng",
                 "Biến cảnh báo thành việc có người chịu trách nhiệm và có hạn xử lý",
                 body, "DMP · Menu 3.4 — SỰ CỐ CHẤT LƯỢNG · Màn DANH SÁCH", "m34",
                 tabs=("Đang mở", ["Đang mở", "Tôi xử lý", "Chờ tôi duyệt", "Quá hạn", "Đã đóng"]))


# ============================================================ 3.4 chi tiết sự cố
def inc_detail():
    bad = "".join(
        f'<tr><td class="mono">{a}</td><td class="mono" style="color:#B42318"><b>{b}</b></td>'
        f'<td>{c}</td><td class="mono">{d}</td></tr>'
        for a, b, c, d in [
            ("GD20260803001204", "+84-912-345-678", "Có dấu gạch nối và dấu +", "2026-08-03"),
            ("GD20260803001881", "0912345", "Chỉ có 7 chữ số", "2026-08-03"),
            ("GD20260803002140", "N/A", "Không phải số", "2026-08-03"),
            ("GD20260803002377", "0212345678", "Đầu số cố định", "2026-08-03"),
            ("GD20260803002903", "(trống)", "Giá trị rỗng", "2026-08-03")])
    steps = "".join(
        f'<div style="display:flex;gap:10px;padding:9px 0;border-bottom:1px solid #eef1f6">'
        f'<div style="width:96px;font-size:11.5px;color:#8b95a7">{t}</div>'
        f'<div style="flex:1;font-size:12.5px">{c}</div></div>'
        for t, c in [
            ("31/07 06:14", "🔴 <b>Hệ thống</b> — sự cố mở tự động, trạng thái <b>Mới</b>, "
                            "mức nghiêm trọng <b>Cao</b> (bảng Tier 1)"),
            ("31/07 06:14", "👤 <b>Hệ thống</b> — tự gán cho <b>Trần Văn Hùng</b> "
                            "(DE phụ trách của bảng) → <b>Đã gán</b>"),
            ("31/07 09:20", "💬 <b>Nguyễn Thị Phương</b> — đã báo đối tác A. Họ xác nhận đổi hệ thống "
                            "từ 31/07, sẽ gửi lại file chuẩn trong tuần"),
            ("31/07 09:05", "🔧 <b>Trần Văn Hùng</b> — nhận xử lý → <b>Đang xử lý</b>. "
                            "Đã chặn 1.204 dòng không cho chảy xuống báo cáo"),
            ("05/08 14:30", "📎 <b>Trần Văn Hùng</b> — tải file 1.204 dòng lỗi gửi đối tác")])

    body = _kpi([
        ("TRẠNG THÁI", "Đang xử lý", "quá hạn 1 ngày", "#B42318"),
        ("MỨC NGHIÊM TRỌNG", "Cao", "bảng Tier 1 · cột có nhãn PII", "#B42318"),
        ("TỈ LỆ SAI HÔM NAY", "0,96%", "ngưỡng cho phép 0,5%", "#B42318"),
        ("SỐ DÒNG SAI", "1.204", "trên 12.480.331 dòng", "#101828"),
        ("LẶP LẠI", "7 ngày liên tiếp", "từ 31/07", "#B54708"),
    ]) + f"""
<div style="display:flex;gap:16px">
  <div style="flex:1.4">
    <div class="card" style="padding:16px 19px;margin-bottom:14px">
      <div class="sec">THÔNG TIN SỰ CỐ</div>
      <table class="g" style="font-size:12.5px">
        <tr><td style="width:180px;color:#667085">Luật bị hỏng</td>
            <td><b>so_dien_thoai đúng đầu số di động VN</b> <span class="muted">(format_regex)</span></td></tr>
        <tr><td style="color:#667085">Bảng · Cột</td>
            <td class="mono">bi.doi_soat_giao_dich_A › so_dien_thoai</td></tr>
        <tr><td style="color:#667085">Chiều chất lượng</td><td>{chip("Hợp lệ", "o")}</td></tr>
        <tr><td style="color:#667085">Người xử lý</td><td>Trần Văn Hùng (DE phụ trách)</td></tr>
        <tr><td style="color:#667085">Hạn xử lý</td>
            <td style="color:#B42318"><b>06/08/2026 — đã quá 1 ngày</b></td></tr>
        <tr><td style="color:#667085">Nguyên nhân đã ghi nhận</td>
            <td>Đối tác A đổi định dạng file từ 31/07</td></tr>
      </table>
    </div>
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:9px">
      <div style="font-size:13.5px;font-weight:700">5 dòng sai đầu tiên (mẫu 100 dòng đã lưu)</div>
      <div style="display:flex;gap:8px"><span class="btn w">⬇️ Tải toàn bộ 1.204 dòng</span>
        <span class="btn w">📧 Gửi đối tác A</span></div></div>
    <div class="card"><table class="g">
      <tr><th>Mã giao dịch</th><th>Giá trị sai</th><th>Sai ở chỗ nào</th><th>Ngày</th></tr>
      {bad}</table></div>
  </div>
  <div style="width:520px;flex-shrink:0">
    <div class="card" style="padding:15px 17px;margin-bottom:13px">
      <div class="sec">CHUYỂN TRẠNG THÁI</div>
      <div style="display:flex;align-items:center;gap:5px;flex-wrap:wrap;margin-bottom:11px">
        {chip("✓ Mới", "n")}→{chip("✓ Đã gán", "n")}→{chip("● Đang xử lý", "o")}→
        {chip("Chờ duyệt", "n")}→{chip("Đã giải quyết", "n")}→{chip("Đóng", "n")}</div>
      <div style="display:flex;gap:8px;margin-bottom:11px">
        <span class="btn">Gửi duyệt ▶</span><span class="btn w">Đổi người xử lý</span></div>
      <div class="note" style="background:#FFFAEB;border:1px solid #FEDF89">
        ⚠️ <b>Nguyên tắc 4 mắt.</b> Người xử lý <b>không được tự đóng</b> sự cố của mình.
        Bấm "Gửi duyệt" thì sự cố chuyển sang <b>Chờ duyệt</b> và người duyệt
        <i>(BDA phụ trách của bảng)</i> mới có quyền đóng.
      </div>
    </div>
    <div class="card" style="padding:15px 17px;margin-bottom:13px">
      <div class="sec">LÝ DO ĐÓNG SỰ CỐ &nbsp;<span class="muted"
        style="font-weight:400;font-size:11px">(bắt buộc chọn)</span></div>
      <div style="font-size:12.5px;line-height:2">
        ○ Đã sửa dữ liệu nguồn &nbsp;&nbsp; ○ Đã sửa job xử lý<br>
        ○ Cảnh báo sai — luật đặt chưa đúng &nbsp;&nbsp; ○ Chấp nhận rủi ro<br>
        ○ Trùng với sự cố khác &nbsp;&nbsp; ○ Khác (ghi rõ)</div>
      <div class="muted" style="font-size:11.5px;margin-top:8px">
        Thống kê lý do đóng ở <b>6.1</b> cho biết bao nhiêu % cảnh báo là <b>báo động giả</b> —
        chỉ số quyết định người dùng có tin hệ thống hay không.</div>
    </div>
    <div class="card" style="padding:15px 17px">
      <div class="sec">DÒNG THỜI GIAN</div>{steps}</div>
  </div>
</div>"""
    return shell("dmp.vds.vn/quality/incidents/4821",
                 "Data Quality › Sự cố chất lượng › #4821", "🚨 Sự cố #4821",
                 "so_dien_thoai đúng đầu số di động VN &nbsp;·&nbsp; bi.doi_soat_giao_dich_A "
                 "&nbsp;·&nbsp; mở 31/07/2026", body,
                 "DMP · Menu 3.4 — SỰ CỐ CHẤT LƯỢNG · Màn CHI TIẾT", "m34",
                 tabs=("Tổng quan", ["Tổng quan", "Dòng lỗi", "Dòng thời gian", "Sự cố liên quan"]),
                 actions='<span class="btn w">🔗 Xem luật</span><span class="btn">Gửi duyệt</span>')


# ============================================================ 3.5 Cảnh báo
def alert_list():
    rows = [
        ("QT-01", "Sự cố mức Cao trên bảng Tier 1", "Ngay lập tức", "Telegram · Email",
         "DE + BDA phụ trách", "Bật", "18"),
        ("QT-02", "Sự cố mức Trung bình", "Gom 60 phút", "Email", "DE phụ trách", "Bật", "42"),
        ("QT-03", "Tổng hợp hằng ngày", "Bản tin 08:00", "Email", "Nhóm quản trị dữ liệu",
         "Bật", "1"),
        ("QT-04", "Tổng hợp hằng tuần cho lãnh đạo", "Bản tin thứ Hai", "Email",
         "Ban Giám đốc", "Bật", "1"),
        ("QT-05", "Dữ liệu về trễ so với cam kết", "Ngay lập tức", "Telegram · SMS",
         "DE phụ trách", "Bật", "23"),
        ("QT-08", "Cảnh báo thử nghiệm", "Ngay lập tức", "Webhook", "Đội DE", "Tắt", "0"),
    ]
    tr = ""
    for code, nm, mode, ch, who, st, cnt in rows:
        tr += (f'<tr><td class="mono muted">{code}</td><td><b>{nm}</b></td>'
               f'<td>{chip(mode, "b")}</td><td>{ch}</td><td>{who}</td>'
               f'<td>{chip(st, "g" if st == "Bật" else "n")}</td>'
               f'<td style="text-align:right">{cnt}</td>'
               f'<td><span class="ico">✎</span><span class="ico">⋯</span></td></tr>')

    body = _kpi([
        ("QUY TẮC ĐANG BẬT", "7", "1 quy tắc đang tắt", "#101828"),
        ("CẢNH BÁO GỬI HÔM NAY", "84", "▼ 62% nhờ cơ chế gom", "#067647"),
        ("ĐÃ CHẶN DO TRÙNG", "137", "cùng luật, cùng bảng, trong 60 phút", "#101828"),
        ("KÊNH ĐANG DÙNG", "4", "Email · Telegram · SMS · Webhook", "#101828"),
    ]) + f"""
<div style="display:flex;gap:10px;margin-bottom:13px;align-items:center">
  <div style="flex:1;border:1px solid #d0d7e2;border-radius:8px;padding:9px 13px;font-size:13px;
    background:#fff">🔍 <span class="muted">Tìm quy tắc…</span></div>
  <span class="btn w">Chế độ gửi: tất cả ▾</span><span class="btn w">Kênh: tất cả ▾</span>
</div>
<div class="card"><table class="g">
  <tr><th>Mã</th><th>Tên quy tắc</th><th>Chế độ gửi</th><th>Kênh</th><th>Người nhận</th>
    <th>Trạng thái</th><th style="text-align:right">Gửi hôm nay</th><th></th></tr>{tr}</table></div>
<div style="display:flex;gap:14px;margin-top:14px">
  <div class="note" style="flex:1;background:#ECFDF3;border:1px solid #A6F4C5">
    ✅ <b>Phần này SQLWF đã có và còn mạnh hơn mặt bằng thị trường:</b>
    `notify-manager` quản nhóm nhận email · `telegram` · `warning-history` có duyệt hàng loạt
    và tạo ticket SOC. Đủ cả <b>Email · SMS · Telegram</b> — nhiều tool thị trường chỉ có
    Email và Slack.
  </div>
  <div class="note" style="width:520px;background:#EFF4FF;border:1px solid #C7D7FE">
    💡 <b>Bốn chế độ gửi để chống spam</b> — đây là thứ cần bổ sung:<br>
    ① <b>Ngay lập tức</b> — chỉ dành cho sự cố mức Cao<br>
    ② <b>Gom N phút</b> — nhiều sự cố trong khoảng thời gian gộp thành một tin<br>
    ③ <b>Bản tin hằng ngày</b> — tổng hợp gửi buổi sáng<br>
    ④ <b>Bản tin hằng tuần</b> — cho lãnh đạo<br>
    Con số <b>137 cảnh báo bị chặn do trùng</b> cho thấy giá trị của cơ chế này.
  </div>
</div>"""
    return shell("dmp.vds.vn/quality/alerts", "Data Quality › Cảnh báo",
                 "🔔 Cảnh báo & Kênh gửi",
                 "Quy tắc gửi cảnh báo — ai nhận gì, qua kênh nào, gom hay gửi ngay",
                 body, "DMP · Menu 3.5 — CẢNH BÁO · Màn DANH SÁCH QUY TẮC", "m35",
                 tabs=("Quy tắc", ["Quy tắc", "Lịch sử gửi", "Kênh gửi", "Mẫu nội dung"]),
                 actions='<span class="btn">➕ Tạo quy tắc</span>')


def alert_create():
    body = f"""
<div style="display:flex;gap:18px">
  <div style="width:480px;flex-shrink:0">
    <div class="card" style="padding:17px 19px">
      <div class="sec">① ĐIỀU KIỆN KÍCH HOẠT</div>
      {fld("Tên quy tắc", "Sự cố mức Cao trên bảng Tier 1", True)}
      {fld("Kích hoạt khi", "Sự cố chất lượng được sinh ra ▾", True,
           "Các lựa chọn: sự cố sinh ra · luật thất bại · dữ liệu về trễ · "
           "điểm chất lượng tụt dưới ngưỡng · cấu trúc bảng thay đổi")}
      {fld("Chỉ áp dụng cho", "Mức quan trọng: Tier 1 ▾ &nbsp; Mức nghiêm trọng: Cao ▾",
           hint="Để trống là áp dụng cho tất cả — <b>nên thu hẹp</b> để tránh gửi tràn lan")}
      {fld("Miền dữ liệu", "Tất cả ▾", hint="Lọc thêm theo miền nếu mỗi ban muốn quy tắc riêng")}
    </div>
  </div>
  <div style="flex:1">
    <div class="card" style="padding:17px 19px;margin-bottom:13px">
      <div class="sec">② CHẾ ĐỘ GỬI</div>
      <div style="font-size:12.5px;line-height:2.2">
        <div>◉ <b>Ngay lập tức</b> — gửi ngay khi sự cố sinh ra
          <span class="muted">· chỉ nên dùng cho mức Cao</span></div>
        <div>○ <b>Gom lại</b> — <input style="width:40px" value="60"> phút gửi một lần
          <span class="muted">· nhiều sự cố gộp thành một tin</span></div>
        <div>○ <b>Bản tin hằng ngày</b> — gửi lúc <input style="width:52px" value="08:00"></div>
        <div>○ <b>Bản tin hằng tuần</b> — gửi thứ Hai lúc 08:00</div>
      </div>
      <div class="note" style="background:#FFFAEB;border:1px solid #FEDF89;margin-top:11px">
        ⚠️ <b>Chống trùng:</b> cùng một luật trên cùng một bảng, trong khoảng
        <input style="width:40px" value="60"> phút chỉ gửi <b>một lần</b>, kèm số lần lặp.<br>
        Không có cơ chế này thì một luật hỏng chạy 5 phút/lần sẽ gửi <b>288 tin mỗi ngày</b> —
        và người nhận sẽ tắt thông báo.
      </div>
    </div>
    <div class="card" style="padding:17px 19px;margin-bottom:13px">
      <div class="sec">③ NGƯỜI NHẬN & KÊNH</div>
      {fld("Người nhận", chip("DE phụ trách của bảng", "b") + chip("BDA phụ trách của bảng", "b") +
           '<span class="muted">+ Thêm</span>', True,
           "<b>Không khai tên cụ thể</b> mà dùng vai trò — người phụ trách đổi thì cảnh báo tự đi đúng chỗ")}
      {fld("Kênh gửi", chip("Telegram", "t") + chip("Email", "t") +
           '<span class="muted">+ SMS · Webhook</span>', True,
           "Nhiều kênh thì gửi song song. SMS chỉ nên dùng cho mức Cao vì tốn phí")}
      {fld("Mẫu nội dung", "Mẫu chuẩn — sự cố chất lượng ▾",
           hint="Mẫu chứa: tên luật · bảng · cột · số dòng sai · link mở sự cố")}
    </div>
    <div style="display:flex;gap:10px">
      <span class="btn">▶️ Gửi thử cho tôi</span><span class="btn w">Lưu</span>
      <span class="btn w">Huỷ</span></div>
  </div>
</div>"""
    return shell("dmp.vds.vn/quality/alerts/create",
                 "Data Quality › Cảnh báo › Tạo quy tắc", "➕ Tạo quy tắc cảnh báo",
                 "Khai điều kiện kích hoạt, chế độ gửi và người nhận", body,
                 "DMP · Menu 3.5 — CẢNH BÁO · Màn TẠO QUY TẮC", "m35")


SCREENS = {
    "dmp-21-rule-library": rule_lib,
    "dmp-22-rule-create": rule_create,
    "dmp-23-quality-board": rule_board,
    "dmp-24-rule-assign": rule_assign,
    "dmp-25-profiling": profiling,
    "dmp-26-incident-list": inc_list,
    "dmp-27-incident-detail": inc_detail,
    "dmp-28-alert-list": alert_list,
    "dmp-29-alert-create": alert_create,
}
