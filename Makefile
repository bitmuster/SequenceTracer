

sample:
	python3 sequencetracer.py sample_code.py
	seqdiag3 -T svg output.sdiag
	seqdiag3 -T png output.sdiag
	eom output.png

sample_anymate_gui:
	# Warning: The png will be very very very large
	# That shows us the necessity of filters
	python3 sequencetracer.py ../AnyMate/AnyMate.py ../AnyMate/template.anymate
	seqdiag3 -T svg output.sdiag
	seqdiag3 -T png output.sdiag
	eom output.png

sample_anymate:
	# Warning: The png will be very very large 8Kpx x 27Kpx
	# That shows us the necessity of filters
	python3 sequencetracer.py ../AnyMate/AnyMate.py --nogui xclock ../AnyMate/template.anymate
	seqdiag3 -T svg output.sdiag
	seqdiag3 -T png output.sdiag
	eom output.png

view:
	seqdiag3 -T svg output.sdiag
	seqdiag3 -T png output.sdiag
	eom output.png

test:
	python3 sequencetracer.py tests/global_symbols.py Laserpony

pytest:
	pytest-3

clean:
	rm output.*
