#!/usr/bin/env python

""" sloth.py: A small python script used to automate a YT Shorts Channel """

import subprocess
from moviepy.editor import *
from video_lib import *
from audio_lib import *

__author__ = "Caleb Smith"
__copyright__ = "Copyright 2007, The Cogent Project"
__credits__ = ["Caleb Smith"]
__version__ = "1.0"
__maintainer__ = "Caleb Smith"
__email__ = "me@calebmsmith.com"
__status__ = "Development"


def export_video(filename: str, video, audio):
    video.write_videofile('temp.mp4')

    audio.write_audiofile('temp.mp3')

    command = ['ffmpeg',
               '-y',
               '-i', "temp.mp4",
               '-i', "temp.mp3",
               '-c:v', 'copy',
               '-c:a', 'aac',
               '-shortest',
               filename]

    # run ffmpeg command
    subprocess.run(command)

    os.remove('temp.mp3')
    os.remove('temp.mp4')


# def generate_fact_video(duration: float, topic: str, captions: list, channel: str):
#     """
#     Generates a Youtube Short/TikTok/Instagram Reel, in the format of a two-part fact.
#
#     :param duration: duration of the clip
#     :param topic: topic text
#     :param captions: quote list
#     :param channel: channel name
#
#     :return: file location
#     """
#
#     # get video clip
#     video_clip = random_pexels_video_clip(duration, 'nature').set_pos('center').set_duration(8)
#
#     # create topic text clip
#     topic_clip = (generate_text(topic.upper(), box_size=None, font_size=83, bg_opacity=1, radius=20,
#                                 text_color='black', bg_color=(255, 255, 255), text_type='label',
#                                 font='Oswald-Medium').set_position(('center', 200)).set_duration(8))
#
#     # create part text clips
#     part1_clip = generate_text(part1, font='Lato-Black', font_size=75, bg_opacity=0, text_color='white',
#                                stroke_color='black', stroke_width=3).set_position('center').set_duration(3.5).set_start(
#         0)
#     part2_clip = generate_text(part2, font='Lato-Black', font_size=75, bg_opacity=0, text_color='white',
#                                stroke_color='black', stroke_width=3).set_position('center').set_duration(4).set_start(4)
#
#     # create channel name text clip
#     channel_clip = generate_text(channel, box_size=None, font_size=50, bg_opacity=1, text_type='label',
#                                  bg_padding=(60, 30), radius=25).set_position(('center', 1600)).set_duration(8)
#
#     # compose the video
#     video = CompositeVideoClip([video_clip, topic_clip, part1_clip, part2_clip, channel_clip]).set_duration(8)
#
#     # get audio
#     audio = random_audio_clip()
#
#     # create filename
#     filename = 'Output/' + captions[0] + ' #shorts.mp4'
#
#     # export video
#     export_video(filename, video, audio)
#
#     return filename
