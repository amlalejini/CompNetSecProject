#!/bin/bash
for ip in 10.1.1.{1..254}; do
  ping -c 1 -W 1 $ip | grep "64 bytes" &
done
