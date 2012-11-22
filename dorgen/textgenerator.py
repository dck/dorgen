#!/usr/bin/env python
# -*- coding: utf-8 -*-


class TextGenerator:

    def __init__(self, template):
        self.template = template

    def set_template(self, template):
        self.template = template

    def generate(self):
        return ["I want to eat %kw%",
                "I want to test %kw%",
                "I want to listen to %kw%",
                "I want to like %kw%",
                "I want to wear %kw%",
                "I want to buy %kw%",
                "I want to sell %kw%",
                ]