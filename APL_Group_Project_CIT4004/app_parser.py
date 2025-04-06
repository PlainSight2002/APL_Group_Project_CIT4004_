import ply.yacc as yacc

from lexer import tokens


# Parsing rules
def p_program(p):
    """
    program : statements
    """
    p[0] = p[1]


# STATEMENTS
def p_statements(p):
    """
    statements : statement statements
               | empty
    """
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []


def p_statement(p):
    """
    statement : declaration
              | assignment
              | print_statement
              | conditionals
              | book_reservation
              | view_list_reservations
              | cancel_reservation
              | cancel_reservation_identifier
              | confirm_reservation
              | confirm_reservation_identifier
              | pay_reservation
              | pay_reservation_identifier
              | list_api_events
              | cancel_ticket_identifier
              | cancel_ticket
              | book_ticket
              | view_list_tickets
              | view_specific_tickets
              | view_specific_reservations

    """
    p[0] = p[1]


# DECLARATIONS
def p_declaration_with_assignment(p):
    """
    declaration : mutex type IDENTIFIER EQUAL expression LINEEND
    """
    p[0] = ("declaration", p[1], p[2], p[3], p[5])  # Literal value


def p_declaration_without_assignment(p):
    """declaration : mutex type IDENTIFIER LINEEND"""
    p[0] = ("declaration", p[1], p[2], p[3])


def p_book_reservation_client(p):
    """
    book_reservation : BOOK RESERVATION ATPLACE place_name FOR person_name ON date FROM start_location TO destination ATTIME record_time LINEEND
                    | BOOK RESERVATION ATPLACE place_name FOR person_name ON date ATTIME record_time LINEEND
    """
    if len(p) == 16:
        p[0] = ("book_reservation", p[4], p[6], p[8], p[10], p[12], p[14])
    elif len(p) == 12:
        p[0] = ("book_reservation_no_location", p[4], p[6], p[8], p[10])


def p_book_ticket_client(p):
    """
    book_ticket : BOOK TICKET ATPLACE place_name FOR person_name ON date FROM start_location TO destination ATTIME record_time LINEEND
    """
    p[0] = ("book_ticket", p[4], p[6], p[8], p[10], p[12], p[14])


def p_cancel_ticket_client(p):
    """
    cancel_ticket : CANCEL TICKET ATPLACE place_name FOR person_name LINEEND
    """
    p[0] = ("cancel_ticket", p[4], p[6])


def p_cancel_ticketbooking_client_identifier(p):
    """
    cancel_ticket_identifier : CANCEL TICKET ATPLACE place_name FOR person_name DCOLON record_identifier LINEEND
    """
    p[0] = ("cancel_ticket_with_identifier", p[4], p[6], p[8])


def p_cancel_reservation_client(p):
    """
    cancel_reservation : CANCEL RESERVATION ATPLACE place_name FOR person_name LINEEND
    """
    p[0] = ("cancel_reservation", p[4], p[6])


def p_cancel_reservation_client_identifier(p):
    """
    cancel_reservation_identifier : CANCEL RESERVATION ATPLACE place_name FOR person_name DCOLON record_identifier LINEEND
    """
    p[0] = ("cancel_reservation_with_identifier", p[4], p[6], p[8])


def p_confirm_reservation_client(p):
    """
    confirm_reservation : CONFIRM RESERVATION ATPLACE place_name FOR person_name LINEEND
    """
    p[0] = ("confirm_reservation", p[4], p[6])


def p_confirm_reservation_client_identifier(p):
    """
    confirm_reservation_identifier : CONFIRM RESERVATION ATPLACE place_name FOR person_name DCOLON record_identifier LINEEND
    """
    p[0] = ("confirm_reservation_with_identifier", p[4], p[6], p[8])


def p_pay_reservation_client(p):
    """
    pay_reservation : PAY RESERVATION ATPLACE place_name FOR person_name LINEEND
    """
    p[0] = ("pay_reservation", p[4], p[6])


