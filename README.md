# secure_file_organizer
# Secure File Organizer with Malware Detection

A Python-based file organizer that categorizes files, detects duplicates using SHA-256 hashing, and quarantines suspicious executable files for security.

## Features
- Automatically organizes files into folders (Images, Documents, Videos, Music)
- Detects duplicate files using SHA-256 hash comparison
- Identifies suspicious files (.exe, .bat, .vbs, .ps1)
- Moves suspicious files to a Quarantine folder
- Maintains a detailed security log
- Prevents filename overwriting using smart renaming

## Technologies Used
- Python 3
- os
- shutil
- hashlib

## How It Works
1. User provides a folder path
2. Files are scanned securely
3. Duplicates are detected via hashing
4. Suspicious files are quarantined
5. All actions are logged

## How to Run
```bash
python secure_file_organizer.py
