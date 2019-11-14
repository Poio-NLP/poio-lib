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
