#!/bin/sh
if [ $0 = "-bash" -o $0 = "-zsh" -o $0 = "zsh"  ]; then
    DIR=`pwd`
else
    DIR="$( cd "$(dirname $(readlink -f "$0"))" ; pwd -P )"
fi

sh $DIR/getopts_ex.sh -a hahah

sh $DIR/getopts_ex.sh



sh $DIR/getopts_ex.sh -b hahah

sh $DIR/getopts_ex.sh -c good -d  # -d will not be triggered
sh $DIR/getopts_ex.sh -c -d  # -d will be triggered
sh $DIR/getopts_ex.sh -cd  # -d will be triggered


echo "For unsupported arguments"
sh $DIR/getopts_ex.sh -x  #  it raises error due to lack of implements of getopts (lack of supported getopts)

# sh $DIR/getopts_ex.sh -x xixi  #  it raises error due to lack of arguments

sh $DIR/getopts_ex.sh -y yiyi #  it will fails silently if not supported.


sh $DIR/getopts_ex.sh -z #  it will fails silently if not supported.
