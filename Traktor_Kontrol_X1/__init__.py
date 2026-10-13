# uncompyle6 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.7.0 (v3.7.0:1bf9cc5093, Jun 27 2018, 04:59:51) [MSC v.1914 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Traktor_Kontrol_X1\__init__.py
# Compiled at: 2024-04-05 18:27:47
# Size of source mod 2**32: 367 bytes
from __future__ import absolute_import, print_function, unicode_literals
from .TraktorKontrolX1 import TraktorKontrolX1

def create_instance(c_instance):
    return TraktorKontrolX1(c_instance)
