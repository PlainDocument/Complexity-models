import xml.etree.ElementTree as ET
import argparse
import re
import glob
from collections import Counter
import math as m
import csv
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
import os


def N_word(words):
    return sum([len(i) for i in words])

def V_word(words):
    return len(set([item['word'] for sublist in words for item in sublist]))

def N_lemma(words):
    return N_word(words)

def V_lemma(words):
    return len(set([item['lemma'] for sublist in words for item in sublist]))

def C(sents):
    return sum([len(i) for i in sents])

def punct(words):
    return len([item for sublist in words for item in sublist if item['pos']=='PUNCT'])

def let(sents):
    return sum([len(re.sub('[^a-zA-Zа-яА-Я]+', '', s)) for s in sents])

def N(sents):
    return sum([len(re.sub('[^0-9]+', '', s)) for s in sents])

def syl(sents):
    return sum([len(re.sub('[^ауоыиэяюёе]+', '', s)) for s in sents])

def sent(sents):
    return len(sents)

def word_long(words):
    syls = [re.sub('[^ауоыиэяюёе]+', '', item['word']) for sublist in words for item in sublist]
    return len([i for i in syls if len(i)>3])

def word_long_pr(words):
    syls = [re.sub('[^ауоыиэяюёе]+', '', item['word']) for sublist in words for item in sublist]
    if len(syls)>0:
        return len([i for i in syls if len(i)>3])/len(syls)
    else:
        return 0

def lemma_long(words):
    syls = [re.sub('[^ауоыиэяюёе]+', '', item['lemma']) for sublist in words for item in sublist]
    return len([i for i in syls if len(i)>3])

def lemma_long_pr(words):
    syls = [re.sub('[^ауоыиэяюёе]+', '', item['lemma']) for sublist in words for item in sublist]
    if len(syls)>0:
        return len([i for i in syls if len(i)>3])/len(syls)
    else:
        return 0

def comma_pr(words):
    return len([item for sublist in words for item in sublist if item['word']==','])/sum([len(item) for sublist in words for item in sublist])

def ASL(words):
    word_ls = [len(i) for i in words]
    return sum(word_ls)/len(word_ls)

def ASS(words):
    syls = [[re.sub('[^ауоыиэяюёе]+', '', item['word']) for item in ls] for ls in words]
    syls = [sum([len(i) for i in k]) for k in syls]
    return sum(syls)/len(syls)

def ASW(words):
    syls = [len(re.sub('[^ауоыиэяюёе]+', '', item['word'])) for sublist in words for item in sublist]
    return sum(syls)/len(syls)

def ACW(words):
    wrd = [len(item['word']) for sublist in words for item in sublist]
    return sum(wrd)/len(wrd)

def L(words):
    return ACW(words)*100

def S(words):
    return 100/ASL(words)

def TTR_word(words):
    return V_word(words)/N_word(words)

def TTR_lemma(words):
    return V_lemma(words)/N_lemma(words)

def YulesK_word(words):
    wrds = [item['word'] for sublist in words for item in sublist]
    cnt = list(Counter(wrds).values())
    N = N_word(words)
    return (10**4)*((-1/N)+ sum([cnt.count(i)*((i/N)**2) for i in range(len(set(wrds)))]))

def YulesK_lemma(words):
    wrds = [item['lemma'] for sublist in words for item in sublist]
    cnt = list(Counter(wrds).values())
    N = N_lemma(words)
    return (10**4)*((-1/N)+ sum([cnt.count(i)*((i/N)**2) for i in range(len(set(wrds)))]))

def YulesI_word(words):
    V = V_word(words)
    wrds = [item['word'] for sublist in words for item in sublist]
    cnt = list(Counter(wrds).values())
    M = sum([cnt.count(i)*(i**2) for i in range(len(set(wrds)))])
    if M-V!=0:
        return (V**2)/(M-V)
    else:
        return 0

def YulesI_lemma(words):
    V = V_lemma(words)
    wrds = [item['lemma'] for sublist in words for item in sublist]
    cnt = list(Counter(wrds).values())
    M = sum([cnt.count(i)*(i**2) for i in range(len(set(wrds)))])
    if M-V!=0:
        return (V**2)/(M-V)
    else:
        return 0

