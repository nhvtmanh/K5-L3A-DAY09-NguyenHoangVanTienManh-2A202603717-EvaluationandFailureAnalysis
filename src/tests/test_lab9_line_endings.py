"""Dataset identity survives CRLF checkout while genuine input edits remain visible."""
import hashlib
import json

import pytest

from lab9 import evalset

pytestmark = pytest.mark.student


def test_dataset_sha_matches_linux_checkout_on_windows(tmp_path):
    lf = b'{"item_id":"E-001","failure_modes":["FM-03"]}\n'
    unix = tmp_path / "unix.jsonl"
    windows = tmp_path / "windows.jsonl"
    unix.write_bytes(lf)
    windows.write_bytes(lf.replace(b"\n", b"\r\n"))
    assert evalset.sha12(unix) == evalset.sha12(windows) == hashlib.sha256(lf).hexdigest()[:12]
    windows.write_bytes(lf.replace(b"FM-03", b"FM-06"))
    assert evalset.sha12(unix) != evalset.sha12(windows)


def test_builder_emits_lf_without_changing_labels(tmp_path, monkeypatch):
    source = tmp_path / "claims.jsonl"
    source.write_text(json.dumps({"claim_id": "C-001", "matrix_id": "T01",
                                  "expected": {"refund_vnd": 35000}}), encoding="utf-8")
    items, labels = tmp_path / "items.jsonl", tmp_path / "labels.json"
    monkeypatch.setattr(evalset, "ITEMS", items)
    monkeypatch.setattr(evalset, "LABELS", labels)
    assert evalset.build(source) == (1, 1)
    assert items.read_bytes().endswith(b"\n") and b"\r" not in items.read_bytes()
    assert json.loads(labels.read_text(encoding="utf-8")) == {"C-001": {"refund_vnd": 35000}}
