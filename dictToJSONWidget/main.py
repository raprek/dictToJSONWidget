from typing import Union, List
import json
import copy


class DictToSchema:
    dict_template = {
        "type": "object",
        "title": "",
        "properties": {}
    }
    list_template = {
        "type": "array",
        "title": "",
        "items": {}
    }
    str_template = {
        "type": "string",
        "title": ""
    }
    int_template = {
        "type": "number",
        "title": ""
    }
    bool_template = {
        "type": "boolean",
        "title": "",
        'format': 'checkbox'
    }
    none_template = {
        "type": "null",
        "title": ""
    }

    @classmethod
    def get_template(cls, python_type: Union[type]) -> dict:
        """Helps to get template in convenient and safe way"""
        if not isinstance(python_type, type):
            python_type = type(python_type)

        if python_type is dict:
            return copy.deepcopy(cls.dict_template.copy())

        if python_type is list:
            return copy.deepcopy(cls.list_template.copy())

        if python_type is str:
            return copy.deepcopy(cls.str_template.copy())

        if python_type is int:
            return copy.deepcopy(cls.int_template.copy())

        if python_type is bool:
            return copy.deepcopy(cls.bool_template.copy())

        if issubclass(python_type, type(None)):
            return copy.deepcopy(cls.none_template.copy())

        assert False, f"Type was not found: {python_type}"

    @staticmethod
    def update_or_append(input_el: Union[dict, List], to_add) -> None:
        """Add element to list or dict"""
        if isinstance(input_el, dict):
            input_el.update(to_add)
        else:
            input_el.append(to_add)

    @classmethod
    def dict_to_schema(cls, in_dict: dict) -> dict:
        """Converts python dict to schema of django-json-widget"""
        final_schema = {}

        def make_down_step(non_decoded, current_dict) -> None:

            if isinstance(non_decoded, dict):
                template_temp = cls.get_template(dict)

                cls.update_or_append(current_dict, template_temp)
                for key, value in non_decoded.items():
                    to_ad_el = current_dict if isinstance(current_dict, dict) else current_dict[-1]
                    to_ad_el["properties"].update({key: {}})
                    make_down_step(non_decoded[key], to_ad_el["properties"][key])

            if isinstance(non_decoded, list):
                template_temp = cls.get_template(list)
                cls.update_or_append(current_dict, template_temp)
                to_ad_el = current_dict if isinstance(current_dict, dict) else current_dict[-1]

                if len(non_decoded) == 1:
                    make_down_step(non_decoded[0], to_ad_el["items"])

                elif len(non_decoded) > 1:
                    cls.update_or_append(to_ad_el["items"], {"anyOf": []})
                    to_ad_el = current_dict if isinstance(current_dict, dict) else current_dict[-1]
                    for el in non_decoded:
                        make_down_step(el, to_ad_el["items"]["anyOf"])


            if isinstance(non_decoded, (str, bool, int, type(None))) \
                    or (isinstance(non_decoded, type) and issubclass(non_decoded, (str, bool, int))):
                template_temp = cls.get_template(non_decoded)
                cls.update_or_append(current_dict, template_temp)

        make_down_step(in_dict, final_schema)

        return final_schema

    @classmethod
    def dict_to_schema_and_save(cls, in_dict: dict, path: str):
        json_ = cls.dict_to_schema(in_dict)
        with open(path, "w") as file:
            json.dump(json_, file, indent=4)


