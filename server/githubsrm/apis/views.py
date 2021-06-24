from rest_framework.views import APIView
from .definations import *


class Contribute(APIView):
    '''
    Contributors API Allows additon of contributors to the database
    '''
    throttle_scope = 'contributor'
    pass 
