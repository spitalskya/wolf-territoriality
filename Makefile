sim: FORCE
	python -m two_wolves_one_d_sim.simulate

sim-display: FORCE
	python -m two_wolves_one_d_sim.simulate_display_steps

check: FORCE
	mypy two_wolves_one_d_sim --strict

lint: FORCE
	pylint two_wolves_one_d_sim/

all: FORCE check lint

FORCE: ;