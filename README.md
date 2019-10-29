# Poio Library

A NLP library of common functionality within the Poio project.

## Install package

Local install:

    $ pip install path/to/poio-lib

Install from PyPI:

    $ pip install poio-lib

## Usage

```
import poiolib
langinfo = poiolib.LangInfo()
iso_639_1 = langinfo.iso_639_1_for_3("deu")
```

## Running the tests

    $ python -m unittest discover
 
