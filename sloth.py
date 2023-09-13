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


def template_video(template: dict, name: str):
    """
    Generates a video based upon a JSON template.

    :param template:
    :param name:
    :return:
    """

    video_elements = []

    video_duration = template['video_data']['duration']

    video_elements.append(random_video_clip(video_duration, 'nature').set_pos('center').set_duration(video_duration))

    for element in template['text_elements'].keys():
        if template['text_elements'][element]['duration'] == 'x':
            duration = video_duration
        else:
            duration = template['text_elements'][element]['duration']

        template_data = template['text_elements'][element]

        video_elements.append(generate_text(template_data[element]['text'],
                                            font=template_data['font'],
                                            box_size=(template_data['box_size'][0], template_data['box_size'][1]),
                                            font_size=template_data['font_size'],
                                            bg_opacity=template_data['bg_opacity'],
                                            bg_padding=(template_data['bg_padding'][0], template_data['bg_padding'][1]),
                                            bg_color=(template_data['bg_color'][0], template_data['bg_color'][1],
                                                      template_data['bg_color'][2]),
                                            radius=template_data['radius'],
                                            text_type=template_data['text_type'],
                                            text_color=template_data['text_color'],
                                            stroke_width=template_data['stroke_width'],
                                            stroke_color=template_data['stroke_color']
                                            ).set_position((template_data['position'][0], template_data['position'][1]))
                              .set_duration(duration).set_start(template_data['start_time']))

    video = CompositeVideoClip(video_elements).set_duration(template['video_data']['duration'])

    # create temporary video file
    video.write_videofile('temp.mp4')

    # get audio
    audio = get_audio_clip()

    # create temporary audio file
    audio.write_audiofile('temp.mp3')

    # create file path
    filename = 'Output/' + name + '.mp4'

    # create ffmpeg command
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

    # remove temporary files
    os.remove('temp.mp3')
    os.remove('temp.mp4')


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
    video_clip = random_video_clip('nature').set_pos('center').set_duration(8)

    # create topic text clip
    topic_clip = (generate_text(topic.upper(), box_size=None, font_size=83, bg_opacity=1, radius=20,
                                text_color='black', bg_color=(255, 255, 255), text_type='label',
                                font='Oswald-Medium').set_position(('center', 200)).set_duration(8))

    # create part text clips
    part1_clip = generate_text(part1, font='Lato-Black', font_size=75, bg_opacity=0, text_color='white',
                               stroke_color='black', stroke_width=3).set_position('center').set_duration(3.5).set_start(0)
    part2_clip = generate_text(part2, font='Lato-Black', font_size=75, bg_opacity=0, text_color='white',
                               stroke_color='black', stroke_width=3).set_position('center').set_duration(4).set_start(4)

    # create channel name text clip
    channel_clip = generate_text(channel, box_size=None, font_size=50, bg_opacity=1, text_type='label',
                                 bg_padding=(60, 30), radius=25).set_position(('center', 1600)).set_duration(8)

    # compose the video
    video = CompositeVideoClip([video_clip, topic_clip, part1_clip, part2_clip, channel_clip]).set_duration(8)

    video.write_videofile('temp.mp4')

    # get audio
    audio = get_audio_clip()

    audio.write_audiofile('temp.mp3')

    filename = 'Output/' + part1 + ' #shorts.mp4'

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

    return filename
