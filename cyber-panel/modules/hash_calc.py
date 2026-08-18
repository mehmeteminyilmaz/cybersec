import hashlib
import re

def generate_all_hashes(text: str, salt: str = "") -> dict:
    if not text:
        text = ""

    full_text = text + salt
    bytes_data = full_text.encode('utf-8')

    try:
        ntlm_hash = hashlib.new('md4', text.encode('utf-16le')).hexdigest()
    except Exception:
        ntlm_hash = "Desteklenmiyor"

    results = {
        "MD5": {
            "hash": hashlib.md5(bytes_data).hexdigest(),
            "bit_length": 128,
            "security": "Zayıf / Kırılmış (Eski)",
            "badge_class": "badge-warn"
        },
        "SHA-1": {
            "hash": hashlib.sha1(bytes_data).hexdigest(),
            "bit_length": 160,
            "security": "Zayıf / Eski",
            "badge_class": "badge-warn"
        },
        "SHA-224": {
            "hash": hashlib.sha224(bytes_data).hexdigest(),
            "bit_length": 224,
            "security": "Orta Güvenlik",
            "badge_class": "badge-active"
        },
        "SHA-256": {
            "hash": hashlib.sha256(bytes_data).hexdigest(),
            "bit_length": 256,
            "security": "Endüstri Standardı (Güçlü)",
            "badge_class": "badge-active"
        },
        "SHA-384": {
            "hash": hashlib.sha384(bytes_data).hexdigest(),
            "bit_length": 384,
            "security": "Yüksek Güvenlik",
            "badge_class": "badge-active"
        },
        "SHA-512": {
            "hash": hashlib.sha512(bytes_data).hexdigest(),
            "bit_length": 512,
            "security": "Çok Yüksek Güvenlik",
            "badge_class": "badge-active"
        },
        "NTLM": {
            "hash": ntlm_hash,
            "bit_length": 128,
            "security": "Windows SAM Parola Formatı",
            "badge_class": "badge-warn"
        }
    }

    return {
        "input_text": text,
        "salt": salt,
        "hashes": results
    }

def identify_hash_type(hash_str: str) -> dict:
    clean_hash = hash_str.strip().lower()
    
    if not clean_hash:
        return {
            "status": "error",
            "message": "Lütfen geçerli bir hash dizisi girin."
        }

    if clean_hash.startswith(("$2a$", "$2b$", "$2y$")):
        return {
            "status": "success",
            "hash": clean_hash,
            "possible_types": ["bcrypt"],
            "confidence": "Yüksek (%100)",
            "bit_length": "Değişken (Blowfish)",
            "security_note": "Parola hashleme için son derece güvenli ve yavaş algoritma."
        }
    elif clean_hash.startswith("$6$"):
        return {
            "status": "success",
            "hash": clean_hash,
            "possible_types": ["SHA-512 Crypt (Linux shadow)"],
            "confidence": "Yüksek (%100)",
            "bit_length": 512,
            "security_note": "Linux parola saklama standardı."
        }
    elif clean_hash.startswith("$5$"):
        return {
            "status": "success",
            "hash": clean_hash,
            "possible_types": ["SHA-256 Crypt (Linux shadow)"],
            "confidence": "Yüksek (%100)",
            "bit_length": 256,
            "security_note": "Linux parola saklama formatı."
        }

    if not re.match(r'^[a-fA-F0-9]+$', clean_hash):
        return {
            "status": "error",
            "message": "Girilen metin geçerli bir Hexadecimal veya bilinen hash formatında değil."
        }

    length = len(clean_hash)
    possible_types = []
    bit_length = length * 4
    note = ""

    if length == 32:
        possible_types = ["MD5", "NTLM", "MD4", "LM"]
        note = "En olası: MD5 veya Windows NTLM hash'i. Zayıf ve kırılabilir."
    elif length == 40:
        possible_types = ["SHA-1", "RIPEMD-160", "Tiger-160"]
        note = "En olası: SHA-1. Eski protokollerde sıklıkla kullanılır."
    elif length == 56:
        possible_types = ["SHA-224", "SHA3-224"]
        note = "SHA-224 ailesi."
    elif length == 64:
        possible_types = ["SHA-256", "SHA3-256", "GOST R 34.11-94"]
        note = "En olası: SHA-256. Günümüz web/kripto endüstri standardı."
    elif length == 96:
        possible_types = ["SHA-384", "SHA3-384"]
        note = "SHA-384 yüksek güvenlikli hash."
    elif length == 128:
        possible_types = ["SHA-512", "SHA3-512", "Whirlpool"]
        note = "En olası: SHA-512. Yüksek güvenlikli kriptografik özet."
    else:
        possible_types = [f"Özel Format ({length} karakter / {bit_length}-bit)"]
        note = "Standart dışı hash uzunluğu."

    return {
        "status": "success",
        "hash": clean_hash,
        "length": length,
        "bit_length": bit_length,
        "possible_types": possible_types,
        "confidence": "Yüksek" if possible_types else "Düşük",
        "security_note": note
    }

def verify_hash_match(plain_text: str, target_hash: str, salt: str = "") -> dict:
    clean_target = target_hash.strip().lower()
    generated = generate_all_hashes(plain_text, salt)["hashes"]
    
    matched_algo = None
    for algo_name, algo_data in generated.items():
        if algo_data["hash"].lower() == clean_target:
            matched_algo = algo_name
            break

    return {
        "is_match": matched_algo is not None,
        "matched_algorithm": matched_algo or "Eşleşme Bulunamadı",
        "input_text": plain_text,
        "target_hash": target_hash
    }
