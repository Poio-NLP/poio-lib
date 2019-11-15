import re
import collections
import typing

import pressagio.tokenizer
import pressagio.dbconnector

import poiolib.corpus


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
    files: typing.List[str],
    ngram_size: int,
    capitals_map: typing.Dict[str, str] = {},
    cutoff: int = 0,
) -> pressagio.tokenizer.NgramMap:
    """
    Tokenize a file and return an ngram store.

    Parameters
    ----------
    files : list of str
       A list of paths to files to parse.
    ngram_size : int
        The size of the ngrams to generate.
    capitals_map : Dict[str, str]
        This is a dict to map tokens at sentence starts to their lowercase.
        Check `capitalize.py` how to create such a map.
    cutoff : int
        Perform a cutoff after parsing. We will only return ngrams that have a
        frequency higher than the cutoff.

    Returns
    -------
    poiolib.tokenizer.NgramMap
        The ngram map that allows you to iterate over the ngrams.
    """
    ngram_map = pressagio.tokenizer.NgramMap()
    for document in poiolib.corpus.corpus_documents(files):
        document = preprocess(document)
        ngram_list = []
        tokenized_document = poiolib.corpus.tokenize_normalized_casing(
            document, capitals_map
        )
        if ngram_size > 1:
            for token in tokenized_document:
                token_idx = ngram_map.add_token(token)
                ngram_list.append(token_idx)
                if len(ngram_list) == ngram_size - 1:
                    break
        if len(ngram_list) < ngram_size - 1:
            continue

        for token in tokenized_document:
            token_idx = ngram_map.add_token(token)
            ngram_list.append(token_idx)
            ngram_map.add(ngram_list)
            ngram_list.pop(0)

    if cutoff > 0:
        ngram_map.cutoff(cutoff)

    return ngram_map


def ngrams_to_postgres(
    ngram_map: pressagio.tokenizer.NgramMap, ngram_size: int, iso_639_3: str
):
    """Insert ngrams into postgres database.

    This is a simple convenience wrapper around the pressagio function.

    Parameters
    ----------
    ngrams : pressagion.tokenizer.NgramMap
        The ngrams to insert into the database.
    ngram_size : int
        The size of the ngrams.
    iso_639_3 : str
        The ISO code of the language of the ngrams.
    """
    pressagio.dbconnector.insert_ngram_map_postgres(
        ngram_map,
        ngram_size,
        iso_639_3,
        append=False,
        create_index=True,
        lowercase=True,
        normalize=True,
    )
