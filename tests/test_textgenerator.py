#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from dorgen.textgenerator import TextGenerator



class TestTextGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = TextGenerator()

    def test_simple_generation(self):
        t = "{1|2} {3|4}"
        need = sorted(["1 3", "1 4", "2 3", "2 4"])
        res = self.generator.generate(t)
        self.assertEqual(need, res)

    def test_complex_generation(self):
        t = "{1|2} %kw% {3|4}"
        need = sorted(["1 %kw% 3", "1 %kw% 4", "2 %kw% 3", "2 %kw% 4"])
        res = sorted(self.generator.generate(t))
        self.assertEqual(need, res)

    def test_multilevel_generation(self):
        t = "{1|2{a|b}} {4|5}"
        need = sorted(["1 4", "2a 4", "2b 4", "1 5", "2a 5", "2b 5"])
        res = sorted(self.generator.generate(t))
        self.assertEqual(need, res)