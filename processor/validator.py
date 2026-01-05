from pydantic import create_model, ValidationError
from typing import Any, List, Dict

def validate_dataset(data: List[Dict[str, Any]], expected_fields: List[str]):
    """
    Dynamically creates a model to validate the AI output.
    """
    # Create a dynamic Pydantic model based on the user's requested fields
    DynamicModel = create_model('DatasetItem', **{field: (Any, ...) for field in expected_fields})
    
    valid_records = []
    errors = []

    for i, record in enumerate(data):
        try:
            valid_records.append(DynamicModel(**record).dict())
        except ValidationError as e:
            errors.append({"index": i, "error": str(e)})
            
    return valid_records, errors