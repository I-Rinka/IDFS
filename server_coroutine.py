import socket
import re
from threading import Thread


def service_client(new_socket):
    # 接受浏览器发过来的http请求
    # GET / HTTP/1.1
    request = new_socket.recv(1024).decode("utf-8")
    # print(request)
    request_lines = request.splitlines()
    req = re.match(r"[^/]+(/\S*)", request_lines[0])
    file_name: str = ""
    if req:
        file_name = req.group(1)
        if file_name == "/":
            file_name = "/index.html"
        print(file_name)
    # print(request_lines)
    # 返回http响应

    try:
        with open("./html" + file_name, "r", encoding="utf-8") as f:
            resposne = "HTTP/1.1 200 OK\r\n"
            resposne += "\r\n"
            # resposne += "<h1>hello world</h1>"
            resposne += f.read()
    except Exception as e:
        resposne = "HTTP/1.1 400 NOT FOUND\r\n"
        resposne += "\r\n"
        resposne += "--file not found--"

    new_socket.send(resposne.encode("utf-8"))
    # new_socket.send(body)
    # 关闭套接字
    new_socket.close()


def main():
    # 创建套接字
    http_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 防止端口被占用无法启动程序
    http_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 绑定端口
    http_server.bind(("", 80))
    # 变为监听套接字
    http_server.listen(128)
    while True:
        # 等在新客户端连接
        client, info = http_server.accept()
        # 开启一个子线程为这个客户端服务
        p = Thread(target=service_client, args=(client,))
        p.start()


if __name__ == "__main__":
    main()