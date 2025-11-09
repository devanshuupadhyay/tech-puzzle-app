# backend/puzzle_models.py (Updated for Pydantic)

from pydantic import BaseModel, Field
from typing import List, Dict, Any


# Define the model for the data coming OUT of DynamoDB
class PuzzleBlueprint(BaseModel):
    """
    Model for the blueprint data fetched from the Data Tier.
    Pydantic handles automatic type enforcement and serialization.
    """

    PuzzleID: str
    Title: str
    BlueprintURL: str  # S3 Link to the puzzle image
    Difficulty: str
    Tags: List[str]
    CorrectSolution: Dict[str, Any]


# --- New Model for the User's SUBMISSION (Input Validation) ---


class UserSolutionSubmission(BaseModel):
    """
    Model for the JSON body submitted by the Next.js front-end
    when a user tries to solve a puzzle. This ensures we reject bad data early.
    """

    PuzzleID: str = Field(min_length=1)
    # The user's solution is a list of their placement choices
    UserPlacements: List[Dict[str, Any]]
    UserID: str  # This will come from AWS Cognito
