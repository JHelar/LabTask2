class Person:
    name = ""
    status = ""
    smoker = ""
    manyVisitors = ""
    constraintsVal = 0

class Rooms:
    amount = 0
    currentAmount = 0
    contains = []
    constraintsVal = 0

    def __init__(self,amount,constraintsVal):
        self.contains = []
        self.amount = amount
        self.constraintsVal = constraintsVal

class Office:
    persons = list()
    unAssignedPeople = list()
    originalPeopleList = list()
    officeRooms = dict()
    MCV = False
    
    def __init__(self):
        self.officeRooms['T13'] = Rooms(1,2)
        self.officeRooms['T14'] = Rooms(1,2)
        self.officeRooms['T15'] = Rooms(1,2)
        self.officeRooms['T16'] = Rooms(1,2)
        self.officeRooms['T11'] = Rooms(2,4)
        self.officeRooms['T12'] = Rooms(2,4)
        self.officeRooms['T10'] = Rooms(3,4)
        self.setPeople()

    def setPeople(self):
        dataFile = open("People.txt")
        for dataLine in dataFile.readlines():
            dataLine = dataLine[:len(dataLine) - 1]
            dummyPerson = Person()
            dummyPerson.name,dummyPerson.smoker,dummyPerson.manyVisitors,dummyPerson.status = dataLine.split(';')
            self.persons.append(dummyPerson)
            self.unAssignedPeople.append(dummyPerson)
            self.originalPeopleList.append(dummyPerson)
        dataFile.close()
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
        global count
        count = count + 1
        result = ReckursiveBacktracking(assignment,csp)
        if result != None:
            return result
        personToDelete = assignment[person]
        csp.office.officeRooms[personToDelete].contains.remove(person)
        csp.office.officeRooms[personToDelete].currentAmount -= 1
        del assignment[person]
    csp.office.persons.insert(0,person)
    if len(csp.office.persons) < len(csp.office.unAssignedPeople):
        csp.office.unAssignedPeople = list()
        for p in csp.office.persons:
            csp.office.unAssignedPeople.append(p)
    return None

def roomList(person,assignment,csp):
    roomsToReturn = list()
    for room in csp.office.officeRooms.keys():
        if csp.checkConstraints(person,csp.office.officeRooms[room]):
            roomsToReturn.append(room)
    if csp.office.MCV == True:
        roomsToReturn.sort()
        roomsToReturn.reverse()
        return roomsToReturn
    else:
        return roomsToReturn

def assign(person,room,assignment,csp):
    personToAppend = csp.office.officeRooms[room]
    personToAppend.contains.append(person)
    personToAppend.currentAmount += 1
    assignment[person] = room 

def LeastConstrainingVal(csp):
    csp.office.persons = list(csp.office.originalPeopleList)
    for person in csp.office.persons:
        if person.status == "head" or person.status == "professor":
            person.constraintsVal += 10
        if person.manyVisitors == "many visitors":
            person.constraintsVal += 7
        if person.smoker == "smoker":
            person.constraintsVal += 3
        else:
            person.constraintsVal += 0
    csp.office.persons.sort(key = lambda Person: Person.constraintsVal)
    csp.office.unAssignedPeople.clear()
    csp.office.unAssignedPeople = list(csp.office.persons)
    return ReckursiveBacktracking({},csp)

def MostConstrainedVariable(csp):
    csp.office.persons = list(csp.office.originalPeopleList)
    csp.office.unAssignedPeople.clear()
    csp.office.unAssignedPeople = list(csp.office.persons)
    csp.office.MCV = True
    return ReckursiveBacktracking({},csp)



count = 0 
csp = Constraints()
assignments = BackTrackingSearch(csp)

if assignments != None:
    for a in assignments.keys():
        print("Person:",a.name,"with status:",a.status,a.smoker,a.manyVisitors,"assigned to room:",assignments[a])
    del a
    assignments.clear()
else:
    print("Couldn't assign everybody")
    print("People that couldn't be assigned a room:")
    for person in csp.office.unAssignedPeople:
        print(person.name,person.status,person.smoker,person.manyVisitors)
    del person
print("It took",count,"recursions in order for the assignment to finish")

dummy = input("Press enter to do the other search!")
count = 0

for room in csp.office.officeRooms.values():
    room.contains.clear()
    room.currentAmount = 0

assignments = LeastConstrainingVal(csp)

if assignments != None:
    for a in assignments.keys():
        print("Person:",a.name,"with status:",a.status,a.smoker,a.manyVisitors,"assigned to room:",assignments[a])
    del a
    assignments.clear()
else:
    for person in csp.office.unAssignedPeople:
        print(person.name,person.status,person.smoker,person.manyVisitors)
print("It took",count,"recursions in order for the assignment to finish")

dummy = input("Press enter to do the other search!")
count = 0

for room in csp.office.officeRooms.values():
    room.contains.clear()
    room.currentAmount = 0

assignments = MostConstrainedVariable(csp)

if assignments != None:
    for a in assignments.keys():
        print("Person:",a.name,"with status:",a.status,a.smoker,a.manyVisitors,"assigned to room:",assignments[a])
    del a
    assignments.clear()
else:
    for person in csp.office.unAssignedPeople:
        print(person.name,person.status,person.smoker,person.manyVisitors)
print("It took",count,"recursions in order for the assignment to finish")

  
