import sys, os
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
from inv_env import register
import matplotlib.pylab as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

# Set current working directory to be 2 levels above the current file
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from inv_env.envs.aux_functions import *

# Test data
H = np.array([[100, 2, 39, 190], [402, 55, 369, 1023], [300, 700, 8, 412], [170, 530, 330, 1]])
Z = np.array([[3, 290, 600, 480], [1011, 230, 830, 0], [152, 750, 5, 919], [340, 7, 543, 812]])

class mainAncestor(QWidget):
    def __init__(self):
        super(mainAncestor, self).__init__()
        
        # Root attributes
        self.setWindowTitle("Tweaking Agent - Debugging Area")
        self.resize(500, 500)
        self.layout = QGridLayout()
        
        # Add env
        self._env = gym.make('inv_fold/TweakWorld-v0')

        # Test data
        self.figure = plt.figure()
        self.canvas = FigureCanvasQTAgg(self.figure)

        # Create widgets
        self.seq_label = QLabel("Sequence will appear here")
        self.seq_label.setFrameStyle(QFrame.Panel)
        self.seq_label.setLineWidth(2)
        self.seq_label.setFixedSize(500, 200)
        self.seq_label.setAlignment(QtCore.Qt.AlignCenter)

        btn_init = QPushButton("New env")
        btn_init.clicked.connect(self._init_env)

        btn_submit = QPushButton("Submit")
        btn_submit.clicked.connect(self._dummy)

        action_input = QDoubleSpinBox()
        
        # Shape viewer
        self.shape_img = matrixCanvas(self, width=5, height=5, dpi=100)
        self.shape_img.axes.imshow([[0,1,2,3,4], [10,1,20,3,40]],
                            interpolation='nearest', cmap=plt.cm.ocean)

        self.target_img = matrixCanvas(self, width=5, height=5, dpi=100)
        self.target_img.axes.plot([0,1,2,3,4], [10,1,20,3,40])
        
        # Populate mwindow
        # row, col, row_span, col_span
        self.layout.addWidget(self.seq_label, 1, 1, 2, 2)
        self.layout.addWidget(btn_init, 3, 2)
        self.layout.addWidget(btn_init, 4, 2)
        self.layout.addWidget(action_input, 5, 2)
        self.layout.addWidget(btn_submit, 6, 2)

        self.layout.addWidget(self.shape_img, 3, 1, 2, 1)
        self.layout.addWidget(self.target_img, 5, 1, 2, 1)
        
        ### Data storage-related variables
        self.new_batch = None
        self.current_batch = ["", "", "", ""]

        # Final step
        self.setLayout(self.layout)
    
    ### BUTTONS ACTIONS
    def _do_action(self):
        print("I was summoned...")

    def _init_env(self):
        self.new_batch = self._env.reset()

        # Initialise target shape
        target = self.new_batch[0][1]
        self.target_img.axes.clear()
        self.target_img.axes.imshow(target, cmap=plt.cm.ocean)
        self.target_img.draw()

        # Update label
        self.seq_label.setText("Hey \n fucker")
        self.seq_label.update()
    def _update_ui(self):
        new_fold = self.new_batch[0][1]        

    def _dummy(self):
        print("stfu")

class  matrixCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(matrixCanvas, self).__init__(fig)

        
# Actually opening a window
App = QApplication(sys.argv)
window=mainAncestor()
window.show()
App.exec()
