

from sqlalchemy.orm import Session

from src_code.ev_data.models import EVDataModel


class EVDataRepository:

    @staticmethod
    def bulk_insert(db: Session, records: list[EVDataModel]):

        db.bulk_save_objects(records)

        db.commit()