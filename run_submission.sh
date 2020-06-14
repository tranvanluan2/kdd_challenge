#!/bin/bash
rm examples/results/*.txt
for i in {1..10}
do
   python example.py
done