#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from dorgen.textgenerator import TextGenerator



class TestTextGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = TextGenerator(capitalize = True)

    def test_simple_generation(self):
        t = "{1|2} {3|4}"
        need = sorted(["1 3", "1 4", "2 3", "2 4"])
        res = sorted(self.generator.generate(t))
        self.assertEqual(need, res)

    def test_complex_generation(self):
        t = "{1|2} %kw% {3|4}"
        need = sorted(["1 %kw% 3", "1 %kw% 4", "2 %kw% 3", "2 %kw% 4"])
        res = sorted(self.generator.generate(t))
        self.assertEqual(need, res)

    def test_capitalizing(self):
        text = "i want to born. hey, lala ley!   what?damn, it! yes!!! da?! v"
        cap_text = self.generator.smart_capitalize(text)
        self.assertEqual(cap_text, "I want to born. Hey, lala ley!   What?Damn, it! Yes!!! Da?! V")