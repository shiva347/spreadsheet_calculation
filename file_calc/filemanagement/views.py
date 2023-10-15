from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from .models import FileRequest
from .tasks import perform_calculations


class FileUploadView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request):
        file = request.data['file']
        if file.name.endswith(('.csv', '.xlsx')):
            # Save the request and file to the database
            request_instance = FileRequest.objects.create(user=request.user, file=file)
            # request_instance.save()

            # Start asynchronous calculations
            perform_calculations.delay(request_instance.id)

            return Response(
                {"message": "File uploaded and calculations started."},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"error": "Invalid file format. Only CSV and XLSX files are allowed."},
                status=status.HTTP_400_BAD_REQUEST
            )
