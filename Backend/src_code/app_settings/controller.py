from sqlalchemy.orm import Session

from src_code.users.models import UserModel

from src_code.app_settings.models import (
    AppSettingsModel
)

from src_code.app_settings.dtos import (
    UpdateAppSettingsRequest,
    AppSettingsResponse
)


def get_response(
    settings: AppSettingsModel
):

    return AppSettingsResponse(
        id=settings.id,
        user_id=settings.user_id,

        theme=settings.theme,

        distance_unit=settings.distance_unit,

        temperature_unit=settings.temperature_unit,

        default_vehicle_id=settings.default_vehicle_id
    )


def create_default_settings(
    db: Session,
    user: UserModel
):

    settings = AppSettingsModel(
        user_id=user.user_id
    )

    db.add(settings)
    db.commit()
    db.refresh(settings)

    return get_response(
        settings
    )


def get_settings(
    db: Session,
    user: UserModel
):

    settings = (
        db.query(AppSettingsModel)
        .filter(
            AppSettingsModel.user_id == user.user_id
        )
        .first()
    )

    if settings is None:

        return create_default_settings(
            db=db,
            user=user
        )

    return get_response(
        settings
    )


def update_settings(
    db: Session,
    payload: UpdateAppSettingsRequest,
    user: UserModel
):

    settings = (
        db.query(AppSettingsModel)
        .filter(
            AppSettingsModel.user_id == user.user_id
        )
        .first()
    )

    if settings is None:

        settings = AppSettingsModel(
            user_id=user.user_id
        )

        db.add(settings)
        db.commit()
        db.refresh(settings)

    update_data = payload.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():

        setattr(
            settings,
            key,
            value
        )

    db.commit()
    db.refresh(settings)

    return get_response(
        settings
    )