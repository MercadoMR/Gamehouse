# Python program to read
import os
import re
import sqlite3
import nltk
import num2words as nw
import numpy as np
import math as mt
from nltk.corpus import stopwords
import random


""" FUNCIONES DE PREPROCESAMIENTO """
def lower_case(data):
    minus = [desc.lower() for desc in data]  # A list of strings
    return minus

def remove_punctuation(texts):
    data = []
    for desc in texts:
        data.append(re.sub(r'[^\w\s]', '', desc))
    return data

def tokenize1(texts):
    data = []  # List to keep each string coverted to list
    for desc in texts:
        tokens = nltk.word_tokenize(desc, "spanish")
        data.append(tokens)
    return data

def convert_number(texts):
    data = []
    for desc in texts:
        data.append([nw.num2words(word, lang="es") if word.isnumeric()
                     else word for word in desc])
    return data

def single_character(texts):
    data = []
    for desc in texts:  # Could it be for 2 characters?
        no_single = [word for word in desc if len(word) > 2]
        data.append(no_single)
    return data

def stop_words(texts):
    data = []
    sw = stopwords.words("spanish")
    for desc in texts:
        data.append([word for word in desc if word not in sw])
    return data

def tag_sentences(texts):
    from django.conf import settings
    from pickle import load
    dt = open(settings.ALGORITHMS_DIR + 'tagger.pkl', "rb")
    tagger = load(dt)
    dt.close()
    tagged = []
    for desc in texts:
        # List of tuples (word,tag) for each description
        desc_tagged = tagger.tag(desc)
        # Simple 'string tag' instead of a tuple
        desc_tagged = [pair[0] + " " + pair[1][0] for pair in desc_tagged]
        desc_tagged = [wordtag.lower()
                       for wordtag in desc_tagged]  # Lower each word+tag
        tagged.append(desc_tagged)
    return tagged

def tag_description(description):
    from django.conf import settings
    from pickle import load
    dt = open(settings.ALGORITHMS_DIR + 'tagger.pkl', "rb")
    tagger = load(dt)
    dt.close()
    # List of tuples (word,tag) for each description
    tagged = tagger.tag(description)
    # Simple 'string tag' instead of a tuple
    tagged = [pair[0] + " " + pair[1][0] for pair in tagged]
    # Lower each word+tag
    tagged = [wordtag.lower() for wordtag in tagged]
    return tagged

def lemmatize(texts):
    from django.conf import settings
    from pickle import load
    dt = open(settings.ALGORITHMS_DIR + 'lemmas.pkl', "rb")
    lemmas = load(dt)
    dt.close()
    lemmatized = []
    for desc in texts:
        lemmatized.append([lemmas[word] if word in lemmas else
                           word[:-2] for word in desc])
    return lemmatized

def lemmatize_description(description):
    from django.conf import settings
    from pickle import load
    dt = open(settings.ALGORITHMS_DIR + 'lemmas.pkl', "rb")
    lemmas = load(dt)
    dt.close()
    lemmatized = [lemmas[word] if word in lemmas else
                           word[:-2] for word in description]
    return lemmatized

""" FUNCIONES PARA TF-IDF """
#https://towardsdatascience.com/natural-language-processing-feature-engineering-using-tf-idf-e8b9d00e7e76
#https://towardsdatascience.com/a-gentle-introduction-to-calculating-the-tf-idf-values-9e391f8a13e5
def clean_word(word):
    from django.conf import settings
    from pickle import load
    word = word.lower()
    word = re.sub(r'[^\w\s]', '', word)
    if word.isnumeric():
        word = nw.num2words(word, lang="es")
    word = [word,]
    
    dt = open(settings.ALGORITHMS_DIR + 'tagger.pkl', "rb")
    tagger = load(dt)
    dt.close()
    pair = tagger.tag(word)[0]
    word = pair[0] + " " + pair[1][0].lower()
    dt = open(settings.ALGORITHMS_DIR + 'lemmas.pkl', "rb")
    lemmas = load(dt)
    dt.close()
    if word in lemmas:
        word = lemmas[word]
    else:
        word = word[:-2]
    return word

