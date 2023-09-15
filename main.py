""" main.py """

from data import *
from generator import *


def main():
    # data = random_data()

    generate_fact_video(10, {
        'topic': 'Love Fact',
        'captions': ["Love is the language that transcends words...", "...it's the unspoken poetry of the heart...", "...and the warmth that envelops your soul."],
        'channel': '@awesomechannel'
    })


    # generate_fact_video(12, {
    #     'topic': data[0].upper(),
    #     'captions': [data[1], data[2]],
    #     'channel': '@littlethoughtbites'
    # })

    data = random_data()

    generate_fact_video(12, {
        'topic': data[0].upper(),
        'captions': [data[1], data[2]],
        'channel': '@littlethoughtbites'
    })


if __name__ == '__main__':
    main()
