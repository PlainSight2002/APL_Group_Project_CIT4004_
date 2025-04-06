'''
Authors
Sassania Hibbert 1901201
Darrell King 1803342
Shavar Mclean 1903893
Mark Vernon 1908916
Jelani Jackson 1901811
'''

from symbol_table import *
from app_parser import parser
from code_generator import generate_code
from semantic_analyzer import semantic_analyzer


def main():
    # Get the source code
    from sourcecode import code as written_source_code

    # Create a global symbol table
    global_symbol_table = SymbolTable()

    print("*" * 50)
    print("Parsing the source code:")
    ast = parser.parse(written_source_code)
    print(ast)
    print("*" * 50)

    # Semantic Analysis
    print("*" * 50)
    print("Performing Semantic Analysis:")
    semantic_analyzer(ast, global_symbol_table)
    print("*" * 50)

    # Interpreter Code Generation
    print("*" * 50)
    print("Generating Python code:")

    code_header = "import code_handler as handler\n\n"
    python_code = code_header + generate_code(ast)
    # print(python_code)

    print("*" * 50)
    exec(python_code)


if __name__ == "__main__":
    main()
