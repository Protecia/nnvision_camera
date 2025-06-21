from QR-code-setup import capture_qr_code
import json
import requests


def load_config():
    with open('/home/protecia/config.json', 'r') as file:
        config = json.load(file)
        return config

def main():
    # tente de faire un ping serveur
    # li le json de config
    try:
        config = load_config()
        requests.get(f"https://{config['server_host']}/ping")
    except:
        # get the gr code

    # si erreur, attend un QR code
    print("Hello depuis mon script !")


if __name__ == "__main__":
    main()
