'''
Authors
Sassania Hibbert 1901201
Darrell King 1803342
Shavar Mclean 1903893
Mark Vernon 1908916
Jelani Jackson 1901811
'''

from symbol_table import *


# Goes through the AST and performs semantic analysis
# The semantic analyzer gets passed the AST and the current scope
def semantic_analyzer(ast, current_scope):
    for x in ast:
        if x[0] == "declaration":
            handle_declaration(x, current_scope)
        elif x[0] == "assignment":
            handle_assignment(x, current_scope)
        elif x[0] == "abstract_function_declaration":
            handle_abstract_function_declaration(x, current_scope)
        elif x[0] == "print_statement":
            handle_print_statement(x, current_scope)
        elif x[0] == "attempt_findout_block":
            handle_attempt_findout_block(x, current_scope)
        elif x[0] == "abstract_call":
            handle_abstract_call(x, current_scope)
        elif x[0] == "conditionals":
            handle_conditionals(x, current_scope)


# Type checking
def type_checking(var_type, value):
    if var_type == "int":
        if type(value) != int:
            return False
        else:
            return True
    elif var_type == "float":
        if type(value) != float:
            return False
        else:
            return True
    elif var_type == "bool":
        if type(value) != bool:
            return False
        else:
            return True
    elif var_type == "string":
        if type(value) != str:
            return False
        else:
            return True
    else:
        return False


# Handles expressions
def handle_expression(node, current_scope):
    if isinstance(node, int) or isinstance(node, float) or isinstance(node, bool):
        return node
    elif isinstance(node, tuple):
        if node[0] == "add":
            left_operand = handle_expression(node[1], current_scope)
            right_operand = handle_expression(node[2], current_scope)
            result = left_operand + right_operand
            return result
        elif node[0] == "sub":
            left_operand = handle_expression(node[1], current_scope)
            right_operand = handle_expression(node[2], current_scope)
            result = left_operand - right_operand
            return result
        elif node[0] == "mul":
            left_operand = handle_expression(node[1], current_scope)
            right_operand = handle_expression(node[2], current_scope)
            result = left_operand * right_operand
            return result
        elif node[0] == "div":
            left_operand = handle_expression(node[1], current_scope)
            right_operand = handle_expression(node[2], current_scope)
            result = left_operand / right_operand
            return result
        elif node[0] == "power":
            left_operand = handle_expression(node[1], current_scope)
            right_operand = handle_expression(node[2], current_scope)
            result = left_operand**right_operand
            return result
        elif node[0] == "not":
            operand = handle_expression(node[1], current_scope)
            if not isinstance(operand, bool):
                raise ValueError(f"Expected a boolean, got '{type(operand).__name__}'")
            result = not operand
            return result
        elif node[0] == "equivalent":
            left_operand = handle_expression(node[1], current_scope)
            right_operand = handle_expression(node[2], current_scope)
            result = left_operand == right_operand
            return result
        elif node[0] == "greater_than":
            left_operand = handle_expression(node[1], current_scope)
            right_operand = handle_expression(node[2], current_scope)
            result = left_operand > right_operand
            return result
        elif node[0] == "less_than":
            left_operand = handle_expression(node[1], current_scope)
            right_operand = handle_expression(node[2], current_scope)
            result = left_operand < right_operand
            return result
        elif node[0] == "not_equal":
            left_operand = handle_expression(node[1], current_scope)
            right_operand = handle_expression(node[2], current_scope)
            result = left_operand != right_operand
            return result
        elif node[0] == "less_than_or_equal":
            left_operand = handle_expression(node[1], current_scope)
            right_operand = handle_expression(node[2], current_scope)
            result = left_operand <= right_operand
            return result
        elif node[0] == "greater_than_or_equal":
            left_operand = handle_expression(node[1], current_scope)
            right_operand = handle_expression(node[2], current_scope)
            result = left_operand >= right_operand
            return result
    # Check if the node is a string
    elif isinstance(node, str):
        # Check is the node is a variable
        if node[0] == "_":
            # If the node is a variable, check if it is in the symbol table
            lookup_var = current_scope.lookup(node)
            if not lookup_var:
                # print(f"Undeclared variable '{node}'")
                raise ValueError(f"Undeclared variable '{node}'")
            # var_type, value, is_locked, symbol_type = symbol_table[node]
            value = lookup_var.value
            return value
    elif node == None:
        return node
    else:
        raise ValueError(f"Invalid expression {node}")


