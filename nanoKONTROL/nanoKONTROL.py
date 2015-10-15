# live9 forward compatibility
from __future__ import with_statement

import Live
import time  # We will be using time functions for time-stamping our log file outputs

# import parameters assigned in other file
from parameters import *

""" All of the Framework files are listed below, but we are only using using some of them in this script (the rest are commented out) """
from _Framework.ButtonElement import ButtonElement  # Class representing a button a the controller
# from _Framework.ButtonMatrixElement import ButtonMatrixElement # Class representing a 2-dimensional set of buttons
# from _Framework.ButtonSliderElement import ButtonSliderElement # Class representing a set of buttons used as a slider
from _Framework.ChannelStripComponent import ChannelStripComponent  # Class attaching to the mixer of a given track
# from _Framework.ChannelTranslationSelector import ChannelTranslationSelector # Class switches modes by translating the given controls' message channel
from _Framework.ClipSlotComponent import ClipSlotComponent  # Class representing a ClipSlot within Live
from _Framework.CompoundComponent import \
    CompoundComponent  # Base class for classes encompasing other components to form complex components
from _Framework.ControlElement import \
    ControlElement  # Base class for all classes representing control elements on a controller
from _Framework.ControlSurface import ControlSurface  # Central base class for scripts based on the new Framework
from _Framework.ControlSurfaceComponent import \
    ControlSurfaceComponent  # Base class for all classes encapsulating functions in Live
from _Framework.DeviceComponent import DeviceComponent # Class representing a device in Live
# from _Framework.DisplayDataSource import DisplayDataSource # Data object that is fed with a specific string and notifies its observers
from _Framework.EncoderElement import EncoderElement # Class representing a continuous control on the controller
from _Framework.InputControlElement import *  # Base class for all classes representing control elements on a controller
# from _Framework.LogicalDisplaySegment import LogicalDisplaySegment # Class representing a specific segment of a display on the controller
from _Framework.MixerComponent import MixerComponent  # Class encompassing several channel strips to form a mixer
# from _Framework.ModeSelectorComponent import ModeSelectorComponent # Class for switching between modes, handle several functions with few controls
# from _Framework.NotifyingControlElement import NotifyingControlElement # Class representing control elements that can send values
# from _Framework.PhysicalDisplayElement import PhysicalDisplayElement # Class representing a display on the controller
from _Framework.SceneComponent import SceneComponent  # Class representing a scene in Live
from _Framework.SessionComponent import \
    SessionComponent  # Class encompassing several scene to cover a defined section of Live's session
from _Framework.SessionZoomingComponent import \
    SessionZoomingComponent  # Class using a matrix of buttons to choose blocks of clips in the session
from _Framework.SliderElement import SliderElement  # Class representing a slider on the controller
# from _Framework.TrackEQComponent import TrackEQComponent # Class representing a track's EQ, it attaches to the last EQ device in the track
# from _Framework.TrackFilterComponent import TrackFilterComponent # Class representing a track's filter, attaches to the last filter in the track
from _Framework.TransportComponent import \
    TransportComponent  # Class encapsulating all functions in Live's transport section


