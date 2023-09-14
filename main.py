""" main.py """

from sloth import *
from data import *
from generator import *


def main():
    data = random_data()

    generate_fact_video(12, {
        'topic': data[0].upper(),
        'captions': [data[1], data[2]],
        'channel': '@littlethoughtbites'
    })


if __name__ == '__main__':
    main()
