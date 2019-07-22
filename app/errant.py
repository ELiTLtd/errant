import os
import spacy
from contextlib import ExitStack
from nltk.stem.lancaster import LancasterStemmer
import scripts.align_text as align_text
import scripts.cat_rules as cat_rules
import scripts.toolbox as toolbox
from io import StringIO

# Load Tokenizer and other resources
nlp = spacy.load("en")

# Lancaster Stemmer
stemmer = LancasterStemmer()
# GB English word list (inc -ise and -ize)
gb_spell = toolbox.loadDictionary("resources/en_GB-large.txt")
# Part of speech map file
tag_map = toolbox.loadTagMap("resources/en-ptb_map")

class Defaults:
    lev = True
    merge = "rules"

def annotate(original, corrected):
    args = Defaults()
    out = StringIO()
    orig = original.splitlines()
    cor = corrected.splitlines()
    for orig_sent, cor_sent in zip(orig, cor):
        orig_sent = orig_sent.strip()
        cor_sent = cor_sent.strip()
        out.write("S "+orig_sent + "\n")
        proc_orig = toolbox.applySpacy(orig_sent.split(), nlp)
        cor_id = 0
        # Identical sentences have no edits, so just write noop.
        if orig_sent == cor_sent:
            out.write("A -1 -1|||noop|||-NONE-|||REQUIRED|||-NONE-|||"+str(cor_id)+"\n")
        # Otherwise, do extra processing.
        else:
            # Markup the corrected sentence with spacy (assume tokenized)
            proc_cor = toolbox.applySpacy(cor_sent.strip().split(), nlp)
            # Auto align the parallel sentences and extract the edits.
            auto_edits = align_text.getAutoAlignedEdits(proc_orig, proc_cor, nlp, args)
            # Loop through the edits.
            for auto_edit in auto_edits:
                # Give each edit an automatic error type.
                cat = cat_rules.autoTypeEdit(auto_edit, proc_orig, proc_cor, gb_spell, tag_map, nlp, stemmer)
                auto_edit[2] = cat
                # Write the edit to the output m2 file.
                out.write(toolbox.formatEdit(auto_edit, cor_id)+"\n")
                # Write a newline when we have processed all corrections for a given sentence.
        out.write("\n")
    return out.getvalue()
