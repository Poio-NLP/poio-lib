import os
import glob
import typing

import syntok.segmenter as segmenter
from pressagio.tokenizer import ForwardTokenizer


StringGenerator = typing.Generator[str, None, None]
TextprocessorCallable = typing.Callable[[str], str]


class CorpusReader:
    """
    A Poio corpus consists of one or more text files. Each text files contains
    documents, one document per line.
    """

    def __init__(
        self,
        files: typing.List[str],
        document_preprocessor: TextprocessorCallable = None,
    ):
        """
        Intialize the corpus reader.
        
        Parameters
        ----------
        files : list of str
            The paths to the corpus files.
        """
        self.files = files
        self.document_preprocessor = document_preprocessor

    def documents(self) -> StringGenerator:
        """
        Get the documents of the corpus.

        Returns
        -------
        Generator of str
            The document, one after the other.
        """
        for fn in self.files:
            with open(fn, "r", encoding="utf-8") as f:
                for line in f:
                    if self.document_preprocessor:
                        line = self.document_preprocessor(line)
                    yield line

    def tokenized_documents(
        self, lowercase=False
    ) -> typing.Generator[StringGenerator, None, None]:
        """
        Get the tokenized documents of the corpus.

        Parameters
        ----------
        lowercase : bool (Optional, default: `false`)
            Whether or not to lowercase all tokens.

        Returns
        -------
        Generator of Generator of str
            The documents and their tokens.
        """
        for document in self.documents():
            tokenizer = ForwardTokenizer(document)
            tokenizer.lowercase = lowercase
            yield (token for token in tokenizer)

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

    def tokenized_sentences(
        self, lowercase=False
    ) -> typing.Generator[StringGenerator, None, None]:
        """
        Get the sentences of the corpus, with their tokens.

        Parameters
        ----------
        lowercase : bool (Optional, default: `false`)
            Whether or not to lowercase all tokens.

        Returns
        -------
        Generator of Generator of str
            The sentences, each is a generator of its tokens.
        """
        for sentence in self.sentences():
            tokenizer = ForwardTokenizer(sentence)
            tokenizer.lowercase = lowercase
            yield (token for token in tokenizer)
