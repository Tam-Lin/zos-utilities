import logging


class CPC():
    """
    Represents an IBM Z CPC, aka CEC
    """

    def __init__(self):
        self.name = None
        self.status = None

        self.machine_model = None
        self.machine_type = None
        self.physical_general_processors = None
        self.physical_ziips = None
        self.physical_zaaps = None
        self.physical_ifls = None
        self.physical_icfs = None

        self.lpars = dict()

        self.start_data_gathering = None
        self.finish_data_gathering = None