def p_pay_reservation_client_identifier(p):
    """
    pay_reservation_identifier : PAY RESERVATION ATPLACE place_name FOR person_name DCOLON record_identifier LINEEND
    """
    p[0] = ("pay_reservation_with_identifier", p[4], p[6], p[8])


def p_view_list_events(p):
    """
    list_api_events : LIST ai_prompt LINEEND
    """
    p[0] = ("view_openai_response", p[2])


def p_place_name(p):
    """
    place_name : STRING_LITERAL
              | IDENTIFIER
    """
    p[0] = p[1]


def p_record_time_name(p):
    """
    record_time : STRING_LITERAL
              | IDENTIFIER
    """
    p[0] = p[1]

def p_api_events_prompt(p):
    """
    ai_prompt : STRING_LITERAL
                    | IDENTIFIER
    """
    p[0] = p[1]


def p_person_name(p):
    """
    person_name : STRING_LITERAL
              | IDENTIFIER
    """
    p[0] = p[1]


def p_reservation_start_location(p):
    """
    start_location : STRING_LITERAL
                | IDENTIFIER
    """
    p[0] = p[1]


def p_reservation_destination_location(p):
    """
    destination : STRING_LITERAL
                | IDENTIFIER
    """
    p[0] = p[1]


def p_date_string(p):
    """
    date : DATESTRING
    """
    p[0] = p[1]


def p_record_identifier_value(p):
    """
    record_identifier : INTEGER
                    | STRING_LITERAL
                    | IDENTIFIER
    """
    p[0] = p[1]


def p_view_all_reservation(p):
    """
    view_list_reservations : VIEW RESERVATION DCOLON reservation_status LINEEND
    """
    p[0] = ("view_reservation_with_status", p[4])


def p_view_specific_reservation(p):
    """
    view_specific_reservations : VIEW RESERVATION FOR person_name LINEEND
    """
    p[0] = ("view_reservation_with_name", p[4])


def p_view_all_tickets(p):
    """
    view_list_tickets : VIEW TICKET DCOLON ticket_status LINEEND
    """
    p[0] = ("view_tickets_with_status", p[4])


def p_view_specific_ticket(p):
    """
    view_specific_tickets : VIEW TICKET FOR person_name LINEEND
    """
    p[0] = ("view_specific_tickets", p[4])


def p_def_reservation_status(p):
    """
    reservation_status : STRING_LITERAL
                        | IDENTIFIER
    """
    p[0] = p[1]


def p_def_ticket_status(p):
    """
    ticket_status : STRING_LITERAL
                        | IDENTIFIER
    """
    p[0] = p[1]


# ASSIGNMENT
def p_assignment(p):
    """
    assignment : IDENTIFIER EQUAL expression LINEEND
    """
    p[0] = ("assignment", p[1], p[2], p[3])


# PRINT STATEMENTS
def p_print_statement_string(p):
    """
    print_statement : OUTPUT LPAREN STRING_LITERAL RPAREN LINEEND

    """
    p[0] = ("print_statement", p[3])


def p_print_statement_id(p):
    """
    print_statement : OUTPUT LPAREN IDENTIFIER RPAREN LINEEND
    """
    p[0] = ("print_statement", p[3])


def p_print_statement_id_with_id(p):
    """
    print_statement : OUTPUT LPAREN IDENTIFIER COMMA IDENTIFIER RPAREN LINEEND
    """
    p[0] = ("print_statement", p[3], p[5])


def p_print_statement_id_with_string(p):
    """
    print_statement : OUTPUT LPAREN STRING_LITERAL COMMA IDENTIFIER RPAREN LINEEND
    """
    p[0] = ("print_statement", p[3], p[5])


# CONDITIONALS
def p_conditionals(p):
    """
    conditionals : if_statement
                 | for_statement
                 | repeatif_statement
    """
    p[0] = ("conditionals", p[1])


