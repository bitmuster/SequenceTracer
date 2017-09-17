
# This file is to test general features that we expect from the environment.
# Just to make sure we everything works as expected and that we are not stupid.

import os.path

def test_abspath():
    current_dir=os.path.abspath('./')
    c='/home/micha/Dump/CodeLand/SequenceTracer'
    assert current_dir == c

def test_abspath_relative():
    path = os.path.abspath('/home/../home/../home')
    exp = '/home'
    assert path == exp


def test_normpath_abspath_on_absolute_path():
    """According to the python doc abspath can be replaced by normpath"""
    path='/home/../home/../home'
    abspath = os.path.abspath(path)

    # Replacement for abspath : normpath(join(os.getcwd(), path))
    # Solution: use os.path.join not str.join (difference in absolute paths)
    abspath_normpath = os.path.normpath(os.path.join(os.getcwd(), path))
    assert abspath == abspath_normpath
