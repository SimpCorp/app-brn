import os
from pathlib import Path
from PyQt6.QtCore import QThread, pyqtSignal

TARGET_MEDIA_EXTS = {".mp3", ".mp4", ".mkv", ".m4a", ".3gp"}
PDF_SIZE_THRESHOLD_BYTES = 200 * 1024 * 1024  # 200 MB

class FileAuditWorker(QThread):
    file_discovered = pyqtSignal(dict)
    scan_finished = pyqtSignal(int)

    def __init__(self, target_folders=None):
        super().__init__()
        if target_folders is None:
            # Default to standard user profile folders where files accumulate
            user_profile = Path(os.environ.get("USERPROFILE", "C:\\Users\\Default"))
            self.target_folders = [
                user_profile / "Downloads",
                user_profile / "Documents",
                user_profile / "Desktop",
                user_profile / "Videos",
                user_profile / "Music",
            ]
        else:
            self.target_folders = target_folders

    def run(self):
        total_found = 0
        for base_folder in self.target_folders:
            if not base_folder.exists():
                continue

            # Traverse directory safely handling permission exceptions
            for root, _, files in os.walk(base_folder, followlinks=False):
                for filename in files:
                    file_path = os.path.join(root, filename)
                    try:
                        file_stat = os.stat(file_path)
                        file_size = file_stat.st_size
                        ext = Path(filename).suffix.lower()

                        is_media = ext in TARGET_MEDIA_EXTS
                        is_large_pdf = (ext == ".pdf" and file_size >= PDF_SIZE_THRESHOLD_BYTES)

                        if is_media or is_large_pdf:
                            size_mb = file_size / (1024 * 1024)
                            item_type = "Large PDF Document" if is_large_pdf else f"Media ({ext.upper().replace('.', '')})"
                            
                            self.file_discovered.emit({
                                "name": filename,
                                "type": item_type,
                                "size": f"{size_mb:.2f} MB",
                                "path": file_path
                            })
                            total_found += 1
                    except (PermissionError, FileNotFoundError, OSError):
                        continue

        self.scan_finished.emit(total_found)
