import os

import pytest
from mock import patch

import gease.constants as constants
import gease.exceptions as exceptions
from gease.utils import get_info


class TestMain:
    def setup_method(self):
        self.patcher = patch("gease.utils.os.path.expanduser")
        self.fake_expand = self.patcher.start()
        self.fake_expand.return_value = os.path.join("tests", "fixtures")

    def teardown_method(self):
        self.patcher.stop()

    def test_get_token(self):
        self.fake_expand.return_value = os.path.join("tests", "fixtures")
        user = get_info(constants.KEY_GEASE_TOKEN)
        assert user == "test"

    def test_no_gease_file(self):
        self.fake_expand.return_value = os.path.join("tests")
        with pytest.raises(exceptions.NoGeaseConfigFound):
            get_info(constants.KEY_GEASE_TOKEN)

    def test_wrong_key(self):
        self.fake_expand.return_value = os.path.join(
            "tests", "fixtures", "malformed"
        )
        with pytest.raises(KeyError):
            get_info(constants.KEY_GEASE_TOKEN)
