#!/usr/bin/env bash
# Do not run this script directly. Run it through run_tests.sh.

set -e

spack stack create env \
  --name testB-env --template empty --site wcoss2 --compiler oneapi@2024.2.1 \
  --upstream /lfs/h1/emc/nceplibs/noscrub/dev-spack-stack-test/spack-stack-1.9.2rc3/envs/nco-oneapi-2024.2.1/install \
  --dir .

spack env activate testB-env
spack config add 'config:deprecated:true'
spack add ed
utils/make_only_nco_approved_packages_buildable.sh

# Should fail on concretization:
spack concretize -f --fresh |& tee testB-env/log.concretize
utils/validate_concretized_environment.py
spack install
utils/detect_unauthorized_packages.py $PWD utils/alertees.txt
