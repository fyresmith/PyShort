from pytube import YouTube
import os


def populate_audio():
    """
    Populates the Audio folder with a set of audio files from YouTube

    :return:
    """

    urls = ['https://www.youtube.com/watch?v=NvwnIZX-1cs', 'https://www.youtube.com/watch?v=-iNHtdL-zu4',
            'https://www.youtube.com/watch?v=VGEbA_VQg1o', 'https://www.youtube.com/watch?v=_A0Beo0M-tQ',
            'https://www.youtube.com/watch?v=vQfTPbAaSjk', 'https://www.youtube.com/watch?v=iOOG2lFkMf0',
            'https://www.youtube.com/watch?v=Ip6cw8gfHHI', 'https://www.youtube.com/watch?v=1i8WJ8cRWsE',
            'https://www.youtube.com/watch?v=QCtEe-zsCtQ', 'https://www.youtube.com/watch?v=eKL3TceSxvk',
            'https://www.youtube.com/watch?v=qnFcVpItds4', 'https://www.youtube.com/watch?v=jKRW9ZV8QzI',
            'https://www.youtube.com/watch?v=mmO3KqoK1vU']

    # download videos
    for video in urls:
        download_audio(video)


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