# IF_ELIF_ELSE
def p_if_statement(p):
    """
    if_statement : IF expression LBRACE statements RBRACE
                 | IF expression LBRACE statements RBRACE ELSE LBRACE statements RBRACE
                 | IF expression LBRACE statements RBRACE ELIF expression LBRACE statements RBRACE
                 | IF expression LBRACE statements RBRACE ELIF expression LBRACE statements RBRACE ELSE LBRACE statements RBRACE
    """
    if len(p) == 6:
        p[0] = ("if", p[2], p[4])
    elif len(p) == 10:
        if p[6] == "else":
            p[0] = ("if_else", ("if", p[2], p[4]), ("else", p[8]))
    elif len(p) == 11:
        p[0] = ("if_elif", ("if", p[2], p[4]), ("elif", p[7], p[9]))
    elif len(p) == 15:
        p[0] = (
            "if_elif_else",
            ("if", p[2], p[4]),
            ("elif", p[7], p[9]),
            ("else", p[13]),
        )


# FOR_BLOCK
def p_for_statement(p):
    """
    for_statement : FOR IDENTIFIER IN RANGE LPAREN arguments RPAREN LBRACE statements RBRACE
    """
    p[0] = ("for_loop", "range", p[2], p[6], p[9])


def p_for_statement_with_identifiers(p):
    """
    for_statement : FOR IDENTIFIER IN iterables LBRACE statements RBRACE
    """
    p[0] = ("for_loop", "in", p[2], p[4], p[6])


def p_iterables(p):
    """
    iterables : STRING_LITERAL
              | IDENTIFIER
    """
    p[0] = p[1]


# REPEATIF_BLOCK
def p_repeatif_statement(p):
    """
    repeatif_statement : REPEATIF expression LBRACE statements RBRACE
    """
    p[0] = ("repeatif_statement", p[2], p[4])


# EXPRESSION
def p_expression_group(p):
    "expression : LPAREN expression RPAREN"
    p[0] = p[2]


def p_expression(p):
    """
    expression : expression PLUS expression
               | expression MINUS expression
               | expression TIMES expression
               | expression DIVIDE expression
               | expression POWER expression
               | expression NOTEQUAL expression
               | expression LESSTHAN expression
               | expression GREATERTHAN expression
               | expression LESSTHANOREQUAL expression
               | expression GREATERTHANOREQUAL expression
               | expression EQUIVALENT expression
               | expression BITWISEAND expression
               | expression BITWISEOR expression
               | expression BITWISEXOR expression
               | expression SHIFTLEFT expression
               | expression SHIFTRIGHT expression
               | NOT expression
               | PLUS expression
               | MINUS expression
               | BITWISEINVERT expression
               | INTEGER
               | FLOAT
               | IDENTIFIER
               | BOOLEAN
               | STRING_LITERAL
    """
    precedence = (
        ("left", "PLUS", "MINUS"),
        ("left", "TIMES", "DIVIDE"),
        ("left", "POWER"),
        ("right", "UNARY_MINUS", "UNARY_PLUS", "NOT", "BITWISEINVERT"),
        ("left", "BITWISEAND"),
        ("left", "BITWISEXOR"),
        ("left", "BITWISEOR"),
        ("left", "SHIFTLEFT", "SHIFTRIGHT"),
    )
    if len(p) == 4:
        if p[2] == "+":
            p[0] = ("add", p[1], p[3])
        elif p[2] == "-":
            p[0] = ("sub", p[1], p[3])
        elif p[2] == "*":
            p[0] = ("mul", p[1], p[3])
        elif p[2] == "/":
            p[0] = ("div", p[1], p[3])
        elif p[2] == "**":
            p[0] = ("power", p[1], p[3])
        elif p[2] == "!=":
            p[0] = ("not_equal", p[1], p[3])
        elif p[2] == "<":
            p[0] = ("less_than", p[1], p[3])
        elif p[2] == ">":
            p[0] = ("greater_than", p[1], p[3])
        elif p[2] == "<=":
            p[0] = ("less_than_or_equal", p[1], p[3])
        elif p[2] == ">=":
            p[0] = ("greater_than_or_equal", p[1], p[3])
        elif p[2] == "==":
            p[0] = ("equivalent", p[1], p[3])
        elif p[2] == "&":
            p[0] = ("bitwise_and", p[1], p[3])
        elif p[2] == "|":
            p[0] = ("bitwise_or", p[1], p[3])
        elif p[2] == "^":
            p[0] = ("bitwise_xor", p[1], p[3])
        elif p[2] == "<<":
            p[0] = ("shift_left", p[1], p[3])
        elif p[2] == ">>":
            p[0] = ("shift_right", p[1], p[3])
    elif len(p) == 3:
        if p[1] == "!":
            p[0] = ("not", p[2])
        elif p[1] == "+":
            p[0] = p[2]
        elif p[1] == "-":
            p[0] = ("unary_minus", p[2])
        elif p[1] == "~":
            p[0] = ("bitwise_invert", p[2])
    elif len(p) == 2:
        p[0] = p[1]
    else:
        raise ValueError("Invalid expression")


