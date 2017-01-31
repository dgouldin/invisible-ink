# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid

import pytest

from invisible_ink import (
    decode_watermark,
    encode_watermark,
    find_all_watermark_uuids,
    uuid_to_watermark,
    watermark_to_uuid,
)


def test_uuid_to_watermark():
    hex = '0123456789abcdef0123456789abcdef'
    watermark_uuid = uuid.UUID(hex=hex)
    assert uuid_to_watermark(watermark_uuid) == ''.join((
        '\u200b\u200b',  # 0
        '\u200b\u200c',  # 1
        '\u200b\u200d',  # 2
        '\u200b\ufeff',  # 3
        '\u200c\u200b',  # 4
        '\u200c\u200c',  # 5
        '\u200c\u200d',  # 6
        '\u200c\ufeff',  # 7
        '\u200d\u200b',  # 8
        '\u200d\u200c',  # 9
        '\u200d\u200d',  # a
        '\u200d\ufeff',  # b
        '\ufeff\u200b',  # c
        '\ufeff\u200c',  # d
        '\ufeff\u200d',  # e
        '\ufeff\ufeff',  # f
        '\u200b\u200b',  # 0
        '\u200b\u200c',  # 1
        '\u200b\u200d',  # 2
        '\u200b\ufeff',  # 3
        '\u200c\u200b',  # 4
        '\u200c\u200c',  # 5
        '\u200c\u200d',  # 6
        '\u200c\ufeff',  # 7
        '\u200d\u200b',  # 8
        '\u200d\u200c',  # 9
        '\u200d\u200d',  # a
        '\u200d\ufeff',  # b
        '\ufeff\u200b',  # c
        '\ufeff\u200c',  # d
        '\ufeff\u200d',  # e
        '\ufeff\ufeff',  # f
    ))


def test_watermark_to_uuid_invalid_length():
    with pytest.raises(ValueError) as excinfo:
        watermark_to_uuid('')
    excinfo.match('Watermark must be 64 characters')


def test_watermark_to_uuid_invalid_characters():
    with pytest.raises(ValueError) as excinfo:
        watermark_to_uuid('a' * 64)
    excinfo.match('Watermark contains invalid characters')


def test_watermark_to_uuid():
    hex = '0123456789abcdef0123456789abcdef'
    watermark_uuid = uuid.UUID(hex=hex)
    assert watermark_to_uuid(''.join((
        '\u200b\u200b',  # 0
        '\u200b\u200c',  # 1
        '\u200b\u200d',  # 2
        '\u200b\ufeff',  # 3
        '\u200c\u200b',  # 4
        '\u200c\u200c',  # 5
        '\u200c\u200d',  # 6
        '\u200c\ufeff',  # 7
        '\u200d\u200b',  # 8
        '\u200d\u200c',  # 9
        '\u200d\u200d',  # a
        '\u200d\ufeff',  # b
        '\ufeff\u200b',  # c
        '\ufeff\u200c',  # d
        '\ufeff\u200d',  # e
        '\ufeff\ufeff',  # f
        '\u200b\u200b',  # 0
        '\u200b\u200c',  # 1
        '\u200b\u200d',  # 2
        '\u200b\ufeff',  # 3
        '\u200c\u200b',  # 4
        '\u200c\u200c',  # 5
        '\u200c\u200d',  # 6
        '\u200c\ufeff',  # 7
        '\u200d\u200b',  # 8
        '\u200d\u200c',  # 9
        '\u200d\u200d',  # a
        '\u200d\ufeff',  # b
        '\ufeff\u200b',  # c
        '\ufeff\u200c',  # d
        '\ufeff\u200d',  # e
        '\ufeff\ufeff',  # f
    ))) == watermark_uuid


def test_find_all_watermark_uuids():
    uuids = [uuid.uuid4() for i in range(5)]

    encoded_text = """{}asdf\ufeff\u200b

    \u200b\u200d\u200b\ufeffasdfasdf{}asdfasdf

    {}{}

    asdfasdfasdf{}""".format(*map(uuid_to_watermark, uuids))

    assert find_all_watermark_uuids(encoded_text) == uuids


def test_encode_watermark_requires_unicode_text():
    with pytest.raises(ValueError) as excinfo:
        encode_watermark(b'bytestring')
    excinfo.match('text must be a unicode string')


def test_encode_watermark_uses_given_uuid():
    text = 'asdf'
    watermark_uuid = uuid.uuid4()
    encoded_text, encoded_uuid = encode_watermark(
        text,
        watermark_uuid=watermark_uuid,
    )

    assert encoded_uuid == watermark_uuid
    assert encoded_text[:len(text)] == text
    assert watermark_to_uuid(encoded_text[len(text):]) == watermark_uuid


def test_encode_watermark_generates_uuid_if_not_given():
    text = 'asdf'
    encoded_text, watermark_uuid = encode_watermark(text)

    assert encoded_text[:len(text)] == text
    assert watermark_to_uuid(encoded_text[len(text):]) == watermark_uuid


def test_encode_watermark_optionally_prepends_watermark():
    text = 'asdf'
    encoded_text, watermark_uuid = encode_watermark(text, prepend=True)

    assert encoded_text[-1 * len(text):] == text
    assert watermark_to_uuid(encoded_text[:-1 * len(text)]) == watermark_uuid


def test_decode_watermark_requires_unicode_encoded_text():
    with pytest.raises(ValueError) as excinfo:
        decode_watermark(b'bytestring')
    excinfo.match('text must be a unicode string')


def test_decode_watermark_returns_original_encoded_text_if_too_short():
    encoded_text = 'asdf'
    assert decode_watermark(encoded_text) == (encoded_text, None)


def test_decode_watermark_returns_original_encoded_text_if_no_watermark():
    encoded_text = 'a' * 65
    assert decode_watermark(encoded_text) == (encoded_text, None)


def test_decode_watermark_prepended():
    watermark_uuid = uuid.uuid4()
    watermark = uuid_to_watermark(watermark_uuid)
    text = 'asdf'
    assert decode_watermark(''.join((watermark, text))) == (
        text,
        watermark_uuid,
    )


def test_decode_watermark_appended():
    watermark_uuid = uuid.uuid4()
    watermark = uuid_to_watermark(watermark_uuid)
    text = 'asdf'
    assert decode_watermark(''.join((text, watermark))) == (
        text,
        watermark_uuid,
    )
