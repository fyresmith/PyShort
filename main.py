""" main.py """

from data import *
from generator import *
from youtube import *


def create_fact_video():
    data = caption_video_data()

    data['channel'] = '@truethoughtsdaily'

    file_path = generate_fact_video(10 if data['type'] == 'THREE' else 7, data)

    package = {
        'title': data['captions'][0] + '#shorts',
        'video': file_path,
        'description': '#truethoughtsdaily #inspiration #inspirationalquotes  #wisdomquotes #positivity '
                       '#dailyinspiration #shorts'
                       '#positivevibes #mindfulness #lifequotes #lovequotes #motivation #quotes #quoteoftheday '
                       '#quotesaboutlife #positivethinking #thoughtprovoking #thoughtfulreflections #thinking #thoughts'
                       '#thoughtfortheday #thoughtoftheday #thoughtfortoday #quotes #quotestoliveby #wisdomforliving '
                       '#wisdomquote',
        'tags': ['truethoughtsdaily ', 'inspiration ', 'inspirationalquotes  ', 'wisdomquotes ', 'positivity ',
                 'dailyinspiration ', 'shorts ', 'positivevibes ', 'mindfulness ', 'lifequotes ', 'lovequotes ',
                 'motivation', 'quotes ', 'quoteoftheday ', 'quotesaboutlife ', 'positivethinking ',
                 'thoughtprovoking ',
                 'thoughtfulreflections ', 'thinking ', 'thoughts ', 'thoughtfortheday ', 'thoughtoftheday ',
                 'thoughtfortoday ', 'quotes ', 'quotestoliveby ', 'wisdomforliving ', 'wisdomquote']
    }

    package_video(package)


if __name__ == '__main__':
    for i in range(50):
        create_fact_video()
