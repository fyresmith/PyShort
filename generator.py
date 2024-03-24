#!/usr/bin/env python

"""
generator.py

Python script which takes input for video, audio, and data and compiles them into videos.
"""

import subprocess
from moviepy.editor import *
from video import *
from audio import *

__author__ = "Caleb Smith"
__credits__ = ["Caleb Smith"]
__version__ = "1.0"
__maintainer__ = "Caleb Smith"
__email__ = "me@calebmsmith.com"
__status__ = "Development"


class Element:
    def __init__(self, **kwargs):
        """
        Constructor for the Element class.

        :param kwargs: keyword arguments with which to build the instance
        :return: None
        """

        # default fields for an Element
        self.fields = {
            'text': '',
            'text_color': 'white',
            'text_type': 'label',
            'font': 'Lato-Bold',
            'font_size': 50,
            'box_size': (None, None),
            'bg_opacity': 1.0,
            'bg_padding': (60, 40),
            'bg_color': (0, 0, 0),
            'radius': 30,
            'stroke_color': None,
            'stroke_width': 0,
            'position': ('center', 'center'),
            'start': 0,
            'duration': 5
        }

        # initialize fields based on provided keyword arguments
        for key, value in kwargs.items():
            if key in self.fields:
                self.__setitem__(key, value)

        self._clip = None
        self.update_clip()

    @classmethod
    def from_dict(cls, import_dict):
        """
        Method to create an Element from a dictionary

        :param import_dict: imported dictionary
        :return: created instance
        """

        element = cls()
        element.import_values(import_dict)
        return element

    def __setitem__(self, key: str, value):
        """
        Method to set a field's value and perform type and value checks

        :param key: key with which to set value
        :param value: value to be set
        :return: None
        """

        # define expected types and value checks for fields
        field_checks = {
            'text': (str, None),
            'text_color': (str, None),
            'text_type': (str, None),
            'font': (str, None),
            'box_size': (tuple, lambda v: len(v) == 2),
            'bg_padding': (tuple, lambda v: len(v) == 2),
            'bg_color': (tuple, lambda v: len(v) == 3 and all(isinstance(x, int) for x in v)),
            'font_size': (int, lambda v: v >= 0),
            'radius': (int, lambda v: v >= 0),
            'stroke_width': (int, lambda v: v >= 0),
            'bg_opacity': (float, lambda v: 0 <= v <= 1.0),
            'start': (float, lambda v: v >= 0),
            'duration': (float, lambda v: v >= 0),
        }

        expected_type, value_check = field_checks.get(key, (None, None))

        if expected_type is not None:
            if not isinstance(value, expected_type):
                if expected_type == float and type(value) is int:
                    pass
                else:
                    raise TypeError(f'Expected type {expected_type.__name__} for field: "{key}"')

            if value_check is not None and not value_check(value):
                raise ValueError(f'Invalid value for field: "{key}"')

        self.fields[key] = value
        self.update_clip()

    def __getitem__(self, item: str):
        """
        Method to get a field's value

        :param item: key to access value
        :return: value
        """

        return self.fields[item]

    def update_clip(self):
        """
        Method to update the clip associated with this Element
        :return: None
        """
        self._clip = generate_text(**self.fields)

    # method to import values from a dictionary
    def import_values(self, import_dict):
        for key, value in import_dict.items():
            if key in self.fields:
                self.__setitem__(key, value)

    def export_values(self):
        """
        Method to export field values as a dictionary
        :return: field values
        """
        return self.fields

    def get_clip(self):
        """
        Method to get the associated clip
        :return: clip
        """
        return self._clip

    def to_image(self, filename):
        """
        Method to save the clip as an image
        :param filename: name for the file
        :return: None
        """
        self._clip.save_frame(filename)

    def to_string(self):
        """
        Method to convert the Element to a string representation
        :return: returns a string representing Element
        """
        key_str = ", ".join(f"{key}={self.__getitem__(key)!r}" for key in self.fields.keys())
        return f"Element({key_str})"