# Handles declarations
def handle_declaration(node, current_scope):
    if len(node) == 4:
        var_mut, var_type, var_name = node[1][1], node[2], node[3]
        if var_mut == "declare":
            is_locked = False
        else:
            raise ValueError("Invalid mutex declaration")
        check_if_variable_exists = current_scope.lookup(var_name)
        if check_if_variable_exists:
            raise ValueError(f"Variable '{var_name}' is already declared")
        elif check_if_variable_exists is None:
            add_to_symbol_table = current_scope.insert(
                VariableSymbol(var_name, var_type, None, is_locked)
            )
            if add_to_symbol_table == False:
                raise ValueError(f"Variable '{var_name}' is already declared")
    elif len(node) == 5:
        var_mut, var_type, var_name, value = node[1][1], node[2], node[3], node[4]
        if var_mut == "declare":
            is_locked = False
        else:
            raise ValueError("Invalid mutex declaration")

        # LOOKUP
        check_if_variable_exists = current_scope.lookup(var_name)
        # Check if the variable is already declared
        if check_if_variable_exists:  # If the variable is already declared
            if (
                is_locked == True and check_if_variable_exists.value is not None
            ):  # If the variable is locked and has a value
                raise ValueError(f"Cannot reassign locked variable '{var_name}'")
            # raise ValueError(f"Variable '{var_name}' is already declared") #

        # Handles any expressions
        if isinstance(value, tuple):
            value = handle_expression(value, current_scope)
        # Checks if the type is correct
        type_check = type_checking(var_type, value)
        if not type_check:
            raise ValueError(f"Expected an {var_type}, got '{type(value).__name__}'")
            # raise ValueError(f"Cannot assign locked variable '{var_name}'")
        # If the type is correct, assign the value to the variable
        add_to_symbol_table = current_scope.insert(
            VariableSymbol(var_name, var_type, value, is_locked)
        )
        if add_to_symbol_table == False:
            raise ValueError(f"Variable '{var_name}' is already declared")
    else:
        raise ValueError("Invalid declaration")


# Handles assignments
def handle_assignment(node, current_scope):
    if len(node) == 4:
        var_name, value = node[1], node[3]
        if isinstance(value, tuple):
            value = handle_expression(value, current_scope)
        # Check if the variable is in the symbol table
        # Check if the variable has a value
        # Check if the variable is locked

        lookup_var = current_scope.lookup(var_name)
        if lookup_var is None:
            # print(f"Undeclared variable '{var_name}'")
            raise ValueError(f"Undeclared variable '{var_name}'")
        else:
            var_type = lookup_var.type
            old_value = lookup_var.value
            is_locked = lookup_var.is_locked
            if is_locked and old_value is not None:
                # print(f"Cannot reassign locked variable '{var_name}'")
                raise ValueError(f"Cannot reassign locked variable '{var_name}'")
            else:

                # Check if the type is correct
                type_check = type_checking(var_type, value)
                # If the type is incorrect, raise an error
                if type_check == False:
                    raise ValueError(
                        f"Expected an {var_type}, got '{type(value).__name__}'"
                    )
                # If the type is correct, assign the value to the variable
                elif type_check:
                    lookup_var.value = value
                    # print(f"Assigned value '{value}' to variable '{var_name}'")
                else:
                    # print(
                    #     f"Type mismatch for variable '{var_name}' expected '{var_type}'"
                    # )
                    raise ValueError(
                        f"Type mismatch for variable '{var_name}' expected '{var_type}'"
                    )
    else:
        raise ValueError("Invalid assignment")


