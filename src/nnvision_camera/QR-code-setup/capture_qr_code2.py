import cv2
import numpy as np
import subprocess
from pyzbar.pyzbar import decode

width, height = 1920, 1080
frame_size = width * height * 3 // 2  # taille YUV420p

cmd = [
    'libcamera-vid',
    '--codec', 'yuv420',  # flux YUV brut
    '-t', '0',
    '--width', str(width),
    '--height', str(height),
    '--framerate', '2',
    '--inline',
    '-o', '-',  # stdout
]

process = subprocess.Popen(cmd, stdout=subprocess.PIPE)

print("Capture YUV directe démarrée (Ctrl+C pour arrêter).")

try:
    while True:
        # Lire une frame complète en YUV
        yuv_frame = process.stdout.read(frame_size)
        if len(yuv_frame) < frame_size:
            continue

        # Conversion YUV → RGB (très rapide)
        yuv = np.frombuffer(yuv_frame, dtype=np.uint8).reshape((height * 3 // 2, width))
        frame = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_I420)

        # Décode QR code
        decoded_objs = decode(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        for obj in decoded_objs:
            print(f"QR code détecté : {obj.data.decode('utf-8')}")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Interrompu par utilisateur.")

finally:
    process.terminate()
    cv2.destroyAllWindows()

