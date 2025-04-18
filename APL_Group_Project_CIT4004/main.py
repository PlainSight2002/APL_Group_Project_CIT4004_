'''
Authors
Sassania Hibbert 1901201
Darrell King 1803342
Shavar Mclean 1903893
Mark Vernon 1908916
Jelani Jackson 1901811
'''

from flask import Flask, request, jsonify
from symbol_table import *
from app_parser import parser
from semantic_analyzer import semantic_analyzer
from code_generator import generate_code
import io, sys
from flask_cors import CORS

# TODO: Add arithmetic operations to the language (Done)
# TODO: Make sure you can assign a variable to another variable (Done)
# TODO: Add conditionals to the language (DONE)
# TODO: Add scope and binding to the language (Done)
# TODO: Add params and args to the language (Done)
# TODO: Finish the code generator (Done)
# TODO: Finish the server backend (Done)


app = Flask(__name__)
allowed_origins = [
    "https://apl-cit-4004-web-ui.vercel.app",
    "https://apl-web-ui.vercel.app",
    "*",
]
CORS(app, origins=allowed_origins)
printed_output = ""


@app.route("/generate_code", methods=["POST"])
def parse_code():
    global_symbol_table = SymbolTable()
    input_code = request.json.get("code")
    print(input_code)
    # Parse the input code
    try:
        ast = parser.parse(input_code)
    except Exception as e:
        response = {"error": str(e)}
        return jsonify(response)

    try:
        # Perform Semantic Analysis
        semantic_analyzer(ast, global_symbol_table)
    except Exception as e:
        response = {"error": str(e)}
        return jsonify(response)
    # Generate Python code
    compiled_python_code = generate_code(ast)

    output = io.StringIO()
    sys.stdout = output
    # Execute the generated Python code
    exec(compiled_python_code)
    sys.stdout = sys.__stdout__
    printed_output = output.getvalue()
    # Return the printed output from the executed Python code
    response = {"python_code": printed_output}
    return jsonify(response)


@app.route("/test", methods=["GET"])
def test():
    return jsonify({"message": "Hello, World!"})


# Get the output from the compiled Python code
@app.route("/get_output", methods=["GET"])
def get_output():
    if not printed_output:
        response = {"output": "No output to display."}
        return jsonify(response)
    response = {"output": printed_output}
    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
