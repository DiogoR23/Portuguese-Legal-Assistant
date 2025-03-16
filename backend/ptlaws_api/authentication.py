from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Users
import uuid

class CassandraJWTAuthentication(JWTAuthentication):
    """Custom Authentication for SimpleJWT in Cassandra."""

    def get_user(self, validated_token):
        user_id = validated_token.get("user_id")

        if not user_id:
            return None
        
        user_id = uuid.UUID(user_id)

        user = Users.objects.filter(id=user_id).first()
        if user:
            return user

        return None