def p_error_type(p):
    """
    error_type : UNBOUNDLOCALERROR
                | TYPEERROR
                | VALUEERROR
                | INDEXERROR
                | KEYERROR
                | EXCEPTION
                | SYNTAXERROR
                | STOPITERATION
                | ARITHMETICERROR
                | FLOATINGPOINTERROR
                | OVERFLOWERROR
                | ZERODIVISIONERROR
                | ASSERTIONERROR
                | ATTRIBUTEERROR
                | BUFFERERROR
                | EOFERROR
                | IMPORTERROR
                | MODULENOTFOUNERROR
                | LOOKUPERROR
                | MEMORYERROR
                | NAMEERROR
                | BLOCKINGIOERROR
                | CHILDPROCESSERROR
                | CONNECTIONERROR
                | BROKENPIPEERROR
                | CONNECTIONABORTEDERROR
                | CONNECTIONREFUSEDERROR
                | CONNECTIONRESETERROR
                | FILEEXISTERROR
                | FILENOTFOUNERROR
                | INTERRUPTEDERROR
                | ISADIRECTORYERROR
                | NOTADIRECTORYERROR
                | PERMISSIONERROR
                | PROCESSLOOKUPERROR
                | TIMEOUTERROR
                | REFERENCEERROR
                | RUNTIMEERROR
                | INDENTATIONERROR
                | TABERROR
                | SYSTEMERROR
                | UNICODEERROR
                | UNICODEENCODEERROR
                | UNICODEDECODEERROR
                | UNICODETRANSLATEERROR
                | WARNING
                | USERWARNING
                | DEPRECATIONWARNING
                | PENDINGDEPRECATIONWARNING
                | SYNTAXWARNING
                | RUNTIMEWARNING
                | FUTUREWARNING
                | IMPORTWARNING
                | UNICODEWARNING
                | BYTESWARNING
                | RESOURCEWARNING
                | KEYBOARDINTERRUPT
    """
    p[0] = p[1]


def p_parameter(p):
    """
    parameter : type IDENTIFIER
    """
    p[0] = ("parameter", p[1], p[2])


def p_parameters(p):
    """
    parameters : parameter COMMA parameters
               | parameter
               | empty
    """
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = []


def p_arguments(p):
    """
    arguments : argument COMMA arguments
              | argument
              | empty
    """
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = []


def p_argument(p):
    """
    argument : IDENTIFIER
        | expression
    """
    p[0] = ("argument_declaration", p[1])


def p_mutex(p):
    """
    mutex : DECLARE
    """
    p[0] = ("mutex_declaration", p[1])


def p_type(p):
    """
    type : INT_TYPE
         | FLOAT_TYPE
         | BOOL_TYPE
         | STRING_TYPE
    """
    p[0] = p[1]


def p_empty(p):
    """
    empty :
    """
    pass


def p_error(p):
    if p:
        # print(f"Syntax error at line {p.lineno}, token='{p.value}'")
        raise SyntaxError(f"Syntax error at line {p.lineno}, token='{p.value} '")
    else:
        # print("Syntax error at EOF")
        raise SyntaxError(f"Syntax error at EOF")


parser = yacc.yacc()

# Parser Testing
# input_data = shortdata
# result = parser.parse(input_data)
# print(result)
