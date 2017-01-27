#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" CONVENTION 1
number at the end of images names will be ignored
Example:
    Apple.jpg   -> Apple
    Apple 2.png -> Apple
"""

# TODO Repeat wrong answers more
# TODO No need create new box each time, same buttons reus

import sys, os, random, re

from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *

class Right_Wrong(QWidget):
    image_extensions = ('.jpg', '.png', '.gif', '.JPG', '.PNG', '.GIF')
    number_of_options = 4
    image_size = 400
    window_size = image_size + 100
    score = 0
    curr_question = 0

    # init
    photos = []
    info = ''
    cwd = None

    # images
    right_path = None
    options = None
    right = None

    # UI
    image_label = None
    grid = None
    score_label = None
    info_box = None
    btns = []

    def __init__(self, argv):
        super().__init__()
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

        # random order
        random.shuffle(self.photos)

        # assert more than number_of_options images
        assert (len(self.photos) >= self.number_of_options)

        # UI
        self.initUI()
        self.updateUI()

    def remove_extension(self, s):
        # see CONVENTION 1
        # remove extension
        s = s[:s.find('.')]
        # remove number
        s = re.split(r"\s+\d+$", s)[0]

        return s

    def get_score(self):
        return 'Score {} / {}'.format(self.score, len(self.photos))

    def button_clicked(self):
        selected_option = self.sender().text()
        if selected_option == self.right:
            self.score += 1
            self.info += 'RIGHT, Answer was {}'.format(self.right)
        else:
            self.score -= 1
            self.info += 'Wrong, Answer was {}'.format(self.right)
        self.updateUI()

    def updateUI(self):
        self.new_random_image()

        pixmap = QPixmap(self.right_path)
        pixmap = pixmap.scaled(self.image_size, self.image_size, Qt.KeepAspectRatio)

        self.image_label.setPixmap(pixmap)

        for opt, btn in zip(self.options, self.btns):
            btn.setText(self.remove_extension(opt))

        self.score_label.setText(self.get_score())
        self.info_box.setText(self.info)
        self.info = ''

    def new_random_image(self):
        # assure not extending the number of images
        if self.curr_question == len(self.photos) - self.number_of_options - 1:
            self.curr_question = 0
            random.shuffle(self.photos) # reshuffle

        # right image path (to load it later)
        self.right_path = os.path.join(self.cwd, self.photos[self.curr_question])

        # right answer and image randomly
        self.right = self.remove_extension(self.photos[self.curr_question])

        self.options = self.photos[self.curr_question:self.curr_question + self.number_of_options]
        random.shuffle(self.options)

        self.curr_question += 1

    def initUI(self):
        # image
        self.image_label = QLabel(self)

        # score
        self.score_label = QLabel(self.get_score(), self)

        # info
        self.info_box = QLabel(self)

        # options buttons
        options_box = QGroupBox(self)  # layout to display btns
        options_layout = QHBoxLayout(self)
        for i in range(self.number_of_options):
            btn = QPushButton(self)
            btn.clicked.connect(self.button_clicked)
            self.btns.append(btn)
            options_layout.addWidget(btn)  # widget, row, col
        options_box.setLayout(options_layout)

        # layout
        self.grid = QVBoxLayout(self)
        self.grid.setSpacing(10)

        self.grid.addWidget(self.score_label)
        self.grid.addWidget(self.info_box)
        self.grid.addWidget(options_box)
        self.grid.addWidget(self.image_label)

        self.setLayout(self.grid)
        self.resize(self.window_size, self.window_size)
        self.setWindowTitle('Photo Quiz')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Right_Wrong(sys.argv)
    sys.exit(app.exec_())
