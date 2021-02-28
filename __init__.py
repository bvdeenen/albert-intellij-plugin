# -*- coding: utf-8 -*-

"""This is a simple python template extension.

This extension should show the API in a comprehensible way. Use the module docstring to provide a \
description of the extension. The docstring should have three paragraphs: A brief description in \
the first line, an optional elaborate description of the plugin, and finally the synopsis of the \
extension.

Synopsis: <trigger> [delay|throw] <query>"""

from albert import *
import xmltodict
from os import path
import os
from time import sleep


__title__ = "IntelliJ launches"
__version__ = "0.1.0"
__triggers__ = "ij "
__authors__ = "bart van deenen"
#__exec_deps__ = ["whatever"]


entries=[]

def initialize():
    def parse(config_file):
        global entries
        with open(config_file) as _f:
            r = xmltodict.parse(_f.read())
            entries = r["application"]["component"]["option"][0]["map"]["entry"]

    config_file = path.expanduser("~/.config/JetBrains/IntelliJIdea2020.3/options/recentProjects.xml")
    parse(config_file)


# Can be omitted
def finalize():
    pass


def handleQuery(query):
    if not query.isTriggered:
        return

    # Note that when storing a reference to query, e.g. in a closure, you must not use
    # query.isValid. Apart from the query beeing invalid anyway it will crash the appplication.
    # The Python type holds a pointer to the C++ type used for isValid(). The C++ type will be
    # deleted when the query is finished. Therfore getting isValid will result in a SEGFAULT.

    results = []
    search_string = query.string.lower()

    def matcher(a):
        i=0
        for c in search_string:
            i = a.find(c, i)
            if i < 0: return False
        return a

    for e in entries:

        project_dir = e["@key"].replace("$USER_HOME$","~")
        project = os.path.basename(project_dir)
        if not matcher(project.lower()): continue
        item = Item(id=__title__,
                    icon=os.path.dirname(__file__)+"/plugin.svg",
                    text=project,
                    subtext=project_dir,
                    completion=__triggers__ + 'Hellooohooo!',
                    actions=[
                        ProcAction(text="ProcAction",
                                   commandline=["idea.sh", path.expanduser(project_dir)])
                    ])
        results.append(item)
    return results
