#!/usr/bin/env python3
"""
Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.

Permission is hereby granted, free of charge, to any person obtaining a copy of this
software and associated documentation files (the "Software"), to deal in the Software
without restriction, including without limitation the rights to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


import argparse
import json
import cfn_flip


def get_functions(template):
    """
    Extracts functions and environment variables from a template

    This returns a dict with the function name as the key and a list of variable names
    as value.
    """

    # Extract variables from the Globals section
    try:
        global_variables = list(template["Globals"]["Function"]["Environment"]["Variables"].keys())
    except KeyError:
        global_variables = []

    # Extract functions in the Resources section
    functions = {}

    for name, resource in template.get("Resources", {}).items():
        if resource.get("Type", "") != "AWS::Serverless::Function":
            continue

        try:
            local_variables = list(resource["Properties"]["Environment"]["Variables"].keys())
        except KeyError:
            local_variables = []

        # Don't add functions without environment variables
        if local_variables or global_variables:
            functions[name] = global_variables + local_variables

    return functions


def parse_vars(vars):
    """
    Transform a list of NAME=value environment variables into a dict
    """

    retval = {}

    for var in vars:
        key, value = var.split("=", 1)
        retval[key] = value

    return retval


parser = argparse.ArgumentParser()
parser.add_argument("--template", help="Template file", default="template.yml")
parser.add_argument("vars", nargs="*")


if __name__ == "__main__":
    args = parser.parse_args()

    with open(args.template, "r") as template_file:
        template_data = template_file.read()

    template = json.loads(cfn_flip.to_json(template_data))

    functions = get_functions(template)

    vars = parse_vars(args.vars)

    output = {}
    for name, function_vars in functions.items():
        function_output = {}
        for function_var in function_vars:
            function_output[function_var] = vars.get(function_var, "")

        output[name] = function_output

    print(json.dumps(output, indent=2))
