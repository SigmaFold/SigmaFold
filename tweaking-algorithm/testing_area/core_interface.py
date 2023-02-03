import sys
from PySide6.QtWidgets import (
    QMainWindow,
    QApplication,
    QPushButton,
    QLabel
    )

# Custom imports
import gym
import inv_env

class mainAncestor(QMainWindow):
    def __init__(self):
        super(mainAncestor, self).__init__()

        self.setWindowTitle("TweakTest")
        self.resize(1000, 500)
        
        # Add env
        self._env = gym.make('inv_fold/PrimWorld-v0')

        # Add buttons

        # Create labels
        lbl_sequence_list = QLabel("fuck you", self)

        # Populate mwindow
        self.test = lbl_sequence_list

        self.show()



# Actually opening a window
App = QApplication(sys.argv)
window=mainAncestor()
App.exec()
