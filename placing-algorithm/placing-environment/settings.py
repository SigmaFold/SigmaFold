LEFT = 0
UP = 1
RIGHT = 2
DOWN = 3
NOTHING_LEFT = 4
NOTHING_RIGHT = 5
NOTHING_UP = 6
NOTHING_DOWN = 7

# Actions dictionary - Defines the action space also so important
epsilon = 0.1

actions_dict = {
    LEFT: 'left',
    UP: 'up',
    RIGHT: 'right',
    DOWN: 'down',
    NOTHING_LEFT: 'nothing_left',
    NOTHING_RIGHT: 'nothing_right',
    NOTHING_UP: 'nothing_up',
    NOTHING_DOWN: 'nothing_down'

}
num_actions = len(actions_dict)