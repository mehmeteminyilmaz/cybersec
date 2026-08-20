import pytest
import os
import sys
import tempfile
import hashlib

# Path setup
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'cyber-panel', 'modules')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'file-integrity-monitor')))

from fim import (
    calculate_string_hash,
    calculate_file_hash,
    compare_file_records,
    get_demo_simulation
)

def test_calculate_string_hash():
    text = "system_configuration_v1"
    expected = hashlib.sha256(text.encode()).hexdigest()
    assert calculate_string_hash(text, "sha256") == expected
    assert len(calculate_string_hash(text, "sha256")) == 64

def test_calculate_file_hash():
    data = b"admin:x:1000:1000:Admin User:/home/admin:/bin/bash\n"
    with tempfile.NamedTemporaryFile(delete=False, mode='wb') as tmp:
        tmp.write(data)
        tmp_path = tmp.name

    try:
        file_hash = calculate_file_hash(tmp_path, "sha256")
        expected_hash = hashlib.sha256(data).hexdigest()
        assert file_hash == expected_hash
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

def test_compare_file_records_intact():
    baseline = {
        "/etc/hosts": {"hash": "aaaabbbbcccc", "size": 100},
        "/etc/resolv.conf": {"hash": "111122223333", "size": 50}
    }
    current = {
        "/etc/hosts": {"hash": "aaaabbbbcccc", "size": 100},
        "/etc/resolv.conf": {"hash": "111122223333", "size": 50}
    }
    res = compare_file_records(baseline, current)
    assert res["status"] == "success"
    assert res["is_compromised"] is False
    assert res["intact_count"] == 2
    assert res["modified_count"] == 0
    assert res["security_score"] == 100

def test_compare_file_records_tamper_and_anomaly():
    baseline = {
        "/var/www/index.php": {"hash": "ORIGINAL_HASH", "size": 500},
        "/etc/nginx.conf": {"hash": "NGINX_HASH", "size": 300},
        "/var/log/audit.log": {"hash": "LOG_HASH", "size": 1000}
    }
    current = {
        "/var/www/index.php": {"hash": "TAMPERED_HASH", "size": 520},   # MODIFIED
        "/etc/nginx.conf": {"hash": "NGINX_HASH", "size": 300},        # INTACT
        "/var/www/backdoor.php": {"hash": "SHELL_HASH", "size": 250}   # CREATED
        # /var/log/audit.log is missing -> DELETED
    }
    res = compare_file_records(baseline, current)
    assert res["status"] == "success"
    assert res["is_compromised"] is True
    assert res["intact_count"] == 1
    assert res["modified_count"] == 1
    assert res["created_count"] == 1
    assert res["deleted_count"] == 1

def test_get_demo_simulation():
    res_clean = get_demo_simulation("clean")
    assert res_clean["is_compromised"] is False
    assert res_clean["security_score"] == 100

    res_tamper = get_demo_simulation("tamper")
    assert res_tamper["is_compromised"] is True
    assert res_tamper["modified_count"] > 0
    assert res_tamper["created_count"] > 0
    assert res_tamper["deleted_count"] > 0

    res_webshell = get_demo_simulation("webshell")
    assert res_webshell["created_count"] == 1
