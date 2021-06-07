from dataclasses import dataclass


@dataclass
class ORToolsOptimizerInputParams:
    A: list
    V: list
    P: list
    D: list
    K: list
    n: int
    s: dict
    c: dict
    t: dict
    q: dict
    Q: dict
    L: dict
    a: dict
    b: dict


@dataclass
class ORToolsOptimizerConfig:
    pass


@dataclass
class ORToolsOutput:
    x: dict
    T: dict
    Q: dict


# OutputType

class ORToolsOptimizerServiceABC:
    def solve(self, params: ORToolsOptimizerInputParams, config: ORToolsOptimizerConfig):
        pass
