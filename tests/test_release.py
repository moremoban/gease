from mock import MagicMock, patch
import pytest

import gease.exceptions as exceptions
from gease.release import EndPoint


class TestPublish:
    def setup_method(self):
        self.patcher = patch("gease.release.Api")
        self.fake_api_singleton = self.patcher.start()
        self.fake_api = MagicMock()
        self.fake_api_singleton.get_api = self.fake_api
        self.patcher2 = patch("gease.rest.get_token")
        self.fake_token = self.patcher2.start()
        self.fake_token.return_value = "token"

    def teardown_method(self):
        self.patcher2.stop()
        self.patcher.stop()

    def test_create_release(self):
        self.fake_api.return_value = MagicMock(
            create=MagicMock(return_value={"html_url": "aurl"})
        )
        release = EndPoint("owner", "repo")
        release.publish(hello="world")

    def test_unknown_error(self):
        self.fake_api.return_value = MagicMock(
            create=MagicMock(return_value={})
        )
        release = EndPoint("owner", "repo")
        with pytest.raises(exceptions.AbnormalGithubResponse):
            release.publish(hello="world")

    def test_release_exist(self):
        self.fake_api.return_value = MagicMock(
            create=MagicMock(side_effect=exceptions.ReleaseExistException)
        )
        release = EndPoint("owner", "repo")
        with pytest.raises(exceptions.AbnormalGithubResponse):
            release.publish(hello="world", tag_name="existing tag")

    def test_repo_not_found(self):
        self.fake_api.return_value = MagicMock(
            create=MagicMock(side_effect=exceptions.RepoNotFoundError)
        )
        release = EndPoint("owner", "repo")
        release.republish = MagicMock(side_effect=exceptions.RepoNotFoundError)
        with pytest.raises(exceptions.AbnormalGithubResponse):
            release.publish(hello="world")

    def test_unhandled_exception(self):
        self.fake_api.return_value = MagicMock(
            create=MagicMock(side_effect=exceptions.UnhandledException)
        )
        release = EndPoint("owner", "repo")
        with pytest.raises(exceptions.AbnormalGithubResponse):
            release.publish(hello="world")


class TestRepublish:
    def setup_method(self):
        self.patcher = patch("gease.release.Orgs")
        self.fake_orgs = self.patcher.start()
        self.patcher2 = patch("gease.release.Repo")
        self.fake_repo = self.patcher2.start()
        self.patcher3 = patch("gease.release.Api")
        self.fake_api_singleton = self.patcher3.start()
        self.fake_api = MagicMock()
        self.fake_api_singleton.get_api = self.fake_api

    def teardown_method(self):
        self.patcher3.stop()
        self.patcher2.stop()
        self.patcher.stop()

    def test_create_release(self):
        test_url = "special url"
        self.fake_orgs.return_value = MagicMock(
            get_all_organisations=MagicMock(
                return_value=[{"repos_url": "repo", "login": "zhangfei"}]
            )
        )
        self.fake_repo.return_value = MagicMock(
            get_all_repos=MagicMock(return_value=[{"name": "repo"}])
        )
        self.fake_api.return_value = MagicMock(
            create=MagicMock(return_value={"html_url": test_url})
        )
        release = EndPoint("owner", "repo")
        ret = release.republish(hello="world")
        assert ret == test_url
