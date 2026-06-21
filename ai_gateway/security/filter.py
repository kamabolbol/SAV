SENSITIVE_WORDS = ["salaire", "mot de passe", "password", "compte bancaire", "RIB", "carte bleue", "secret"]
INJECTION_PATTERNS = ["ignore", "drop", "reset", "system", "command", "exec", "eval"]

def security_check(text: str) -> bool:
    text_lower = text.lower()
    for word in SENSITIVE_WORDS:
        if word in text_lower:
            return False
    for pattern in INJECTION_PATTERNS:
        if pattern in text_lower:
            return False
    return True
