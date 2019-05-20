import os
import sys
import json
import csv
from dclnt import dclnt
from git import Repo

REPO = 'repo'
CHECK_ARG ='https://github.com'
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


def get_repo(folder,git_path):
    clean_dir(folder)
    if CHECK_ARG == git_path[:18] :
        repo = Repo.clone_from(git_path, REPO)
    else:
        print('invalid git_path')
        sys.exit()


def list_verb(L_word):
    from nltk import pos_tag
    L_word_out=[]
    for word in L_word:
        pos_info=pos_tag([word])
        if pos_info[0][1] == 'VB':
            L_word_out.append(pos_info[0][0])
    return L_word_out 


def list_noun(L_word):
    from nltk import pos_tag
    L_word_out=[]
    for word in L_word:
        pos_info=pos_tag([word])
        if pos_info[0][1] == 'NN':
            L_word_out.append(pos_info[0][0])
    return L_word_out 


def dict_out(wrdtype, ndtype):
    L_verbs = list_verb(dclnt.get_all_words_in_path(REPO))
    L_nouns = list_noun(dclnt.get_all_words_in_path(REPO))
    L_fncs = dclnt.get_functions_names_in_path(REPO)
    L_varbs = dclnt.get_varbls_names_in_path(REPO)

    top_size = 200
    D_out ={} # словарь куда помещаются выходные данные 

    D_word = {} # словарь куда помещаются данные по noun либо verbs
    Name_dword = '' # имя набора данных noun либо verbs
    if wrdtype == VERB:
        # print('total %s verbs, %s unique' % (len(L_verbs), len(set(L_verbs))))
        Name_dword+='Verbs'
        for word, occurence in dclnt.collections.Counter(L_verbs).most_common(top_size):
            D_word[word] = occurence
    if wrdtype == NOUN:
        Name_dword+='Nouns'
        for word, occurence in dclnt.collections.Counter(L_nouns).most_common(top_size):
            D_word[word] = occurence

    D_nods={} # словарь куда помещаются данные по названиям функций  либо локальных переменных
    Name_dnods='' # имя набора данных функциb  либо локальные переменные
    if ndtype == FNC:
        Name_dnods+='words in function'
        for word, occurence in dclnt.collections.Counter(L_fncs).most_common(top_size):
            D_nods[word] = occurence
    if ndtype == LVAR:
        Name_dnods+='words in variables'
        for word, occurence in dclnt.collections.Counter(L_varbs).most_common(top_size):
            D_nods[word] = occurence
    D_out[Name_dword]=D_word
    D_out[Name_dnods]=D_nods
    return D_out


def lex_report(Dict_in, outype):
    if outype == CON:
        L_keys = list(Dict_in.keys())
        L_val = list(Dict_in.values())
        L_word = list(L_val[0].keys()) # список слов
        L_nword = list(L_val[0].values()) # список количества вхождений слов
        L_nod = list(L_val[1].keys()) # список названий функций  либо локальных переменных
        L_nnod = list(L_val[1].values()) # список количества вхождений названий функций  либо локальных переменных
        print('--'*50)
        print (L_keys[0], 'in repo')
        for word, tot in enumerate(L_word):
            print(L_word[word], ' = ', L_nword[word])
        print('--'*50)
        print (L_keys[1], 'in repo')
        for word, tot in enumerate(L_nod):
            print(L_nod[word], ' = ', L_nnod[word])
    if outype == JSN:
        fw = open('json.out','w')
        json.dump(Dict_in,fw)
        fw.close()
    if outype == CSV:
        L_keys = list(Dict_in.keys()) # список слов
        L_val = list(Dict_in.values()) # список количества вхождений слов
        fw = csv.writer(open(L_keys[0]+'.csv', "w"))
        fw.writerow([L_keys[0], 'Qantity'])
        for key, val in L_val[0].items():
            fw.writerow([key, val])
        fw = csv.writer(open(L_keys[1]+'.csv', "w"))
        fw.writerow([L_keys[1], 'Qantity'])
        for key, val in L_val[1].items():
            fw.writerow([key, val])


if __name__ == '__main__':
    L_arg = []
    for args in sys.argv:
        L_arg.append(args)
    if len(L_arg) != 5:
        print('invalid args')
        sys.exit()
    get_repo(REPO,L_arg[1])
    D_out = dict_out(L_arg[3], L_arg[2])
    lex_report(D_out, L_arg[4])