def hapax1_pr(words):
    wrds = [item['lemma'] for sublist in words for item in sublist]
    cnt = list(Counter(wrds).values())
    return cnt.count(1)/len(wrds)

def hapax2_pr(words):
    wrds = [item['lemma'] for sublist in words for item in sublist]
    cnt = list(Counter(wrds).values())
    return cnt.count(2)/len(wrds)

def FRE_GL(words):
    return  0.5*ASL(words) + 8.4*ASW(words) - 15.59

def SMOG(words, sents):
    return 1.1 * m.sqrt(64.6 / sent(sents) * word_long(words)) + 0.05

def ARI(words, sents):
     return 6.26 * (C(sents) / N_word(words)) + 0.2805 * (N_word(words) / sent(sents)) - 31.04
    
def DCI(words, sents):
    return 0.552 * (100.0 * word_long(words) / N_word(words)) + 0.273 * (N_word(words) / sent(sents))

def CLI(words):
     return 0.055*L(words) - 0.35*S(words) - 20.33
    
def Func_word_pr(words):
    wsw = len([item['word'] for sublist in words for item in sublist if (item['pos']=='ADP') or (item['pos']=='AUX') or (item['pos']=='CCONJ') or (item['pos']=='PART') or (item['pos']=='SCONJ')])
    return wsw / N_word(words)

def Verb_pr(words):
    wsw = len([item['word'] for sublist in words for item in sublist if (item['pos']=='VERB') or (item['pos']=='AUX')])
    return wsw / N_word(words)

def Noun_pr(words):
    wsw = len([item['word'] for sublist in words for item in sublist if (item['pos']=='NOUN') or (item['pos']=='PROPN')])
    return wsw / N_word(words)

def Adj_pr(words):
    wsw = len([item['word'] for sublist in words for item in sublist if (item['pos']=='ADJ')])
    return wsw / N_word(words)

def Prop_pr(words):
    wsw = len([item['word'] for sublist in words for item in sublist if (item['pos']=='DET') or (item['pos']=='PRON')])
    return wsw / N_word(words)

def Autosem_pr(words):
    wsw = len([item['word'] for sublist in words for item in sublist if (item['pos']=='ADJ') or (item['pos']=='ADV') or (item['pos']=='NOUN') or (item['pos']=='NUM') or (item['pos']=='PROPN') or (item['pos']=='VERB')])
    return wsw / N_word(words)

def Nouns_pr(words):
    wsw = len([item['word'] for sublist in words for item in sublist if (item['pos']=='ADJ') or (item['pos']=='NOUN') or (item['pos']=='PROPN')])
    return wsw / N_word(words)

def NVR(words):
    wsw1 = len([item['word'] for sublist in words for item in sublist if (item['pos']=='NOUN') or (item['pos']=='PROPN')])
    wsw2 = len([item['word'] for sublist in words for item in sublist if (item['pos']=='VERB') or (item['pos']=='AUX')])
    if wsw2!=0:
        return wsw1 / wsw2
    else:
        return 0

def Cconj_pr(words):
    wsw = len([item['word'] for sublist in words for item in sublist if (item['pos']=='CCONJ')])
    return wsw / N_word(words)

def Sconj_pr(words):
    wsw = len([item['word'] for sublist in words for item in sublist if (item['pos']=='SCONJ')])
    return wsw / N_word(words)

def Adjs_pr(words):
    wsw = len([item['word'] for sublist in words for item in sublist if ('ADJS' in item['morph'].split(','))])
    return wsw / N_word(words)

def Prtf_pr(words):
    wsw = len([item['word'] for sublist in words for item in sublist if ('PRTF' in item['morph'].split(','))])
    return wsw / N_word(words)

def Prts_pr(words):
    wsw = len([item['word'] for sublist in words for item in sublist if ('PRTS' in item['morph'].split(','))])
    return wsw / N_word(words)

def Npro_pr(words):
    wsw = len([item['word'] for sublist in words for item in sublist if ('NPRO' in item['morph'].split(','))])
    return wsw / N_word(words)

def Pred_pr(words):
    wsw = len([item['word'] for sublist in words for item in sublist if ('PRED' in item['morph'].split(','))])
    return wsw / N_word(words)

