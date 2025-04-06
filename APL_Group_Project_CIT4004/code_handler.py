'''
Authors
Sassania Hibbert 1901201
Darrell King 1803342
Shavar Mclean 1903893
Mark Vernon 1908916
Jelani Jackson 1901811
'''

import sys

from db import DB as database
from openai_api import chat_with_gpt


def book_reservation(booking_place, person_name, booking_date, start_location, end_location, time):
    sqlquery = """ EXEC Create_New_Reservation @Client_Name=?, @Place=?, @Start_Date=?, 
                   @End_Date=?, @Location=?, @Destination=?, @Time=? """

    params = (person_name, booking_place, booking_date, booking_date, start_location, end_location, time)
    if database.execute_query_params(sqlquery, params):
        print("Reservation CREATED Successfully for:", person_name)


def cancel_reservation_identifier(booking_place, person_name, reservation_number):
    sqlquery = """ EXEC Cancel_Active_Reservation @Client_Name=?, @Place=?, @Reservation_No=? """
    params = (person_name, booking_place, reservation_number)

    if not reservation_number:
        record_identifier = person_name
    else:
        record_identifier = f"{person_name}:{reservation_number}"

    if database.execute_query_params(sqlquery, params):
        print("Reservation CANCELLED Successfully for:", record_identifier)


def cancel_reservation(booking_place, person_name):
    sqlquery = """ EXEC Cancel_Active_Reservation @Client_Name=?, @Place=?, @Reservation_No='' """
    params = (person_name, booking_place)

    if database.execute_query_params(sqlquery, params):
        print("Reservation CANCELLED Successfully for:", person_name)


def confirm_reservation(booking_place, person_name):
    sqlquery = """ EXEC Confirm_Client_Reservation @Client_Name=?, @Place=?, @Reservation_No= '' """
    params = (person_name, booking_place)

    record_identifier = person_name

    if database.execute_query_params(sqlquery, params):
        print("Reservation CONFIRMED Successfully for:", record_identifier)


def confirm_reservation_identifier(booking_place, person_name, reservation_number):
    sqlquery = """ EXEC Confirm_Client_Reservation @Client_Name=?, @Place=?, @Reservation_No=? """
    params = (person_name, booking_place, reservation_number)

    if not reservation_number:
        record_identifier = person_name
    else:
        record_identifier = f"{person_name}:{reservation_number}"

    if database.execute_query_params(sqlquery, params):
        print("Reservation CONFIRMED Successfully for:", record_identifier)


def pay_reservation(booking_place, person_name):
    sqlquery = """ EXEC Pay_Client_Reservation @Client_Name=?, @Place=?, @Reservation_No= '' """
    params = (person_name, booking_place)

    record_identifier = person_name

    if database.execute_query_params(sqlquery, params):
        print("Reservation PAID Successfully for:", record_identifier)


def pay_reservation_identifier(booking_place, person_name, reservation_number):
    sqlquery = """ EXEC Pay_Client_Reservation @Client_Name=?, @Place=?, @Reservation_No=? """
    params = (person_name, booking_place, reservation_number)

    if not reservation_number:
        record_identifier = person_name
    else:
        record_identifier = f"{person_name}:{reservation_number}"

    if database.execute_query_params(sqlquery, params):
        print("Reservation PAID Successfully for:", record_identifier)


def view_list_reservations_with_status(status):

    if status.upper() == "ALL":
        sqlquery = f" SELECT * from Reservations "
    else:
        sqlquery = f" SELECT * from Reservations WHERE Status = '{status}' "

    try:
        conn = database.create_server_connection()
        cursor = conn.cursor()
        cursor.execute(sqlquery)

        # Output list of all reservations
        records = cursor.fetchall()

        # Make status word uppercase
        upper_case_status = status.upper()

        if len(records) > 0:
            print(f"{upper_case_status} RESERVATIONS:")
            for r in records:
                print(f"{r.ClientName}\t{r.Place}\t{r.StartDate}\t{r.EndDate}\t{r.Location}\t{r.Destination}")
        else:
            if upper_case_status == 'ALL':
                print(f"No reservations found.")
            else:
                print(f"No {upper_case_status} reservations found.")

        cursor.close()
        conn.close()


    except BaseException as e:
        # Get current system exception
        ex_type, ex_value, ex_traceback = sys.exc_info()
        print(f"Error retrieving list of reservations\nERROR: {ex_value}")


def view_list_reservations_specific(name):

    sqlquery = f" SELECT * from Reservations WHERE ClientName LIKE '{name}' "

    try:
        conn = database.create_server_connection()
        cursor = conn.cursor()
        cursor.execute(sqlquery)

        # Output list of all reservations
        records = cursor.fetchall()

        # Make status word uppercase
        upper_case_val = name.upper()

        if len(records) > 0:
            print(f"{upper_case_val} RESERVATIONS:")
            for r in records:
                print(f"{r.ClientName}\t{r.Place}\t{r.StartDate}\t{r.EndDate}\t{r.Location}\t{r.Destination}")
        else:
            print(f"No {upper_case_val} reservations found.")

        cursor.close()
        conn.close()

    except BaseException as e:
        # Get current system exception
        ex_type, ex_value, ex_traceback = sys.exc_info()
        print(f"Error retrieving list of reservations for {name}\nERROR: {ex_value}")


