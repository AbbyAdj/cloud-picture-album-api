from unittest.mock import Mock
from fastapi.exceptions import HTTPException
from fastapi.testclient import TestClient
import pytest
from src.utils.db_operations import util_funcs
from src.models.models import PostPictureModel, AddNewUserModel
