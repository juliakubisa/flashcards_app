from src.domain.entities.entity_base import EntityBase
from sqlalchemy.orm import Mapped, mapped_column

class Language(EntityBase):
    __tablename__ = "language"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()

    def __init__(self, lang_name, lang_code):
        self.id = lang_code
        self.name = lang_name
