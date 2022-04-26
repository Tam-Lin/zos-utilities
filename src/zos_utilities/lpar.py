import re
import logging

from collections import OrderedDict

class LPAR():
    """
    Represents a IBM z/OS LPAR
    """

    def __init__(self):

        logger = logging.getLogger(__name__)

        self.logical_processors = OrderedDict()

        self.physical_cpus = OrderedDict()
        self.hiperdispatch = None
        self.mt_mode = None
        self.cp_mt_mode = None
        self.ziip_mt_mode = None
        self.cpc_nd = None
        self.cpc_si = None
        self.cpc_model = None
        self.cpc_id = None
        self.cpc_name = None
        self.lpar_name = None
        self.lpar_id = None
        self.css_id = None
        self.mif_id = None

        self.name = None
        self.part_id = None
        self.partition_number = None
        self.CPC = None
        self.shared_processors = None
        self.active = None
        self.IPL_volume = None
        self.os = None
        self.os_name = None
        self.os_level = None
        self.last_updated = None
        self.url = None
        self.start_update = None
        self.finish_update = None

        self.number_general_cpus = None
        self.number_reserved_cps = None
        self.number_general_cores = None
        self.number_reserved_cores = None

        self.number_ziip_cpus = None
        self.number_reserved_ziip_cpus = None
        self.number_ziip_cores = None
        self.number_reserved_ziip_cores = None

        self.number_ifl_cpus = None
        self.number_reserved_ifl_cpus = None
        self.number_ifl_cores = None
        self.number_reserved_ifl_cores = None

        self.number_icf_cpus = None
        self.number_reserved_icf_cpus = None
        self.number_icf_cores = None
        self.number_reserved_icf_cores = None

        self.general_cp_weight_current = None
        self.general_cp_weight_minimum = None
        self.general_cp_weight_maximum = None

        self.zaap_weight = None
        self.zaap_weight_minimum = None
        self.zaap_weight_maximum = None

        self.ziip_weight = None
        self.ziip_weight_minimum = None
        self.ziip_weight_maximum = None

        self.ifl_weight = None
        self.ifl_weight_minimum = None
        self.ifl_weight_maximum = None

        self.icf_weight = None
        self.icf_weight_minimum = None
        self.icf_weight_maximum = None

        self.storage = None

        self.initial_central_storage = None
        self.current_central_storage = None
        self.maximum_central_storage = None

    def parse_d_m_core(self, iee174i_message):
        """
        Takes the output of the response to 'D M=CORE' and builds a representation of the system logical processor
        state at that time

        :param core_status_message: The output of the message you want parsed
        :return: Updates the internal state information of the lpar
        """

        logger = logging.getLogger(__name__)

        if iee174i_message[0].split()[0] != "IEE174I":
            raise LPARException("Incorrect message passed in")

        if iee174i_message[1].startswith("CORE STATUS:") == False:
            raise LPARException("IEE174I missing information")

        split_line_1 = iee174i_message[1].split()

        logger.debug(split_line_1)

        hd_value = split_line_1[2][3]

        logger.debug(hd_value)

        if hd_value == "Y":
            self.hiperdispatch = True
        elif hd_value == "N":
            self.hiperdispatch = False
        else:
            logger.exception(LPARException("HD= should be Y or N; got %s" % hd_value))

        mt_value = split_line_1[3][3]

        if split_line_1[3][0:2] != "MT=":
            logger.exception(LPARException("MT= was not in the correct place"))

        if mt_value.isdigit:
            self.mt_mode = int(mt_value)
        else:
            logger.exception(LPARException("MT= should be a number; got %s" % mt_value))

        cp_mt_mode = split_line_1[5][3]

        if split_line_1[5][0:2] != "CP=":
            logger.exception(LPARException("CP= was not in the correct place"))

        if split_line_1[5][3].isdigit:
            self.cp_mt_mode = int(cp_mt_mode)
        else:
            logger.exception(LPARException("CP= should be a number; got %s" % cp_mt_mode))

        ziip_mt_mode = split_line_1[6][5]

        if split_line_1[5][0:4] != "zIIP=":
            logger.exception(LPARException("zIIP= was not in the correct place; got %s" % split_line_1[5][0:4]))

        if ziip_mt_mode.isdigit:
            self.ziip_mt_mode = int(ziip_mt_mode)
        else:
            raise LPARException("zIIP= should be a number, got %s" % ziip_mt_mode)



        core_re = re.compile(
            '(?P<coreid>[0-9A-F]{4})  (?P<wlmmanaged>.)(?P<online>.)(?P<type>.)  (?P<lowid>[0-9A-F]{4})-(?P<highid>['
            '0-9A-F]{4})(  (?P<polarity>.)(?P<parked>.)  (?P<subclassmask>[0-9A-F]{4})  (?P<state1>.)(?P<state2>.))?')

        linenum = 3

        for linenum, line in enumerate(iee174i_message[3:], start=3):

            core_info = core_re.search(line)

            if core_info is None:
                break
            else:
                core = dict()

                core["coreid"] = core_info.group("coreid")

                if core_info.group("online") == "+":
                    core["online"] = True
                else:
                    core["online"] = False

                if core_info.group("type") == " ":
                    core["type"] = "CP"
                elif core_info.group("type") == "I":
                    core["type"] = "zIIP"

                core["lowid"] = core_info.group("lowid")
                core["highid"] = core_info.group("highid")

                core["polarity"] = core_info.group("polarity")

                if core_info.group("parked") == "P":
                    core["parked"] = True
                else:
                    core["parked"] = False

                core["subclassmask"] = core_info.group("subclassmask")

                if core_info.group("state1") == "+":
                    core["core_1_state"] = "online"
                elif core_info.group("state1") == "N":
                    core["core_1_state"] = "not_available"
                elif core_info.group("state1") == "-":
                    core["core_1_state"] = "offline"

                if core_info.group("state2") == "+":
                    core["core_2_state"] = "online"
                elif core_info.group("state2") == "N":
                    core["core_2_state"] = "not_available"
                elif core_info.group("state2") == "-":
                    core["core_2_state"] = "offline"

                self.logical_processors[core["coreid"]] = core

        linenum += 1

        if iee174i_message[linenum].startswith("CPC ND = "):
            self.cpc_nd = iee174i_message[linenum][9:].rstrip()
        else:
            error = ("line didn't start with CPC ND =; got %s" % iee174i_message[linenum])
            logger.error(error)
            raise LPARException(error)

        linenum += 1

        if iee174i_message[linenum].startswith("CPC SI = "):
            self.cpc_si = iee174i_message[linenum][9:].rstrip()
        else:
            error = ("line didn't start with CPC SI =; got %s" % iee174i_message[linenum])
            logger.error(error)
            raise LPARException(error)

        linenum += 1

        if iee174i_message[linenum].lstrip().startswith("Model: "):
            self.cpc_model = iee174i_message[linenum].lstrip()[7:].rstrip()
        else:
            error = ("line didn't start with Model =; got %s" % iee174i_message[linenum])
            logger.error(error)
            raise LPARException(error)

        linenum += 1

        if iee174i_message[linenum].startswith("CPC ID = "):
            self.cpc_id = iee174i_message[linenum][9:].rstrip()
        else:
            error = ("line didn't start with CPC ID = ;  got %s" % iee174i_message[linenum])
            logger.error(error)
            raise LPARException(error)

        linenum += 1

        if iee174i_message[linenum].startswith("CPC NAME = "):
            self.cpc_name = iee174i_message[linenum][11:].rstrip()
        else:
            error = ("line didn't start with CPC NAME = ;  got %s" % iee174i_message[linenum])
            logger.error(error)
            raise LPARException(error)

        linenum += 1

        if iee174i_message[linenum].startswith("LP NAME = "):
            self.lpar_name = iee174i_message[linenum][10:14].rstrip()
        else:
            error = ("line didn't start with LP NAME = ;  got %s" % iee174i_message[linenum])
            logger.error(error)
            raise LPARException(error)

        if iee174i_message[linenum][21:].startswith("LP ID = "):
            self.lpar_id = iee174i_message[linenum][29:].rstrip()
        else:
            error = ("LP ID not where I expected; got %s" % iee174i_message[linenum])
            logger.error(error)
            raise LPARException(error)

        linenum += 1

        if iee174i_message[linenum].startswith("CSS ID  = "):
            self.css_id = iee174i_message[linenum][10:].rstrip()
        else:
            error = ("line didn't start with CSS ID = ;  got %s" % iee174i_message[linenum])
            logger.error(error)
            raise LPARException(error)

        linenum += 1

        if iee174i_message[linenum].startswith("MIF ID  = "):
            self.mif_id = iee174i_message[linenum][10:].rstrip()
        else:
            error = ("line didn't start with MIF ID = ;  got %s" % iee174i_message[linenum])
            logger.error(error)
            raise LPARException(error)



class LPARException(Exception):
    pass