#! /usr/bin/env python
from pylab import *
import cv2
import os
from scipy import *
from skimage.morphology import label
from skimage.measure import regionprops
from collections import deque
import scipy.ndimage as ndimage

# function definitions:


def load_bmp(format, folder='.'):
    '''
    load bmps and return lisf of filenames and indices (last four or 3 digit)
    '''
    filenames = []
    for dirpath, dirnames, filenames_c in os.walk(folder):
        for name in filenames_c:
            if type(name) != str:
                raise Exception
            if format in name.lower():
                filenames.append(name)
    return filenames


def get_scale(folder, filenames):
    '''
    '''
    print filenames
    img = imread(str(folder) + str('/') + str(filenames[-1]))
    size = len(img)
    with open(str(folder) + str('/') + str(filenames[-1][:-4]) +
              '.ssc', 'r') as file_open:
        for line in file_open:
            if 'LowerLeftUV' in line:
                low, drop = line[12:30].split(",")
                low = abs(float(low))
            elif 'UpperRightUV' in line:
                up, drop = line[13:30].split(",")
                up = abs(float(up))
                scale_r = abs(up - low) * 1000
    scale_factor = (float(scale_r) / float(size)) * 1000
    return scale_factor


def get_histogram(folder, filenames):
    '''
    test
    '''
    img = imread(str(folder) + str('/') + str(filenames[0]))
    ndimage.gaussian_filter(img, sigma=6)
    fig, ax = subplots()
    for i in img:
        ax.plot(i)
    fig.show()
    tresh = float(raw_input('type threshold:'))
    close()
    return tresh


def find_radius(folder, scale_factor, filenames,
                area=5000, area_max=337250.0,
                treshold=80):
    '''
    filenames is list of images
    '''
    radii = []
    results = {}
    for filename in filenames:
        img = imread(str(folder) + str('/') + str(filename))
        img = ndimage.gaussian_filter(img, sigma=3)   # needs some smoothing
        print str(filename) + ' loaded'
        print 'start analysis...'
        dots = (img > treshold)
        label_image = label(dots)
        radii = deque()
        win_name = str(filename)
        cv2.namedWindow(win_name)
        radii_x = []
        radii_y = []
        for props in regionprops(label_image):
            if props['Area'] < area or props['Area'] > area_max:
                if abs(props['Area']  - area) < 100:
                    print 'module too big or too small'
                print 'measured area too small'
                continue
            y0, x0 = props.centroid
            orientation = props.orientation
            x1 = x0 + math.cos(orientation) * 0.5 * props.major_axis_length
            y1 = y0 - math.sin(orientation) * 0.5 * props.major_axis_length
            x2 = x0 - math.sin(orientation) * 0.5 * props.minor_axis_length
            y2 = y0 - math.cos(orientation) * 0.5 * props.minor_axis_length
            radii_x.append(math.sqrt((x1-x0)**2 +(y1-y0)**2 ))
            radii_y.append(math.sqrt((x2-x0)**2 +(y2-y0)**2 ))
            #area = np.pi * radii_x[0] * radii_y[0]
            #area = area[0] # filter out more than one fit x region
            #radius = area / np.sqrt(4 * np.pi)
            if type(radii_x) == list:
                ra_x = radii_x [0]
            if type(radii_y) == list:
                ra_y = radii_y [0]
            radius = (ra_x + ra_y)/2
            # print radius
            cv2.circle(img, (int(props['Centroid'][1]),
                             int(props['Centroid'][0])), int(
                       radius), (255, 255, 255), 7)  # draw the outer circle
            # draw the center of the circle
            cv2.circle(
                img, (int(props['Centroid'][1]),
                      int(props['Centroid'][0])), 10, (0, 255, 255), 5)
            radius = radius * scale_factor
            radii.append(radius)
            cv2.imshow(win_name, cv2.resize(img, (600, 600)))
            cv2.waitKey(9)
        radii_arr = array(radii)
        cv2.imwrite(str(folder)+'/'+str(filename[:-4])+'.jpg', img)
        if len(radii_arr) > 0:
            np.savetxt(str(folder) + '/' +
                       str(int(treshold)) +
                       str(filename[:-4])+'.csv',
                       radii_arr, delimiter=",")
    print 'finished analysis for folder {}'.format(str(folder))
    return results

