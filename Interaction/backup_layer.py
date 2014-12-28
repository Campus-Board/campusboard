from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_media.protocolentities  import ImageDownloadableMediaMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
#from yowsup.layers.protocol_media.protocolentities  import LocationMediaMessageProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import OutgoingAckProtocolEntity
#from yowsup.layers.protocol_media.protocolentities  import VCardMediaMessageProtocolEntity

from Data.models import Message
from Data.models import User
from datetime import datetime
import smtplib
from ManagerBoard.models import Document
import traceback
import pickle
from Personalization import constants
from Personalization import text_analysis

import logging
logger = logging.getLogger(__name__)


class EchoLayer(YowInterfaceLayer):

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):

        if not messageProtocolEntity.isGroupMessage():
            if messageProtocolEntity.getType() == 'text':
                self.onTextMessage(messageProtocolEntity)
            elif messageProtocolEntity.getType() == 'media':
                self.onMediaMessage(messageProtocolEntity)
    
    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        ack = OutgoingAckProtocolEntity(entity.getId(), "receipt", "delivery")
        self.toLower(ack)
    def parse_command(self, requestor_phone, body):
        tokens = body.split()
        try:
            if len(tokens) == 0:
                return
            print (tokens[0] == '#cadastrar')
            if tokens[0] == '#cadastrar':
                if len(tokens) >= 3:
                    inbase = User.objects.filter(phone_number=requestor_phone)
                    print "found %d users!" % len(inbase)
                    print len(requestor_phone)
                    print len(tokens[1])
                    print len(tokens[2])
                    print len(pickle.dumps(constants.default_profile()))
                    if len(inbase) == 0:
                        user = User()
                        user.phone_number = requestor_phone
                        user.bluetooth_id = tokens[1]
                        user.alias = tokens[2]
                        print "LEN profile"
                        user.set_profile(constants.default_profile())
                        print len(user.get_profile())
                        user.save()
                    else:
                        user = inbase[0]
                        user.bluetooth_id = tokens[1]
                        user.alias = tokens[2]
                        user.save()
            elif tokens[0] == '#obter':
                if len(tokens) >= 3:
                    doc_id = tokens[1].lower()
                    real_id = (ord(doc_id[0]) - ord('0'))*10 + (ord(doc_id[1]) - ord('0'))
                    docs = Document.objects.filter(id=real_id)
                    if len(docs) != 1:
                        print "[WARNING] Docs retrieved %d" % (len(docs))
                    else:
                        msg = docs[0].title.upper() + '\n' + docs[0].message + '\n'
                        self.send_email(tokens[2], requestor_phone, msg)
        except Exception, err:
            print 'parsing command error'
            print Exception, err

    def send_email(self, to, from_, message):
        gmail_user = 'mail.campusboard@gmail.com'
        gmail_pwd = 'Campusboard1'
        smtpserver = smtplib.SMTP("smtp.gmail.com",587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo
        smtpserver.login(gmail_user, gmail_pwd)
        header = 'To:' + to + '\n' + 'From: mail@campusboard.com' + gmail_user + '\n' + 'Subject: Conteudo solicitado por ' + from_ + '\n'
        msg = header + '\n ' + message + ' \n\n'
        smtpserver.sendmail(gmail_user, to, msg)
        smtpserver.close()
        users = User.objects.filter(phone_number = from_)
        assert len(users) <= 1
        if len(users == 0):
            logger.debug("Unregistered user: %s"%(from_))
        else:
            users[0].set_profile(text_analysis.update_profile_by_data(users[0].get_profile(), message, 0.2))
            users[0].save()

    def onTextMessage(self,messageProtocolEntity):
        receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom())
        outgoingMessageProtocolEntity = TextMessageProtocolEntity(
            messageProtocolEntity.getBody(),
            to = messageProtocolEntity.getFrom())

        print("Message received: %s from %s" % (messageProtocolEntity.getBody(), messageProtocolEntity.getFrom(False)))
        body = messageProtocolEntity.getBody()
        if len(body) > 0 and body[0] == '#':
            self.parse_command(messageProtocolEntity.getFrom(), body)
        else:
            print "non-command"
            phone = messageProtocolEntity.getFrom()
            message_body = messageProtocolEntity.getBody()
            Message.objects.create(author = phone, content = message_body, creation = datetime.now())

            users = User.objects.filter(phone_number = phone)
            assert len(users) <= 1
            if len(users) == 1:
                user = users[0]
                print "Registered user: " + user.alias
                user.set_profile(text_analysis.update_profile_by_data(user.get_profile(), message_body, 0.2))
                user.save()
                print "User saved"
        self.toLower(receipt)

    def onMediaMessage(self, messageProtocolEntity):
        if messageProtocolEntity.getMediaType() == "image":
            receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom())
            outImage = ImageDownloadableMediaMessageProtocolEntity(
                messageProtocolEntity.getMimeType(), messageProtocolEntity.fileHash, messageProtocolEntity.url, messageProtocolEntity.ip,
                messageProtocolEntity.size, messageProtocolEntity.fileName, messageProtocolEntity.encoding, messageProtocolEntity.width, messageProtocolEntity.height,
                messageProtocolEntity.getCaption(),
                to = messageProtocolEntity.getFrom(), preview = messageProtocolEntity.getPreview())
            #print("Echoing image %s to %s" % (messageProtocolEntity.url, messageProtocolEntity.getFrom(False)))
            #send receipt otherwise we keep receiving the same message over and over
            self.toLower(receipt)
            self.toLower(outImage)

        elif messageProtocolEntity.getMediaType() == "vcard":
            receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom())
            outVcard = VCardMediaMessageProtocolEntity(messageProtocolEntity.getName(),messageProtocolEntity.getCardData(),to = messageProtocolEntity.getFrom())
            print("Echoing vcard (%s, %s) to %s" % (messageProtocolEntity.getName(), messageProtocolEntity.getCardData(), messageProtocolEntity.getFrom(False)))
            #send receipt otherwise we keep receiving the same message over and over
            self.toLower(outVcard)
            self.toLower(receipt)
        elif messageProtocolEntity.getMediaType() == "location":
            receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom())
            outLocation = LocationMediaMessageProtocolEntity(messageProtocolEntity.getLatitude(),
                messageProtocolEntity.getLongitude(), messageProtocolEntity.getLocationName(),
                messageProtocolEntity.getLocationURL(), messageProtocolEntity.encoding,
                to = messageProtocolEntity.getFrom(), preview=messageProtocolEntity.getPreview())
            print("Echoing location (%s, %s) to %s" % (messageProtocolEntity.getLatitude(), messageProtocolEntity.getLongitude(), messageProtocolEntity.getFrom(False)))
            #send receipt otherwise we keep receiving the same message over and over
            self.toLower(outLocation)
            self.toLower(receipt)