#!/usr/bin/env python

import re
import requests
import os

"""
This will download the freshest datafile contents
and populate a Python file that gets imported within the Lambda script
"""

datafile_url = os.environ.get('DATAFILE_URL')
print("Fetching datafile from {}...".format(datafile_url))

datafile = requests.get(datafile_url).text

try:
    app_source_code_fh = open('datafile.py', 'w')
    code = """#!/usr/bin/env python 

datafile=r\"\"\"{}\"\"\"
datafile_url=\"{}\"
""".format(datafile, datafile_url)
    app_source_code_fh.write(code)
except:
    print("Unable to write to datafile.py file")
finally:
    app_source_code_fh.close()
    