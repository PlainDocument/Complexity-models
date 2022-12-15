## Models
Complexity estimation models


## Complexity metrics
<details>
  <summary>Basic metrics</summary>
  
  
| Name  | Explanation | Explanation (in Russian) |
| ------------- | ------------- | ------------- |
| N_word | Number of tokens |количество токенов (словоформы) |
| V_word | Unique tokens |количество типов (словоформы) |
| N_lemma | Number of lemmas |количество токенов (леммы) |
| V_lemma | Unique lemmas |количество типов (леммы) |
| C | Number of symbols |количество знаков |
| punct | Number of punctuation marks |количество пунктуационных символов |
| let | Number of letters |количество букв |
| N | Number of numerals |количество числовых символов |
| syl | Number of syllables |количество слогов |
| sent | Number of sentences |количество предложений |
| word_long | Number of long words |количество длинных слов |
| word_long_pr | Proportion of long words |доля длинных слов |
| lemma_long | Number of long lemmas |количество длинных лемм |
| lemma_long_pr | Proportion of long lemmas |доля длинных лемм |
| comma_pr | Number of commas |доля запятых |
| ASL | ASL |ASL |
| ASS | ASS |ASS |
| ASW | ASW |ASW |
| ACW | ACW |ACW |
| L | L |L |
| S | S |S |
| TTR_word | SimpleTTR (tokens) |SimpleTTR (словоформы) |
| TTR_lemma | SimpleTTR (lemmas) |SimpleTTR (леммы) |
| Yule'sK_word | Yule's K (tokens) |Yule's K (словоформы) |
| Yule'sK_lemma | Yule's K (lemmas) |Yule's K (леммы) |
| Yule'sI_word | Yule's I (tokens) |Yule's I (словоформы) |
| Yule'sI_lemma | Yule's I (lemmas) |Yule's I (леммы) |
| hapax1_pr | Proportion of hapax legomena (lemmas) |доля hapax legomena (леммы) |
| hapax2_pr | Proportion of hapax dislegomena (lemmas) |доля hapax dislegomena (леммы) |
  
</details>

<details>
  <summary>Readability metrics</summary>
  
  
  
| Name  | Explainantion | Formula |
| ------------- | ------------- | ------------- |
| FRE_GL | Adapted Flesch-Kincaid |GL = 0.5 * ASL + 8.4 * ASW – 15.59 |
| SMOG | Adapted SMOG (Simple Measure of Gobbledygook) |SMOG = 1,1 * sqrt((float(64,6) / sent) * word_long) + 0,05 |
| ARI | Adapted Automated readability index |ARI = 6,26 * (float(с) / N_word) + 0,2805 * (float(N_word) / sent) – 31,04 |
| DCI | Dale-Chale index |DCI = 0,552 * (100,0 * word_long / N_word) + 0,273 * (N_word / sent) |
| CLI | Coleman-Liau index |CLI = 0,055 * L – 0,35 * S – 20,33 |

  
</details>


<details>
  <summary>Part of speech metrics</summary>

| Name | Formula |
| ------------- | ------------- |
| Func_word_pr | func_word_pr= (ADP + AUX + CCONJ + PART + SCONJ) / pos |
| Verb_pr | Verb_pr = (VERB + AUX) / pos |
| Noun_pr | Noun_pr = (NOUN + PROPN) / pos |
| Adj_pr | Adj_pr = ADJ / pos |
| Pron_pr | Pron_pr = (DET + PRON) / pos |
| Autosem_pr | Autosem_pr = (ADJ + ADV + NOUN + NUM + PROPN + VERB) / pos |
| Nouns_pr | Nouns_pr = (ADJ + NOUN + PROPN) / pos |
| NVR | NVR = (NOUN + PROPN) / (VERB + AUX) |
| Cconj_ pr | Proportion of Cconj_ pr |
| Sconj_pr | Proportion of Sconj_pr |
| Adjs_pr | Proportion of Adjs_pr |
| Prtf_pr | Proportion of Prtf_pr |
| Prts_pr | Proportion of Prts_pr |
| Npro_pr | Proportion of Npro_pr |
| Pred_pr | Proportion of Pred_pr |
| Grnd_pr | Proportion of Grnd_pr |
| Infn_pr | Proportion of Infn_pr |
| Numr_pr | Proportion of Numr_pr |
| Prcl_pr | Proportion of Prcl_pr |
| Prep_pr | Proportion of Prep_pr |
| Comp_pr | Proportion of Comp_pr |
  
</details>


