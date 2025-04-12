from typing import List, Optional

from langchain_core.pydantic_v1 import BaseModel, Field


class Person(BaseModel):
    """Information about a person."""

    # ^ Doc-string for the entity Person.
    # This doc-string is sent to the LLM as the description of the schema Person,
    # and it can help to improve extraction results.

    # Note that:
    # 1. Each field is an `optional` -- this allows the model to decline to extract it!
    # 2. Each field has a `description` -- this description is used by the LLM.
    # Having a good description can help improve extraction results.
    name: Optional[str] = Field(..., description="The name of the person")
    hair_color: Optional[str] = Field(
        ..., description="The color of the peron's hair if known"
    )
    height_in_meters: Optional[str] = Field(
        ..., description="Height measured in meters"
    )


class Data(BaseModel):
    """Extracted data about people."""

    # Creates a model so that we can extract multiple entities.
    people: List[Person]


class CodeBlock(BaseModel):
    """A code block."""

    language: Optional[str] = Field(
        ..., description="The language of the code block. If unknown, use 'Generic'"
    )
    isCamelCase: Optional[bool] = Field(
        ..., description="Whether the code block is in camel case or not"
    )
    reason: Optional[str] = Field(
        ...,
        description="The reason why the code block is or isn't in camel case. POinting out the specific parts of the code block that make it camel case or not.",
    )


class ListOfCodeBlocks(BaseModel):
    """A list of code blocks."""

    code_blocks: List[CodeBlock]
