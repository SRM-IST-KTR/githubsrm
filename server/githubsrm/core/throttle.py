from rest_framework import throttling


class PostThrottle(throttling.AnonRateThrottle):
    scope = "post_throttle"

    def allow_request(self, request, view):
        if request.method == "GET":
            return True
        return super().allow_request(request, view)
