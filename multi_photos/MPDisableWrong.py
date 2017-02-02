#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" CONVENTION 1
number at the end of images names will be ignored
Example:
    Apple.jpg   -> Apple
    Apple 2.png -> Apple
"""

import sys, os, random, re

from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *

from QuizBase import QuizBase


class MPDisableWrong(QuizBase):
    # quiz options
    number_of_rows = 2
    number_of_cols = 4
    number_of_options = number_of_rows * number_of_cols
    image_size = 100
    window_size = image_size * max(number_of_cols, number_of_rows)

    # UI
    score_label = None
    question_label = None

    def __init__(self, argv):
        # assert grid compatible layout
        assert(self.number_of_options == self.number_of_cols * self.number_of_rows)

        super().__init__(argv)


    def initUI(self):
        # fixed window size
        self.setFixedSize(self.window_size, self.window_size)

        # score board
        self.score_label = QLabel(self)

        # question label
        self.question_label = QLabel(self)

        # images
        options_box = QGroupBox(self)  # layout to display images
        options_layout = QGridLayout(options_box)
        for i in range(self.number_of_rows):
            for j in range(self.number_of_cols):
                pass

    def updateUI(self):
        pass



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MPDisableWrong(sys.argv)
    sys.exit(app.exec_())