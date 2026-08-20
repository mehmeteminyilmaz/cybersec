import os
import hashlib
import json
from datetime import datetime

def calculate_string_hash(text: str, algorithm="sha256") -> str:
    hasher = getattr(hashlib, algorithm.lower(), hashlib.sha256)()
    hasher.update(text.encode('utf-8'))
    return hasher.hexdigest()

def calculate_file_hash(filepath: str, algorithm="sha256") -> str:
    hasher = getattr(hashlib, algorithm.lower(), hashlib.sha256)()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(65536):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        return f"Error: {str(e)}"

def compare_file_records(baseline_records: dict, current_records: dict) -> dict:
    """
    baseline_records: { "filepath": { "hash": "...", "size": 123 } }
    current_records:  { "filepath": { "hash": "...", "size": 123 } }
    """
    results = []
    intact_count = 0
    modified_count = 0
    created_count = 0
    deleted_count = 0

    all_paths = set(baseline_records.keys()).union(set(current_records.keys()))

    for path in sorted(all_paths):
        in_baseline = path in baseline_records
        in_current = path in current_records

        if in_baseline and in_current:
            base_hash = baseline_records[path].get("hash", "")
            curr_hash = current_records[path].get("hash", "")
            curr_size = current_records[path].get("size", 0)

            if base_hash.lower() == curr_hash.lower():
                intact_count += 1
                results.append({
                    "file": path,
                    "status": "INTACT",
                    "status_title": "Bütünlük Korundu",
                    "badge_class": "badge-active",
                    "icon": "fas fa-shield-check",
                    "baseline_hash": base_hash,
                    "current_hash": curr_hash,
                    "size": f"{curr_size} B",
                    "detail": "Dosya özeti referans baseline ile tam eşleşiyor."
                })
            else:
                modified_count += 1
                results.append({
                    "file": path,
                    "status": "MODIFIED",
                    "status_title": "Yetkisiz Değişiklik",
                    "badge_class": "badge-danger",
                    "icon": "fas fa-triangle-exclamation",
                    "baseline_hash": base_hash,
                    "current_hash": curr_hash,
                    "size": f"{curr_size} B",
                    "detail": "Kritik uyarı: Dosya içeriği referans durumdan farklı, manipüle edilmiş olabilir!"
                })
        elif in_current and not in_baseline:
            created_count += 1
            curr_hash = current_records[path].get("hash", "")
            curr_size = current_records[path].get("size", 0)
            results.append({
                "file": path,
                "status": "CREATED",
                "status_title": "Yeni Dosya (Şüpheli)",
                "badge_class": "badge-warn",
                "icon": "fas fa-file-circle-exclamation",
                "baseline_hash": "-",
                "current_hash": curr_hash,
                "size": f"{curr_size} B",
                "detail": "Baseline'da bulunmayan yeni dosya eklendi. Olası Web Shell veya yetkisiz script."
            })
        elif in_baseline and not in_current:
            deleted_count += 1
            base_hash = baseline_records[path].get("hash", "")
            results.append({
                "file": path,
                "status": "DELETED",
                "status_title": "Dosya Silindi",
                "badge_class": "badge-warn",
                "icon": "fas fa-file-circle-xmark",
                "baseline_hash": base_hash,
                "current_hash": "-",
                "size": "-",
                "detail": "Baseline'da kayıtlı kritik dosya sistemde bulunamadı. Servis bozulması veya kanıt silme."
            })

    total = len(results)
    security_score = int((intact_count / total) * 100) if total > 0 else 100

    return {
        "status": "success",
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "total_files": total,
        "intact_count": intact_count,
        "modified_count": modified_count,
        "created_count": created_count,
        "deleted_count": deleted_count,
        "security_score": security_score,
        "is_compromised": (modified_count > 0 or created_count > 0 or deleted_count > 0),
        "results": results
    }

def get_demo_simulation(scenario: str = "tamper") -> dict:
    """
    Web UI üzerinden gerçekçi simülasyon senaryoları sunar.
    """
    baseline = {
        "/etc/nginx/nginx.conf": {
            "hash": "4a7d1ed414474e4033ac29ccb8653d9b04856f642456e300fc48b0a9960ff694",
            "size": 1850
        },
        "/var/www/html/index.php": {
            "hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "size": 2400
        },
        "/etc/ssh/sshd_config": {
            "hash": "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9",
            "size": 3210
        },
        "/etc/passwd": {
            "hash": "cd2eb0837c9b4c962c22d2ff8b5441b7b45805887f051d39bf133b5836a04d55",
            "size": 1420
        },
        "/var/log/auth.log": {
            "hash": "5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5",
            "size": 8900
        }
    }

    current = dict(baseline)

    if scenario == "clean":
        pass
    elif scenario == "webshell":
        current["/var/www/html/backdoor_shell.php"] = {
            "hash": "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918",
            "size": 842
        }
    elif scenario == "tamper":
        # nginx.conf ve passwd manipüle edildi, shell eklendi, auth.log silindi
        current["/etc/nginx/nginx.conf"] = {
            "hash": "1111111111111111111111111111111111111111111111111111111111111111",
            "size": 2100
        }
        current["/var/www/html/c99_webshell.php"] = {
            "hash": "9999999999999999999999999999999999999999999999999999999999999999",
            "size": 1540
        }
        if "/var/log/auth.log" in current:
            del current["/var/log/auth.log"]
    elif scenario == "ransomware":
        # Tüm dosyalar şifrelendi
        for k in list(current.keys()):
            current[k] = {
                "hash": hashlib.sha256(f"encrypted_{k}".encode()).hexdigest(),
                "size": current[k]["size"] + 64
            }
        current["README_DECRYPT.txt"] = {
            "hash": "7777777777777777777777777777777777777777777777777777777777777777",
            "size": 420
        }

    return compare_file_records(baseline, current)
