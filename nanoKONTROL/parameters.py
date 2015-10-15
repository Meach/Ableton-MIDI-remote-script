# midi_channel
midi_channel=0


""" Here we define some global variables """
mixer = None #Global mixer object - global so that we can manipulate the same mixer object from within any of our methods
device = None

# Transport
#----------
midi_transport_play_button=45
midi_transport_stop_button=46
midi_transport_record_button=44
midi_transport_loop_button=49
midi_transport_seek_ffwd=48
midi_transport_seek_rwd=47
#midi_transport_tap_tempo=23
#midi_transport_tempo_control=14
#midi_transport_tempo_fine_control=2


# Mixer (Scene 1)
#----------------
midi_mixer_volume_master=13 # midi map is same for 9th slider for all 4 scenes
mixer_num_tracks = 8 #A mixer is one-dimensional; here we define the width in tracks - 8 columns, which we will map to 8 sliders
midi_mixer_volume_channels=[2, 3, 4, 5, 6, 8, 9, 12] # Has to be same size as mixer_num_tracks
midi_mixer_solo_channels=[33, 34, 35, 36, 37, 38, 39, 40] # Has to be same size as mixer_num_tracks
midi_mixer_mute_channels=[23, 24, 25, 26, 27, 28, 29, 30] # Has to be same size as mixer_num_tracks


# Effect control (Scene 2)
#-------------------------
midi_track_select_next = 75
midi_track_select_previous = 84
midi_device_on_off = 67
midi_device_controls = [57, 58, 59, 60, 61, 62, 63, 64] # encoders: control effect rack modulation controls

#... = [67, 68, 69, 70, 71, 72, 73, 74] # top buttons
#... = [76, 77, 78, 79, 80, 81, 82, 83] # bottom buttons


# Session (Scene 3)
#------------------
midi_session_up = 115
midi_session_down = 124

midi_session_launch_clip = [107, 108, 109, 110, 111, 112, 113, 114]
midi_session_stop_track = [116, 117, 118, 119, 120, 121, 122, 123]

