import sys
import pytest

import ncs_uml
from ncs_uml.main import NcsUml

class TestNcsUml:

    @pytest.fixture
    def setup(self):
        if sys.version_info.major == 2:
            import imp
            imp.reload(sys)
            sys.setdefaultencoding('utf-8')

        uml = NcsUml()
        yield uml

    def test_ncs_uml_module(self):
        assert ncs_uml.__name__ == 'ncs_uml'
        assert ncs_uml.__version__ == '1.1.0'
        assert ncs_uml.__description__ == ncs_uml.__description__

    def test_uml_generation(self, setup):
        pass