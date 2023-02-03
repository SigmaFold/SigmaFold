import tensorflow as tf 
import tensorflow.keras.backend as K 

class MyAdam(tf.keras.optimizers.Optimizer):
    """Custom Adam optimizer that is compatible with the Keras RL DQNAgent."""
    def __init__(self, learning_rate=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-7, name="mytest", **kwargs):
        self.learning_rate = learning_rate
        super(MyAdam, self).__init__(name, **kwargs)
        with tf.keras.backend.name_scope(self.__class__.__name__):

            self.iterations = tf.keras.backend.variable(0, dtype='int64', name='iterations')
            self.learning_rate = tf.keras.backend.variable(learning_rate, name='learning_rate')
            self.beta_1 = tf.keras.backend.variable(beta_1, name='beta_1')
            self.beta_2 = tf.keras.backend.variable(beta_2, name='beta_2')
            self.epsilon = tf.keras.backend.variable(epsilon, name='epsilon')

    def get_updates(self, loss, params):
        grads = tf.gradients(loss, params)
        self.updates = [tf.keras.backend.update_add(self.iterations, 1)]

        lr = self.learning_rate * (tf.keras.backend.sqrt(1. - tf.keras.backend.pow(self.beta_2, self.iterations)) /
                                   (1. - tf.keras.backend.pow(self.beta_1, self.iterations)))

        t = tf.cast(self.iterations, tf.float32) + 1
        lr_t = lr * (tf.keras.backend.sqrt(1. - tf.keras.backend.pow(self.beta_2, t)) /
                     (1. - tf.keras.backend.pow(self.beta_1, t)))

        for p, g in zip(params, grads):
            m = tf.keras.backend.zeros(shape=tf.keras.backend.int_shape(p), dtype=tf.dtypes.float32)
            v = tf.keras.backend.zeros(shape=tf.keras.backend.int_shape(p), dtype=tf.dtypes.float32)

            m_t = (self.beta_1 * m) + (1. - self.beta_1)

class CustomAdam(tf.keras.optimizers.Optimizer):

    def __init__(self, lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-7, name='dcdc', **kwargs):
        self._learning_rate = lr
        self._name = name
        super(CustomAdam, self).__init__(name, **kwargs)
        self.lr = tf.keras.backend.variable(lr, name='lr')
        self.beta_1 = tf.keras.backend.variable(beta_1, name='beta_1')
        self.beta_2 = tf.keras.backend.variable(beta_2, name='beta_2')
        self.epsilon = epsilon

    def get_updates(self, loss, params):
        grads = self.get_gradients(loss, params)
        self.updates = [K.update_add(self.iterations, 1)]

        t = K.cast(self.iterations, K.floatx()) + 1
        lr_t = self.lr * (K.sqrt(1. - K.pow(self.beta_2, t)) /
                         (1. - K.pow(self.beta_1, t)))

        for p, g in zip(params, grads):
            m = K.zeros(K.int_shape(p), dtype=K.floatx())
            v = K.zeros(K.int_shape(p), dtype=K.floatx())

            m_t = (self.beta_1 * m) + (1. - self.beta_1) * g
            v_t = (self.beta_2 * v) + (1. - self.beta_2) * K.square(g)
            p_t = p - lr_t * m_t / (K.sqrt(v_t) + self.epsilon)

            self.updates.append(K.update(m, m_t))
            self.updates.append(K.update(v, v_t))
            self.updates.append(K.update(p, p_t))
        return self.updates

    def get_gradients(self, loss, params):
        return K.gradients(loss, params)