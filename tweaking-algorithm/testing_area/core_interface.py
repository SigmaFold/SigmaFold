import sys
from PySide6.QtWidgets import (
    QMainWindow,
    QApplication,
    QLabel,
    QGridLayout,
    QFrame,
    QPushButton,
    QWidget,
    QTableView,
    QDoubleSpinBox,
    )
from PySide6 import QtCore
from PySide6.QtCore import QAbstractTableModel, Qt 
# Custom imports
import gym
# import inv_env

import sys, os

# Set current working directory to be 2 levels above the current file
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from inv_env.envs.aux_functions import *
print(sys.path) 

class mainAncestor(QWidget):
    def __init__(self):
        super(mainAncestor, self).__init__()
        
        # Root attributes
        self.setWindowTitle("TweakTest")
        self.resize(500, 500)
        layout = QGridLayout()
        
        # Add env
        self._env = gym.make('inv_fold/TweakWorld-v0')

        # Create widgets
        lbl_seq = QLabel("Sequence will appear here")
        lbl_seq.setFrameStyle(QFrame.Panel)
        lbl_seq.setLineWidth(2)
        lbl_seq.setFixedSize(500, 200)
        lbl_seq.setAlignment(QtCore.Qt.AlignCenter)

        btn_init = QPushButton("New env")
        btn_init.clicked.connect(self._dummy)

        btn_submit = QPushButton("Submit")
        btn_submit.clicked.connect(self._dummy)

        action_input = QDoubleSpinBox()
        
        # Shape viewer
        target_tbl = ShapeDisplay([0])
        table = QTableView()
        table.setModel(target_tbl)

        seq_tbl = ShapeDisplay([0])
        table2 = QTableView()
        table2.setModel(seq_tbl)
        
        # Populate mwindow
        layout.addWidget(lbl_seq, 1, 1, 2, 2)
        layout.addWidget(btn_init, 3, 2)
        layout.addWidget(action_input, 5, 2)
        layout.addWidget(btn_submit, 6, 2)

        layout.addWidget(table, 3, 1, 2, 1)
        layout.addWidget(table2, 5, 1, 2, 1)

        self.setLayout(layout)

    def _do_action(self):
        print("I was summoned...")

    def _init_env(self):
        out = self._env.reset()
        print(self._env.decode(out[0][1]))

    def _dummy(self):
        print("stfu")

class ShapeDisplay(QAbstractTableModel):

    def __init__(self, data):
        super(ShapeDisplay, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

# Actually opening a window
App = QApplication(sys.argv)
window=mainAncestor()
window.show()
App.exec()
