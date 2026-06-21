def build_context(context_dict: dict, user_id: int = 0) -> dict:
    enriched = context_dict.copy()
    enriched["user_id"] = user_id
    return enriched
