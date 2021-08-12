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
    def post_cleaner(cls, input_):
        cleaned_obj = input_.copy()

        def go_deep(input_obj):
            if isinstance(input_obj, dict) and input_obj.get('type') == 'array' and input_obj.get('items', {}).get('anyOf'):
                cleaned_any = cls.clean_up_list(input_obj['items'].get('anyOf', input_obj['items']))
                input_obj['items']['anyOf'] = cleaned_any

                if len(cleaned_any) == 1:
                    input_obj['items'] = cleaned_any[0]

                else:
                    for el in input_obj['items']['anyOf']:
                        if el['type'] == 'object':
                            go_deep(el)

            elif isinstance(input_obj, dict) and input_obj.get('type') == 'object':
                go_deep(input_obj.get('properties'))

            elif isinstance(input_obj, dict):
                for value in input_obj.values():
                    go_deep(value)

        go_deep(cleaned_obj)
        return cleaned_obj

    @staticmethod
    def clean_up_list(in_list: List):

        if not in_list:
            return []

        clear_pull = []

        def go_deep(in_list_local):
            nonlocal clear_pull
            current_list = [in_list_local.pop(0)]
            for el in in_list_local:
                if el != current_list[0]:
                    current_list.append(el)

            if len(current_list) > 1:
                clear_pull.append(current_list.pop(0))
                go_deep(current_list)
            else:
                clear_pull = clear_pull + current_list

        go_deep(in_list.copy())
        return clear_pull

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
    def dict_to_schema(cls, in_dict: dict, use_post_cleaner: bool = True) -> dict:
        """
        Converts python dict to schema of django-json-widget
        :param use_post_cleaner: Apply or not cleaner for to avoid repetition in  anyOf case
            Example:
                {...
                    'items': {'anyOf':
                     [
                     {'type': 'string', 'title': ''},
                     {'type': 'string', 'title': ''}
                     ]
                 ...}
                automatically converts to:
                {...
                    'items':
                     {'type': 'string', 'title': ''},
                 }

        :param in_dict: data to convert
        :
        """
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

        if use_post_cleaner:
            final_schema = cls.post_cleaner(final_schema)

        return final_schema

    @classmethod
    def dict_to_schema_and_save(cls, in_dict: dict, path: str):
        json_ = cls.dict_to_schema(in_dict)
        with open(path, "w") as file:
            json.dump(json_, file, indent=4)
