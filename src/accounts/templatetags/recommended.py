# from django import template
# from django.contrib.auth import get_user_model
# from ..models import Userprofile
#
#
# register = template.library()
#
#
# User = get_user_model()
#
#
# @register.inclusion_tag("accounts/snippets/recommended.html")
# def recommended(user):
#     if inistance(user, User):
#         qs = UserProfile.objects.recommended(user)
#         return {"recommended", qs}