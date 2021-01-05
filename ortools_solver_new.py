from ortools.sat.python import cp_model
import os
import math
import csv
import sys

def ortoolsSolverReduceVar(num, cap, refill, fun, goal):
    model = cp_model.CpModel()
    token = [model.NewIntVar(-2147483648, 2147483647, 't%i' % i)
             for i in range(1, num + 1)]
    play = [model.NewIntVar(-2147483648, 2147483647, 'q%i' % i)
            for i in range(1, num + 1)]
    compare = [model.NewBoolVar('c%i' % i)
               for i in range(1, num + 1)]
    total_fun = sum([fun[i] * play[i] for i in range(num)])
    model.Add(total_fun >= goal)
    model.Add(token[0] == cap)
    for i in range(num):
        model.Add(token[i] - play[i] + refill > cap).OnlyEnforceIf(compare[i])
        model.Add(token[i] - play[i] + refill <=
                  cap).OnlyEnforceIf(compare[i].Not())
        model.Add(play[i] >= 1)
        model.Add(play[i] <= token[i])
    for i in range(1, num):
        model.Add(token[i] == cap).OnlyEnforceIf(compare[i - 1])
        model.Add(token[i] == token[i - 1] - play[i - 1] +
                  refill).OnlyEnforceIf(compare[i - 1].Not())
    model.Maximize(total_fun)
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    sat = solver.StatusName()
    time = solver.UserTime()
    if status == cp_model.INFEASIBLE:
        token = None
        play = None
        total_fun = None
    else:
        token = [solver.Value(token[i]) for i in range(num)]
        play = [solver.Value(play[i]) for i in range(num)]
        total_fun = solver.Value(total_fun)
    return [sat, token, play, total_fun, time]

def ortoolsSolverRange(num, cap, refill, fun, goal):
    model = cp_model.CpModel()
    token = [model.NewIntVar(1, cap, 't%i' % i)
             for i in range(1, num + 1)]
    play = [model.NewIntVar(1, cap, 'q%i' % i)
            for i in range(1, num + 1)]
    compare = [model.NewBoolVar('c%i' % i)
               for i in range(1, num + 1)]
    total_fun = model.NewIntVar(-100, 1000, 'total_fun')
    model.Add(total_fun == sum([fun[i] * play[i] for i in range(num)]))
    model.Add(total_fun >= goal)
    model.Add(token[0] == cap)
    for i in range(num):
        model.Add(token[i] - play[i] + refill > cap).OnlyEnforceIf(compare[i])
        model.Add(token[i] - play[i] + refill <=
                  cap).OnlyEnforceIf(compare[i].Not())
        model.Add(play[i] >= 1)
        model.Add(play[i] <= token[i])
    for i in range(1, num):
        model.Add(token[i] == cap).OnlyEnforceIf(compare[i - 1])
        model.Add(token[i] == token[i - 1] - play[i - 1] +
                  refill).OnlyEnforceIf(compare[i - 1].Not())
    model.Maximize(total_fun)
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    sat = solver.StatusName()
    time = solver.UserTime()
    if status == cp_model.INFEASIBLE:
        token = None
        play = None
        total_fun = None
    else:
        token = [solver.Value(token[i]) for i in range(num)]
        play = [solver.Value(play[i]) for i in range(num)]
        total_fun = solver.Value(total_fun)
    return [sat, token, play, total_fun, time]


