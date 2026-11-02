from sqlalchemy import select
from app.database import SessionLocal
from app.models import RecordType

DEFAULT_RECORD_TYPES = [
    "Вакцинация",
    "Осмотр",
    "Лечение",
    "Анализ",
    "Профилактика",
]


def seed_record_types():
    """Добавляет стандартные типы, если их ещё нет."""

    with SessionLocal() as session:
        for type_name in DEFAULT_RECORD_TYPES:
            existing_type = session.scalar(
                select(RecordType).where(
                    RecordType.name == type_name
                )
            )

            if existing_type is None:
                session.add(RecordType(name=type_name))

        session.commit()

if __name__ == "__main__":
    seed_record_types()
    print("Справочник типов успешно заполнен!")
