# -*- coding: utf-8 -*-
"""Màn hình công cụ Data Observability (Monte Carlo / Metaplane) — tự học ngưỡng."""
from common import shell, nav

AC = "#3B5BFD"
NAVI = lambda act: nav("Giám sát dữ liệu", AC, [
    ("🏠", "Trang chủ", act == "home"),
    ("📡", "Bộ giám sát", act == "monitor"),
    ("🚨", "Sự cố", act == "incident"),
    ("🔗", "Nguồn gốc", act == "lineage"),
    ("📈", "Báo cáo sức khoẻ", act == "report"),
    ("⚙️", "Cài đặt", act == "settings"),
], AC, "#B8C0D6")


def _chart():
    """Đồ thị số dòng theo ngày + dải ngưỡng hệ thống TỰ HỌC."""
    vals = [118, 121, 119, 124, 122, 117, 78, 120, 123, 125, 121, 118, 122, 80,
            124, 126, 123, 119, 121, 124, 122, 120, 125, 121, 123, 122, 124, 47]
    lo = [104, 105, 104, 106, 106, 104, 70, 105, 106, 108, 106, 104, 106, 72,
          107, 108, 107, 105, 106, 107, 107, 106, 108, 106, 107, 107, 108, 107]
    hi = [134, 136, 135, 138, 137, 133, 90, 136, 138, 140, 137, 134, 137, 92,
          139, 141, 139, 136, 137, 139, 138, 137, 140, 137, 139, 138, 140, 139]
    W, H, PAD = 1000, 250, 10
    n = len(vals)
    sx = lambda i: PAD + i * (W - 2 * PAD) / (n - 1)
    sy = lambda v: H - (v / 160) * H

    band = ("M " + " L ".join(f"{sx(i):.1f},{sy(v):.1f}" for i, v in enumerate(hi)) +
            " L " + " L ".join(f"{sx(i):.1f},{sy(v):.1f}" for i, v in reversed(list(enumerate(lo)))) + " Z")
    line = "M " + " L ".join(f"{sx(i):.1f},{sy(v):.1f}" for i, v in enumerate(vals))
    dots = "".join(
        f'<circle cx="{sx(i):.1f}" cy="{sy(v):.1f}" r="{5 if (lo[i] <= v <= hi[i]) is False else 2.6}" '
        f'fill="{"#F04438" if not (lo[i] <= v <= hi[i]) else "#3B5BFD"}"/>'
        for i, v in enumerate(vals))
    marks = "".join(
        f'<line x1="{sx(i):.1f}" y1="0" x2="{sx(i):.1f}" y2="{H}" stroke="#F04438" '
        f'stroke-width="1" stroke-dasharray="3 3"/>'
        for i, v in enumerate(vals) if not (lo[i] <= v <= hi[i]))
    return f"""<svg width="{W}" height="{H + 24}" viewBox="0 0 {W} {H + 24}">
  <path d="{band}" fill="#3B5BFD" opacity="0.13"/>
  {marks}
  <path d="{line}" fill="none" stroke="#3B5BFD" stroke-width="2"/>
  {dots}
  <text x="{sx(27) - 232:.0f}" y="{sy(47) - 14:.0f}" fill="#B42318" font-size="13"
        font-weight="700" font-family="Segoe UI">▼ Giảm 62% — bất thường</text>
  <text x="{sx(6) - 40:.0f}" y="{sy(78) - 10:.0f}" fill="#B42318" font-size="11.5"
        font-family="Segoe UI">Chủ nhật</text>
  <text x="{sx(13) - 40:.0f}" y="{sy(80) - 10:.0f}" fill="#B42318" font-size="11.5"
        font-family="Segoe UI">Chủ nhật</text>
  <text x="4" y="{H + 18}" fill="#98A2B3" font-size="11" font-family="Segoe UI">07/07</text>
  <text x="{W / 2 - 20:.0f}" y="{H + 18}" fill="#98A2B3" font-size="11" font-family="Segoe UI">21/07</text>
  <text x="{W - 60}" y="{H + 18}" fill="#98A2B3" font-size="11" font-family="Segoe UI">03/08</text>
</svg>"""


