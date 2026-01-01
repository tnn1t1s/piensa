"""LLM agent for translating Alpaca instruction samples to Hebrew."""

import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

from src.models.alpaca import HebrewAlpacaSample

# Load environment variables from project root
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)

SYSTEM_PROMPT = """You are a professional English-Hebrew translator specializing in instruction-following data for AI training.

Your task is to translate English instruction-response pairs to Hebrew (עברית).

Guidelines:
1. Preserve the meaning and intent of the original exactly
2. Use natural, fluent Hebrew phrasing - not literal word-for-word translation
3. Keep technical terms in English if they are commonly used that way in Hebrew tech/academic contexts
4. Maintain the same level of formality and style as the original
5. For code examples: translate comments to Hebrew but keep code syntax unchanged
6. For lists: maintain the same structure and numbering
7. Use proper Hebrew grammar including gender agreement where applicable

Translate ALL three parts: instruction, input (if present), and output."""


class AlpacaTranslator:
    """Agent that translates English Alpaca samples to Hebrew using an LLM."""

    def __init__(
        self,
        model_name: str = "openai/gpt-4o",
        temperature: float = 0.3
    ):
        """
        Initialize the translator.

        Args:
            model_name: Model to use for translation (via OpenRouter)
            temperature: Temperature for generation (default: 0.3 for some creativity but consistency)
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
            output_type=HebrewAlpacaSample,
            system_prompt=SYSTEM_PROMPT,
        )

    async def translate(
        self,
        instruction: str,
        input_text: str = "",
        output: str = ""
    ) -> HebrewAlpacaSample:
        """
        Translate a single Alpaca sample to Hebrew.

        Args:
            instruction: The English instruction
            input_text: Optional English input context
            output: The English output/response

        Returns:
            HebrewAlpacaSample with translated content
        """
        if input_text:
            prompt = f"""Translate this instruction-response pair to Hebrew:

INSTRUCTION:
{instruction}

INPUT:
{input_text}

OUTPUT:
{output}"""
        else:
            prompt = f"""Translate this instruction-response pair to Hebrew:

INSTRUCTION:
{instruction}

OUTPUT:
{output}"""

        result = await self.agent.run(prompt)
        return result.output

    async def translate_batch(
        self,
        samples: list[dict],
        max_concurrent: int = 5
    ) -> list[HebrewAlpacaSample]:
        """
        Translate multiple samples with concurrency control.

        Args:
            samples: List of dicts with 'instruction', 'input', 'output' keys
            max_concurrent: Maximum concurrent API calls

        Returns:
            List of HebrewAlpacaSample results
        """
        import asyncio
        from asyncio import Semaphore

        semaphore = Semaphore(max_concurrent)

        async def translate_with_semaphore(sample: dict) -> HebrewAlpacaSample:
            async with semaphore:
                return await self.translate(
                    instruction=sample.get("instruction", ""),
                    input_text=sample.get("input", ""),
                    output=sample.get("output", "")
                )

        tasks = [translate_with_semaphore(s) for s in samples]
        return await asyncio.gather(*tasks)
