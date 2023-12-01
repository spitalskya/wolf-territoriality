sim: FORCE
	python -m two_wolves_one_d_sim.simulate

check: FORCE
	mypy two_wolves_one_d_sim --strict

lint: FORCE
	pylint two_wolves_one_d_sim/

all: FORCE check lint

FORCE: ;