def ortoolsSolverNeg(num, cap, refill, fun, goal):
    model = cp_model.CpModel()
    token = [model.NewIntVar(-2147483648, 2147483647, 't%i' % i)
             for i in range(1, num + 1)]
    play = [model.NewIntVar(-2147483648, 2147483647, 'q%i' % i)
            for i in range(1, num + 1)]
    compare = [model.NewBoolVar('c%i' % i)
               for i in range(1, num + 1)]
    neg = [model.NewBoolVar('n%i' % i)
           for i in range(1, num + 1)]
    total_fun = model.NewIntVar(-2147483648, 2147483647, 'total_fun')
    model.Add(total_fun == sum([fun[i] * play[i] for i in range(num)]))
    model.Add(total_fun >= goal)
    model.Add(token[0] == cap)
    for i in range(num):
        model.Add(token[i] - play[i] + refill > cap).OnlyEnforceIf(compare[i])
        model.Add(token[i] - play[i] + refill <=
                  cap).OnlyEnforceIf(compare[i].Not())
        model.Add(fun[i] < 0).OnlyEnforceIf(neg[i])
        model.Add(fun[i] >= 0).OnlyEnforceIf(neg[i].Not())
        model.Add(play[i] <= token[i])
        model.Add(play[i] == 1).OnlyEnforceIf(neg[i])
        model.Add(play[i] >= 1).OnlyEnforceIf(neg[i].Not())
    for i in range(1, num):
        model.Add(token[i] == cap).OnlyEnforceIf(compare[i - 1])
        model.Add(token[i] == token[i - 1] - play[i - 1] +
                  refill).OnlyEnforceIf(compare[i - 1].Not())
    model.Maximize(total_fun)
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    sat = solver.StatusName()
    time = solver.UserTime()
    if status == cp_model.INFEASIBLE:
        token = None
        play = None
        total_fun = None
    else:
        token = [solver.Value(token[i]) for i in range(num)]
        play = [solver.Value(play[i]) for i in range(num)]
        total_fun = solver.Value(total_fun)
    return [sat, token, play, total_fun, time]

def ortoolsSolverComb(num, cap, refill, fun, goal):
    model = cp_model.CpModel()
    token = [model.NewIntVar(1, cap, 't%i' % i)
             for i in range(1, num + 1)]
    play = [model.NewIntVar(1, cap, 'q%i' % i)
            for i in range(1, num + 1)]
    compare = [model.NewBoolVar('c%i' % i)
               for i in range(1, num + 1)]
    neg = [model.NewBoolVar('n%i' % i)
           for i in range(1, num + 1)]
    total_fun = sum([fun[i] * play[i] for i in range(num)])
    model.Add(total_fun >= goal)
    model.Add(token[0] == cap)
    for i in range(num):
        model.Add(token[i] - play[i] + refill > cap).OnlyEnforceIf(compare[i])
        model.Add(token[i] - play[i] + refill <=
                  cap).OnlyEnforceIf(compare[i].Not())
        model.Add(fun[i] < 0).OnlyEnforceIf(neg[i])
        model.Add(fun[i] >= 0).OnlyEnforceIf(neg[i].Not())
        model.Add(play[i] <= token[i])
        model.Add(play[i] == 1).OnlyEnforceIf(neg[i])
        model.Add(play[i] >= 1).OnlyEnforceIf(neg[i].Not())
    for i in range(1, num):
        model.Add(token[i] == cap).OnlyEnforceIf(compare[i - 1])
        model.Add(token[i] == token[i - 1] - play[i - 1] +
                  refill).OnlyEnforceIf(compare[i - 1].Not())
    model.Maximize(total_fun)
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    sat = solver.StatusName()
    time = solver.UserTime()
    if status == cp_model.INFEASIBLE:
        token = None
        play = None
        total_fun = None
    else:
        token = [solver.Value(token[i]) for i in range(num)]
        play = [solver.Value(play[i]) for i in range(num)]
        total_fun = solver.Value(total_fun)
    return [sat, token, play, total_fun, time]

if __name__ == '__main__':
    file = sys.argv[1]
    f = open(file)
    for i in range(5):
        exec(f.readline())
    f.close()
    [sat, token, play, total_fun, time] = ortoolsSolverComb(
        num, cap, refill, fun, goal)
    print('Status:', sat)
    if sat == 'OPTIMAL':
        print('Maximum total fun:', total_fun)
