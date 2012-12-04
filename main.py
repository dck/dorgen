#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
from dorgen import dorgen
from dorgen.exceptions import Error
from dorgen.config import Config

config_file = "dorgen.cfg"  # as argument?

def usage():
    s = """
    Usage: {scriptname} <deploy>

    This script provides generation of texts by keywords
        deploy - folder where the script should generate a site
    """ .format(scriptname = sys.argv[0])
    print s

if "--help" in sys.argv or len(sys.argv) < 2:
    usage()
    exit(1)

try:
    key_values = Config().load(config_file)
    dorgen = dorgen.Dorgen(**key_values)
    dorgen.run(sys.argv[1])
    print "[OK] Script executed successfully"
except Error as e:
    print "[FAIL] Error while executing the script"
    print e