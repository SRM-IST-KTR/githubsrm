import os
import time

import psutil
from django.http import JsonResponse

from .utils import api_view


@api_view(["GET"])
def health_check(request) -> JsonResponse:
    """Get Process UpTime

    Args:
        request
    """
    uptime = time.time() - psutil.Process(os.getpid()).create_time()
    return JsonResponse(
        {"uptime": uptime, "status": "OK", "timeStamp": time.time()}, status=200
    )
