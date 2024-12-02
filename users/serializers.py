import phonenumbers
from rest_framework import serializers

from users.models import User


class OTPResponseSerializer(serializers.Serializer):
    message = serializers.CharField()


class UserAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone_number"]

    def validate_phone_number(self, value):
        try:
            phone_number = phonenumbers.parse(value, None)
            if not phonenumbers.is_valid_number(phone_number):
                raise serializers.ValidationError("Invalid phone number.")
        except phonenumbers.phonenumberutil.NumberParseException:
            raise serializers.ValidationError("Invalid phone number.")
        return value
    

class UserCreateSerializer(UserAuthSerializer):
    otp = serializers.IntegerField(min_value=1000, max_value=9999, write_only=True)

    class Meta(UserAuthSerializer.Meta):
        fields = UserAuthSerializer.Meta.fields + ["otp"]


class UserSerializer(serializers.ModelSerializer):
    invitees = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="phone_number",
     )

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields =  ["phone_number", "invite_code", "activated_invite_code", "invitees"]


class UserUpdateSerializer(serializers.ModelSerializer):
    activated_invite_code = serializers.CharField(max_length=6, required=True)

    class Meta:
        fields = ['activated_invite_code']

    def validate_activated_invite_code(self, value):
        if self.instance and self.instance.activated_invite_code:
            raise serializers.ValidationError(
                f"Invite code already activated: {self.instance.activated_invite_code}."
            )
        elif self.invite_code == value or not User.objects.filter(invite_code=value).exists():
            raise serializers.ValidationError('Invalid invite code.')
        return value
    

class UserUpdateSerializer(serializers.ModelSerializer):
    activated_invite_code = serializers.CharField(min_length=6, max_length=6, required=True)

    class Meta:
        model = User
        fields = ['activated_invite_code']

    def validate_activated_invite_code(self, value):
        if self.instance and self.instance.activated_invite_code:
            raise serializers.ValidationError(
                f"Invite code already activated: {self.instance.activated_invite_code}."
            )
        elif self.instance and self.instance.invite_code == value:
            raise serializers.ValidationError("You cannot activate your own invite code.")
        try:
            user = User.objects.get(invite_code=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid invite code.")
        return user