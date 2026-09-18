import os
import json

def scan_browser_extensions():
    """Discovers installed extensions across Microsoft Edge and Google Chrome."""
    results = []

    browser_profiles = {
        "Microsoft Edge": os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Extensions"),
        "Google Chrome": os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Extensions")
    }

    for browser_title, root_dir in browser_profiles.items():
        if not os.path.exists(root_dir):
            continue

        try:
            for ext_id in os.listdir(root_dir):
                ext_dir = os.path.join(root_dir, ext_id)
                if not os.path.isdir(ext_dir):
                    continue

                version_folders = [f for f in os.listdir(ext_dir) if os.path.isdir(os.path.join(ext_dir, f))]
                if not version_folders:
                    continue

                active_ver = version_folders[0]
                version_path = os.path.join(ext_dir, active_ver)
                manifest_file = os.path.join(version_path, "manifest.json")

                if os.path.exists(manifest_file):
                    ext_name = ext_id
                    version_num = active_ver

                    try:
                        with open(manifest_file, "r", encoding="utf-8") as m:
                            data = json.load(m)
                            raw_name = data.get("name", ext_id)
                            version_num = data.get("version", active_ver)

                            # Handle localized Chrome string titles
                            if raw_name.startswith("__MSG_"):
                                ext_name = f"{ext_id} (System / Localized)"
                            else:
                                ext_name = raw_name
                    except Exception:
                        pass

                    results.append({
                        "browser": browser_title,
                        "name": ext_name,
                        "version": version_num,
                        "id": ext_id,
                        "path": version_path
                    })
        except Exception:
            continue

    return results