def Grnd_pr(words):
    wsw = len([item['word'] for sublist in words for item in sublist if ('GRND' in item['morph'].split(','))])
    return wsw / N_word(words)

def Infn_pr(words):
    wsw = len([item['word'] for sublist in words for item in sublist if ('INFN' in item['morph'].split(','))])
    return wsw / N_word(words)

def Numr_pr(words):
    wsw = len([item['word'] for sublist in words for item in sublist if ('NUMR' in item['morph'].split(','))])
    return wsw / N_word(words)

def Prcl_pr(words):
    wsw = len([item['word'] for sublist in words for item in sublist if ('PRCL' in item['morph'].split(','))])
    return wsw / N_word(words)

def Prep_pr(words):
    wsw = len([item['word'] for sublist in words for item in sublist if ('PREP' in item['morph'].split(','))])
    return wsw / N_word(words)

def Comp_pr(words):
    wsw = len([item['word'] for sublist in words for item in sublist if ('COMP' in item['morph'].split(','))])
    return wsw / N_word(words)

def Pos_ngrams_1_pr(words):
    wsw = '+'.join([item['morph'].split(',')[0] for sublist in words for item in sublist])
    return wsw.count('VERB+NOUN') / N_word(words)

def Pos_ngrams_2_pr(words):
    wsw = '+'.join([item['morph'].split(',')[0] for sublist in words for item in sublist])
    return wsw.count('NOUN+VERB') / N_word(words)

def Pos_ngrams_3_pr(words):
    wsw = '+'.join([item['morph'].split(',')[0] for sublist in words for item in sublist])
    return wsw.count('ADVB+VERB') / N_word(words)

def Pos_ngrams_4_pr(words):
    wsw = '+'.join([item['morph'].split(',')[0] for sublist in words for item in sublist])
    return wsw.count('ADJF+NOUN') / N_word(words)

def Pos_ngrams_5_pr(words):
    wsw = '+'.join([item['morph'].split(',')[0] for sublist in words for item in sublist])
    return wsw.count('NOUN+NOUN') / N_word(words)

def Pos_ngrams_6_pr(words):
    wsw = '+'.join([item['morph'].split(',')[0] for sublist in words for item in sublist])
    return wsw.count('NOUN+NOUN+NOUN') / N_word(words)

def Pos_ngrams_7_pr(words):
    wsw = [item['morph'].split(',') for sublist in words for item in sublist]
    n = 0
    for i in range(len(wsw)-1):
        if 'NOUN' in wsw[i]:
            if ('NOUN' in wsw[i+1]) and ('gent' in wsw[i+1]):
                n+=1
    return n / N_word(words)

def Pos_ngrams_8_pr(words):
    wsw = '+'.join([item['morph'].split(',')[0] for sublist in words for item in sublist])
    return wsw.count('GRND+NOUN') / N_word(words)

def Pos_ngrams_9_pr(words):
    wsw = '+'.join([item['morph'].split(',')[0] for sublist in words for item in sublist])
    return wsw.count('ADVB+GRND') / N_word(words)

def Pos_ngrams_10_pr(words):
    wsw = '+'.join([item['morph'].split(',')[0] for sublist in words for item in sublist])
    return wsw.count('PRTF+NOUN') / N_word(words)

def Pos_ngrams_11_pr(words):
    wsw = [item['morph'].split(',') for sublist in words for item in sublist]
    n = 0
    for i in range(len(wsw)-1):
        if 'NOUN' in wsw[i]:
            if 'PNCT' in wsw[i+1]:
                try:
                    if 'PRTF' in wsw[i+2]:
                        n+=1
                except:
                    pass
            else:
                if 'PRTF' in wsw[i+1]:
                    n+=1
    return n / N_word(words)

def Pos_ngrams_12_pr(words):
    wsw = '+'.join([item['morph'].split(',')[0] for sublist in words for item in sublist])
    return (wsw.count('PRTF+ADVB') + wsw.count('PRTS+ADVB'))/ N_word(words)

