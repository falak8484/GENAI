
# app/tools.py

# OWASP minimum password-hashing requirements
OWASP_MINIMUMS = {
    "argon2id": {
        "memory_mib": 19,
        "iterations": 2
    },
    "bcrypt": {
        "work_factor": 10,
        "max_password_bytes": 72
    },
    "pbkdf2": {
        "iterations": 600000
    }
}


def password_hash_config_checker(config: dict) -> dict:
    """
    Check a password-hashing configuration against
    OWASP minimum requirements.
    """

    algorithm = config.get("algorithm", "").lower()

    if algorithm not in OWASP_MINIMUMS:
        return {
            "algorithm": algorithm,
            "status": "FAIL",
            "message": "Unsupported hashing algorithm.",
            "rules": []
        }

    minimums = OWASP_MINIMUMS[algorithm]
    rules = []

    def check_rule(name, actual, minimum, comparison):
        if actual is None:
            passed = False
            message = "Value is missing."
        else:
            try:
                if comparison == "minimum":
                    passed = actual >= minimum
                    message = (
                        f"{actual} meets the minimum of {minimum}."
                        if passed else
                        f"{actual} is below the minimum of {minimum}."
                    )

                elif comparison == "maximum":
                    passed = actual <= minimum
                    message = (
                        f"{actual} is within the maximum of {minimum}."
                        if passed else
                        f"{actual} exceeds the maximum of {minimum}."
                    )

            except TypeError:
                passed = False
                message = "Invalid value type."

        rules.append({
            "rule": name,
            "actual": actual,
            "required": minimum,
            "status": "PASS" if passed else "FAIL",
            "message": message
        })

    if algorithm == "argon2id":
        check_rule(
            "Memory (MiB)",
            config.get("memory_mib"),
            minimums["memory_mib"],
            "minimum"
        )

        check_rule(
            "Iterations",
            config.get("iterations"),
            minimums["iterations"],
            "minimum"
        )

    elif algorithm == "bcrypt":
        check_rule(
            "Work factor",
            config.get("work_factor"),
            minimums["work_factor"],
            "minimum"
        )

        check_rule(
            "Maximum password bytes",
            config.get("max_password_bytes"),
            minimums["max_password_bytes"],
            "maximum"
        )

    elif algorithm == "pbkdf2":
        check_rule(
            "Iterations",
            config.get("iterations"),
            minimums["iterations"],
            "minimum"
        )

    all_passed = all(rule["status"] == "PASS" for rule in rules)

    return {
        "algorithm": algorithm,
        "status": "PASS" if all_passed else "FAIL",
        "rules": rules
    }
