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

class Disable_Wrong(QWidget):
    image_extensions = ('.jpg', '.png', '.gif', '.JPG', '.PNG', '.GIF')
    number_of_options = 4
    image_size = 400
    window_size = image_size + 100
    score = 0
    curr_question = 0
    wrong_answers = 0
    difficulty = "hard" # options: ["easy", "hard"]

    # init
    photos = []
    cwd = None
    curr_options = []

    # images
    right_path = None
    options = set([])
    right = None

    # UI
    image_label = None
    grid = None
    score_label = None
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

    def remove_extension(self, s):
        # see CONVENTION 1
        # remove extension
        s = s[:s.find('.')]
        # remove number
        s = re.split(r"\s+\d+$", s)[0]

        return s

    def update_score(self):
        new = 'Score {} / {}'.format(self.score, len(self.photos))
        self.score_label.setText(new)

    def button_clicked(self):
        clicked_btn = self.sender()
        selected_option = clicked_btn.text()
        if selected_option == self.right:
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
            clicked_btn.setEnabled(False)
            self.update_score() # no need to update the full UI just the score

    def updateUI(self):
        self.new_random_image()

        pixmap = QPixmap(self.right_path)
        pixmap = pixmap.scaled(self.image_size, self.image_size, Qt.KeepAspectRatio)

        self.image_label.setPixmap(pixmap)

        for opt, btn in zip(self.curr_options, self.btns):
            btn.setText(opt)

        self.update_score()

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
                probability = 8 / 10
            5 -> random index in range(5, 10) from right in sorted_options_list (seim-similar)
                probability = 2 / 10
            """
            if abs(case) in [1,2,3,4]:
                return sorted_options_list[(right_index + case) % len(sorted_options_list)]
            elif abs(case) == 5:
                return sorted_options_list[(right_index + random.randint(-5, 5) + 5) % len(sorted_options_list)]

    def initUI(self):
        # image
        self.image_label = QLabel(self)

        # score
        self.score_label = QLabel(str(self.score), self)

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
        self.grid.addWidget(options_box)
        self.grid.addWidget(self.image_label)

        self.setLayout(self.grid)
        self.resize(self.window_size, self.window_size)
        self.setWindowTitle('Photo Quiz')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Disable_Wrong(sys.argv)
    sys.exit(app.exec_())