# class representing a video composition
class Short:
    def __init__(self, video: VideoClip, audio: AudioClip):
        """
        Constructor for the Short class
        :param video: a video clip
        :param audio: an audio clip
        :return: None
        """
        self._elements = []
        self._video = video
        self._audio = audio

    def add_element(self, element: Element):
        """
        Method to add an Element to the composition
        :param element: pre-created Element
        :return: None
        """
        self._elements.append(element)

    def add(self, **kwargs):
        """
        Method to add a new Element to the composition
        :param kwargs: new Element arguments
        :return: None
        """
        self._elements.append(Element(**kwargs))

    def get_pool(self):
        """
        Method to get the list of Elements in the composition
        :return: the list of elements
        """
        return self._elements

    def export_dict(self):
        """
        Method to export Elements as a dictionary
        :return: Elements as a dictionary
        """
        elements = {}

        for i in range(len(self._elements)):
            elements[str(i)] = self._elements[i].export_values()

        return elements

    def import_dict(self, elements: dict):
        """
        Method to import Elements from a dictionary
        :param elements: element dictionary
        :return: None
        """
        for element in elements:
            self.add_element(Element.from_dict(element))

    def set_audio(self, audio: AudioClip):
        """
        Method to set the audio for the composition
        :param audio: audio clip
        :return: None
        """
        self._audio = audio

    def get_audio(self):
        """
        Method to get the audio of the composition
        :return: audio clip
        """
        return self._audio

    def set_video(self, video: VideoClip):
        """
        Method to set the video for the composition
        :param video: video clip
        :return: None
        """
        self._video = video

    def get_video(self):
        """
        Method to get the video of the composition
        :return: video clip
        """
        return self._video

    def compile_elements(self):
        """
        Method to compile the elements into a composite video
        :return: compiled video clip
        """
        compiled_elements = [self._video]

        for element in self._elements:
            compiled_elements.append(element.get_clip())

        return CompositeVideoClip(compiled_elements).set_duration(self._video.duration)

    def render(self, title: str):
        """
        Method to render the composition to a video file
        :param title: title of the video
        :return: None
        """

        # write to temporary files
        self.compile_elements().write_videofile('temp.mp4')
        self._audio.write_audiofile('temp.mp3')

        # construct command
        command = ['ffmpeg',
                   '-y',
                   '-i', "temp.mp4",
                   '-i', "temp.mp3",
                   '-c:v', 'copy',
                   '-c:a', 'aac',
                   '-shortest',
                   'output/' + title + '.mp4']

        # run the ffmpeg command
        subprocess.run(command)

        # remove temporary files
        os.remove('temp.mp3')
        os.remove('temp.mp4')


def export_video(filename: str, video: VideoClip, audio: AudioClip):
    """
    Exports a video given the filename, video component, and audio component.

    :param filename: name for the new file
    :param video: video clip
    :param audio: audio clip
    :return: None
    """

    # write to temporary files
    video.write_videofile('temp.mp4')
    audio.write_audiofile('temp.mp3')

    # construct command
    command = ['ffmpeg',
               '-y',
               '-i', "temp.mp4",
               '-i', "temp.mp3",
               '-c:v', 'copy',
               '-c:a', 'aac',
               '-shortest',
               filename]

    # run ffmpeg command
    subprocess.run(command)

    # remove temporary files
    os.remove('temp.mp3')
    os.remove('temp.mp4')


def generate_fact_video(duration: float, data: dict, transition_timing=0.5):
    """
    Function to generate a video based on data

    :param duration: duration of the video
    :param data: data to be displayed
    :param transition_timing: transition timing between captions
    :return: None
    """
    # create a Short object with random video and audio clips
    short = Short(random_video_clip(duration), random_audio_clip(duration))

    # add a title Element
    short.add(text=data['topic'],
              font_size=83,
              radius=20,
              text_color='black',
              bg_color=(255, 255, 255),
              font='Oswald-Medium',
              position=('center', 200),
              duration=duration)

    num_captions = len(data['captions'])

    # calculate the duration for each segment (except the last one)
    segment_duration = (duration - transition_timing * (num_captions - 1)) / num_captions

    for i in range(num_captions):
        if i == num_captions - 1:
            # last segment covers the remaining duration
            segment_end = duration
        else:
            # calculate the end time for this segment
            segment_end = i * (segment_duration + transition_timing) + segment_duration

        # add a caption Element for each segment
        short.add(
            text=data['captions'][i],
            font='Lato-Black',
            radius=0,
            box_size=(720, None),
            font_size=75,
            bg_opacity=0,
            text_color='white',
            stroke_color='black',
            text_type='caption',
            stroke_width=3,
            position=('center', 'center'),
            start=i * (segment_duration + transition_timing),
            duration=segment_end - (i * (segment_duration + transition_timing))
        )

    # add a footer credit Element
    short.add(text=data['channel'],
              font_size=50,
              text_type='label',
              bg_padding=(60, 30),
              radius=25,
              position=('center', 1600),
              duration=duration)

    # render the video
    short.render(data['captions'][0] + ' #shorts')

    return 'output/' + data['captions'][0] + ' #shorts.mp4'
