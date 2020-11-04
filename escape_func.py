#!/usr/bin/env python3
# PYTHON_PREAMBLE_START_STANDARD:{{{

# Christopher David Cotton (c)
# http://www.cdcotton.com

# modules needed for preamble
import importlib
import os
from pathlib import Path
import sys

# Get full real filename
__fullrealfile__ = os.path.abspath(__file__)

# Function to get git directory containing this file
def getprojectdir(filename):
    curlevel = filename
    while curlevel is not '/':
        curlevel = os.path.dirname(curlevel)
        if os.path.exists(curlevel + '/.git/'):
            return(curlevel + '/')
    return(None)

# Directory of project
__projectdir__ = Path(getprojectdir(__fullrealfile__))

# Function to call functions from files by their absolute path.
# Imports modules if they've not already been imported
# First argument is filename, second is function name, third is dictionary containing loaded modules.
modulesdict = {}
def importattr(modulefilename, func, modulesdict = modulesdict):
    # get modulefilename as string to prevent problems in <= python3.5 with pathlib -> os
    modulefilename = str(modulefilename)
    # if function in this file
    if modulefilename == __fullrealfile__:
        return(eval(func))
    else:
        # add file to moduledict if not there already
        if modulefilename not in modulesdict:
            # check filename exists
            if not os.path.isfile(modulefilename):
                raise Exception('Module not exists: ' + modulefilename + '. Function: ' + func + '. Filename called from: ' + __fullrealfile__ + '.')
            # add directory to path
            sys.path.append(os.path.dirname(modulefilename))
            # actually add module to moduledict
            modulesdict[modulefilename] = importlib.import_module(''.join(os.path.basename(modulefilename).split('.')[: -1]))

        # get the actual function from the file and return it
        return(getattr(modulesdict[modulefilename], func))

# PYTHON_PREAMBLE_END:}}}

def escape(inputfolder, outputfolder):
    import os
    import re
    import shutil

    if inputfolder[-1] !='/':
        inputfolder = inputfolder + '/'
    if outputfolder[-1] !='/':
        outputfolder = outputfolder + '/'

    if os.path.isdir(outputfolder):
        shutil.rmtree(outputfolder)
    os.mkdir(outputfolder)

    filenames = os.listdir(inputfolder)

    renotescapedtext = re.compile('BEGINNOESCAPEHERE(.*?)ENDNOESCAPEHERE', re.DOTALL)

    for filename in filenames:
        with open(inputfolder + filename, 'r') as f:
            text = f.read()

        notescaped = []
        while True:
            match = renotescapedtext.search(text)
            if match:
                text = text.replace(match.group(0), 'BEGINNOESCAPEWASHEREENDNOESCAPEWASHERE', 1)
                notescaped.append(match.group(1))
            else:
                break

        # need to do \ first otherwise replace escape twice
        text = text.replace('\\', '\\\\')
        text = text.replace('`', '\\`')
        text = text.replace('{', '\\{')
        text = text.replace('$', '\\$')

        for i in range(len(notescaped)):
            text = text.replace('BEGINNOESCAPEWASHEREENDNOESCAPEWASHERE', notescaped[i], 1)

        with open(outputfolder + filename, 'w+') as f:
            f.write(text)


