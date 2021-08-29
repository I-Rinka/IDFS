import local as tsk
from concurrent.futures import thread as th
import socket,re
def open_file(路径):
    # """ 读取文件 """
    # try:
    #     client_html_data=open(路径,'rb')
    # except :
    #     return '404 页面不存在\r\n您输入的地址有误,请重新输入'.encode('gbk')
    # else:
    #     html_read_data=client_html_data.read()
    #     print(html_read_data)
    #     client_html_data.close()
    #     return html_read_data
    return "你好"

def client(new_client_socket):
    ''' 负责服务客户端 '''
    print('正在等待浏览器发送信息')
    recv_data=new_client_socket.recv(10240).decode('utf-8')
    print(recv_data)
    ret_filename_=re.search(r'\w+\.html',recv_data)
    if ret_filename_:
        client_html_filename=ret_filename_.group()
        print(client_html_filename)
        file_data=open_file('python_demo/HTTP协议/'+client_html_filename)
    else:
        file_data=open_file('python_demo/HTTP协议/index.html')

    return_web= 'HTTP/1.1 200 OK\r\n\r\n' # 这个必须要在行首给出
    new_client_socket.send( return_web.encode('utf-8'))
    new_client_socket.send( file_data)
    new_client_socket.close()
    print('客户端链接已断开')
    print('---------------正在等待新的客户端链接---------------')
 
 
def main():
    ''' 负责监听客户端链接 '''
    print('-------------------服务端已运行-------------------')
    while True:
        print('正在等待客户端链接')
        new_client_socket,clientAddr=tcp_socket_sever.accept()
        print('链接成功,客户端ip与端口:',clientAddr)
        requests = thp.submit(client,(new_client_socket,))
        # threadpool.makeRequests(client,(new_client_socket,))
        # for req in requests:
        #     tpo.putRequest(req)
 
 
def input_ip_port():
    ip_=input('请输入服务端使用的ip地址')
    port=int(input('请输入服务端要使用的端口号'))
    tcp_socket_sever.bind((ip_,8001))
    tcp_socket_sever.listen(128)
 
 
if __name__ == '__main__':
    tcp_socket_sever=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    thp=th.ThreadPoolExecutor(3)
    input_ip_port()
    main()
    # tpo.wait()