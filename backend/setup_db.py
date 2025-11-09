import boto3

# Initialize the DynamoDB resource (Resource is easier for table operations)
dynamodb = boto3.resource("dynamodb")  # type: ignore


def create_blueprints_table():
    print("Attempting to create DynamoDB table: TechPuzzleBlueprints...")
    try:
        table = dynamodb.create_table(  # type: ignore
            TableName="TechPuzzleBlueprints",
            KeySchema=[{"AttributeName": "PuzzleID", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "PuzzleID", "AttributeType": "S"}],
            # Using PAY_PER_REQUEST for cost efficiency in the free tier
            BillingMode="PAY_PER_REQUEST",
        )
        table.wait_until_exists()  # type: ignore
        print(f"Table {table.name} created successfully.")  # type: ignore
    except Exception as e:
        # Check if the table already exists, which is not an error for us
        if "Table already exists" in str(e):
            print("Table TechPuzzleBlueprints already exists. Skipping creation.")
        else:
            print(f"Error creating table: {e}")


if __name__ == "__main__":
    create_blueprints_table()
