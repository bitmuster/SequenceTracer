
import sys
import simple_script
sys.path.append('./')
import sequencetracer


def test_simple_script():
    argv = ['sequencetracer.py', 'tests/simple_script.py']
    sequencetracer.main(argv)
    outputfile = open('output.sdiag')
    lines = ''.join(outputfile.readlines())
    assert simple_script.expected_diagram == lines
