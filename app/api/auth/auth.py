from fastapi_users.authentication import CookieTransport, AuthenticationBackend, JWTStrategy
from fastapi_users import FastAPIUsers
from app.api.auth.manager import get_user_manager
from app.models.models import User

from app.config import SECRET

cookie_transport = CookieTransport(cookie_name="access_token", cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
