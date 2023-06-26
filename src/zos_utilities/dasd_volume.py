import dataclasses


@dataclasses.dataclass
class DasdVolume:
    """
    Represents a DASD volume
    """

    volser: str = None
    unit_address: str = None
