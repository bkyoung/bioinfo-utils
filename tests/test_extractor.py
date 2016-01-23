#!/usr/bin/env python

import unittest, os, sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

import extractor

class TestExtractorMethods(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_listify(self):
        str = "1,2,3,4,5"
        actual = extractor.listify(str)
        desired = [`x` for x in range(1,6)]
        self.assertListEqual(actual, desired)

    def test_find_column_by_name(self):
        l = ["col1","col2","col3","col4"]
        c = "col2"
        actual = extractor.find_column_by_name(l, c)
        desired = "2"
        self.assertEqual(actual, desired)

    def test_get_columns(self):
        l = ["col1","col2","col3","col4"]
        s = "1:2"
        actual = extractor.get_columns(l, s)
        desired = ["col1", "col2"]
        self.assertListEqual(actual, desired)

    def test_match_line_and(self):
        l = ["col1","col2","col3","col4"]
        s_true = "1:col1,2:col2"
        s_false = "1:col1,2:col3"
        actual_true = extractor.match_line_and(l, s_true)
        actual_false = extractor.match_line_and(l, s_false)
        self.assertTrue(actual_true)
        self.assertFalse(actual_false)

    def test_match_line_or(self):
        l = ["col1","col2","col3","col4"]
        s = "1:col1,2:col3"
        result = extractor.match_line_or(l, s)
        self.assertTrue(result)

    def test_extracted_line(self):
        l = ["col1","col2","col3","col4"]
        cl = "2,3"
        dc = ","
        dt = "\t"
        actual_comma = extractor.extracted_line(l, cl, dc)
        desired_comma = "col2,col3\n"
        self.assertEqual(actual_comma, desired_comma)
        actual_tab = extractor.extracted_line(l, cl, dt)
        desired_tab = "col2\tcol3\n"


if __name__ == '__main__':
    unittest.main()