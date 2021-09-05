#!/bin/bash
# Usage:
#   evaluate_language.sh <corpus> <lang-code> <translation system>
#
# e.g.,
# ../scripts/evaluate_language.sh ../data/agg/en.txt es google

set -e
#deibiased = "debiased"
#non_debiased = "non-debiased"
# Parse parameters
dataset=$1
lang=$2
trans_sys=$3
prefix=en-$lang
prefix_debiased=$prefix-debiased
prefix_non_debiased=$prefix-non-debiased

# Prepare files for translation
#cut -f3 $dataset > ./tmp.in            # Extract sentences
mkdir -p ../translations/$trans_sys/
mkdir -p ../data/human/$lang

# Translate
trans_fn_debiased=../translations/$trans_sys/$prefix_debiased.txt
trans_fn_non_debiased=../translations/$trans_sys/$prefix_non_debiased.txt
trans_fn=../translations/$trans_sys/$prefix.txt
echo "!!! debiased file: $trans_fn_debiased non debiased file: $trans_fn_non_debiased"
#if [ ! -f $trans_fn ]; then
#    python translate.py --trans=$trans_sys --in=./tmp.in --src=en --tgt=$2 --out=$trans_fn
#else
#    echo "Not translating since translation file exists: $trans_fn"
#fi

# Align
align_fn_debiased=forward.$prefix_debiased.align
align_fn_non_debiased=forward.$prefix_non_debiased.align
echo "FAST_ALIGN_BASE:${FAST_ALIGN_BASE}"
$FAST_ALIGN_BASE/build/fast_align -i $trans_fn_debiased -d -o -v > $align_fn_debiased
$FAST_ALIGN_BASE/build/fast_align -i $trans_fn_non_debiased -d -o -v > $align_fn_non_debiased

# Evaluate
mkdir -p ../data/human/$trans_sys/$lang/
out_fn_debiased=../data/human/$trans_sys/$lang/${lang}-debiased.pred.csv
out_fn_non_debiased=../data/human/$trans_sys/$lang/${lang}-non_debiased.pred.csv
echo "output path: ${out_fn_debiased}"
python load_alignments.py --ds=$dataset  --bi=$trans_fn_debiased --align=$align_fn_debiased --lang=$lang --out=$out_fn_debiased
echo "********************finished load_alignments for debiased********************"
python load_alignments.py --ds=$dataset  --bi=$trans_fn_non_debiased --align=$align_fn_non_debiased --lang=$lang --out=$out_fn_non_debiased
echo "********************finished load_alignments for non debiased********************"

# Prepare files for human annots
# human_fn=../data/human/$trans_sys/$lang/${lang}.in.csv
# python human_annots.py --ds=$dataset --bi=$trans_fn --out=$human_fn