def Dyn_Stat(words):
    wsw = '+'.join([item['morph'].split(',')[0] for sublist in words for item in sublist])
    if (wsw.count('NOUN+NOUN') + wsw.count('ADJF+VERB'))!=0:
        return (wsw.count('VERB+NOUN') + wsw.count('NOUN+VERB') + wsw.count('ADVB+VERB') + wsw.count('GRND+NOUN') + wsw.count('ADVB+GRND'))/ (wsw.count('NOUN+NOUN') + wsw.count('ADJF+VERB'))
    else:
        return 0

with open("./Dictionaries/metrics_int.csv", encoding = 'utf-8') as fp:
    reader = csv.reader(fp, delimiter="\t", quotechar='"')
    m_dict = [row for row in reader]
    
zipf_dict = {i[0]:int(i[13]) for i in m_dict[1:]}

def Zipf_0_pr(words):
    n = 0
    for word in [item['lemma'] for sublist in words for item in sublist]:
        try:
            if zipf_dict[word] == 0:
                n+=1
        except:
            pass
    return n / N_word(words)

def Zipf_1_pr(words):
    n = 0
    for word in [item['lemma'] for sublist in words for item in sublist]:
        try:
            if zipf_dict[word] == 1:
                n+=1
        except:
            pass
    return n / N_word(words)

def Zipf_2_pr(words):
    n = 0
    for word in [item['lemma'] for sublist in words for item in sublist]:
        try:
            if zipf_dict[word] == 2:
                n+=1
        except:
            pass
    return n / N_word(words)

def Zipf_3_pr(words):
    n = 0
    for word in [item['lemma'] for sublist in words for item in sublist]:
        try:
            if zipf_dict[word] == 3:
                n+=1
        except:
            pass
    return n / N_word(words)

def Zipf_4_pr(words):
    n = 0
    for word in [item['lemma'] for sublist in words for item in sublist]:
        try:
            if zipf_dict[word] == 4:
                n+=1
        except:
            pass
    return n / N_word(words)

def Zipf_5_pr(words):
    n = 0
    for word in [item['lemma'] for sublist in words for item in sublist]:
        try:
            if zipf_dict[word] == 5:
                n+=1
        except:
            pass
    return n / N_word(words)

def Zipf_6_pr(words):
    n = 0
    for word in [item['lemma'] for sublist in words for item in sublist]:
        try:
            if zipf_dict[word] == 6:
                n+=1
        except:
            pass
    return n / N_word(words)

def Zipf_7_pr(words):
    n = 0
    for word in [item['lemma'] for sublist in words for item in sublist]:
        try:
            if zipf_dict[word] == 7:
                n+=1
        except:
            pass
    return n / N_word(words)

def Zipf_8_pr(words):
    n = 0
    for word in [item['lemma'] for sublist in words for item in sublist]:
        try:
            if zipf_dict[word] == 3:
                n+=1
        except:
            pass
    return n / N_word(words)

def Word_form(words):
    lems = [item['lemma'] for sublist in words for item in sublist]
    n = 0
    for lem in lems:
        if lem.endswith(tuple(['ция', 'ние', 'вие', 'тие', 'ист', 'изм', 'ура', 'ище', 'ство', 'ость', 'овка', 'атор', 'итор', 'тель', 'льный', 'овать'])):
            n+=1
    return n/N_word(words)

def Gen_pr(words):
    wsw = [item['morph'].split(',') for sublist in words for item in sublist]
    n = 0
    for mor in wsw:
        if 'gent' in mor:
            n+=1
    return n/N_word(words)

def Ablt_pr(words):
    wsw = [item['morph'].split(',') for sublist in words for item in sublist]
    n = 0
    for mor in wsw:
        if 'ablt' in mor:
            n+=1
    return n/N_word(words)

def datv(words):
    wsw = [item['morph'].split(',') for sublist in words for item in sublist]
    n = 0
    for mor in wsw:
        if 'datv' in mor:
            n+=1
    return n/N_word(words)

def nomn(words):
    wsw = [item['morph'].split(',') for sublist in words for item in sublist]
    n = 0
    for mor in wsw:
        if 'nomn' in mor:
            n+=1
    return n/N_word(words)

def loct(words):
    wsw = [item['morph'].split(',') for sublist in words for item in sublist]
    n = 0
    for mor in wsw:
        if 'loct' in mor:
            n+=1
    return n/N_word(words)

