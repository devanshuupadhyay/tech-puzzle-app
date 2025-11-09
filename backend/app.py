# backend/app.py (The Thin Controller/Handler)

import json
from typing import Dict, Any

# Import our service layer and model
import puzzle_service
from puzzle_models import PuzzleBlueprint
from pydantic import ValidationError

# Pydantic's ValidationError is critical for input validation
from pydantic import ValidationError


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    API Gateway Handler: Routes the request and maps service layer output to HTTP responses.
    """
    try:
        # 1. Parameter Extraction: Get ID from the URL path
        puzzle_id = event.get("pathParameters", {}).get("puzzleId")

        if not puzzle_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "PuzzleID is required in the path."}),
            }

        # 2. CALL THE SERVICE LAYER (Business Logic)
        # This returns a Pydantic object (PuzzleBlueprint)
        puzzle_blueprint: PuzzleBlueprint = puzzle_service.get_puzzle_blueprint(
            puzzle_id
        )

        # 3. Success Response: Pydantic's built-in .model_dump() method converts
        # the object to a dictionary that can be safely serialized to JSON.
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",  # Required for Next.js/Vue.js frontend
            },
            "body": json.dumps(puzzle_blueprint.model_dump()),
        }

    except ValueError as ve:
        # Handles the 'Puzzle not found' exception raised by puzzle_service.py
        return {"statusCode": 404, "body": json.dumps({"error": str(ve)})}
    except Exception as e:
        # Handles all other unexpected runtime errors (e.g., DynamoDB connectivity issues)
        print(f"Internal server error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps(
                {"error": "An unexpected error occurred processing the puzzle request."}
            ),
        }