def view_list_tickets_specific(name):

    sqlquery = f" SELECT * from TicketBookings WHERE ClientName LIKE '{name}' "

    try:
        conn = database.create_server_connection()
        cursor = conn.cursor()
        cursor.execute(sqlquery)

        # Output list of all reservations
        records = cursor.fetchall()

        # Make status word uppercase
        upper_case_val = name.upper()

        if len(records) > 0:
            print(f"{upper_case_val} TICKETS:")
            for r in records:
                print(f"{r.ClientName}\t{r.Place}\t{r.StartDate}\t{r.EndDate}\t{r.Location}\t{r.Destination}")
        else:
            print(f"No {upper_case_val} ticket(s) found.")

        cursor.close()
        conn.close()

    except BaseException as e:
        # Get current system exception
        ex_type, ex_value, ex_traceback = sys.exc_info()
        print(f"Error retrieving list of tickets for {name}\nERROR: {ex_value}")


def view_list_tickets_status(status):

    if status.upper() == "ALL":
        sqlquery = f" SELECT * from TicketBookings "
    else:
        sqlquery = f" SELECT * from TicketBookings WHERE Status = '{status}' "

    try:
        conn = database.create_server_connection()
        cursor = conn.cursor()
        cursor.execute(sqlquery)

        # Output list of all reservations
        records = cursor.fetchall()

        # Make status word uppercase
        upper_case_status = status.upper()

        if len(records) > 0:
            print(f"{upper_case_status} TICKETS:")
            for r in records:
                print(f"{r.ClientName}\t{r.Place}\t{r.StartDate}\t{r.EndDate}\t{r.Location}\t{r.Destination}")
        else:
            if upper_case_status == 'ALL':
                print(f"No reservations found.")
            else:
                print(f"No {upper_case_status} reservations found.")

        cursor.close()
        conn.close()


    except BaseException as e:
        # Get current system exception
        ex_type, ex_value, ex_traceback = sys.exc_info()
        print(f"Error retrieving list of reservations\nERROR: {ex_value}")


def view_api_response(input_prompt):
    prompt = input_prompt + """
        . If this is an event, please include the event date and time, how many tickets available, and
           the cost of tickets if the event is not free.
    """

    response = chat_with_gpt(prompt)
    print("=" * 50)
    print("ChatGPT Response:")
    print(response)
    print("=" * 50)


def view_list_payed_reservations():
    sqlquery = """ SELECT * from Reservations WHERE IsPaid = 1 """

    try:
        conn = database.create_server_connection()
        cursor = conn.cursor()
        cursor.execute(sqlquery)

        # Output list of all reservations
        records = cursor.fetchall()

        if len(cursor.fetchall()) > 0:
            print("PAYED RESERVATIONS:")
            for r in records:
                print(f"{r.ClientName}\t{r.Place}\t{r.StartDate}\t{r.EndDate}\t{r.Location}\t{r.Destination}")
        else:
            print("No PAID reservations found.")

        cursor.close()
        conn.close()


    except BaseException as e:
        # Get current system exception
        ex_type, ex_value, ex_traceback = sys.exc_info()
        print(f"Error retrieving PAID reservations\nERROR: {ex_value}")


def book_ticket(booking_place, person_name, booking_date, start_location, end_location, time):
    sqlquery = """ EXEC Create_New_TicketBooking @Client_Name=?, @Place=?, @Start_Date=?, 
                   @End_Date=?, @Location=?, @Destination=?, @Time=? """

    params = (person_name, booking_place, booking_date, booking_date, start_location, end_location, time)
    if database.execute_query_params(sqlquery, params):
        print("Ticket BOOKED Successfully for:", person_name)


def cancel_ticket(booking_place, person_name):
    sqlquery = """ EXEC Cancel_TicketBooking_For_Client @Client_Name=?, @Place=?, @Ticket_No='' """
    params = (person_name, booking_place)

    if database.execute_query_params(sqlquery, params):
        print("Ticket CANCELLED Successfully for:", person_name)


def cancel_ticket_identifier(booking_place, person_name, ticket_number):
    sqlquery = """ EXEC Cancel_TicketBooking_For_Client @Client_Name=?, @Place=?, @Ticket_No=? """
    params = (person_name, booking_place, ticket_number)

    if not ticket_number:
        record_identifier = person_name
    else:
        record_identifier = f"{person_name}:{ticket_number}"

    if database.execute_query_params(sqlquery, params):
        print("Reservation CANCELLED Successfully for:", record_identifier)