def Adjif_pr(words):
    wsw = ' '.join([item['morph'] for sublist in words for item in sublist])
    return wsw.count('ADJF')/N_word(words)

def Neut_pr(words):
    wsw = [item['morph'].split(',') for sublist in words for item in sublist]
    n = 0
    for mor in wsw:
        if 'neut' in mor:
            n+=1
    return n/N_word(words)

def Inan_pr(words):
    wsw = [item['morph'].split(',') for sublist in words for item in sublist]
    n = 0
    for mor in wsw:
        if 'inan' in mor:
            n+=1
    return n/N_word(words)

def P1_pr(words):
    wsw = [item['morph'].split(',') for sublist in words for item in sublist]
    n = 0
    for mor in wsw:
        if '1per' in mor:
            n+=1
    return n/N_word(words)

def P3_pr(words):
    wsw = [item['morph'].split(',') for sublist in words for item in sublist]
    n = 0
    for mor in wsw:
        if '3per' in mor:
            n+=1
    return n/N_word(words)

def Pres_pr(words):
    wsw = [item['morph'].split(',') for sublist in words for item in sublist]
    n = 0
    for mor in wsw:
        if 'pres' in mor:
            n+=1
    return n/N_word(words)

def Futr_pr(words):
    wsw = [item['morph'].split(',') for sublist in words for item in sublist]
    n = 0
    for mor in wsw:
        if 'futr' in mor:
            n+=1
    return n/N_word(words)

def Past_pr(words):
    wsw = [item['morph'].split(',') for sublist in words for item in sublist]
    n = 0
    for mor in wsw:
        if 'past' in mor:
            n+=1
    return n/N_word(words)

def Impf_pr(words):
    wsw = [item['morph'].split(',') for sublist in words for item in sublist]
    n = 0
    for mor in wsw:
        if 'impf' in mor:
            n+=1
    return n/N_word(words)

def Perf_pr(words):
    wsw = [item['morph'].split(',') for sublist in words for item in sublist]
    n = 0
    for mor in wsw:
        if 'perf' in mor:
            n+=1
    return n/N_word(words)

def Pssv_prtf_pr(words):
    wsw = [item['morph'].split(',') for sublist in words for item in sublist]
    n = 0
    for mor in wsw:
        if ('pssv' in mor) and ('PRTF' in mor):
            n+=1
    return n/N_word(words)

def Pssv_prts_pr(words):
    wsw = [item['morph'].split(',') for sublist in words for item in sublist]
    n = 0
    for mor in wsw:
        if ('pssv' in mor) and ('PRTS' in mor):
            n+=1
    return n/N_word(words)

def Sja_verb_pr(words):
    wsw = [[item['morph'].split(',')[0],item['word']] for sublist in words for item in sublist]
    n = 0
    for i in wsw:
        if (i[1].endswith('ся')) and (i[0]=='VERB'):
            n+=1    
    return n / N_word(words)

def Yavl_pr(words):
    wsw = [item['lemma'] for sublist in words for item in sublist]
    n = 0
    for i in wsw:
        if i=='являться':
            n+=1    
    return n / N_word(words)


with open('./Dictionaries/Textdeixis.txt', encoding='utf-8') as file:
    lines = file.readlines()
    Textdeixis = [line.rstrip() for line in lines]
    
def Textdeixis_pr(words):
    wsw = [item['word'] for sublist in words for item in sublist]
    n = 0
    for i in wsw:
        if i.startswith(tuple(Textdeixis)):
            n+=1
    return n / N_word(words)

with open('./Dictionaries/Sokr.txt', encoding='utf-8') as file:
    lines = file.readlines()
    Sokr = [line.rstrip() for line in lines]
    
def Sokr_pr(words):
    wsw = [item['word'].lower() for sublist in words for item in sublist]
    n = 0
    for i in wsw:
        if i in Sokr:
            n+=1
    return n / N_word(words)

with open('./Dictionaries/Abbr.txt', encoding='utf-8') as file:
    lines = file.readlines()
    Abbr = [line.rstrip() for line in lines]
    
def Abbr_pr(words):
    wsw = [item['word'].lower() for sublist in words for item in sublist]
    n = 0
    for i in wsw:
        if i in Abbr:
            n+=1
    return n / N_word(words)

