import tensorflow as tf
import numpy as np
import pkg_resources
from collectmeterdigits import glob

interpreter=None
internal_model_path = pkg_resources.resource_filename('collectmeterdigits', 'models/dig-s1-md-v1.2-q.tflite')

def load_interpreter(model_path):
    global interpreter
    print("Use model: " + model_path)
    
    interpreter = tf.lite.Interpreter(model_path=model_path)
    return interpreter

def predict( image):
    global interpreter

    if interpreter==None:
        if glob.model_path==None:
            glob.model_path=internal_model_path
        load_interpreter(glob.model_path)

    interpreter.allocate_tensors()
    input_index = interpreter.get_input_details()[0]["index"]
    input_shape = interpreter.get_input_details()[0]["shape"]
    output_index = interpreter.get_output_details()[0]["index"]

    image = image.resize((input_shape[2], input_shape[1]))
    
    interpreter.set_tensor(input_index, np.expand_dims(np.array(image).astype(np.float32), axis=0))
    # Run inference.
    interpreter.invoke()
    output = interpreter.get_tensor(output_index)
    print("Model=" + str(len(output[0])))
    if (len(output[0])==11):
        prediction = (np.argmax(output, axis=1).reshape(-1))[0]
    else:
        if (len(output[0])==10):
            _num = (np.argmax(output, axis=1).reshape(-1))[0]
            _numplus = (_num + 1) % 10
            _numminus = (_num - 1 + 10) % 10

            _val = output[0][_num]
            _valplus = output[0][_numplus]
            _valminus = output[0][_numminus]

            result = _num

            if (_valplus > _valminus):
                result = result + _valplus / (_valplus + _val)
                _fit = _val + _valplus
            
            else:
            
                result = result - _valminus / (_val + _valminus)
                _fit = _val + _valminus
            if (result >= 10):
                result = result - 10
            if (result < 0):
                result = result + 10
            prediction = result
        else:
            prediction = (np.argmax(output, axis=1).reshape(-1)/10)[0]
    return prediction
        
    