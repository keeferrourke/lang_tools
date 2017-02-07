# Language Tools

This set of scripts will parse text and provide suggestions for spelling
and grammatical corrections. The scripts may be used on the command line with
verbose console output, or to produce JSON formatted output.

These scripts are intended to be merged into the _Immediate Feeback System_ as
part of the core tools.

## Prequisites

#### Python Hunspell
The spell check script makes use of Hunspell dictionaries and correction.
```
$ sudo apt install hunspell
```

You also need the python wrapper:
```
$ sudo -H pip install hunspell
```

#### Language Tool
Install LanguageTool and its python wrapper by:
```
$ sudo -H pip install --upgrade 3to2
$ sudo -H pip install --upgrade language-check
```

## Usage

### spell\_check.py

Run check on a file called `misspellings` against Canadian English dictionaries
with output to the console. If the `--lang` or short `-l` option isn't specified, then the
default language that is used is Canadian English.
```
spell_check.py --lang=en_CA -i mispellings
```

Run check on a file called `misspellings` against US English dictionaries, with
output to `corrections.json`.
```
spell_check.py --lang=en_US --json=corrections.json -i mispellings
spell_check.py -l en_US -j corrections.json -i misspellings
```

Note that if Hunspell is not installed at the default path
`/usr/share/hunspell`, then you may specify the path with the `--path` option.
For instance:
```
spell_check.py --path=/opt/hunspell -i misspellings
spell_check.py -p /opt/hunspell -i misspellings
```

For help:
```
spell_check.py --help
```

### grammar.py

Run check on a file called `bad_grammar` against Canadian English rules with
output to the console. If the `--lang` option isn't specified, then the
default language rules that are used belong to Canadian English.
```
grammar.py --lang=en_CA -i bad_grammar
```

Run check on a file called `bad_grammar` against US English rules, with output
to `grammatical.json`.
```
grammar.py --lang=en_US --json=grammatical.json -i bad_grammar
grammar.py -l en_US -j grammatical.json -i bad_grammar
```

For help:
```
grammar.py --help
```

## Caveats

### spell\_check.py

By nature of the engine, hyphenated compound words that are correct on each
side of the hyphen will pass the spellcheck even if the compound is not in the
given language's lexicon. Ex. "cat-dog" is not an English word, but will pass.

### grammar.py

Kind of slow?

## License Information

These scripts are
[free software](https://www.gnu.org/philosophy/free-sw.en.html), and are
licensed permissively under the ISC License. See the comment headers of each
script for additional information.

See also the license information attached to the libraries that were used for
this project.
