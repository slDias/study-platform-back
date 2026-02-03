from unittest.mock import AsyncMock, patch

from fastapi import FastAPI

from dependencies import lifespan


@patch("dependencies.app.database", new_callable=AsyncMock)
async def test_lifespan_sets_up_database(db_mock):
    app = FastAPI()

    async with lifespan(app):
        pass

    db_mock.set_up.assert_called_once_with(db_mock.engine)
