import cv2
import numpy as np
import statistics as stat

def adjust_gamma(image):
    # Load in the image using the typical imread function using our watch_folder path, and the fileName passed in, then set the final output image to our current image for now
    # Set thresholds. Here, we are using the Hue, Saturation, Value color space model. We will be using these values to decide what values to show in the
    # ranges using a minimum and maximum value.  THESE VALUES CAN BE PLAYED AROUND FOR DIFFERENT COLORS
    hMin = 29  # Hue minimum
    sMin = 30  # Saturation minimum
    vMin = 0   # Value minimum (Also referred to as brightness)
    hMax = 179 # Hue maximum
    sMax = 255 # Saturation maximum
    vMax = 255 # Value maximum
    # Set the minimum and max HSV values to display in the output image using numpys' array function. We need the numpy array since OpenCVs' inRange function will use those.
    lower = np.array([hMin, sMin, vMin])
    upper = np.array([hMax, sMax, vMax])
    # Create HSV Image and threshold it into the proper range.
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) # Converting color space from BGR to HSV
    mask = cv2.inRange(hsv, lower, upper) # Create a mask based on the lower and upper range, using the new HSV image
    # Create the output image, using the mask created above. This will perform the removal of all unneeded colors, but will keep a black background.
    output = cv2.bitwise_and(image, image, mask=mask)
    # Add an alpha channel, and update the output image variable
    *_, alpha = cv2.split(output)
    dst = cv2.merge((output, alpha))
    output = dst
    return output



# return background
def background(grayImage):
    x = []
    for arr in grayImage:
        x.append(np.bincount(arr).argmax())

    return np.bincount(x).argmax()


def get_step(image1):
    (H, W) = image1.shape[:2]
    h_w_ratio = W / (1.0 * H)
    h = 270
    w = int(h * h_w_ratio)
    step = 26
    image1 = cv2.resize(image1, (w, h))
    grayImage = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    bg_x = background(grayImage)
    saw_code = False
    block = []
    lines = []
    tab_count = 0
    for i, row in enumerate(grayImage):
        temp = np.where(row < bg_x, 0, row)
        temp = np.where(temp > bg_x, 0, temp)
        skip_vlines = np.count_nonzero(temp == 0)
        block.append(temp)
        # print(i, skip_vlines, saw_code)
        if temp.__contains__(0) and skip_vlines > 6:
            saw_code = True
        elif saw_code:
            saw_code = False
            segment = []
            subseg = []
            seg = []
            for j in range(len(block)):
                seg.append(block[j][0:50])  # would work for no lines
                segment.append(block[j][step])  # would work for no lines
                subseg.append(block[j][step - step // 2])
            np_segment = np.asarray(segment)
            np_subseg = np.asarray(subseg)
            # check 13s and last line
            tab = not (np.any(np_segment == 0) or np.any(np_subseg == 0))
            if tab:
                seg_lines = []
                tab_count += 1
                for se in seg:
                    bg_seen = False
                    for k, s in enumerate(se):
                        if s == bg_x:
                            bg_seen = True
                        if bg_seen and s == 0 or s>240: # consider black or white background
                            seg_lines.append(k)
                            break
                # print(seg_lines)
                return stat.mode(seg_lines)

                # segment.clear()
                # subseg.clear()
                # seg.clear()
                # break
            else:
                lines.append(tab_count)
                tab_count = 0
            block.clear()
    return 20


def get_tabs(image1, step_size):
    (H, W) = image1.shape[:2]
    h_w_ratio = W / (1.0 * H)
    h = 270
    w = int(h * h_w_ratio)
    if step_size > 29:
        step = 26
    else:
        step = 20
    image1 = cv2.resize(image1, (w, h))
    grayImage = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    bg_x = background(grayImage)
    saw_code = False
    block = []
    lines = []
    tab_count = 0
    for i, row in enumerate(grayImage):
        temp = np.where(row < bg_x, 0, row)
        temp = np.where(temp > bg_x, 0, temp)
        skip_vlines = np.count_nonzero(temp == 0)
        block.append(temp)
        if temp.__contains__(0) and skip_vlines > 6:
            saw_code = True
        elif saw_code:
            saw_code = False
            segment = []
            subseg = []
            for k in range(1, 40):  # upto 20 tabs
                for j in range(len(block)):
                    # print(len(block[1]))
                    #TODO  temporary check -- needs be fixed
                    if (step * k) <= len(block[1]):
                        segment.append(block[j][step * k])  # would work for no lines
                    # TODO  temporary check -- needs be fixed
                    if (step * k - step // 2) <= len(block[1]):
                        subseg.append(block[j][step * k - step // 2])
                np_segment = np.asarray(segment)
                np_subseg = np.asarray(subseg)
                # check 13s and last line

                tab = not (np.any(np_segment == 0) or np.any(np_subseg == 0))
                if tab:
                    tab_count += 1
                    segment.clear()
                    subseg.clear()
                else:
                    lines.append(tab_count)
                    tab_count = 0
                    break
            block.clear()
    return lines


def contrast_old(img):
    # -----Converting image to LAB Color model-----------------------------------
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    # cv2.imshow("lab",lab)

    # -----Splitting the LAB image to different channels-------------------------
    l, a, b = cv2.split(lab)
    # cv2.imshow('l_channel', l)
    # cv2.imshow('a_channel', a)
    # cv2.imshow('b_channel', b)

    # -----Applying CLAHE to L-channel-------------------------------------------
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    # cv2.imshow('CLAHE output', cl)

    # -----Merge the CLAHE enhanced L-channel with the a and b channel-----------
    limg = cv2.merge((cl, a, b))
    # cv2.imshow('limg', limg)

    # -----Converting image from LAB Color model to RGB model--------------------
    final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    return final


def contrast_bright(img, alpha, beta):
    new_img = cv2.addWeighted( img, alpha, img, 0, beta)
    return new_img