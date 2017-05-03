# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import pytest

from RPLCD import codecs


@pytest.mark.parametrize(['input_', 'lookahead', 'result'], [
    ('hi', 0, [('h',), ('i',)]),
    ('hi', 1, [('h', 'i'), ('i', ' ')]),
    ('hi', 2, [('h', 'i', ' '), ('i', ' ', ' ')]),
    ('', 0, []),
    ('', 1, []),
    ('', 7, []),
])
def test_window_function(input_, lookahead, result):
    assert list(codecs._window(input_, lookahead)) == result


@pytest.mark.parametrize(['input_', 'result_a00', 'result_a02'], [
    # Empty
    ('', b'', b''),
    # Single char, obvious mapping
    (' ', b'\x20', b'\x20'),
    ('a', b'\x61', b'\x61'),
    # Single char, different mapping depending on charmap
    ('α', b'\xE0', b'\x90'),
    # Multiple 1:1 mapped chars
    ('asdf', b'\x61\x73\x64\x66', b'\x61\x73\x64\x66'),
    # Combined mapping
    ('\u207B\u00B9', b'\xE9', b'\x20\x20'),
    ('as\u207B\u00B9df', b'\x61\x73\xE9\x64\x66', b'\x61\x73\x20\x20\x64\x66'),
    ('\u207B', b'\x20', b'\x20'),
    ('\u207Ba', b'\x20\x61', b'\x20\x61'),
])
def test_encode(input_, result_a00, result_a02):
    a00 = codecs.A00Codec()
    # a02 = codecs.A02Codec()

    assert a00.encode(input_) == result_a00, \
            'Input %r encoded to %s' % (input_, a00.encode(input_))

    # TODO: A02
