"""LLM agent for reviewing academic papers."""

import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

# Load environment variables from project root
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)

SYSTEM_PROMPT = """You are an expert academic peer reviewer for machine learning and cognitive science venues (NeurIPS, ICML, CogSci). Your task is to provide constructive, rigorous feedback on research papers.

Review the paper according to these criteria:

1. **Clarity**: Is the writing clear and well-organized? Are claims precise and unambiguous?

2. **Technical Soundness**: Are the methods appropriate? Are there confounds or limitations not addressed?

3. **Novelty**: What is the contribution? Is it clearly stated?

4. **Reproducibility**: Could someone replicate this work from the description?

5. **Scope of Claims**: Do the conclusions follow from the evidence? Are claims appropriately scoped (especially for negative results)?

For each criterion, provide:
- A rating: Strong Accept / Accept / Weak Accept / Borderline / Weak Reject / Reject
- Specific, actionable feedback with line references where possible

End with:
- **Overall Recommendation**: Accept / Revise / Reject
- **Summary**: 2-3 sentence summary of main strengths and weaknesses
- **Top 3 Required Changes**: Specific edits that would improve the paper"""


class PaperReviewer:
    """Agent that reviews academic papers using an LLM."""

    def __init__(
        self,
        model_name: str = "anthropic/claude-sonnet-4",
        temperature: float = 0.3,
        system_prompt: str = SYSTEM_PROMPT
    ):
        """
        Initialize the reviewer.

        Args:
            model_name: Model to use for review (via OpenRouter)
            temperature: Temperature for generation
            system_prompt: System prompt for the reviewer
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
            system_prompt=system_prompt,
        )

    async def review(self, paper_content: str) -> str:
        """
        Review a paper.

        Args:
            paper_content: The full paper text (markdown)

        Returns:
            Review text
        """
        prompt = f"Please review the following academic paper:\n\n{paper_content}"
        result = await self.agent.run(prompt)
        return result.output
