#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, os, random, re

from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *

from photo_quiz.QuizBase import QuizBase

class MPDisableWrong(QuizBase):
    # quiz options
    number_of_rows = 2
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

        mapper = QSignalMapper(self)

        options_box = QGroupBox(self)  # layout to display images
        options_layout = QGridLayout(options_box)
        options_counter = 0
        for i in range(self.number_of_rows):
            for j in range(self.number_of_cols):
                if options_counter < self.number_of_options:
                    btn = QPushButton()
                    self.connect(btn, SIGNAL("clicked()"), mapper, SLOT("map()"))
                    mapper.setMapping(btn, options_counter)
                    btn.setIconSize(QSize(self.image_size, self.image_size))
                    self.btns.append(btn)
                    options_layout.addWidget(btn, i, j, Qt.AlignCenter)
                    options_counter += 1
        self.connect(mapper, SIGNAL("mapped(int)"), self.button_clicked)
        options_box.setLayout(options_layout)

        grid = QVBoxLayout(self)
        grid.setSpacing(10)

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

        # set the other images
        for i in range(self.number_of_options):
            if i != self.right_index:
                # avoid right image and image with same name
                image = random.choice(self.photos)
                while image == right_image or self.remove_extension(image) == self.remove_extension(right_image):
                    image = random.choice(self.photos)
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