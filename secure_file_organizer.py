import os
import shutil
import hashlib

FILE_TYPES = {
    "Images": [".jpg", ".png", ".jpeg"],
    "Documents": [".pdf", ".docx", ".txt"],
    "Videos": [".mp4", ".mkv"],
    "Music": [".mp3", ".wav"]
}

SUSPICIOUS_EXTENSIONS = [".exe", ".bat", ".vbs", ".ps1"]

folder_path = input("Enter folder path to organize securely: ").strip()

if not os.path.exists(folder_path):
    print("Invalid path!")
    exit()

log_path = os.path.join(folder_path, "security_log.txt")
hashes_seen = set()

def get_file_hash(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for block in iter(lambda: f.read(4096), b""):
            sha256.update(block)
    return sha256.hexdigest()

def get_unique_name(folder, filename):
    name, ext = os.path.splitext(filename)
    count = 1
    new_name = filename
    while os.path.exists(os.path.join(folder, new_name)):
        new_name = f"{name}({count}){ext}"
        count += 1
    return new_name

with open(log_path, "a") as log:
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)

        if os.path.isfile(file_path) and file != "security_log.txt":
            file_ext = os.path.splitext(file)[1].lower()
            file_hash = get_file_hash(file_path)

            # Detect duplicate content
            if file_hash in hashes_seen:
                log.write(f"DUPLICATE FILE: {file} | HASH: {file_hash}\n")
            else:
                hashes_seen.add(file_hash)

            # Detect suspicious files
            if file_ext in SUSPICIOUS_EXTENSIONS:
                quarantine = os.path.join(folder_path, "Quarantine")
                os.makedirs(quarantine, exist_ok=True)

                safe_name = get_unique_name(quarantine, file)
                shutil.move(file_path, os.path.join(quarantine, safe_name))

                log.write(f"SUSPICIOUS FILE MOVED: {file} -> Quarantine | HASH: {file_hash}\n")
                continue

            moved = False
            for folder, extensions in FILE_TYPES.items():
                if file_ext in extensions:
                    dest = os.path.join(folder_path, folder)
                    os.makedirs(dest, exist_ok=True)

                    safe_name = get_unique_name(dest, file)
                    shutil.move(file_path, os.path.join(dest, safe_name))

                    log.write(f"MOVED: {file} -> {folder} | HASH: {file_hash}\n")
                    moved = True
                    break

            if not moved:
                other = os.path.join(folder_path, "Others")
                os.makedirs(other, exist_ok=True)

                safe_name = get_unique_name(other, file)
                shutil.move(file_path, os.path.join(other, safe_name))

                log.write(f"MOVED: {file} -> Others | HASH: {file_hash}\n")

print("\nSecure file organization completed.")
print("Security log created: security_log.txt")
