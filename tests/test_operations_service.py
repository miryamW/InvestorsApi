import pytest

from app.services import operations_service


def test_get_all_operations():
    assert operations_service.get_all_operations() == []
