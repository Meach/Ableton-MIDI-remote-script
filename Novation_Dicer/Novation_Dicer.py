# live9 forward compatibility
from __future__ import with_statement

import Live
import time # We will be using time functions for time-stamping our log file outputs

# import parameters assigned in other file
from parameters import *

""" All of the Framework files are listed below, but we are only using using some of them in this script (the rest are commented out) """
from _Framework.ButtonElement import ButtonElement # Class representing a button a the controller
from _Framework.ControlSurface import ControlSurface # Central base class for scripts based on the new Framework
from _Framework.InputControlElement import * # Base class for all classes representing control elements on a controller
from _Framework.SessionComponent import SessionComponent # Class encompassing several scene to cover a defined section of Live's session


class Novation_Dicer(ControlSurface):
    __module__ = __name__
    __doc__ = " Initial testing script for Novation Dicer controller to be used by 2 people to navigate in Ableton"


    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        with self.component_guard():
            # Turn off rebuild MIDI map until after we're done setting up
            self._set_suppress_rebuild_requests(True)

            # Setup the selection box object
            self._setup_selection_box_control(index_dicer)

            #link the session model to the Live object-> shows your ring
            self.set_highlighting_session_component(session)

            """ Here is some Live API stuff just for fun """
            app = Live.Application.get_application() # get a handle to the App
            maj = app.get_major_version() # get the major version from the App
            min = app.get_minor_version() # get the minor version from the App
            bug = app.get_bugfix_version() # get the bugfix version from the App
            self.show_message("Loading Novation_Dicer #" + str(index_dicer) + " for Live " + str(maj) + "." + str(min) + "." + str(bug)) #put them together and use the ControlSurface show_message method to output version info to console on the status bar of Live

            #Turn rebuild back on, now that we're done setting up
            self._set_suppress_rebuild_requests(False)

    """ Initialisation of the session """
    def _setup_selection_box_control(self, indexDicer):
        is_momentary = True


        # Size of session box
        num_tracks = 1 #1 column
        num_scenes = 1 #1 row


        """ Buttons declaration """
        # Navigation
        button_navig_up = ButtonElement(is_momentary, MIDI_NOTE_TYPE, midi_channel_red[indexDicer] - 1, midi_cc_normal[0])
        button_navig_down = ButtonElement(is_momentary, MIDI_NOTE_TYPE, midi_channel_red[indexDicer] - 1, midi_cc_normal[1])
        button_navig_left = ButtonElement(is_momentary, MIDI_NOTE_TYPE, midi_channel_red[indexDicer] - 1, midi_cc_normal[3])
        button_navig_right = ButtonElement(is_momentary, MIDI_NOTE_TYPE, midi_channel_red[indexDicer] - 1, midi_cc_normal[4])
        # Launch clip
        button_launch_clip = ButtonElement(is_momentary, MIDI_NOTE_TYPE, midi_channel_red[indexDicer] - 1, midi_cc_normal[2])
        # Stop track
        button_stop_track = ButtonElement(is_momentary, MIDI_NOTE_TYPE, midi_channel_red[indexDicer] - 1, midi_cc_shifted[2])
        # Stop all tracks
        #button_stop_track_all


        """ Declare our session box """
        global session #We want to instantiate the global session as a SessionComponent object (it was a global "None" type up until now...)
        session = SessionComponent(num_tracks, num_scenes) #(num_tracks, num_scenes) A session highlight ("red box") will appear with any two non-zero values
        session.set_offsets(indexDicer * 4, 0) #(track_offset, scene_offset) Sets the initial offset of the "red box" from top left
        session._do_show_highlight()   #to ensure that this session will be highlighted


        """ Buttons association """
        # Navigation up, down, left, right
        session.set_scene_bank_buttons(button_navig_down, button_navig_up)
        session.set_track_bank_buttons(button_navig_right, button_navig_left)
        # Launch selected clip
        session.scene(0).clip_slot(0).set_launch_button(button_launch_clip)
        # Stop selected track
        stop_track_buttons = []
        stop_track_buttons.append(button_stop_track)
        session.set_stop_track_clip_buttons(tuple(stop_track_buttons)) #array size needs to match num_tracks
        # Stop all tracks
        #session.set_stop_all_clips_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, midi_channel_red[indexDicer], midi_box_stop_all[indexSession]))
        # Launch selected scene
        #session.scene(0).set_launch_button(ButtonElement(is_momentary, MIDI_CC_TYPE, midi_channel_red[indexDicer], midi_box_launch_scene[indexSession]))


    def disconnect(self):
        """clean things up on disconnect"""
        self.log_message(time.strftime("%d.%m.%Y %H:%M:%S", time.localtime()) + "--------------= Novation_Dicer log closed =--------------") #Create entry in log file
        ControlSurface.disconnect(self)
        return None