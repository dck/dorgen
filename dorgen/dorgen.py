#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from exceptions import *
import os
class Dorgen:

    def __init__(self, text, kw, template, deploy = "."):
        try:
            with open(text, "r") as f:
                self.text = f.read()
        except Exception as e:
            raise FileError(text)

        try:
            with open(template, "r") as f:
                self.template = f.read()
        except Exception as e:
            raise FileError(template)

        f = os.path.abspath(deploy)
        print f
        if not os.path.exists(f):
            os.makedirs(f)
        if not os.access(f, os.W_OK):
            raise FolderAccessError(f)
        if not os.access(kw, os.R_OK):
            raise FileError(kw)
        self.kw = kw

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