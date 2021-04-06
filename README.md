# pisdr_hat

This is a budget Raspberry Pi SDR project by Yuan Wang (BG3MDO)

The aim is to make a cheaper PI HAT to do HF/6m band SDR TRX, while using Raspberry Pi to do the digital signal processing (DSP).

Current stage, full TX RX working well.

Set up:
  - Raspberray Pi with PI SDR HAT pluged in
  - Extra CM108 USB sound card for speaker and micphone

To do list:
  - Fix Quisk frequency offset issue, this is due to sound card crystal osc is not accurate.
  - I Q need to be balanced, new HW design?
