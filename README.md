# Language Tools

This set of scripts will parse text and provide suggestions for spelling
and grammatical corrections. The scripts may be used on the command line with
verbose console output, or to produce JSON formatted output.

These scripts have been merged into the
[_Immediate Feeback System_](https://github.com/ian-james/IFS) as part of the
core tools.

![IFS integration](https://krourke.org/img/lang_tools.png)

## Notes
There are now two versions of each utility, one for python2 environments, and
one for python3 environments. They accomplish the exact same task, in the
exact same fashion. A python3 rewrite was required for compatibility with
IFS however.

## Prequisites

#### Python Hunspell
The spell check script makes use of Hunspell dictionaries and correction.
```sh
$ sudo apt install hunspell libhunspell-dev
```

You also need the python wrapper:
```sh
$ sudo -H pip install hunspell
```

#### Language Tool
Install LanguageTool and its python wrapper by:
```sh
$ sudo -H pip install --upgrade 3to2
$ sudo -H pip install --upgrade language-check
```

## Usage

### spell\_check.py

Run check on a file called `misspellings` against Canadian English
dictionaries with JSON output to the console. If the `--lang` or short `-l`
option isn't specified, then the default language that is used is Canadian
English.
```sh
spell_check.py --lang=en_CA -i mispellings
```

Run check on a file called `misspellings` against US English dictionaries,
with output to `corrections.json`.
```sh
spell_check.py --lang=en_US --outfile=corrections.json --infile=mispellings
spell_check.py -l en_US -o corrections.json -i misspellings
```

Note that if Hunspell is not installed at the default path
`/usr/share/hunspell`, then you may specify the path with either the `-p` or
the  `--path` option.

For instance:
```sh
spell_check.py --path=/opt/hunspell --infile=misspellings
spell_check.py -p /opt/hunspell -i misspellings
```

By default the list of correctly spelled words is suppressed from the output,
however this can be revealed by specifying either the `-c` or `--correct`
option.
```sh
spell_check.py --correct --ifile=misspellings
spell_check.py -c -i misspellings
```

For alternative, simplified plain English output, pass the `--english` flag.

To suppress output to console when an output file is specified, pass either
`-q` or `--quiet`.

For help:
```sh
spell_check.py --help
```

### grammar.py

Run check on a file called `bad_grammar` against Canadian English rules with
JSON output to the console. If the `--lang` option isn't specified, then the
default language rules that are used belong to Canadian English.
```sh
grammar.py --lang=en_CA --infile bad_grammar
grammar.py -l en_CA -i bad_grammar
```

Run check on a file called `bad_grammar` against US English rules, with output
to `grammatical.json`.
```sh
grammar.py --lang=en_US --outfile=grammatical.json --infile bad_grammar
grammar.py -l en_US -o grammatical.json -i bad_grammar
```

Include spell checking with the grammar check:
```sh
grammar.py --infile bad_grammar --with_spelling
grammar.py -i --with_spelling
```

For alternative, simplified plain English output, pass the `--english` flag.

To suppress output to console when an output file is specified, pass either
`-q` or `--quiet`.

For help:
```sh
grammar.py --help
```

### Output
These scripts will print JSON containing feedback objects, as specified in the
[IFS Wiki](https://github.com/ian-james/IFS/wiki).

Spell checking JSON output is as follows:

```javascript
{
    "feedback" : [
        {
            "target": "received",
            "wordNum": 40,
            "lineNum": 2,
            "linePos": 12,
            "charPos": 89,
            "type": "spelling",
            "lang": "en_CA",
            "toolName": "hunspell",
            "filename": "infile.txt",
            "feedback": "Selected word not found in en_CA dictionary",
            "suggestions": [
                "recieved",
                "recieves"
            ]
        }
    ]
}

```

Grammar checking JSON output is as follows, where the `hl_begin` and `hl_end`
attributes specify the (character on line, line) positions where the error
begins, and the error ends.

```javascript
{
    "feedback" : [
        {
            "target": "...context of the error...",
            "hl_begin": [
                20,
                2
            ],
            "hl_end": [
                12,
                3
            ],
            "lang": "en_CA",
            "type": "type of grammar rule that was violated",
            "toolName": "Language Tool",
            "filename": "infile.txt",
            "feedback": "Language Tool feedback message",
            "suggestions": [
                "replacement suggestion 1",
                "replacement suggestion 2",
                "replacement suggestion 3"
            ]
        }
    ]
}

```

## Caveats

### spell\_check.py

By nature of the engine, hyphenated compound words that are correct on each
side of the hyphen will pass the spellcheck even if the compound is not in the
given language's lexicon. Ex. "cat-dog" is not an English word, but will pass.

### grammar.py

Kind of slow, maybe?

## License Information

These scripts are
[free software](https://www.gnu.org/philosophy/free-sw.en.html), and are
licensed permissively under the ISC License. See the comment headers of each
script for additional information.

See also the license information attached to the libraries that were used for
this project.
