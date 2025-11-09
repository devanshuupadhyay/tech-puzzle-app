# backend/puzzle_service.py (Pragmatic, Clean Version)

import boto3
from boto3.dynamodb.types import TypeDeserializer
from typing import Dict, Any
import os, json

if os.environ.get("DYNAMODB_ENDPOINT"):
    # Use DynamoDB Local when running SAM locally
    dynamodb_client: Any = boto3.client(  # type: ignore
        "dynamodb", endpoint_url=os.environ.get("DYNAMODB_ENDPOINT")
    )
else:
    dynamodb_client: Any = boto3.client("dynamodb")  # type: ignore

from puzzle_models import PuzzleBlueprint

# Initialize Boto3 clients. Use 'Any' and ignore the dynamic call.
dynamodb_client: Any = boto3.client("dynamodb")  # type: ignore
TABLE_NAME = "TechPuzzleBlueprints"

# FIX: Apply type ignore for the untyped Boto3 utility object.
deserializer = TypeDeserializer()  # type: ignore


def get_puzzle_blueprint(puzzle_id: str) -> PuzzleBlueprint:
    """
    Retrieves, validates (at runtime via Pydantic), and returns a typed object.
    """
    try:
        # Boto3 interaction...
        response = dynamodb_client.get_item(  # Pylance is quiet due to the 'type: ignore' on initialization
            TableName=TABLE_NAME, Key={"PuzzleID": {"S": puzzle_id}}
        )

        item = response.get("Item")

        if not item:
            raise ValueError(f"Puzzle with ID '{puzzle_id}' not found.")

        # Convert DynamoDB format to standard Python dictionary
        python_item: Dict[str, Any] = {
            k: deserializer.deserialize(v) for k, v in item.items()  # type: ignore
        }
        if "CorrectSolution" in python_item and isinstance(
            python_item["CorrectSolution"], str
        ):
            python_item["CorrectSolution"] = json.loads(python_item["CorrectSolution"])

        # CRUCIAL STEP: Instantiate the Pydantic Model.
        # This relies on Pydantic's runtime validation.
        return PuzzleBlueprint(**python_item)  # type: ignore

    except Exception as e:
        # Re-raise or handle, ensuring robust error reporting
        raise e