def FZ_pr(words, sents):
    n = sum([len(re.findall(r'[0-9]-ФЗ', sent)) for sent in sents])
    return n / N_word(words)

with open('./Dictionaries/Term.txt', encoding='utf-8') as file:
    lines = file.readlines()
    Term = [line.rstrip() for line in lines]
    
def Term_pr(words):
    wsw = ' '.join([item['lemma'].lower() for sublist in words for item in sublist])
    n = 0
    for i in Term:
        n+=wsw.count(i)
    return n / N_word(words)

with open('./Dictionaries/Abstract.txt', encoding='utf-8') as file:
    lines = file.readlines()
    Abstract = [line.rstrip() for line in lines]
    
def Abstr_pr(words):
    wsw = [item['lemma'].lower() for sublist in words for item in sublist]
    n = 0
    for i in wsw:
        if i in Abstract:
            n+=1
    return n / N_word(words)

with open('./Dictionaries/Deont.txt', encoding='utf-8') as file:
    lines = file.readlines()
    Deont = [line.rstrip() for line in lines]
    
def Deont_pr(words):
    wsw = [item['lemma'].lower() for sublist in words for item in sublist]
    n = 0
    for i in wsw:
        if i in Deont:
            n+=1
    return n / N_word(words)

with open('./Dictionaries/Prep_mw.txt', encoding='utf-8') as file:
    lines = file.readlines()
    Prep_mw = [line.rstrip() for line in lines]
    
def Prep_mw_pr(words):
    wsw = ' '.join([item['word'].lower() for sublist in words for item in sublist])
    n = 0
    for i in Prep_mw:
        if i in wsw:
            n+=1
        #n+=wsw.count(i)
    return n / N_word(words)

with open('./Dictionaries/Conj_mw.txt', encoding='utf-8') as file:
    lines = file.readlines()
    Conj_mw = [line.rstrip() for line in lines]
    
def Conj_mw_pr(words):
    wsw = ' '.join([item['word'].lower() for sublist in words for item in sublist])
    n = 0
    for i in Conj_mw:
        if i in wsw:
            n+=1
        #n+=wsw.count(i)
    return n / N_word(words)

with open('./Dictionaries/LVC.txt', encoding='utf-8') as file:
    lines = file.readlines()
    LVC = [line.rstrip() for line in lines]
    
def LVC_pr(words):
    wsw = ' '.join([item['lemma'].lower() for sublist in words for item in sublist])
    n = 0
    for i in LVC:
        if i in wsw:
            n+=1
        #n+=wsw.count(i)
    return n / N_word(words)

with open('./Dictionaries/Archaic_words.txt', encoding='utf-8') as file:
    lines = file.readlines()
    archaic = [line.rstrip() for line in lines]
    
def Arch_pr(words):
    wsw = ' '.join([item['lemma'].lower() for sublist in words for item in sublist])
    n = 0
    for i in archaic:
        if i in wsw:
            n+=1
        #n+=wsw.count(i)
    return n / N_word(words)

def Acl_pr(words, sents):
    wsw = [item['dep'].lower() for sublist in words for item in sublist]
    n = 0
    for i in wsw:
        if i == 'acl':
            n += 1
    return n / len(sents)

def Aclrelcl_pr(words, sents):
    wsw = [item['dep'].lower() for sublist in words for item in sublist]
    n = 0
    for i in wsw:
        if i == 'acl:relcl':
            n += 1
    return n / len(sents)
    
def Advcl_pr(words, sents):
    wsw = [item['dep'].lower() for sublist in words for item in sublist]
    n = 0
    for i in wsw:
        if i == 'advcl':
            n += 1
    return n / len(sents)

def Advmod_pr(words, sents):
    wsw = [item['dep'].lower() for sublist in words for item in sublist]
    n = 0
    for i in wsw:
        if i == 'advmod':
            n += 1
    return n / len(sents)

def Amod_pr(words, sents):
    wsw = [item['dep'].lower() for sublist in words for item in sublist]
    n = 0
    for i in wsw:
        if i == 'amod':
            n += 1
    return n / len(sents)

