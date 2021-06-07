from dataclasses import dataclass

from dataclasses_json import dataclass_json, Undefined


# TODO: integrate
@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class Constraint:
    name: int
    type: str
    data_type: str
    data: object
