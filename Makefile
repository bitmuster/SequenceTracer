

sample:
	python3 sequencetracer.py > sample.sdiag
	seqdiag3 -T svg sample.sdiag
	eom sample.svg
