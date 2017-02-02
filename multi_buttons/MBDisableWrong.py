#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *

from multi_buttons.MBQuizBase import MBQuizBase

class MBDisableWrong(MBQuizBase):
    # globals
    wrong_answers = 0

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
        super().updateUI()
        self.update_score()

    def initUI(self):
        super().initUI()

        # score
        self.score_label = QLabel(str(self.score), self)

        self.grid.addWidget(self.score_label)
        self.grid.addWidget(self.options_box)
        self.grid.addWidget(self.image_label)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MBDisableWrong(sys.argv)
    sys.exit(app.exec_())
