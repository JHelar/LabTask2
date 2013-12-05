class Person:
    name = ""
    status = ""
    smoker = ""
    manyVisitors = ""

class Rooms:
    amount = 0
    currentAmount = 0
    contains = []

    def __init__(self,amount):
        self.contains = []
        self.amount = amount

class Office:
    persons = list()
    officeRooms = dict()
    
    def __init__(self):
        self.officeRooms['T13'] = Rooms(1)
        self.officeRooms['T14'] = Rooms(1)
        self.officeRooms['T15'] = Rooms(1)
        self.officeRooms['T16'] = Rooms(1)
        self.officeRooms['T11'] = Rooms(2)
        self.officeRooms['T12'] = Rooms(2)
        self.officeRooms['T10'] = Rooms(3)
        self.setPeople()

    def setPeople(self):
        dataFile = open("People.txt")
        for dataLine in dataFile.readlines():
            dataLine = dataLine[:len(dataLine) - 1]
            dummyPerson = Person()
            dummyPerson.name,dummyPerson.smoker,dummyPerson.manyVisitors,dummyPerson.status = dataLine.split(';')
            self.persons.append(dummyPerson)
        dataFile.close()
        self.persons.reverse()
        del dataFile
        del dataLine
    
class Constraints:

    office = Office()

    def checkConstraints(self,one,room):
        if not self.FullRoom(room):
            return False
        if not self.Smoker(one,room):
            return False
        if not self.Visitors(one,room):
            return False
        if not self.CheckStatus(one,room):
           return False
        return True

    def Smoker(self,one,room):
        for another in room.contains:
            if one.smoker != another.smoker:
                return False
        return True
         
    def Visitors(self,one,room):
        for another in room.contains:
            if one.manyVisitors == "many visitors" and another.manyVisitors == "many visitors":
                return False
        return True

    def FullRoom(self,room):
        if room.currentAmount == room.amount:
            return False
        for another in room.contains:
            if another.status == "head" or another.status == "professor":
                return False
        else:
            return True

    def CheckStatus(self,one,room):
        if one.status == "head" or one.status == "professor":
            if room.contains == []:
                if room.amount == 2 or room.amount == 3:
                    return True
                else:
                    return False
        else:
            return True

    
def BackTrackingSearch(csp):
    assignment = dict()
    return ReckursiveBacktracking(assignment,csp)

def ReckursiveBacktracking(assignment,csp):
    if csp.office.persons == []:
        return assignment
    person = csp.office.persons.pop()
    for room in roomList(person,assignment,csp):
        assign(person,room,assignment,csp)
        result = ReckursiveBacktracking(assignment,csp)
        if result != None:
            return result
        personToDelete = assignment[person]
        csp.office.officeRooms[personToDelete].contains.remove(person)
        csp.office.officeRooms[personToDelete].currentAmount -= 1
        del assignment[person]
    csp.office.persons.append(person)
    return None

def roomList(person,assignment,csp):
    roomsToReturn = list()
    for room in csp.office.officeRooms.keys():
        if csp.checkConstraints(person,csp.office.officeRooms[room]):
            roomsToReturn.append(room)
    return roomsToReturn

def assign(person,room,assignment,csp):
    personToAppend = csp.office.officeRooms[room]
    personToAppend.contains.append(person)
    personToAppend.currentAmount += 1
    assignment[person] = room

csp = Constraints()
assignments = BackTrackingSearch(csp)
if assignments != None:
    for a in assignments.keys():
        print("Person:",a.name,"with status:",a.status,a.smoker,a.manyVisitors,"assigned to room:",assignments[a])
else:
    print("Couldn't assign everybody")
  
