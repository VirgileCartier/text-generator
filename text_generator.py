from nltk import ngrams
from numpy import random
import numpy as np

def read_corpus(nom_fichier): # Lire le corpus
    corpus = open(nom_fichier, "r", encoding="utf-8")
    return corpus.read()
    
def n_grams_corpus(corpus,n): # Renvoie les ngrams du corpus à partir de ngrams nltk
    n_grammes = ngrams(corpus.split(), n)
    return n_grammes

def print_n_grammes(n_grammes): # Print ngrams
    for ngram in n_grammes:
        print(ngram)
                
def count_n_grammes(n_grammes, counts): # renvoie un compte des ngrams
    for n_gram in n_grammes:
        if not n_gram in counts:
            counts[n_gram] = 0
        counts[n_gram] += 1
    return counts

def add_beginning_end(corpus, n): # rajoute des $ à la fin des phrases - utile pour marquer le début d'un texte et ainsi toujours avoir un contexte assurant le fonctionnement du générateur
    dollars = ""
    for i in range(n-1):
        dollars = dollars + " $ "
    corpus = dollars + corpus
    sentence_end = ['.', '!', '?']
    for i in sentence_end:
        corpus = corpus.replace(i,dollars)
    corpus = corpus + dollars
    return corpus
    
def remove_punctuation(corpus): # enlève certaines ponctuations pour simplifier 
    punctuation = ['(', ')', ':', '/', '"']
    for p in punctuation:
        corpus = corpus.replace(p,"")
    return corpus
       
def give_cond_probabilities(counts,counts_moins1): # renvoie la probabilité conditionnelle pour le cotexte droite d'un ngramm
    pr_con = {}
    for ngram in counts:
        context = []
        for w in ngram[:-1] :
            context.append(w)
        context = tuple(context)
        if context in pr_con:
            pr_con[context][ngram[len(ngram) - 1]] = counts[ngram] / counts_moins1[context]
        else:
            pr_con[context] = {ngram[len(ngram) - 1]: counts[ngram] / counts_moins1[context]}
    return(pr_con)

def generer_ngram(con_proba, context): # génére un mot aléatoire selon les probabilités conditionnelles 
    possible_outcomes = list(con_proba[context].keys())
    proba_dist = list(con_proba[context].values())
    new_proba_dist = []             # pour éviter des erreurs d'arrondissment
    for p in proba_dist:            
        q = p / sum(proba_dist)     
        new_proba_dist.append(q)    
    new_word = random.choice(possible_outcomes, 1, p=new_proba_dist)
    return(new_word[0])

def generate_text(n, con_proba, i): # générer ngram et ajouter le mot au texte renvoyé par la fonction
    text = ""
    context = []
    for k in range(n - 1):
        context.append("$")
    context = tuple(context)
    for j in range(i):
        new_word = generer_ngram(con_proba, context)
        text = text+new_word+" "
        context = list(context)
        context = context[1:]
        context.append(new_word)
        context = tuple(context)
    return text

def main(n):
    #corpus ouvert :
    corpus = read_corpus("corpus.txt")

    # n est le nombre de mots dans le ngram
    corpus = remove_punctuation(corpus)
    corpus = add_beginning_end(corpus, n)

    n_grammes = n_grams_corpus(corpus, n)
    nmoins1_grammes = n_grams_corpus(corpus, n-1)

    # Pour calculer les probabilités conditionnelles on a besoin du ngram et du ngram - 1 (le contexte)
    counts_n = {}
    counts_n = count_n_grammes(n_grammes, counts_n)
    counts_nmoins1 = {}
    counts_nmoins1 = count_n_grammes(nmoins1_grammes, counts_nmoins1)
    
    # calcule les probabilités conditionnelles
    conditional_Proba = give_cond_probabilities(counts_n,counts_nmoins1)
    
    # génère 10 fois des textes de 50 mots (peu être augmenté si souhaité)
    for i in range(0,10):
        print(generate_text(n, conditional_Proba, 50))
        input() # appuyer sur une touche pour continuer la génération
    


# 3 pour les tri-grammes, 2 pour les bi-grammes
main(3)