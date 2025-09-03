from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://neondb_owner:npg_qdvMWCcBNY10@ep-aged-unit-a1xgv1rd-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

engine = create_engine( SQLALCHEMY_DATABASE_URL )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()





# SQLALCHEMY_DATABASE_URL = "sqlite:///bookstore.db"

# engine = create_engine(  f"sqlite:///file:bookstore.db?mode=ro&uri=true", connect_args={"check_same_thread": False} )

