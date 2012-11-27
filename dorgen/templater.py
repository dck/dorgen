#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Templater:

    def __init__(self, text, data, deploy = "."):
        self.text = text
        self.data = data
        self.deploy = deploy

    def run(self):
        pass