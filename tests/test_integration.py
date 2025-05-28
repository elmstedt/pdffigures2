import os
import json
import subprocess
import sys


def test_cli_end_to_end(tmp_path):
    pdf = os.path.join(os.path.dirname(__file__), "sample_papers", "test1.pdf")
    out_prefix = tmp_path / "out"
    subprocess.run([
        sys.executable,
        "-m",
        "pdffigures2_python.cli",
        pdf,
        "-d",
        str(out_prefix),
    ], check=True)
    out_json = tmp_path / "out.json"
    assert out_json.exists()
    data = json.loads(out_json.read_text())
    assert isinstance(data, list)
