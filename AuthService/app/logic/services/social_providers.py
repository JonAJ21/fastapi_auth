from dataclasses import dataclass

from async_oauthlib import OAuth2Session
from httpx import AsyncClient, HTTPStatusError
from fastapi import HTTPException, status

from infrastructure.models.user import User
from schemas.result import GenericResult
from logic.services.user import BaseUserService
from schemas.social import SocialNetworks, SocialUser
from settings.config import settings


@dataclass
class SocialNetworkProvider:
    social_name: SocialNetworks | None = SocialNetworks
    session: OAuth2Session | None = None
    auth_token_url: str | None = None
    user_info_url: str | None = None
    client_secret: str | None = None
    client_id: str | None = None
    
    async def init_session(self):
        self.session = OAuth2Session(
            client_id=self.client_id, redirect_uri=settings.social_auth_redirect_url
        )
        
    @classmethod
    async def create(cls):
        intance = cls()
        await intance.init_session()
        return intance
    
    async def fetch_data(self, code: str):
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": settings.social_auth_redirect_url,
        }
        try:
            async with AsyncClient() as client:
                token_response = await client.post(self.auth_token_url, data=data)
                token_response.raise_for_status()
                token =  token_response.json()["access_token"]
                
                headers = {"Authorization": f"Bearer {token}"}
                user_info_response = await client.get(self.user_info_url, headers=headers)
                user_info_response.raise_for_status()
                return user_info_response.json()
        except HTTPStatusError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Code is expired"
            )
    
    async def process_user(
        self, code: str, user_service: BaseUserService
    ) -> GenericResult[User]:
        data = await self.fetch_data(code)
        return await user_service.get_or_create_user(
            social=SocialUser(
                social_name=self.social_name,
                email=data["default_email"],
                **data
            )
        )
        
class Yandex(SocialNetworkProvider):
    social_name = SocialNetworks.YANDEX
    auth_token_url = settings.yandex_auth_token_url
    userinfo_url = settings.yandex_userinfo_url
    client_secret = settings.yandex_client_secret
    client_id = settings.yandex_client_id
    
class VK(SocialNetworkProvider):
    social_name = SocialNetworks.VK
    auth_token_url = settings.yandex_auth_token_url
    userinfo_url = settings.yandex_userinfo_url
    client_secret = settings.yandex_client_secret
    client_id = settings.yandex_client_id
    
async def get_provider(provider_name: SocialNetworks) -> SocialNetworkProvider:
    providers = {
        SocialNetworks.YANDEX: Yandex,
        SocialNetworks.VK: VK
    }
    provider_class = providers.get(provider_name)
    if not provider_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unsupported social network"
        )
    return await provider_class.create()