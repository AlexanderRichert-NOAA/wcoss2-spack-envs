#!/usr/bin/env bash
# Do not run this script directly. Run it through run_tests.sh.

set -e

spack stack create env \
  --name testA-env --template empty --site wcoss2 --compiler oneapi@2024.2.1 \
  --upstream /lfs/h1/emc/nceplibs/noscrub/dev-spack-stack-test/spack-stack-1.9.2rc3/envs/nco-oneapi-2024.2.1/install \
  --dir .

spack env activate testA-env
spack config add 'config:deprecated:true'
spack add hdf5@1.14.5
spack config add 'packages:hdf5:require::"@1.14.5 +hl +fortran +mpi +threadsafe ~szip"'
utils/make_only_nco_approved_packages_buildable.sh

spack concretize -f --fresh |& tee testA-env/log.concretize
utils/validate_concretized_environment.py
spack install
utils/detect_unauthorized_packages.py $PWD utils/alertees.txt
