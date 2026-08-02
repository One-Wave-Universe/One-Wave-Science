import pytest

from onewave_mapper import calibration
from onewave_mapper.calibration import CalibrationProfile, ReferenceSignalType


def test_dbfs_available_without_calibration():
    assert calibration.dbfs(1.0) == pytest.approx(0.0, abs=1e-6)
    assert calibration.dbfs(0.5) < 0.0


def test_to_volts_refuses_without_profile():
    with pytest.raises(ValueError):
        calibration.to_volts(0.5, None)


def test_to_spl_refuses_without_profile():
    with pytest.raises(ValueError):
        calibration.to_spl(0.5, None)


def test_calibration_profile_round_trip_conversion(tmp_path):
    profile = CalibrationProfile.create(
        device_id="scarlett_2i2", driver_type="ASIO", input_channel=1, sample_rate=48000,
        interface_gain_setting="12 o'clock", reference_signal=ReferenceSignalType.VOLTAGE,
        reference_voltage_or_spl=1.0, measured_digital_rms=0.5,
    )
    assert profile.conversion_factor == pytest.approx(2.0)
    assert calibration.to_volts(0.25, profile) == pytest.approx(0.5)

    path = tmp_path / "cal.json"
    profile.save(path)
    loaded = CalibrationProfile.load(path)
    assert loaded == profile


def test_wrong_reference_type_rejected():
    profile = CalibrationProfile.create(
        device_id="dev", driver_type="WASAPI", input_channel=0, sample_rate=48000,
        interface_gain_setting="unity", reference_signal=ReferenceSignalType.SPL,
        reference_voltage_or_spl=94.0, measured_digital_rms=0.1,
    )
    with pytest.raises(ValueError):
        calibration.to_volts(0.1, profile)
