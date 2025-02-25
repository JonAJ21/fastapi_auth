
from fastapi import APIRouter, Depends, HTTPException, Query, status



from schemas.social import SocialNetworks
from logic.services.social_providers import SocialNetworkProvider, get_provider
from logic.services.user import BaseUserService
from logic.services.auth import BaseAuthService
from schemas.result import GenericResult
from schemas.token import Token


from settings.config import settings


router = APIRouter(
    tags=['Socials'],   
)


@router.get("/login/yandex")
async def login_yandex():
    auth_url = f"https://oauth.yandex.ru/authorize?response_type=code&client_id={settings.yandex_client_id}&redirect_uri={settings.social_auth_redirect_url}"
    return {"url":auth_url}

@router.get("/yandex/callback")
async def auth_yandex_callback(
    code: str = Query(None, description="Code from auth provider"),
    user_service: BaseUserService = Depends(),
    auth: BaseAuthService = Depends()
):
    provider = await get_provider(SocialNetworks.YANDEX)
    user = await provider.process_user(code, user_service)
        
    token: GenericResult[Token] = await auth.login_by_oauth(
        login=user.response.login,
    )
    
    if not token.is_success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="login or/and password incorrect"
        )

    return token.response


     