libcamera-vid -t 0 --awbgains 0,0 --saturation 0 --mode 1920:1080:10:P  --inline  --framerate 5  -o - | \
 ffmpeg -i pipe:0 -c copy -f rtsp rtsps://mtx.protecia.net:8555/protecia