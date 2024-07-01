import jwt
import secrets

from django.shortcuts import redirect, render

from rest_framework import status, generics
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User
from rest_framework.permissions import IsAuthenticated
from users.serializers import *
from users.services import create_bearer_token, create_sms_token


class AuthenticationView(APIView):
    template_login = 'users/login.html'
    template_sms_conf = 'users/sms_conf.html'

    def get(self, request):
        if request.query_params.get('sms_confirmation'):
            if request.session.get('sms_token'):
                return render(request, self.template_sms_conf, context={})
            return redirect('users:login')
        return render(request, self.template_login, context={})

    def post(self, request):
        if request.query_params.get('sms_confirmation'):
            return self.verify_sms(request)
        return self.attempt_auth(request)

    def attempt_auth(self, request):
        serializer = PhoneSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            sms_token = create_sms_token(serializer.data)

            if request.accepted_media_type == 'application/json':
                return Response(status=status.HTTP_200_OK, data={
                    'sms_token': sms_token,
                    'url_to_next': request.stream.path + '?sms_confirmation=1',
                    'fields_to_be_required': ['sms_code']
                })

            request.session['sms_token'] = sms_token
            return redirect('/users/login?sms_confirmation=1')

    def verify_sms(self, request):
        serializer = SMSVerificationSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            sms_token = serializer.data.get('sms_token') or request.session.get('sms_token')

            token = sms_token
            payload = jwt.decode(token, '', algorithms=["HS256"])

            return self.authorize(request, payload['credentials'])

    def authorize(self, request, credentials):
        phone = credentials['phone']
        obj = User.objects.filter(phone=phone).first()
        if not obj:
            inv_code = secrets.token_hex(3)
            user, created = User.objects.get_or_create(phone=phone, invite_code=inv_code)
            user.save()

        token = create_bearer_token(user)
        return Response({
            'message': 'Вы прошли аутенфикацию!',
            'bearer_token': token
        })


class ProfileView(RetrieveModelMixin, generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, pk=None):
        if pk is None:
            self.kwargs['pk'] = request.user.id
            return self.retrieve(request)

        return self.retrieve(request)


class ListProfileView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class InvitationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SetInvitationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            invite_code = serializer.data.get('invite_code')
            referral_user = User.objects.filter(invite_code=invite_code).first()
            request.user.invited_by = referral_user
            request.user.save()
            return Response(UserSerializer(request.user).data)
