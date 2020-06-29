# IMAGE_2_CODE
        Convert images of python code into formatted python code.
        Uses Neural LSTM Engine technology.

## Rquirements/dependencies: 
### To run this code, you need the following packages:
* Tesseract-OCR --> download from this [**Link**](https://tesseract-ocr.github.io/tessdoc/4.0-with-LSTM.html#400-alpha-for-windows) or if running on windows download the binaries from the [**tesseract_exe**](https://github.com/mhamdan91/IMAGE_2_CODE/tree/master/tesseract_exe) folder.
* pytesseract.
* numpy.
* matplotlib.
* open-cv (cv2).

## Tesseract Installation
    1- Install pytesseract, e.g. using pip --> **pip install pytesseract**
    2- Install Tesseract-OCR .exe to this location on your machine: C:\Users\\username\AppData\Roaming 
------------------------------------

### main.py arguments:
    1. '-i', '--batch_size', default=2, type=int, help='Batch size between 1 & 15 -- default: 2 '
    2. '-o', '--train_mode', default=0, type=int, help='0: Predict, 1: Train from a previous checkpoint, 2: Train from scratch -- default: 0'
    3. '-b', '--bg', default=False, type=bool, help=' Employ background processing along with Neural LSTM engine. -- default: False'
    4. '-g', '--gamma', default=False, type=bool, help=' Adjust input image gamma level -- default: False'
