import pytest
import json

# Logic to test: CO2 < 1000 is SAFE, >= 1000 is DANGER
def validate_air_quality(co2_level):
    return "SAFE" if co2_level < 1000 else "DANGER"

def test_air_quality_safe():
    """Verify that CO2 level below 1000 returns SAFE status"""
    assert validate_air_quality(800) == "SAFE"

def test_air_quality_danger():
    """Verify that CO2 level at or above 1000 returns DANGER status"""
    assert validate_air_quality(1200) == "DANGER"

def test_json_payload_format():
    """Verify the telemetry payload structure matches expectations"""
    sample_payload = '{"device_id": "IOT-001", "co2_level": 950, "air_quality": "SAFE"}'
    data = json.loads(sample_payload)
    
    assert "device_id" in data
    assert "air_quality" in data
    assert data["air_quality"] == "SAFE"
