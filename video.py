#!/usr/bin/env python

""" video.py """

import requests
import random
from pexelsPy import API
from dotenv import load_dotenv
from moviepy.editor import *
from PIL import Image, ImageDraw

__author__ = "Caleb Smith"
__credits__ = ["Caleb Smith"]
__version__ = "1.0"
__maintainer__ = "Caleb Smith"
__email__ = "me@calebmsmith.com"
__status__ = "Development"

# load .env
load_dotenv()

# retrieve the Pexels API key from environment variables
PEXELS_API = os.getenv('PEXELS_API')


def round_corners(image: Image, rad: int):
    """
    Rounds the corners of a given image based on a given radius.

    :param image: Image to be processed
    :param rad: Radius of the corners
    :return: Processed image
    """

    # create a circular mask
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)

    # create an alpha mask
    alpha = Image.new('L', image.size, 255)

    w, h = image.size

    # paste the circular mask to the corners of the alpha mask
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))

    # apply the alpha mask to the image
    image.putalpha(alpha)

    return image


def generate_text(text='{Text Clip}', text_type='label', text_color='white', font='Lato-Bold', box_size=(None, None),
                  font_size=50, bg_opacity=1, bg_padding=(60, 40), bg_color=(0, 0, 0), radius=30, stroke_color=None,
                  stroke_width=0, position=('center', 'center'), start=0, duration=5.0):
    """
    Generates a text clip to be inserted into a video.

    :param text: Raw text for the clip
    :param text_type: Text type
    :param text_color: Color of the text itself
    :param font: Font for the clip
    :param box_size: Size of the clip mask
    :param font_size: Font size of the text
    :param bg_opacity: Opacity of the text background
    :param bg_padding: Padding of the text background
    :param bg_color: Color of the text background
    :param radius: Radius of the background text borders
    :param stroke_color: Outline color
    :param stroke_width: Outline width
    :param position: Position of the text
    :param start: Start second of the text
    :param duration: Duration of the text in the video
    :return: Final text clip
    """

    # create a base text clip
    text_clip = TextClip(txt=text, size=box_size, font=font, stroke_color=stroke_color, stroke_width=stroke_width,
                         color=text_color, method=text_type, fontsize=font_size).set_position('center')

    # create the color clip rectangle
    color_clip = ColorClip(size=(text_clip.size[0] + bg_padding[0], text_clip.size[1] + bg_padding[1]), color=bg_color).set_opacity(bg_opacity)

    if bg_opacity > 0 and radius > 0:
        # save the clip as an image to be rounded
        CompositeVideoClip([color_clip]).save_frame('temp.png')

        # round the corners of the rectangle
        round_corners(Image.open('temp.png'), radius).save('temp.png')

        # open the final version of the rectangle into an image clip
        color_clip = ImageClip('temp.png').set_opacity(bg_opacity)

        # delete the temporary image
        os.remove('temp.png')

    # overlay the text on top of the background clip
    final_clip = CompositeVideoClip([color_clip, text_clip])

    # return the product
    return final_clip.set_position(position).set_start(start).set_duration(duration)


def add_to_video_pool(video: str):
    """
    Adds a video to the video pool file.

    :param video: Video file path to be added
    :return: None
    """

    file = open(os.getenv('VIDEO_POOL'), 'a+')

    file.write(video + '\n')

    file.close()


def get_video_pool():
    """
    Reads the video pool file and retrieves a list of video paths.

    :return: List of video paths
    """

    videos = open(os.getenv('VIDEO_POOL'), 'r').readlines()

    for i in range(len(videos)):
        videos[i] = videos[i].replace('\n', '')

    return videos


def download_video(video_url: str, title: str):
    """
    Downloads a video from a given URL and saves it with the specified title.

    :param video_url: URL of the video to be downloaded
    :param title: Title to be used for the saved video
    :return: None
    """

    r = requests.get(video_url)

    with open(title, 'wb') as outfile:
        outfile.write(r.content)

    outfile.close()


def fetch_video(topic):
    """
    Downloads a random vertical video from Pexels.

    :param topic: Topic of the video
    :return: Path of the downloaded video
    """

    # load the Pexels API using the API key
    api = API(PEXELS_API)

    # retrieve all previously used videos
    video_pool = get_video_pool()

    # set the initial page number
    page_num = 1

    # search for a new Pexels video
    while True:
        api.search_videos(topic, page=page_num, results_per_page=10)
        videos = api.get_videos()

        for data in videos:
            if data.width < data.height:  # look for vertical orientation videos
                if data.url not in video_pool:
                    add_to_video_pool(data.url)

                    download_video('https://www.pexels.com/video/' + str(data.id) +
                                   '/download', 'video/' + data.url.split('/')[-2] + '.mp4')

                    return 'video/' + data.url.split('/')[-2] + '.mp4'

        page_num += 1


def random_pexels_video_clip(duration: float, topic: str):
    """
    Retrieves a random video file from Pexels and formats it.

    :param duration: Desired duration of the video clip
    :param topic: Topic to be used for video search
    :return: 8-second video clip
    """

    while True:
        # fetch a random video from Pexels
        video_path = fetch_video(topic)

        clip = VideoFileClip(video_path).without_audio()

        if clip.duration >= duration:
            break

    # resize the clip
    clip = clip.resize(newsize=(1080, 1920))

    # get a random 8-second segment based on clip duration
    end_point = random.uniform(duration, clip.duration)

    # get subclip
    clip = clip.subclip(end_point - duration, end_point)

    # delete the downloaded video to prevent clutter
    os.remove(video_path)

    # return the final product
    return clip


def random_video_clip(duration: float):
    """
    Retrieves a random video clip from the 'video' directory with a specified duration.

    :param duration: Desired duration of the video clip
    :return: Video clip with the specified duration
    """

    if duration > int(os.getenv('MAX_DURATION')):
        raise Exception('Given duration exceeds the maximum duration in the video library.')

    checked_videos = []

    # list all video files in the 'video' directory
    video_files = [file for file in os.listdir('video_archive') if file.endswith('.mp4')]

    while True:
        # randomly select a video path from the list of video files
        video_path = random.choice(video_files)

        if video_path not in checked_videos:
            checked_videos.append(video_path)
            video_path = os.path.join('video_archive', video_path)

            clip = VideoFileClip(video_path).without_audio()

            if clip.duration >= duration:
                break
        elif len(checked_videos) == len(video_files):
            raise FileNotFoundError('There are no videos with a duration of at least ' + str(duration) + ' seconds')

    # resize the clip
    clip = clip.resize(newsize=(1080, 1920))

    # get a random segment based on clip duration
    end_point = random.uniform(duration, clip.duration)

    # get subclip
    clip = clip.subclip(end_point - duration, end_point)

    return clip
