try:
    import tflite_runtime.interpreter as tflite
    print("Environment OK: tflite-runtime found.")
except ImportError:
    try:
        import tensorflow.lite as tflite
        print("Environment OK: tensorflow.lite found.")
    except ImportError:
        print("Environment Error: Neither tflite-runtime nor tensorflow.lite found.")
        exit(1)
