# -*- coding: utf-8 -*-

# Copyright (C) 2008-2009 The Tegaki project contributors
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

# Contributors to this file:
# - Christoph Burgmer, cburgmer ÂT ira DÔT uka DÔT de (main author)
# - Mathieu Blondel

import glob
import os
import imp

from tegaki.character import Writing
from tegaki.recognizer import Recognizer

class StrokeRecognizerError(Exception):
    pass

class StrokeRecognizer(object):

    def __init__(self, recognizer):
        self._recognizer = recognizer

    def recognize(self, writing, n=5, strokes=None):
        """
        Recognizes writing and returns a list of recognized strokes.
        """
        strokes = strokes or []

        stroke_data = writing.get_strokes(True)
        for idx, stroke in enumerate(stroke_data):
            if len(strokes) <= idx:
                strokes.append([])
            # if user fixed a stroke, no need to recognize
            if not strokes[idx]:
                stroke_writing = Writing()
                stroke_writing.append_stroke(stroke_data[idx])
                #stroke_writing.normalize()
                stroke_writing.normalize_position()

                strokes[idx] = self._recognizer.recognize(stroke_writing, n)

        return strokes

if __name__ == "__main__":
    import sys
    import locale
    from tegaki.character import Character

    output_encoding = sys.stdout.encoding or locale.getpreferredencoding() \
            or 'ascii'
    def encode(text):
        return text.encode(output_encoding)

    recognizer = sys.argv[1] # name of recognizer
    model = sys.argv[2] # name of model file
    char = Character()
    char.read(sys.argv[3]) # path of .xml file
    writing = char.get_writing()

    recognizers = Recognizer.get_available_recognizers()
    print "Available recognizers", recognizers

    if not recognizer in recognizers:
        raise Exception, "Not an available recognizer"

    recognizer_klass = recognizers[recognizer]
    recognizer = recognizer_klass()

    models = recognizer_klass.get_available_models()
    print "Available models", models

    if not model in models:
        raise Exception, "Not an available model"

    recognizer.set_model(model)
    stroke_recognizer = StrokeRecognizer(recognizer)

    print encode(char.get_utf8().decode('utf8'))
    strokes = stroke_recognizer.recognize(writing)
    for stroke in strokes:
        for candidate, score in stroke:
            print encode(("%s (%.0f)," % (candidate, score)).decode('utf8')),
        print
