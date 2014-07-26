qt_dot_fitter
=============

Qt and pyton GUI to measure statistics on SEM images(image files, bundled with the .ssc meta data from ZEISS SEMs) of circular objects.

=============

# usage:

run the main app, app.py with :

```
python /qt_dot_fitter/app.py ./path_to_/a_reference_image.bmp ./root_foolder_with pictures min_size format
```

where min_size is a gray number that limits the smallest possible are fitted by the app;
there is no general rule, it must be found out iteratively.

format is the format of the images on the hard disk

