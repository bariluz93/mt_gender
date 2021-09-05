from sacrebleu.metrics import BLEU
refs = [ # First set of references
       ['The dog bit the man.', 'It was not unexpected.', 'The man bit him first.'],
       # Second set of references
       ['The dog had bit the man.', 'No one was surprised.', 'The man had bitten the dog.'],
       ]
sys = ['The dog bit the man.', "It wasn't surprising.", 'The man had just bitten him.']
def evaluate_translation():
    bleu = BLEU()
    print(bleu.corpus_score(sys, refs))
if __name__ == '__main__':
    evaluate_translation()