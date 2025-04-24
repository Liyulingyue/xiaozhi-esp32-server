import socket
from config.logger import setup_logging

TAG = __name__

logger = setup_logging()

def get_IoT_query(query: str) -> str:
    """从 IoT 获取, 并生成提示词"""

    logger.bind(tag=TAG).info(f"从 IoT 获取数据: {query}")
    # return "今天湿度：20%，温度：30度，天气：晴天，风速：10km/h，空气质量：良好。"
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(120) # 设置连接超时时间，单位为秒
            logger.bind(tag=TAG).info("连接到 IoT 服务器")
            # 连接到 IoT 服务器
            s.connect(('localhost', 8092))
            logger.bind(tag=TAG).info("连接成功")
            logger.bind(tag=TAG).info(f"发送查询请求: {query}")
            # 发送查询请求
            s.sendall(query.encode('utf-8'))
            logger.bind(tag=TAG).info("请求发送成功")
            # 接收响应数据
            logger.bind(tag=TAG).info("接收响应数据")
            data = s.recv(1024).decode('utf-8')
            logger.bind(tag=TAG).info(f"接收数据: {data}")
            if not data:
                logger.bind(tag=TAG).error("服务器关闭连接或未返回数据")
                raise ConnectionError("服务器关闭连接或未返回数据")
            logger.bind(tag=TAG).info("接收数据成功")
            # 关闭连接
            s.close()
            logger.bind(tag=TAG).info("关闭连接成功")
            return data
    except (ConnectionRefusedError, BrokenPipeError, ConnectionResetError) as e:
        if data is not None and data != "":
            return data
        logger.bind(tag=TAG).error(f"连接失败, 错误信息: {e}")
        return "连接失败，请稍后重试"
    except socket.timeout:
        logger.bind(tag=TAG).error("连接或返回数据超时")
        return "连接或返回数据超时，请稍后重试"

