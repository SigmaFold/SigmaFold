import sys, os
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QGridLayout,
    QFrame,
    QPushButton,
    QWidget,
    QDoubleSpinBox,
    )
from PySide6 import QtCore

import gym
from inv_env import register # required
import matplotlib.pylab as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

# Set current working directory to be 2 levels above the current file
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from inv_env.envs.aux_functions import *

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
        btn_submit.clicked.connect(self._do_action)

        self.action_input = QDoubleSpinBox()
        
        # Shape viewer
        self.shape_img = matrixCanvas(self, width=5, height=5, dpi=100)
        self.shape_img.axes.imshow([[0]],
                            interpolation='nearest', cmap=plt.cm.ocean)

        self.target_img = matrixCanvas(self, width=5, height=5, dpi=100)
        self.target_img.axes.imshow([[1]],
                            interpolation='nearest', cmap=plt.cm.ocean)
        
        # Populate mwindow
        # row, col, row_span, col_span
        self.layout.addWidget(self.seq_label, 1, 1, 2, 2)
        self.layout.addWidget(btn_init, 3, 2)
        self.layout.addWidget(btn_init, 4, 2)
        self.layout.addWidget(self.action_input, 5, 2)
        self.layout.addWidget(btn_submit, 6, 2)

        self.layout.addWidget(self.shape_img, 3, 1, 2, 1)
        self.layout.addWidget(self.target_img, 5, 1, 2, 1)
        
        ### Data storage-related variables
        # Batch only stores human-readable data:
        # Degeneracy (int) - Correlation (int) - Target (matrix) - Seq (list)
        self.new_batch_info = {'seq_list': []}
        self.current_batch_info = {'seq_list': []}

        # Final step
        self.setLayout(self.layout)
    
    ### BUTTONS ACTIONS
    def _do_action(self):
        action_id = int(self.action_input.value())
        resp = self._env.step(action_id)
        self._update_ui(resp)

    def _init_env(self):
        self.new_batch = self._env.reset()
        new_batch_obs = self.new_batch[0]
        new_batch_info = self.new_batch[1]

        # Initialise target shape
        target = new_batch_obs[1]
        self.target_img.axes.clear()
        self.target_img.axes.imshow(target, cmap=plt.cm.ocean)
        self.target_img.draw()

        self.current_batch_info = new_batch_info
        self._update_seq_label()

    def _update_ui(self, resp):
        obs, reward, done, info = resp
        
        # Shift batch info
        # self.current_batch_info = self.new_batch_info
        self.new_batch_info = info

        # Update folded sequence:
        self.shape_img.axes.clear()
        print(info['fold'])
        self.shape_img.axes.imshow(info['fold'])
        self.shape_img.draw()

        self._update_seq_label()

    def _update_seq_label(self):
        pre_seq_str = ''.join([str(x) for x in self.current_batch_info['seq_list']])
        post_seq_str = ''.join([str(x) for x in self.new_batch_info['seq_list']])
        self.seq_label.setText(f'Before: {pre_seq_str} \n After: {post_seq_str}')
        self.seq_label.update()

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
