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

    is_valid_info = False
    while not is_valid_info: # until a successful query is executed, repeat
        rdate = str(input("Please enter ride date: "))
        seats = str(input("Please enter number of seats: "))
        price = str(input("Please enter price per seat: "))
        lugDesc = str(input("Please enter a luggage description: "))
        src = str(input("Please enter a ride source: "))
        dst = str(input("Please enter ride destination: "))
        #offer_info = (rdate, seats, price, lugDesc, src, dst, email)
        valid_info_res = cursor.execute("INSERT INTO rides (rdate, seats, price, lugDesc, src, dst, driver) VALUES ((:rdate), (:seats), (:price), (:lugDesc), (:src), (:dst), (:email))", {"rdate":rdate, "seats":seats, "price":price, "lugDesc":lugDesc, "src":src, "dst":dst, "email":email})
        if valid_info_res:
            connection.commit()
            is_valid_info = True

    is_valid_optional_cno = False
    while not is_valid_optional_cno: # until a valid input is given, repeat
        optional_cno_input = str(input("Would you like to add a car number? (y/n): "))

        if optional_cno_input == 'y':
            cno = str(input("Please enter your car number (cno): "))
            #cno_info = [cno, email, rdate]
            cursor.execute("SELECT * FROM cars WHERE cars.cno = (:cno) AND cars.owner = (:email)", {"cno":cno, "email":email})
            if cursor.fetchone() is not None: # if the cno is associated to the owner, update it
                cursor.execute("UPDATE rides SET cno = (:cno) WHERE rides.driver = (:email) AND rides.rdate = (:rdate)", {"cno":cno, "email":email, "rdate":rdate}) # update the cno for the logged in driver
                connection.commit()
            else:
                optional_cno_try_again = str(input("That cno does not exist. Try again? (y/n): "))
                if optional_cno_try_again == 'y':
                    optional_cno_input = 'y'
                elif optional_cno_try_again == 'n':
                    print("cno not updated.")
                    optional_cno_input = 'n' # move to the next step (get the location input)
                
        elif optional_cno_input == 'n':
            is_valid_location_selection = False
            while not is_valid_location_selection: # until a valid lcode is selected, repeat
                location_search_input = str(input("Please search for the appropriate lcode associate with your ride using lcode or using a keyword: "))
                location_search_result = split_list(get_location("%" + location_search_input + "%"), 5) # call the function to query the input

                scroll(location_search_result) # allow the user to scroll through the results

                location_selection_input = str(input("lcode selection: ")) # take an lcode selection
                cursor.execute("SELECT locations.lcode FROM locations WHERE locations.lcode = (:lcode)", {"lcode":location_selection_input}) # query it
                #connection.commit()
                if cursor.fetchone() is not None: # test the query to see if it exists
                    rno = random.randint(1, 100000) # assign a random int to the rno
                    cursor.execute("UPDATE rides SET rno = (:rno) WHERE rdate = (:rdate) AND driver = (:email)", {"rno":rno, "rdate":rdate, "email":email}) # insert it into the rides table
                    print("rno has been updated") # print a success message
                    connection.commit()
                    is_valid_location_selection = True 
                else:
                    print("That location does not exist or is invalid. Try again.")

            is_valid_optional_cno = True

        else:
            print("Invalid input. Try again.")
    is_valid_optional_enroute_input = False

    while not is_valid_optional_enroute_input:
        optional_enroute_input = str(input("Would you like to add an enroute location? (y/n): "))
        if optional_enroute_input == 'y':
            is_valid_enroute_location = False
            while not is_valid_enroute_location:
                enroute_search_input = str(input("Please search for the appropriate lcode associate with your ride using lcode or a keyword: "))
                enroute_search_result = split_list(get_location("%" + enroute_search_input + "%"), 5) # split the list of the location list into n sized chunks

                scroll(enroute_search_result) # allow user to scroll through the results

                enroute_selection_input = str(input("lcode selection: "))
                cursor.execute("SELECT locations.lcode FROM locations WHERE locations.lcode = (:lcode)", {"lcode":enroute_selection_input})

                if cursor.fetchone() is not None:
                    #enroute_info = [rno, enroute_selection_input]
                    cursor.execute("INSERT INTO enroute (rno, lcode) VALUES ((:rno), (:enroute_selection_input))", {"rno":rno ,"enroute_selection_input":enroute_selection_input}) #insert into enroute table where rno of location is the same
                    connection.commit()
                    enroute_again_input = str(input("Enroute location added.\nWould you like to add another enroute location? (y/n): "))
                    if enroute_again_input == 'y':
                        optional_enroute_input = 'y'
                    elif enroute_again_input == 'n':
                        #optional_enroute_input = 'n'
                        is_valid_enroute_location = True
                        is_valid_optional_enroute_input = True
                    else:
                        print("Invalid input. Try again.")
                else:
                    print("That is an invalid lcode. Try again.")
        elif optional_enroute_input == 'n':
            print("No enroute location added.")
            is_valid_optional_enroute_input = True
        else:
            print("Invalid input. Try again.")

def get_location(location):

    try:
        cursor.execute("SELECT * FROM locations WHERE locations.prov LIKE (:location) OR locations.city LIKE (:location) OR locations.address LIKE (:location) OR locations.lcode LIKE (:location)", {"location":location})
        attempt = cursor.fetchall()
        #print("here1")
    except sqlite3.Error as e:
        print('Error:'), e.args[0]
    else:
        return attempt

def split_list(arr, n): # splits an arr into n sized chunks -> arr

    return [arr[i * n:(i + 1) * n] for i in range((len(arr) + n - 1) // n)]

def print_next(arr, last_iter, new_iter): # a function to print the next elements in an array -> None

    for i in range(last_iter, new_iter):
        for j in range(len(arr[i])):
            print(arr[i][j])

def scroll(arr): # a function to scroll through an arr of results -> None
    see_more = False
    from_iter = 0
    up_to = 0
    while (from_iter < len(arr) and up_to < len(arr) and not see_more):
        up_to += 1
        if len(arr[from_iter]) != 5: # if there are less than 5 results
            for i in range(from_iter, up_to):
                for j in range(len(arr[i])):
                    print(arr[i][j])
            print("End of results.")
            see_more = True
        else: # if there are more than 5
            print_next(arr, from_iter, up_to) #results, prompt with an input message to see more
            see_more_input = str(input("Press s to scroll down or press 0 to enter lcode: "))
            if see_more_input == "s":
                from_iter += 1
                print_next(arr, from_iter, up_to)
                #print(from_iter, up_to)                                    
            elif see_more_input == "0":
                see_more = True

    
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