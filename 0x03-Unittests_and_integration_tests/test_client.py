#!/usr/bin/env python3
"""Unittests for client.GithubOrgClient"""

import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """
    TestGithubOrgClient class to test GithubOrgClient.org
    """

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"})
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str,
                 expected_response: dict, mock_get_json: Mock) -> None:
        """
        Test that GithubOrgClient.org returns the correct value
        """
        mock_get_json.return_value = expected_response
        client = GithubOrgClient(org_name)
        result = client.org
        url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(url)
        self.assertEqual(result, expected_response)

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """
        Test that GithubOrgClient._public_repos_url returns the correct value
        """
        url = f"https://api.github.com/orgs/test-org/repos"
        mock_org.return_value = {"repos_url": url}
        client = GithubOrgClient("test-org")
        result = client._public_repos_url
        self.assertEqual(result, url)

    @patch('client.get_json', return_value=[{"name": "repo1"},
                                            {"name": "repo2"}])
    @patch('client.GithubOrgClient._public_repos_url',
           new_callable=PropertyMock)
    def test_public_repos(self, mock_public_repos_url, mock_get_json):
        """
        Test that GithubOrgClient.public_repos returns the correct value
        """
        url = f"https://api.github.com/orgs/test-org/repos"
        mock_public_repos_url.return_value = url
        github_org_client = GithubOrgClient("test-org")
        result = github_org_client.public_repos()
        mock_get_json.assert_called_once()
        mock_public_repos_url.assert_called_once()
        self.assertEqual(result, ["repo1", "repo2"])

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False)
    ])
    def test_has_license(self, repo: dict, license_key: str,
                         expected: bool) -> None:
        """
        Test that GithubOrgClient.has_license returns the correct value
        """
        client = GithubOrgClient("test_org")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)

@parameterized_class(('org_payload', 'repos_payload',
                      'expected_repos', 'apache2_repos'), TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Set up the class by patching requests.get"""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            """Mocked side effect function for requests.get"""
            class MockResponse:
                def __init__(self, json_data):
                    self.json_data = json_data

                def json(self):
                    return self.json_data

            if url.endswith("/orgs/google"):
                return MockResponse(cls.org_payload)
            elif url.endswith("/orgs/google/repos"):
                return MockResponse(cls.repos_payload)
            else:
                return None

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Tear down the class by stopping the patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test the public_repos method"""
        github_org_client = GithubOrgClient("google")
        result = github_org_client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test the public_repos method filtering by license"""
        github_org_client = GithubOrgClient("google")
        result = github_org_client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)
