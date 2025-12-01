from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


class BearerTokenAuthentication(TokenAuthentication):
    """
    自定义认证类，支持Bearer令牌格式
    """
    keyword = 'Bearer'
    
    def authenticate_credentials(self, key):
        try:
            # 尝试使用Bearer格式
            print(super().authenticate_credentials(key))
            return super().authenticate_credentials(key)
        except AuthenticationFailed:
            # 如果失败，回退到Token格式
            self.keyword = 'Token'
            try:
                return super().authenticate_credentials(key)
            finally:
                # 恢复原始关键字
                self.keyword = 'Bearer'