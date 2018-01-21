import re
import json
import logging
from channels import Group
from channels.sessions import channel_session

log = logging.getLogger(__name__)


@channel_session
def ws_connect(message):
    # Extract the room from the message. This expects message.path to be of the
    # form /chat/{label}/, and finds a Room if the message path is applicable,
    # and if the Room exists. Otherwise, bails (meaning this is a some othersort
    # of websocket). So, this is effectively a version of _get_object_or_404.
    print("WS CONNECT")
    try:
        prefix, label = message['path'].decode('ascii').strip('/').split('/')
        print (prefix, label)
        if prefix != 'chat':
            log.debug('invalid ws path=%s', message['path'])
            return
    except ValueError:
        log.debug('invalid ws path=%s', message['path'])
        return


    log.debug('chat connect room=%s client=%s:%s',label, message['client'][0], message['client'][1])

    # Need to be explicit about the channel layer so that testability works
    # This may be a FIXME?
    Group('chat-' + label, channel_layer=message.channel_layer).add(message.reply_channel)

    message.channel_session['room'] = label


@channel_session
def ws_receive(message):
    # Look up the room from the channel session, bailing if it doesn't exist
    print("WS RECEIVE")
    print(type(message), message)
    try:
        label = message.channel_session['room']
        print(label)
    except KeyError:
        log.debug('no room in channel_session')
        return


    # Parse out a chat message from the content text, bailing if it doesn't
    # conform to the expected message format.
    try:
        data = json.loads(message['text'])
        print(data)
        print(message.channel_layer)
    except ValueError:
        log.debug("ws message isn't json text=%s", text)
        return

    if set(data.keys()) != set(('handle', 'message')):
        log.debug("ws message unexpected format data=%s", data)
        return

    if data:
        log.debug('chat message room=%s handle=%s message=%s',label, data['handle'], data['message'])
        m = {}

        # See above for the note about Group
        Group('chat-' + label, channel_layer=message.channel_layer).send({'text': json.dumps(m)})


@channel_session
def ws_disconnect(message):
    print("WS DISCONNECT")
    try:
        label = message.channel_session['room']
        Group('chat-' + label, channel_layer=message.channel_layer).discard(message.reply_channel)
    except (KeyError):
        pass
