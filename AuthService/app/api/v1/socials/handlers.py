
from fastapi import APIRouter, Depends, HTTPException, Query, Request, requests, status

import httpx

from schemas.token import Token


from settings.config import settings


router = APIRouter(
    tags=['Socials'],    
)

YANDEX_AUTH_URL = "https://oauth.yandex.ru/authorize"
YANDEX_TOKEN_URL = "https://oauth.yandex.ru/token"
YANDEX_USERINFO_URL = "https://login.yandex.ru/info"

@router.get("/yandex")
async def auth_yandex():
    yandex_oauth_url = (
        "https://oauth.yandex.ru/authorize?"
        "response_type=code"
        f"&client_id={settings.yandex_client_id}"
        f"&redirect_uri={settings.social_auth_redirect_url}"
        "&scope=login:email"
    )
    return {
        "yandex_url": yandex_oauth_url
    }
    
    
@router.post(
    "/yandex/callback",
    response_model=Token,
)
async def login_by_social_network(
    code: str
):
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            YANDEX_TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": settings.yandex_client_id,
                "client_secret": settings.yandex_client_secret,
                "redirect_uri": settings.social_auth_redirect_url
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        if token_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Ошибка получения токена")

        token_data = token_response.json()
        access_token = token_data["access_token"]

    return {"access_token": access_token}
    
    # token_url = "https://oauth.yandex.ru/token"
    # data = {
    #     "grant_type": "authorization_code",
    #     "code": code,
    #     "client_id": settings.yandex_client_id,
    #     "client_secret": settings.yandex_client_secret,
    #     "redirect_uri": settings.social_auth_redirect_url
    # }
    
    # response = httpx.post(token_url, data=data)
    # if response.status_code != 200:
    #     raise HTTPException(status_code=400, detail="Could not get token from Yandex")
    
    # provider: SocialNetworkProvider = await get_provider(SocialNetworks.YANDEX)
    
    # user = await provider.process_user(code, user_service)
    # print(provider.social_name, "\n\n\n\n\n\n")

    # token: GenericResult[Token] = await auth.login_by_oauth(
    #     login=user.response.login,
    # )
    # if not token.is_success:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST, detail="login or/and password incorrect"
    #     )

    # return token.response    