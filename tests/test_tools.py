
from app.tools import password_hash_config_checker


def test_bcrypt_valid_configuration_passes():
    config = {
        "algorithm": "bcrypt",
        "work_factor": 12,
        "max_password_bytes": 72
    }

    result = password_hash_config_checker(config)

    assert result["status"] == "PASS"


def test_bcrypt_weak_work_factor_fails():
    config = {
        "algorithm": "bcrypt",
        "work_factor": 8,
        "max_password_bytes": 72
    }

    result = password_hash_config_checker(config)

    assert result["status"] == "FAIL"


def test_unsupported_algorithm_fails():
    config = {
        "algorithm": "md5"
    }

    result = password_hash_config_checker(config)

    assert result["status"] == "FAIL"
    assert result["rules"] == []


def test_missing_bcrypt_configuration_fails():
    config = {
        "algorithm": "bcrypt"
    }

    result = password_hash_config_checker(config)

    assert result["status"] == "FAIL"
    assert len(result["rules"]) == 2
