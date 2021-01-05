Sequential Games Problem

files:
change_num: a folder contains instances with fixed cap, refill and ordered fun
hard_instances: a folder contains hard instances
random_instances: a folder contains randomly formed instances
instances_generator.py
minizinc_solver.mzn
minizinc_solver_comb.mzn
minizinc_solver_neg.mzn
minizinc_solver_range.mzn
minizinc_solver_reduceVar.mzn
ortools_solver.py
ortools_solver_new.py
solver_result.py (generate csv for results)

Module need to install:
pip install minizinc
pip install ortools

run with command:

MiniZinc:
minizinc minizinc_solverXXX.mzn [./foldername/filename]
for example:
minizinc minizinc_solver.mzn ./random_instances/04_1.dzn
minizinc minizinc_solver_comb.mzn ./random_instances/04_1.dzn

OR-Tools in Python:
python3 ortools_solverXXX.py [./foldername/filename]
for example:
python3 ortools_solver.py ./random_instances/04_1.dzn
python3 ortools_solver_new.py ./random_instances/04_1.dzn
