export FAST_ALIGN_BASE=/cs/usr/bareluz/gabi_labs/nematus_clean/nematus/fast_align
echo "./../scripts/evaluate_language.sh ../data/aggregates/en_${1}_anti_${2}.en.txt $1 nematus"
./../scripts/evaluate_language.sh ../data/aggregates/en_${1}_anti_${2}.en.txt $1 nematus $2

