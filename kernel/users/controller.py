from http import HTTPStatus

from fastapi import APIRouter

from kernel.users.schemas import UserSchema

router = APIRouter()

databases = []


@router.get('/', status_code=HTTPStatus.OK)
def get_users(user: UserSchema): ...


@router.get('/{id}', status_code=HTTPStatus.OK)
def get_user_by_id(user: UserSchema): ...


@router.post('/', status_code=HTTPStatus.CREATED)
def create_user(user: UserSchema): ...


@router.patch('/{id}', status_code=HTTPStatus.CREATED)
def update_user(user: UserSchema): ...


@router.delete('/{id}', status_code=HTTPStatus.CREATED)
def delete_user(user: UserSchema): ...
