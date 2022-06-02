import os
import psycopg2

print(str(os.environ.keys()))

conn = psycopg2.connect(
    host=os.environ['DB_URL'],
    database=os.environ['POSTGRES_DB'],
    user=os.environ['POSTGRES_USER'],
    password=os.environ['POSTGRES_PASSWORD'])

def isDeforested(lat: float, lng: float):
  return str(os.environ.keys())