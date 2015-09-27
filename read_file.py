from lxml import objectify
from pandas import DataFrame, Series
import pandas as pd

def read_file(filepath):
  parse_file = objectify.parse(open(filepath))
  root = parse_file.getroot()

  elt = root.Document

  flightname = elt.name.text
  print flightname

  #get the three placemarks
  placemarks = []
  for plc in elt.Placemark:
    placemarks.append(plc)

  #get origin airport's name and coordinates
  begin_name = placemarks[0].name.text.split()[0]
  begin_coordinates = placemarks[0].Point.coordinates

  #get destination airport's name and coordinates
  end_name = placemarks[1].name.text.split()[0]
  end_coordinates = placemarks[1].Point.coordinates

  print begin_name, end_name

  gx = placemarks[2].getchildren()[2]

  #lists to hold flight path information, to be put into dataframe
  when_date = []
  when_time = []
  coord_longitude = []
  coord_latitude = []
  coord_altitude = []

  #read in flightpath by time and coordinate
  for child in gx.getchildren():
    tagname = child.tag.rpartition('}')[2]
    if tagname in ("extrude","tessellate","altitudeMode"):
      continue
    if tagname == "when":
      when_date.append(child.text.rpartition('T')[0])
      when_time.append(child.text.rpartition('T')[2])
    elif tagname == "coord":
      data = child.text.split()
      coord_longitude.append(data[0])
      coord_latitude.append(data[1])
      coord_altitude.append(data[2])

  #put data into dataframe
  data = {'date': when_date, 'time': when_time, 'longitude': coord_longitude, 'latitude': coord_latitude, 'altitude': coord_altitude}
  frame = DataFrame(data, columns=['date', 'time', 'longitude', 'latitude', 'altitude'])
  
  ###print frame
  return frame

def read_all():
  frames = []

  import os
  for file in os.listdir("./KML"):
    if file.endswith(".kml"):
      frame = read_file("./KML/" + file)
      frames.append(frame)
  print len(frames)
  print frames[0]

if __name__ == '__main__':
  read_all()