#!/bin/bash

runner=./fastText/fasttext 

# prepare data
python ../parse/parse_text_fasttext.py $1 $2 $3
python ./split_fasttext.py $1 $2 $3

# train
for i in {0..2}
do
    train_file=./${i}_train_$1_$2_$3.txt
    model_file=./${i}_fastmodel_$1_$2_$3
    ls $train_file
    $runner supervised -verbose 1 -input $train_file -output $model_file -thread 20
done

# valid
for i in {0..2}
do
    test_file=./${i}_test_$1_$2_$3.txt 
    pred_file=./${i}_pred_$1_$2_$3.txt 
    model_file=./${i}_fastmodel_$1_$2_$3    
    ls $test_file
    $runner predict ${model_file}.bin $test_file > $pred_file
done

python ./exp_text_fasttext.py $1 $2 $3
