import os
import psycopg2
import json
import math
import pandas as pd
from datetime import datetime

def getSquare(rows):
  return (rows[0][1], rows[0][2], rows[0][3], rows[0][4])

def calculateDeforestation(rows):
  predictionPast = rows[1][5]
  predictionPresent = rows[0][5]

  primary = predictionPast.find('primary') > 0 and predictionPresent.find('primary') < 0
  cm = predictionPast.find('conventional_mine') < 0 and predictionPresent.find('conventional_mine') > 0
  am = predictionPast.find('artisinal_mine') < 0 and predictionPresent.find('artisinal_mine') > 0
  sl = False # sl = predictionPast.find('selective_logging') < 0 and predictionPresent.find('selective_logging') > 0
  a = False # a = predictionPast.find('agriculture') < 0 and predictionPresent.find('agriculture') > 0
  bd = False #bd = predictionPast.find('blow_down') < 0 and predictionPresent.find('blow_down') > 0
  sb = predictionPast.find('slash_burn') < 0 and predictionPresent.find('slash_burn') > 0
  rd = False #rd = predictionPast.find('road') < 0 and predictionPresent.find('road') > 0
  haze = predictionPast.find('haze') < 0 and predictionPresent.find('haze') < 0 
  cloudy = predictionPast.find('cloudy') < 0 and predictionPresent.find('cloudy') < 0
  partly_cloudy = predictionPast.find('partly_cloudy') < 0 and predictionPresent.find('partly_cloudy') < 0
  
  print(f'primary: {primary}')
  print(f'cm: {cm}')
  print(f'am: {am}')
  print(f'sl: {sl}')
  print(f'a: {a}')
  print(f'bd: {bd}')
  print(predictionPast.find('slash_burn') < 0)
  print(predictionPresent.find('slash_burn') > 0)
  print(predictionPast.find('slash_burn') < 0 and predictionPresent.find('slash_burn') > 0)
  print(f'sb: {sb}')
  print(f'rd: {rd}')
  print(f'haze: {haze}')
  print(f'cloudy: {cloudy}')
  print(f'partly_cloudy: {partly_cloudy}')

  result = haze and cloudy and partly_cloudy and (primary or cm or am or sl or a or bd or sb or rd)

  print(f'Result: {result}')

  return result

def getImage(row):
  # https://storage.googleapis.com/atforestry-model-tracker/planet_data/mosaics/a4917528-8540-45bc-be55-b92fb053f602/722-1001/10.png
  baseUrl = 'https://storage.googleapis.com/atforestry-model-tracker/planet_data/mosaics'
  mosaic = row[9]
  tiff = row[7]
  roster = row[8]

  return f'{baseUrl}/{mosaic}/{tiff}/{roster}.png'


def calculateChip(lng, lat, sqbl_lng, sqbl_lat):
  chipLng = 0.17578125
  chipLat = 0.17543409750702
  deltaLng = chipLng / 18.25
  deltaLat = chipLat / 18.25

  deltaLng = math.ceil((lng - sqbl_lng) / deltaLng)
  deltaLat = math.ceil((lat - sqbl_lat) / deltaLat)

  chip = deltaLat * 18 + (deltaLng - 1)

  return chip
  
def isDeforested(lat: float, lng: float):

  print("Starting deforestation calculation")
  print("connect to db")

  conn = psycopg2.connect(
      host=os.environ['DB_URL'],
      database=os.environ['POSTGRES_DB'],
      user=os.environ['POSTGRES_USER'],
      password=os.environ['POSTGRES_PASSWORD'])

  print("Create cursor + query")
  cur = conn.cursor()
  query = """SELECT * FROM prediction WHERE 
  sqbl_longitude <= %s AND sqbl_latitude <= %s AND 
  sqtr_longitude >= %s AND sqtr_latitude >= %s
  """


  print("Execute Query")
  cur.execute(query, (lng, lat, lng, lat))
  print("Fetch all")
  rows = cur.fetchall()

  
  print("getSquare")
  (sqbl_lng, sqbl_lat, sqtr_lng, sqtr_lat) = getSquare(rows)
  print("calculateChip")
  chip = calculateChip(lng, lat, sqbl_lng, sqbl_lat)

  query = """SELECT * FROM prediction WHERE 
  sqbl_longitude <= %s AND sqbl_latitude <= %s AND 
  sqtr_longitude >= %s AND sqtr_latitude >= %s AND roster = %s
  ORDER BY predictiontimestamp DESC
  """
  
  print("Query Chip to DB")
  cur.execute(query, (lng, lat, lng, lat, str(chip)))
  rows = cur.fetchall()
  
  print("close connection")
  conn.close()

  if len(rows) > 0:
    datePredictionPast = rows[1][6].strftime("%d %b, %Y")
    datePredictionPresent = rows[0][6].strftime("%d %b, %Y")
    deforestation = calculateDeforestation(rows)
    imagePast = getImage(rows[1])
    imagePresent = getImage(rows[0])

    result = {
      'deforestation': deforestation,
      'imagePast': imagePast,
      'imagePresent': imagePresent,
      'past': str(rows[1]),
      'present': str(rows[0]),
      'datePredictionPast': str(datePredictionPast),
      'datePredictionPresent': str(datePredictionPresent)
    }

    print(result)

    return(result)
  else:
    return json.encoder('{}')


