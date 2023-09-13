from sloth import *
import data


def main():
    data_set = data.random_data()

    generate_fact_video(data_set[0], data_set[1], data_set[2], '@littlethoughtbites')


if __name__ == '__main__':
    main()
