from minizinc import Instance, Model, Solver
from ortools_solver import ortoolsSolver
from ortools_solver_new import *
import os
import math
import csv
import re

original = './minizinc_solver.mzn'
Neg = './minizinc_solver_neg.mzn'
reduceVar = './minizinc_solver_reduceVar.mzn'
changeRange = './minizinc_solver_range.mzn'
comb = './minizinc_solver_comb.mzn'


def minizincSolver(file, model):
    games = Model(model)
    games.add_file(file)
    gecode = Solver.lookup('gecode')
    instance = Instance(gecode, games)
    result = instance.solve()

    token = None
    play = None
    total_fun = None
    sat = result.status
    time = result.statistics['time'].total_seconds()
    if result.status.has_solution():
        token = result['token']
        play = result['play']
        total_fun = result['total_fun']
    return [sat, token, play, total_fun, time]


def minizincSolverNew(file, model):
    games = Model(model)
    games.add_file(file)
    gecode = Solver.lookup('gecode')
    instance = Instance(gecode, games)
    result = instance.solve()
    token = None
    play = None
    total_fun = None
    sat = result.status
    time = result.statistics['time'].total_seconds()
    if result.status.has_solution():
        token = result['token']
        play = result['play']
        total_fun = re.search(r'\d+',str(result.solution)).group()
    return [sat, token, play, total_fun, time]

def createCSV(path, output):
    instances = os.listdir(path)
    with open(output, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['file', 'num', 'cap', 'refill', 'fun', 'goal',
                         'minizinc sat', 'minizinc token', 'minizinc play',
                         'minizinc total_fun', 'minizinc time',
                         'ortools sat', 'ortools token', 'ortools play',
                         'ortools total_fun', 'ortools time'])
        for instance in instances:
            print(instance)
            filename = path+instance
            with open(filename, 'r') as f:
                for i in range(5):
                    exec(f.readline(), globals())
                info = [instance, num, cap, refill, fun, goal]
                ortools_result = ortoolsSolver(num, cap, refill, fun, goal)
                minizinc_result = minizincSolver(path + '/' + instance, original)
                writer.writerow(info + minizinc_result + ortools_result)

def createMinizincCSV(path, output):
    instances = os.listdir(path)
    with open(output, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['num', 'original', 'reduceVar', 'Neg', 'changeRange', 'final'])
        for instance in instances:
            print(instance)
            filename = path+instance
            with open(filename, 'r') as f:
                for i in range(5):
                    exec(f.readline(), globals())                
                original_result = minizincSolver(path + '/' + instance, original)
                reduceVar_result = minizincSolverNew(path + '/' + instance, reduceVar)
                Neg_result = minizincSolver(path + '/' + instance, Neg)
                changeRange_result = minizincSolver(path + '/' + instance, changeRange)
                final_result = minizincSolverNew(path + '/' + instance, comb)
                writer.writerow([num, original_result[4], reduceVar_result[4],
                                 Neg_result[4], changeRange_result[4], final_result[4]])


def createORToolsCSV(path, output):
    instances = os.listdir(path)
    with open(output, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['num', 'original', 'reduceVar', 'Neg', 'changeRange', 'final'])
        for instance in instances:
            print(instance)
            filename = path+instance
            with open(filename, 'r') as f:
                for i in range(5):
                    exec(f.readline(), globals())
                original_result = ortoolsSolver(num, cap, refill, fun, goal)
                reduceVar_result = ortoolsSolverReduceVar(num, cap, refill, fun, goal)
                Neg_result = ortoolsSolverNeg(num, cap, refill, fun, goal)
                changeRange_result = ortoolsSolverRange(num, cap, refill, fun, goal)
                final_result = ortoolsSolverComb(num, cap, refill, fun, goal)
                writer.writerow([num, original_result[4], reduceVar_result[4], Neg_result[4],changeRange_result[4],final_result[4]])


def createfinalCSV(path, output):
    instances = os.listdir(path)
    with open(output, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['file', 'num', 'cap', 'refill', 'fun', 'goal',
                         'minizinc sat', 'minizinc token', 'minizinc play',
                         'minizinc total_fun', 'minizinc time',
                         'ortools sat', 'ortools token', 'ortools play',
                         'ortools total_fun', 'ortools time'])
        for instance in instances:
            print(instance)
            filename = path+instance
            with open(filename, 'r') as f:
                for i in range(5):
                    exec(f.readline(), globals())
                info = [instance, num, cap, refill, fun, goal]
                ortools_result = ortoolsSolverComb(num, cap, refill, fun, goal)
                minizinc_result = minizincSolverNew(path + '/' + instance, comb)
                writer.writerow(info + minizinc_result + ortools_result)

#createCSV('./change_num/', 'change_num.csv')
#createCSV('./random_instances/', 'random_instances.csv')
#createORToolsCSV('./change_num/', 'ORTools_num.csv')
#createORToolsCSV('./random_instances/', 'ORTools_random.csv')
#createMinizincCSV('./random_instances/', 'Minizinc_random.csv')
#createMinizincCSV('./change_num/', 'Minizinc_num.csv')
#createfinalCSV('./hard_instances/', 'test.csv')