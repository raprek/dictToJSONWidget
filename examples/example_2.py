import sys
import json
sys.path.append("../")

from dictToJSONWidget import DictToSchema

if __name__ == "__main__":
    test_json = {
        "key_1": [str, None, True, [{"key_1_1": [str, None, True, []]}]],
        "key_2": {
            "key_2_2": ""
        }
    }
    DictToSchema.dict_to_schema_and_save(test_json, 'example_2.json')