<details>
  <summary>Bigram and Trigram metrics</summary>

| Name | Proportion of |
| ------------- | ------------- |
| Pos_ngrams_1_pr | VERB +NOUN |
| Pos_ngrams_2_pr | NOUN + VERB |
| Pos_ngrams_3_pr | ADVB + VERB |
| Pos_ngrams_4_pr | ADJF + 'NOUN |
| Pos_ngrams_5_pr | NOUN + NOUN |
| Pos_ngrams_6_pr | NOUN + NOUN + NOUN |
| Pos_ngrams_7_pr | NOUN + NOUN, * gent |
| Pos_ngrams_8_pr | GRND + NOUN  |
| Pos_ngrams_9_pr | ADVB + GRND |
| Pos_ngrams_10_pr | PRTF + NOUN |
| Pos_ngrams_11_pr | NOUN + PRTF and NOUN + PNCT + PRTF |
| Pos_ngrams_12_pr | PRTF + ADVB' and PRTS + ADVB |
| Pos_ngrams_13_pr | NOUN + NOUN + NOUN + NOUN |
| Dyn_Stat | Dyn_Stat= (#'VERB +NOUN' + #'NOUN+ VERB' + #'ADVB + VERB' + #'GRND + NOUN' + #'ADVB + GRND') / (#'NOUN + NOUN' + #'ADJF + NOUN') |

</details>



<details>
  <summary>Frequency zipf values</summary>
  
| Name | Proportion of |
| ------------- | ------------- |
| Zipf_0_pr | Low frequency |
| Zipf_1_pr | Low frequency |
| Zipf_2_pr | Low frequency |
| Zipf_3_pr | Low frequency |
| Zipf_4_pr | Medium frequency |
| Zipf_5_pr | Medium frequency |
| Zipf_6_pr | Medium frequency |
| Zipf_7_pr | High frequency |
| Zipf_8_pr | High frequency |
  
</details>  


<details>
  <summary>Word formation and Grammem metrics</summary>

| Name  | Explainantion | Explainantion (in russian) |
| ------------- | ------------- | ------------- |
| Word_form | share of lemmas with "tails" including certain derivational affixes (or their fragments) |доля лемм с «хвостами», включающими определённые словообразовательные аффиксы (или их фрагменты) |
| Gen_pr | proportion of word forms in the genitive case |доля словоформ в родительном падеже |
| Ablt_pr | share of word forms in instrumental case |доля словоформ в творительном падеже |
| datv | proportion of word forms in the dative case |доля словоформ в дательном падеже |
| nomn | proportion of word forms in the nominative case |доля словоформ в именительном падеже |
| loct | proportion of word forms in the prepositional case |доля словоформ в предложном падеже |
| Adjf_pr | proportion of full adjectives |доля полных прилагательных |
| Neut_pr | proportion of neuter nouns |доля существительных среднего рода |
| Inan_pr | proportion of inanimate nouns |доля неодушевлённых существительных |
| 1P_pr | proportion of verbs in the form of the 1st person |доля глаголов в форме 1-го лица |
| 3P_pr | share of verbs in the form of the 3rd person |доля глаголов в форме 3-го лица |
| Pres_pr | proportion of verbs in the present tense |доля глаголов в форме настоящего времени |
| Futr_pr | proportion of verbs in the future tense |доля глаголов в форме будущего времени |
| Past_pr | proportion of verbs in the past tense |доля глаголов в форме прошедшего времени |
| Impf_pr | proportion of imperfective verbs |доля глаголов несовершенного вида |
| Perf_pr | proportion of perfective verbs |доля глаголов совершенного вида |
| Pssv_prtf_pr | proportion of full passive participles |доля полных страдательных причастий |
| Pssv_prts_pr | proportion of short passive participles |доля кратких страдательных причастий |
| Sja_verb_pr | proportion of personal verb forms ending in -sya |доля личных глагольных форм на -ся |
  
</details>    

<details>
  <summary>Lexical and Semantic metrics</summary>

| Name  | Explainantion | Explainantion (in russian) |
| ------------- | ------------- | ------------- |
| Yavl_pr | proportion of the lemma "to be" |доля леммы "являться" |
| Textdeixis_pr | proportion of text deixis words providing coherence |доля слов текстового дейксиса, обеспечивающих связность |
| Sokr_pr | proportion of graphic abbreviations |доля графических сокращений |
| Abbr_pr | share of abbreviations |доля аббревиатур |
| FZ_pr | share of references to federal laws such as "231-FZ" |доля указаний на федеральные законы типа "231-ФЗ" |
| Term_pr | share of legal terms |доля юридических терминов |
| Abstr_pr | fraction of abstract lemmas |доля абстрактных лемм |
| Deont_pr | share of lexical indicators of deontic possibility and necessity |доля лексических показателей деонтической возможности и необходимости |
| Prep_mw_pr | share of non-single-word prepositions |доля неоднословных предлогов |
| Conj_mw_pr | proportion of non-single-word turnovers in the function of a union or conjunction word |доля неоднословных оборотов в функции союза или союзного слова |
| LVC_pr | proportion of constructions with light verbs |доля конструкций с лёгкими глаголами |
| Arch_pr | proportion of archaic words and expressions |доля архаичных слов и выражений |
  
</details>      
  
<details>
  <summary>Syntactic metrics</summary>
 
| Name  | Explainantion | Explainantion (in russian) |
| ------------- | ------------- | ------------- |
| Acl_pr | share of clausal name modifiers, sentential definitions (relative clauses are taken into account separately) |доля клаузальных модификаторов имени, сентенциальных определений (относительные клаузы учитываются отдельно) |
| Acl:relcl_pr | proportion of relative clauses |доля относительных клауз |
| Advcl_pr | share of sentimental circumstances |доля сентенциальных обстоятельств |
| Advmod_pr | proportion of adverbial predicate modifiers (adverbs or adverbial groups) |доля наречных модификаторов предиката (наречий или наречных групп) |
| Amod_pr | proportion of adjectival name modifiers |доля адъективных модификаторов имени |
| Appos_pr | share of appositive constructions |доля аппозитивных конструкций |
| Aux:pass_pr | proportion of passive constructions with an auxiliary verb |доля пассивных конструкций со вспомогательным глаголом |
| Cc_pr | proportion of conjunctions associated with conjuncts by the syntactic relation "cc" (coordination) |доля союзов, связанных с конъюнктами синтаксическим отношением "cc" (координация)  |
| Ccomp_pr | proportion of constructions with sentential additions |доля конструкций с сентенциальными дополнениями |
| Compound_pr | proportion of compound (non-single-word) expressions |доля составных (неоднословных) выражений |
| Conj_pr | the proportion of conjuncts connected by coordinating conjunctions or unionless |доля конъюнктов, связанных сочинительными союзами или бессоюзно |
| Cop_pr | proportion of clauses with elements treated as connectives |доля клауз с элементами, трактуемыми как связочные |
| Csubj_pr | share of constructions "with a sentential subject" |доля конструкций «с сентенциальным субъектом» |
| Csubj:pass_pr | share of passive constructions "with a sentential subject" |доля пассивных конструкций «с сентенциальным субъектом» |
| Discourse_pr | the proportion of occurrences of elements that serve to segment the discourse and provide connectivity |доля вхождений элементов, служащих для сегментации дискурса и обеспечения связности |
| Mark_pr | percentage of occurrences of elements that introduce dependent clauses |доля вхождений элементов, вводящих зависимые клаузы |
| Nsubj_pr | proportion of occurrences of the active subject of the main or dependent clause |доля вхождений активного подлежащего главной или зависимой клаузы |
| Nsubj:pass_pr | proportion of occurrences of the passive subject of the main or dependent clause |доля вхождений пассивного подлежащего главной или зависимой клаузы |
| Nummod_pr | proportion of numerical noun modifiers |доля числовых модификаторов существительного |
| Orphan_pr | fraction of constructions with predicate ellipsis |доля конструкций с эллипсисом предиката |
| Parataxis_pr | the proportion of elements connected by a paratactical relationship with other elements (discourse-like equivalent of coordination), as well as a paraphrase |доля элементов, связанных паратактическим отношением с другими элементами (discourse-like equivalent of coordination), а также парафраз |
| Xcomp_pr | proportion of occurrences of sentential objects with an unexpressed subject |доля вхождений сентенциальных дополнений с невыраженным подлежащим |
  
</details>     


<details>
  <summary>Coherence metrics</summary>
 
| Name  | Explainantion | Explainantion (in russian) |
| ------------- | ------------- | ------------- |
| Cohes_1 | the number of repetitions of nouns in adjacent sentences |количество повторов существительных в соседних предложениях |
| Cohes_2 | the number of repetitions of grammes of tense and form for verbs in personal form (in neighboring sentences) |количество повторов граммем времени и вида у глаголов в личной форме (в соседних предложениях) |
  
  
</details> 
