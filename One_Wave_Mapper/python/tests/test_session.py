from onewave_mapper.session import Session, NoteEvent


def test_session_create_and_save_round_trip(tmp_path):
    session = Session.create(sample_rate=48000, bit_depth="float32", channel_count=2,
                              buffer_size=256, instrument="guitar")
    session.save(tmp_path)

    root = session.root_dir(tmp_path)
    assert (root / "session.json").exists()
    for sub in ("audio", "analysis/pitch_tracks", "analysis/harmonic_tracks",
                "analysis/envelopes", "analysis/resonance_events",
                "analysis/interference_events", "thumbnails", "exports", "logs"):
        assert (root / sub).is_dir()

    loaded = Session.load(root / "session.json")
    assert loaded.session_id == session.session_id
    assert loaded.sample_rate == 48000
    assert loaded.instrument == "guitar"


def test_note_event_json_round_trip(tmp_path):
    event = NoteEvent(
        event_id="note_00017", source_channel=1, start_sample=482100, end_sample=721440,
        sample_rate=48000, expected_note="A3", measured_frequency_hz=219.83,
        cents_offset=-1.34, pitch_confidence=0.97, attack_time_ms=12.4,
        decay_20db_seconds=2.83, rms_dbfs=-18.7, peak_dbfs=-5.1,
    )
    path = tmp_path / "event.json"
    event.save(path)

    loaded = NoteEvent.load(path)
    assert loaded == event
