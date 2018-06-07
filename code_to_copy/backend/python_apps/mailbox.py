#!/usr/bin/env python
#-*- coding:utf8 -*-

import mailbox
import email
from email.utils import getaddresses, parsedate, parseaddr, decode_params


mailbox_obj = mailbox.Maildir(XXX_MAIL_PATH)


for k in XXX_INBOX.keys():
    message = email.message_from_string(XXX_INBOX.get_string(k))
    fr = parseaddr(message.get("from"))
    tos = message.get_all('to', [])
    ccs = message.get_all('cc', [])
    resent_tos = message.get_all('resent-to', [])
    resent_ccs = message.get_all('resent-cc', [])
    all_recipients = getaddresses(tos + ccs + resent_tos + resent_ccs)

XXX_INBOX.add(ANOTHER_XXX_INBOX.get_string(k))
XXX_INBOX.discard(k)




# send mail with html with python
# https://stackoverflow.com/questions/882712/sending-html-email-using-python

# send mail with attachments with python
# https://stackoverflow.com/questions/3362600/how-to-send-email-attachments
