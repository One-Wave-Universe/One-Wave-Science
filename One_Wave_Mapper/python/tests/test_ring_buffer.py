import numpy as np

from onewave_mapper.ring_buffer import RingBuffer


def test_write_and_read_latest_within_capacity():
    rb = RingBuffer(num_channels=1, capacity_samples=100, sample_rate=1000)
    block = np.arange(50, dtype=np.float32).reshape(1, -1)
    rb.write(block)
    out = rb.read_latest(50)
    assert np.array_equal(out[0], block[0])


def test_wraparound_preserves_most_recent_samples():
    capacity = 10
    rb = RingBuffer(num_channels=1, capacity_samples=capacity, sample_rate=1000)
    data = np.arange(25, dtype=np.float32).reshape(1, -1)
    rb.write(data)
    out = rb.read_latest(capacity)
    assert np.array_equal(out[0], data[0, -capacity:])


def test_total_written_tracks_absolute_position():
    rb = RingBuffer(num_channels=2, capacity_samples=16, sample_rate=48000)
    rb.write(np.zeros((2, 5)))
    rb.write(np.zeros((2, 7)))
    assert rb.total_written == 12


def test_read_range_clips_to_retained_window():
    capacity = 8
    rb = RingBuffer(num_channels=1, capacity_samples=capacity, sample_rate=1000)
    rb.write(np.arange(20, dtype=np.float32).reshape(1, -1))
    oldest, newest = rb.available_range()
    assert newest == 20
    assert oldest == 12
    out = rb.read_range(0, 20)
    assert out.shape[1] == 8
    assert np.array_equal(out[0], np.arange(12, 20))


def test_multichannel_block_larger_than_capacity_keeps_tail():
    rb = RingBuffer(num_channels=2, capacity_samples=4, sample_rate=1000)
    block = np.vstack([np.arange(10), np.arange(100, 110)]).astype(np.float32)
    rb.write(block)
    out = rb.read_latest(4)
    assert np.array_equal(out[0], block[0, -4:])
    assert np.array_equal(out[1], block[1, -4:])
