"""
Pydantic модели:
  - IncidentRow - одна строка очищенного датасета
  - LLMRequest - данные отправляемые в LLM
  - LLMResponse - ответ от LLM
  - BatchResult - результат обработки одного батча
"""

from __future__ import annotations

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field, field_validator, model_validator


class IncidentRow(BaseModel):
    """
    Представляет одну запись из датасета с нужными колонками. Все ненужные колонки убраны
    """

    id: int = Field(..., description="Уникальный ID обращения из исходного файла")
    date_created: datetime | None = Field(None, description="Дата создания обращения")
    topic_group: str | None = Field(None, description="Группа тем")
    topic: str | None = Field(None, description="Тема обращения")
    municipality: str | None = Field(None, description="Муниципалитет")
    locality: str | None = Field(None, description="Населённый пункт")
    incident_text: str = Field(..., description="Очищенный текст обращения")

    @field_validator("incident_text")
    @classmethod
    def text_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("incident_text не может быть пустым")
        return v.strip()


class LLMRequest(BaseModel):
    """
    Данные для анализа llm. Только id и текст инцедента
    """

    id: int
    incident_text: str = Field(..., alias="текст_инцидента")

    model_config = {"populate_by_name": True}

    @classmethod
    def from_row(cls, row: IncidentRow) -> "LLMRequest":
        return cls(id=row.id, текст_инцидента=row.incident_text)

    def to_prompt_dict(self) -> dict:
        """Сериализует в словарь, который вставляется в строку промпта"""
        return {"id": self.id, "текст_инцидента": self.incident_text}


# Оценка критичности строго от 1 до 5
CriticalityGrade = Annotated[int, Field(ge=1, le=5)]


class LLMResponse(BaseModel):
    """
    То что будет выдавть модель (id, кртичность ситуации, является ли проблемой, краткий овтет модели)
    Если is_problem=False (благодарность, вопрос, спам и т.д.) - grade_critical=None
    """

    id: int
    is_problem: bool = Field(..., description="True = обращение содержит проблему")
    grade_critical: CriticalityGrade | None = Field(
        None,
        description="Оценка критичности 1-5 (None если is_problem=False)"
    )
    reason: str | None = Field(
        None,
        description="Краткое объяснение от модели (опционально, для дебага)"
    )

    @model_validator(mode="after")
    def grade_required_when_problem(self) -> "LLMResponse":
        """
        Если is_problem=True, в таком случаен оценка критичности должна быть выставлена
        Если is_problem=False, принудительно ставим в нее None
        """
        if self.is_problem and self.grade_critical is None:
            raise ValueError("grade_critical обязателен когда is_problem=True")
        if not self.is_problem:
            self.grade_critical = None
        return self


class EnrichedIncident(BaseModel):
    """
    Модель для сохранения в БД
    складываем оригинальные метаданные + результат классификации LLM
    """

    # Столбцы из исходника
    id: int
    date_created: datetime | None
    topic_group: str | None
    topic: str | None
    municipality: str | None
    locality: str | None
    incident_text: str

    # Результат LLMки
    is_problem: bool
    grade_critical: int | None
    reason: str | None

    @classmethod
    def merge(cls, row: IncidentRow, result: LLMResponse) -> "EnrichedIncident":
        """Объединяет строку датасета и ответ LLM в одну запись"""
        assert row.id == result.id, "ID строки и ответа LLM не совпадают!"
        return cls(
            id=row.id,
            date_created=row.date_created,
            topic_group=row.topic_group,
            topic=row.topic,
            municipality=row.municipality,
            locality=row.locality,
            incident_text=row.incident_text,
            is_problem=result.is_problem,
            grade_critical=result.grade_critical,
            reason=result.reason,
        )