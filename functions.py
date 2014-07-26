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
        for region in regionprops(label_image, ['Area',
                                                'BoundingBox',
                                                'Centroid',
                                                'EquivDiameter',
                                                'Eccentricity']):
            if region['Area'] < area or region['Area'] > area_max:
                if abs(region['Area'] - area) < 100:
                    print 'too big too small. Area: ' + str(region['Area'])
                continue
            if region['Eccentricity'] < .2:
                print 'not round enough: ' + str(region['Eccentricity'])
                continue
            minr, minc, maxr, maxc = region['BoundingBox']
            radius = [(maxc - minc) / 2., (maxr - minr) / 2]
            if radius[0] / radius[1] < .5:
                print 'not round enough'
                continue
            if radius[0] / radius[1] > 1.5:
                print 'not round enough'
                continue
            radius = radius[0]
            # print radius
            cv2.circle(img, (int(region['Centroid'][1]),
                             int(region['Centroid'][0])), int(
                       radius), (255, 255, 255), 7)  # draw the outer circle
            # draw the center of the circle
            cv2.circle(
                img, (int(region['Centroid'][1]),
                      int(region['Centroid'][0])), 10, (0, 255, 255), 5)
            radius = radius * scale_factor
            radii.append(radius)
            cv2.imshow(win_name, cv2.resize(img, (600, 600)))
            cv2.waitKey(9)
        radii_arr = array(radii)
        cv2.imwrite(str(folder)+'/'+str(filename[:-4])+'.jpg', img)
        np.savetxt(str(folder) + '/' +
                   str(int(treshold)) +
                   str(filename[:-4])+'.csv',
                   radii_arr, delimiter=",")
    print 'finished analysis for folder {}'.format(str(folder))
    return results
