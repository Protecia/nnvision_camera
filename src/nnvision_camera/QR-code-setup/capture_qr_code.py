import subprocess
import time
import glob
import os
from PIL import Image
from pyzbar.pyzbar import decode

IMAGES_DIR = "Pictures"
MAX_IMAGES = 10

# Crée le dossier s'il n'existe pas
os.makedirs(IMAGES_DIR, exist_ok=True)

# Lancement de libcamera-vid + ffmpeg en pipe pour extraire une image/sec
ffmpeg_cmd = (
    f"libcamera-vid -t 0 --width 1280 --height 720 --framerate 5 --inline -o - | "
    f"ffmpeg -hide_banner -loglevel error -i pipe:0 -vf fps=1 {IMAGES_DIR}/image_%04d.jpg"
)

# Lance ffmpeg dans un subprocess (bash pour gérer le pipe)
ffmpeg_proc = subprocess.Popen(ffmpeg_cmd, shell=True)

print("Capture en cours... (Ctrl+C pour arrêter)")

try:
    while True:
        # Liste les images par ordre de création (la plus récente en premier)
        images = sorted(
            glob.glob(os.path.join(IMAGES_DIR, "image_*.jpg")),
            key=os.path.getmtime,
            reverse=True
        )
        if images:
            latest_image = images[0]
            print(f"Image la plus récente : {latest_image}")

            # Exemple de traitement : décoder un QR code (si besoin)
            try:
                img = Image.open(latest_image)
                decoded = decode(img)
                for obj in decoded:
                    print(f"QR Code détecté : {obj.data.decode('utf-8')}")
            except Exception as e:
                print(f"Erreur lecture/analyse image : {e}")

            # Supprime les images plus anciennes pour ne garder que les MAX_IMAGES plus récentes
            for old_img in images[MAX_IMAGES:]:
                os.remove(old_img)

        time.sleep(1)

except KeyboardInterrupt:
    print("Arrêt demandé. Fermeture du processus ffmpeg...")
    ffmpeg_proc.terminate()
    ffmpeg_proc.wait()
    print("Terminé proprement.")

