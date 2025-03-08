from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django_cassandra_engine.models import DjangoCassandraModel
from cassandra.cqlengine import columns
import uuid
import datetime

class Conversations(DjangoCassandraModel):
    id_conversation = columns.UUID(primary_key=True, default=uuid.uuid4)
    id_user = columns.UUID(required=True)
    message_ids = columns.List(columns.UUID)
    title = columns.Text()
    created_at = columns.DateTime(default=datetime.datetime.utcnow)

    class Meta:
        db_table = "conversations"

class Message(DjangoCassandraModel):
    id_message = columns.UUID(primary_key=True, default=uuid.uuid4)
    id_conversation = columns.UUID(required=True)
    sender = columns.Text(required=True)
    content = columns.Text(required=True)
    created_at = columns.DateTime(default=datetime.datetime.utcnow)

    class Meta:
        db_table = "messages"

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Email is required!')

        if Users.objects.filter(email=email).first():
            raise ValueError("This email is already in use!")

        if Users.objects.filter(username=username).first():
            raise ValueError("This username is already in use!")

        user = self.model(
            id_user=uuid.uuid4(),
            email=email.lower(),
            username=username
        )
        user.set_password(password)
        user.save()
        
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email, username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        
        return user

class Users(DjangoCassandraModel, AbstractBaseUser):
    id_user = columns.UUID(primary_key=True, default=uuid.uuid4)
    email = columns.Text(required=True, index=True)
    username = columns.Text(required=True, index=True)
    password = columns.Text(required=True)

    is_active = columns.Boolean(default=True)
    is_staff = columns.Boolean(default=False)
    is_superuser = columns.Boolean(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.set_password(self.password)
        
        super().save(*args, **kwargs)

    class Meta:
        db_table = "users"