#!/usr/bin/env python

""" Sloth.py: A small python script used to automate a YT Shorts Channel

TODO: Setup script to retrieve random video clip from Pexels.com
TODO: Setup script to retrieve random audio clip from a downloaded set of audio files
TODO: Change the caption text to have no background and to be white with a black outline
TODO: Setup a data set for the videos to randomly pull from

"""


from moviepy.editor import *
import random
from PIL import Image, ImageDraw

__author__ = "Caleb Smith"
__copyright__ = "Copyright 2007, The Cogent Project"
__credits__ = ["Caleb Smith"]
# __license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Caleb Smith"
__email__ = "me@calebmsmith.com"
__status__ = "Development"


def round_corners(im: Image, rad: int):
    """
    Rounds the corners of a given image based on a given radius.

    :param im: file to be processed
    :param rad: radius of the corners
    :return: processed image
    """

    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
    alpha = Image.new('L', im.size, 255)

    w, h = im.size

    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))

    im.putalpha(alpha)

    return im


def get_clip():
    """
    Selects a random 8-second video clip from the b-roll library.

    :return: 8-second video clip
    """

    # open video
    clip = VideoFileClip("input.mp4")

    # get a random 8-second segment based on clip duration
    end_point = random.randint(8, int(clip.duration))

    # return sub clip
    clip = clip.subclip(end_point - 8, end_point)

    return clip


def generate_text(txt: str, font='Lato-Bold', size=(720, None), font_size=50, opacity=0.5, padding=(60, 40),
                  radius=30, text_type='caption', color=(0, 0, 0), text_color='white'):
    """
    Generates a text clip to be inserted into a video.

    :param txt: raw text for the clip
    :param font: font for the clip
    :param size: size of the clip mask
    :param font_size: font size of the text
    :param opacity: opacity of the text background
    :param padding: padding of the text background
    :param radius: radius of the background text borders
    :param text_type: text type
    :param color: color of the text background
    :param text_color: color of the text itself

    :return: final text clip
    """

    # create base text clip
    text_clip = TextClip(txt=txt, size=size, font=font,
                         color=text_color, method=text_type, fontsize=font_size).set_position('center')

    # create the color clip rectangle
    color_clip = ColorClip(size=(text_clip.size[0] + padding[0], text_clip.size[1] + padding[1]), color=color)

    # save the clip as an image to be rounded
    CompositeVideoClip([color_clip]).save_frame('temp.png')

    # round the corners of the rectangle
    round_corners(Image.open('temp.png'), radius).save('temp.png')

    # open final version of the rectangle into an image clip
    bg_clip = ImageClip('temp.png').set_opacity(opacity)

    # overlay the text on top of the background clip
    final_clip = CompositeVideoClip([bg_clip, text_clip])

    # return the product
    return final_clip


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
    video_clip = get_clip().set_pos('center').set_duration(8)

    # create topic text clip
    topic_clip = (generate_text(topic.upper(), size=None, font_size=83, opacity=1, radius=20,
                                text_color='black', color=(255, 255, 255), text_type='label',
                                font='Oswald-Medium').set_position(('center', 200)).set_duration(8))

    # create part text clips
    part1_clip = generate_text(part1, font_size=70).set_position('center').set_duration(3.5).set_start(0)
    part2_clip = generate_text(part2, font_size=70).set_position('center').set_duration(4).set_start(4)

    # create channel name text clip
    channel_clip = generate_text(channel, size=None, font_size=50, opacity=1, text_type='label',
                                 padding=(60, 30), radius=25).set_position(('center', 1600)).set_duration(8)

    # compose the video
    video = CompositeVideoClip([video_clip, topic_clip, part1_clip, part2_clip, channel_clip]).set_duration(8)

    # setup the filename
    filename = 'Output/' + part1 + ' #shorts.mp4'

    # export the completed short
    video.write_videofile(filename)

    # return the filename
    return filename