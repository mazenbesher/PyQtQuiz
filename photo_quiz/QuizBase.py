#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" CONVENTION 1
number at the end of images names will be ignored
Example:
    Apple.jpg   -> Apple
    Apple 2.png -> Apple
"""

import os, random, re

from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *

class QuizBase(QWidget):
    # quiz options
    image_extensions = ('.jpg', '.png', '.gif', '.JPG', '.PNG', '.GIF')
    number_of_options = 4

    # init
    photos = []
    cwd = None
    options = set([])

    def __init__(self, argv):
        super().__init__()
        # print options
        self.print_quiz_options()

        # get images directory (argv or browse for directory)
        if len(argv) > 1: # not just the name of the program
            self.cwd = argv[1]
        else:
            self.cwd = str(QFileDialog.getExistingDirectory(self, "Select Directory")) # browse
        print("Directory:", self.cwd)

        # get list of file names
        photos = os.listdir(self.cwd)
        print("Found {} Files".format(len(photos)))

        # filter just images (.png, .jpg)
        not_loaded = []
        for p in photos:
            if p.endswith(self.image_extensions):
                self.photos.append(p)
            else:
                not_loaded.append(p)

        print("Loaded {} Photos".format(len(self.photos)))
        print("Not loaded:", not_loaded)

        # generate options
        for image_name in self.photos:
            self.options.add(self.remove_extension(image_name))

        print("Unique options:", len(self.options))

        # check number of options (not enough options)
        assert(len(self.options) >= self.number_of_options)

        # random order
        random.shuffle(self.photos)

        # assert more than number_of_options images (number of images less than number_of_options images)
        assert (len(self.photos) >= self.number_of_options)

        # UI
        self.initUI()
        self.updateUI()

    def print_quiz_options(self):
        print("Quiz options a.k.a the magic numbers :P")
        print("image_extensions:", self.image_extensions)

    def remove_extension(self, s):
        # see CONVENTION 1
        # remove extension
        s = s[:s.find('.')]
        # remove number
        s = re.split(r"\s+\d+$", s)[0]
        return s