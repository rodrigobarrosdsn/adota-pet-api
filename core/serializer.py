"""_summary_

Raises:
    serializers.ValidationError: _description_
    serializers.ValidationError: _description_

Returns:
    _type_: _description_
"""
from rest_framework import serializers
from .models import Animal, User
from drf_base64.fields import Base64ImageField
# pylint: disable=W0237


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.

    Args:
        serializers.ModelSerializer: The base model serializer class.

    Returns:
        dict: The validated user data.

    Attributes:
        old_password (serializers.CharField): A write-only field for the old password.
        email (serializers.EmailField): A required email field.
    """

    old_password = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(required=True)
    imagem_perfil = Base64ImageField(required=False)
    # cpf = serializers.CharField(required=True)

    # def validate(self, data):
    #     """
    #     Validate the creation of a user.

    #     Args:
    #         data (dict): The user data to validate.

    #     Returns:
    #         dict: The validated user data.

    #     Raises:
    #         serializers.ValidationError: If any required field is missing.
    #     """
    #     for field in self.fields:
    #         if self.fields[field].required and field not in data:
    #             raise serializers.ValidationError(f"{field} field is required.")

    #     return data

    def create(self, validated_data):
        """_summary_

        Args:
            validated_data (_type_): _description_

        Returns:
            _type_: _description_
        """
        password = validated_data.pop('password')

        validated_data['is_active'] = True

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        old_password = validated_data.pop('old_password', None)

        if password is not None and not instance.check_password(old_password):
            raise serializers.ValidationError({'detail': 'Senha inválida'})

        # Update other fields
        for key, value in validated_data.items():
            setattr(instance, key, value)

        # Update password if provided
        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance

    class Meta:
        """_summary_
        """
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True},
                        'old_password': {'write_only': True}}
        read_only_fields = ('id',)


class AnimalSerializer(serializers.ModelSerializer):
    """
    _summary_
    """

    user_obj = serializers.SerializerMethodField()
    imagem_perfil = Base64ImageField(required=False)
    imagem_detalhe = Base64ImageField(required=False)
    imagem_capa = Base64ImageField(required=False)

    def get_user_obj(self, obj):
        """
        _summary_

        Args:
            obj (_type_): _description_

        Returns:
            _type_: _description_
        """
        if obj.user:
            return UserSerializer(obj.user).data
        return None

    class Meta:
        """
        _summary_
        """
        model = Animal
        fields = '__all__'


class UserAnimalSerializer(serializers.ModelSerializer):
    # Defina os campos desejados para o serializer aqui
    class Meta:
        model = Animal
        fields = '__all__'
