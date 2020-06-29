import numpy as np
import cv2
import pytesseract
from matplotlib import pyplot as plt
import os
import glob
from utils import *

sep = os.sep

pytesseract.pytesseract.tesseract_cmd = os.getenv('APPDATA')+sep+r'Tesseract-OCR'+sep+'tesseract.exe'





def run(input_path = 'input'+sep+'code.png', output_path= 'output', bg= False, gamma= False):
    paths = []
    print("=============================")
    print("Reading images....")
    print("=============================")
    if os.path.isdir(input_path):
        # os.walk works for reading nested directories

        # for dirname, _, filenames in os.walk(input_path):
        #     print(dirname + "----------------")
        #     for filename in filenames:
        #         print(os.path.join(dirname, filename))
        #         paths.append(os.path.join(dirname, filename))

        # read only .png files
        for path in glob.glob(input_path+sep+'*.png'):
            paths.append(path)

        # trt look for jepg if no png found
        if len(paths) == 0:
            for path in glob.glob(input_path+sep+'*.jpeg'):
                paths.append(path)
    else:
        paths.append(input_path)

    print("done reading")
    print(paths)
    for image_path in paths:
        print(image_path)
        image_name = image_path.split(sep)[-1].split('.')[0]

        image = cv2.imread(image_path)
        plt.figure(1, figsize=(8, 8))
        mngr = plt.get_current_fig_manager()
        # set position of figure
        mngr.window.wm_geometry("+500+100")
        plt.imshow(image)
        try:
            plt.show(block=False)
            plt.pause(1)
            plt.close()
        except:
            pass


        # pre-process the input image
        tabs = get_tabs(image, get_step(image))
        # contrast_img = contrast_old(image)
        (H, W) = image.shape[:2]
        scale = 3
        h_w_ratio = W / (1.0 * H)
        h = 2048
        w = int(h * h_w_ratio)
        resized_image = cv2.resize(image, (W * scale, H * scale), interpolation=cv2.INTER_CUBIC)

        # (Language) english and (Page segmentation mode)Automatic page segmentation with OSD , (OCR engine mode) - defulat   Neural nets LSTM engine only.
        # configuration = ("-l eng --psm 1 --oem 1")
        configuration = ("-l eng --psm 1")
        grayImage = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

        # get background pixel color
        bg_x = background(grayImage)

        print("=============================")
        print("pre-processing images")
        print("=============================")
        # use background to pre-process

        if bg:
            if gamma:
                grayImage = adjust_gamma(resized_image)
            else:
                grayImage = np.array(grayImage)
                grayImage = np.where(grayImage < bg_x, 255, grayImage)
                grayImage = np.where(grayImage > bg_x, 0, grayImage)
                grayImage = np.where(grayImage == bg_x, 255, grayImage)


        print("=============================")
        print("generating code")
        print("=============================")
        # generate text using tesseract
        text = pytesseract.image_to_string(resized_image, config=configuration)

        plt.figure(figsize=(8, 8))
        mngr = plt.get_current_fig_manager()
        # set position of figure
        mngr.window.wm_geometry("+500+100")
        plt.imshow(grayImage)
        try:
            plt.show(block=False)
            plt.pause(1)
            plt.close()
        except:
            pass


        lines = text.split('\n')



        print("=============================")
        print("generating tabs")
        print("=============================")
        # generate tabs
        tabs_t = tabs.copy()
        for i, line in enumerate(lines):
            if (line == "" or line == '   ') and i != 0:
                if i <= len(tabs_t):
                    tabs_t.insert(i, tabs_t[i - 1])
                else:
                    # TODO - needs to be fixed
                    tabs_t.insert(i, tabs_t[-1])
                    # pass



        # append tabs
        for i, line in enumerate(lines):
            for j in range(tabs_t[i]):
                lines[i] = "\t" + lines[i]



        print("=============================")
        print("saving "+image_name+".py files")
        print("=============================")
        # save to a file
        txt = ""
        for line in lines:
            txt += "\n" + line

        path = output_path
        with open(os.path.join(path, image_name+'.py'), mode="w") as f:
            f.write(txt)
            f.close()

