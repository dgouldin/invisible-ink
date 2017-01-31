# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid

_INVISIBLE_CHARS = (
    '\u200b',
    '\u200c',
    '\u200d',
    '\ufeff',
)
_INVISIBLE_MAP = dict(zip(
    '0123456789abcdef',
    (''.join((i, j)) for i in _INVISIBLE_CHARS for j in _INVISIBLE_CHARS),
))
_INVISIBLE_REVERSE_MAP = {v: k for k, v in _INVISIBLE_MAP.iteritems()}


def uuid_to_watermark(watermark_uuid):
    "Returns the watermark unicode string for a given uuid"
    return ''.join(_INVISIBLE_MAP[c] for c in watermark_uuid.get_hex())


_WATERMARK_LENGTH = len(uuid_to_watermark(uuid.uuid4()))


def watermark_to_uuid(watermark):
    "Returns the uuid for a given watermark string"
    if len(watermark) != _WATERMARK_LENGTH:
        raise ValueError('Watermark must be {} characters'.format(
            _WATERMARK_LENGTH))

    try:
        watermark_hex = ''.join(
            _INVISIBLE_REVERSE_MAP[k]
            for k in map(''.join, zip(*[iter(watermark)] * 2))
        )
    except KeyError:
        raise ValueError('Watermark contains invalid characters')

    return uuid.UUID(hex=watermark_hex)


def encode_watermark(text, watermark_uuid=None, prepend=False):
    """Encodes the given text with a watermark string generated from the given
    uuid. Optionally appends or prepends the watermark string.

    Returns a 2-tuple (encoded_text, watermark_uuid)
    """
    if not isinstance(text, unicode):
        raise ValueError('text must be a unicode string')

    watermark_uuid = watermark_uuid or uuid.uuid4()
    watermark = uuid_to_watermark(watermark_uuid)
    if prepend:
        encoded_text = ''.join((watermark, text))
    else:
        encoded_text = ''.join((text, watermark))

    return encoded_text, watermark_uuid


def decode_watermark(encoded_text):
    """Decodes the given text, separating out the original text and the
    watermark uuid.

    Returns a 2-tuple (text, watermark_uuid). If no watermark is detected, text
    is the original text and watermark_uuid is None.
    """
    if not isinstance(encoded_text, unicode):
        raise ValueError('encoded_text must be a unicode string')

    if len(encoded_text) < _WATERMARK_LENGTH:
        return encoded_text, None

    # appended watermark
    watermark = encoded_text[-_WATERMARK_LENGTH:]
    text = encoded_text[:-_WATERMARK_LENGTH]
    try:
        watermark_uuid = watermark_to_uuid(watermark)
    except ValueError:
        pass
    else:
        return text, watermark_uuid

    # prepended watermark
    watermark = encoded_text[:_WATERMARK_LENGTH]
    text = encoded_text[_WATERMARK_LENGTH:]
    try:
        watermark_uuid = watermark_to_uuid(watermark)
    except ValueError:
        pass
    else:
        return text, watermark_uuid

    return encoded_text, None
