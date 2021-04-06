# pisdr_hat

This is a budget Raspberry Pi SDR project by Yuan Wang (BG3MDO)

The aim is to make a cheaper PI HAT to do HF/6m band SDR TRX, while using Raspberry Pi to do the digital signal processing (DSP).

Currently, it uses Quisk to process signals.

I have Quisk configuration files (Python scripts) attached.

Set up:
  - Raspberray OS installed
  - Raspberray Pi 4 with PI SDR HAT pluged in - the PCB
  - Install Quisk, and setup using the attached configuration Python scrips
  - Extra CM108 USB sound card for speaker and micphone

Sound card configurations:

Uninstall Pluseaudio, and fallback to alsa sound layer using 
sudo apt remove pluseaudio

/boot/config.txt adding the following statement to enable i2c/i2s/i2s-mmap and wm8731 device tree for Linux

dtparam=i2c_arm=on
dtparam=i2s=on
dtoverlay=i2s-mmap
dtoverlay=audioinjector-wm8731-audio

You might use alsamixer to setting wm8731, enable input and adjust gains.

To do list:
  - Fix Quisk frequency offset issue, this is due to sound card crystal osc is not accurate.
  - I Q need to be balanced, new HW design?
