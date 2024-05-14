#!/usr/bin/env python3
"""Unittests and Integration Tests"""

import unittest
from parameterized import parameterized
from typing import Dict, Any, Tuple
from utils import access_nested_map, get_json, memoize
from unittest.mock import patch, Mock


class TestAccessNestedMap(unittest.TestCase):
    """
    Test access_nested_map Class
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map: Dict[str, Any],
                               path: Tuple[str], expected: Any) -> None:
        """
        Test access_nested_map
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map: Dict[str, Any],
                                         path: Tuple[str]) -> None:
        """
        Test access_nested_map raises KeyError
        """
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """
    Test get_json Class
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch('requests.get')
    def test_get_json(self, test_url: str, test_payload: Dict[str, Any],
                      mock_get: Mock) -> None:
        """
        Test get_json
        """
        mock_get.return_value.json.return_value = test_payload
        self.assertEqual(get_json(test_url), test_payload)
        mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """Test memoize class"""

    def test_memoize(self) -> None:
        """Test Memoize method"""

        class TestClass:

            def a_method(self):
                """a_method"""
                return 42

            @memoize
            def a_property(self):
                """a_property"""
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mock:
            test_class = TestClass()
            res1 = test_class.a_property
            res2 = test_class.a_property
            self.assertEqual(res1, 42)
            self.assertEqual(res2, 42)
            mock.assert_called_once()
