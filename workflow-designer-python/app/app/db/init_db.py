from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
from app.db import base  # noqa: F401

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    #workflow = crud.workflow.get(db, id=1)
    #if not workflow:
    print('yesss')
    workflow_in = schemas.WorkflowCreate(
        id=1,
        name='test',
        fileName='test_file',
        services=['test_device_1', 'test_device_2'],
        data='A fancy script.',
        owner='Hans',
        owner_id=1,
        description='I do not care.',
    )
    print('yooo')
    # workflow = crud.workflow.create(db, obj_in=workflow_in)
    print('gasa')
    # user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    # if not user:
    #     user_in = schemas.UserCreate(
    #         email=settings.FIRST_SUPERUSER,
    #         password=settings.FIRST_SUPERUSER_PASSWORD,
    #         is_superuser=True,
    #     )
    #     user = crud.user.create(db, obj_in=user_in)  # noqa: F841
    pass
