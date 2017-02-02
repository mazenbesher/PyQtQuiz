#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, os, random, re

from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *

class QuizBase(QWidget):
    # quiz options
    image_extensions = ('.jpg', '.png', '.gif', '.JPG', '.PNG', '.GIF')
    number_of_options = 4
    image_size = 600
    window_size = image_size + 100
    difficulty = "hard"  # options: ["easy", "hard"]

    # globals
    score = 0

    # init
    photos = []
    cwd = None
    curr_options = []

    # images
    right_path = None
    right = None
    options = set([])

    # UI
    options_box = None
    image_label = None
    grid = None
    score_label = None
    btns = []

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
        print("number_of_options:", self.number_of_options)
        print("image_size:",self.image_size)
        print("window_size:",self.window_size)
        print("difficulty:", self.difficulty)
        print('-' * 40)

    def remove_extension(self, s):
        # see CONVENTION 1
        # remove extension
        s = s[:s.find('.')]
        # remove number
        s = re.split(r"\s+\d+$", s)[0]
        return s

    def updateUI(self):
        self.new_random_image()

        pixmap = QPixmap(self.right_path)
        pixmap = pixmap.scaled(self.image_size, self.image_size, Qt.KeepAspectRatio)

        self.image_label.setPixmap(pixmap)

        for opt, btn in zip(self.curr_options, self.btns):
            btn.setText(opt)

    def new_random_image(self):
        # assure not extending the number of images
        if self.curr_question == len(self.photos) - self.number_of_options - 1:
            self.curr_question = 0
            random.shuffle(self.photos) # reshuffle

        # right image path (to load it later)
        self.right_path = os.path.join(self.cwd, self.photos[self.curr_question])

        # right answer and image randomly
        self.right = self.remove_extension(self.photos[self.curr_question])

        # add number_of_option to curr_options avoiding duplicates
        self.curr_options = []
        while len(self.curr_options) < (self.number_of_options - 1): # -1 because we already have the right option
            choice = self.select_random_image_from_options_set()
            if choice != self.right and not choice in self.curr_options:
                self.curr_options.append(choice)
        self.curr_options.append(self.right)
        random.shuffle(self.curr_options)

        self.curr_question += 1

    def select_random_image_from_options_set(self):
        # depends on difficulty
        if self.difficulty == "easy":
            return random.choice(list(self.options))
        elif self.difficulty == "hard":
            # select options "similar" to self.right
            sorted_options_list = sorted(list(self.options))
            right_index = sorted_options_list.index(self.right)

            case = random.randint(-5, 5)
            while case == 0:
                case = random.randint(-5, 5)
            """
            case \in [-5, 5] / {0}
            sign define direction (+ -> next, - -> prev)
            [1,2,3,4] -> index in sorted_options_list (similar)
                probability = 8 / 10 = 4 / 5
            5 -> random index in range(5, 10) from right in sorted_options_list (seim-similar)
                probability = 2 / 10 = 1 / 5
            """
            if abs(case) in [1,2,3,4]:
                return sorted_options_list[(right_index + case) % len(sorted_options_list)]
            elif abs(case) == 5:
                return sorted_options_list[(right_index + random.randint(-5, 5) + 5) % len(sorted_options_list)]

    def initUI(self):
        # fixed window size
        self.setFixedSize(self.window_size, self.window_size)

        # image
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        # options buttons
        self.options_box = QGroupBox(self)  # layout to display btns
        options_layout = QHBoxLayout(self)
        for i in range(self.number_of_options):
            btn = QPushButton(self)
            btn.clicked.connect(self.button_clicked)
            self.btns.append(btn)
            options_layout.addWidget(btn)  # widget, row, col
        self.options_box.setLayout(options_layout)

        # layout
        self.grid = QVBoxLayout(self)
        self.grid.setSpacing(10)

        # add widgets to grid in child class

        self.setLayout(self.grid)
        self.layout().setSizeConstraint(QLayout.SetFixedSize)  # fixed layout size
        self.resize(self.window_size, self.window_size)
        self.setWindowTitle('Photo Quiz')
        self.show()