def Appos_pr(words, sents):
    wsw = [item['dep'].lower() for sublist in words for item in sublist]
    n = 0
    for i in wsw:
        if i == 'appos':
            n += 1
    return n / len(sents)

def Auxpass_pr(words, sents):
    wsw = [item['dep'].lower() for sublist in words for item in sublist]
    n = 0
    for i in wsw:
        if i == 'aux:pass':
            n += 1
    return n / len(sents)

def Cc_pr(words, sents):
    wsw = [item['dep'].lower() for sublist in words for item in sublist]
    n = 0
    for i in wsw:
        if i == 'cc':
            n += 1
    return n / len(sents)

def Ccomp_pr(words, sents):
    wsw = [item['dep'].lower() for sublist in words for item in sublist]
    n = 0
    for i in wsw:
        if i == 'ccomp':
            n += 1
    return n / len(sents)

def Compound_pr(words, sents):
    wsw = [item['dep'].lower() for sublist in words for item in sublist]
    n = 0
    for i in wsw:
        if i == 'compound':
            n += 1
    return n / len(sents)

def Conj_pr(words, sents):
    wsw = [item['dep'].lower() for sublist in words for item in sublist]
    n = 0
    for i in wsw:
        if i == 'conj':
            n += 1
    return n / len(sents)

def Cop_pr(words, sents):
    wsw = [item['dep'].lower() for sublist in words for item in sublist]
    n = 0
    for i in wsw:
        if i == 'cop':
            n += 1
    return n / len(sents)

def Csubj_pr(words, sents):
    wsw = [item['dep'].lower() for sublist in words for item in sublist]
    n = 0
    for i in wsw:
        if i == 'csubj':
            n += 1
    return n / len(sents)

def Csubjpass_pr(words, sents):
    wsw = [item['dep'].lower() for sublist in words for item in sublist]
    n = 0
    for i in wsw:
        if i == 'csubj:pass':
            n += 1
    return n / len(sents)

def Discourse_pr(words, sents):
    wsw = [item['dep'].lower() for sublist in words for item in sublist]
    n = 0
    for i in wsw:
        if i == 'discourse':
            n += 1
    return n / len(sents)

def Mark_pr(words, sents):
    wsw = [item['dep'].lower() for sublist in words for item in sublist]
    n = 0
    for i in wsw:
        if i == 'mark':
            n += 1
    return n / len(sents)

def Nsubj_pr(words, sents):
    wsw = [item['dep'].lower() for sublist in words for item in sublist]
    n = 0
    for i in wsw:
        if i == 'nsubj':
            n += 1
    return n / len(sents)

def Nsubjpass_pr(words, sents):
    wsw = [item['dep'].lower() for sublist in words for item in sublist]
    n = 0
    for i in wsw:
        if i == 'nsubj:pass':
            n += 1
    return n / len(sents)

def Nummod_pr(words, sents):
    wsw = [item['dep'].lower() for sublist in words for item in sublist]
    n = 0
    for i in wsw:
        if i == 'nummod':
            n += 1
    return n / len(sents)

def Orphan_pr(words, sents):
    wsw = [item['dep'].lower() for sublist in words for item in sublist]
    n = 0
    for i in wsw:
        if i == 'orphan':
            n += 1
    return n / len(sents)

def Parataxis_pr(words, sents):
    wsw = [item['dep'].lower() for sublist in words for item in sublist]
    n = 0
    for i in wsw:
        if i == 'parataxis':
            n += 1
    return n / len(sents)

def Xcomp_pr(words, sents):
    wsw = [item['dep'].lower() for sublist in words for item in sublist]
    n = 0
    for i in wsw:
        if i == 'xcomp':
            n += 1
    return n / len(sents)

def Cohes_1(words):
    wsw = [[[item['lemma'],item['pos']] for item in snt] for snt in words]
    n = 0
    for i in range(len(wsw)-1):
        ws1 = [k[0] for k in wsw[i] if k[1]=='NOUN']
        ws2 = [k[0] for k in wsw[i+1] if k[1]=='NOUN']
        n+= len(list(set(ws1) & set(ws2)))
    return n

