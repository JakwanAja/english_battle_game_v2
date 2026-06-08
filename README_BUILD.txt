====================================================
  CARA BUILD KE .EXE (Windows)
====================================================

SYARAT:
  - Python 3.10 / 3.11 / 3.12 terinstall
    Download: https://www.python.org/downloads/
    (centang "Add Python to PATH" saat install!)

LANGKAH:
  1. Ekstrak folder ini ke mana saja
  2. Double-klik file: BUILD_EXE.bat
  3. Tunggu proses selesai (~1-3 menit)
  4. File .exe ada di: dist\EnglishBattlePets.exe

ALTERNATIF (manual via Command Prompt):
  > pip install pygame pyinstaller
  > pyinstaller --onefile --windowed --name "EnglishBattlePets" --add-data "assets;assets" main.py
  
CATATAN:
  - --onefile  = satu file .exe tunggal (praktis dibawa)
  - --windowed = tidak muncul console/terminal saat game jalan
  - Ukuran .exe sekitar 20-30 MB (sudah include semua asset)
  - File .exe hanya jalan di Windows (tidak perlu Python terinstall)

TROUBLESHOOT:
  - Jika antivirus blokir .exe: itu false positive, wajar untuk
    file yang di-bundle PyInstaller. Tambahkan ke whitelist.
  - Jika muncul error "pygame not found": jalankan lagi BUILD_EXE.bat
  - Jika layar hitam saat dijalankan: cek folder dist\ ada subfolder
    _internal\ dengan file assets di dalamnya

====================================================