class nanoKONTROL(ControlSurface):
    __doc__ = " Initial script for Korg nanoKONTROL controller script "
    __module__ = __name__

    """------------------------------------------------------------------------------------------"""
    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        with self.component_guard():
            # Turn off rebuild MIDI map until after we're done setting up
            self._set_suppress_rebuild_requests(True)


            """ Call our setup functions """
            # Setup the transport part
            self._setup_transport_control()

            # Setup the mixer part
            self._setup_mixer_control()

            # Setup the session part
            self._setup_session_control()

            # Track navigation
            #self._setup_track_navigation_control()

            #link the session model to the Live object-> shows your ring
            self.set_highlighting_session_component(session)

            # Device component control (effect rack)
            self._setup_device_control()


            """ Here is some Live API stuff just for fun """
            app = Live.Application.get_application()  # get a handle to the App
            maj = app.get_major_version()  # get the major version from the App
            min = app.get_minor_version()  # get the minor version from the App
            bug = app.get_bugfix_version()  # get the bugfix version from the App
            self.show_message("Loading nanoKONTROL for Live " + str(maj) + "." + str(min) + "." + str(
                bug))  # put them together and use the ControlSurface show_message method to output version info to console on the status bar of Live

            """ Listener for midi input """
            self.encoder_test_input=EncoderElement(MIDI_CC_TYPE, midi_channel, 94, Live.MidiMap.MapMode.relative_smooth_two_compliment) # identifies P&d1 as a ButtonElement. IS_MOMENTARY is true if the button send a message on being released
            self.encoder_test_input.add_value_listener(self._encoder_test_input, identify_sender= False) #adda value listener that will lauch the method self.helloworld when Pad1 is pressed

            # Turn rebuild back on, now that we're done setting up
            self._set_suppress_rebuild_requests(False)



    """ Device control allow to control the audio effect rack for the selected track """
    """------------------------------------------------------------------------------------------"""
    def _setup_device_control(self):
        is_momentary = True

        global device   # We want to instantiate the global mixer as a MixerComponent object (it was a global "None" type up until now...)
        device = DeviceComponent()
        device.name = 'Audio Effect Rack'

        # Button on/off
        button_on_off = ButtonElement(is_momentary, MIDI_CC_TYPE, midi_channel, midi_device_on_off)
        device.set_on_off_button(button_on_off)

        # Audio Effect Rack - 8 modulation controls
        device_parameter_controls = []
        for index in range(8):
            device_parameter_controls.append(EncoderElement(MIDI_CC_TYPE, midi_channel, midi_device_controls[index], Live.MidiMap.MapMode.absolute))
        device.set_parameter_controls(device_parameter_controls)

        self.set_device_component(device)
        self._device_selection_follows_track_selection = True   # select automatically the device of the selected track



    """ Called on configured encoder input """
    """------------------------------------------------------------------------------------------"""
    def _encoder_test_input(self, value):
        self.show_message("Yeah ==> " + str(value) + " ! " + str(mixer.song().view.selected_track))


    """ Initialisation of transport part """
    """------------------------------------------------------------------------------------------"""
    def _setup_transport_control(self):
        is_momentary = True

        """ Instantiate a Transport Component """
        transport = TransportComponent()

        """ Buttons declaration """
        button_play = ButtonElement(is_momentary, MIDI_CC_TYPE, midi_channel, midi_transport_play_button)
        button_stop = ButtonElement(is_momentary, MIDI_CC_TYPE, midi_channel, midi_transport_stop_button)
        button_record = ButtonElement(is_momentary, MIDI_CC_TYPE, midi_channel, midi_transport_record_button)
        button_loop = ButtonElement(is_momentary, MIDI_CC_TYPE, midi_channel, midi_transport_loop_button)
        button_seek_ffwd = ButtonElement(is_momentary, MIDI_CC_TYPE, midi_channel, midi_transport_seek_ffwd)
        button_seek_rwd = ButtonElement(is_momentary, MIDI_CC_TYPE, midi_channel, midi_transport_seek_rwd)

        """ Buttons association """
        transport.set_play_button(button_play)
        transport.set_stop_button(button_stop)
        transport.set_record_button(button_record)
        transport.set_loop_button(button_loop)
        transport.set_seek_buttons(button_seek_ffwd, button_seek_rwd)


    """ Initialisation of mixer part """
    """------------------------------------------------------------------------------------------"""
    def _setup_mixer_control(self):
        is_momentary = True

        """ Instantiate a Mixer Component """
        global mixer  # We want to instantiate the global mixer as a MixerComponent object (it was a global "None" type up until now...)
        mixer = MixerComponent(mixer_num_tracks, 2, with_eqs=True, with_filters=True)  # (num_tracks, num_returns, with_eqs, with_filters)
        mixer.set_track_offset(0)  # Sets start point for mixer strip (offset from left)
        self.song().view.selected_track = mixer.channel_strip(0)._track  # set the selected strip to the first track, so that we don't, for example, try to assign a button to arm the master track, which would cause an assertion error

        """ Buttons and Sliders association """
        # Master channel
        mixer.master_strip().set_volume_control(SliderElement(MIDI_CC_TYPE, midi_channel, midi_mixer_volume_master))  # sets the continuous controller for volume

        # Other channels, same size as mixer_num_tracks
        # Set volume control, solo and mute buttons
        for index in range(mixer_num_tracks):  # launch_button assignment must match number of scenes
            mixer.channel_strip(index).set_volume_control(SliderElement(MIDI_CC_TYPE, midi_channel, midi_mixer_volume_channels[index]))  # sets the continuous controller for volume
            mixer.channel_strip(index).set_solo_button(ButtonElement(is_momentary, MIDI_CC_TYPE, midi_channel, midi_mixer_solo_channels[index]))  # sets the solo button
            mixer.channel_strip(index).set_mute_button(ButtonElement(is_momentary, MIDI_CC_TYPE, midi_channel, midi_mixer_mute_channels[index]))  # sets the mute ("activate") button

        """ Buttons to select track """
        button_next_track = ButtonElement(is_momentary, MIDI_CC_TYPE, midi_channel, midi_track_select_next)
        button_previous_track = ButtonElement(is_momentary, MIDI_CC_TYPE, midi_channel, midi_track_select_previous)
        mixer.set_select_buttons(button_next_track, button_previous_track)

        """ Listeners """
        # When selected track if changed
        self.song().view.add_selected_track_listener(self.on_track_selected)


    """ Called when a track is changed """
    """------------------------------------------------------------------------------------------"""
    def on_track_selected(self):
        self.show_message("Track changed!")

        """ Encoder for Sends controls on selected track """
        '''encoder_test = EncoderElement(MIDI_CC_TYPE, midi_channel, 57, Live.MidiMap.MapMode.absolute)
        encoder_test2 = EncoderElement(MIDI_CC_TYPE, midi_channel, 58, Live.MidiMap.MapMode.absolute)
        encoder_send_buttons = []
        encoder_send_buttons.append(encoder_test)
        encoder_send_buttons.append(encoder_test2)
        mixer.selected_strip().set_send_controls(encoder_send_buttons)'''



    """ Initialisation of session part """
    """------------------------------------------------------------------------------------------"""
    def _setup_session_control(self):
        is_momentary = True

        # Size of session box
        num_tracks = 8 # column
        num_scenes = 1 # row


        """ Buttons declaration """
        # Navigation
        button_navig_up = ButtonElement(is_momentary, MIDI_CC_TYPE, midi_channel, midi_session_up)
        button_navig_down = ButtonElement(is_momentary, MIDI_CC_TYPE, midi_channel, midi_session_down)


        """ Declare our session box """
        global session #We want to instantiate the global session as a SessionComponent object (it was a global "None" type up until now...)
        session = SessionComponent(num_tracks, num_scenes) #(num_tracks, num_scenes) A session highlight ("red box") will appear with any two non-zero values
        session.set_offsets(0, 0) #(track_offset, scene_offset) Sets the initial offset of the "red box" from top left
        session._do_show_highlight()   #to ensure that this session will be highlighted


        """ Buttons association """
        # Navigation up, down, left, right
        session.set_scene_bank_buttons(button_navig_down, button_navig_up)
        # Launch selected clip
        for index in range(num_tracks):
            session.scene(0).clip_slot(index).set_launch_button(ButtonElement(is_momentary, MIDI_CC_TYPE, midi_channel, midi_session_launch_clip[index]))
        # Stop selected track
        stop_track_buttons = []
        for index in range(num_tracks):
            stop_track_buttons.append(ButtonElement(is_momentary, MIDI_CC_TYPE, midi_channel, midi_session_stop_track[index]))
        session.set_stop_track_clip_buttons(tuple(stop_track_buttons)) #array size needs to match num_tracks



    """------------------------------------------------------------------------------------------"""
    def disconnect(self):
        """clean things up on disconnect"""
        self.log_message(time.strftime("%d.%m.%Y %H:%M:%S", time.localtime()) + "--------------= nanoKONTROL log closed =--------------")  # Create entry in log file
        ControlSurface.disconnect(self)
        return None
