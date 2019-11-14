import re
import collections
import typing

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
    files: typing.List[str], ngram_size: int, lowercase: bool = False, cutoff: int = 0
) -> pressagio.tokenizer.NgramMap:
    """
    Tokenize a file and return an ngram store.

    Parameters
    ----------
    files : list of str
       A list of paths to files to parse.
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
    corpus_reader = CorpusReader(files, document_preprocessor=preprocess)
    ngram_map = pressagio.tokenizer.NgramMap()
    for document in corpus_reader.tokenized_documents(lowercase):
        ngram_list = []
        if ngram_size > 1:
            for token in document:
                token_idx = ngram_map.add_token(token)
                ngram_list.append(token_idx)
                if len(ngram_list) == ngram_size - 1:
                    break
        if len(ngram_list) < ngram_size - 1:
            continue

        for token in document:
            token_idx = ngram_map.add_token(token)
            ngram_list.append(token_idx)
            ngram_map.add(ngram_list)
            ngram_list.pop(0)

    if cutoff > 0:
        ngram_map.cutoff(cutoff)

    return ngram_map
