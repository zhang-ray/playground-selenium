#!/usr/bin/fish
while true
    pkill chrom
    pkill python3
    python3 Entry-2020-12-16.py &
    sleep 1800
end




