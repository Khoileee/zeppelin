# -*- coding: utf-8 -*-
"""Sửa các màn DataHub cho khớp tài liệu chính thức."""
p = "s_dh.py"
t = open(p, encoding="utf-8").read()
n = 0


def rep(a, b):
    global t, n
    if a not in t:
        print("  KHONG THAY:", a[:60].replace("\n", " "))
        return
    t = t.replace(a, b)
    n += 1


# 1) Trạng thái hợp đồng theo metamodel: ACTIVE / PENDING
rep('''          <div class="chip" style="background:#FEF3F2;color:#B42318;font-size:13px;padding:5px 13px">
            🔴 ĐANG VI PHẠM</div>
          <div class="muted" style="font-size:11.5px;margin-top:5px">4/5 điều khoản đạt</div></div>''',
    '''          <div class="chip" style="background:#ECFDF3;color:#067647;font-size:13px;padding:5px 13px">
            State: ACTIVE</div>
          <div class="muted" style="font-size:11.5px;margin-top:5px">
            4/5 phép kiểm đạt · <span style="color:#B42318">1 đang thất bại</span></div></div>''')

# 2) Thay thẻ "tỉ lệ tuân thủ 30 ngày" (không có trong tài liệu) bằng khối Sự cố
i = t.find('<div style="font-size:12px;font-weight:700;color:#5a6472;margin-bottom:8px">TỈ LỆ TUÂN THỦ 30 NGÀY</div>')
j = t.find('return shell("DataHub — Hợp đồng dữ liệu"')
if i > 0 and j > i:
    k = t.rfind('<div class="card"', 0, i)
    t = t[:k] + '''<div class="card" style="padding:13px 15px">
      <div style="font-size:12px;font-weight:700;color:#5a6472;margin-bottom:8px">SỰ CỐ ĐANG MỞ</div>
      <div style="font-size:12.5px;line-height:1.85">
        <b>Incident #4821</b><br>
        Nguồn sinh ra: <span class="mono">ASSERTION_FAILURE</span> (hệ thống tự tạo)<br>
        Trạng thái: <b>INVESTIGATION</b><br>
        <span class="muted" style="font-size:11px">Chuỗi trạng thái: TRIAGE → INVESTIGATION →
        WORK_IN_PROGRESS → FIXED / NO_ACTION_REQUIRED</span><br><br>
        <span class="muted" style="font-size:11.5px">Ở màn tìm kiếm có bộ lọc
        "Has Active Incidents" để xem mọi bảng đang có sự cố.</span>
      </div></div>
  </div>
</div>"""
    ''' + t[j:]
    n += 1

# 3) Sửa ô "hệ thống tự động làm 3 việc"
rep('''      🔴 <b>Vì hợp đồng đang vi phạm:</b> hệ thống tự động (1) gắn nhãn cảnh báo lên bảng để mọi người
      dùng đều thấy, (2) thông báo cho <b>4 đơn vị tiêu thụ</b> ở cột bên phải,
      (3) tạm dừng job hạ nguồn <span class="mono">job_tonghop_doanh_thu</span> theo cấu hình.</div>''',
    '''      🔴 <b>Khi một phép kiểm thất bại:</b> DataHub <b>tự sinh một Sự cố (Incident)</b> gắn vào bảng,
      với nguồn sinh ra là <span class="mono">ASSERTION_FAILURE</span>, rồi gửi thông báo theo đăng ký.<br>
      ⚠️ <b>Việc chặn job hạ nguồn KHÔNG tự động.</b> Đó là cơ chế riêng tên là
      <b>Pipeline Circuit Breaking</b>, phải <b>tự tích hợp</b>: luồng Airflow/Dagster gọi API hỏi
      "bảng đầu vào có sự cố đang mở không" rồi tự quyết định dừng. Tài liệu DataHub ghi rõ khung hợp đồng
      chỉ <b>định nghĩa và theo dõi</b>, còn <b>thực thi phải tích hợp thêm</b>.</div>''')

# 4) Impact analysis — bỏ cột "Rủi ro" tự bịa, dùng các facet có trong tài liệu
rep('''    def row(ic, name, kind, level, owner, usage, risk):
        rc = {"Cao": "#B42318", "Trung bình": "#B54708", "Thấp": "#067647"}[risk]
        return (f'<tr><td>{ic} <b>{name}</b></td><td>{kind}</td><td class="mono">{level}</td>'
                f'<td>{owner}</td><td>{usage}</td>'
                f'<td style="color:{rc};font-weight:700">{risk}</td></tr>')''',
    '''    def row(ic, name, kind, level, owner, usage, risk):
        return (f'<tr><td>{ic} <b>{name}</b></td><td>{kind}</td><td class="mono">{level}</td>'
                f'<td>{owner}</td><td>{usage}</td><td>{risk}</td></tr>')''')

