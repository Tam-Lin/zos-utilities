import pytest

from src.zos_utilities.data_set import DataSet
from src.zos_utilities.dasd_volume import DasdVolume
from src.zos_utilities.lpar import LPAR


class Test_LPAR_Parse_D_ASM():

    @pytest.fixture
    def good_d_asm_output_scm_present_not_used(self):
        return [
            "  IEE200I 16.03.37 DISPLAY ASM 913          ",
            "  TYPE     FULL STAT   DEV  DATASET NAME    ",
            "  PLPA      45%   OK  2212  SYS1.R7A.PLPA   ",
            "  COMMON     7%   OK  2212  SYS1.R7A.COMMON ",
            "  LOCAL      0%   OK  222A  SYS1.R7A.LOCAL  ",
            "  LOCAL      0%   OK  2282  SYS1.R7A.LOCAL1 ",
            "  LOCAL      0%   OK  228A  SYS1.R7A.LOCAL2 ",
            "  LOCAL      0%   OK  229A  SYS1.R7A.LOCAL3 ",
            "  LOCAL      0%   OK  9645  SYS1.R7A.LOCAL6 ",
            "  LOCAL      0%   OK  9646  SYS1.R7A.LOCAL7 ",
            "  LOCAL      0%   OK  9814  SYS1.R7A.LOCAL8 ",
            "  SCM        0%   OK   N/A   N/A            ",
            "  PAGEDEL COMMAND IS NOT ACTIVE             "
        ]

    @pytest.fixture
    def good_d_asm_output_no_scm(self):
        return [
          "  IEE200I 16.32.55 DISPLAY ASM 992         ",
          "  TYPE     FULL STAT   DEV  DATASET NAME   ",
          "  PLPA      44 % OK  2214  SYS1.R7C.PLPA   ",
          "  COMMON     7 % OK  2214  SYS1.R7C.COMMON ",
          "  LOCAL      0 % OK  222C  SYS1.R7C.LOCAL  ",
          "  LOCAL      0 % OK  2284  SYS1.R7C.LOCAL1 ",
          "  LOCAL      0 % OK  228C  SYS1.R7C.LOCAL2 ",
          "  LOCAL      0 % OK  229C  SYS1.R7C.LOCAL3 ",
          "  LOCAL      0 % OK  9946  SYS1.R7C.LOCAL6 ",
          "  LOCAL      0 % OK  9947  SYS1.R7C.LOCAL7 ",
          "  LOCAL      0 % OK  9945  SYS1.R7C.LOCAL8 ",
          "  LOCAL      0 % OK  9649  SYS1.R7C.LOCAL9 ",
          "  LOCAL      0 % OK  964A  SYS1.R7C.LOCALA ",
          "  LOCAL      0 % OK  981A  SYS1.R7C.LOCALB ",
          "  PAGEDEL COMMAND IS NOT ACTIVE            "
        ]

    @pytest.fixture
    def good_d_asm_output_scm_in_use(self):
        return [
          "  IEE200I 16.32.55 DISPLAY ASM 992         ",
          "  TYPE     FULL STAT   DEV  DATASET NAME   ",
          "  PLPA      44 % OK  2214  SYS1.R7C.PLPA   ",
          "  COMMON     7 % OK  2214  SYS1.R7C.COMMON ",
          "  LOCAL      0 % OK  222C  SYS1.R7C.LOCAL  ",
          "  LOCAL      0 % OK  2284  SYS1.R7C.LOCAL1 ",
          "  LOCAL      0 % OK  228C  SYS1.R7C.LOCAL2 ",
          "  LOCAL      0 % OK  229C  SYS1.R7C.LOCAL3 ",
          "  LOCAL      0 % OK  9946  SYS1.R7C.LOCAL6 ",
          "  LOCAL      0 % OK  9947  SYS1.R7C.LOCAL7 ",
          "  LOCAL      0 % OK  9945  SYS1.R7C.LOCAL8 ",
          "  LOCAL      0 % OK  9649  SYS1.R7C.LOCAL9 ",
          "  LOCAL      0 % OK  964A  SYS1.R7C.LOCALA ",
          "  LOCAL      0 % OK  981A  SYS1.R7C.LOCALB ",
          "  SCM        0%   OK   N/A   N/A           ",
          "  PAGEDEL COMMAND IS NOT ACTIVE            "
        ]

    def test_d_asm_output_no_scm(self, good_d_asm_output_no_scm):

        test_lpar = LPAR()

        test_lpar.parse_d_asm(good_d_asm_output_no_scm)

        plpa_dasd = DasdVolume(unit_address="2214")
        common_dasd = DasdVolume(unit_address="2214")
        local_dasd = DasdVolume(unit_address="222C")
        local_dasd1 = DasdVolume(unit_address="2284")
        local_dasd2 = DasdVolume(unit_address="228C")
        local_dasd3 = DasdVolume(unit_address="229C")
        local_dasd6 = DasdVolume(unit_address="9946")
        local_dasd7 = DasdVolume(unit_address="9947")
        local_dasd8 = DasdVolume(unit_address="9945")
        local_dasd9 = DasdVolume(unit_address="9649")
        local_dasda = DasdVolume(unit_address="964A")
        local_dasdb = DasdVolume(unit_address="981A")

        plpa_dataset = DataSet(name="SYS1.R7C.PLPA", location=plpa_dasd)
        common_dataset = DataSet(name="SYS1.R7C.COMMON", location=common_dasd)
        local_dataset_list = [
            DataSet(name="SYS1.R7C.LOCAL", location=local_dasd),
            DataSet(name="SYS1.R7C.LOCAL1", location=local_dasd1),
            DataSet(name="SYS1.R7C.LOCAL2", location=local_dasd2),
            DataSet(name="SYS1.R7C.LOCAL3", location=local_dasd3),
            DataSet(name="SYS1.R7C.LOCAL6", location=local_dasd6),
            DataSet(name="SYS1.R7C.LOCAL7", location=local_dasd7),
            DataSet(name="SYS1.R7C.LOCAL8", location=local_dasd8),
            DataSet(name="SYS1.R7C.LOCAL9", location=local_dasd9),
            DataSet(name="SYS1.R7C.LOCALA", location=local_dasda),
            DataSet(name="SYS1.R7C.LOCALB", location=local_dasdb)
        ]

        assert test_lpar.plpa_data_set == plpa_dataset
        assert test_lpar.common_data_set == common_dataset
        assert test_lpar.local_data_set == local_dataset_list
        assert test_lpar.scm is None

    def test_d_asm_output_scm_in_use(self, good_d_asm_output_no_scm):

        test_lpar = LPAR()

        test_lpar.parse_d_asm(good_d_asm_output_no_scm)

        plpa_dasd = DasdVolume(unit_address="2214")
        common_dasd = DasdVolume(unit_address="2214")
        local_dasd = DasdVolume(unit_address="222C")
        local_dasd1 = DasdVolume(unit_address="2284")
        local_dasd2 = DasdVolume(unit_address="228C")
        local_dasd3 = DasdVolume(unit_address="229C")
        local_dasd6 = DasdVolume(unit_address="9946")
        local_dasd7 = DasdVolume(unit_address="9947")
        local_dasd8 = DasdVolume(unit_address="9945")
        local_dasd9 = DasdVolume(unit_address="9649")
        local_dasda = DasdVolume(unit_address="964A")
        local_dasdb = DasdVolume(unit_address="981A")

        plpa_dataset = DataSet(name="SYS1.R7C.PLPA", location=plpa_dasd)
        common_dataset = DataSet(name="SYS1.R7C.COMMON", location=common_dasd)
        local_dataset_list = [
            DataSet(name="SYS1.R7C.LOCAL", location=local_dasd),
            DataSet(name="SYS1.R7C.LOCAL1", location=local_dasd1),
            DataSet(name="SYS1.R7C.LOCAL2", location=local_dasd2),
            DataSet(name="SYS1.R7C.LOCAL3", location=local_dasd3),
            DataSet(name="SYS1.R7C.LOCAL6", location=local_dasd6),
            DataSet(name="SYS1.R7C.LOCAL7", location=local_dasd7),
            DataSet(name="SYS1.R7C.LOCAL8", location=local_dasd8),
            DataSet(name="SYS1.R7C.LOCAL9", location=local_dasd9),
            DataSet(name="SYS1.R7C.LOCALA", location=local_dasda),
            DataSet(name="SYS1.R7C.LOCALB", location=local_dasdb)
        ]

        assert test_lpar.plpa_data_set == plpa_dataset
        assert test_lpar.common_data_set == common_dataset
        assert test_lpar.local_data_set == local_dataset_list
        assert test_lpar.scm is None
