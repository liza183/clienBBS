#-*-coding:utf-8
import sys
import socket
import select
import readline

HOST = '' 
SOCKET_LIST = []
RECV_BUFFER = 4096 
PORT = 9009
user_list_sock2user = {}
user_list_user2sock = {}

def chat_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
 
    # add server socket object to the list of readable connections
    SOCKET_LIST.append(server_socket)
    print(" -----------------------------------\n ")
    print(" clienBBS를 위한 채팅 서버 v 0.1b \n")
    print(" -----------------------------------\n ")
    print(" now listening on port "+ str(PORT)+ " ...\n")

    while True:

        # get the list sockets which are ready to be read through select
        # 4th arg, time_out  = 0 : poll and never block
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
      
        for sock in ready_to_read:
            
            # a new connection request recieved
            if sock == server_socket: 
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                print("사용자 (%s, %s) 가 접속 하였습니다." % addr)
                
                broadcast(server_socket, sockfd, "[%s:%s] 가 접속하였습니다. \n" % addr)
                
            # a message from a client, not a new connection
            else:
                # process data recieved from client, 
                try:
                    # receiving data from the socket.
                    data = sock.recv(RECV_BUFFER)
                    data = data.decode("utf-8")
                    if data:
                        # there is something in the socket
                        print(str(data))
                        if "**cmd**" in data:
                            cmd = data.split(":")[1]
                            arg = data.split(":")[2]
                            
                            if cmd =="who":
                                broadcast_to_self(server_socket, sock, "현재 대화 방의 참가자는 "+ str(list(user_list_user2sock.keys())) +" 입니다.")

                            if cmd =="enter":
                                user_list_sock2user[sock] = arg
                                user_list_user2sock[arg] = sock
                                broadcast_to_self(server_socket, sock, "현재 대화 방의 참가자는 "+ str(list(user_list_user2sock.keys())) +" 입니다.")
                                broadcast(server_socket, sock, arg + " 가 접속 하였습니다.")

                            elif cmd =="quit":
                                broadcast(server_socket, sock, arg + " 가 접속 종료 하였습니다.")
                                try:
                                    del user_list_user2sock[arg]
                                    del user_list_sock2user[sock]
                                    SOCKET_LIST.remove(sock)
                                except:
                                    pass
                        else:
                            broadcast(server_socket, sock, str(data))  
                    else:
                        # remove the socket that's broken    
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)
                            user = user_list_sock2user[sock]
                            del user_list_sock2user[sock]
                            del user_list_user2sock[user]
                        
                            broadcast(server_socket, sock, user + " 가 접속 종료 하였습니다.")
                        
                        # at this stage, no data means probably the connection has been broken
                        #broadcast(server_socket, sock, "사용자 (%s, %s) 가 접속 종료 하였습니다. \n" % addr) 

                # exception 
                except:
                    #broadcast(server_socket, sock, "사용자 (%s, %s) 가 접속 종료 하였습니다. \n" % addr)
                    continue

    server_socket.close()

# broadcast chat messages to all connected clients
def broadcast_to_self (server_socket, sock, message):
    for socket in SOCKET_LIST:
        # send the message only to peer
        if socket != server_socket and socket == sock :
            try :
                socket.send(bytes(message, 'utf-8'))
            except :
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)

# broadcast chat messages to all connected clients
def broadcast (server_socket, sock, message):
    for socket in SOCKET_LIST:
        # send the message only to peer
        if socket != server_socket and socket != sock :
            try :
                socket.send(bytes(message, 'utf-8'))
            except :
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)
 
if __name__ == "__main__":

    sys.exit(chat_server())         
