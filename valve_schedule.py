'''
David Rodriguez

Goal: Continuously looping while to perform valve actions at specified times, 
introduce substance at a specific ratio based on flow data, recording 
and saving flow data, and actuating a flush at a specified time.

Inputs: A schedule of events based on entered times.

Outputs: Sequence of events to a screen as they happen. 
daily flow rate data
'''
#Handles all scheduling related tasks
from valve_event import Event
import datetime

class Schedule:
    
    def __init__(self):
        self.eventList = []
        self.eventCount = 0
        
    def displayMenu(self):
        print "\n1: Import Existing Schedule"
        print "2: Add Event"
        print "3: Remove Event"
        print "4: Display Events"
        print "5: Save Schedule"
        print "6: Return to main menu"
        
    def addEvent(self):
        start = datetime.time()
        enteredTime = raw_input("Please enter the time you want the event to "
                                  "occur. Format as HH:MM:SS (eg 15:30:12) ")
        start = datetime.datetime.strptime(enteredTime, "%H:%M:%S").time()
        datetime.time(3, 55, 55)
        
        end = datetime.time()
        enteredTime = raw_input("Please enter the time you want to stop "
                                  "the event. Format as HH:MM:SS (eg 15:31:06) ")
        end = datetime.datetime.strptime(enteredTime, "%H:%M:%S").time()
        datetime.time(3, 55, 55)

        tag = raw_input("Please enter which valve this event is for. Your options are kitchen_sink, bathroom_sink, and shower.\n")

        new = Event(start, end, tag)
        
        self.eventList.append(new)
        self.eventCount += 1
        print "\nEvent added."
        new.displayEvent()
    
    def displaySchedule(self):
        self.eventList.sort(key = lambda event: event.startTime)
        counter = 1
        for event in self.eventList:
            print str(counter) + ": " + event.displayEvent()
            counter += 1
            
    def saveSchedule(self):
        self.eventList.sort(key = lambda event: event.startTime)
        filename = raw_input("Please enter a name for the Schedule.\n")
        target = open(filename, 'w')
        for e in self.eventList:
            target.write(e.storeEvent())
            target.write("\n")
        target.close()
        print "Schedule saved as %s" % filename
        
    def importSchedule(self):
        filename = raw_input("\nType the name of the schedule you want to import.\n")
        with open(filename, 'r') as target:
            for line in target:
                start = line.split(" ")[0]
                hour = int(start.split(":")[0])
                minute = int(start.split(":")[1])
                second = int(start.split(":")[2])
                start = datetime.time(hour, minute, second)
                
                end = line.split(" ")[1]
                hour = int(end.split(":")[0])
                minute = int(end.split(":")[1])
                second = int(end.split(":")[2])
                end = datetime.time(hour, minute, second)
                
                tag = line.split(" ")[2]
                
                new = Event(start, end, tag)
                
                self.eventList.append(new)
                self.eventCount += 1
        target.close()
        print "\nSchedule imported:\n"
