"""Test the LLM judge choice extractor on sample responses."""

import asyncio
from src.agents.choice_extractor import ChoiceExtractor


# Sample responses from actual experiment runs
TEST_CASES = [
    # Clear A choices
    ("A", "en", "A"),
    ("Para maximizar el número de vidas salvadas, elijo A", "es", "A"),
    ("A (בחירה בתרופה)", "he", "A"),

    # Clear B choices
    ("B", "en", "B"),
    ("'B' is chosen because the expected value calculation favors it", "en", "B"),
    ("B (תרופה ב)", "he", "B"),

    # Embedded in explanation
    ("Given the information provided, choosing Medicine A guarantees saving 200,000 lives", "en", "A"),
    ("To minimize the potential loss, I would select option B for the gamble", "en", "B"),
    ("En este caso, el Medicamento A es la mejor opción", "es", "A"),

    # Unclear/ambiguous
    ("This is a classic problem in decision theory", "en", "unclear"),
    ("Sin saber la probabilidad exacta, no puedo decidir", "es", "unclear"),

    # Hebrew responses
    ("A (choosing treatment A saves 200,000)", "he", "A"),
    ("B (יש סיכוי של 33%)", "he", "B"),
]


async def main():
    print("Testing ChoiceExtractor with sample responses...\n")

    extractor = ChoiceExtractor(model_name="openai/gpt-4-turbo")

    correct = 0
    total = len(TEST_CASES)

    for response, lang, expected in TEST_CASES:
        result = await extractor.extract(response, lang)

        is_correct = result.choice.value == expected
        correct += int(is_correct)

        status = "✓" if is_correct else "✗"
        print(f"{status} [{lang}] Expected: {expected}, Got: {result.choice.value}")
        print(f"   Response: {response[:50]}...")
        print(f"   Confidence: {result.confidence:.2f}")
        print(f"   Reasoning: {result.reasoning}")
        print()

    print(f"\nAccuracy: {correct}/{total} ({100*correct/total:.1f}%)")


if __name__ == "__main__":
    asyncio.run(main())
