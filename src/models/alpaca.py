"""Pydantic models for Alpaca instruction data."""

from pydantic import BaseModel, Field


class AlpacaSample(BaseModel):
    """An English Alpaca instruction-response sample."""
    instruction: str = Field(description="The instruction/task description")
    input: str = Field(default="", description="Optional input context")
    output: str = Field(description="The expected response/output")


class HebrewAlpacaSample(BaseModel):
    """A Hebrew translation of an Alpaca instruction-response sample."""
    instruction_he: str = Field(description="Hebrew translation of the instruction")
    input_he: str = Field(default="", description="Hebrew translation of the input (if any)")
    output_he: str = Field(description="Hebrew translation of the output")


class TranslatedAlpacaSample(BaseModel):
    """Full record of a translated sample with original for reference."""
    # Original English
    instruction_en: str
    input_en: str = ""
    output_en: str
    # Hebrew translation
    instruction_he: str
    input_he: str = ""
    output_he: str

    def to_training_text(self) -> str:
        """Format as training text in Hebrew Alpaca style."""
        if self.input_he:
            return f"""להלן הוראה המתארת משימה, יחד עם קלט המספק הקשר נוסף. כתוב תגובה המשלימה את הבקשה בצורה מתאימה.

### הוראה:
{self.instruction_he}

### קלט:
{self.input_he}

### תגובה:
{self.output_he}"""
        else:
            return f"""להלן הוראה המתארת משימה. כתוב תגובה המשלימה את הבקשה בצורה מתאימה.

### הוראה:
{self.instruction_he}

### תגובה:
{self.output_he}"""
