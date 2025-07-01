#!/usr/bin/env python3

# This utility checks a concretized Spack environment (spack.lock) against the
# authoritative list of NCO-approved software (ASCII file with Spack package
# name on each line).
#
# If any unapproved packages are found, spack.lock is relocated to avoid
# accidental installation.

# Run '. setup.sh' to point to authoritative spack-stack dir containing the NCO
# approved list.

from datetime import datetime
import json
import os
import shutil
import sys

spack_env = os.getenv("SPACK_ENV")
basedir = spack_env if spack_env else "./"

spack_stack_dir = os.getenv("SPACK_STACK_DIR")
approved_list_path = os.path.join(spack_stack_dir, "configs/templates/nco/approved_list.txt")
with open(approved_list_path, "r") as f:
    approved_list = [l.strip() for l in f.readlines()]

spack_lock_path = os.path.realpath(os.path.join(basedir, "spack.lock"))
with open(spack_lock_path, "r") as f:
    spack_lock_json = f.read()

spack_lock = json.loads(spack_lock_json)

success = True

for _hash in spack_lock["concrete_specs"].keys():
    pkg_name = spack_lock["concrete_specs"][_hash]["name"]
    if pkg_name not in approved_list:
        print(f"Package '{pkg_name}' not approved!")
        success = False

if success:
    print(f"Environment validated - no unauthorized packages found in {spack_lock_path}")
else:
    datestr = datetime.now().strftime("%Y%m%d-%H%M%S")
    dest = spack_lock_path + ".disable_" + datestr
    shutil.move(spack_lock_path, dest)
    print("Unauthorized packages detected!")
    print(f"Relocating {spack_lock_path} to {dest}")
    sys.exit(1)
