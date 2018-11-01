import sqlite3, time, random

global connection, cursor
connection = sqlite3.connect('miniproject1.db')
cursor = connection.cursor()
loggedIn = False

def register(email, name, phone, pwd):
    cursor.execute ("INSERT INTO members VALUES (:email, :name, :phone, :pwd)", {'email': email, 'name': name, 'phone': phone, 'pwd': pwd})
    
def askDupEmail(email):

    dupEmail = False
    cursor.execute("SELECT m.email FROM members m")
    emailList = cursor.fetchall()
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
    cursor.execute("SELECT i.content FROM inbox i, members m WHERE m.email = (:email) AND i.seen = 'n'", {'email': email})
    messages = cursor.fetchall()
    
    update_seen = """UPDATE inbox SET seen = 'y' WHERE seen = 'n'"""
    cursor.execute(update_seen)
    for item in messages:
        print(item)
    if messages == None:
        print('You have no new messages')

def offerRide(email):

    is_valid_info = False
    while not is_valid_info:
        rdate = str(input("Please enter ride date: "))
        seats = str(input("Please enter number of seats: "))
        price = str(input("Please enter price per seat: "))
        lugDesc = str(input("Please enter a luggage description: "))
        src = str(input("Please enter a ride source: "))
        dst = str(input("Please enter ride destination: "))
        offer_info = [rdate, seats, price, lugDesc, src, dst, email]
        valid_info_res = cursor.execute("INSERT INTO rides (rdate, seats, price, lugDesc, src, dst, driver) VALUES ((:offer_info))", {"offer_info":offer_info})
        if valid_info_res:
            is_valid_info = True

    optional_cno_input = str(input("Would you like to add a car number? (y/n): "))
    if optional_cno_input == 'y':
        cno = str(input("Please enter your car number (cno): "))
        cno_info = [cno, email, rdate]
        cursor.execute("UPDATE rides SET cno = (:cno_info) WHERE rides.driver = (:cno_info) AND rides.rdate = (:cno_info)", {"cno_info":cno_info}) # update the cno for the logged in driver
    elif optional_cno_input == 'n':
        location_search_input = str(input("Please search for the appropriate lcode associate with your ride using lcode or using a keyword: "))
        location_search_result = get_location("%" + location_search_input + "%")
        if len(location_search_result) >= 5:
            location_decision_input = str(input("The search returned more than 5 locations matching your query. Would you like to see them all? (y/n): "))
            if location_decision_input == 'y':
                print("Please select from the following list:\nlcode\tCity\tProvince\tAddress")
                for i in range(len(location_search_result)):
                    print(location_search_result[i])
            elif location_decision_input == 'n':
                print("Please select from the following list:\nlcode\tCity\tProvince\tAddress")
                for j in range(5):
                    print(location_search_result[j])
            else:
                print("Invalid input. Try again")

        location_selection_input = str(input("lcode selection: "))
        location_selection_res = cursor.execute("SELECT locations.lcode FROM locations WHERE locations.lcode = (:lcode)", {"lcode":location_selection_input})
        
        if location_selection_res:
            rno = random.randint(1, 100000) # assign a random int to the rno
            rno_info = [rno, rdate, email]
            cursor.execute("UPDATE rides SET rno = (:rno_info) WHERE rdate = (:rno_info) AND driver = (:rno_info)", {"rno_info":rno_info}) # insert it into the rides table
            print("rno has been updated") # print a success message
        else:
            print("That location does not exist or is invalid. Try again.")
    else:
        print("Invalid input. Try again.")

    optional_enroute_input = str(input("Would you like to add an enroute location? (y/n): "))
    if optional_enroute_input == 'y':
        enroute_search_input = str(input("Please search for the appropriate lcode associate with your ride using lcode or a keyword: "))
        enroute_search_result = get_location("%" + enroute_search_input + "%")
        if len(enroute_search_result) >= 5:
            enroute_decision_input = str(input("The search returned more than 5 locations matching your query. Would you like to see them all? (y/n): "))
            if enroute_decision_input == 'y':
                print("Please select from the following list:\nlcode\tCity\tProvince\tAddress")
                for i in range(len(enroute_search_result)):
                    print(enroute_search_result[i])
            elif enroute_decision_input == 'n':
                print("Please select from the following list:\nlcode\tCity\tProvince\tAddress")
                for i in range(5):
                    print(enroute_search_result[i])
            else:
                print("Invalid input. Try again.")

        enroute_selection_input = str(input("lcode selection: "))
        enroute_selection_res = cursor.execute("SELECT locations.lcode FROM locations WHERE locations.lcode = (:lcode)", {"lcode":enroute_selection_input})

        if enroute_selection_res:
            enroute_info = [rno, enroute_selection_input]
            cursor.execute("INSERT INTO enroute (rno, lcode) VALUES (:enroute_info)", {"enroute_info":enroute_info}) #insert into enroute table where rno of location is the same
            enroute_again_input = str(input("Enroute location added.\nWould you like to add another enroute location? (y/n): "))
            if enroute_again_input == 'y':
                optional_enroute_input == 'y'
            elif enroute_again_input == 'n':
                optional_enroute_input == 'n'
            else:
                print("Invalid input. Try again.")
        
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

