#!/bin/bash

while [ 1 ]
do
    read -t 0.05 answer
    sftp robot@10.42.0.3 << !
    put red_ball_info.txt
!
    if [ "$answer" == "Q" ]; then
        exit
    fi
done
