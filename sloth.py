#!/usr/bin/env python

""" sloth.py: A small python script used to automate a YT Shorts Channel """

import subprocess

from moviepy.editor import *
from video_engine import *
from audio_engine import *

__author__ = "Caleb Smith"
__copyright__ = "Copyright 2007, The Cogent Project"
__credits__ = ["Caleb Smith"]
__version__ = "1.0"
__maintainer__ = "Caleb Smith"
__email__ = "me@calebmsmith.com"
__status__ = "Development"


def generate_fact_video(topic: str, part1: str, part2: str, channel: str):
    """
    Generates a Youtube Short/TikTok/Instagram Reel, in the format of a two-part fact.

    :param topic: topic text
    :param part1: part 1 of the quote
    :param part2: part 2 of the quote
    :param channel: channel name

    :return: file location
    """

    # get video clip
    video_clip = random_video_clip().set_pos('center').set_duration(8)

    # create topic text clip
    topic_clip = (generate_text(topic.upper(), size=None, font_size=83, opacity=1, radius=20,
                                text_color='black', color=(255, 255, 255), text_type='label',
                                font='Oswald-Medium').set_position(('center', 200)).set_duration(8))

    # create part text clips
    part1_clip = generate_text(part1, font='Lato-Black', font_size=75, opacity=0, text_color='white',
                               stroke_color='black', stroke_width=3).set_position('center').set_duration(3.5).set_start(0)

    part2_clip = generate_text(part2, font='Lato-Black', font_size=75, opacity=0, text_color='white',
                               stroke_color='black', stroke_width=3).set_position('center').set_duration(4).set_start(4)

    # create channel name text clip
    channel_clip = generate_text(channel, size=None, font_size=50, opacity=1, text_type='label',
                                 padding=(60, 30), radius=25).set_position(('center', 1600)).set_duration(8)

    # compose the video
    video = CompositeVideoClip([video_clip, topic_clip, part1_clip, part2_clip, channel_clip]).set_duration(8)

    video.write_videofile('temp.mp4')

    # get audio
    audio = get_audio_clip()

    audio.write_audiofile('temp.mp3')

    filename = 'Output/' + part1 + ' #shorts.mp4'

    command = ['ffmpeg',
               '-y',  # approve output file overwite
               '-i', "temp.mp4",
               '-i', "temp.mp3",
               '-c:v', 'copy',
               '-c:a', 'aac',  # to convert mp3 to aac
               '-shortest',
               filename]

    subprocess.run(command)

    # set audio
    # final_clip = video.set_audio(audio)

    # set up the filename
    # filename = 'Output/' + part1 + ' #shorts.mp4'

    # export the completed short
    # final_clip.write_videofile(filename)

    # return the filename
    return filename
