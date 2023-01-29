import tensorflow as tf

def build_model(states, actions):
    """
    Function that sets up the Neural Network. 
    Input Layer: state space
    2 densly connected layers
    Output Layer: action space
    """


    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(3,)),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(20, activation='softmax')
    ])

    return model