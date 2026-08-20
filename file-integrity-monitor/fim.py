import os
import hashlib
import json
import argparse
from datetime import datetime

def calculate_string_hash(text: str, algorithm="sha256") -> str:
    """Metin girdisinin belirtilen algoritma ile kriptografik özetini hesaplar."""
    hasher = getattr(hashlib, algorithm.lower(), hashlib.sha256)()
    hasher.update(text.encode('utf-8'))
    return hasher.hexdigest()

def calculate_file_hash(filepath, algorithm="sha256"):
    """Dosyanın belirtilen algoritma ile kriptografik özetini hesaplar."""
    hasher = getattr(hashlib, algorithm.lower(), hashlib.sha256)()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(65536):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        return f"Error: {str(e)}"

def compare_file_records(baseline_records: dict, current_records: dict) -> dict:
    """İki sözlük halindeki dosya hash kayıtlarını kıyaslar."""
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
                    "baseline_hash": base_hash,
                    "current_hash": curr_hash,
                    "size": f"{curr_size} B"
                })
            else:
                modified_count += 1
                results.append({
                    "file": path,
                    "status": "MODIFIED",
                    "status_title": "Yetkisiz Değişiklik",
                    "badge_class": "badge-danger",
                    "baseline_hash": base_hash,
                    "current_hash": curr_hash,
                    "size": f"{curr_size} B"
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
                "baseline_hash": "-",
                "current_hash": curr_hash,
                "size": f"{curr_size} B"
            })
        elif in_baseline and not in_current:
            deleted_count += 1
            base_hash = baseline_records[path].get("hash", "")
            results.append({
                "file": path,
                "status": "DELETED",
                "status_title": "Dosya Silindi",
                "badge_class": "badge-warn",
                "baseline_hash": base_hash,
                "current_hash": "-",
                "size": "-"
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
    baseline = {
        "/etc/nginx/nginx.conf": {"hash": "4a7d1ed414474e4033ac29ccb8653d9b04856f642456e300fc48b0a9960ff694", "size": 1850},
        "/var/www/html/index.php": {"hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "size": 2400},
        "/etc/ssh/sshd_config": {"hash": "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9", "size": 3210},
        "/etc/passwd": {"hash": "cd2eb0837c9b4c962c22d2ff8b5441b7b45805887f051d39bf133b5836a04d55", "size": 1420},
        "/var/log/auth.log": {"hash": "5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5", "size": 8900}
    }
    current = dict(baseline)
    if scenario == "clean":
        pass
    elif scenario == "webshell":
        current["/var/www/html/backdoor_shell.php"] = {"hash": "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918", "size": 842}
    elif scenario == "tamper":
        current["/etc/nginx/nginx.conf"] = {"hash": "1111111111111111111111111111111111111111111111111111111111111111", "size": 2100}
        current["/var/www/html/c99_webshell.php"] = {"hash": "9999999999999999999999999999999999999999999999999999999999999999", "size": 1540}
        if "/var/log/auth.log" in current:
            del current["/var/log/auth.log"]
    return compare_file_records(baseline, current)

def create_baseline(directory, algorithm="sha256"):
    """Belirtilen dizindeki tüm dosyaların hash'lerini çıkararak referans baseline üretir."""
    baseline = {}
    if not os.path.exists(directory):
        return baseline

    for root, _, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, directory)
            file_hash = calculate_file_hash(full_path, algorithm)
            file_size = os.path.getsize(full_path) if os.path.exists(full_path) else 0
            
            baseline[rel_path] = {
                "hash": file_hash,
                "size": file_size,
                "algorithm": algorithm.upper(),
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
    return baseline

def verify_integrity(directory, baseline):
    """Mevcut dizini baseline ile kıyaslayarak değişiklikleri raporlar."""
    results = []
    current_files = set()

    # 1. Mevcut dosyaları kontrol et (INTACT, MODIFIED, CREATED)
    if os.path.exists(directory):
        for root, _, files in os.walk(directory):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, directory)
                current_files.add(rel_path)

                current_hash = calculate_file_hash(full_path)
                current_size = os.path.getsize(full_path) if os.path.exists(full_path) else 0

                if rel_path not in baseline:
                    results.append({
                        "file": rel_path,
                        "status": "CREATED",
                        "status_text": "YENİ DOSYA (Şüpheli / Web Shell Olabilir)",
                        "badge_class": "badge-warn",
                        "baseline_hash": "-",
                        "current_hash": current_hash,
                        "size": current_size
                    })
                else:
                    base_entry = baseline[rel_path]
                    if current_hash == base_entry["hash"]:
                        results.append({
                            "file": rel_path,
                            "status": "INTACT",
                            "status_text": "GÜVENLİ (Değişiklik Yok)",
                            "badge_class": "badge-active",
                            "baseline_hash": base_entry["hash"],
                            "current_hash": current_hash,
                            "size": current_size
                        })
                    else:
                        results.append({
                            "file": rel_path,
                            "status": "MODIFIED",
                            "status_text": "DEĞİŞTİRİLDİ (Yetkisiz Müdahale)",
                            "badge_class": "badge-danger",
                            "baseline_hash": base_entry["hash"],
                            "current_hash": current_hash,
                            "size": current_size
                        })

    # 2. Silinen dosyaları kontrol et (DELETED)
    for rel_path, base_entry in baseline.items():
        if rel_path not in current_files:
            results.append({
                "file": rel_path,
                "status": "DELETED",
                "status_text": "SİLİNDİ (Kritik Dosya Kayıp)",
                "badge_class": "badge-warn",
                "baseline_hash": base_entry["hash"],
                "current_hash": "-",
                "size": base_entry.get("size", 0)
            })

    return results

def main():
    parser = argparse.ArgumentParser(description="CyberSec File Integrity Monitor (FIM) CLI")
    parser.add_argument("-d", "--dir", required=True, help="Hedef dizin")
    parser.add_argument("-b", "--baseline", help="Baseline JSON dosya yolu (Kayıt veya Okuma)")
    parser.add_argument("--create", action="store_true", help="Yeni baseline oluştur ve kaydet")
    parser.add_argument("--verify", action="store_true", help="Mevcut dizini baseline ile doğrula")

    args = parser.parse_args()

    if args.create:
        baseline = create_baseline(args.dir)
        output_file = args.baseline or "baseline.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(baseline, f, indent=4)
        print(f"[+] Baseline başarıyla oluşturuldu ({len(baseline)} dosya): {output_file}")
    elif args.verify:
        if not args.baseline or not os.path.exists(args.baseline):
            print("[-] Hata: Doğrulama için geçerli bir baseline JSON dosyası belirtmelisiniz (-b <dosya>)")
            return
        with open(args.baseline, 'r', encoding='utf-8') as f:
            baseline = json.load(f)
        results = verify_integrity(args.dir, baseline)
        print(f"\n[+] Bütünlük Kontrol Raporu ({len(results)} dosya):")
        for res in results:
            print(f"  [{res['status']}] {res['file']} -> {res['status_text']}")

if __name__ == "__main__":
    main()
