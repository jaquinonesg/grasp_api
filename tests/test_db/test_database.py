# from unittest.mock import AsyncMock, MagicMock, patch

# import pytest
# from de.core.conf import settings
# from pkgsettings import PrefixedSettings
# from sqlalchemy.pool import NullPool

# from de_hapib_ng.db.database import configure_db_session, get_read_only_session, get_session
# from de_hapib_ng.db.models import (
#     EquipmentService,
#     GenericService,
#     InternetService,
#     ITVService,
#     Keyring,
#     TelephonyService,
# )


# class TestDatabase:
#     @pytest.mark.parametrize("db_prefix", ["DATABASE_", "DATABASE_RO_"])
#     @pytest.mark.parametrize("db_pool_class", ["NullPool", None])
#     async def test_configure_db(self, db_prefix, db_pool_class):
#         db_config = {
#             "DATABASE_USER": "username",
#             "DATABASE_PASSWORD": "password",
#             "DATABASE_HOST": "db-host",
#             "DATABASE_PORT": 5452,
#             "DATABASE_NAME": "db_hapib_name",
#             "DATABASE_POOL_SIZE": 33,
#             "DATABASE_POOL_CLASS": "NullPool",
#             "DATABASE_SSLMODE": "allow",
#             "DATABASE_RO_USER": "username_ro",
#             "DATABASE_RO_PASSWORD": "password_ro",
#             "DATABASE_RO_HOST": "db-host-ro",
#             "DATABASE_RO_PORT": 5453,
#             "DATABASE_RO_NAME": "db_hapib_name_ro",
#             "DATABASE_RO_POOL_SIZE": 10,
#             "DATABASE_RO_SSLMODE": None,
#         }

#         with patch("de_hapib_ng.db.database.create_async_engine", return_value="engine1") as engine_mock, settings(
#             DEBUG=True, **db_config
#         ):
#             # Main db
#             configure_mock = MagicMock(return_value="")
#             configure_db_session(MagicMock(configure=configure_mock), PrefixedSettings(settings, "DATABASE_"))

#             db_config_expected = dict(
#                 url=f"postgresql+asyncpg://{db_config['DATABASE_USER']}:{db_config['DATABASE_PASSWORD']}@{db_config['DATABASE_HOST']}:{db_config['DATABASE_PORT']}/{db_config['DATABASE_NAME']}",
#                 pool_size=db_config["DATABASE_POOL_SIZE"],
#                 connect_args={"ssl": "allow"},
#                 poolclass=NullPool,
#             )
#             assert engine_mock.call_args[1] == db_config_expected
#             assert configure_mock.call_args[1]["bind"] == "engine1"

#             # Read only db
#             configure_mock = MagicMock(return_value="")
#             configure_db_session(MagicMock(configure=configure_mock), PrefixedSettings(settings, "DATABASE_RO_"))

#             db_config_expected = dict(
#                 url=f"postgresql+asyncpg://{db_config['DATABASE_RO_USER']}:{db_config['DATABASE_RO_PASSWORD']}@{db_config['DATABASE_RO_HOST']}:{db_config['DATABASE_RO_PORT']}/{db_config['DATABASE_RO_NAME']}",
#                 pool_size=db_config["DATABASE_RO_POOL_SIZE"],
#                 connect_args={"ssl": "require"},
#             )
#             assert engine_mock.call_args[1] == db_config_expected
#             assert configure_mock.call_args[1]["bind"] == "engine1"

#     async def test_get_session(self):
#         with patch("de_hapib_ng.db.database.Session", return_value=AsyncMock()):
#             async for _ in get_session():
#                 pass

#     async def test_get_ro_session(self):
#         with patch("de_hapib_ng.db.database.ReadOnlySession", return_value=AsyncMock()):
#             async for _ in get_read_only_session():
#                 pass

#     async def test_create_model_instance(self):
#         Keyring(bss_id="SDF")
#         GenericService(service_id="45345")
#         InternetService(service_id="45345")
#         ITVService(service_id="45345")
#         TelephonyService(service_id="45345")
#         TelephonyService(service_id="45345")
#         EquipmentService(service_id="45345")
