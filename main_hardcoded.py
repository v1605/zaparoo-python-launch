import sys
from zaparoo_launch_api import ZaparooLaunchApi

websocket_url = "ws://mister.local:7497"


def main():
    if len(sys.argv) != 2:
        print("Usage: python launch_rom.py <script>")
        sys.exit(1)

    rom_path = sys.argv[1]

    zaparoo_api = ZaparooLaunchApi(websocket_url)

    result_code = zaparoo_api.launch(content=rom_path)

    if result_code == 0:
        print(f"Successfully launched script: {rom_path}")
    else:
        print(f"Failed to launch script: {rom_path} (Error code: {result_code})")


if __name__ == "__main__":
    main()
