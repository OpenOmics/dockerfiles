#!/bin/bash
for i in /work/centrifuger/*; do
    bn=$(basename $i)
    if [[ ( -f $i) && ( ${bn:0:11} == centrifuger ) ]]; then
        real_path=$(readlink -f $i)
        ln -s ${real_path} /usr/bin/${bn}
    fi
done