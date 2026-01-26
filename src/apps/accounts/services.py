from django.db import transaction
from companies.models import EmployerProfile
from candidates.models import CandidateProfile


def register_user(email, password, role, username=None, **extra_fields):

    from django.contrib.auth import get_user_model
    User = get_user_model()

    with transaction.atomic():
        user = User.objects.create_user(
            email = email,
            password = password,
            role = role,
            username = username or email,
            **extra_fields
        )

        if role == User.Role.EMPLOYER:
            EmployerProfile.objects.create(user=user)
        elif role == User.Role.CANDIDATE:
            CandidateProfile.objects.create(user=user)
            
        return user
