#!/bin/bash

echo "direct pass to child process; inline indicates to export"
XXX=123123 bash -c 'echo sub_xxx=$XXX; export -p | grep "^declare -x XXX="'
echo

echo "assign does not mean export"
XXX=123123
export -p | grep "^declare -x XXX="
unset XXX
echo



echo "fail to pass to child process without export"
XXX=123123; bash -c 'echo sub_xxx=$XXX'
echo

echo "successfully export to child-child process without export;  Export is treated as the most default/reasonable behavior"
XXX=123123 bash -c 'echo sub_xxx=$XXX; export -p | grep "^declare -x XXX=" ; bash -c "echo in sub sub; echo sub_sub_xxx=\$XXX; export -p | grep \"^declare -x XXX=\""'
echo

echo "Unset will stop the propogation of the export"
XXX=123123 bash -c 'echo sub_xxx=$XXX; unset XXX ; bash -c "echo in sub sub; echo sub_sub_xxx=\$XXX; export -p | grep \"^declare -x XXX=\""'
echo


# summary
# - Export trigger:
#   - one process scope: XXX= assign
#   - script scope:  export command
# - Export Stop:
#   - Only unset (otherwise it is the default value)
