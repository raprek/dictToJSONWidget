import sys
import json
sys.path.append("../")

from dictToJSONWidget import DictToSchema

if __name__ == "__main__":
    test_json = {
        'test_of_combine': [
            {
                "test_el_1": [
                    "1",
                    None,
                    3
                ],
            },
            {
                "test_el_2": [
                    {
                        "test_el_5": ["5"],
                        "test_rl_3": None
                    }
                ]
            }
        ],
        'just_test': [
            'test'
        ]
    }
    DictToSchema.dict_to_schema_and_save(test_json, 'example_1.json')

