from .object_storage import PastesStorage
from .repository import PastesRepository
from .service import PastesService

paste_service: PastesService = PastesService(
    pastes_repo=PastesRepository,
    object_storage=PastesStorage,
)
