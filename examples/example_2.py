import sys
import json
sys.path.append("../")

from src.main import DictToSchema

if __name__ == "__main__":
    test_json = {
        "key_1": [str, None, True, [{"key_1_1": [str, None, True, []]}]],
        "key_2": {
            "key_2_2": ""
        }
    }
    json_ = DictToSchema.dict_to_schema(test_json)
    print(DictToSchema.dict_to_schema(test_json))
    with open("test.json", "w") as file:
        json.dump(json_, file, indent=4)

