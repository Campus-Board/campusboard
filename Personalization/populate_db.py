# -*- coding: utf-8 -*-
__author__ = 'mac'
from os.path import join
import csv

import Personalization.text_analysis
from ManagerBoard.models import Document

DATA_PATH = "./Data"
PERSONALIZATION_PATH = "./Personalization/"

NEWS_IC = "noticias-ic-06-today.csv"
NEWS = "noticias-unicamp.csv"
PALES = "palestras.csv"
CDC = "expos-cdc.csv"
LAGO = "casa-do-lago.csv"
ANNOT = "annotations.csv"
LABEL = "labels.csv"
TAXONOMY = 'taxonomy.txt'
TAXONOMY_LEN = 16
BOW_CORPUS = PERSONALIZATION_PATH + "bcorpus"
DICT = PERSONALIZATION_PATH + "dict"
MODEL = PERSONALIZATION_PATH + "model"
CLASSIFIER = PERSONALIZATION_PATH + "classifier"
TOPICS = 20

"""
class Document(models.Model):
    docfile = models.FileField(upload_to='board/images/%Y/%m/%d', null=True, default='', blank=True)
    title = models.CharField(max_length=100, default='')
    message = models.TextField(default='No message defined')
    date = models.DateTimeField(default=datetime.datetime.now, blank=True)
    dateEnd = models.DateTimeField(default=datetime.datetime.now, blank=True)

    type = models.TextField(blank=True)

    def __str__(self):
        return self.title"""

def load_news():
    reader = csv.reader(file(join(DATA_PATH, NEWS)), delimiter='$', quotechar='#')
    for row in reader:
        [date, title, content] = row
        doc = Document.objects.create(title=title, message=content, type='information')
        doc.save()
        print "Saved"

def load_news_ic():
    reader = csv.reader(file(join(DATA_PATH, NEWS_IC)), delimiter='$', quotechar='#')
    for row in reader:
        [title, content] = row
        Document.objects.create(title=title, message=content, type='important')

def load_expo_cdc():
    print DATA_PATH + " --- " + CDC
    print join(DATA_PATH, CDC)
    reader = csv.reader(file(join(DATA_PATH, CDC)), delimiter='$', quotechar='#')
    for row in reader:
        [inid, endd, inih, endh, title, content] = row
        Document.objects.create(title=title, message=content, type='event')

def load_palestras():
    reader = csv.reader(file(join(DATA_PATH, PALES)), delimiter='$', quotechar='#')
    res = []
    for row in reader:
        [date, title, content] = row
        Document.objects.create(title=title, message=content, type='event')
    return res

def load_lago():
    reader = csv.reader(file(join(DATA_PATH, LAGO)), delimiter='$', quotechar='#')
    res = []
    for row in reader:
        [ini, end, title, content] = row
        Document.objects.create(title=title, message=content, type='event')

from Data.models import Message
def load_whatsapp():
    cnt = "Frases Natal e Ano Novo Feliz Natal para você e sua família, Um ano novo repleto de coisas boas... Cansou de mandar sempre as mesmas mensagens de boas festas? Inove!"
    msgs = [cnt]*20
    for msg in msgs:
        #Message.objects.create(author = 'anon', content = msg)
        m = Message()
        m.author = 'anon'
        m.content = cnt
        m.save()
def populate():
    load_expo_cdc()
    load_lago()
    load_news()
    load_news_ic()
    load_palestras()
    load_whatsapp()