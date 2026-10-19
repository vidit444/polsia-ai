def calculate_lead_score(customer_name: str, industry: str | None, source: str | None) -> int:
    score = 10
    if len(customer_name) > 8:
        score += 10
    if industry:
        high_value = {"saas", "finance", "healthcare", "ecommerce", "manufacturing"}
        if industry.lower() in high_value:
            score += 35
    if source:
        source_weights = {"referral": 25, "organic": 20, "campaign": 15, "partner": 18}
        score += source_weights.get(source.lower(), 5)
    return min(score, 100)
