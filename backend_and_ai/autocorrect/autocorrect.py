"""Module containing autocorrect functionalities."""
import re
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize
import pandas as pd
import spacy
from spacy.vocab import Vocab
import contextualSpellCheck
import textdistance
import sparknlp
from sparknlp.base import DocumentAssembler, LightPipeline
from sparknlp.annotator import Tokenizer, ContextSpellCheckerApproach
from pyspark.ml import Pipeline
import pyspark.sql.functions as F
from textblob import TextBlob

nltk.download('punkt')
# import contextualSpellCheck.data

class Autocorrect:
    """Master Autocorrect class to select and utiize a method."""
    def __init__(self) -> None:
        # self.models = [TextblobMethod(), SpacyContextualSpellCheckMethod()]
        self.model = TextblobMethod()

    def __call__(self, input_str: str):
        return self.model(input_str)

class EditDistanceMethod:
    """Autocorrect using Edit Distance method over the English Vocabulary."""
    def __init__(self) -> None:
        words = []
        with open('datasets/autocorrect/book.txt', 'r', encoding="utf-8") as f:
            file_name_data = f.read()
            file_name_data=file_name_data.lower()
            words = re.findall(r'\w+',file_name_data)

        self.v = set(words)

        self.word_freq = {}
        self.word_freq = Counter(words)

        self.probs = {}
        total = sum(self.word_freq.values())
        for k, v in self.word_freq.items():
            self.probs[k] = v/total

    def __call__(self, input_word: str):
        input_word = input_word.lower()
        if input_word in self.v:
            return input_word

        sim = [1-(textdistance.Jaccard(qval=2).distance(v,input_word)) for v in self.word_freq]
        df = pd.DataFrame.from_dict(self.probs, orient='index').reset_index()
        df = df.rename(columns={'index':'Word', 0:'Prob'})
        df['Similarity'] = sim
        output = df.sort_values(['Similarity', 'Prob'], ascending=False).head()
        return output

class SpacyContextualSpellCheckMethod:
    """Autocorrect by ContextualSpellCheck from Spacy"""
    def __init__(self) -> None:
        df = pd.read_csv("datasets/train.csv")
        first_column_list = df["text"].to_list()

        vocab = Vocab(strings=first_column_list)
        self.nlp = spacy.load('en_core_web_sm', vocab=vocab)
        contextualSpellCheck.add_to_pipe(self.nlp)

    def __call__(self, input_str: str):
        doc = self.nlp(input_str)
        return doc._.outcome_spellCheck

class SparkNLPMethod:
    """
    Autocorrect using SparkNLP module.
    Doesn't work on ARM processors of MacBook.
    """
    def __init__(self) -> None:

        # Start spark session
        self.spark = sparknlp.start()

        document_assembler = (
            DocumentAssembler()
            .setInputCol("text")
            .setOutputCol("document")
        )

        tokenizer = Tokenizer().setInputCols(["document"]).setOutputCol("token")

        spell_checker = (
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

        self.pipeline = Pipeline(stages=[document_assembler, tokenizer, spell_checker])

        self.train()

    def train(self):
        """Train the model using vocab from queries."""
        df = self.spark.read.csv("datasets/train.csv", header=True)
        first_column_list = df.select(F.collect_list(df.columns[0])).first()[0]
        corpus = ' '.join(first_column_list)
        corpus_df = self.spark.createDataFrame([(corpus,)], ["text"])
        self.model = self.pipeline.fit(corpus_df)
        self.lp = LightPipeline(self.model)

    def __call__(self, input_str: str):
        res = []
        result = self.lp.annotate(input_str)
        for _, checked in zip(result["token"], result["checked"]):
            res.append(checked)

        res = " ".join(res)

        return res

class TextblobMethod:
    """Autocorrect using textblob class."""
    def __init__(self):
        df = pd.read_csv("datasets/train.csv")
        text = " ".join(df["text"])
        tokens = word_tokenize(text.lower())
        self.vocab = set(tokens)

    def __call__(self, input_str: str):
        blob = TextBlob(input_str.lower())
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
        corrected_str = " ".join(corrected_words)
        mod_inp = " ".join(blob.words)
        print(mod_inp, corrected_str)
        changed = corrected_str != mod_inp
        return corrected_str, changed

# input_str = "I lost my crd"
# # ac = SparkNLPMethod()
# ac = Autocorrect()
# print(ac(input_str))
