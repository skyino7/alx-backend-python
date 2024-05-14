#!/usr/bin/env python3
"""Unittests and Integration Tests"""

import unittest
from parameterized import parameterized
from typing import Dict, Any, Tuple
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """
    Test access_nested_map Class
    """

    @parameterized.expand([
        ({'a': 1}, ['a'], 1),
        ({'a': {'b': 2}}, ['a', 'b'], 2),
        ({'a': {}}, ['a', 'b'], None),
    ])
    def test_access_nested_map(self, nested_map: Dict[str, Any],
                               path: Tuple[str], expected: Any) -> None:
        """
        Test access_nested_map Doc
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ['a']),
        ({'a': 1}, ['a', 'b']),
    ])
    def test_access_nested_map_exception(self, nested_map: Dict[str, Any],
                                         path: Tuple[str]) -> None:
        """
        Test access_nested_map_exception Doc
        """
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)
