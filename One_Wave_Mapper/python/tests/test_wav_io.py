import numpy as np

from onewave_mapper import signal_generator, wav_io


def test_float32_round_trip_is_bit_exact(tmp_path):
    sr = 48000
    signal = signal_generator.sine(440, 0.5, sr, amplitude=0.75).astype(np.float32)
    path = tmp_path / "tone.wav"
    wav_io.write_wav(str(path), signal, sr, bit_depth="float32")

    data = wav_io.read_wav(str(path))
    assert data.sample_rate == sr
    assert data.original_bit_depth == 32
    assert data.original_format == wav_io.IEEE_FLOAT_FORMAT
    assert np.allclose(data.samples[:, 0], signal, atol=1e-7)


def test_pcm16_round_trip_within_quantization_error(tmp_path):
    sr = 48000
    signal = signal_generator.sine(440, 0.5, sr, amplitude=0.75)
    path = tmp_path / "tone16.wav"
    wav_io.write_wav(str(path), signal, sr, bit_depth="pcm16")

    data = wav_io.read_wav(str(path))
    assert data.original_bit_depth == 16
    assert np.max(np.abs(data.samples[:, 0] - signal)) < 2.0 / 32768.0


def test_multichannel_round_trip_preserves_channel_order(tmp_path):
    sr = 48000
    left = signal_generator.sine(300, 0.2, sr, amplitude=0.5)
    right = signal_generator.sine(600, 0.2, sr, amplitude=0.25)
    stereo = np.stack([left, right], axis=1)

    path = tmp_path / "stereo.wav"
    wav_io.write_wav(str(path), stereo, sr, bit_depth="float32")

    data = wav_io.read_wav(str(path))
    assert data.samples.shape[1] == 2
    assert np.allclose(data.samples[:, 0], left, atol=1e-6)
    assert np.allclose(data.samples[:, 1], right, atol=1e-6)


def test_never_overwrites_are_caller_responsibility_but_write_is_deterministic(tmp_path):
    sr = 8000
    signal = signal_generator.sine(100, 0.1, sr)
    path = tmp_path / "a.wav"
    wav_io.write_wav(str(path), signal, sr, bit_depth="float32")
    first_bytes = path.read_bytes()
    wav_io.write_wav(str(path), signal, sr, bit_depth="float32")
    second_bytes = path.read_bytes()
    assert first_bytes == second_bytes
