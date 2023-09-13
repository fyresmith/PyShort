""" main.py """

from sloth import *
from data import *


def main():
    data_set = random_data()

    template = retrieve_template('fact_video')
    template['text_elements']['topic']['text'] = data_set[0]
    template['text_elements']['part1']['text'] = data_set[1]
    template['text_elements']['part2']['text'] = data_set[2]
    template['text_elements']['channel']['text'] = '@littlethoughtbites'

    template_video(template, data_set[1] + ' #shorts')

    # generate_fact_video(data_set[0], data_set[1], data_set[2], '@littlethoughtbites')


if __name__ == '__main__':
    main()
