import winreg
import psutil

KNOWN_VPN_KEYWORDS = [
    "vpn", "wireguard", "openvpn", "cisco anyconnect", 
    "proton", "nordvpn", "zerotier", "tailscale", "forticlient",
    "surfshark", "expressvpn", "mullvad", "windscribe"
]

def scan_installed_vpn_clients():
    """Scans Windows Uninstall registries for installed VPN desktop software."""
    installed = []
    reg_paths = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Uninstall")
    ]

    for root_hkey, path in reg_paths:
        try:
            with winreg.OpenKey(root_hkey, path) as base_key:
                num_subkeys = winreg.QueryInfoKey(base_key)[0]
                for i in range(num_subkeys):
                    try:
                        subkey_name = winreg.EnumKey(base_key, i)
                        with winreg.OpenKey(base_key, subkey_name) as app_key:
                            try:
                                name, _ = winreg.QueryValueEx(app_key, "DisplayName")
                            except FileNotFoundError:
                                continue

                            install_path = ""
                            try:
                                install_path, _ = winreg.QueryValueEx(app_key, "InstallLocation")
                            except FileNotFoundError:
                                pass

                            if any(kw in name.lower() for kw in KNOWN_VPN_KEYWORDS):
                                installed.append({
                                    "name": str(name),
                                    "location": str(install_path) if install_path else f"Registry: {subkey_name}"
                                })
                    except (FileNotFoundError, OSError):
                        continue
        except (FileNotFoundError, OSError):
            continue

    # Deduplicate entries by name
    unique_entries = {item["name"]: item for item in installed}
    return list(unique_entries.values())


def scan_active_network_adapters():
    """Detects virtual network interfaces used by VPN tunnels."""
    adapters = []
    stats = psutil.net_if_stats()

    for iface_name, stat in stats.items():
        clean_name = iface_name.lower()
        is_virtual = any(kw in clean_name for kw in ["tap", "tun", "wireguard", "wintun", "vpn"])
        if is_virtual:
            adapters.append({
                "interface": iface_name,
                "status": "Active (Up)" if stat.isup else "Disconnected",
                "speed": f"{stat.speed} Mbps" if stat.speed > 0 else "Virtual Tunnel"
            })

    return adapters
