#! /usr/bin/env python
import sys
from functions import load_bmp, get_histogram, get_scale, find_radius
import os

if len(sys.argv) > 0:
    print sys.argv
    folder = sys.argv[1]
    tresh = float(sys.argv[2])
    area = float(sys.argv[3])
    format = str(sys.argv[4])
    filenames = load_bmp(format, folder)
    try:
        sys.argv[5]
        screen = ':0.0'
        os.environ['DISPLAY'] = screen
        print 'remote plotting on screen{}'.format(screen)
    except Exception as e:
        print 'plotting locally'
else:
        folder = raw_input('folder: ')
        format = raw_input('format?')
        filenames = load_bmp(format, folder)
        tresh = get_histogram(folder, filenames)
        area = float(raw_input('Small dots= 5000, big dots = 10000. Area:'))

scale_factor = get_scale(folder, filenames)
radii = find_radius(folder, scale_factor=scale_factor,
                    filenames = filenames,
                    area=area, treshold=tresh)
raw_input('quit?')
