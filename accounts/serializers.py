
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField( required=True)  
    last_name = serializers.CharField( required=True) 
    email = serializers.CharField( required=True)    
    password = serializers.CharField(write_only=True, required=True) 
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']  # Include password in the fields

    def create(self, validated_data):
        # Remove password from validated_data (it will be handled separately)
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)  # Create a user with the validated data (password will be hashed)
        user.set_password(password)  # Manually set the password to ensure it's hashed
        user.save()  # Save the user object
        return user
    
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)  # Get the password, if provided
        
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Update the password if it's provided
        if password:
            instance.set_password(password)  # Hash the new password
        instance.save()
        return instance