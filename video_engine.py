import requests
import random
from pexelsPy import API
from dotenv import load_dotenv
from moviepy.editor import *
from PIL import Image, ImageDraw

load_dotenv()
PEXELS_API = os.getenv('PEXELS_API')


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


def generate_text(txt: str, font='Lato-Bold', size=(720, None), font_size=50, opacity=0.5, padding=(60, 40),
                  radius=30, text_type='caption', color=(0, 0, 0), text_color='white', stroke_color=None, stroke_width=0):
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
    :param stroke_color: outline color
    :param stroke_width: outline width

    :return: final text clip
    """

    # create base text clip
    text_clip = TextClip(txt=txt, size=size, font=font, stroke_color=stroke_color, stroke_width=stroke_width,
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


def add_video(video: str):
    file = open(os.getenv('VIDEO_POOL'), 'a+')

    file.write(video + '\n')

    file.close()


def get_video_list():
    videos = open('downloaded_files.txt', 'r').readlines()

    for i in range(len(videos)):
        videos[i] = videos[i].replace('\n', '')

    return videos


def download_video(video_url: str, title: str):
    r = requests.get(video_url)

    with open(title, 'wb') as outfile:
        outfile.write(r.content)

    outfile.close()


def fetch_video(topic):
    """
    Downloads a random vertical video from Pexels

    :param topic: topic of video
    :return: path of the video
    """

    # loaf pexels api
    api = API(PEXELS_API)

    # retrieve all previously used videos
    video_pool = get_video_list()

    # set page number
    page_num = 1

    # search for new pexels video
    while True:
        api.search_videos(topic, page=page_num, results_per_page=10)
        videos = api.get_videos()

        for data in videos:
            if data.width < data.height:  # look for vertical orientation videos
                if data.url not in video_pool:
                    add_video(data.url)

                    download_video('https://www.pexels.com/video/' + str(data.id) +
                                   '/download', 'video/' + data.url.split('/')[-2] + '.mp4')

                    return 'video/' + data.url.split('/')[-2] + '.mp4'

        page_num += 1


def random_video_clip():
    """
    Retrieves a random video file from Pexels and formats it

    :return: 8-second video clip
    """

    # get a random video from pexels
    video_path = fetch_video('nature')

    # open video
    clip = VideoFileClip(video_path).without_audio()

    # resize clip
    clip = clip.resize(newsize=(1080, 1920))

    # get a random 8-second segment based on clip duration
    end_point = random.randint(8, int(clip.duration))

    # get sub clip
    clip = clip.subclip(end_point - 8, end_point)

    # delete video to prevent clutter
    os.remove(video_path)

    # return final product
    return clip