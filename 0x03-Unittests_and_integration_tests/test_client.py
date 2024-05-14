#!/usr/bin/env python3
"""Unittests for client.GithubOrgClient"""

import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


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

    @patch('client.get_json', return_value=[{"name": "repo1"}, {"name": "repo2"}])
    @patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock)
    def test_public_repos(self, mock_public_repos_url, mock_get_json):
        """
        Test that GithubOrgClient.public_repos returns the correct value
        """
        mock_public_repos_url.return_value = "https://api.github.com/orgs/test-org/repos"
        github_org_client = GithubOrgClient("test-org")
        result = github_org_client.public_repos()
        mock_get_json.assert_called_once()
        mock_public_repos_url.assert_called_once()
        self.assertEqual(result, ["repo1", "repo2"])