def Cohes_2(words):
    wsw = [[item['morph'].split(',') for item in snt] for snt in words]
    n = 0
    for i in range(len(wsw)-1):
        ws1 = [1 if ('VERB' in k) and ('impf' in k) and ('pres' in k) else 0 for k in wsw[i]]
        ws2 = [1 if ('VERB' in k) and ('impf' in k) and ('pres' in k) else 0 for k in wsw[i+1]]
        n+= sum(ws1+ws2)
        ws1 = [1 if ('VERB' in k) and ('impf' in k) and ('past' in k) else 0 for k in wsw[i]]
        ws2 = [1 if ('VERB' in k) and ('impf' in k) and ('past' in k) else 0 for k in wsw[i+1]]
        n+= sum(ws1+ws2)
        ws1 = [1 if ('VERB' in k) and ('impf' in k) and ('futr' in k) else 0 for k in wsw[i]]
        ws2 = [1 if ('VERB' in k) and ('impf' in k) and ('futr' in k) else 0 for k in wsw[i+1]]
        n+= sum(ws1+ws2)
        ws1 = [1 if ('VERB' in k) and ('perf' in k) and ('pres' in k) else 0 for k in wsw[i]]
        ws2 = [1 if ('VERB' in k) and ('perf' in k) and ('pres' in k) else 0 for k in wsw[i+1]]
        n+= sum(ws1+ws2)
        ws1 = [1 if ('VERB' in k) and ('perf' in k) and ('past' in k) else 0 for k in wsw[i]]
        ws2 = [1 if ('VERB' in k) and ('perf' in k) and ('past' in k) else 0 for k in wsw[i+1]]
        n+= sum(ws1+ws2)
        ws1 = [1 if ('VERB' in k) and ('perf' in k) and ('futr' in k) else 0 for k in wsw[i]]
        ws2 = [1 if ('VERB' in k) and ('perf' in k) and ('futr' in k) else 0 for k in wsw[i+1]]
        n+= sum(ws1+ws2)
    return n    
 

class FeatureExtractor:

    def __init__(self, input_path, output_path, num_workers):
        self.input_path = input_path
        self.output_path = output_path
        self.num_workers = num_workers
        self.file_list =  [f for f in glob.glob(self.input_path + "/*.xml")]

        with open('features.txt', encoding='utf-8') as file:
            lines = file.readlines()
            functions_args = [line.rstrip() for line in lines]
        self.function_list = [i.split('(')[0] for i in functions_args]
        self.arglist = [i.split('(')[1][:-1] for i in functions_args]



    def parse_xml(self, file_path):
        tree = ET.parse(file_path) 
        root = tree.getroot()
        wordlist = []
        sentlist = []
        for sent in root.findall("./body/b/p/s"):
            sentwords = []
            for token in sent:
                word = token.attrib
                word['word'] = token.text
                word['morph'] = word['morph_pymorhy']
                word['lemma'] = word['lem']
                sentwords.append(word)
            wordlist.append(sentwords)
            sent = re.sub(r' (?=\W)', '', ' '.join([i['word'] for i in sentwords])) 
            sentlist.append(sent)
        return wordlist, sentlist

    def get_metr(self, file_path):
        words, sents = self.parse_xml(file_path)
        metrics_list = [os.path.basename(file_path)]+[eval(name)(words) 
                    if arg == 'words' else eval(name)(sents) 
                    if arg =='sents' else eval(name)(words, sents) for name, arg in zip(self.function_list, self.arglist)]
        return metrics_list

    def run(self):
        pool = Pool(processes=(self.num_workers))
        metr_list_all = list(tqdm(pool.imap(self.get_metr, self.file_list)))
        
        pool.close()
        with open(self.output_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(['fname']+self.function_list)
            writer.writerows(metr_list_all)




def main():
    parser = argparse.ArgumentParser(description="Extract linguistic features from xml files")

    parser.add_argument(
        "--input-path", default="./xml_test", help="input path"
    )

    parser.add_argument(
        "--output-path", default="metrics.csv", help="output file name"
    )

    parser.add_argument(
        "--num-workers", default=cpu_count(), type=int, help="number of workers"
    )

    args = parser.parse_args()

    feature_extractor = FeatureExtractor(
        input_path = args.input_path,
        output_path = args.output_path,
        num_workers= args.num_workers
    )
    feature_extractor.run()


if __name__ == "__main__":
    main()
