# make a video from cam
libcamera-vid -t 0 --inline --width 640 --height 480 --framerate 15  -o - | ffmpeg -i pipe:0 -c copy video2.mp4

# test camera
libcamera-vid --list-cameras

# Record a 1s video
libcamera-vid -t 10000 -o test.h264

# record an image
libcamera-still  -o image.jpg
libcamera-jpeg -o test.jpg
libcamera-still --mode 2592:1944:10:P -o image.jpg
libcamera-still --mode 640:480:10:P -o image.jpg


# record in IR mode
libcamera-still --awbgains 0,0 --saturation 0 -t 2000 -o image.jpg
libcamera-vid --awbgains 0,0 --saturation 0 -t 5000 --output ir_video.h264

# ------------------------------  configure rpi on the right sensor
sudo nano /boot/firmware/config.txt
#Find the line: camera_auto_detect=1, update it to:
camera_auto_detect=0
#Find the line: [all], add the following item under it:
dtoverlay=ov5647
#Save and reboot.

# Change resolution
libcamera-vid --mode 640:480:10:P -t 10000 -o video.h264
libcamera-vid --mode 2592:1944:10:P -t 10000 -o video.h264

# -------------------------------------------  memory CMA
grep -i cma /proc/meminfo
dmesg | grep -i cma
# to change CMA size add to /boot/firmware/config.txt
dtoverlay=cma,cma-96

# ---------------------------------------------- memory GPU
vcgencmd get_mem arm && vcgencmd get_mem gpu
# to change GPU memory add to /boot/firmware/config.txt
gpu_mem=128

# some documentation from arducam
https://docs.arducam.com/Raspberry-Pi-Camera/Native-camera/5MP-OV5647/#hardware-connection