# #try:
#     cursor.execute("SELECT rides.rdate, rides.seats, rides.lugDesc, rides.src, rides.dst, rides.price FROM rides WHERE rides.driver = :email", {"email":email})
#     #print("here")
# #except:
#     #pass
#     #print("some error occurred")
# #else:
#     optional_input = str(input("would you like to add a car number and enroute locations? (y/n): "))
#     valid_selection = False
#     while not valid_selection:
#         if optional_input == 'y':
#             enroute_decision = False
#             while not enroute_decision:
#                 check_cno = "SELECT cars.cno, cars.owner, rides.cno, rides.driver FROM cars, rides WHERE cars.cno = rides.cno AND cars.owner = :email", {"email":email}
#                 cursor.execute(check_cno)
#                 if check_cno: # if the query returns True get the enroute location
#                     enroute_input = str(input("enter a location code (lcode) or a location keyword: "))
#                     enroute_location = get_location("%" + enroute_input + "%") # query the search with this function and return it
#                     if len(enroute_location) >= 5:
#                         see_more_enroute = str(input("There are more than 5 locations that match your query. Would you like to see them all? (y/n): "))
#                         if see_more_enroute =='y':
#                             print("lcode\tCity\tProvince\tAddress")
#                             for i in range(len(enroute_location)):
#                                 print(enroute_location[i])
#                         elif see_more_enroute == 'n':
#                             print("lcode\tCity\tProvince\tAddress\t")
#                             for j in range(5):
#                                 print(enroute_location[j])
#                     valid_enroute_lcode = False
#                     while not valid_enroute_lcode:
#                         enroute_lcode_selection = str(input("Please select a lcode from above: "))
#                         enroute_lcode_res = cursor.execute("SELECT * FROM locations WHERE locations.lcode = (:lcode)", {"lcode":enroute_lcode_selection})
#                         if enroute_lcode_res:
#                             cursor.execute("INSERT INTO enroute (lcode) VALUES ((:lcode))", {"lcode":enroute_lcode_selection})
#                             valid_enroute_lcode = True
#                         else:
#                             print("That location does not exist. Please try again.")
#                     enroute_decision_input = str(input("Would you like to add another enroute location? (y/n): "))
#                     if enroute_decision_input == 'y':
#                         enroute_decision = False
#                     elif enroute_decision_input == 'n':
#                         enroute_decision = True
#             valid_selection = True
#         elif optional_input == 'n':
#             location_input = str(input("Enter a location code or a location keyword: "))
#             location = get_location("%" + location_input + "%")
#             #print(location)
#             if len(location) >= 5:
#                 see_more = str(input("There are more than 5 locations that match your query. Would you like to see them all? (y/n): "))
#                 if see_more =='y':
#                     print("lcode\tCity\tProvince\tAddress")
#                     for i in range(len(location)):
#                         print(location[i])
#                 elif see_more == 'n':
#                     print("lcode\tCity\tProvince\tAddress\t")
#                     for j in range(5):
#                         print(location[j])
#             #print(location)
#             #location_confirmation =
#             #str(input("Please select from this list: %s", location))
#             # book the enroute locations
#             valid_selection = True
#         else:
#             print("Please enter a valid input")
#     if valid_selection:
#         rno = random.randint(0, 100000)
#         #update_offer = 
#         cursor.execute("INSERT INTO rides (email, rno) VALUES ((:email), (:rno))", {"email":email, "rno": rno})
#         print("driver and ride number have been updated")


def get_location(location):

    try:
        cursor.execute("SELECT * FROM locations WHERE locations.prov LIKE (:location) OR locations.city LIKE (:location) OR locations.address LIKE (:location) OR locations.lcode LIKE (:location)", {"location":location})
        attempt = cursor.fetchall()
        #print("here1")
    except sqlite3.Error as e:
        print('Error:'), e.args[0]
    else:
        return attempt


def SearchRides():
    locVal = False
    while not locVal:
        locNo = input('Type a number between 1 and 3 for the number of location keywords you want to enter.\nType 0 to exit: ')
        
        if locNo == '1': #or locNo == '2' or locNo =='3':
            searchInput = input('Enter the location key: ')
            
            cursor.execute("SELECT r.rno FROM rides r, locations l, enroute e WHERE (:searchInput) == r.src or (:searchInput) == r.dst or (:searchInput) == l.lcode or (:searchInput) == e.lcode or (:searchInput) == l.city or (:searchInput) == l.prov or (:searchInput) == l.address LIMIT 5" , {'searchInput': searchInput})
            SearchQuery = cursor.fetchall()
            print(SearchQuery)
            moreOption = input('To continue, type 1.\nTo view all the ride option, type 2.\nType 0 to exit: ')
            if moreOption =='2':
                
                cursor.execute("SELECT r.rno FROM rides r, locations l, enroute e WHERE (:searchInput) == r.src or (:searchInput) == r.dst or (:searchInput) == l.lcode or (:searchInput) == e.lcode or (:searchInput) == l.city or (:searchInput) == l.prov or (:searchInput) == l.address" , {'searchInput': searchInput})
                SearchQuery = cursor.fetchall()
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
    
    cursor.execute("SELECT count(*) FROM requests")
    for item in (cursor.fetchall()):
        rid = item
    
    rid = rid[0] + 1
    rdate = input("Provide a date in MM/DD/YYYY form: ")
    pickup = input("Provide a Pick up Location code: ")
    dropoff = input("Provide a Drop off Location code: ")
    amount = input("Provide the amount willing to pay per seat: $")
    
    cursor.execute("INSERT INTO requests VALUES (:rid, :email, :rdate, :pickup, :dropoff, :amount)", {'rid': rid, 'email': email, 'rdate': rdate, 'pickup': pickup, 'dropoff': dropoff, 'amount': amount})
    print("The ride request has been successfully created!")

def searchDelRideReq():
    pass

def login():
    loginSuccess = False

    email = str(input("Please enter E-mail or press 0 to go back to main screen: "))
    if email == '0':
        loginScreen()
    pwd = str(input("Please enter password: "))
    cursor.execute("SELECT m.email FROM members m")
    userEmail = cursor.fetchall()
    
    userFound = False
    for items in userEmail:
        if userFound == True:
            break
        
        else:
            check = email in list(items)
            if check:
                userFound = True
                
                cursor.execute("SELECT m.pwd FROM members m WHERE m.email = (:email)", {'email': email})
                dataPwd = cursor.fetchall()
                
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