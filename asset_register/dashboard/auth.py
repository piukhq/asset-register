from mozilla_django_oidc.auth import OIDCAuthenticationBackend


class MyOIDCAuthBackend(OIDCAuthenticationBackend):
    def create_user(self, claims):
        user = super(MyOIDCAuthBackend, self).create_user(claims)

        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user

    def update_user(self, user, claims):
        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user