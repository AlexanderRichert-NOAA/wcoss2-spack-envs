#!/usr/bin/env bash

echo "$0: Setting all packages to buildable:false by default"
spack config add 'packages:all:buildable:false'
APPROVED_LIST_PATH=${APPROVED_LIST_PATH:-${SPACK_STACK_DIR:?}/configs/templates/nco/approved_list.txt}
echo "$0: Setting only NCO-approved packages to buildable:true, using $APPROVED_LIST_PATH"
cat $APPROVED_LIST_PATH | xargs --max-procs 1 -I{} spack config add 'packages:{}:buildable:true'