def clean_description(description):
    description = description.lower() # Minimizar
    description = re.sub(r'[^\w\s]', '', description)
    description = nltk.word_tokenize(description, "spanish")
    description = [nw.num2words(word, lang="es") if word.isnumeric()
                     else word for word in description]
    description = [word for word in description if len(word) > 2]
    description = [word for word in description if word not in stopwords.words("spanish")]
    description = tag_description(description)
    description = lemmatize_description(description)
    description = ' '.join(description)
    return description

def preprocess(data):
    data = lower_case(data)  # Lowercase each string
    # Remove dots and punctuation on each string
    data = remove_punctuation(data)
    data = tokenize1(data)  # Convert each string to a list of words
    data = convert_number(data)  # Convert numbers to its word's representation
    data = single_character(data)  # Remove words of len 1
    data = stop_words(data)  # Remove stopwords
    data = tag_sentences(data)
    data = lemmatize(data)  # Lemmatize the data
    return data

def get_vocabulary(texts):
    voc = set()
    for desc in texts:
        voc.update(set(desc))
    #voc = sorted(voc)  # Comment for a set type
    return voc

def get_dict(voc):
    dict = {word: 0 for word in voc}
    return dict

def obtener_tf(bow,voc):
    """ Create a tf_vector for each description (bow) """ 
    tf_vect = np.zeros(len(voc), dtype=float)
    for word in bow:
        tf_vect[voc.index(word)] += 1
    #Version usando maximo 
    tf_vect = tf_vect / np.amax(tf_vect)
    """
    tf_vect = tf_vect / len(bow) ## En lugar de len(bow) dividir entre la palabra más grande
    """
    return tf_vect

def obtener_df(corpus,voc):
    df_vect = np.zeros(len(voc), dtype=float)
    for word in voc:
        for desc in corpus:
            if word in desc:
                df_vect[voc.index(word)] += 1
    return df_vect

#https://towardsdatascience.com/natural-language-processing-feature-engineering-using-tf-idf-e8b9d00e7e76
#https://towardsdatascience.com/a-gentle-introduction-to-calculating-the-tf-idf-values-9e391f8a13e5
def ex_tf_idf(corpus):
    N = len(corpus)
    vocabulario = set()
    corpus_bow = []
    print("Número de descripciones a procesar:",N)
    ## Convertir descripciones (string) a BoW(lista de strings)
    for i in range(N):
        #Convertir a tokens, lo que es una BoW
        corpus_bow.append(nltk.word_tokenize(corpus[i], "spanish"))
        vocabulario.update(set(corpus_bow[i]))
    corpus = corpus_bow
    vocabulario = sorted(vocabulario)
    print("Tamanio vocabulario",len(vocabulario))
    tf_vectors = []
    for i in range(N):
        tf_vectors.append(obtener_tf(corpus[i], vocabulario))
    idf_vector = obtener_df(corpus, vocabulario) #Regresa el vector DF
    print("Vector df:",idf_vector)
    idf_vector = np.log(N / idf_vector)
    print("Vector idf:",idf_vector)
    tf_idf_vectors = []
    for i in range(N):
        tf_idf_vectors.append(np.multiply(tf_vectors[i], idf_vector))
    """ Guardar vocabulario """
    from django.conf import settings
    from pickle import dump
    archivo = settings.ANALITYCS_DIR +'vocabulario.pkl' 
    output = open(archivo,'wb') #web -- write bytes
    dump(vocabulario,output, -1) #mete bytes en archivo nuestro diccionario de lemmas
    output.close()
    
    return tf_idf_vectors
    
