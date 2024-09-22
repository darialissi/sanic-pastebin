from sqlalchemy.ext.asyncio import AsyncSession

from backend.storage.repository import AbstractRepository
from backend.storage.s3 import AbstractStorage
from backend.utils.uri_generator import URIGen

from .schema import PasteSchema, PasteURI


class PastesService:
    def __init__(self, pastes_repo: AbstractRepository, object_storage: AbstractStorage):
        self.pastes_repo: AbstractRepository = pastes_repo()
        self.object_storage: AbstractStorage = object_storage()

    async def add_paste(self, session: AsyncSession, paste: dict) -> PasteURI:
        paste["uri"] = URIGen.uri_gen()
        body = paste.pop("text")
        await self.object_storage.put_object(object_name=paste["uri"], body=body)
        model = await self.pastes_repo.add_one(session, paste)
        await session.commit()
        return model.uri

    async def get_paste(self, session: AsyncSession, uri: PasteURI) -> PasteSchema:
        info = await self.pastes_repo.get_one(session, uri=uri)
        i_dict = info.to_dict()
        body = await self.object_storage.get_object(object_name=uri)
        i_dict.update({"text": body})
        return i_dict

    async def get_user_pastes(self, session: AsyncSession, user_id: int) -> dict:
        result = dict()
        pastes = await self.pastes_repo.get_all(session, user_id=user_id)
        for info in pastes:
            i_dict = info.to_dict()
            uri = i_dict.pop("uri")
            body = await self.object_storage.get_object(object_name=uri)
            i_dict.update({"text": body})
            result[uri] = i_dict
        return result
