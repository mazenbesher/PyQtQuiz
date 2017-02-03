#!/usr/bin/python3
# -*- coding: utf-8 -*-

# TODO Errors of not enough images (otherwise infinite loop)
# TODO Tool tip the score how it works

import sys, os, random

from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *

from photo_quiz.QuizBase import QuizBase

class MPDisableWrong(QuizBase):
    # quiz options
    number_of_rows = 3
    number_of_cols = 4
    number_of_options = number_of_rows * number_of_cols
    image_size = 200
    window_size = image_size * max(number_of_cols, number_of_rows)
    question_font = QFont("Arial", 20)

    # globals
    curr_question = 0
    score = 0
    right_index = -1 # \in [0, len(self.btns)]
    wrong_answers = 0

    # UI
    score_label = None
    question_label = None

    def print_quiz_options(self):
        super().print_quiz_options()
        print("Multi Photos Quiz ---------------------")
        print("number_of_rows:", self.number_of_rows)
        print("number_of_cols:", self.number_of_cols)
        print("question_font:", self.question_font.toString())
        print("number_of_options:", self.number_of_options)
        print("image_size:",self.image_size)
        print("window_size:",self.window_size)
        print('-' * 40)

    def __init__(self, argv):
        # assert grid compatible layout
        assert(self.number_of_options <= self.number_of_cols * self.number_of_rows)

        super().__init__(argv)


    def initUI(self):
        # fixed window size
        self.setFixedSize(self.window_size, self.window_size)

        # score board
        self.score_label = QLabel(self)

        # question label
        self.question_label = QLabel(self)
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setFont(self.question_font)

        # images
        self.btns = []
        mapper = QSignalMapper(self) # map each btn with the current counter and send as parameter
        options_box = QGroupBox(self)  # layout to display images
        options_layout = QGridLayout(options_box)
        options_counter = 0
        for i in range(self.number_of_rows):
            for j in range(self.number_of_cols):
                if options_counter < self.number_of_options:
                    btn = QPushButton()
                    self.connect(btn, SIGNAL("clicked()"), mapper, SLOT("map()"))
                    mapper.setMapping(btn, options_counter) # call mapped(counter) on SIGNAL i.e. clicked
                    btn.setIconSize(QSize(self.image_size, self.image_size))
                    self.btns.append(btn)
                    options_layout.addWidget(btn, i, j, Qt.AlignCenter)
                    options_counter += 1
        self.connect(mapper, SIGNAL("mapped(int)"), self.button_clicked) # send counter as parameter
        options_box.setLayout(options_layout)

        grid = QVBoxLayout(self)
        grid.setSpacing(10) # vertical spacing since "V"Box

        self.setLayout(grid)
        self.layout().setSizeConstraint(QLayout.SetFixedSize)  # fixed layout size
        self.resize(self.window_size, self.window_size)
        self.setWindowTitle('Photo Quiz')
        self.show()

        grid.addWidget(self.score_label)
        grid.addWidget(self.question_label)
        grid.addWidget(options_box)

    def updateUI(self):
        # TODO maybe better randomizing algorithm
        # set right image
        self.right_index = random.randrange(len(self.btns))
        right_image = self.photos[self.curr_question]
        self.question_label.setText(self.remove_extension(right_image))
        right_path = os.path.join(self.cwd, right_image)
        self.btns[self.right_index].setIcon(QIcon(right_path))

        # update curr question
        self.curr_question += 1
        if self.curr_question == len(self.photos):
            self.curr_question = 0
            random.shuffle(self.photos) # reshuffle

        # set the other images TODO more efficient algorithm
        photos_no_right = self.photos
        photos_no_right.pop(self.curr_question) # avoid right image
        # avoid images with the same name as the right image (e.g. Apple 1, Apple 2, ...) see CONVENTION 1
        photos_no_right = [p for p in photos_no_right if self.remove_extension(p) != self.remove_extension(right_image)]

        options_images = random.sample(photos_no_right, self.number_of_options - 1)

        options_images_indexes = list(range(len(self.btns)))
        options_images_indexes.pop(self.right_index)

        for i in options_images_indexes:
            image = options_images.pop()
            path = os.path.join(self.cwd, image)
            self.btns[i].setIcon(QIcon(path))

        self.update_score()

    def button_clicked(self, btn_id):
        if btn_id == self.right_index:
            # update score if not only one option
            if self.wrong_answers < self.number_of_options - 1:
                self.score += 1

            # enable all btns
            for btn in self.btns:
                btn.setEnabled(True)

            # reset
            self.wrong_answers = 0

            self.updateUI()
        else:
            self.score -= 1
            self.wrong_answers += 1
            self.btns[btn_id].setEnabled(False)
            self.update_score() # no need to update the full UI just the score

    def update_score(self):
        new = 'Score {} / {}'.format(self.score, len(self.photos))
        self.score_label.setText(new)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MPDisableWrong(sys.argv)
    sys.exit(app.exec_())