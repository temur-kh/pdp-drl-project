from dataclasses import dataclass

from dataclasses_json import dataclass_json, Undefined


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class Query:
    created_at: int
    origin_node: str
    destination_node: str
    capacity: int
    weight: int
    operation_duration: int

