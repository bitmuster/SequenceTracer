

sample:
	python3 sequencetracer.py sample_code.py
	seqdiag3 -T svg output.sdiag
	seqdiag3 -T png output.sdiag
	eom output.png

test:
	python3 sequencetracer.py tests/global_symbols.py Laserpony

pytest:
	pytest-3
