"""Pydantic AI agent for generating presentation visuals using Gemini."""

import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables from project root
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)

# System prompt for arxiv-quality figure generation
FIGURE_SYSTEM_PROMPT = """You are creating a figure for an arxiv paper from a top AI lab (DeepMind, Anthropic, OpenAI).

STRICT REQUIREMENTS:
- Vector-style diagram with CLEAN LINES only
- NO photorealistic elements, NO 3D renders, NO gradients
- Flat colors only: white background, black lines, 2-3 accent colors max
- ALL TEXT must be CRISP, READABLE, properly spelled
- Use standard academic fonts (sans-serif like Helvetica/Arial)
- Simple geometric shapes: rectangles, circles, arrows
- NO decorative elements, NO shadows, NO glows
- Think: LaTeX/TikZ diagram or matplotlib figure aesthetic

FORBIDDEN:
- Blurry or illegible text
- Photorealistic imagery
- Complex gradients or 3D effects
- Clip art or stock imagery style
- Busy backgrounds
- Decorative flourishes

Reference style: Figures from "Attention Is All You Need", "BERT", "GPT-4 Technical Report".
Output: Clean, minimal, publication-ready scientific diagram."""


class VisualPrompt(BaseModel):
    """A prompt for generating a presentation visual."""
    name: str
    prompt: str
    aspect_ratio: str = "16:9"


# Arxiv-quality figure prompts for FLE paper presentation
FLE_VISUALS = [
    VisualPrompt(
        name="01_fle_concept",
        prompt="""Scientific diagram: The Foreign Language Effect (FLE) in cognitive processing.

Central element: stylized brain or dual-process icon
Left side labeled "L1 (Native)": warm accent color (coral/orange), icons suggesting automatic/emotional processing
Right side labeled "L2 (Foreign)": cool accent color (teal/blue), icons suggesting deliberate/analytical processing

Arrow or gradient showing the switch between processing modes.
Clean white background, thin precise lines, Nature/Science figure quality.
Subtle grid or alignment guides visible in composition."""
    ),
    VisualPrompt(
        name="02_lora_architecture",
        prompt="""Technical architecture diagram: LoRA (Low-Rank Adaptation) for language models.

Show transformer blocks as stacked rectangles in neutral gray (frozen weights).
Small colored modules (blue/green) attached to attention layers representing LoRA adapters.
Arrows showing forward pass flow.
Labels: "Frozen Base Model (7B params)" and "LoRA Adapter (~4M params)"

Style: similar to figures in "LoRA: Low-Rank Adaptation" paper or Anthropic technical reports.
Clean vector style, white background, precise alignment."""
    ),
    VisualPrompt(
        name="03_framing_effect",
        prompt="""Behavioral economics diagram: The Framing Effect in decision-making.

Split panel visualization:
Left (gain frame): abstract representation of "200,000 saved" with green/positive visual weight, showing risk-averse choice
Right (loss frame): abstract representation of "400,000 die" with red/negative visual weight, showing risk-seeking choice

Use abstract shapes or simple icons, NOT realistic people or medical imagery.
Kahneman & Tversky style conceptual diagram.
Clean academic aesthetic, white background."""
    ),
    VisualPrompt(
        name="04_results_heatmap",
        prompt="""Data visualization: 4x4 experimental results matrix.

Heatmap grid showing framing effect magnitude (Δ) across conditions:
- Rows: Adapter language (EN, ES, HE, ZH)
- Columns: Prompt language (EN, ES, HE, ZH)
- Color intensity: light (weak effect) to dark blue/purple (strong effect)
- Diagonal cells (matched conditions) with subtle border highlight

Include color scale legend. Clean data viz style like Seaborn/matplotlib academic figures.
White background, clear axis labels, publication-ready."""
    ),
    VisualPrompt(
        name="05_instruction_collapse",
        prompt="""Abstract visualization: Instruction-following degradation in language models.

Left side: structured, aligned text blocks or tokens (representing coherent responses)
Right side: same elements fragmenting, scattering, dissolving into noise/entropy

Gradient transition from order to disorder, left to right.
Color: grayscale with subtle red accent on the degraded side.
Conceptual diagram style, like figures in alignment or interpretability papers.
White background, clean composition."""
    ),
]


class SlideVisualGenerator:
    """Agent that generates presentation visuals using Gemini 3 image generation."""

    def __init__(self):
        """Initialize the visual generator with Gemini."""
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable is not set. "
                "Get one from https://aistudio.google.com and add to .env"
            )
        self.api_key = api_key

        # Use google-genai SDK directly for reliable image generation
        from google import genai
        self.client = genai.Client(api_key=api_key)

    async def generate_visual(
        self,
        prompt: str,
        output_path: Path,
        aspect_ratio: str = "16:9"
    ) -> Path:
        """
        Generate a single visual and save to file.

        Args:
            prompt: Description of the visual to generate
            output_path: Where to save the image
            aspect_ratio: Image aspect ratio (16:9, 4:3, 1:1, etc.)

        Returns:
            Path to the saved image
        """
        from google.genai import types

        # Combine system context with specific prompt
        full_prompt = f"{FIGURE_SYSTEM_PROMPT}\n\n{prompt}\n\nGenerate this as a publication-ready figure."

        # Generate image using Gemini 3 Pro Image
        response = self.client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=full_prompt,
            config=types.GenerateContentConfig(
                response_modalities=["image", "text"],
            ),
        )

        # Extract and save the image
        output_path.parent.mkdir(parents=True, exist_ok=True)

        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                with open(output_path, 'wb') as f:
                    f.write(part.inline_data.data)
                return output_path

        raise ValueError("No image generated in response")

    async def generate_all_visuals(self, output_dir: Path) -> list[Path]:
        """
        Generate all FLE presentation visuals.

        Args:
            output_dir: Directory to save images

        Returns:
            List of paths to generated images
        """
        output_dir.mkdir(parents=True, exist_ok=True)

        results = []
        for visual in FLE_VISUALS:
            output_path = output_dir / f"{visual.name}.png"
            print(f"Generating: {visual.name}...")

            try:
                path = await self.generate_visual(
                    visual.prompt,
                    output_path,
                    visual.aspect_ratio
                )
                results.append(path)
                print(f"  Saved: {path}")
            except Exception as e:
                print(f"  Error: {e}")

        return results


async def main():
    """Generate all visuals for the FLE presentation."""
    # Output to slides/public/images/
    output_dir = Path(__file__).parent.parent.parent / "papers" / "001-fle-lora" / "slides" / "public" / "images"

    generator = SlideVisualGenerator()
    paths = await generator.generate_all_visuals(output_dir)

    print(f"\nGenerated {len(paths)} visuals in {output_dir}")


if __name__ == "__main__":
    asyncio.run(main())
