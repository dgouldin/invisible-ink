Invisible Ink
=============

This library includes a set of tools for using zero-width unicode characters to
embed human-invisible messages in text.

Watermarking
------------
You can use invisible ink to uniquely identify a piece of text by embedding a
UUID:

::

    >>> from invisible_ink import encode_watermark, decode_watermark
    >>> encoded_text, uuid = encode_watermark(u'asdf')
    >>> print encoded_text
    asdf
    >>> uuid
    UUID('3ca37a37-9c5a-4b9e-a9c0-a50c47c48dba')
    >>> decode_watermark(encoded_text)
    (u'asdf', UUID('3ca37a37-9c5a-4b9e-a9c0-a50c47c48dba'))

encode_watermark *(text, watermark_uuid=None, prepend=False)*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Encodes the given text with a watermark string generated from the given uuid.
Optionally appends or prepends the watermark string.

Parameters:

* ``text``: Unicode string to which the watermark will be added

* ``watermark_uuid``: ``uuid.UUID`` instance to use as the watermark.
  (``uuid.uuid4()`` will be used to generate one if not provided.)

* ``prepend``: Indicates whether the watermark should be prended to ``text``
  (defaults to ``False``). If ``False``, the watermark will be appended.

Returns:

A 2-tuple: ``(encoded_text, watermark_uuid)``

decode_watermark *(encoded_text)*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Decodes the given text, separating out the original text and the watermark uuid.

Paramters:

* ``encoded_text``: Unicode string which potentially includes a watermark

Returns:

A 2-tuple: ``(text, watermark_uuid)``. If no watermark is detected,
``text`` is the original text and ``watermark_uuid is None``.

Installation
------------
::

    $ pip install invisible-ink
