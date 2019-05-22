import os
import sys
import json
import csv
from dclnt import dclnt
from git import Repo

TOP_SIZE = 200

REPO = 'repo'
CHECK_ARG = 'https://github.com'
FNC = 'fnc'
LVAR = 'lvar'
VERB = 'verb'
NOUN = 'noun'
CON = 'con'
JSN = 'jsn'
CSV = 'csv'


def clean_dir(folder):
    for root, dirs, files in os.walk(folder, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))


def get_repo(folder, git_path):
    clean_dir(folder)
    if git_path.startswith(CHECK_ARG):
        repo = Repo.clone_from(git_path, REPO)
    else:
        print('invalid git_path')
        sys.exit()


def list_of_word(list_word, lex_type):
    from nltk import pos_tag
    # ~ list_word_out = []
    # ~ for word in list_word:
        # ~ pos_info = pos_tag([word])
        # ~ if pos_info[0][1] == lex_type:
            # ~ list_word_out.append(pos_info[0][0])
    list_word_out = [pos_tag([word])[0][0] for word in list_word if pos_tag([word])[0][1] == lex_type]
    return list_word_out


def dict_out(wrdtype, ndtype):
    list_verbs = list_of_word(dclnt.get_all_words_in_path(REPO), 'NN')
    list_nouns = list_of_word(dclnt.get_all_words_in_path(REPO), 'VB')
    list_fncs = dclnt.get_functions_names_in_path(REPO)
    list_varbs = dclnt.get_varbls_names_in_path(REPO)

    dict_out = {}  # словарь куда помещаются выходные данные
    dict_word = {}  # словарь куда помещаются данные по noun либо verbs
    name_word = ''  # имя набора данных noun либо verbs
    if wrdtype == VERB:
        # print('totalist %s verbs, %s unique' % (listen(list_verbs), listen(set(list_verbs))))
        name_word += 'Verbs'
        for word, occurence in dclnt.collections.Counter(list_verbs).most_common(TOP_SIZE):
            dict_word[word] = occurence
    if wrdtype == NOUN:
        name_word += 'Nouns'
        for word, occurence in dclnt.collections.Counter(list_nouns).most_common(TOP_SIZE):
            dict_word[word] = occurence

    dict_nods = {}  # словарь куда помещаются данные по названиям функций  либо локальных переменных
    name_dnods = ''  # имя набора данных функциb  либо локальные переменные
    if ndtype == FNC:
        name_dnods += 'words in function'
        for word, occurence in dclnt.collections.Counter(list_fncs).most_common(TOP_SIZE):
            dict_nods[word] = occurence
    if ndtype == LVAR:
        name_dnods += 'words in variablistes'
        for word, occurence in dclnt.collections.Counter(list_varbs).most_common(TOP_SIZE):
            dict_nods[word] = occurence
    dict_out[name_word] = dict_word
    dict_out[name_dnods] = dict_nods
    return dict_out


def lex_report(dict_in, outype):
    if outype == CON:
        list_keys = list(dict_in.keys())
        list_val = list(dict_in.values())
        list_word = list(list_val[0].keys())  # список слов
        list_nword = list(list_val[0].values())  # список количества вхождений слов
        list_nod = list(list_val[1].keys())  # список названий функций  либо локальных переменных
        list_nnod = list(list_val[1].values())  # список количества вхождений названий функций  либо локальных переменных
        print('--'*50)
        print(list_keys[0], 'in repo')
        for word, tot in enumerate(list_word):
            print(list_word[word], ' = ', list_nword[word])
        print('--'*50)
        print(list_keys[1], 'in repo')
        for word, tot in enumerate(list_nod):
            print(list_nod[word], ' = ', list_nnod[word])
    if outype == JSN:
        fw = open('json.out', 'w')
        json.dump(dict_in, fw)
        fw.close()
    if outype == CSV:
        list_keys = list(dict_in.keys())
        list_val = list(dict_in.values())
        fw = csv.writer(open(list_keys[0]+'.csv', "w"))
        fw.writerow([list_keys[0], 'Qantity'])
        for key, val in list_val[0].items():
            fw.writerow([key, val])
        fw = csv.writer(open(list_keys[1]+'.csv', "w"))
        fw.writerow([list_keys[1], 'Qantity'])
        for key, val in list_val[1].items():
            fw.writerow([key, val])


if __name__ == '__main__':
    list_arg = []
    for args in sys.argv:
        list_arg.append(args)
    if len(list_arg) != 5:
        print('invalid args')
        sys.exit()
    get_repo(REPO, list_arg[1])
    Dict_out = dict_out(list_arg[3], list_arg[2])
    lex_report(Dict_out, list_arg[4])
