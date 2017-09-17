

# Sequence Tracer #

Automatically enerate UML-Sequence diagrams from Python3 code traces.

Sill in the state of a bad hack to demonstrate the intended concept!

## Requirements ##

This project uses seqdiag a simple sequence-diagram image generator.
http://blockdiag.com/en/seqdiag/index.html

As debian packet: python3-seqdiag

## ToDo ##

- Add usefil sample- and test-code files
- Add model class for sequences than export from there
- Add test files
- Add Makefile with tests linters runs etc
- Also derive object's code names (is it possible?)
- Find a nice real-life example
- Add filter to filter unwanted objects
- Add trick to filter sys & os calls that are handled in C (e.g. os.system)
- Clone output to file instead of console
- Add license info
- Any way to debug??? We cannot trace and debug at the same time!
  - Can we test this nicely ?
- Separate diagram context e.g. generate one diagram per function/method
- How can tests be executed in other scripts and the results analysed?
    Especially, when some functions like abspath do not work as expected.
- Decide about license
- We still see arguments for sequencetracer appear on the analyzed script
- Add filters to ignore calls, e.g. class IncrementalDecoder, inits etc.
- Why are there so many other call since we switched from imported modules
    to compiled code?


