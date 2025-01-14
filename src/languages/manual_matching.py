""" Usage:
    <file-name> --in=IN_FILE --out=OUT_FILE [--debug]
"""
# External imports
import logging
from docopt import docopt
import re
import json

# Local imports
from languages.util import GENDER, get_gender_from_token
from languages.german import GermanPredictor
from languages.semitic_languages import HebrewPredictor
from languages.pymorph_support import PymorphPredictor
from languages.spacy_support import SpacyPredictor
import sys
sys.path.append("../../")
from debias_files.src.consts import DATA_HOME


# =-----

class ManualPredictor:
    """
    Class for Manual matching German and Herbrew
    """

    de_variants_fn = DATA_HOME+"professions_annotations/"+"de_variants.json"
    he_variants_fn = DATA_HOME+"professions_annotations/"+"he_variants.json"
    ru_variants_fn = DATA_HOME+"professions_annotations/"+"ru_variants.json"
    es_variants_fn = DATA_HOME+"professions_annotations/"+"es_variants.json"

    def __init__(self, lang):
        self.lang = lang
        self.automatic_predictor = None
        if self.lang == 'de':
            self.automatic_predictor = GermanPredictor()
            with open(self.de_variants_fn, 'r') as var_json:
                self.variants = json.load(var_json)
        elif self.lang == 'he':
            self.automatic_predictor = HebrewPredictor()
            with open(self.he_variants_fn, 'r') as var_json:
                self.variants = json.load(var_json)
        elif self.lang == 'ru':
            self.automatic_predictor = PymorphPredictor("ru")
            with open(self.ru_variants_fn, 'r') as var_json:
                self.variants = json.load(var_json)
        elif self.lang == 'es':
            self.automatic_predictor = SpacyPredictor("es")
            with open(self.es_variants_fn, 'r') as var_json:
                self.variants = json.load(var_json)
        else:
            raise ValueError(f"Unrecognized language {self.lang}, supported: de and he")

    def get_gender(self, profession: str, translated_sent = None, entity_index = None, ds_entry = None) -> (GENDER, str, int):
        """
        Predict gender of an input profession.
        """
        correct_prof = ds_entry[3].lower()
        if ds_entry[0] == "neutral":
            return GENDER.ignore, None, None

        gender, matched_word, matched_index = self._get_gender(profession, translated_sent, entity_index, ds_entry)

        return gender, matched_word, matched_index

    def _get_gender(self, profession: str, translated_sent = None, entity_index = None, ds_entry = None) -> (GENDER, str, int):
        expected_english_profession = ds_entry[3].lower()
        expected_gender = ds_entry[0]

        # initially try to resolve problem based on exact manual rules
        gender, matched_word, matched_index = self._get_gender_manual_rules(profession, translated_sent, entity_index, ds_entry)

        if gender in [GENDER.male, GENDER.female, GENDER.neutral]:
            return gender, matched_word, matched_index

        return self.automatic_predictor.get_gender(profession, translated_sent, entity_index, ds_entry), None, None

    def _get_gender_manual_rules(self, profession: str, translated_sent = None, entity_index = None, ds_entry = None) -> (GENDER, str, int):
        expected_english_profession = ds_entry[3].lower()
        expected_gender = ds_entry[0]

        translated_sent = translated_sent.lower()

        found_gender = GENDER.unknown

        male = expected_english_profession + "-male"
        female = expected_english_profession + "-female"

        both_possible = False
        matched_word = None
        matched_index = None
        if male in self.variants:
            for index, form in enumerate(self.variants[male]):
                if re.search(form.lower() + "[^a-z\u0590-\u05fe]", translated_sent):
                    found_gender = GENDER.male
                    matched_word = form
                    matched_index = index
                    break

        if female in self.variants:
            for index, form in enumerate(self.variants[female]):
                if re.search(form.lower() + "[^a-z\u0590-\u05fe]", translated_sent):
                    if found_gender is GENDER.male:
                        found_gender = GENDER.unknown
                        both_possible = True
                        if matched_word != form:
                            matched_word = None
                            matched_index = None
                        break
                    matched_word = form
                    matched_index = index
                    found_gender = GENDER.female

        # our morphology analysis cannot analyze whole sentence, therefore if both are possible, mark it as correct
        if both_possible:
            if expected_gender == "male":
                return GENDER.male, matched_word, matched_index
            else:
                return GENDER.female, matched_word, matched_index

        return found_gender, matched_word, matched_index


if __name__ == "__main__":
    # Parse command line arguments
    args = docopt(__doc__)
    inp_fn = args["--in"]
    out_fn = args["--out"]
    debug = args["--debug"]
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    logging.info("DONE")
