import json
import tempfile
from acmecli import run as run_mod
from acmecli.metrics import ramp_up as real_ramp_up


def test_run_urls_prints_ndjson(monkeypatch, capsys):
    def fake_compute(model_id):
        return (0.73, 12)

    monkeypatch.setattr(real_ramp_up, "compute_ramp_up", fake_compute)

    with tempfile.NamedTemporaryFile("w+", delete=False) as tf:
        tf.write("https://huggingface.co/google/gpt2\n")
        tf.flush()
        filename = tf.name

    rc = run_mod.run_urls(filename)
    assert rc == 0

    captured = capsys.readouterr()
    out_lines = [ln.strip() for ln in captured.out.splitlines() if ln.strip()]
    assert len(out_lines) >= 1
    rec = json.loads(out_lines[0])
    assert rec["category"] == "MODEL"
    assert "ramp_up_time" in rec
    assert "net_score" in rec
