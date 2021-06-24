from rest_framework.views import APIView
from .definations import *
from rest_framework import response, status

class Contribute(APIView):
    '''
    Contributors API Allows additon of contributors to the database
    '''
    throttle_scope = 'common'

    def post(self, request, **kwargs) -> response.Response:
        """Adding Contributors to Projects

        Args:
            request

        Returns:
            response.Response
        """
        pass


class Maintainer(APIView):
    '''
    Maintainer API to Allow addition of maintainers to the database 
    '''
    throttle_scope = 'common'

    def post(self, request, **kwargs):
        validate = CommonSchema(request.data, headers={
            "path_info": request.path_info
        }).valid()
        if 'error' not in validate:
            return response.Response(validate, status=status.HTTP_200_OK)
        return response.Response(validate.get('error'), status=status.HTTP_400_BAD_REQUEST)
