from rest_framework import serializers as s

from users.models import User


class PhoneSerializer(s.Serializer):
    phone = s.RegexField(r'^[\+]?[0-9]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$', min_length=12,
                         max_length=20)


class SMSVerificationSerializer(s.Serializer):
    sms_token = s.CharField(required=False)
    sms_code = s.CharField(max_length=4, min_length=4)


class UserSerializer(s.ModelSerializer):
    invited_users_phones = s.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'phone', 'invite_code', 'invited_by', 'invited_users_phones')

    def get_invited_users_phones(self, obj: User):
        return obj.invite_users.values_list('phone', flat=True)


class SetInvitationSerializer(s.Serializer):
    invite_code = s.CharField(max_length=6)
