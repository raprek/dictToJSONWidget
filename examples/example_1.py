import sys
import json
sys.path.append("../")

from src.main import DictToSchema

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
    json_ = DictToSchema.dict_to_schema(test_json)
    print(DictToSchema.dict_to_schema(test_json))
    with open("test.json", "w") as file:
        json.dump(json_, file, indent=4, sort_keys=True)

