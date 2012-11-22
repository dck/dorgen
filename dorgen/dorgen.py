#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from exceptions import *

class Dorgen:

    def __init__(self, text, kw, template, deploy = "."):
        try:
            with open(text, "r") as f:
                self.text = f.read()
        except Exception as e:
            raise FileError(text)

    def run(self):
         pass

    def generate_dict(self):
        pass

    def set_text_file(self, file):
        pass

    def set_keywords_file(self, file):
        pass

    def set_template_file(self, file):
        pass

    def create_enviroment(self, file):
        pass

    def output(self):
        pass