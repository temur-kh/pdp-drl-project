import logging

from services import ORToolsOptimizerInputParams, ORToolsOptimizerServiceABC, ORToolsOptimizerConfig, ORToolsOutput

from ortools.sat.python import cp_model


class ORToolsOptimizerService(ORToolsOptimizerServiceABC):
    def solve(self, params: ORToolsOptimizerInputParams, config: ORToolsOptimizerConfig):
        model = cp_model.CpModel()

        x = {(i, j, k): model.NewIntVar(0, 1, f'x_{(i, j, k)}') for (i, j) in params.A for k in params.K}
        T = {(i, k): model.NewIntVar(params.a[i], params.b[i], f'T_{(i, k)}') for i in params.V for k in params.K}
        Q = {(i, k): model.NewIntVar(max(0, params.q[i]), min(params.Q[k], params.Q[k] + params.q[i]), f'Q_{(i, k)}')
             for i in params.V for k in params.K}

        # constraint 2
        for i in params.P:
            model.Add(sum([x[(i, j, k)] for k in params.K for j in params.V]) == 1)

        # constraint 3
        for i in params.P:
            for k in params.K:
                model.Add(sum([x[(i, j, k)] for j in params.V]) - sum(
                    [x[(params.n + i, j, k)] for j in params.V]) == 0)

        # constraint 4
        for k in params.K:
            model.Add(sum([x[(0, j, k)] for j in params.V]) == 1)

        # constraint 5
        for i in (params.P + params.D):
            for k in params.K:
                model.Add(sum([x[(j, i, k)] for j in params.V]) - sum([x[(i, j, k)] for j in params.V]) == 0)

        # constraint 6
        for k in params.K:
            model.Add(sum([x[(i, 2 * params.n + 1, k)] for i in params.V]) == 1)

        # constraint 7
        extra_T_vars = []
        for i in params.V:
            for j in params.V:
                for k in params.K:
                    var = model.NewIntVar(0, params.b[i], f'extra_T_{(i, j, k)}')
                    extra_T_vars.append(var)
                    model.AddMultiplicationEquality(var, variables=[T[(i, k)], x[(i, j, k)]])
                    model.Add(T[(j, k)] >= var + (params.s[i] + params.t[(i, j)]) * x[(i, j, k)])

        # constraint 8
        extra_Q_vars = []
        for i in params.V:
            for j in params.V:
                for k in params.K:
                    var = model.NewIntVar(0, min(params.Q[k], params.Q[k] + params.q[i]), f'extra_Q_{(i, j, k)}')
                    extra_Q_vars.append(var)
                    model.AddMultiplicationEquality(var, variables=[Q[(i, k)], x[(i, j, k)]])
                    model.Add(Q[(j, k)] >= var + params.q[j] * x[(i, j, k)])

        # constraint 9
        for i in params.P:
            for k in params.K:
                model.Add(T[(params.n + i, k)] - T[(i, k)] - params.s[i] - params.t[(i, params.n + i)] >= 0)

        # constraint 10
        for k in params.K:
            model.Add(T[(2 * params.n + 1, k)] - T[(0, k)] <= params.L[k])

        # constraint 1
        model.Minimize(sum([params.c[(i, j)] * x[(i, j, k)] for k in params.K for i in params.V for j in params.V]))

        solver = cp_model.CpSolver()
        status = solver.Solve(model)

        logging.info(status)
        logging.info(solver.ResponseStats())

        res_x = {k: solver.Value(v) for k, v in x.items()}
        res_T = {k: solver.Value(v) for k, v in T.items()}
        res_Q = {k: solver.Value(v) for k, v in Q.items()}

        return ORToolsOutput(x=res_x, T=res_T, Q=res_Q)
