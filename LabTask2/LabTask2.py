class Person:
    name = ""
    status = ""
    smoker = ""
    manyVisitors = ""

class Rooms:
    amount = 0
    contains = []

    def __init__(self,amount):
        self.contains = []
        self.amount = amount

class Office:
    persons = list()
    assignedPeople = list()
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
        del dataFile
        del dataLine
    
class Constraints:

    office = Office()

    def Smoker(self,one,roomList):
        for another in roomList.contains:
            if one.smoker != another.smoker:
                return False
        return True
         
    def Visitors(self,one,roomList):
        for another in roomList.contains:
            if one.manyVisitors == "many visitors" and another.manyVisitors == "many visitors":
                return False
        return True
    
    def assignRooms(self):
        for person in self.office.persons:
            for room in self.office.officeRooms.values():
                if person.status == "head" or person.status == "professor":
                    if room.amount == 2 or room.amount == 3:
                        if room.contains == []:
                            room.contains.append(person)
                            break
                else:
                    if self.Smoker(person,room):
                        if self.Visitors(person,room):
                            room.contains.append(person)
                            
                            break
                del room
        return True
    

    

const = Constraints()
const.assignRooms()
print("Woop")
  
