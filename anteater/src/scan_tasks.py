#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import
import os
import sh
import yaml

__author__ = "Luke Hinds"
__copyright__ = "Luke Hinds"
__license__ = "none"


with open('configs/anteater.yml', 'r') as ymlcfg:
    cfg = yaml.safe_load(ymlcfg)
    projects = (cfg['projects'])


def audit_all():
    for project in projects:
        audit_project(project)


def audit_project(project):
    '''
    Passed project name and declares repo directory 'projdir'.
    Performs recursive search to find file extensions.
    When extension matches, it breaks loop with True and runs related scanner
    '''
    py = False
    shell = False
    java = False
    c = False
    projdir = 'repos/{0}'.format(project)
    for dirname, dirnames, filenames in os.walk(projdir):
        for filename in filenames:
            if filename.endswith('.py'):
                py = True
                break
            elif filename.endswith('.sh'):
                shell = True
                break
            elif filename.endswith('.java'):
                java = True
                break
            elif filename.endswith('.c'):
                c = True
                break
    if py:
        run_bandit(project, projdir)
    elif shell:
        pass
    elif java:
        pass
    elif c:
        pass


def run_bandit(project, projdir):
    report = ('{0}_report.html'.format(project))
    print ('Performing Bandit Scan on: {0}'.format(projdir))
    try:
        sh.bandit('-r', '-f', 'html', '-o', report, projdir)
    except sh.ErrorReturnCode, e:
        print(e.stderr)
