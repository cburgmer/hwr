Extracting stroke data
======================

The strokes handwriting model can be extracted from existing models. This
process helps to quickly create a large model.

Building
--------
This archive contains a pre-built .xml file but if you like, you can
re-run the bootstrapping process from source using "tegaki-extractstrokes",
available from tegaki-tools. This requires external dependency cjklib
(http://code.google.com/p/cjklib).

$ python tegaki-extractstrokes -l J -m 100 \
    strokes-ja.xml \
    -t ../data/train/japanese/handwriting-ja.xml
$ python tegaki-extractstrokes -l C -m 100 \
    strokes-zh_CN.xml \
    -t ../data/train/simplified-chinese/handwriting-zh_CN.xml
$ python tegaki-extractstrokes -l T -m 100 \
    strokes-zh_TW.xml \
    -c ../data/train/traditional-chinese/handwriting-zh_TW.xml \
    -d ../data/train/traditional-chinese/out-domain
$ tegaki-convert -c strokes-ja.xml -c strokes-zh_CN.xml \
    -c strokes-zh_TW.xml strokes.xml -m 100

A review of the file can improve later recognition accuracy.

To build the final model file, please see README.txt.
