#!/usr/bin/bash
#g++ AppendExpected.cpp -O3
#./a.out 1
#./a.out 2
python3 preProcData.py ./csv/train_append_dbz.csv ./csv/trainMerged.csv 'train' '2,3,5,6,7,9,10,15,17,18'
python3 preProcData.py ./csv/test_append_dbz.csv ./csv/testMerged.csv 'test' '2,3,5,6,7,9,10,15,17,18'
python3 plot_xgboost.py xgb
