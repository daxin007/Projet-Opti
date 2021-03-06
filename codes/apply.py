import numpy as np
from cocoex import Suite, Observer
import cocopp
import scipy.optimize
#import IEBA
max_runs=10000
number_of_batches = 5  
current_batch = 1 
# prepare (the most basic example solver)
def random_search(fun, lbounds, ubounds, budget):
    """Efficient implementation of uniform random search between
    `lbounds` and `ubounds`
    """
    lbounds, ubounds = np.array(lbounds), np.array(ubounds)
    dim, x_min, f_min = len(lbounds), None, None
    max_chunk_size = 1 + 4e4 / dim
    while budget > 0:
        chunk = int(max([1, min([budget, max_chunk_size])]))
        # about five times faster than "for k in range(budget):..."
        X = lbounds + (ubounds - lbounds) * np.random.rand(chunk, dim)
        if fun.number_of_constraints > 0:
            C = [fun.constraint(x) for x in X]  # call constraints
            F = [fun(x) for i, x in enumerate(X) if np.all(C[i] <= 0)]
        else:
            F = [fun(x) for x in X]
        if fun.number_of_objectives == 1:
            index = np.argmin(F) if len(F) else None
            if index is not None and (f_min is None or F[index] < f_min):
                x_min, f_min = X[index], F[index]
        budget -= chunk
    return x_min 
"""  
def random_search(f, lb, ub, m):
    candidates = lb + (ub - lb) * np.random.rand(m, len(lb))
    #print(candidates)
    #return candidates[np.argmin([f(x) for x in candidates])]
    return candidates[0]
"""
solver = random_search #for test
#solver = scipy.optimize.fmin
#solver = IEBA

def main(budget,suite,observer,solver,dimension,max_runs=max_runs,current_batch=current_batch,number_of_batches=number_of_batches):
    """ 
        suite: dataset
        observer: output
        solver: optimisation of function
        dimension, current_batch, number_of_batches: choose data
        max_run: max times of run
    """
    for fun_index, fun in enumerate(suite):
        if (fun_index + current_batch - 1) % number_of_batches:
            continue
        if fun.dimension >dimension:
            continue
        fun.observe_with(observer)
        solver(fun, fun.lower_bounds, fun.upper_bounds, budget)

    # cocopp.main(observer.result_folder)  # re-run folders look like "...-001" etc
    # webbrowser.open("file://" + os.getcwd() + "/ppdata/index.html")
   



if __name__ == '__main__':
    """add parameters here """
    suite = Suite('bbob-biobj', 'year:2018', '')
    observer = Observer("bbob-biobj", "result_folder: %s_on_%s" % (solver.__name__, "bbob2018"))
    solver = random_search
    dimension=5
    budget=100
    main(budget,suite,observer,solver,dimension,max_runs, current_batch, number_of_batches)
