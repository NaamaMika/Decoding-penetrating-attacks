import socket
from datetime import datetime


def get_attacks(server_msg):
    """ The function give us the attack of the specific country.
    :param server_msg: the message we get from the server
    :return: the numbers of the attacks
    """
    index_attacks_S = server_msg.index("attacks=")  # start
    index_date_E = server_msg.index("date")  # end
    attacks = server_msg[index_attacks_S + 8:index_date_E - 1]
    return attacks


def get_target(server_msg):
    """ The function give us the attack of the specific country.
    :param server_msg: the message we get from the server
    :return: the target of the attack
    """
    index_target_S = server_msg.index("target=")
    attacks_type_index = server_msg.index("attacks_type")
    target = server_msg[index_target_S + 7:attacks_type_index - 1]
    return target


def get_attacks_type(server_msg):
    """ The function give us the attack of the specific country
    :param server_msg:  the message we get from thr server
    :return: the type of the attack
    """
    attacks_type_index = server_msg.index("attacks_type")
    attacks_type = server_msg[attacks_type_index + 13:]
    return attacks_type


def calculating_date_checksum(date):
    """ The function calculate the checksum of the date
    :param date: the current date
    :return: the checksum of the date
    """
    LIST_DIGITS = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    date_digits = date.replace("/", '')
    checksum_date = 0
    for i in range(len(date_digits)):
        if int(date_digits[i]) in LIST_DIGITS:
            checksum_date += int(date_digits[i])
    return checksum_date


def calculating_country_checksum(country):
    """ The function calculating the checksum of the country
    :param country: the current country
    :return: the checksum of the country
    """
    DICT_LETTERS = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "I": 9, "J": 10, "K": 11,
                    "L": 12, "M": 13, "N": 14, "O": 15, "P": 16, "Q": 17, "R": 18, "S": 19, "T": 20, "U": 21,
                    "V": 22, "W": 23, "X": 24, "Y": 25, "Z": 26}
    checksum_country = 0
    for i in range(len(country)):
        if country[i] != ' ':
            checksum_country += DICT_LETTERS[country.upper()[i]]
    return checksum_country


def arrange_msg_to_send(country, date, checksum_date, checksum_country):
    """ The function arrange the message that we will send to the server.
    :param country: the current country
    :param date: the current date
    :param checksum_date: the checksum of the date
    :param checksum_country: the checksum of the country
    :return: the message we will send to the country
    """
    msg_structure = "100:REQUEST:country=", str(country), "&date=", str(date), \
                    "&checksum=", str(checksum_country), ".", str(checksum_date), "&more_info=yes"
    msg_to_send = ""
    for item in msg_structure:  # casting from tuple to string
        msg_to_send += item
    return msg_to_send


def daily_update(date, country, server_msg):
    """ The function of the current daily update
    :param date: the current date
    :param country: the current country
    :param server_msg: the server we get from the server
    :return: the daily update
    """
    print("\033[1;34;36m**************************************************************************************")
    print("\033[1;34;36mDaily Update for country", country, ":")
    print("\033[1;34;36mdate:", date, "\t\033[1;34;36mattacks:", get_attacks(server_msg),
          "\t\033[1;34;36mtarget:", get_target(server_msg),
          "\t\033[1;34;36mattacks_type:", get_attacks_type(server_msg), "\n\n")
    print("\033[1;34;36mCountries with more then 20 attacks today:")
    print(arrange_countries_list(countries_in_danger(date)))
    print("\033[1;34;36m**************************************************************************************")


def get_list_of_countries():
    """ The function take the countries from the file path and arrange them to list.
    :return: the list of the countries
    """
    file_path = open("countries20.txt", "r")
    list_file = file_path.readlines()
    country_list = []
    for value in list_file:
        index_comma = value.index(',')
        sec_index_comma = None
        for i in range(len(value)):
            if value[i] == ',' and i != index_comma:
                sec_index_comma = i
                break
        country_list.append(value[index_comma+1:sec_index_comma])
    return country_list


def connect_to_server(server_ip, server_port, msg_to_send):
    """ The function connect to the server.
    :param server_ip: the ip of the server
    :param server_port: the port of the server
    :param msg_to_send: the message we will send to the server
    :return: the server message
    """
    sock = socket.socket()
    server_address = (server_ip, server_port)
    sock.connect(server_address)
    server_msg = sock.recv(1024).decode()
    sock.sendall(msg_to_send.encode())
    server_msg = sock.recv(1024).decode()
    sock.close()
    return server_msg


def countries_in_danger(date):
    """ The function get us the list of the countries that in danger
    :param date: the current date
    :return: list of countries in danger
    """
    SERVER_IP = "52.35.198.18"
    SERVER_PORT = 1050
    countries_in_danger_list = []
    countries_list = get_list_of_countries()
    checksum_date = calculating_date_checksum(date)
    for country in countries_list:
        checksum_country = calculating_country_checksum(country)
        msg_to_send = arrange_msg_to_send(country, date, checksum_date, checksum_country)
        server_msg = connect_to_server(SERVER_IP, SERVER_PORT, msg_to_send)
        if int(get_attacks(server_msg)) > 20:
            countries_in_danger_list += ["country:", country, "   attacks:", get_attacks(server_msg), "\n"]
    return countries_in_danger_list


def arrange_countries_list(countries_in_danger_list):
    """ arrange the list of the countries that in danger
    :param countries_in_danger_list: the list of countries that in danger
    :return: arrange list
    """
    country_list = ""
    for country in countries_in_danger_list:  # casting from tuple to string
        country_list += country
    return country_list


def main():
    SERVER_IP = "52.35.198.18"
    SERVER_PORT = 1050
    country = input("Please enter country name")
    now = datetime.now()
    date = now.strftime("%d/%m/%Y")
    checksum_date = calculating_date_checksum(date)
    checksum_country = calculating_country_checksum(country)
    msg_to_send = arrange_msg_to_send(country, date, checksum_date, checksum_country)
    server_msg = connect_to_server(SERVER_IP, SERVER_PORT, msg_to_send)
    daily_update(date, country, server_msg)


if __name__ == '__main__':
    main()
