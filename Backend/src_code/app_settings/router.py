from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src_code.utils.db import get_db

from src_code.app_settings.dtos import (
    UpdateAppSettingsRequest,
    AppSettingsResponse
)

from src_code.app_settings.controller import (
    get_settings,
    update_settings
)

from src_code.users.controller import (
    is_authenticated
)

from src_code.users.models import UserModel


settings_routes = APIRouter(
    prefix="/app-settings"
)


@settings_routes.get(
    "/get",
    response_model=AppSettingsResponse
)
def get_user_settings(
    db: Session = Depends(get_db),
    user: UserModel = Depends(is_authenticated)
):

    return get_settings(
        db=db,
        user=user
    )


@settings_routes.put(
    "/update",
    response_model=AppSettingsResponse
)
def update_user_settings(
    payload: UpdateAppSettingsRequest,
    db: Session = Depends(get_db),
    user: UserModel = Depends(is_authenticated)
):

    return update_settings(
        db=db,
        payload=payload,
        user=user
    )