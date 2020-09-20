import re
from random import uniform
from collections import defaultdict

class TextGenerator:

    r_alphabet = re.compile(u'[а-яА-Я0-9-]+|[.,:;?!]+')
    file_name = ""
    model = {}

    def __init__(self, file_name):
        self.file_name = file_name

    def fit(self):
        self.train(self.file_name)

    def generate(self, phrase):
        t0, t1 = '$', '$'
        while 1:
            t0, t1 = t1, self.unirand(self.model[t0, t1])
            if t1 == '$': break
            if t1 in ('.!?,;:') or t0 == '$':
                phrase += t1
            else:
                phrase += ' ' + t1
        return phrase.capitalize()

    def gen_lines(self, corpus):
        data = open(corpus)
        for line in data:
            yield line.lower()

    def gen_tokens(self, lines):
        for line in lines:
            for token in self.r_alphabet.findall(line):
                yield token

    def gen_trigrams(self, tokens):
        t0, t1 = '$', '$'
        for t2 in tokens:
            yield t0, t1, t2
            if t2 in '.!?':
                yield t1, t2, '$'
                yield t2, '$','$'
                t0, t1 = '$', '$'
            else:
                t0, t1 = t1, t2

    def train(self, corpus):
        lines = self.gen_lines(corpus)
        tokens = self.gen_tokens(lines)
        trigrams = self.gen_trigrams(tokens)

        bi, tri = defaultdict(lambda: 0.0), defaultdict(lambda: 0.0)

        for t0, t1, t2 in trigrams:
            bi[t0, t1] += 1
            tri[t0, t1, t2] += 1

        for (t0, t1, t2), freq in tri.items():
            if (t0, t1) in self.model:
                self.model[t0, t1].append((t2, freq/bi[t0, t1]))
            else:
                self.model[t0, t1] = [(t2, freq/bi[t0, t1])]


    def unirand(self, seq):
        sum_, freq_ = 0, 0
        for item, freq in seq:
            sum_ += freq
        rnd = uniform(0, sum_)
        for token, freq in seq:
            freq_ += freq
            if rnd < freq_:
                return token


TextG = TextGenerator("tolstoy.txt")
TextG.fit()
print(TextG.generate("Правду "))