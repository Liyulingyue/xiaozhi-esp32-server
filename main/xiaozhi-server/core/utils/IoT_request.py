import socket
import time
from config.logger import setup_logging

TAG = __name__

logger = setup_logging()

def get_IoT_query(query: str) -> str:
    """从 IoT 获取, 并生成提示词"""

    logger.bind(tag=TAG).info(f"从 IoT 获取数据: {query}")
    
    # 设置超时时间（秒）
    timeout = 120
    
    try:
        start_time = time.time()
        
        logger.bind(tag=TAG).info(f"尝试连接到 IoT 服务器 (localhost:8092)，超时时间: {timeout}秒")
        
        # 使用阻塞模式但设置超时
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # 直接设置超时，这样连接操作也会受到超时限制
            s.settimeout(timeout)

            # 尝试连接
            s.connect(('localhost', 8092))

            conn_time = time.time() - start_time
            logger.bind(tag=TAG).info(f"连接成功！用时: {conn_time:.2f}秒")
            
            # 发送查询请求
            logger.bind(tag=TAG).info(f"发送查询请求: {query}")
            s.sendall(query.encode('utf-8'))
            logger.bind(tag=TAG).info("请求发送成功")
            
            # 接收响应数据
            logger.bind(tag=TAG).info("接收响应数据")
            data = s.recv(1024).decode('utf-8')
            logger.bind(tag=TAG).info(f"接收数据: {data}")
            
            if not data:
                logger.bind(tag=TAG).error("服务器关闭连接或未返回数据")
                return "服务器未返回数据"
            return data

    except socket.timeout:
        logger.bind(tag=TAG).error(f"连接超时（{timeout}秒）")
        return "连接超时，请稍后重试"

    except ConnectionRefusedError:
        logger.bind(tag=TAG).error("连接被拒绝，服务器可能未运行")
        return "连接被拒绝，请确认服务器是否运行"

    except (BrokenPipeError, ConnectionResetError) as e:
        logger.bind(tag=TAG).error(f"连接中断: {e}")
        return "连接异常中断，请稍后重试"

    except Exception as e:
        logger.bind(tag=TAG).error(f"未预期的错误: {str(e)}")
        return f"连接错误: {str(e)}"
