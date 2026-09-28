import re
from typing import List, Dict

class TransactionUtils:
    @staticmethod
    def clean_currency_string(amount_text: str) -> float:
        """
        Cleans currency string:
        - Normalizes Unicode dashes/hyphens
        - Removes commas, letters, currency codes
        - Preserves standard decimal floats
        """
        # Normalize non-breaking spaces and dash variations
        normalized = (
            amount_text.replace("\xa0", " ")
            .replace(",", "")  # Remove comma thousands separator (CRUCIAL)
            .replace("–", "-")
            .replace("—", "-")
            .replace("−", "-")
            .strip()
        )

        is_negative = "-" in normalized

        # Extract only digits and decimal point
        digits = re.findall(r"\d+\.?\d*", normalized)
        if not digits:
            return 0.0

        val = float(digits[0])
        return -val if is_negative else val

    @classmethod
    def categorize_transactions(cls, raw_amounts: List[str]) -> Dict[str, float]:
        total_spent = 0.0
        total_earned = 0.0

        for raw_val in raw_amounts:
            val = cls.clean_currency_string(raw_val)
            if val < 0:
                total_spent += abs(val)
            else:
                total_earned += abs(val)

        return {
            "total_spent": round(total_spent, 2),
            "total_earned": round(total_earned, 2),
            "net_flow": round(total_earned - total_spent, 2)
        }