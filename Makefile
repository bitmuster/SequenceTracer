

sample:
	python3 sequencetracer.py
	seqdiag3 -T svg output.sdiag
	seqdiag3 -T png output.sdiag
	eom output.png
