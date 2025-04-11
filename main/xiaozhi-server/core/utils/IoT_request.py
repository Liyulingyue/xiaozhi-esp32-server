import socket

def get_IoT_query(query: str) -> str:
    """从 IoT 获取, 并生成提示词"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # 连接到 IoT 服务器
            s.connect(('localhost', 8092))
            # 发送查询请求
            s.sendall(query.encode('utf-8'))
            # 接收响应数据
            data = s.recv(1024).decode('utf-8')
            if not data:
                raise ConnectionError("服务器关闭连接或未返回数据")
            # 关闭连接
            s.close()
            return data
    except (ConnectionRefusedError, BrokenPipeError, ConnectionResetError) as e:
        if data is not None and data != "":
            return data
        print(f"连接失败: {e}")
        return "连接失败，请稍后重试"

