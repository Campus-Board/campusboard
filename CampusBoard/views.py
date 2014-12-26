# -*- coding: utf-8 -*-

# Create your views here.
from random import randrange

from django.shortcuts import render_to_response
from django.template import RequestContext

from Data.Tile import Tile
from Data.Row import Row
from Data.Entry import Entry
from Data.models import Message
from CampusBoard.models import WhatsappMsg
from ManagerBoard.models import Document

import logging
logger = logging.getLogger(__name__)

from Personalization import text_analysis
from Personalization import constants
from Data.models import Message
from Data.models import User
import pickle
def main(request):
    return render_to_response('main.html', dict(), RequestContext(request))

def personal(request):
    bluetooth_id = str(request.GET.get('id'))
    users = User.objects.filter(bluetooth_id=bluetooth_id)
    assert len(users) <= 1
    profile = None
    if len(users) == 0:
        profile = constants.default_profile()
    else:
        profile = users.get_profile()

    logger.debug("PROFILE LEN: " + str(len(profile)))
    documents = Document.objects.all().order_by('-date')

    k = min( len(documents), 30)
    documents = text_analysis.get_personalized_content(profile, 20, documents)

    docsList = split_list(documents, wanted_parts=6)
    logger.debug("doclist " + str(len(docsList)))

    row = Row()
    row.tiles = []
    for docs in docsList:
        tile = Tile()
        entries = []
        type = ""
        for doc in docs:
            entries.append(Entry(doc.title, doc.message, doc.id))
            type = tile.typeMap[doc.type]
        tile.addEntries(entries)
        tile.setType(type)
        row.addTile(tile)

    rows = [row]

    return render_to_response('personal.html', dict(rows = rows), RequestContext(request))

def general(request):
    documents = Document.objects.all().order_by('-date')
    docsList = split_list(documents, wanted_parts=4)
    #logger.debug("doclist " + str(len(docsList)))

    row = Row()
    row.tiles = []
    for docs in docsList:
        tile = Tile()
        entries = []
        type = ""
        for doc in docs:
            entries.append(Entry(doc.title, doc.message, doc.id))
            type = tile.typeMap[doc.type]
            #logger.debug("doctype: "+doc.type)
        #logger.debug("type: "+type)
        tile.addEntries(entries)
        tile.setType(type)
        row.addTile(tile)

    rows = [row]
    """
    for i in range(0,2):
        logger.debug("i: "+str(i))
        logger.debug("doclist " + str(len(docsList)))
        #logger.debug("tiles en row 0 antes: "+str(len(rows[0].tiles)))
        row = Row()

        tile1 = Tile()
        docs1 = docsList[0]
        for doc in docs1:
            tile1.addEntry(Entry(doc.title, doc.message))
            tile1.setType(doc.type)
        row.addTile(tile1)

        tile2 = Tile()
        docs2 = docsList[1]
        for doc in docs2:
            tile2.addEntry(Entry(doc.title, doc.message))
            tile2.setType(doc.type)
        row.addTile(tile2)
        rows.append(row)

        logger.debug("tiles en row 0 despues: "+str(len(rows[0].tiles)))

        docsList = docsList[2:]
        """
    return render_to_response('general.html', dict(rows = rows), RequestContext(request))

from Data.models import User

def forum(request):
    whatsappMsgs = WhatsappMsg.objects.all().order_by('-creation')
    logger.debug(whatsappMsgs)
    if len(whatsappMsgs) <= 0:
        whatsappMsgs = loadMessages()
    whatsapp = whatsappMsgs[0]
    whatsapp.delete()
    return render_to_response('message.html', dict(message = whatsapp), RequestContext(request))

def loadMessages():
    whatsappMsg = []
    for msg in Message.objects.all().order_by('-creation'):
        whatsapp = WhatsappMsg(author = msg.author, content = msg.content)
        whatsapp.save()
        whatsappMsg.append(whatsapp)
    return whatsappMsg

def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] for i in range(wanted_parts) ]
