# dictToJSONWidget
The util helping to avoid annoying handwork of data transformation into json scheme for JSONEditorWidget
## INSTALL
```
pip install git+https://github.com/raprek/dictToJSONWidget.git
```
## Possible type specification
For primitive types you can use both instances of classes as 
<b>"any-text", 12, True/False, None</b> and python class notations as
<b>str, int, bool, None</b>.

### Note
Be cautious with case of using array/list in pseudo schema(input). Every element in
array(list) pseudo schema is considered as different types in final schema. Thus, if you have
an array of same type just use <b>{ "some_key" : [""] or [str] } </b> syntax. (Check examples)

## Usage / Examples:

```
from dictToJSONWidget import DictToSchema

test_json = {
        "key_1": [str, None, True],
        "key_2": {
            "key_2_2": "text"
        }
    }
    
json_ = DictToSchema.dict_to_schema(test_json)

# convert and save
# DictToSchema.dict_to_schema_and_save(json_, 'json_out.json')

```

### JSON OUT
```
{
    "type": "object",
    "title": "",
    "properties": {
        "key_1": {
            "type": "array",
            "title": "",
            "items": {
                "anyOf": [
                    {
                        "type": "string",
                        "title": ""
                    },
                    {
                        "type": "null",
                        "title": ""
                    },
                    {
                        "type": "boolean",
                        "title": "",
                        "format": "checkbox"
                    }
                ]
            }
        },
        "key_2": {
            "type": "object",
            "title": "",
            "properties": {
                "key_2_2": {
                    "type": "string",
                    "title": ""
                }
            }
        }
    }
}

```
