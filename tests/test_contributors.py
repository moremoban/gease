from mock import MagicMock, patch

from gease.contributors import EndPoint
from gease.exceptions import NoGeaseConfigFound


class TestPublish:
    @patch("gease.contributors.get_token")
    @patch("gease.contributors.Api.get_public_api")
    def test_all_contributors(self, fake_api, get_token):
        get_token.side_effect = [NoGeaseConfigFound]
        sample_reply = [
            {"login": "howdy", "url": "https://api.github.com/users/howdy"}
        ]
        fake_api.return_value = MagicMock(
            get=MagicMock(
                side_effect=[
                    sample_reply,
                    {"name": "hello world", "html_url": ""},
                ]
            )
        )

        repo = EndPoint("test", "repo")
        contributors = repo.get_all_contributors()

        assert contributors == [{"name": "hello world", "html_url": ""}]

    @patch("gease.contributors.get_token")
    @patch("gease.contributors.Api.get_public_api")
    def test_private_api(self, fake_api, get_token):
        get_token.side_effect = [NoGeaseConfigFound]
        sample_reply = [
            {"login": "howdy", "url": "https://api.github.com/users/howdy"}
        ]
        fake_api.return_value = MagicMock(
            get=MagicMock(
                side_effect=[sample_reply, {"name": None, "html_url": ""}]
            )
        )

        repo = EndPoint("test", "repo")
        contributors = repo.get_all_contributors()

        assert contributors == [{"name": "howdy", "html_url": ""}]

    @patch("gease.contributors.get_token")
    @patch("gease.contributors.Api.get_api")
    def test_no_names(self, fake_api, _):
        sample_reply = [
            {"login": "howdy", "url": "https://api.github.com/users/howdy"}
        ]
        fake_api.return_value = MagicMock(
            get=MagicMock(
                side_effect=[sample_reply, {"name": None, "html_url": ""}]
            )
        )

        repo = EndPoint("test", "repo")
        contributors = repo.get_all_contributors()

        assert contributors == [{"name": "howdy", "html_url": ""}]
