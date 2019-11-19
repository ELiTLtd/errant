import argparse
import os
import spacy
from contextlib import ExitStack
from nltk.stem.lancaster import LancasterStemmer
from io import StringIO

from errant import AlignText
from errant import CatRules
from errant import Toolbox

class TextToM2:

    @staticmethod
    def convert(original_text, corrected_text, merge_strategy='rules', levenshtein=False):
        """
        :param original_text: The path to the original tokenized text file
        :param corrected_text: list - The paths to >= 1 corrected tokenized text files
        :param merge_strategy: Choose a merging strategy for automatic alignment, possible values:
                                rules: Use a rule-based merging strategy (default)
                                all-split: Merge nothing; e.g. MSSDI -> M, S, S, D, I
                                all-merge: Merge adjacent non-matches; e.g. MSSDI -> M, SSDI
                                all-equal: Merge adjacent same-type non-matches; e.g. MSSDI -> M, SS, D, I
        :param levenshtein: Use standard Levenshtein to align sentences
        :return:
        """
        # Get base working directory.
        basename = os.path.dirname(os.path.realpath(__file__))
        print("Loading resources...")
        # Load Tokenizer and other resources
        nlp = spacy.load("en")
        # Lancaster Stemmer
        stemmer = LancasterStemmer()
        # GB English word list (inc -ise and -ize)
        gb_spell = Toolbox.load_dictionary(basename + "/resources/en_GB-large.txt")
        # Part of speech map file
        tag_map = Toolbox.load_tag_map(basename + "/resources/en-ptb_map")
        # Setup output m2 file
        out_m2 = StringIO.StringIO()

        orig_sent = original_text
        cor_sents = [corrected_text]

        # Write the original sentence to the output m2 file.
        out_m2.write("S " + orig_sent + "\n")
        # Markup the original sentence with spacy (assume tokenized)
        proc_orig = Toolbox.apply_spacy(orig_sent.split(), nlp)
        # Loop through the corrected sentences
        for cor_id, cor_sent in enumerate(cor_sents):
            cor_sent = cor_sent.strip()
            # Identical sentences have no edits, so just write noop.
            if orig_sent == cor_sent:
                out_m2.write("A -1 -1|||noop|||-NONE-|||REQUIRED|||-NONE-|||" + str(cor_id) + "\n")
            # Otherwise, do extra processing.
            else:
                # Markup the corrected sentence with spacy (assume tokenized)
                proc_cor = Toolbox.apply_spacy(cor_sent.strip().split(), nlp)
                # Auto align the parallel sentences and extract the edits.
                auto_edits = AlignText.get_auto_aligned_edits(proc_orig, proc_cor, merge_strategy, levenshtein)
                # Loop through the edits.
                for auto_edit in auto_edits:
                    # Give each edit an automatic error type.
                    cat = CatRules.auto_type_edit(auto_edit, proc_orig, proc_cor, gb_spell, tag_map, nlp,
                                                  stemmer)
                    auto_edit[2] = cat
                    # Write the edit to the output m2 file.
                    out_m2.write(Toolbox.format_edit(auto_edit, cor_id) + "\n")
                # Write a newline when we have processed all corrections for a given sentence.
                out_m2.write("\n")

        return out_m2.getValue()
