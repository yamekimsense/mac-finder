# python3
# find MAC all switch together
import time, paramiko

iii = input("Put last 4 digits of MAC as ****? ")

x = open("switch.txt", 'r')

while True:
    line = x.readline()

    if not line:
        break

    line = line.split(",")

    ip = line[0].strip('\n')
    username = line[1].strip('\n')
    password = line[2].strip('\n')

    remote_conn_pre = paramiko.SSHClient()
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    remote_conn_pre.connect(ip, port=22, username=username,
                            password=password,
                            look_for_keys=False, allow_agent=False)

    remote_conn = remote_conn_pre.invoke_shell()
    time.sleep(0.1)
    output = remote_conn.recv(65535)

    remote_conn.send("terminal length 0\n")
    time.sleep(0.1)
    output = remote_conn.recv(65535)

    remote_conn.send("show mac address-table | inc " + iii + "\n")
    time.sleep(0.1)
    output = remote_conn.recv(65535)
    length = len(output)

    if length < 70:
        a = 0
        print ("There is no such a MAC on " + ip)

    if length > 70:
        output = str(output, 'utf-8')

        f = open("temp.txt", 'w')
        f.write(output)
        f.close()

        f = open("temp.txt", 'r')
        line0 = f.readline()
        line1 = f.readline()
        f.close()

        line1 = line1.replace("     ", " ")
        line1 = line1.replace("    ", " ")
        line1 = line1.replace("    ", " ")
        line1 = line1.replace("  ", " ")
        line1 = line1.replace("  ", " ")
        line1 = line1.replace("  ", " ")
        line1 = line1.replace("  ", " ")
        line1 = line1.replace("  ", " ")
        line1 = line1.replace("  ", " ")
        line1 = line1.split(" ")

        port = line1[4].strip('\n')
        print ("MAC " + line1[2].strip('\n') + " is connected port " + port + " of " + ip)

        ### port des
        command_des = "show run interface " + port + " | inc des\n"
        remote_conn.send(command_des)
        time.sleep(0.1)
        output_des = remote_conn.recv(65535)
        output_des = str(output_des, 'utf-8')

        f = open("temp1.txt", 'w')
        f.write(output_des)
        f.close()

        f = open("temp1.txt", 'r')
        line0 = f.readline()
        line1 = f.readline()
        line2 = f.readline()
        f.close()

        print ("host name is", line2)
        print (line1)

x.close()