# TODO: Fix the print statement so it accepts variables (DONE)
# Handles print statements
def handle_print_statement(node, current_scope):
    if len(node) == 2:
        # Check is it an identifier or a string
        if isinstance(node[1], str):
            if node[1][0] == "_":
                lookup_var = current_scope.lookup(node[1])
                if not lookup_var:
                    # print(f"Undeclared variable '{node}'")
                    raise ValueError(
                        f"Undeclared variable '{node[1]}' in scribe statement "
                    )
                # var_type, value, is_locked, symbol_type = symbol_table[node]
                # value = lookup_var.value
                # return value
                # else:
                # print(lookup_var.value)
            # else:
            #     print(node[1])
        else:
            raise ValueError("Invalid scribe statement")
        # print("2")

        # print(node[1])
    elif len(node) == 3:
        if isinstance(node[1], str):
            if node[1][0] == "_":
                lookup_var_1 = current_scope.lookup(node[1])
                lookup_var_2 = current_scope.lookup(node[2])
                if not lookup_var_1:
                    # print(f"Undeclared variable '{node}'")
                    raise ValueError(
                        f"Undeclared variable '{node[1]}' in scribe statement "
                    )
                if not lookup_var_2:
                    # print(f"Undeclared variable '{node}'")
                    raise ValueError(
                        f"Undeclared variable '{node[2]}' in scribe statement "
                    )
                # var_type, value, is_locked, symbol_type = symbol_table[node]
                # value = lookup_var.value
                # return value
                # else:
                #     print(lookup_var_1.value, lookup_var_2.value)
            else:
                lookup_var_2 = current_scope.lookup(node[2])
                if lookup_var_2 == None:
                    raise ValueError(
                        f"The second argument '{node[2]}' is not a declared in this scope"
                    )
                # print(node[1], lookup_var_2.value)
                # else
                # print(lookup_var_2)
                # print(node[1], node[2])
        else:
            raise ValueError("Invalid scribe statement")
        # if node[0][0] == "_":
        #     print(node[0][0])
        #     print("******" * 40)
        #     raise ValueError("Invalid scribe statement")
        # if isinstance(node[2], str):
        #     if node[2][0] == "_":
        #         lookup_var = current_scope.lookup(node[2])
        #         if not lookup_var:
        #             # print(f"Undeclared variable '{node}'")
        #             raise ValueError(
        #                 f"Undeclared variable '{node[2]}' in scribe statement "
        #             )
        #         # var_type, value, is_locked, symbol_type = symbol_table[node]
        #         # value = lookup_var.value
        #         # return value
        #         else:
        #             print(node[2], lookup_var.value)
        #     else:
        #         raise ValueError(
        #             "If using the second argument in the scribe statement, it must be a variable"
        #         )
        # else:
        #     raise ValueError("Invalid scribe statement")
    else:
        raise ValueError("Invalid scribe statement")


# Handles attempt and findout blocks
def handle_attempt_findout_block(node, current_scope):
    attempt_scope = new_scope(current_scope)
    handle_attempt_block(node[1], attempt_scope)
    handle_findout_block(node[2], attempt_scope)


# Handles attempt block
def handle_attempt_block(node, current_scope):
    semantic_analyzer(node[1], current_scope)


# Handles findout block
def handle_findout_block(node, current_scope):
    semantic_analyzer(node[2], current_scope)


# TODO: Implement parameter and argument declaration (DONE)
# Handles abstract function declaration
def handle_abstract_function_declaration(node, current_scope):
    check_if_function_exists = current_scope.lookup(node[1])
    if check_if_function_exists:
        raise ValueError(f"Function '{node[1]}' is already declared")
    else:
        add_function = current_scope.insert(
            FunctionSymbol(node[1], node[2], "void", node[3])
        )
        if add_function == False:
            raise ValueError(f"Function '{node[1]}' is already declared")
        elif add_function:
            pass
        else:
            raise ValueError(f"Function '{node[1]}' was not declared")


