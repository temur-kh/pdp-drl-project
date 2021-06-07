from dataclasses import dataclass

from dataclasses_json import dataclass_json, Undefined


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class TransportUnit:
    id: str
    capacity: int  # liters
    weight: int  # grams
    max_working_time: int  # seconds
