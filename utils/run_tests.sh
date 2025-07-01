#!/usr/bin/env bash
# Run in emc-dev (or whatever root-level installation dir)

mkdir -p test_logs

pushd /lfs/h1/emc/nceplibs/noscrub/dev-spack-stack-test/spack-stack-1.9.2rc3
. setup.sh
popd

# Test A - should build successfully (after tweaking approved_list.txt for testing purposes, 30 Jun 2025)
utils/tests/testA.sh |& tee test_logs/testA.out

# Test B - should fail because 'ed' package is not buildable
utils/tests/testB.sh |& tee test_logs/testB.out

# Test C - should fail because 'ed' package is concretized but not authorized
utils/tests/testC.sh |& tee test_logs/testC.out

# Test D - should fail because 'ed' package is installed but not authorized
utils/tests/testD.sh |& tee test_logs/testD.out
