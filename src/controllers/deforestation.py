import os
import psycopg2

print(str(os.environ.keys()))

conn = psycopg2.connect(
    host=os.environ['DB_URL'],
    database=os.environ['POSTGRES_DB'],
    user=os.environ['POSTGRES_USER'],
    password=os.environ['POSTGRES_PASSWORD'])

def isDeforested(lat: float, lng: float):
  cur = conn.cursor()
  query = """SELECT * FROM Prediction WHERE 
  sqbl_longitude >= %s AND sqbl_latitude >= %s 
  AND sqtr_longitude <= %s AND sqtr_latitude <= %s"""
  
  cur.execute(query, (lng, lat, lng, lat))
  rows = cur.fetchall()

  if len(rows) == 0:
    return None 
  else:
    return rows

