# Author: Wenjie Xi, Jun Wang
# Upated Date: 10/3/2019
# DNS client

import socket as s
import struct
import os

# encode the message
def encode(hostname):
    print("Preparing DNS query..")
    req_id = os.urandom (2) # create a identifier
    header = struct.pack("!2s10B",req_id,1,0,0,1,0,0,0,0,0,0)
    quest = b''
    for n in hostname.split("."):
        n = bytes(n,encoding="utf-8")
        quest += struct.pack("!B",len(n))+n
    quest += struct.pack("!BHH",0,1,1)
    mes_1 = header + quest
    req_id = struct.unpack("!H",req_id)
    return mes_1, quest, req_id

# send the request message to DNS server by UDP
def sender(message):
    print("Sending DNS query..")
    ip = '8.8.8.8'
    port = 53   
    socket.sendto(message,(ip,port))

def printer(req_id):
    print("Processing DNS response..")
    print("--------------------------")
    print("hearder.ID = %d" % req_id )
    print("header.QR = 0" )
    print("header.OPCODE = 0")
    print("header.RD = 1")
    print("header.QDCOUNT = 1")
    print("--------------------------")
    print("question.QNAME = %s" % hostname)
    print("question.QTYPE = A" )
    print("question.QCLASS = IN")


def decode(data, addr):
    (transaction_id,flags,num_questions,answer_rrs,authority_rrs,additional_rrs)\
        = struct.unpack("!HHHHHH",data[:12])
    data_resp = data[12:]

    # First we print some general information of response send from dns server
    print('=========== Response ===========')
    print('Trasaction ID: ',transaction_id)
    print('Flags: ',hex(flags))
    if flags == 0x8183:  # No such hostname
        print('(No such hostname!)')
    if flags == 0x8180:
        print('(No error)')
    print('Questions: ',num_questions)
    print('Answer RRs: ',answer_rrs)
    print('Authority RRs: ',authority_rrs)
    print('Additional RRs: ',additional_rrs)
    whole_resp = data_resp[len(quest):]

    if authority_rrs == 0:
        # If we have over one questions, we should print them all
        for num in range(int(len(whole_resp)/16)):
            resp = whole_resp[(num*16):(16*(num+1))]
            (offset, Atype, rclass, ttl, data_len, ip1, ip2, ip3, ip4)\
                = struct.unpack('!HHHLHBBBB', resp[:struct.calcsize('!HHHLHBBBB')])
            print('=========== Answer', num+1,'===========')
            print('answer.NAME = ', hostname)
            if Atype == 1:
                print('answer.TYPE = A')
            if rclass == 1:
                print('answer.CLASS = IN')
            print('answer.TTL = ',ttl)
            print('answer.RDLENGTH = ',data_len)
            print('answer.RDATA = ',ip1,'.',ip2,'.',ip3,'.',ip4,sep='')

    # condition if we have authoritative answers
    elif authority_rrs > 0:
            resp = whole_resp[:12]
            (offset, Atype, rclass, ttl, data_len)\
                = struct.unpack('!HHHLH', resp[:struct.calcsize('!HHHLH')])

            print('=========== Authoritative nameservers 1','===========')
            if offset == 49164:
                print('answer.NAME = ', hostname)
            if flags == 0x8183:  # No such hostname
                if offset != 49164:  # If we have no such hostname we start from TLD
                    print('answer.NAME = ', hostname.split(".")[-1])
            if Atype == 6:  # This is for SOA
                print('answer.TYPE = SOA')
            if rclass == 1:  # We just care about class = 1
                print('answer.CLASS = IN')
            print('answer.TTL = ',ttl)
            print('answer.RDATA = ',data_len)

            # Try to get authoritative nameservers
            nameserver = ''
            n = 12
            i = whole_resp[n]
            while i != 192 and ('net.' not in nameserver) and ('edu.' not in nameserver):
                nameserver += str(whole_resp[(n+1):(n+1+i)], encoding = 'utf-8') + '.'
                n = n + 1 + i
                i = whole_resp[n]
            # if our nameserver have end by com, we add com to it or we pass it
            if i == 192:
                nameserver += 'com'
            else:
                nameserver = nameserver[0:-1]
            print('Primary name server: ', nameserver)

    # If we get additional records
    elif additional_rrs > 0:
        data_additional = data[-39*additional_rrs]
        for num in range(int(len(data_additional)/39)):
            data_additional_iter = data_additional[(num*39):((num+1)*39)]
            add_name = data_additional_iter[num*39]
            print('=========== Additional records', num+1,'===========')
            if add_name == 0:
                print('Name: <Root>')
            add_type = struct.unpack('!H', data_additional_iter[num*39+1:num*39+3])[0] # We get Type number
            if add_type == 41:
                print('Type: OPT')
            add_UDP_payload_size = struct.unpack('!H', data_additional_iter[num*39+3:num*39+5])[0] # We get UDP payload size
            print('UDP payload size:', add_UDP_payload_size)


if __name__ == "__main__":
    hostname = input('Please enter the hostname: ')
    if hostname[:3] == 'www':          # We accept hostname without www
        hostname = hostname[4:]
    message, quest, req_id = encode(hostname)
    socket = s.socket(s.AF_INET,s.SOCK_DGRAM)
    print("Contacting DNS server..")
    socket.settimeout(5000)      # We set our timeout to 5 sec
    sender(message)
    t = 1 # creat the time pings
    while t < 4:
        print('DNS response received (attempt ', t, ' of 3)', sep='')
        try:
            data, addr = socket.recvfrom(512)  # limitation is 512
            t = 5
        except:
            t += 1
    if t == 4:  # Does not get the response, try again, after 3 times leave loop
        print("Error, This DNS request is timeout!")
    if t == 5:
        printer(req_id)
        decode(data, addr)
    socket.close()







	
