from framing import split_frames


def test_split_frames_single_complete_message():
    frames, remainder = split_frames(b'{"a": 1}\n')
    assert frames == ['{"a": 1}']
    assert remainder == b""


def test_split_frames_partial_message_kept_in_buffer():
    frames, remainder = split_frames(b'{"a": 1')
    assert frames == []
    assert remainder == b'{"a": 1'


def test_split_frames_multiple_messages_in_one_chunk():
    frames, remainder = split_frames(b'{"a": 1}\n{"b": 2}\n{"c":')
    assert frames == ['{"a": 1}', '{"b": 2}']
    assert remainder == b'{"c":'


def test_split_frames_skips_blank_lines():
    frames, remainder = split_frames(b'\n\n{"a": 1}\n')
    assert frames == ['{"a": 1}']
    assert remainder == b""
