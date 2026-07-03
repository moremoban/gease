from mock import MagicMock, patch
import pytest

from gease.rest import Api
from gease.exceptions import (
    Forbidden,
    UrlNotFound,
    RepoNotFoundError,
    ReleaseExistException,
    AbnormalGithubResponse,
)

SAMPLE_422_ERROR = {
    "errors": [
        {"code": "already_exists", "field": "tag_name", "resource": "Release"}
    ],
    "documentation_url": "https://.../#create-a-release",
    "message": "Validation Failed",
}
WRONG_CREDENTIALS = {
    "message": "Bad credentials",
    "documentation_url": "https://developer.github.com/v3",
}


class TestApi:
    def setup_method(self):
        self.patcher = patch("gease.rest.requests.Session")
        self.fake_session = self.patcher.start()

    def teardown_method(self):
        self.patcher.stop()

    def test_create(self):
        self.fake_session.return_value = MagicMock(
            post=MagicMock(
                return_value=MagicMock(
                    status_code=201, json=MagicMock(return_value={})
                )
            )
        )
        api = Api("test")
        api.create("http://localhost/", "cool")

    def test_existing_release(self):
        self.fake_session.return_value = MagicMock(
            post=MagicMock(
                return_value=MagicMock(
                    status_code=422,
                    json=MagicMock(return_value=SAMPLE_422_ERROR),
                )
            )
        )
        api = Api("test")
        with pytest.raises(ReleaseExistException):
            api.create("http://localhost/", "cool")

    def test_wrong_credentials(self):
        self.fake_session.return_value = MagicMock(
            post=MagicMock(
                return_value=MagicMock(
                    status_code=401,
                    json=MagicMock(return_value=WRONG_CREDENTIALS),
                )
            )
        )
        api = Api("test")
        with pytest.raises(AbnormalGithubResponse):
            api.create("http://localhost/", "cool")

    def test_404(self):
        self.fake_session.return_value = MagicMock(
            post=MagicMock(
                return_value=MagicMock(
                    status_code=404,
                    json=MagicMock(return_value=WRONG_CREDENTIALS),
                )
            )
        )
        api = Api("test")
        with pytest.raises(RepoNotFoundError):
            api.create("http://localhost/", "cool")

    def test_unknown_error(self):
        self.fake_session.return_value = MagicMock(
            post=MagicMock(
                return_value=MagicMock(
                    status_code=400, json=MagicMock(return_value={})
                )
            )
        )
        api = Api("test")
        with pytest.raises(Exception):
            api.create("http://localhost/", "cool")

    def test_get_unknown_url(self):
        self.fake_session.return_value = MagicMock(
            get=MagicMock(side_effect=UrlNotFound)
        )
        api = Api("test")
        with pytest.raises(UrlNotFound):
            api.get("s")

    def test_get_forbidden_url(self):
        self.fake_session.return_value = MagicMock(
            get=MagicMock(side_effect=Forbidden)
        )
        api = Api("test")
        with pytest.raises(Forbidden):
            api.get("s")
