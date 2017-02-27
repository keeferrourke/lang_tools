#!/usr/bin/env python

# This script uses Hunspell to process arbitrary text strings and provide
# suggestions for spelling correction.
#
# Copyright (c) 2017 Keefer Rourke <mail@krourke.org>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
# OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.

import sys
import getopt
import os
import io
import json
import re
import hunspell


# spcheck(string to_check, string lang, hunspell.HunSpell hun, bool console)
def spcheck(to_check, lang, hun, console, correct_flag):
    misspelled = []  # each element is (line_num, word_num, (word, suggest[]))
    correct_words = []  # each element is (line_num, word_num, word)
    json_string = ''

    line_num = 0
    for line in to_check:
        word_num = 0
        line_num += 1
        for word in line.split():  # tokenize by whitespace delimeters?
            word_num += 1
            # simple regex to ensure that punctuation at the end of a word is
            # not passed to hunspell i.e. prevents false alarms
            word = re.sub(r'([\w])([\-,.!?]+)$', r'\1', word)
            # note that hunspell will think that cat!dog is not a word, but
            # hyphenated words such as cat-dog may pass, even though they
            # aren't in the English lexicon
            if not hun.spell(word):
                suggestion = (line_num, word_num, (word, hun.suggest(word)))
                misspelled.append(suggestion)
            else:
                correct_words.append((line_num, word_num, word))
    # print data from lists to the console if in console mode
    if console is True:
        print 'lang: ', lang
        # print correctly spelled words
        if correct_flag is True:
            print 'correctly spelled words:'
            for i in range(len(correct_words)):
                print 'at word:', correct_words[i][1],
                print 'on line:', correct_words[i][0],
                print '"' + correct_words[i][2] + '"'
            print '\n'
        # print suggestions for misspelled words
        for i in range(len(misspelled)):
            print 'misspelled word:'
            print 'at word:', misspelled[i][1],
            print 'on line:', misspelled[i][0],
            print '"' + misspelled[i][2][0] + '"'
            print 'suggestions:',
            for j in range(len(misspelled[i][2][1])):
                print misspelled[i][2][1][j],
            print '\n'
    # build a JSON string from list structures
    else:
        json_string += '{ '
        json_string += '"lang": ' + '"' + lang + '", '
        if correct_flag is True:
            json_string += '"correct words": { '
            for i in range(len(correct_words)):
                json_string += '"' + str(correct_words[i][2]) + '": { '
                json_string += '"word_num": ' + str(correct_words[i][1]) + ','
                json_string += '"line_num": ' + str(correct_words[i][0])
                json_string += ' }'
                if i != (len(correct_words) - 1):
                    json_string += ','
            json_string += ' }, '
        json_string += '"misspelled words": { '
        for i in range(len(misspelled)):
            json_string += '"' + str(misspelled[i][2][0]) + '": { '
            json_string += '"word_num": ' + str(misspelled[i][1]) + ', '
            json_string += '"line_num": ' + str(misspelled[i][0]) + ', '
            j_array = json.dumps(misspelled[i][2][1])
            json_string += '"suggestions": ' + j_array
            json_string += ' }'
            if i != (len(misspelled) - 1):
                json_string += ','
        json_string += ' } }'

        # make formatting prettier
        json_obj = json.loads(json_string)
        json_string = json.dumps(json_obj, indent=2, sort_keys=True)
        json_string += '\n'

    return json_string


# main program that takes arguments
def main(argv):
    # options
    path = '/usr/share/hunspell/'  # default hunspell install path
    lang = 'en_CA'  # default language
    json_path = ''
    ifile = ''
    console = True
    correct_words = False

    # define command line arguments and check if the script call is valid
    opts, args = getopt.getopt(argv, 'p:l:j:i:ch', ['path=', 'lang=', 'json=', 'ifile=', 'correct', 'help'])

    for opt, arg in opts:
        if opt in ('--path', '-p'):
            path = arg
            if not os.path.isdir(path):
                sys.stderr.write('Error. Path ' + path + ' does not exist.\n')
                sys.exit()
        elif opt in ('--lang', '-l'):
            lang = arg
        elif opt in ('--json', '-j'):
            json_path = arg
            console = False
        elif opt in ('--ifile', '-i'):
            ifile = arg
            if not (os.path.isfile(ifile)):
                sys.stderr.wrtie('Error. File ' + ifile + ' does not exist.\n')
                sys.exit()
        elif opt in ('--correct', '-c'):
            correct_words = True
        elif opt in ('--help', '-h') or opt not in ('--ifile', '-i'):
            print 'Usage:'
            print 'spell_check.py [--path=PATH] [--lang=LANG] [--correct]'
            print '               [--json=OUT.json] --ifile=INPUTFILE'
            print
            print 'spell_check.py [-p PATH] [-l LANG] [-c] [-j OUT.json]'
            print '               -i INPUTFILE'
            sys.exit()


    # check dictionaries exist
    hun_path = path + '/' + lang
    if not (os.path.isfile(hun_path + '.dic')):
        sys.stderr.write('Error. Could not find dictionary at '
                          + hun_path + '.dic\n')
        sys.exit()
    if not (os.path.isfile(hun_path + '.aff')):
        sys.stderr.write('Error. Count not find aff file at '
                          + hun_path + '.aff\n')
        sys.exit()

    # init hunspell
    hun = hunspell.HunSpell(hun_path + '.dic', hun_path + '.aff')

    # open infile for reading
    f_in = open(ifile, 'r')

    # perform analysis on file and return json_data for writing to file
    json_data = spcheck(f_in, lang, hun, console, correct_words)
    if console is False and json_data != '':
        json_out = open(json_path, 'w')
        json_out.write(json_data)
        json_out.close()

    f_in.close()

if __name__ == '__main__':
    main(sys.argv[1:])
