# pisdr_hat

This is a budget Raspberry Pi SDR project by Yuan Wang (BG3MDO)

2021 Easter holiday project

The aim is to make a cheaper PI HAT to do HF/6m band SDR TRX, while using Raspberry Pi to do the digital signal processing (DSP).

Frequency range: 3.2MHz to 58MHz, in this range, Si5351 can produce good 90-degree I Q signals. It can go down to 500k-1.5MHz where is used to receive MW band radios - VCO phase will not meet 90 degree, but it is okay for demod AM signals. 

Currently, it uses Quisk to process signals.

I have Quisk configuration files (Python scripts) attached.

Set up:
  - Raspberray OS installed
  - Raspberray Pi 4 with PI SDR HAT pluged in - the PCB
  - Install Quisk, and setup using the attached configuration Python scrips
  - Extra CM108 USB sound card for speaker and micphone

Quisk install can be as easy as using:

sudo pip3 install quisk

Quisk uses wxpython, you might need to install the following to compile wxpython:

sudo apt install Csudo apt install libjpeg-dev libtiff5-dev libnotify-dev libgtk2.0-dev libgtk-3-dev libsdl1.2-dev libgstreamer-plugins-base0.10-dev libwebkitgtk-dev freeglut3 freeglut3-dev

Then:

sudo pip3 install wxpython

you also need this:

sudo apt-get install libfftw3-dev

Sound card configurations:

Uninstall Pluseaudio, and fallback to alsa sound layer using 
sudo apt remove pluseaudio

/boot/config.txt adding the following statement to enable i2c/i2s/i2s-mmap and wm8731 device tree for Linux

dtparam=i2c_arm=on
dtparam=i2s=on
dtoverlay=i2s-mmap
dtoverlay=audioinjector-wm8731-audio

You might use alsamixer to setting wm8731, enable input and adjust gains. Max. bandwidth is 96K.

To do list:
  - Fix Quisk frequency offset issue, this is due to sound card crystal osc is not accurate.
  - I Q need to be balanced, new HW design?
  - Modify Linux kernel to overclock audio codec to do more bandwidth?
  - Adding RF gain stage? or ATT stage?
  - Adding VHF/UHF RX by placing a TV dongle silicon tuner - still using I2C bus to control?
  - Adding VHF/UHF TX by adding AX5043/ADF7021 to produce a pure carrier, or maybe ADF5351? and a mixer, for example SA612, to do upconverter?

More to follow, many thanks, DE BG3MDO
