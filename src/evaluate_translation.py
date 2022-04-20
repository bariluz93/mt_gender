from sacrebleu.metrics import BLEU
import pickle
import sys
sys.path.append("../../") # Adds higher directory to python modules path.
from nematus.consts import get_evaluate_translation_files
import argparse
def evaluate_translation():
    # refs = []
    with open(TRANSLATED_DEBIASED_PICKLE, 'rb') as d, open(TRANSLATED_NON_DEBIASED_PICKLE, 'rb') as nd, open(
            BLEU_GOLD_DATA_FILTERED, 'r') as g:
        sys_debiased = pickle.load(d)
        sys_non_debiased = pickle.load(nd)
        refs = g.readlines()
        # refs.append(pickle.load(nd))
    bleu = BLEU()
    print("debiased")
    print(bleu.corpus_score(sys_debiased, [refs]))
    print("non debiased")
    print(bleu.corpus_score(sys_non_debiased, [refs]))

    # print("debised")
    # print(bleu.corpus_score(['eine gute Idee , vorausgesetzt , dass es wird , wird diesmal realistisch . \n'],
    #                         [['eine gute Idee , unter der Voraussetzung , dass sie diesmal in die Tat umgesetzt wird .\n']]))
    # print("non debised")
    # print(bleu.corpus_score(['eine gute Idee , vorausgesetzt , sie wird sich diesmal als realistisch erweisen . \n'],
    #                         [['eine gute Idee , unter der Voraussetzung , dass sie diesmal in die Tat umgesetzt wird .\n']]))

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
    _, _, _, _, TRANSLATED_DEBIASED_PICKLE, TRANSLATED_NON_DEBIASED_PICKLE, \
    BLEU_GOLD_DATA_FILTERED = get_evaluate_translation_files(args.config_str)

    evaluate_translation()