##https://chartio.com/resources/tutorials/how-to-filter-for-empty-or-null-values-in-a-django-queryset/
##https://kavita-ganesan.com/tfidftransformer-tfidfvectorizer-usage-differences/
def im_tf_idf(corpus):
    """
    from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
    #instantiate CountVectorizer() 
    cv = CountVectorizer() 
    # this steps generates word counts for the words in your docs 
    vectores_frecuencias = cv.fit_transform(corpus) 
    tfidf_transformer = TfidfTransformer(smooth_idf=True,use_idf=True)
    tfidf_transformer.fit(vectores_frecuencias) 
    vectores_tf_idf= tfidf_transformer.transform(vectores_frecuencias)
    """
    from sklearn.feature_extraction.text import TfidfVectorizer
    print("Entro COrpus")
    vectorizer = TfidfVectorizer(use_idf=True)
    vectores_tf_idf = vectorizer.fit_transform(corpus)
    vectores_tf_idf = vectores_tf_idf.todense()
    vectores_tf_idf = vectores_tf_idf.tolist()
    vectores_numpy = []
    for vector in vectores_tf_idf:
        vectores_numpy.append(np.array(vector))
        
    """ Guardar vocabulario """
    from django.conf import settings
    from pickle import dump
    vocabulary = vectorizer.get_feature_names()
    archivo = settings.ANALITYCS_DIR +'vocabulario.pkl' 
    output = open(archivo,'wb') #web -- write bytes
    dump(vocabulary,output, -1) #mete bytes en archivo nuestro diccionario de lemmas
    output.close()
    print("Termino")
    return vectores_numpy


""" FUNCION DE RECOMENDACION """
def recomendar_tf_idf(game,generos):
    from gamehouse.sjug.models import Imagen
    from gamehouse.sadm.models import Tf_Idf
    from django.conf import settings
    from pickle import load
    dt = open(game.vector, 'rb')
    vector_favorito = load(dt)
    dt.close()
    juego_puntaje = []
    juegos = set()
    for genero in generos:
        juegos.update(genero.juego_set.all())
    for juego in juegos:
            ruta = Tf_Idf.objects.get(juego = juego)
            dt = open(ruta.vector, 'rb')
            vector_juego = load(dt)
            dt.close()
            similitud = similitud_coseno(vector_favorito, vector_juego)
            juego_puntaje.append( (juego,similitud) )
    juego_puntaje.sort(key=lambda x: x[1], reverse=True)
    recomendacion = []
    for juego in juego_puntaje:
        if juego[1] >= 0.15:
            recomendacion.append(juego[0])
    return recomendacion


def similitud_coseno(vec_1,vec_2):
    coseno = np.dot(vec_1,vec_2) / \
         ( ( np.sqrt(np.sum(vec_1**2)) ) * ( np.sqrt(np.sum(vec_2**2)) ) )
    return coseno

"""


    # coseno = np.dot(vec_1,vec_2) / \
    #     ( ( np.sqrt(np.sum(vec_1**2)) ) * ( np.sqrt(np.sum(vec_2**2)) ) )
    
    
    VIEJO TF-IDF
    

def explicit_tf_idf(texts, voc):
    N = len(texts)
    voc = sorted(voc)
    dimension = len(voc)
    # Create a dictionary of positions 
    positions = {}
    for i in range(dimension):
        positions[voc[i]] = i
    #Getting the DF 
    DF = {}
    for i in range(N):
        desc = texts[i]  # Take each description
        for word in desc:
            try:
                # Makes a set of ids from descriptions the word is in
                DF[word].add(i)
            except BaseException:
                DF[word] = {i}  # If have not been seen create a new entry
    for word in DF:
        DF[word] = len(DF[word])  # Replace the set with its length
    # Make DF vector
    df_vect = np.zeros(dimension, dtype=float)
    #Change later
    for word in DF:
        index = positions[word]
        df_vect[index] = DF[word]
    df_vect = df_vect + 1
    idf_vect = np.log(N / df_vect)
    #Getting the TF
    tf = []  # This list has a size of len(texts), each position is a vector
    for i in range(N):
        desc_vect = np.zeros(dimension, dtype=int)
        desc = texts[i]
        for word in desc:
            index = positions[word]
            desc_vect[index] += 1
        desc_vect = desc_vect / len(desc)  # Divide by description length
        tf.append(desc_vect)
    tf_idf = []
    for i in range(N):
        tfidf_vect = np.multiply(tf[i], idf_vect)
        tf_idf.append(tfidf_vect)
    return tf_idf
    
"""
