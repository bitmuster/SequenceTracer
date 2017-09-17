
import sys
import simple_script
import global_symbols
sys.path.append('./')
from sequencetracer import SequenceTracer


def test_simple_script_file_output():
    argv = ['sequencetracer.py', 'tests/simple_script.py']
    tracer=SequenceTracer(argv)
    tracer.start()
    outputfile = open('output.sdiag')
    lines = ''.join(outputfile.readlines())
    assert simple_script.expected_diagram == lines

def test_global_symbols_file_output():
    argv = ['sequencetracer.py', 'tests/global_symbols.py']
    tracer=SequenceTracer(argv)
    tracer.start()
    outputfile = open('output.sdiag')
    lines = ''.join(outputfile.readlines())
    assert global_symbols.expected_diagram == lines
