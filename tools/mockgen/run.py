# -*- coding: utf-8 -*-
"""Sinh HTML rồi render ra PNG bằng Chrome headless."""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_HTML = os.path.join(HERE, "html")
OUT_PNG = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(HERE, "png")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

os.makedirs(OUT_HTML, exist_ok=True)
os.makedirs(OUT_PNG, exist_ok=True)

MODULES = ["s_om", "s_dh", "s_soda", "s_mc", "s_ranger", "s_forms", "s_diag", "s_dmp1", "s_diag2", "s_dmp2", "s_dmp3", "s_dmp4", "s_dmp5", "s_dmp6", "s_dmp7", "s_dmp8", "s_dmp9", "s_dmp10", "s_dmp11"]
only = sys.argv[2] if len(sys.argv) > 2 else None

DEFAULT_SIZE = "1440,1010"
SIZE = {
    "diag-01-luong-thi-truong": "1280,560",
    "diag-02-sqlwf-tren-luong": "1280,560",
    "diag-03-mo-hinh-dmp": "1560,1080",
    "dmp-01-table-list": "1560,1060",
    "dmp-02-table-create": "1560,1130",
    "dmp-03-table-overview": "1700,1060",
    "dmp-04-table-columns": "1700,1010",
    "dmp-05-table-quality": "1700,1050",
    "dmp-06-table-lineage": "1700,1060",
    "dmp-07-table-perm": "1700,1010",
    "dmp-08-table-history": "1700,1010",
    "dmp-09-group-list": "1620,1010",
    "dmp-10-group-create": "1620,1010",
    "dmp-11-domain-list": "1620,1010",
    "dmp-12-domain-create": "1620,1010",
    "dmp-13-refdata-list": "1700,1010",
    "dmp-14-refdata-create": "1700,1050",
    "dmp-15-refdata-detail": "1750,1120",
    "dmp-16-glossary-list": "1700,1010",
    "dmp-17-glossary-detail": "1700,1130",
    "dmp-18-glossary-create": "1700,1090",
    "dmp-19-classification-tree": "1700,1080",
    "dmp-20-classification-create": "1660,1010",
    "dmp-21-rule-library": "1780,1050",
    "dmp-22-rule-create": "1780,1140",
    "dmp-23-quality-board": "1780,1090",
    "dmp-24-rule-assign": "1780,1345",
    "dmp-25-profiling": "1820,1010",
    "dmp-26-incident-list": "1820,1050",
    "dmp-27-incident-detail": "1820,1190",
    "dmp-28-alert-list": "1780,1010",
    "dmp-29-alert-create": "1700,1010",
    "dmp-31-job-list": "1860,1090",
    "dmp-33-job-steps": "1780,1180",
    "dmp-34-job-runs": "1820,1250",
    "dmp-36-ingest-list": "1860,1250",
    "dmp-37-ingest-create": "1820,1250",
    "dmp-39-pipeline-monitor": "1860,1420",
    "dmp-40-user-list": "1820,1150",
    "dmp-42-policy-data": "1860,1160",
    "dmp-43-policy-mask": "1880,1400",
    "dmp-45-policy-rowfilter": "1880,1390",
    "dmp-47-policy-bytag": "1820,1120",
    "dmp-48-request-list": "1900,1130",
    "dmp-50-request-approve": "1860,1300",
    "dmp-51-audit-log": "1920,1220",
    "dmp-52-perm-report": "1860,1140",
    "dmp-53-health-board": "1880,1410",
    "dmp-54-health-domain": "1780,1010",
    "dmp-55-system-config": "1880,1350",
    "dmp-30-alert-channels": "1820,1100",
    "dmp-32-job-create": "1880,1260",
    "dmp-35-job-versions": "1860,1120",
    "dmp-38-ingest-quarantine": "1900,1330",
    "dmp-41-group-acl": "1880,1230",
    "dmp-44-mask-create": "1900,1300",
    "dmp-46-rowfilter-create": "1900,1330",
    "dmp-49-request-create": "1880,1250",
}
for _rg in ("rg-01-policy-list", "rg-02-mask", "rg-03-rowfilter", "rg-04-audit",
            "rg-05-report", "rg-06-tagpolicy"):
    SIZE[_rg] = "1440,760"

screens = {}
for m in MODULES:
    try:
        mod = __import__(m)
    except ImportError:
        continue
    screens.update(mod.SCREENS)

for name, fn in screens.items():
    if only and only not in name:
        continue
    hp = os.path.join(OUT_HTML, name + ".html")
    with open(hp, "w", encoding="utf-8") as f:
        f.write(fn())
    pp = os.path.join(OUT_PNG, name + ".png")
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1.5",
                    "--screenshot=" + pp.replace("\\", "/"), "--window-size=" + SIZE.get(name, DEFAULT_SIZE),
                    "file:///" + hp.replace("\\", "/")],
                   capture_output=True)
    print(("OK  " if os.path.exists(pp) else "FAIL") + " " + name)
