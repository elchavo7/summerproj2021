__author__ = 'Yossi'
import socket
import SQL_ORM
import Queue, threading, time, random
from tcp_by_size import send_with_size, recv_by_size
import sys, os
DEBUG = True
exit_all = False


def handl_client(sock, tid, db):
    global exit_all
    
    print("New Client num " + str(tid))
    
    while not exit_all:
        try:
            data = recv_by_size(sock)
            if data == "":
                print( "Error: Seens Client DC")
                break

            to_send = do_action(data, db)

            send_with_size(sock, to_send)

        except socket.error as err:
            if err.errno == 10054:
                #'Connection reset by peer'
                print("Error %d Client is Gone. %s reset by peer." % (err.errno, str(sock)))
                break
            else:
                print("%d General Sock Error Client %s disconnected" % (err.errno, str(sock)))
                break

        except Exception as err:
            print("General Error:", err)
            print(sys.exc_info()[0].__name__, os.path.basename(sys.exc_info()[2].tb_frame.f_code.co_filename), sys.exc_info()[
                2].tb_lineno)

            break
    sock.close()


def do_action(data, db):
    """
    check what client ask and fill to send with the answer
    """
    to_send = "Not Set Yet"
    action = data[:6]
    data = data[7:]
    fields = data.split('|')

    if DEBUG:
        print("Got client request " + action + " -- " + str(fields) )

    if action == "INSCOM":
        #computer = SQL_ORM.Computer(fields[0], fields[1], fields[2], fields[3], fields[4], fields[5])
        if db.insert_computer(fields[0], fields[1], fields[2], fields[3], fields[4], fields[5]):
            to_send = "INSCOM|" + "Success"
        else:
            to_send = "INSCOM|" + "Error"

    elif action == "DELCOM":
        if db.delete_computer(data):
            to_send = "DELCOMP|" + "success"
        else:
            to_send = "DELCOMP|" + "Error seems like there no such pc"
    elif action == "UPDCOM":
        if db.update_computer(data):
            to_send = "UPDCOMP|" + "success"
        else:
            to_send = "DELCOMP|" + "Error seems like there no such pc"
    elif action == "GETALL":
        all_computers = db.GetComputers(data)
        print("all computer: " + "|".join(str(elem) for elem in all_computers))
        d = []
        for pc in all_computers:
            d.append(", ".join(str(elem) for elem in pc))
        d = "Pc: " + "\nPc: ".join(d)
        to_send = "TAKALL|" + str(d)
        print("sent: " + to_send)
    elif action == "GETCOM":
        computer = db.GetComputer(data)[0]
        computer = ", ".join(str(elem) for elem in computer)
        d = "PC: " + computer
        to_send = "TAKCOM|" + str(d)
    elif action == "RULIVE":
        to_send = "RULIVER|"+ "yes i am a live server"

    else:
        print ("Got unknown action from client " + action)
        to_send = "ERR___R|001|" + "unknown action"

    return to_send


def q_manager(q, tid):
    global exit_all
    
    print ("manager start:" + str(tid))
    while not exit_all:
        item = q.get()
        print ("manager got somthing:" + str(item))
        # do some work with it(item)



        q.task_done()
        time.sleep(0.3)
    print ("Manager say Bye")
    

def main():
    global exit_all
    
    exit_all = False
    db = SQL_ORM.ComputerAppORM()
    
    s = socket.socket()
    
    q = Queue.Queue()

    q.put("Hi for start")
    
    
    manager = threading.Thread(target=q_manager, args=(q, 0))

    
    s.bind(("0.0.0.0", 33445))

    s.listen(4)
    print ("after listen")

    threads = []
    i = 1
    while True:
        cli_s , addr = s.accept()
        print("[+] Connected")
        t = threading.Thread(target =handl_client, args=(cli_s, i,db))
        t.start()
        i += 1
        threads.append(t)



    exit_all = True
    for t in threads:
        t.join()
    manager.join()
    
    s.close()


if __name__ == '__main__':
    main()
