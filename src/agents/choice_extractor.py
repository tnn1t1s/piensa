"""LLM judge for extracting choices from Asian Disease Problem responses."""

import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

from src.models.choice import ChoiceExtraction

# Load environment variables from project root
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)

SYSTEM_PROMPT = """You are extracting the choice (A or B) from a response to the Asian Disease Problem.

The Asian Disease Problem asks participants to choose between:
- Option A: A certain/sure outcome (e.g., "200,000 people will be saved" or "400,000 will die")
- Option B: A risky gamble (e.g., "33% chance all saved, 67% chance none saved")

The response may be in ANY language (English, Spanish, Hebrew, Arabic, Chinese, etc.).

Look for:
1. Explicit letter choice: "A", "B", "Medicamento A", "תרופה B", etc.
2. Ordinal references: "first option", "segunda opción", "האפשרות הראשונה"
3. Semantic content: preference for "certain/sure" (= A) vs "gamble/chance" (= B)
4. The answer may be embedded in explanation text

Classification rules:
- A: Response clearly indicates Option A (sure/certain outcome)
- B: Response clearly indicates Option B (risky/probabilistic outcome)
- unclear: Response is ambiguous, discusses both without choosing, or is incoherent
- refused: Model explicitly refuses to answer or says it cannot/should not choose

Be generous in interpretation. If the response leans toward one option, extract that choice.
Only mark "unclear" if genuinely ambiguous or incoherent."""


class ChoiceExtractor:
    """Agent that extracts A/B choice from model responses using an LLM judge."""

    def __init__(
        self,
        model_name: str = "openai/gpt-4-turbo",
        temperature: float = 0.0
    ):
        """
        Initialize the choice extractor.

        Args:
            model_name: Model to use for extraction (via OpenRouter)
            temperature: Temperature for extraction (default: 0.0 for determinism)
        """
        self.model_name = model_name
        self.temperature = temperature

        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENROUTER_API_KEY environment variable is not set. "
                "Please copy .env.example to .env and add your API key."
            )

        self.model = OpenAIModel(
            model_name,
            provider='openrouter',
        )

        self.agent = Agent(
            self.model,
            output_type=ChoiceExtraction,
            system_prompt=SYSTEM_PROMPT,
        )

    async def extract(self, response: str, prompt_language: str = "unknown") -> ChoiceExtraction:
        """
        Extract choice from a single response.

        Args:
            response: The model's response text
            prompt_language: Language code (en, es, he, etc.) for context

        Returns:
            ChoiceExtraction with choice, confidence, and reasoning
        """
        prompt = f"Language: {prompt_language}\n\nResponse to extract from:\n{response}"
        result = await self.agent.run(prompt)
        return result.output

    async def extract_batch(
        self,
        responses: list[str],
        prompt_language: str = "unknown"
    ) -> list[ChoiceExtraction]:
        """
        Extract choices from multiple responses.

        Args:
            responses: List of response texts
            prompt_language: Language code for all responses

        Returns:
            List of ChoiceExtraction results
        """
        import asyncio
        tasks = [self.extract(r, prompt_language) for r in responses]
        return await asyncio.gather(*tasks)
