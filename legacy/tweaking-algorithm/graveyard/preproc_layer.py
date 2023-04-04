from keras.layers import Layer
from tensorflow.python.util.tf_export import keras_export

@keras_export('keras.layers.experimental.preprocessing.Rescaling')
class PrintingLayer(Layer):
  """Multiply inputs by `scale` and adds `offset`.
  For instance:
  1. To rescale an input in the `[0, 255]` range
  to be in the `[0, 1]` range, you would pass `scale=1./255`.
  2. To rescale an input in the `[0, 255]` range to be in the `[-1, 1]` range,
  you would pass `scale=1./127.5, offset=-1`.
  The rescaling is applied both during training and inference.
  Input shape:
    Arbitrary.
  Output shape:
    Same as input.
  Arguments:
    scale: Float, the scale to apply to the inputs.
    offset: Float, the offset to apply to the inputs.
    name: A string, the name of the layer.
  """

  def __init__(self, name=None, **kwargs):
    super(PrintingLayer, self).__init__(name=name, **kwargs)

  def call(self, inputs):
    print("HEYEYEYYEYEYEYEYEYEY")
    return inputs[0][0]

  def compute_output_shape(self, input_shape):
    return input_shape