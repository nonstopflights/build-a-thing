import requests
import arrow

def getJSONObject():
  # Grab the Status page, page 1. Here you could introduce logic to page through all incidents (page after page) and add them to one large object
  request = requests.get("https://status.replit.com/api/v1/notices")
  return (request.json())

def convertToReadableTime(time):
  # Who wants to read that ISO standard time. Let's convert to readable
  prettyTime = arrow.get(time)
  return(prettyTime.format('MM-DD HH:mm:ss'))

def createNewFile():
  # For this exercise we are pulling data a single time to create the file. 
  # Let's make a fresh header
  with open("build-a-thing.md", "w") as file:
    file.write("# |STATUS UPDATES|\n\n")

def writeIncidentsTofile(entry):
  # Let's write each entry to the file
  if entry['state'] not in ["future", "present"]: # Let's not list future or planned down time
    with open("build-a-thing.md", "a") as file:
      output = f"**{entry['started']}** - #{entry['id']} - \
      **{entry['state']}** - {entry['subject']} | Incident Resolved : {entry['ended']}\n\n"
      file.write(output)
  elif entry['state'] == 'present': # Here you could make it <blink> to bring it to someones attention
    with open("build-a-thing.md", "a") as file:
      output = f"**{entry['started']}** - #{entry['id']} - \
      **{entry['state']}** - {entry['subject']} - Active incident\n\n"
      file.write(output)
  file.close()
  
status = getJSONObject() # assign JSON to object

createNewFile() # make a fresh file with header

for item in status["notices"]:
  # Iterate through each incident. 
  statusDict = { # let's pull only the info we want from each line
    "id": item['id'],
    "subject": item['subject'], 
    "state": item['state'],
    "started": convertToReadableTime(item['began_at']),
    "ended": convertToReadableTime(item['ended_at']), 
    "planned": item['type'], 
    "state": item['state']
  }
  writeIncidentsTofile(statusDict)

  
  
