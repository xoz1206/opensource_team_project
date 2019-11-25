#!/bin/bash

while [ 1 ]
do
    read -t 0.1 answer
    sftp robot@10.42.0.3 << !
    put red_ball_info.txt
!
    if [ "$answer" == "q" ]; then
        exit
    fi
done
