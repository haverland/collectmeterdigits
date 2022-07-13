import tensorflow as tf
import numpy as np
import pkg_resources

interpreter=None
internal_model_path = pkg_resources.resource_filename('collectmeterdigits', 'models/cnn32-md-20220621-002622-q.tflite')

def load_interpreter(model_path):
    global interpreter
    interpreter = tf.lite.Interpreter(model_path=model_path)
    return interpreter

def predict( image):
    global interpreter

    if interpreter==None:
        load_interpreter(internal_model_path)

    interpreter.allocate_tensors()
    input_index = interpreter.get_input_details()[0]["index"]
    input_shape = interpreter.get_input_details()[0]["shape"]
    output_index = interpreter.get_output_details()[0]["index"]

    image = image.resize((input_shape[2], input_shape[1]))
    
    interpreter.set_tensor(input_index, np.expand_dims(np.array(image).astype(np.float32), axis=0))
    # Run inference.
    interpreter.invoke()
    output = interpreter.get_tensor(output_index)
    return np.argmax((output)[0])/10
        
    