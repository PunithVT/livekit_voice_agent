import os
import logging
from datetime import datetime
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .storage_backends import upload_to_s3

logger = logging.getLogger(__name__)

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
@permission_classes([AllowAny])
def upload_file(request):
    """
    Handle file upload to S3 bucket (No authentication required)
    """
    try:
        if 'file' not in request.FILES:
            return Response(
                {'error': 'No file provided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        file_obj = request.FILES['file']
        file_name = request.data.get('file_name', file_obj.name)
        
        # Add timestamp to filename to avoid collisions
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        file_extension = os.path.splitext(file_name)[1]
        unique_filename = f"{os.path.splitext(file_name)[0]}_{timestamp}{file_extension}"
        
        # Upload to S3
        try:
            file_url = upload_to_s3(file_obj, unique_filename)
            return Response({
                'url': file_url,
                'file_name': unique_filename,
                'message': 'File uploaded successfully'
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Error uploading file: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return Response(
            {'error': 'An unexpected error occurred'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )