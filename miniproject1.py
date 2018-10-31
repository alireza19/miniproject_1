import sqlite3, time, random

connection = sqlite3.connect('miniproject1.db')
c = connection.cursor()
loggedIn = False
i = '1'

def register(email, name, phone, pwd):
    c.execute ("INSERT INTO members VALUES (:email, :name, :phone, :pwd)", {'email': email, 'name': name, 'phone': phone, 'pwd': pwd})
    
def askDupEmail(email):

    dupEmail = False
    c.execute("SELECT m.email FROM members m")
    emailList = c.fetchall()
    for items in emailList:
        if dupEmail == True:
            break
        for elements in (list(items)):
            if elements == email:
                print('This email already exist. Please try a different Email.')
                dupEmail = True
                break
    return dupEmail
    
def registering():
    
    
    mainInput = str(input("To register, type 1\nTo go back to main screen, type 2\nTo exit, type 0: "))
                        
    if mainInput == '1':
        valEmail = False
        
        while not valEmail:
            email = str(input("Enter your E-mail: "))
            if email == '0':
                loginScreen()
            
            if askDupEmail(email) == False:
                name = str(input("Enter your Name: "))
                phone = str(input("Enter your Phone Number: "))
                pwd = str(input("Enter your Pwd: "))
                valEmail = True
                register(email, name, phone, pwd)
                
    elif mainInput == '0':
        time.sleep(0.5)
        print('Exiting')
    
    else:
        registering()
        
 

def loginScreen():
    Input = input("\n\nPress 1 to login with a valid E-mail and Password.\nPress 2 to sign up today.\nPress 0 to exit this program.\t\t\t____")
    
    if Input == '1':    #if you are already a member
        login()
        
    elif Input == '2':  #if you want to sign up
        registering()       
        
    elif Input == '0':  # To exit
        print("Exiting...")
        time.sleep(0.5)
        print("goodBye!")
    else:
        print("Invalid input, Try Again!")
        loginScreen()
        
def printMessages(email):
    c.execute("SELECT i.content FROM inbox i, members m WHERE m.email = (:email) AND i.seen = 'n'", {'email': email})
    messages = c.fetchall()
    
    update_seen = """UPDATE inbox SET seen = 'y' WHERE seen = 'n'"""
    c.execute(update_seen)
    for item in messages:
        print(item)
    if messages == None:
        print('You have no new messages')

def offerRide(email):
    # give rdate, seats, lugDesc, src, dst, price
    # optional: add a cno and enroute.lcode
    #   if cno is entered: query and check that the cno belongs to the member
    # for locations: take an input from the member offering a ride that can be a keyword or lcode
    # if lcode: return the locations
    #   if len(location query) >= 5: limit to 5 results, give user option to see more or select a location
    #       if see more:
    #           display all matching locations (fetchall)
    #       elif select_location:
    #           take input for the locations
    #           valid_selection = True
    # elif not lcode: return all locations that have the keyword as a substring in city, province or address fields
    #   if len(location query) >= 5: limit to 5 results, give user the option to see more or select a location
    # if a valid_selection == True (i.e. is confirmed): assign a random rno and set that offering member as the driver.
    # ride_offer =  # pass off the offering member's email

#try:
    c.execute("SELECT rides.rdate, rides.seats, rides.lugDesc, rides.src, rides.dst, rides.price FROM rides WHERE rides.driver = (?)", (email,))
    #print("here")
#except:
    #pass
    #print("some error occurred")
#else:
    optional_input = str(input("would you like to add a car number and enroute locations? (y/n): "))
    valid_selection = False
    while not valid_selection:
        if optional_input == 'y':
            check_cno = "SELECT cars.cno, cars.owner, rides.cno, rides.driver FROM cars, rides WHERE cars.cno = rides.cno AND cars.owner = :email", {"email":email}
            c.execute(check_cno)
            if check_cno: # if the query returns True get the enroute location
                enroute_input = str(input("enter a location code (lcode) or a location keyword: "))
                enroute_location = get_location(enroute_input) # query the search with this function and return it
                print(enroute_location)
                #enroute_confirmation =
                #str(input("Please select from this list: %s", enroute_location))
                # book the enroute location
                valid_selection = True
        elif optional_input == 'n':
            location_input = str(input("Enter a location code or a location keyword: "))
            location = get_location(location_input)
            print(location)
            #location_confirmation =
            #str(input("Please select from this list: %s", location))
            # book the enroute locations
            valid_selection = True
        else:
            print("Please enter a valid input")
    if valid_selection:
        rno = random.randint(0, 100000)
        #update_offer = 
        c.execute("UPDATE rides SET driver = (:email), rno = (:rno)", {"email":email, "rno": rno})
        print("driver and ride number have been updated")

def get_location(location):
   try:
       c.execute("SELECT locations.lcode FROM locations WHERE locations.lcode LIKE (:location)", {"location":location})
       attempt1 = c.fetchall()
       return attempt1
   except:
       pass
   try:
       c.execute("SELECT locations.city FROM locations WHERE locations.city LIKE (:location)", {"location":location})
       attempt2 = c.fetchall()
       return attempt2
   except:
       pass
   try:
       c.execute("SELECT locations.prov FROM locations WHERE locations.prov LIKE (:location)", {"location":location})
       attempt3 = c.fetchall()
       return attempt3
   except:
       pass
   try:
       c.execute("SELECT locations.address FROM locations WHERE locations.address LIKE (:location)", {"location":location})
       attempt4 = c.fetchall()
       return attempt4
   except:
       pass
   else:
       print("please enter a better search term: ")


def SearchRides():
    locVal = False
    while not locVal:
        locNo = input('Type a number between 1 and 3 for the number of location keywords you want to enter.\nType 0 to exit: ')
        
        if locNo == '1': #or locNo == '2' or locNo =='3':
            searchInput = input('Enter the location key: ')
            
            c.execute("SELECT r.rno FROM rides r, locations l, enroute e WHERE (:searchInput) == r.src or (:searchInput) == r.dst or (:searchInput) == l.lcode or (:searchInput) == e.lcode or (:searchInput) == l.city or (:searchInput) == l.prov or (:searchInput) == l.address LIMIT 5" , {'searchInput': searchInput})
            SearchQuery = c.fetchall()
            print(SearchQuery)
            moreOption = input('To continue, type 1.\nTo view all the ride option, type 2.\nType 0 to exit: ')
            if moreOption =='2':
                
                c.execute("SELECT r.rno FROM rides r, locations l, enroute e WHERE (:searchInput) == r.src or (:searchInput) == r.dst or (:searchInput) == l.lcode or (:searchInput) == e.lcode or (:searchInput) == l.city or (:searchInput) == l.prov or (:searchInput) == l.address" , {'searchInput': searchInput})
                SearchQuery = c.fetchall()
                print(SearchQuery)
                
            elif moreOption =='0':
                print("Exiting...")
                time.sleep(0.5)
                print("goodBye!")                
                
            elif moreOption =='1':
                pass
            locVal = True
            
        elif locNo == '0':
            print("Exiting...")
            time.sleep(0.5)
            print("goodBye!")
            locVal = True

def bookings():
    pass


def rideRequests(email):
    
    c.execute("SELECT count(*) FROM requests")
    for item in (c.fetchall()):
        rid = item
    
    rid = rid[0] + 1
    rdate = input("Provide a date in MM/DD/YYYY form: ")
    pickup = input("Provide a Pick up Location code: ")
    dropoff = input("Provide a Drop off Location code: ")
    amount = input("Provide the amount willing to pay per seat: $")
    
    c.execute("INSERT INTO requests VALUES (:rid, :email, :rdate, :pickup, :dropoff, :amount)", {'rid': rid, 'email': email, 'rdate': rdate, 'pickup': pickup, 'dropoff': dropoff, 'amount': amount})
    print("The ride request has been successfully created!")

def searchDelRideReq():
    pass

def login():
    loginSuccess = False

    email = str(input("Please enter E-mail or press 0 to go back to main screen: "))
    if email == '0':
        loginScreen()
    pwd = str(input("Please enter password: "))
    c.execute("SELECT m.email FROM members m")
    userEmail = c.fetchall()
    
    userFound = False
    for items in userEmail:
        if userFound == True:
            break
        
        else:
            check = email in list(items)
            if check:
                userFound = True
                
                c.execute("SELECT m.pwd FROM members m WHERE m.email = (:email)", {'email': email})
                dataPwd = c.fetchall()
                
                for item in dataPwd:
                    if (pwd == ''.join(item)):
                        print("Login Successful!")
                        loggedIn = True
                        loginSuccess = True
                        break                           
    if not userFound:
        print("Invalid Email\n")
        login()
        
    if not loginSuccess:
        print("Invalid Password\n")
        login()
    
    if loggedIn:
        printMessages(email)
        optionVal = False
        while not optionVal:
            optionInput = input('\nPress 1 to Offer a ride.\nPress 2 to Search for rides.\nPress 3 to Book members or cancle bookings.\nPress 4 to Post ride requests.\nPress 5 to Search and delete ride requests.\nPress 0 to exit.\n')
            
            if optionInput == '1':
                offerRide(email)
                optionVal = True
                
            elif optionInput == '2':
                SearchRides()
                optionVal = True
                
            elif optionInput == '3':
                bookings()
                optionVal = True
                
            elif optionInput == '4':
                rideRequests(email)
                optionVal = True
                
            elif optionInput == '5':
                searchDelRideReq()
                optionVal = True
                
            elif optionInput == '0':  # To exit
                optionVal = True
                print("Exiting...")
                time.sleep(0.5)
                print("goodBye!")            
        
    
            
def main():
    loginScreen()
    connection.commit()
    connection.close()
    
main()