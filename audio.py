#!/usr/bin/env python

""" audio.py """

import random
import os
from pytube import YouTube
from moviepy.editor import *

# author information
__author__ = "Caleb Smith"
__credits__ = ["Caleb Smith"]
__version__ = "1.0"
__maintainer__ = "Caleb Smith"
__email__ = "me@calebmsmith.com"
__status__ = "Development"


def download_audio(url: str):
    """
    Downloads the audio of a given video from YouTube and saves it as an MP3 file.

    :param url: YouTube video URL
    :return: True if successful, False otherwise
    """

    try:
        # create a YouTube object
        yt = YouTube(url)

        # extract the audio stream with 128kbps bitrate as an MP4 file
        video = yt.streams.filter(only_audio=True, mime_type='audio/mp4', abr='128kbps').first()

        # download the audio file
        out_file = video.download(output_path='audio_archive')

        # save the downloaded file as an MP3 file
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)

        return True
    except Exception as e:
        print(f"Error downloading audio: {str(e)}")
        return False


def populate_audio():
    """
    Populates the 'Audio' folder with a set of audio files from YouTube.

    :return: None
    """

    urls = ['NvwnIZX-1cs', '-iNHtdL-zu4',
            'VGEbA_VQg1o', '_A0Beo0M-tQ',
            'vQfTPbAaSjk', 'iOOG2lFkMf0',
            'Ip6cw8gfHHI', '1i8WJ8cRWsE',
            'QCtEe-zsCtQ', 'eKL3TceSxvk',
            'qnFcVpItds4', 'jKRW9ZV8QzI',
            'mmO3KqoK1vU', 't2-BUAkQ9Ds',
            'TMO3Q16Yvp4', 'XKGXK_koHic']

    # download audio from YouTube videos
    for video_id in urls:
        download_url = 'https://www.youtube.com/watch?v=' + video_id
        download_audio(download_url)


def random_audio_clip(duration: float):
    """
    Selects a random X-second audio clip from the 'Audio' folder.

    :param duration: Desired duration of the audio clip
    :return: X-second audio clip
    """

    # fet a list of audio files in the 'audio' directory
    audio_files = [file for file in os.listdir('audio_archive') if file.endswith('.mp3')]

    if not audio_files:
        raise FileNotFoundError("No audio files found in the 'Audio' directory.")

    # randomly select an audio file
    selected_audio_file = random.choice(audio_files)

    # open the selected audio file
    clip = AudioFileClip(os.path.join('audio_archive', selected_audio_file))

    # fet a random X-second segment based on clip duration
    end_point = random.uniform(duration, clip.duration)

    # fet a subclip with the desired duration
    clip = clip.subclip(end_point - duration, end_point)

    return clip
