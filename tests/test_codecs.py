from RPLCD import codecs

codecs.register()


def test_encode_alpha():
    alpha = 'α'
    assert alpha.encode('hd44780-a00') == b'\xe0', \
            'Alpha encoded to %s' % alpha.encode('hd44780-a00')
    assert alpha.encode('hd44780-a02') == b'\x90', \
            'Alpha encoded to %s' % alpha.encode('hd44780-a02')


def test_decode_alpha():
    assert b'\xe0'.decode('hd44780-a00') == 'α'
    assert b'\x90'.decode('hd44780-a02') == 'α'


def _assert_roundtrip_equality(i, encoding):
    byte = i.to_bytes(1, byteorder='big')
    decoded = byte.decode(encoding)
    encoded = decoded.encode(encoding)
    assert encoded == byte, \
        "Encoded byte %r doesn't match byte %r" % (encoded, byte)


def test_two_way_encoding_a00():
    for i in range(0b00100000, 0b01111111 + 1):
        _assert_roundtrip_equality(i, 'hd44780-a00')
    for i in range(0b10100000, 0b01111111 + 1):
        _assert_roundtrip_equality(i, 'hd44780-a00')


def test_two_way_encoding_a02():
    for i in range(0b00010000, 0b11111111 + 1):
        _assert_roundtrip_equality(i, 'hd44780-a02')
