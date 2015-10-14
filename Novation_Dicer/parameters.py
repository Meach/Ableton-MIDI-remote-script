#!/usr/bin/env python


""" Here we define some global variables """
session = None #Global session object - global so that we can manipulate the same session object from within any of our methods

# Since I cannot find a way to get 2 session in same script at the same time, we duplicate the script and change the following variable
# Change this variable if the dicer is left or right
# 0 = Master
# 1 = Slave
index_dicer=0

# Channels
#---------
midi_channel_red=[11, 14]
midi_channel_green=[12, 15]
midi_channel_amber=[13, 16]


# Key codes
#----------
midi_cc_normal=[60, 61, 62, 63, 64]
midi_cc_shifted=[65, 66, 67, 68, 69]