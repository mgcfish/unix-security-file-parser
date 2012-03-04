#!/usr/bin/env python
from upc.parser.sshd_config import sshd_config
from upc.parser.sudoers import sudoers
from upc.parser.passwd import passwd
from upc.parser.group import group
from upc.parser.ifconfig import ifconfig
from upc.parser.shadow import shadow
from upc.parser.permissions import permissions
from upc.parser.unix_privesc_check import unix_privesc_check
from upc.knowledge_base import knowledge_base 
from wpc.report.report import report
from upc.parseOptions import parseOptions
import upc.utils
import re

# [ wpc notes ]
# We take the reporting engine from windows-privesc-check with minor mods:
# replace wpc/conf.py with our own issues
# remove wpc/*Acl*

# [ Dependencies ]
# apt-get install python-lxml

# unpack tar ball

# need to parse files in a particular order to ensure
# knowlegebase (kb) is populated with info required by
# each parser
#tarball = 1

#for file in upc.parser.order_files(tarball):
#    info, issues = upc.parser.auto_parse(file)

# Parse command line arguments
options = parseOptions()

report = report()
issues = report.get_issues()
kb = knowledge_base()

if options.passwd_file:
    s = passwd()
    s.parse(options.passwd_file, issues, kb)
    
if options.group_file:
    s = group()
    s.parse(options.group_file, issues, kb)
    
if options.shadow_file:
    s = shadow()
    s.parse(options.shadow_file, issues, kb)
    
if options.ifconfig_file:
    s = ifconfig()
    s.parse(options.ifconfig_file, issues, kb)
    
if options.sudoers_file:
    s = sudoers()
    s.parse(options.sudoers_file, issues, kb)
    
if options.perms_file:
    s = permissions()
    s.parse(options.perms_file, issues, kb)
    
if options.sshd_config_file:
    s = sshd_config()
    s.parse(options.sshd_config_file, issues, kb)
    
if options.upc_file:
    s = unix_privesc_check()
    s.parse(options.upc_file, issues, kb)
    
if options.directory:
    for f in upc.utils.dirwalk(options.directory):
        m = re.search("/group$", f)
        if m:
            print "[+] Parsing %s as group file" % f
            s = group()
            s.parse(f, issues, kb)
    
    for f in upc.utils.dirwalk(options.directory):
        print "[D] Processing %s" % f
        
        m = re.search("/passwd$", f)
        if m:
            m2 = re.search("security/passwd$", f)
            if not m2:
                print "[+] Parsing %s as passwd file" % f
                s = passwd()
                s.parse(f, issues, kb)
    
    for f in upc.utils.dirwalk(options.directory):
        m = re.search("[^g]shadow$", f)
        if m:
            print "[+] Parsing %s as shadow file" % f
            s = shadow()
            s.parse(f, issues, kb)
    
    for f in upc.utils.dirwalk(options.directory):
        m = re.search("ifconfig", f)
        if m:
            print "[+] Parsing %s as ifconfig file" % f
            s = ifconfig()
            s.parse(f, issues, kb)
    
        m = re.search("/upc(?:-[^/]+)$", f)
        if m:
            print "[+] Parsing %s as upc file" % f
            s = unix_privesc_check()
            s.parse(f, issues, kb)
    
        m = re.search("sshd_config$", f)
        if m:
            print "[+] Parsing %s as sshd_config file" % f
            s = sshd_config()
            s.parse(f, issues, kb)
    
        m = re.search("sudoers$", f)
        if m:
            print "[+] Parsing %s as sudoers file" % f
            s = sudoers()
            s.parse(f, issues, kb)
    
        m = re.search("(perms.txt|all-files.txt)$", f)
        if m:
            print "[+] Parsing %s as permissions file" % f
            s = permissions()
            s.parse(f, issues, kb)
    
filename = "%s.html" % options.report_file_stem
print "[+] Saving report file %s" % filename
f = open(filename, 'w')
f.write(report.as_html())
f.close()

filename = "%s.txt" % options.report_file_stem
print "[+] Saving report file %s" % filename
f = open(filename, 'w')
f.write(report.as_text())
f.close()
