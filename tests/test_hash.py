import sys
import os
import pytest

# hash-calculator dizinini sys.path'e ekleyelim
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'hash-calculator')))

from hash_calc import (
    generate_all_hashes,
    identify_hash_type,
    verify_hash_match
)

def test_generate_all_hashes():
    res = generate_all_hashes("password123")
    assert "hashes" in res
    hashes = res["hashes"]
    
    # MD5 hash of "password123" is 482c811da5d5b4bc6d497ffa98491e38
    assert hashes["MD5"]["hash"].lower() == "482c811da5d5b4bc6d497ffa98491e38"
    
    # SHA-256 hash of "password123" is ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f
    assert hashes["SHA-256"]["hash"].lower() == "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f"

def test_identify_hash_type_md5():
    res = identify_hash_type("482c811da5d5b4bc6d497ffa98491e38")
    assert res["status"] == "success"
    assert "MD5" in res["possible_types"]
    assert res["length"] == 32

def test_identify_hash_type_sha256():
    res = identify_hash_type("ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f")
    assert res["status"] == "success"
    assert "SHA-256" in res["possible_types"]
    assert res["length"] == 64

def test_identify_hash_type_bcrypt():
    res = identify_hash_type("$2b$12$e8N8Vwz.YV34Wz/14gXJ8O314wZ3X7Y2Z3X4Y5Z6X7Y8Z9X0Y1Z2")
    assert res["status"] == "success"
    assert "bcrypt" in res["possible_types"]

def test_verify_hash_match():
    target_sha256 = "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f"
    res = verify_hash_match("password123", target_sha256)
    assert res["is_match"] is True
    assert res["matched_algorithm"] == "SHA-256"
