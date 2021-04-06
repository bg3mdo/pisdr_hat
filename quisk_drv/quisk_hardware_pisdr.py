# This is a testing only Python script by Yuan Wang (BG3MDO)
# The script adding supports to Quisk for PISDR HAT
# 5 April 2021, email: bg3mdo@gmail.com
# Further optimisation is needed

from __future__ import absolute_import
# Please do not change this hardware control module for Quisk.
# This hardware module is for receivers with a fixed VFO, such as
# the SoftRock.  Change your VFO frequency below.

# If you want to use this hardware module, specify it in quisk_conf.py.
# import quisk_hardware_fixed as quisk_hardware
# See quisk_hardware_model.py for documentation.

from quisk_hardware_model import Hardware as BaseHardware
from pisdr.si5351_drv import Si5351Drv
import RPi.GPIO as GPIO


class Hardware(BaseHardware):
  def __init__(self, app, conf):
    BaseHardware.__init__(self, app, conf)
    self.debug = 1
    self.si5351 = Si5351Drv()
    self.xtalFreq = 25000000
    print("Init/Using PISDR HAT on RPi, by Yuan Wang (BG3MDO)")
    self.vfo = 0
    self.is_tx = 0

  def open(self):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(27, GPIO.OUT)
    GPIO.output(27, GPIO.HIGH)
    if self.debug == 1:
        print("Now setting PISDR HAT into RX mode")
  
  def close(self):
    pass

  def HeartBeat(self):
    pass

  def ChangeRXTX(self, is_tx):
    if is_tx:
      GPIO.setmode(GPIO.BCM)
      GPIO.setwarnings(False)
      GPIO.setup(27, GPIO.OUT)
      GPIO.output(27, GPIO.LOW)
      if self.debug == 1:
        print("PISDR HAT switchs to TX mode")
    else:
      GPIO.setmode(GPIO.BCM)
      GPIO.setwarnings(False)
      GPIO.setup(27, GPIO.OUT)
      GPIO.output(27, GPIO.HIGH)

  def OnButtonPTT(self, event):
    if self.is_tx == 0:
      self.is_tx = 1
    else:
      self.is_tx = 0
    self.ChangeRXTX(self.is_tx)

  def ChangeFrequency(self, tune, vfo, source='', band='', event=None):
    # Change and return the tuning and VFO frequency.  See quisk_hardware_model.py.
    if self.vfo != vfo:
      self.vfo = vfo

      if vfo >= 8000000:
        div = 900000000 // vfo
      if vfo < 8000000:
        div = 400000000 // vfo
      if div % 2:
        div = div - 1
      pllFreq = div * vfo
      pllMult = pllFreq // self.xtalFreq
      if self.debug == 1:
          print("Yuan Wang (BG3MDO) is requested to change freq:")
        print("Expected VFO Freq: " + str(vfo))
        print("Divider: " + str(div))
        print("Expected PLL Freq: " + str(pllFreq))
        print("PLL Mult: " + str(pllMult))
      num = pllFreq % self.xtalFreq
      num = num * 1048575
      num = num // self.xtalFreq
      denom = 1048575
      if self.debug == 1:
        print("PLL num: " + str(num) + " PLL denom: " + str(denom))

      self.si5351.setup_pll(self.si5351.PLL_A, pllMult, num, denom)
      self.si5351.setup_multisynth(0, self.si5351.PLL_A, div)
      self.si5351.setup_multisynth(1, self.si5351.PLL_A, div)
      self.si5351.setup_rdiv(0, self.si5351.R_DIV_1)
      self.si5351.setup_rdiv(1, self.si5351.R_DIV_1)
      self.si5351.set_phase(0, 0)
      self.si5351.set_phase(1, div)
      self.si5351.reset_pll()
      self.si5351.enable_output(True)
        
    return tune, self.vfo
  def ReturnFrequency(self):
    # Return the current tuning and VFO frequency.  See quisk_hardware_model.py.
    return None, None

