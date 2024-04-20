import pandas as pd
import numpy as np
import textdistance
import re
from collections import Counter
import spacy
import contextualSpellCheck
import sparknlp
from sparknlp.base import DocumentAssembler
from sparknlp.annotator import (
    Tokenizer,
    ContextSpellCheckerModel,
    ContextSpellCheckerApproach
)
from pyspark.ml import Pipeline
import pyspark.sql.functions as F
from sparknlp.base import LightPipeline

import contextualSpellCheck.data

from textblob import TextBlob
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize

class Autocorrect:
    def __init__(self) -> None:
        self.models = [TextblobMethod(), SpacyContextualSpellCheckMethod()]

    def __call__(self, input_str: str):
        res = [model(input_str) for model in self.models]
        return res

class EditDistanceMethod:
    def __init__(self) -> None:
        words = []
        with open('../data/autocorrect/book.txt', 'r') as f:
            file_name_data = f.read()
            file_name_data=file_name_data.lower()
            words = re.findall('\w+',file_name_data)

        self.V = set(words)
        # print(f"Top ten words in the text are:{words[0:10]}")
        # print(f"Total Unique words are {len(self.V)}.")

        self.word_freq = {}  
        self.word_freq = Counter(words)
        # print(self.word_freq.most_common()[0:10])


        self.probs = {}     
        Total = sum(self.word_freq.values())    
        for k in self.word_freq.keys():
            self.probs[k] = self.word_freq[k]/Total

    def __call__(self, input_word: str):
        input_word = input_word.lower()
        if input_word in self.V:
                return input_word
        else:
            sim = [1-(textdistance.Jaccard(qval=2).distance(v,input_word)) for v in self.word_freq.keys()]
            df = pd.DataFrame.from_dict(self.probs, orient='index').reset_index()
            df = df.rename(columns={'index':'Word', 0:'Prob'})
            df['Similarity'] = sim
            output = df.sort_values(['Similarity', 'Prob'], ascending=False).head()
            return output

class SpacyContextualSpellCheckMethod:
    def __init__(self) -> None:
        df = pd.read_csv("../../data/train.csv")
        first_column_list = df["text"].to_list()
        # temp = []
        # for row in first_column_list:
        #     temp.extend(row.split())
        
        from spacy.vocab import Vocab
        vocab = Vocab(strings=["card"])
        self.nlp = spacy.load('en_core_web_sm', vocab=vocab)
        contextualSpellCheck.add_to_pipe(self.nlp)

    def __call__(self, input_str: str):
        doc = self.nlp(input_str)
        return doc._.outcome_spellCheck
        # return doc._.performed_spellCheck, doc._.suggestions_spellCheck, doc._.score_spellCheck, doc._.outcome_spellCheck

class SparkNLPMethod:
    def __init__(self) -> None:

        # Start spark session
        self.spark = sparknlp.start()

        documentAssembler = (
            DocumentAssembler()
            .setInputCol("text")
            .setOutputCol("document")
        )
        
        tokenizer = Tokenizer().setInputCols(["document"]).setOutputCol("token")

        spellChecker = (
            ContextSpellCheckerApproach()
            .setInputCols("token")
            .setOutputCol("checked")
            .setBatchSize(8)
            .setEpochs(1)
            .setWordMaxDistance(3) # Maximum edit distance to consider
            .setMaxWindowLen(3) # important to find context
            .setMinCount(3.0) # Removes words that appear less frequent than that
            .setLanguageModelClasses(1650) # Value that we have a TF graph available
        )

        self.pipeline = Pipeline(stages=[documentAssembler, tokenizer, spellChecker])

        self.train()
    
    def train(self):
        df = self.spark.read.csv("../../data/train.csv", header=True)
        first_column_list = df.select(F.collect_list(df.columns[0])).first()[0]
        corpus = ' '.join(first_column_list)
        corpus_df = self.spark.createDataFrame([(corpus,)], ["text"])
        self.model = self.pipeline.fit(corpus_df)
        self.lp = LightPipeline(self.model)

    def __call__(self, input_str: str):
        res = []
        result = self.lp.annotate(input_str)
        for token, checked in zip(result["token"], result["checked"]):
            res.append(checked)

        res = " ".join(res)

        return res

class TextblobMethod:
    def __init__(self):
        df = pd.read_csv("../../data/train.csv")
        text = " ".join(df["text"])
        tokens = word_tokenize(text)
        self.vocab = set(tokens)
    
    def __call__(self, input_str: str):
        blob = TextBlob(input_str)
        corrected_words = []
        for word in blob.words:
            suggestions = word.spellcheck()
            # Prioritize words from the vocabulary
            for suggestion, _ in suggestions:
                if suggestion in self.vocab:
                    corrected_words.append(suggestion)
                    break
            else:
            # If no suggestion from vocab, use TextBlob's first suggestion
                corrected_words.append(suggestions[0][0])
        return " ".join(corrected_words)

# input_str = "I lost my crd"
# # ac = SparkNLPMethod()
# ac = Autocorrect()
# print(ac(input_str))