from rest_framework.throttling import SimpleRateThrottle


class CustomIPThrottle(SimpleRateThrottle):
    scope = "custom_ip"

    def get_cache_key(self, request, view):
        return self.get_ident(request)  # 以 IP 為 key 限制
