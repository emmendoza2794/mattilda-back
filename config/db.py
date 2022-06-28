from importlib_metadata import metadata
from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymysql://mattilda:dO34tApo2inOfI8O1e24CeQaqoB1su@ls-99b3891e52594fb2bf262e57699f48215e7142b7.clahm0ludhas.us-west-2.rds.amazonaws.com:3306/mattilda")

meta = MetaData()

conn = engine.connect()

