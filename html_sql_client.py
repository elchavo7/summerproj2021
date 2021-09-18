__author__ = 'Yossi'

import os
import socket
import webbrowser
import threading
from tcp_by_size import send_with_size, recv_by_size


def sent_to_html(data):
    file_name = "iemp.html"
    with open(file_name, 'w') as file:
        file.write(f"<head> {data} <br> "
                   f"<button onclick='self.close()'>Close</button>"
                   f"</head>")
    print(os.path.realpath(file_name))
    os.system(f"start iemp.html")


def recieve_full_spece():
    serial_num = input("Enter serial num > ")
    brand_name = input("Enter brand name > ")
    gpu = input("Enter gpu > ")
    ram = input("Enter ram > ")
    storage = input("Enter storage > ")
    is_mobile_bool = input("Enter if mobile (True/False) > ")
    if is_mobile_bool == "True":
        is_mobile = 1
    else:
        is_mobile = 0
    return [serial_num, brand_name, gpu, ram, storage, is_mobile]


def update_computer_query():
    specs_dict = {"1": "gpu", "2": "ram", "3": "storage"}
    serial = input("[?] What is the serial num of the computer\n[?] you wish to modify? ")
    print("[?] What will you wish to modify?\n"
          "[1] gpu\n"
          "[2] ram\n"
          "[3] storage")
    change_option = input("[?] 1 / 2 / 3 >> ")
    while change_option != "1" and change_option != "2" and change_option != "3":
        print("[-] Mmmmm, WHAT?")
        change_option = input("[?] 1 / 2 / 3 >>")
    change_option = specs_dict[change_option]
    the_change = input("[?] what do you wish to change for? ")
    return change_option + "|" + the_change + "|" + serial


def manu():
    print ("1. Update Computer\n" + \
          "2. Insert Computer\n" + \
          "3. Delete Computer\n" + \
          "4. Get All Computer\n>" +\
          "5. Get Computer\n>" +\
          "9. exit\n\n>")

    data = input("Enter Num> ")

    if data == "9":
        return "q"
    elif data == "1":
        specs = update_computer_query()
        return "UPDCOM|" + specs
    elif data == "2":
        specs = recieve_full_spece()
        return "INSCOM|" + "|".join(str(elem) for elem in specs)
    elif data == "3":
        pc_id = input("pc to delete serial num > ")
        return "DELCOM|" + str(pc_id)
    elif data == "4":
        pc_type = input("1. All Computers\n" + \
                        "2. laptops\n" + \
                        "3. station\n")
        return "GETALL|" + str(pc_type)
    elif data == "5":
        pc_id = input("pc to get serial num > ")
        return "GETCOM|" + str(pc_id)
    else:
        return "RULIVE"


def handle_recieve(data):
    if data == "":
        print("seems server DC")
        return
    print("Got>>" + "\n".join(data.split("|")))
    sent_to_html("<br>".join(("\n".join(data.split("|"))).split("\n")))


def main():

    cli_s = socket.socket()
    cli_s.connect(("127.0.0.1", 33445))
    print("[+] Connected to server!")

    while True:
        data = manu()

        if data == "q":
            break
        send_with_size(cli_s, data)
        data = recv_by_size(cli_s)
        handle_recieve(data)



if __name__ == '__main__':
    main()