from sacrebleu.metrics import BLEU
import pickle
import sys
sys.path.append("../../") # Adds higher directory to python modules path.
from nematus.consts import get_evaluate_translation_files
import argparse
def evaluate_translation():
    # refs = []
    with open(TRANSLATED_DEBIASED, 'r') as d, open(TRANSLATED_NON_DEBIASED, 'r') as nd, open(
            BLEU_GOLD_DATA, 'r') as g:
        sys_debiased = d.readlines()
        sys_non_debiased = nd.readlines()
        refs = g.readlines()
        # refs.append(pickle.load(nd))
    bleu = BLEU()
    print("debiased")
    print(bleu.corpus_score(sys_debiased, [refs]))
    print("non debiased")
    print(bleu.corpus_score(sys_non_debiased, [refs]))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
            '-c', '--config_str', type=str, required=True,
            help="a config dictionary str that conatains: \n"
                 "debiased= run translate on the debiased dictionary or not\n"
                 "language= the language to translate to from english. RUSSIAN = 0, GERMAN = 1, HEBREW = 2\n"
                 "collect_embedding_table= run translate to collect embedding table or not\n"
                 "print_line_nums= whether to print line numbers to output file in translate")
    args = parser.parse_args()
    BLEU_SOURCE_DATA, BLEU_GOLD_DATA, TRANSLATED_DEBIASED, TRANSLATED_NON_DEBIASED = get_evaluate_translation_files(args.config_str)

    evaluate_translation()