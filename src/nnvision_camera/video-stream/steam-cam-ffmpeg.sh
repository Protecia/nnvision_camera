libcamera-vid -t 0 --inline --width 1296  --height 972  --framerate 5  -o - | \
 ffmpeg -i pipe:0 -c copy -f rtsp rtsps://mtx.protecia.net:8555/protecia
