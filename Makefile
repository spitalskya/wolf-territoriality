sim: FORCE
	python -m two_wolves_one_d_sim.simulation

check: FORCE
	mypy two_wolves_one_d_sim --strict

lint: FORCE
	pylint two_wolves_one_d_sim/

FORCE: ;