# NNVISION CAMERA

These camera ar designed to be very simple to manage. Plug and play using QR code.

They simply send H264 video flux to a server in a secure way from a wifi network.

They can be setup using a simple QR code containing:

- SSID and password to connect to the wifi.
- Url to connect to the media server
- Password to reach the media server

And that's it !

# RPI setup
RPi zero 2 W are used to manage the camera

Use rpi pi imager to make the ssd. 

# QR code setup
Each RPI need a SHA private key and a token to connect to the server.
These credential are not setup they are obtained from the server.

All you need is to setup the token to connect to the api of the server.
This is made using a QR code with the credential.
The project nnvision-camera-rpi-setup is made to setup the RPI. 

