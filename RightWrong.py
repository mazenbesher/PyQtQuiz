#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" CONVENTION 1
number at the end of images names will be ignored
Example:
    Apple.jpg   -> Apple
    Apple 2.png -> Apple
"""

# TODO Repeat wrong answers more

import sys, os, random, re

from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *

from QuizBase import QuizBase


class RightWrong(QuizBase):
    # globals
    curr_question = 0

    # init
    info = ''

    # UI
    info_box = None

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
        super().updateUI()
        self.score_label.setText(self.get_score())
        self.info_box.setText(self.info)
        self.info = ''

    def initUI(self):
        super().initUI()

        # score
        self.score_label = QLabel(self.get_score(), self)

        # info
        self.info_box = QLabel(self)

        self.grid.addWidget(self.score_label)
        self.grid.addWidget(self.info_box)
        self.grid.addWidget(self.options_box)
        self.grid.addWidget(self.image_label)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RightWrong(sys.argv)
    sys.exit(app.exec_())
