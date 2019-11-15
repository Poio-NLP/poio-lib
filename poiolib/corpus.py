import os
import glob
import typing

import syntok.segmenter as segmenter
from pressagio.tokenizer import ForwardTokenizer


StringGenerator = typing.Generator[str, None, None]


def corpus_documents(files: typing.List[str]):
    """
    Get the documents of the corpus.

    Returns
    -------
    Generator of str
        The document, one after the other.
    """
    for fn in files:
        with open(fn, "r", encoding="utf-8") as f:
            for line in f:
                yield line


def tokenize(text: str, lowercase=False) -> StringGenerator:
    """
    Get the tokens of a document text.

    Parameters
    ----------
    text : str
        The text to tokenize.
    lowercase : bool (Optional, default: `false`)
        Whether or not to lowercase all tokens.

    Returns
    -------
    Generator of str
        The tokens of the text.
    """
    tokenizer = ForwardTokenizer(text)
    tokenizer.lowercase = lowercase
    for token in tokenizer:
        yield token


def tokenize_normalized_casing(
    text: str, capitals_map: typing.Dict[str, str]
) -> StringGenerator:
    """
    Get tokens of a text and map sentence start tokens.

    We use this to normalize sentence starts, e.g. to map uppercase tokens at
    sentence starts to their lowercase version.

    Parameters
    ----------
    text : str
        The text to tokenize.
    capitals_map : Dict[str, str]
        This is a dict to map tokens at sentence starts to their lowercase.
        Check `capitalize.py` how to create such a map.

    Returns
    -------
    Generator of str
        The tokens of the text.
 
    """
    for sentence in sentences(text):
        for i, token in enumerate(tokenize(sentence)):
            if i == 0:
                token = capitals_map.get(token, token)
            yield token


def sentences(text: str) -> StringGenerator:
    """
    Get the sentences of a document.

    Parameters
    ----------
    text : str
        The text to tokenize.
 
    Returns
    -------
    Generator of str
        The sentences, one after the other.
    """
    for paragraph in segmenter.analyze(text):
        for sentence in paragraph:
            orig_sentence = ""
            for t in sentence:
                orig_sentence += t.spacing + t.value
            yield orig_sentence


def tokenized_sentences(
    text: str, lowercase=False
) -> typing.Generator[StringGenerator, None, None]:
    """
    Get the sentences of a document, with their tokens.

    Parameters
    ----------
    text : str
        The text to tokenize.
    lowercase : bool (Optional, default: `false`)
        Whether or not to lowercase all tokens.

    Returns
    -------
    Generator of Generator of str
        The sentences, each is a generator of its tokens.
    """
    for sentence in sentences(text):
        yield tokenize(sentence)
