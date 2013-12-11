import operator
class Person:
    name = ""
    status = ""
    smoker = ""
    manyVisitors = ""
    constraintsVal = 0
    potentialRoomKey = list()
    potentialRooms = list()

class Rooms:
    amount = 0
    currentAmount = 0
    contains = []
    constraintsVal = 1000
    roomKey = ""

    def __init__(self,amount,roomKey):
        self.contains = []
        self.amount = amount
        self.roomKey = roomKey

class Office:
    persons = list()
    unAssignedPeople = list()
    originalPeopleList = list()
    officeRooms = dict()
    LCV = False
    countSmoker = 0
    countNonSmoker = 0
    countVisitors = 0
    countNoVisitors = 0
    
    def __init__(self):
        self.officeRooms['T13'] = Rooms(1,'T13')
        self.officeRooms['T14'] = Rooms(1,'T14')
        self.officeRooms['T15'] = Rooms(1,'T15')
        self.officeRooms['T16'] = Rooms(1,'T16')
        self.officeRooms['T11'] = Rooms(2,'T11')
        self.officeRooms['T12'] = Rooms(2,'T12')
        self.officeRooms['T10'] = Rooms(3,'T10')
        self.setPeople()

    def setPeople(self):
        dataFile = open("People.txt")
        for dataLine in dataFile.readlines():
            dataLine = dataLine[:len(dataLine) - 1]
            dummyPerson = Person()
            dummyPerson.name,dummyPerson.smoker,dummyPerson.manyVisitors,dummyPerson.status = dataLine.split(';')
            self.persons.append(dummyPerson)
            self.originalPeopleList.append(dummyPerson)
            self.unAssignedPeople.append(dummyPerson)
            if dummyPerson.smoker == "smoker":
                self.countSmoker += 1
            elif dummyPerson.smoker == "non-smoker":
                self.countNonSmoker += 1
            if dummyPerson.manyVisitors == "many visitors":
                self.countVisitors += 1
            elif dummyPerson.manyVisitors == "few visitors":
                self.countNoVisitors += 1
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
    returnKeys = list()
    for room in csp.office.officeRooms.keys():
        if csp.checkConstraints(person,csp.office.officeRooms[room]):
            returnKeys.append(room)
    return returnKeys

def assign(person,room,assignment,csp):
    personToAppend = csp.office.officeRooms[room]
    personToAppend.contains.append(person)
    personToAppend.currentAmount += 1
    assignment[person] = room 

def LeastConstrainingVal(person,csp,assignment):
    den den assignment som begränsar minst för andra.
    loopa igenom alla kvarvarande personers rum. räkna potentialla rum kvar efter assignment. Den ass som får mest potentialla rum kvar blir rum för assignment
    for i in person.potentialRoomKey:
        for r in csp.office.officeRooms.keys():
            if i == r:
                person.potentialRooms.append(csp.office.officeRooms[r])
                break
        del r
    for room in person.potentialRooms:
        if person.status == "head" or person.status == "professor":
            preCount = len(csp.office.persons) * len(csp.office.officeRooms)
        elif person.status != "head" and person.status != "professor":
            if person.smoker == "smoker" and person.manyVisitors == "many visitors":
                if room.currentAmount + 1 == room.amount:
                    preCount = (csp.office.countSmoker + csp.office.countVisitors) * (len(csp.office.officeRooms) - 1)
                else:
                    preCount = (csp.office.countSmoker + csp.office.countVisitors) * (len(csp.office.officeRooms))
            elif person.smoker == "non-smoker" and person.manyVisitors == "few visitors":
                if room.currentAmount + 1 == room.amount:
                    preCount = (csp.office.countNonSmoker + csp.office.countNoVisitors) * (len(csp.office.officeRooms) - 1)
                else:
                    preCount = (csp.office.countNonSmoker + csp.office.countNoVisitors (room.amount - room.currentAmount)) * (len(csp.office.officeRooms))
            elif person.smoker == "smoker" and person.manyVisitors == "few visitors":
                if room.currentAmount + 1 == room.amount:
                    preCount = (csp.office.countSmoker + csp.office.countNoVisitors) * (len(csp.office.officeRooms) - 1)
                else:
                    preCount = (csp.office.countSmoker + csp.office.countNoVisitors + (room.amount - room.currentAmount)) * (len(csp.office.officeRooms))
            elif person.smoker == "non-smoker" and person.manyVisitors == "many visitors":
                if room.currentAmount + 1 == room.amount:
                    preCount = (csp.office.countNonSmoker + csp.office.countVisitors) * (len(csp.office.officeRooms) - 1)
                else:
                    preCount = (csp.office.countNonSmoker + csp.office.countVisitors + (room.amount - room.currentAmount)) * (len(csp.office.officeRooms))
        if preCount < room.constraintsVal:
            room.constraintsVal = preCount
    

    person.potentialRooms.sort(key = lambda Rooms : Rooms.constraintsVal)
    person.potentialRooms.reverse()
    return person.potentialRooms

def MostConstrainedVariable(csp):
    csp.office.persons = list(csp.office.originalPeopleList)
    den person som har minst rum kvar att vara i.
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
    preAssign(csp)
    return ReckursiveBacktrackingWithH({},csp)

def preAssign(csp):
    for p in csp.office.persons:
        p.potentialRoomKey = list(roomList(p,{},csp))


def ReckursiveBacktrackingWithH(assignment,csp):
    if csp.office.persons == []:
        return assignment
    person = csp.office.persons.pop()
    for room in LeastConstrainingVal(person,csp):
        assignWithH(person,room,assignment)
        global count
        count = count + 1
        result = ReckursiveBacktracking(assignment,csp)
        if result != None:
            return result
        roomToDeletePersonFrom = assignment[person]
        csp.office.officeRooms[roomToDeletePersonFrom.roomKey].contains.remove(person)
        csp.office.officeRooms[roomToDeletePersonFrom.roomKey].currentAmount -= 1
        del assignment[person]
    csp.office.persons.insert(0,person)
    if len(csp.office.persons) < len(csp.office.unAssignedPeople):
        csp.office.unAssignedPeople = list()
        for p in csp.office.persons:
            csp.office.unAssignedPeople.append(p)
    return None

def assignWithH(person,room,assignment):
    room.contains.append(person)
    room.currentAmount += 1
    assignment[person] = room 
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

  
