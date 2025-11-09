import boto3
import json
from typing import Any

# Initialize Boto3 client using the preferred 'Any' type hint
dynamodb_client: Any = boto3.client("dynamodb")  # type: ignore
TABLE_NAME = "TechPuzzleBlueprints"

# A sample puzzle blueprint for testing our retrieval logic
SAMPLE_PUZZLE = {
    "PuzzleID": "ARCH001",
    "Title": "Basic Serverless Website",
    "BlueprintURL": "/assets/blueprints/arch001.png",
    "Difficulty": "Beginner",
    "Tags": ["S3", "CloudFront", "Networking", "Vue.js"],
    "CorrectSolution": {
        "element_1": {"type": "S3", "position": [100, 200]},
        "element_2": {"type": "CloudFront", "position": [300, 100]},
        "element_3": {"type": "Route53", "position": [450, 200]},
    },
}


def seed_single_puzzle(puzzle_data: dict):
    """
    Puts an item into the DynamoDB table using Boto3 Client's put_item.
    """
    print(f"Attempting to seed puzzle: {puzzle_data['PuzzleID']}...")

    # Architectural Note: DynamoDB Client requires the attribute values
    # to be explicitly typed (S for String, SS for String Set, etc.)
    item_to_put = {
        "PuzzleID": {"S": puzzle_data["PuzzleID"]},
        "Title": {"S": puzzle_data["Title"]},
        "BlueprintURL": {"S": puzzle_data["BlueprintURL"]},
        "Difficulty": {"S": puzzle_data["Difficulty"]},
        "Tags": {"SS": puzzle_data["Tags"]},
        # Store the complex solution structure as a JSON string to keep the item simple
        "CorrectSolution": {"S": json.dumps(puzzle_data["CorrectSolution"])},
    }

    try:
        dynamodb_client.put_item(TableName=TABLE_NAME, Item=item_to_put)
        print("Seeding successful!")
    except Exception as e:
        print(f"Error during seeding: {e}")


if __name__ == "__main__":
    seed_single_puzzle(SAMPLE_PUZZLE)
