from fastapi import APIRouter
from src.application.model.output import LanguageResponse
from src.application.queries import GetAllLanguagesQuery
from src.web_api.dependencies import LanguageRepositoryDependency

router = APIRouter(prefix="/languages", tags=['Languages'])

@router.get("")
async def get_languages(language_repository: LanguageRepositoryDependency) -> list[LanguageResponse]:
    query = GetAllLanguagesQuery(language_repository)
    languages = query.handle()
    return languages