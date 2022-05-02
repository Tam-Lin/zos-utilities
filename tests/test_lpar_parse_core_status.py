import pytest

from src.zos_utilities import lpar


class Test_LPAR_Parse_D_M_CORE():

    @pytest.fixture
    def good_input(self):
        return ["IEE174I 14.41.05 DISPLAY M 124                  ",
                "CORE STATUS: HD=Y   MT=2  MT_MODE: CP=1  zIIP=2",
                "ID    ST   ID RANGE   VP  ISCM  CPU THREAD STATUS          ",
                "0000   +   0000-0001  H   FC00  +N                         ",
                "0001   +   0002-0003  M   0000  +N                         ",
                "0002   +   0004-0005  M   0000  +N                         ",
                "0003   +   0006-0007  LP  0000  +N                         ",
                "0004   +   0008-0009  LP  0000  +N                         ",
                "0005   +   000A-000B  LP  0000  +N                         ",
                "0006   +   000C-000D  LP  0000  +N                         ",
                "0007   +   000E-000F  LP  0000  +N                         ",
                "0008   +   0010-0011  LP  0000  +N                         ",
                "0009   +   0012-0013  LP  0000  +N                         ",
                "000A   +   0014-0015  LP  0000  +N                         ",
                "000B   +   0016-0017  LP  0000  +N                         ",
                "000C   +   0018-0019  LP  0000  +N                         ",
                "000D   +   001A-001B  LP  0000  +N                         ",
                "000E   +   001C-001D  LP  0000  +N                         ",
                "000F   +   001E-001F  LP  0000  +N                         ",
                "0010   +   0020-0021  LP  0000  +N                         ",
                "0011   +   0022-0023  LP  0000  +N                         ",
                "0012   +   0024-0025  LP  0000  +N                         ",
                "0013   +   0026-0027  LP  0000  +N                         ",
                "0014   +I  0028-0029  H   0200  ++                         ",
                "0015   +I  002A-002B  M   0200  ++                         ",
                "0016   +I  002C-002D  M   0200  ++                         ",
                "0017   -I  002E-002F                                       ",
                "0018   -I  0030-0031                                       ",
                "0019   -I  0032-0033                                       ",
                "001A   -I  0034-0035                                       ",
                "001B   -I  0036-0037                                       ",
                "001C   -I  0038-0039                                       ",
                "001D   -I  003A-003B                                       ",
                "001E   -I  003C-003D                                       ",
                "001F   -I  003E-003F                                       ",
                "0020   -I  0040-0041                                       ",
                "0021   -I  0042-0043                                       ",
                "0022   -I  0044-0045                                       ",
                "0023   -I  0046-0047                                       ",
                "0024   NI  0048-0049                                       ",
                "0025   NI  004A-004B                                       ",
                "0026   NI  004C-004D                                       ",
                "0027   NI  004E-004F                                       ",
                "0028   NI  0050-0051                                       ",
                "0029   NI  0052-0053                                       ",
                "002A   NI  0054-0055                                       ",
                "002B   NI  0056-0057                                       ",
                "",
                "CPC ND = 008561.T01.IBM.02.000000000078                    ",
                "CPC SI = 8561.776.IBM.02.0000000000000078                  ",
                "          Model: T01                                       ",
                "CPC ID = 00                                                ",
                "CPC NAME = T78                                             ",
                "LP NAME = CB8A       LP ID = 1B                            ",
                "CSS ID  = 1                                                ",
                "MIF ID  = B                                                ",
                "",
                "+ ONLINE    - OFFLINE    N NOT AVAILABLE    / MIXED STATE ",
                "W WLM-MANAGED                                              ",
                ""                                                          ","
                "I        INTEGRATED INFORMATION PROCESSOR (zIIP)           ",
                "CPC ND  CENTRAL PROCESSING COMPLEX NODE DESCRIPTOR         ",
                "CPC SI  SYSTEM INFORMATION FROM STSI INSTRUCTION           ",
                "CPC ID  CENTRAL PROCESSING COMPLEX IDENTIFIER              ",
                "CPC NAME CENTRAL PROCESSING COMPLEX NAME                   ",
                "LP NAME  LOGICAL PARTITION NAME                            ",
                "LP ID    LOGICAL PARTITION IDENTIFIER                      ",
                "CSS ID   CHANNEL SUBSYSTEM IDENTIFIER                      ",
                "MIF ID   MULTIPLE IMAGE FACILITY IMAGE IDENTIFIER          ",
                "IEE174I 14.41.05 DISPLAY M 124                             ",
                "CORE STATUS: HD=Y   MT=2  MT_MODE: CP=1  zIIP=2            "]

    def test_lpar_parse_d_m_core(self, good_input):
        test_lpar = lpar.LPAR()

        test_lpar.parse_d_m_core(good_input)

        assert test_lpar.hiperdispatch is True
        assert test_lpar.mt_mode == 2
        assert test_lpar.cp_mt_mode == 1
        assert test_lpar.ziip_mt_mode == 2

        assert len(test_lpar.logical_processors) == 44

        core_0014 = test_lpar.logical_processors["0014"]

        assert core_0014.type == "zIIP"
        assert core_0014.online is True
        assert core_0014.lowid == "0028"
        assert core_0014.highid == "0029"
        assert core_0014.polarity == "H"
        assert core_0014.parked is False
        assert core_0014.subclassmask == "0200"
        assert core_0014.core_1_state == "online"
        assert core_0014.core_2_state == "online"

        assert test_lpar.cpc_nd == "008561.T01.IBM.02.000000000078"
        assert test_lpar.cpc_si == "8561.776.IBM.02.0000000000000078"
        assert test_lpar.cpc_model == "T01"
        assert test_lpar.cpc_id == "00"
        assert test_lpar.cpc_name == "T78"
        assert test_lpar.lpar_name == "CB8A"
        assert test_lpar.lpar_id == "1B"
        assert test_lpar.css_id == "1"
        assert test_lpar.mif_id == "B"

    def test_missing_IEE174I(self, good_input):

        bad_input = ["14.41.05 DISPLAY M 124                  "] + \
                    good_input[1:]

        with pytest.raises(lpar.LPARException):
            test_lpar = lpar.LPAR()
            test_lpar.parse_d_m_core(bad_input)

    def test_bad_hyperdispatch_value(self, good_input):

        bad_input = [good_input[0]] + \
                     ["CORE STATUS: HD=L   MT=2  MT_MODE: CP=1  zIIP=2"] + \
                     good_input[2:]

        with pytest.raises(lpar.LPARException):
            test_lpar = lpar.LPAR()
            test_lpar.parse_d_m_core(bad_input)

    def test_bad_mt_statement(self, good_input):

        bad_input = [good_input[0]] + \
                    ["CORE STATUS: HD=Y   TM=2  MT_MODE:2 CP=1  zIIP=2"] + \
                     good_input[2:]

        with pytest.raises(lpar.LPARException):
            test_lpar = lpar.LPAR()
            test_lpar.parse_d_m_core(bad_input)

    def test_bad_mt_mode_value(self, good_input):

        bad_input = [good_input[0]] + \
                     ["CORE STATUS: HD=Y   MT=L  MT_MODE: CP=1  zIIP=2"] + \
                     good_input[2:]

        with pytest.raises(lpar.LPARException):
            test_lpar = lpar.LPAR()
            test_lpar.parse_d_m_core(bad_input)

    def test_bad_cp_mt_mode_value(self, good_input):

        bad_input = [good_input[0]] + \
                     ["CORE STATUS: HD=Y   MT=L  MT_MODE:2 CP=N  zIIP=2"] + \
                     good_input[2:]

        with pytest.raises(lpar.LPARException):
            test_lpar = lpar.LPAR()
            test_lpar.parse_d_m_core(bad_input)

    def test_bad_cp_mt_mode_statement(self, good_input):

        bad_input = [good_input[0]] + \
                     ["CORE STATUS: HD=Y   MT=L  MT_MODE:2 PC=2  zIIP=2"] + \
                     good_input[2:]

        with pytest.raises(lpar.LPARException):
            test_lpar = lpar.LPAR()
            test_lpar.parse_d_m_core(bad_input)

    def test_bad_ziip_mt_mode_value(self, good_input):

        bad_input = [good_input[0]] + \
                     ["CORE STATUS: HD=Y   MT=L  MT_MODE:2 CP=1  zIIP=J"] + \
                     good_input[2:]

        with pytest.raises(lpar.LPARException):
            test_lpar = lpar.LPAR()
            test_lpar.parse_d_m_core(bad_input)
