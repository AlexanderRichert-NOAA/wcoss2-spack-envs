#!/usr/bin/env python3

# Check for .spack dir's in installation space and confirm against
# authoritative NCO approved software list. Renames installation directories
# for non-approved packages to prevent accidental build caching/transfer to
# WCOSS2.

# This utility can be run after every "spack install", as well as on a cron
# (especially for monitoring automated builds).

import glob
import json
import os
import sys

assert len(sys.argv)==3, "Provide installation root (/path/to/emc-dev/) and alert recipients file as arguments"
installation_root = os.path.realpath(sys.argv[1])

spack_stack_dir = os.getenv("SPACK_STACK_DIR")
approved_list_path = os.path.join(spack_stack_dir, "configs/templates/nco/approved_list.txt")
with open(approved_list_path, "r") as approved_file:
    approved_list = [l.strip() for l in approved_file.readlines()]

dotspack_dirs = [d for d in glob.glob(installation_root + "/**/.*", recursive=True) if os.path.basename(d)==".spack" and os.path.isdir(d)]

success = True
email_body = f"ALERT: One or more non-NCO authorized packages were found under {installation_root} on Acorn, using the {approved_list_path} approved package list:\n"

for dotspack_dir in dotspack_dirs:
    with open(os.path.join(dotspack_dir, "spec.json"), "r") as spec_file:
        spec = json.loads(spec_file.read())
    pkg_name = spec["spec"]["nodes"][0]["name"]
    if pkg_name not in approved_list:
        success = False
        pkg_dir = os.path.dirname(dotspack_dir)
        alert = (f"Package '{pkg_name}' installed at {pkg_dir} on Acorn not approved by NCO!")
        print("ALERT:", alert)
        renamed_pkg_dir = pkg_dir + ".disabled"
        print(f"    Renaming {pkg_dir} to\n        {renamed_pkg_dir} to prevent build caching.")
        email_body += alert + "\n"

if not success:
    import smtplib
    from email.mime.text import MIMEText
    s = smtplib.SMTP('localhost')
    msg = MIMEText(email_body)
    sender = "alexander.richert@noaa.gov"
    with open(sys.argv[2], "r") as recipients_file:
        recipients = [l.strip() for l in recipients_file.readlines()]
    msg['Subject'] = "Acorn/WCOSS2 installation validation alert"
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)
    s.sendmail(sender, recipients, msg.as_string())