# TODO: Implement parameter and argument declaration (DONE)
# Handles abstract function call
def handle_abstract_call(node, current_scope):
    check_if_function_exists = current_scope.lookup(node[1])
    if check_if_function_exists:
        # Declaring a new scope for the function
        function_scope = new_scope(current_scope)
        # Check if the function has parameters
        params = check_if_function_exists.params
        # Check if the function has arguments
        arguments = node[2]
        # if the function has no parameters and no arguments run the function
        if arguments == [None] and params == [None]:
            statements_ast = check_if_function_exists.statements
            semantic_analyzer(statements_ast, function_scope)
            return
        if arguments == None and params == None:
            statements_ast = check_if_function_exists.statements
            semantic_analyzer(statements_ast, function_scope)
            return
        # if the function has parameters but no arguments raise an error
        if arguments == [None] and params != [None]:
            raise ValueError(f"Expected {len(params)} arguments, got 0")
        # Check if the number of arguments match the number of parameters
        if len(params) != len(arguments):
            raise ValueError(f"Expected {len(params)} arguments, got {len(arguments)}")

        for param, argument in zip(params, arguments):
            if isinstance(argument[1], tuple):
                argument_value = handle_expression(argument[1], current_scope)
                if argument_value:
                    lookup_param = current_scope.lookup(param[2])
                    if lookup_param == None:
                        check_if_param_and_arg_are_same_type = type_checking(
                            param[1], argument_value
                        )
                        if not check_if_param_and_arg_are_same_type:
                            raise ValueError(
                                f"Invalid argument'{argument_value}' of type '{type(argument_value).__name__}' not the same type as the parameter '{param[1]}'"
                            )
                        if check_if_param_and_arg_are_same_type:
                            function_scope.insert(
                                VariableSymbol(
                                    param[2], param[1], argument_value, False
                                )
                            )
                            lookup_param = function_scope.lookup(param[2])
                    else:
                        check_if_param_and_arg_are_same_type = type_checking(
                            lookup_param.type, argument_value
                        )
                        if check_if_param_and_arg_are_same_type:
                            function_scope.insert(
                                VariableSymbol(
                                    param[2], param[1], argument_value, False
                                )
                            )
                        else:
                            raise ValueError(
                                f"Invalid argument'{argument[1]}' not the same type as the parameter '{param[1]}'"
                            )
                else:
                    raise ValueError(
                        f"Invalid argument'{argument[1]}' expression not calculated"
                    )
            elif isinstance(argument[1], str):
                if argument[1][0] == "_":
                    lookup_var = current_scope.lookup(argument[1])
                    if not lookup_var:
                        raise ValueError(
                            f"Undeclared variable '{argument[1]}' in argument"
                        )
                    lookup_param = current_scope.lookup(param[2])
                    if lookup_param.value == lookup_var.value:
                        check_type = type_checking(lookup_param.type, lookup_var.value)
                        if not check_type:
                            raise ValueError(
                                f"Invalid argument'{lookup_var.value}' of type '{type(lookup_var.value).__name__}' not the same type as the parameter '{param[1]}'"
                            )
                        function_scope.insert(
                            VariableSymbol(param[2], param[1], lookup_var.value, False)
                        )
                else:
                    check_type = type_checking(argument[1], param[1])
                    if not check_type:
                        raise ValueError(
                            f"Invalid argument'{lookup_var.value}' of type '{type(lookup_var.value).__name__}' not the same type as the parameter '{param[1]}'"
                        )
                    function_scope.insert(
                        VariableSymbol(param[2], param[1], lookup_var.value, False)
                    )
            elif (
                isinstance(argument[1], int)
                or isinstance(argument[1], float)
                or isinstance(argument[1], bool)
            ):
                check_if_param_and_arg_are_same_type = type_checking(
                    param[1], argument[1]
                )
                if not check_if_param_and_arg_are_same_type:
                    raise ValueError(
                        f"Invalid argument'{argument[1]}' of type '{type(argument[1]).__name__}' not the same type as the parameter '{param[1]}'"
                    )
                function_scope.insert(
                    VariableSymbol(param[2], param[1], argument[1], False)
                )

        statements_ast = check_if_function_exists.statements
        semantic_analyzer(statements_ast, function_scope)
    else:
        raise ValueError(f"Function '{node[1]}' is not declared")


