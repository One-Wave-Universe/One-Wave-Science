import numpy as np
import pytest

from onewave_mapper import signal_generator
from onewave_mapper.session import Session
from onewave_mapper.recorder import Recorder, reopen_recording


def test_record_and_reopen_preserves_original_samples(tmp_path):
    sr = 48000
    signal = signal_generator.sine(440, 0.5, sr, amplitude=0.5).astype(np.float32)

    session = Session.create(sample_rate=sr, bit_depth="float32", channel_count=1, buffer_size=256)
    recorder = Recorder(session, tmp_path)
    recorder.record_array(signal.reshape(1, -1), block_size=512)
    recorder.finalize()

    loaded_session, wav_data = reopen_recording(tmp_path, session.session_id)
    assert loaded_session.session_id == session.session_id
    assert np.allclose(wav_data.samples[:, 0], signal, atol=1e-6)


def test_finalize_refuses_to_overwrite_existing_recording(tmp_path):
    sr = 8000
    signal = signal_generator.sine(200, 0.1, sr)
    session = Session.create(sample_rate=sr, bit_depth="float32", channel_count=1, buffer_size=128)
    recorder = Recorder(session, tmp_path)
    recorder.record_array(signal.reshape(1, -1))
    recorder.finalize()

    recorder2 = Recorder(session, tmp_path)
    recorder2.record_array(signal.reshape(1, -1))
    with pytest.raises(FileExistsError):
        recorder2.finalize()


def test_ring_buffer_mirrors_recent_history_during_recording(tmp_path):
    sr = 48000
    signal = signal_generator.sine(300, 1.0, sr)
    session = Session.create(sample_rate=sr, bit_depth="float32", channel_count=1, buffer_size=256)
    recorder = Recorder(session, tmp_path)
    recorder.record_array(signal.reshape(1, -1), block_size=512)

    latest = recorder.ring_buffer.read_latest(1000)
    assert latest.shape[1] == 1000
