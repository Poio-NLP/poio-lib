import re
import collections

import pressagio.tokenizer

from .corpus import CorpusReader


def preprocess(text: str) -> str:
    """
    Pre-process a document for later ngramming.

    Parameters
    ----------
    text : str
        The string to pre-process

    Returns
    -------
    str
        The pre-processed string.
    """
    re_wordbeg = re.compile(r"(?<=\s)[-']")
    re_wordbeg2 = re.compile(r"(?<=\s\")[-']")
    re_wordend = re.compile(r"[-'](?=\s)")
    re_wordend2 = re.compile(r"[-'](?=\"\s)")
    text = re_wordbeg.sub("", text)
    text = re_wordbeg2.sub("", text)
    text = re_wordend.sub("", text)
    text = re_wordend2.sub("", text)
    return text


def corpus_ngrams(
    corpus_path: str, ngram_size: int, lowercase: bool = False, cutoff: int = 0
) -> pressagio.tokenizer.NgramMap:
    """
    Tokenize a file and return an ngram store.

    Parameters
    ----------
    corpus_path : str
       The path to the Poio corpus 
    ngram_size : int
        The size of the ngrams to generate.
    lowercase : bool
        Whether or not to lowercase all tokens.
    cutoff : int
        Perform a cutoff after parsing. We will only return ngrams that have a
        frequency higher than the cutoff.

    Returns
    -------
    NgramMap
        The ngram map that allows you to iterate over the ngrams.
    """
    corpus_reader = CorpusReader(corpus_path)
    ngram_map = pressagio.tokenizer.NgramMap()
    for document in corpus_reader.documents():
        document = preprocess(document)
        ngram_list = []
        tokenizer = pressagio.tokenizer.ForwardTokenizer(document)
        tokenizer.lowercase = lowercase
        if ngram_size > 1:
            for token in tokenizer:
                token_idx = ngram_map.add_token(token)
                ngram_list.append(token_idx)
                if len(ngram_list) == ngram_size - 1:
                    break
        if len(ngram_list) < ngram_size - 1:
            continue

        for token in tokenizer:
            token_idx = ngram_map.add_token(token)
            ngram_list.append(token_idx)
            ngram_map.add(ngram_list)
            ngram_list.pop(0)

    if cutoff > 0:
        ngram_map.cutoff(cutoff)

    return ngram_map
