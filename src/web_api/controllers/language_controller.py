from fastapi import APIRouter
from src.application.model.output.language_response import LanguageResponse
from src.application.queries.get_all_languages_query import GetAllLanguagesQuery
from src.web_api.dependencies import LanguageRepositoryDependency

router = APIRouter()

@router.get("/languages")
def get_languages(language_repository: LanguageRepositoryDependency) -> list[LanguageResponse]:
    query = GetAllLanguagesQuery(language_repository)
    languages = query.handle()
    return languages