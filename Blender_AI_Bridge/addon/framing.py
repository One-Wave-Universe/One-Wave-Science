"""Zero-dependency wire framing, split out of server.py so it can be unit
tested without bpy or a real socket.
"""


def split_frames(buffer):
    """Split newline-delimited frames out of `buffer`.

    Returns (list_of_complete_frame_strings, remaining_buffer).
    """
    frames = []
    while b"\n" in buffer:
        line, buffer = buffer.split(b"\n", 1)
        if line.strip():
            frames.append(line.decode("utf-8"))
    return frames, buffer
