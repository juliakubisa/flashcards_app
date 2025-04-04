from src.domain.entities.model_base import ModelBase
from dataclasses import dataclass
from sqlalchemy.orm import Mapped, mapped_column

class Language(ModelBase):
    __tablename__ = "language"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()

    def __init__(self, lang_name, lang_code):
        self.id = lang_code
        self.name = lang_name
