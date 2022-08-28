try:
    import tflite_runtime.interpreter as tflite
    has_tflite_runtime = True
except ImportError:
    try:
        import tensorflow.lite as tflite
        has_tflite_runtime = True
    except ImportError:
        has_tflite_runtime = False
import numpy as np
import pkg_resources
from collectmeterdigits import glob

interpreter=None
internal_model_path = pkg_resources.resource_filename('collectmeterdigits', 'models/cnn32-md-20220621-002622-q.tflite')

def load_interpreter(model_path):
    global interpreter
    print("Use model: " + model_path)
    if (glob.model_path=="off"):
        return
    interpreter = tflite.Interpreter(model_path=model_path)
    return interpreter



def predict( image):
    global interpreter

    if (has_tflite_runtime and not glob.model_path=="off" ):
        
        if interpreter==None:
            if glob.model_path==None:
                glob.model_path=internal_model_path
            load_interpreter(glob.model_path)

        interpreter.allocate_tensors()
        input_index = interpreter.get_input_details()[0]["index"]
        output_index = interpreter.get_output_details()[0]["index"]

        interpreter.set_tensor(input_index, np.expand_dims(np.array(image).astype(np.float32), axis=0))
        # Run inference.
        interpreter.invoke()
        output = interpreter.get_tensor(output_index)
        return np.argmax((output)[0])/10
    else: 
        return -1
        
    