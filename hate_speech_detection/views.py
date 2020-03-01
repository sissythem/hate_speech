import logging
from os.path import join
import subprocess
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from hate_speech.settings import BASE_DIR
from hate_speech_detection.serializers import UserSerializer

logger = logging.getLogger(__name__)


class UserView(viewsets.GenericViewSet):
    permission_classes = (permissions.AllowAny,)

    @action(methods=["post"], detail=False, url_name="register", url_path="register")
    def register(self, request, *args, **kwargs):
        try:
            username = request.data["username"]
            password = request.data["password"]
            first_name = request.data["first_name"] if "first_name" in request.data.keys() else None
            last_name = request.data["last_name"] if "last_name" in request.data.keys() else None
            user = User(username=username, password=password, is_superuser=False, first_name=first_name,
                        last_name=last_name)
            user.save()
            serializer = UserSerializer(user, many=False, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (KeyError, Exception) as e:
            logger.error(e)
            return Response("Error while creating user", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=["post"], detail=False, url_name="login", url_path="login")
    def login(self, request, *args, **kwargs):
        try:
            username = request.data["username"]
            password = request.data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request=request, user=user)
                serializer = UserSerializer(user, many=False, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
        except (KeyError, Exception) as e:
            logger.error(e)
            return Response("Error while trying to login! {}".format(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Create your views here.
class NlpSemanticAugmentationView(viewsets.GenericViewSet):
    permission_classes = (permissions.AllowAny,)

    @action(methods=["post"], detail=False, url_name="exec_nlp", url_path="exec_nlp")
    def run_nlp_semantic_augmentation(self, request, *args, **kwargs):
        file = request.FILES['file']
        lines = file.readlines()
        nlp_folder = join(BASE_DIR, "nlp-semantic-augmentation")
        file_path = join(nlp_folder, "config.yml")
        with open(file_path, "w") as f:
            f.writelines(lines)
        command = "cd nlp-semantic-augmentation && python main.py config.yml"
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        output, error = process.stdout, process.stderr
        if not error:
            return Response(output, status=status.HTTP_200_OK)
        else:
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
