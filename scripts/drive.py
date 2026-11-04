"""L2: drive the real CLI like a user would, and keep the evidence."""

import json
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
out_dir = ROOT / "evidence" / datetime.now().strftime("%Y%m%d-%H%M%S")
out_dir.mkdir(parents=True, exist_ok=True)
failed = 0
for s in json.loads((ROOT / "scripts" / "scenarios.json").read_text()):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(s["cart"], f)
    cmd = ["tinycart", f.name] + (["--coupon", s["coupon"]] if s["coupon"] else [])
    r = subprocess.run(cmd, capture_output=True, text=True)
    got = (r.stdout + r.stderr).strip()
    ok = r.returncode == s["code"] and s["expect"] in got
    failed += not ok
    (out_dir / f"{s['name']}.txt").write_text(f"$ {' '.join(cmd)}\nexit={r.returncode}\n{got}\n")
    print(f"{'OK  ' if ok else 'FAIL'} {s['name']:<14} expect={s['expect']!r:<18} got={got!r}")
print(f"evidence: {out_dir.relative_to(ROOT)}")
sys.exit(1 if failed else 0)
