import contextlib
import json
import os
import os.path
import pprint
import sys

import jsonschema.exceptions
import openapi_spec_validator as validator
import yaml


def check_specs():
    def try_load_yaml(filename):
        with open(filename, 'r') as yaml_input:
            try:
                yaml.safe_load(yaml_input.read())
            except Exception:
                print("Error while processing file: {0}".format(filename))
                raise

    def try_load_json(filename):
        try:
            json.load(filename)
        except Exception:
            print("Error while processing file: {0}".format(filename))
            raise

    for root, dirs, files in os.walk(os.getcwd()):
        for filename in files:
            fq_filename = "{0}/{1}".format(root, filename)
            if filename.endswith('.yml') or filename.endswith('.yaml'):
                try_load_yaml(fq_filename)

            elif filename.endswith('.json'):
                try_load_json(fq_filename)


def validate():
    potential_spec_filenames = [
        'openapi.json',
        'openapi.yaml',
        'openapi.yml'
    ]
    for root_filename in potential_spec_filenames:
        print("Checking for {0},,,".format(root_filename), end='')
        if os.path.exists(root_filename):
            print("FOUND")
            spec_url = 'file://{0}/{1}'.format(
                os.getcwd(),
                root_filename
            )

            try:
                print("Attempting to validate...", end='')
                validator.validate_spec_url(
                    spec_url
                )
            except (jsonschema.exceptions.ValidationError, jsonschema.exceptions.SchemaError) as error:
                print("ERROR")
                print("Validation Error")
                print("    Validator: {0}".format(error.validator))
                print("    Message:")
                print("        {0}".format(error.message))
                print("    Error in:")
                for entry in error.validator_value:
                    print("        {0}".format(entry))
                print("    Schema error was in: {0}".format(error.schema))
                print("    Relative Path: {0}".format(error.relative_path))
                print("    Absolute Path: {0}".format(error.absolute_path))
                print("    Context:")
                for entry in error.context:
                    print("        {0}".format(entry))
                print("    Instance: {0}".format(error.instance))
                print("    Cause: {0}".format(error.cause))
                sys.exit(1)
            except jsonschema.exceptions.RefResolutionError as error:
                print("ERROR")
                print("Reference Resolution Error - {0}".format(error))
                sys.exit(2)
            else:
                print("VALID")
        else:
            print("NOT FOUND")

if __name__ == "__main__":
    spec_location = os.getcwd()
    print("Spec Location: {0}".format(spec_location))
    check_specs()
    validate()
    sys.exit(0)
