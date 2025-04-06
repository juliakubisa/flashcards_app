from src.application.model.output.language_response import LanguageResponse
from src.infrastructure.database.repositories.language_repository import LanguageRepository

class GetAllLanguagesQuery:
    def __init__(self, repository: LanguageRepository):
        self.repository = repository

    def handle(self) -> list[LanguageResponse]:
        languages = self.repository.get_all()
        languages_response = [LanguageResponse(id=lang.id, name=lang.name) for lang in languages]
        return languages_response