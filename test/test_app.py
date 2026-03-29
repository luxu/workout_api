import sqlite3
from http import HTTPStatus
from pathlib import Path
from uuid import uuid4

from fastapi.testclient import TestClient

from kernel.main import app
from kernel.users.controller import (
    create_user,
    delete_user,
    get_user_by_id,
    get_users,
    update_user,
)
from kernel.users.schemas import UserSchema


def _client() -> TestClient:
    return TestClient(app)


def _unique_name(prefix: str) -> str:
    return f'{prefix}-{uuid4().hex[:8]}'


def _unique_categoria_name() -> str:
    return f'c{uuid4().hex[:8]}'


DB_PATH = Path(__file__).resolve().parents[1] / 'workout.db'


def _insert_categoria_raw(nome: str) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO categorias (nome) VALUES (?)',
            (nome,),
        )
        conn.commit()


def _create_centro(client: TestClient, nome: str) -> dict:
    response = client.post(
        '/centros_treinamento',
        json={
            'nome': nome,
            'endereco': 'Rua X, Q02',
            'proprietario': 'Marcos',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    return response.json()


def _assert_pagination(payload: dict, limit: int, offset: int) -> None:
    assert payload['limit'] == limit
    assert payload['offset'] == offset
    assert isinstance(payload['items'], list)


def test_get_centro_treinamentos():
    client = _client()
    response = client.get('/centros_treinamento?limit=10&offset=0')
    assert response.status_code == HTTPStatus.OK


def test_list_categorias_empty_page():
    client = _client()
    response = client.get('/categorias?limit=10&offset=0')
    assert response.status_code == HTTPStatus.OK
    payload = response.json()
    _assert_pagination(payload, limit=10, offset=0)


def test_get_categoria_not_found():
    client = _client()
    response = client.get(f'/categorias/{uuid4()}')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_create_and_list_centros():
    client = _client()
    nome = _unique_name('ct')
    centro = _create_centro(client, nome)

    response = client.get('/centros_treinamento?limit=5&offset=0')
    assert response.status_code == HTTPStatus.OK
    payload = response.json()
    _assert_pagination(payload, limit=5, offset=0)
    response = client.get(f"/centros_treinamento/{centro['id']}")
    assert response.status_code == HTTPStatus.OK


def test_centro_duplicate_returns_303():
    client = _client()
    nome = _unique_name('ct-dup')
    _create_centro(client, nome)

    response = client.post(
        '/centros_treinamento',
        json={
            'nome': nome,
            'endereco': 'Rua Y, Q03',
            'proprietario': 'Carlos',
        },
    )
    assert response.status_code == HTTPStatus.SEE_OTHER


def test_get_centro_not_found():
    client = _client()
    response = client.get(f'/centros_treinamento/{uuid4()}')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_get_atletas_empty_page():
    client = _client()
    response = client.get('/atletas?limit=10&offset=0')
    assert response.status_code == HTTPStatus.OK
    payload = response.json()
    _assert_pagination(payload, limit=10, offset=0)


def test_post_atleta_categoria_missing():
    client = _client()
    response = client.post(
        '/atletas',
        json={
            'nome': 'Joao',
            'cpf': '12345678900',
            'idade': 25,
            'peso': 75.5,
            'altura': 1.7,
            'sexo': 'M',
            'categoria': {'nome': _unique_categoria_name()},
            'centro_treinamento': {'nome': _unique_name('ct-any')},
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_post_atleta_centro_missing():
    client = _client()
    categoria_nome = _unique_categoria_name()
    _insert_categoria_raw(categoria_nome)
    response = client.post(
        '/atletas',
        json={
            'nome': 'Maria',
            'cpf': '12345678901',
            'idade': 28,
            'peso': 63.2,
            'altura': 1.65,
            'sexo': 'F',
            'categoria': {'nome': categoria_nome},
            'centro_treinamento': {'nome': _unique_name('ct-miss')},
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_get_atleta_not_found():
    client = _client()
    response = client.get(f'/atletas/{uuid4()}')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_patch_atleta_not_found():
    client = _client()
    response = client.patch(
        f'/atletas/{uuid4()}',
        json={'nome': 'Novo Nome'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_atleta_not_found():
    client = _client()
    response = client.delete(f'/atletas/{uuid4()}')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_users_controller_functions():
    user = UserSchema(
        username='user',
        email='user@example.com',
        password='secret',
    )
    assert get_users(user) is None
    assert get_user_by_id(user) is None
    assert create_user(user) is None
    assert update_user(user) is None
    assert delete_user(user) is None
