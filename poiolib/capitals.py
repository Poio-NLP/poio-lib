import collections
import typing

import regex

from .corpus import CorpusReader


def sentence_starts_lower_map(files: typing.List[str]) -> typing.Dict:
    """
    Create a map for tokens at sentence start that are probably lower case.
    """
    corpus_reader = CorpusReader(files)
    first_tokens = set()
    tokens_count = collections.defaultdict(int)
    re_hascapital = regex.compile(r"[[:upper:]][[:^upper:]]")
    for sentence in corpus_reader.tokenized_sentences():
        for i, token in enumerate(sentence):
            if i == 0:
                if re_hascapital.match(token):
                    first_tokens.add(token)
            else:
                tokens_count[token] += 1

    sentence_start_map = dict()
    for token in first_tokens:
        if tokens_count[token] < tokens_count[token.lower()]:
            sentence_start_map[token] = token.lower()
    return sentence_start_map
