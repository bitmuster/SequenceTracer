

# UML Sequence Diagram Tracer #

Automatically generate UML-sequence diagrams from Python3 code traces.

Sill in the state of a **bad** hack to demonstrate the intended concept!

Author: Michael Abel, mabel@bitmuster.org, 2017

## Usage ##

    python3 sequencetracer.py sample_code.py
    seqdiag3 -T svg output.sdiag

See Makefile for futher examples

## License ##

GPL -> see License.txt

## Requirements ##

This project generates input files for **seqdiag3** a simple sequence-diagram
image generator.

http://blockdiag.com/en/seqdiag/index.html

As debian packet: python3-seqdiag

## ToDo ##

Some things are still open that are already half-implemented.
However, they are not "Done" yet.

- Add useuil sample- and test-code files
- Add model class for sequences than export from there
- Add test files
- Add Makefile with tests linters runs etc
- Also derive object's code names (is it possible?)
- Find a nice real-life example
- Add filter to filter unwanted objects
- Add trick to filter sys & os calls that are handled in C (e.g. os.system)
- Clone output to file instead of console
- Any way to debug here ??? We cannot trace and debug at the same time!
  - Can we test this nicely ?
- Separate diagram context e.g. generate one diagram per function/method
- How can tests be executed in other scripts and the results analysed?
- Add filters to ignore calls, e.g. class IncrementalDecoder, inits etc.
- Why are there so many other call since we switched from imported modules
    to compiled code?


