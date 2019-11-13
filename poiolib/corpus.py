import os
import glob
import typing

import syntok.segmenter as segmenter
from pressagio.tokenizer import ForwardTokenizer


StringGenerator = typing.Generator[str, None, None]


class CorpusReader:
    """
    A Poio corpus consists of one or more text files. Each text files contains
    documents, one document per line.
    """

    def __init__(self, files: typing.List[str]):
        """
        Intialize the corpus reader.
        
        Parameters
        ----------
        files : list of str
            The paths to the corpus files.
        """
        self.files = files

    def documents(self) -> StringGenerator:
        """
        Returns
        -------
        Generator of str
            The document, one after the other.
        """
        for fn in self.files:
            with open(fn, "r", encoding="utf-8") as f:
                for line in f:
                    yield line

    def sentences(self) -> StringGenerator:
        """
        Get the sentences of the corpus.

        Returns
        -------
        Generator of str
            The sentences, one after the other.
        """
        for document in self.documents():
            for paragraph in segmenter.analyze(document):
                for sentence in paragraph:
                    orig_sentence = ""
                    for t in sentence:
                        orig_sentence += t.spacing + t.value
                    yield orig_sentence

    def tokenized_sentences(self) -> typing.Generator[StringGenerator, None, None]:
        """
        Get the sentences of the corpus, with their tokens.

        Returns
        -------
        Generator of Generator of str
            The sentences, each is a generator of its tokens.
        """
        for sentence in self.sentences():
            tokenizer = ForwardTokenizer(sentence)
            yield (token for token in tokenizer)
