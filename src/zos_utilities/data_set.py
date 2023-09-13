import dataclasses

from typing import Union

from .dasd_volume import DasdVolume


@dataclasses.dataclass
class DataSet():

    """
    Represents a data set
    """

    name: str
    location: Union[None, DasdVolume] = None
