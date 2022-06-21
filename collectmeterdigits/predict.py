import tensorflow as tf
import numpy as np
import pkg_resources


def predict( image, model_path='cnn32-md-20220621-002622-q.tflite'):
    DATA_PATH = pkg_resources.resource_filename('collectmeterdigits', 'models/' + model_path)

    interpreter = tf.lite.Interpreter(model_path=DATA_PATH)
    interpreter.allocate_tensors()
    input_index = interpreter.get_input_details()[0]["index"]
    output_index = interpreter.get_output_details()[0]["index"]

    interpreter.set_tensor(input_index, np.expand_dims(np.array(image).astype(np.float32), axis=0))
    # Run inference.
    interpreter.invoke()
    output = interpreter.get_tensor(output_index)
    return np.argmax((output)[0])/10
        
    