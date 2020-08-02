#python3
#find MAC step by step
#added port desc

import time, paramiko

iii = input ("Put last 4 digits of MAC as ****? ")
ip = input ("start switch ip address? ")

username = "cisco"
password = "cisco"

while True:
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
        print ("There is no such a MAC. Check it out.")
        break

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
    command = "show cdp neighbors " + port + " detail | inc IP address\n"

# port des
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

# CDP
    remote_conn.send(command)
    time.sleep(0.1)
    output2 = remote_conn.recv(65535)

    remote_conn.send("exit\n")
    time.sleep(0.1)
    output3 = remote_conn.recv(65535)

    length = len(output2)

    if length < 70:
        break

    output2 = str(output2, 'utf-8')

    f = open("temp.txt", 'w')
    f.write(output2)
    f.close()

    f = open("temp.txt", 'r')
    line0 = f.readline()
    line1 = f.readline()
    f.close()

    line1 = line1.split(":")
    line2 = line1[1].strip(" ")
    ip = line2.strip('\n')

    print ("                     ")
    print ("Now connecting another switch ", ip)
