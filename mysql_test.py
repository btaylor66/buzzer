#!c:\python27\python.exe -u
import MySQLdb
from subprocess import call
import time

# Use all the SQL you like
print "Querying Monolith Prod"

def alarmCritical():
  call("USBCMDAP 0 0 101 22 50 50", shell=True)
  call("USBCMDAP 0 0 101 20 0 2", shell=True)
  call("USBCMDAP 0 0 102 70 1 16 255 20 20", shell=True)

def alarmMajor():
  call("USBCMDAP 0 0 101 22 50 50", shell=True)
  call("USBCMDAP 0 0 101 20 0 2", shell=True)
  call("USBCMDAP 0 0 102 70 1 16 255 20 20", shell=True)

def alarmClear():
  # turn off the buzzer
  call("usbcmdap 0 0 102 70 0 16 255 100 100", shell=True)
  # turn off the flashing function
  call("usbcmdap 0 0 101 20 7 0", shell=True)
  # turn off the light
  call("usbcmdap 0 0 101 12 0 7", shell=True)

db = MySQLdb.connect(host="monolith-prod", # your host, usually localhost
                     user="monolith", # your username
                      passwd="monolith", # your password
                      db="Events") # name of the data base
db.autocommit(True)
# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor() 

inAlarm=False
# Turning Alarm off if on
alarmClear()

while True:
  #print "Querying Monolith"
  #hour=time.localtime(time.time())
  hour=int(time.strftime("%H"))-6
  #print hour
  if (hour >= 7 and hour < 16):
    #print "During Trading Day"
    cur.execute("select AlarmID, Node, AlarmGroup, SubAlarmGroup, Severity, Summary from Alarm where severity >= 5 and ack =0 and Score >= 50 and (Custom3 != 'QA' and Custom3 != 'DEV') and Department != 'Desktop' and SubAlarmGroup not like '%beta%'")

    # print all the first cell of all the rows
    maxSeverity=0
    #print dir(cur)
    for row in cur.fetchall() :
      inAlarm=True
      print "%s\t%s\t%s\t%s\t%s" % (row[0],row[1],row[2],row[3],row[4])
      if row[4] > maxSeverity:
          maxSeverity=row[4]
      alarmCritical()

    #print cur.rowcount
    #print maxSeverity
    if cur.rowcount == 0 and inAlarm==True:
      inAlarm=False
      print "No Critical Alerts found"
      alarmClear()

    #db.commit()

  time.sleep(10)
