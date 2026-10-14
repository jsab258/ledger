#!/bin/bash
# the rooms in the order of the review views: the Hook view's windows, the reverse view's, then the rest (python3 build_windows.py rooms does the same)
cd /home/user/ledger/production/cloud-week/kit/house-windows
OUT=${1:-/home/user/ledger-scratch/house-windows/rooms}
for r in up_lounge_1 up_lounge_2 up_bedroom_1 up_landing_1 up_landing_2 gf_front_1 up_empty_1 up_empty_2 up_lounge_3 up_bedroom_2 up_bedroom_3 gf_front_2 gf_front_3; do
  if [ -f $OUT/$r.json ]; then echo "skip $r"; continue; fi
  nice -n 15 /home/user/.bpyenv/bin/python hw_roomgen.py $r $OUT 24 1.0 2>&1 | grep "^render\|^up_\|^gf_\|Traceback\|Error" 
done
echo ROOMS DONE
