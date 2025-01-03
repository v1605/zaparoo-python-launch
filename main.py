import sys
from zaparoo_launch_api import ZaparooLaunchApi


def main():
    if len(sys.argv) != 3:
        print("Usage: python launch_rom.py <websocket_url> <script>")
        sys.exit(1)

    websocket_url = sys.argv[1]
    rom_path = sys.argv[2]

    zaparoo_api = ZaparooLaunchApi(websocket_url)

    result_code = zaparoo_api.launch(content=rom_path)

    if result_code == 0:
        print(f"Successfully launched script: {rom_path}")
    else:
        print(f"Failed to launch script: {rom_path} (Error code: {result_code})")


if __name__ == "__main__":
    main()