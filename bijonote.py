#!/usr/bin/env python
# coding: utf-8

import hashlib
import binascii
import thrift.protocol.TBinaryProtocol as TBinaryProtocol
import thrift.transport.THttpClient as THttpClient
import evernote.edam.userstore.UserStore as UserStore
import evernote.edam.notestore.NoteStore as NoteStore
import evernote.edam.type.ttypes as Types

import re
import requests
import config
from PIL import Image
from StringIO import StringIO
from datetime import date

BASE_URL = 'http://www.bijogoyomi.com'

def get_note_store():
    userStoreHttpClient = THttpClient.THttpClient(config.user_store_uri)
    userStoreProtocol = TBinaryProtocol.TBinaryProtocol(userStoreHttpClient)
    userStore = UserStore.Client(userStoreProtocol)
    noteStoreUrl = userStore.getNoteStoreUrl(config.auth_token)
    noteStoreHttpClient = THttpClient.THttpClient(noteStoreUrl)
    noteStoreProtocol = TBinaryProtocol.TBinaryProtocol(noteStoreHttpClient)
    return NoteStore.Client(noteStoreProtocol)

def get_image_url(date):
    matcher = re.compile('<img height="517" src="([^"]*)"')
    url = '{0}{1}{2}'.format(BASE_URL, '/bijo3/index.php/', date.strftime('%Y/%m/%d'))
    contents = requests.get(url).content
    return ['{0}{1}'.format(BASE_URL, url) for url in matcher.findall(contents)]

def get_image(url):
    im = Image.open(StringIO(requests.get(url).content))
    size = (800, 800)
    im.thumbnail(size, Image.ANTIALIAS)
    f = StringIO()
    im.save(f, 'JPEG', quality=80)
    return f.getvalue()

def create_note(date=date.today()):
    note = Types.Note()
    note.title = date.strftime('%Y-%m-%d')
    
    resources = []
    hash_list = []
    for url in get_image_url(date):
        image = get_image(url)
        md5 = hashlib.md5()
        md5.update(image)
        hash = md5.digest()
        
        data = Types.Data()
        data.size = len(image)
        data.bodyHash = hash
        data.body = image
        
        resource = Types.Resource()
        resource.mime = 'image/jpeg'
        resource.data = data
    
        resources.append(resource)
        hash_list.append(hash)
    
    if len(hash_list) < 1:
        return

    note.resources = resources
    
    note.content = '<?xml version="1.0" encoding="UTF-8"?>'
    note.content += '<!DOCTYPE en-note SYSTEM ' \
        '"http://xml.evernote.com/pub/enml2.dtd">'
    note.content += '<en-note>'
    for x in hash_list:
        note.content += '<en-media type="image/jpeg" hash="' + binascii.hexlify(x) + '"/>'
    note.content += '</en-note>'
    
    note_store = get_note_store()
    note_store.createNote(config.auth_token, note)

if __name__ == '__main__':
    create_note()