# Handles conditionals
def handle_conditionals(node, current_scope):
    if node[1][0] == "if":
        helper_handle_if(node[1], current_scope)
    elif node[1][0] == "if_elif":
        handle_if_elif(node[1], current_scope)
    elif node[1][0] == "if_else":
        handle_if_else(node[1], current_scope)
    elif node[1][0] == "if_elif_else":
        handle_if_elif_else(node[1], current_scope)
    elif node[1][0] == "repeatif_statement":
        handle_repeatif(node[1], current_scope)
    elif node[1][0] == "for_loop":
        handle_for_loop(node[1], current_scope)
    else:
        raise ValueError("Invalid conditional")


def helper_handle_if(node, current_scope):
    expression = handle_expression(node[1], current_scope)
    if isinstance(expression, bool):
        if_scope = new_scope(current_scope)
        semantic_analyzer(node[2], if_scope)
    else:
        raise ValueError("Expected a boolean expression in IF statement")


def handle_if_elif(node, current_scope):
    ifstatement = node[1]
    helper_handle_if(ifstatement, current_scope)
    elifstatement = node[2]
    helper_handle_elif(elifstatement, current_scope)


def handle_if_else(node, current_scope):
    ifstatement = node[1]
    helper_handle_if(ifstatement, current_scope)
    helper_handle_else(node[2], current_scope)


def handle_if_elif_else(node, current_scope):
    ifstatement = node[1]
    helper_handle_if(ifstatement, current_scope)
    helper_handle_elif(node[2], current_scope)
    helper_handle_else(node[3], current_scope)


def helper_handle_elif(node, current_scope):
    expression = handle_expression(node[1], current_scope)
    if isinstance(expression, bool):
        elif_scope = new_scope(current_scope)
        semantic_analyzer(node[2], elif_scope)
    else:
        raise ValueError("Expected a boolean expression in ELIF statement")


def helper_handle_else(node, current_scope):
    else_scope = new_scope(current_scope)
    semantic_analyzer(node[1], else_scope)


def handle_repeatif(node, current_scope):
    expression = handle_expression(node[1], current_scope)
    if type(expression) == bool:
        repeatif_scope = new_scope(current_scope)
        semantic_analyzer(node[2], repeatif_scope)
    else:
        raise ValueError("Expected a boolean expression in REPEATIF statement")


# Handles for loops
def handle_for_loop(node, current_scope):
    if node[1] == "range":
        var = current_scope.lookup(node[2])
        if var:
            raise ValueError(f"Variable '{node[3]}' in for loop is already declared")
        for x in node[3]:
            for_scope = new_scope(current_scope)
            for_scope.insert(VariableSymbol(x[0], type(x[1]).__name__, x[1], True))
            semantic_analyzer(node[4], for_scope)
    elif node[1] == "in":
        var = current_scope.lookup(node[2])
        if var:
            raise ValueError(f"Variable '{node[3]}' in for loop is already declared")
        for_scope = new_scope(current_scope)
        for_scope.insert(VariableSymbol(node[3], "int", None, True))
        semantic_analyzer(node[4], for_scope)
    else:
        raise ValueError("Invalid for loop")
