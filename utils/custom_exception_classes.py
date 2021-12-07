from rest_framework.exceptions import PermissionDenied
from rest_framework import status


class CustomError(PermissionDenied):
    "this helps me Return a custom error any time i want(freely) all i need is to raise the code"

    def __init__(self, message, status_code=status.HTTP_400_BAD_REQUEST):
        self.detail =  {
            "success":False,
            "message":message,
            'status':'failure','status_code':status_code}

        self.status_code= status_code