import pytest
from pytest_factoryboy import register
from django.contrib.auth import get_user_model

from apps.main.tests.factories import SolicitacaoFactory, TotalEmpresaFactory
from apps.sebrae.tests.factories import EmpresaSebraeFactory

# Modulo Sebrae
register(EmpresaSebraeFactory)

# Modulo Main
register(SolicitacaoFactory)
register(TotalEmpresaFactory)


@pytest.fixture
def headers():
    """default headers on make request"""
    return {'content_type': "application/json"}


@pytest.fixture
def user():
    '''
    Create a user with add_event and view_series permissions
    '''
    klass = get_user_model()
    user = klass.objects.create(email='root_tester@root.com.br')
    return user


@pytest.fixture
def client_permission(user, client):
    client.force_login(user)
    return client


@pytest.fixture
def authenticated_client(client, user):
    client.force_login(user)
    return client
