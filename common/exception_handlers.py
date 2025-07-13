import logging
from rest_framework import status
from rest_framework.response import Response

logger = logging.getLogger(__name__)

def handle_unexpected_error(error, error_message):
    logger.error(f"{error_message}: {error}")
    error = {"error": error_message}
    return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        