def anomaly():
    main = f"""
<div class="crumb">Bộ giám sát › hive_prod › bi.doi_soat_giao_dich_A</div>
<h1 class="t">📡 Giám sát khối lượng dữ liệu — bi.doi_soat_giao_dich_A
  <span class="chip" style="background:#FEF3F2;color:#B42318">🔴 Đang có sự cố</span></h1>
<div class="sub">Không ai khai ngưỡng bằng tay — hệ thống <b>tự học</b> từ 90 ngày lịch sử,
  tự nhận ra quy luật cuối tuần và tự cập nhật dải cho phép mỗi ngày.</div>
<div style="display:flex;gap:14px;margin:16px 0">
  <div class="card" style="flex:1;padding:12px 15px"><div class="muted" style="font-size:11px">SỐ DÒNG HÔM NAY</div>
    <div style="font-size:24px;font-weight:800;color:#B42318">47.210</div>
    <div style="font-size:11.5px;color:#B42318">▼ 62% so với dải dự kiến</div></div>
  <div class="card" style="flex:1;padding:12px 15px"><div class="muted" style="font-size:11px">DẢI HỆ THỐNG TỰ HỌC</div>
    <div style="font-size:24px;font-weight:800">107k – 139k</div>
    <div style="font-size:11.5px" class="muted">độ tin cậy 95% · học từ 90 ngày</div></div>
  <div class="card" style="flex:1;padding:12px 15px"><div class="muted" style="font-size:11px">PHÁT HIỆN LÚC</div>
    <div style="font-size:24px;font-weight:800">06:14</div>
    <div style="font-size:11.5px" class="muted">trước giờ làm 2h46'</div></div>
  <div class="card" style="flex:1;padding:12px 15px"><div class="muted" style="font-size:11px">SỐ LẦN BÁO ĐỘNG GIẢ / 30 NGÀY</div>
    <div style="font-size:24px;font-weight:800">0</div>
    <div style="font-size:11.5px" class="muted">2 ngày Chủ nhật đã được học là bình thường</div></div>
</div>
<div class="card" style="padding:18px 20px">
  <div style="display:flex;justify-content:space-between;margin-bottom:8px">
    <div style="font-size:13.5px;font-weight:700">Số dòng nạp mỗi ngày (nghìn dòng) — 28 ngày gần nhất</div>
    <div style="font-size:12px" class="muted">
      <span style="color:#3B5BFD">▬ giá trị thực tế</span> &nbsp;
      <span style="color:#8FA0FF">▨ dải hệ thống tự học</span> &nbsp;
      <span style="color:#F04438">● điểm bất thường</span></div></div>
  {_chart()}
</div>
<div style="display:flex;gap:16px;margin-top:16px">
  <div class="card" style="flex:1.4;padding:14px 17px;border-left:4px solid #F04438">
    <div style="font-size:13px;font-weight:700;margin-bottom:8px">🔎 HỆ THỐNG TỰ TRUY NGUYÊN NHÂN</div>
    <div style="font-size:12.5px;line-height:1.85">
      1. Job <span class="mono">job_doi_soat_A</span> chạy <b>thành công</b> lúc 06:02 — không phải lỗi job.<br>
      2. Bảng nguồn <span class="mono">raw.gd_doi_tac_A</span> hôm nay chỉ nhận
         <b>48.900 dòng</b> (bình thường ~125.000) → <b>nguyên nhân nằm ở thượng nguồn</b>.<br>
      3. Bảng nguồn có <b>thay đổi cấu trúc</b> lúc 02:11: cột <span class="mono">amount</span>
         đổi kiểu → nghi ngờ đối tác A đổi định dạng file.<br>
      4. <b>Kết luận đề xuất:</b> liên hệ đối tác A, chưa chạy các job hạ nguồn.</div></div>
  <div class="card" style="flex:1;padding:14px 17px">
    <div style="font-size:13px;font-weight:700;margin-bottom:8px">📣 ĐÃ THÔNG BÁO CHO AI</div>
    <div style="font-size:12.5px;line-height:1.9">
      👤 Trần Văn Hùng (DE phụ trách) — Telegram, 06:14<br>
      👤 Nguyễn Thị Phương (BDA phụ trách) — Email, 06:14<br>
      👥 Ban Kinh doanh (4 người dùng báo cáo hạ nguồn) — Email, 06:15<br><br>
      <span class="chip" style="background:#FEF3F2;color:#B42318">Đã tạm dừng 2 job hạ nguồn</span></div></div>
</div>"""
    return shell(
        "Nhóm công cụ Data Observability — bất thường khối lượng",
        "⚠️ Màn MINH HOẠ KHÁI NIỆM CHUNG của nhóm công cụ Data Observability "
        "— KHÔNG dựng theo một sản phẩm cụ thể nào",
        NAVI("monitor"), main, AC, "#1E2749",
        note="Nhóm Data Observability (Monte Carlo · Metaplane · Sifflet · Anomalo…) "
             "· CƠ CHẾ TỰ HỌC NGƯỠNG",
        note_right="<b>Data Observability là TÊN NHÓM SẢN PHẨM, không phải tên một tool.</b> "
                   "Màn này minh hoạ khái niệm chung — không phải ảnh chụp thật của sản phẩm nào")


SCREENS = {"obs-01-anomaly": anomaly}
