from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

engine_WorkflowDesigner_Node_Red = create_engine(settings.SQLALCHEMY_DESIGNER_NODE_RED_DATABASE_URI, pool_pre_ping=True)
SessionLocal_WorkflowDesigner_Node_Red = sessionmaker(autocommit=False,
                                                      autoflush=False,
                                                      bind=engine_WorkflowDesigner_Node_Red)

engine_WorkflowDesigner_Python = create_engine(settings.SQLALCHEMY_DESIGNER_PYTHON_DATABASE_URI, pool_pre_ping=True)
SessionLocal_WorkflowDesigner_Python = sessionmaker(autocommit=False,
                                                    autoflush=False,
                                                    bind=engine_WorkflowDesigner_Python)
