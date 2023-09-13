import random
from pytube import YouTube
from moviepy.editor import *


def download_audio(url: str):
    """
    Downloads the audio of a given video from YouTube

    :param url:
    :return:
    """

    # create YouTube object
    yt = YouTube(url)

    # extract only audio
    video = yt.streams.filter(only_audio=True, mime_type='audio/mp4', abr='128kbps').first()

    # download the file
    out_file = video.download(output_path='Audio')

    # save the file
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)

    # result of success
    return True


def populate_audio():
    """
    Populates the Audio folder with a set of audio files from YouTube

    :return:
    """

    urls = ['NvwnIZX-1cs', '-iNHtdL-zu4',
            'VGEbA_VQg1o', '_A0Beo0M-tQ',
            'vQfTPbAaSjk', 'iOOG2lFkMf0',
            'Ip6cw8gfHHI', '1i8WJ8cRWsE',
            'QCtEe-zsCtQ', 'eKL3TceSxvk',
            'qnFcVpItds4', 'jKRW9ZV8QzI',
            'mmO3KqoK1vU']

    # download videos
    for video in urls:
        download_audio('https://www.youtube.com/watch?v=' + video)


def get_audio_clip():
    """
    Selects a random 8-second audio clip from the Audio folder.

    :return: 8-second audio clip
    """

    # open audio
    clip = AudioFileClip('Audio/' + random.choice(os.listdir('Audio')))

    # geta  random 8-second segment based on clip duration
    end_point = random.randint(8, int(clip.duration))

    # get sub clip
    clip = clip.subclip(end_point - 8, end_point)

    # return final product
    return clip