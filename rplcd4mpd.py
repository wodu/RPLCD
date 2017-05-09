#!/usr/bin/python
# -*- coding: utf-8 -*-

#from __future__ import print_function, division, absolute_import, unicode_literals

import RPi.GPIO as GPIO
import time
import sys
import os
import glob
import subprocess

from RPLCD.i2c import CharLCD
from RPLCD import cleared, cursor
from RPLCD import Alignment, CursorMode, ShiftMode
from time import sleep, strftime
from datetime import datetime
from unidecode import unidecode

GPIO.setwarnings(False)

# --------------
# MPD Info - Start
# --------------
def Get_MPC_info():
   subprocess_list = subprocess.check_output(('ps', '-A'))
   subprocess_list_mpd = subprocess_list.find("mpd")
   
   if subprocess_list_mpd == -1:
      mpd_info = " MPD not started!   "
      return mpd_info
   
   else:
      process = subprocess.Popen('mpc', shell=True, stdout=subprocess.PIPE)
      status = process.communicate()[0]
      statusLines = status.split('\n')
      #print statusLines
      
      # If MPC was not on "STOP"
      if len(statusLines) > 2:
            artist = unicode(statusLines[0].replace("Radio Afera 98,6 MHz: ",""), errors="replace")
      
            mpd_info = artist
               
      else:
            mpd_info = unicode(" STOP    00:00 ")
      
      #print " mpd info = " + mpd_info
      return mpd_info
   
# -------------   
# MPD Info - End
# -------------

# -------------------
# Display section - Start
# -------------------

lcd = CharLCD(0x20, cols=16, rows=4)

lcd.clear()
old_str = ""
while 1:
   str2display = unidecode(Get_MPC_info())
   if str2display != old_str:
	lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string(unidecode(Get_MPC_info()))
   sleep(3)
   old_str = str2display

# ------------------   
# Display section - End
# ------------------