for a, b in [
    ('"bi.doanh_thu_thang", "Bảng", "1", "Đội DE", "412 lượt/tuần", "Cao"',
     '"bi.doanh_thu_thang", "Tập dữ liệu", "1", "Đội DE", "Kinh doanh", "Hive"'),
    ('"Báo cáo Doanh thu ngày", "Báo cáo", "2", "Ban Kinh doanh", "1.204 lượt/tuần", "Cao"',
     '"Báo cáo Doanh thu ngày", "Báo cáo", "2", "Ban Kinh doanh", "Kinh doanh", "PowerBI"'),
    ('"Dashboard Đối soát", "Báo cáo", "2", "Ban Kinh doanh", "310 lượt/tuần", "Trung bình"',
     '"Dashboard Đối soát", "Báo cáo", "2", "Ban Kinh doanh", "Kinh doanh", "PowerBI"'),
    ('"Mô hình dự báo rời mạng", "Mô hình", "2", "Data Science", "chạy hằng tuần", "Trung bình"',
     '"Mô hình dự báo rời mạng", "Mô hình", "2", "Data Science", "Kỹ thuật", "MLflow"'),
    ('"mart.kpi_kinh_doanh", "Bảng", "3", "Đội DE", "88 lượt/tuần", "Trung bình"',
     '"mart.kpi_kinh_doanh", "Tập dữ liệu", "3", "Đội DE", "Kinh doanh", "Hive"'),
    ('"BC Tổng Giám đốc hằng tháng", "Báo cáo", "3", "Văn phòng", "42 lượt/tháng", "Cao"',
     '"BC Tổng Giám đốc hằng tháng", "Báo cáo", "3", "Văn phòng", "Kinh doanh", "PowerBI"'),
    ('"File xuất cho đối tác A", "Tệp xuất", "3", "Ban Kinh doanh", "hằng ngày", "Thấp"',
     '"File xuất cho đối tác A", "Tập dữ liệu", "3", "Ban Kinh doanh", "Kinh doanh", "S3"'),
    ('<th>Mức độ sử dụng</th><th>Rủi ro</th></tr>', '<th>Miền dữ liệu</th><th>Nền tảng</th></tr>'),
    ('<span class="btn ghost">Độ sâu: 3 cấp ▾</span>',
     '<span class="btn ghost">Số cấp phụ thuộc: 3 ▾</span>'),
    ('<span class="btn ghost">Chỉ hiện tài sản có người dùng ▾</span>',
     '<span class="btn ghost">Người phụ trách ▾</span><span class="btn ghost">Nền tảng ▾</span>'),
]:
    rep(a, b)

rep('''    thuộc <b>4 đơn vị</b>, trong đó <b style="color:#B42318">3 tài sản rủi ro Cao</b>.
    Bấm "Xuất danh sách" để gửi thông báo cho đúng người trước khi làm.</div>''',
    '''    thuộc <b>4 đơn vị</b>. Bấm <b>Xuất CSV</b> để tải danh sách — file kèm sẵn
    <b>người phụ trách, miền dữ liệu, nhãn, thuật ngữ</b> và link quay lại từng tài sản.<br>
    <span style="color:#B54708">⚠️ Mặc định hệ thống chỉ tra <b>1 cấp phụ thuộc</b> cho nhẹ máy —
    muốn xem sâu hơn phải tự chỉnh.</span></div>''')

rep('''    <div class="muted" style="font-size:11px">SỐ NGƯỜI DÙNG BỊ ẢNH HƯỞNG</div>
    <div style="font-size:26px;font-weight:800">63</div></div>''',
    '''    <div class="muted" style="font-size:11px">SỐ CẤP PHỤ THUỘC ĐÃ TRA</div>
    <div style="font-size:26px;font-weight:800">3</div></div>''')

rep('''    <div class="muted" style="font-size:11px">GỢI Ý HÀNH ĐỘNG</div>
    <div style="font-size:12.5px;line-height:1.7;margin-top:4px">
      Gửi thông báo trước 5 ngày làm việc cho 4 đơn vị · Đưa thay đổi vào hợp đồng dữ liệu v3 ·
      Chạy song song bảng cũ/mới 1 tuần trước khi cắt.</div></div>''',
    '''    <div class="muted" style="font-size:11px">GHI CHÚ</div>
    <div style="font-size:12.5px;line-height:1.7;margin-top:4px">
      Phần "gợi ý hành động" <b>không phải tính năng của DataHub</b> — đó là quy trình
      <b>ta tự đặt ra</b> dựa trên danh sách này.</div></div>''')

open(p, "w", encoding="utf-8", newline="").write(t)
print("Da sua", n, "cho trong s_dh.py")
