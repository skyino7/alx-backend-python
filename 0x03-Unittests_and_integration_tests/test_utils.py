#!/usr/bin/env python3
"""Unittests and Integration Tests"""

import unittest
from parameterized import parameterized


def access_nested_map(nested_map, path):
    """
    Access nested map
    """
    for key in path:
        if key in nested_map:
            nested_map = nested_map[key]
        else:
            return None
    return nested_map


class TestAccessNestedMap(unittest.TestCase):
    """
    Test access_nested_map Class
    """

    @parameterized.expand([
        ({'a': 1}, ['a'], 1),
        ({'a': {'b': 2}}, ['a', 'b'], 2),
        ({'a': {}}, ['a', 'b'], None),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Test access_nested_map Doc
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)