import subprocess as sp
import pymysql
import pymysql.cursors
# import required module
import mysql.connector


# Functional requirements
def VOTE(candidate_name):
    # connect python with mysql with your hostname, database, user and password
    db = mysql.connector.connect(host='localhost',
                                database='election',
                                user='root',
                                password='mysql123')

    # create cursor object
    cursor = db.cursor()

    query = "SELECT number_of_votes FROM election_results WHERE candidate_name = " + str(candidate_name)
    cursor.execute(query)

    # fetch Vote_Count and display it
    result = cursor.fetchall()[0][0]
    ans = str(candidate_name) + " received " + str(result) + " votes"
    print(ans)

    # terminate connection
    db.close()

    

def WINNER(constituency_name):
    # connect python with mysql with your hostname, database, user and password
    db = mysql.connector.connect(host='localhost',
                                database='election',
                                user='root',
                                password='mysql123')

    # create cursor object
    cursor = db.cursor()

    query = "SELECT party_voted_for, COUNT(*) FROM voters WHERE voters.constituency_name = " + str(constituency_name) + " GROUP BY party_voted_for"
    cursor.execute(query)

    # fetch Election_Winner and display it
    max_votes = 0
    idx = 0
    result = cursor.fetchall()
    for i in range(len(result)):
        if result[i][1] > max_votes:
            max_votes = result[i][1]
            idx = i
    
    ans = str(result[idx][0]) + " won the election with " + str(max_votes) + " votes!"
    print(ans)

    # terminate connection
    db.close()



def PARTY(party_name):
    # connect python with mysql with your hostname, database, user and password
    db = mysql.connector.connect(host='localhost',
                                database='election',
                                user='root',
                                password='mysql123')

    # create cursor object
    cursor = db.cursor()

    query = "SELECT constituency FROM election_results WHERE party_name = " + str(party_name)
    cursor.execute(query)

    # fetch Constituencies and display it
    ans = "List of constituencies where " + str(party_name) + " won: "
    print(ans)
    result = cursor.fetchall()
    for i in range(len(result)):
        print(result[i][0])

    # terminate connection
    db.close()



def total_party_votes(party_name):
    # connect python with mysql with your hostname, database, user and password
    db = mysql.connector.connect(host='localhost',
                                database='election',
                                user='root',
                                password='mysql123')

    # create cursor object
    cursor = db.cursor()

    # fetch Total_Votes of party and display it
    query = "SELECT COUNT(*) FROM voters WHERE party_voted_for = " + str(party_name)
    result = cursor.execute(query)
    ans = str(party_name) + " won " + str(result) + " votes!"
    print(ans)

    # terminate connection
    db.close()



def voter_turnover(constituency):
    # connect python with mysql with your hostname, database, user and password
    db = mysql.connector.connect(host='localhost',
                                database='election',
                                user='root',
                                password='mysql123')

    # create cursor object
    cursor = db.cursor()

    query = "SELECT name FROM constituencies"
    result = cursor.execute(query)
    flag = 0
    for t in result:
        if t[0] == constituency:
            flag = 1
            break

    # constituency is not in the constituencies table
    if flag == 0:
        print("Error: unknown constituency")
        db.close()
        return

    query = "SELECT COUNT(*) FROM voters WHERE constituency_name = " + str(constituency)
    n = cursor.execute(query)

    query = "SELECT COUNT(*) FROM voters WHERE party_voted_for IS NOT NULL"
    x = cursor.execute(query)

    result = "Voter turnover in " + str(constituency) + " is " + str(x/n * 100) + "%"
    print(result)

    # terminate connection
    db.close()



# Updates
def add_voter(id, name, age, aadhar, vote, constituency):
    # Error check
    if len(str(aadhar)) != 12:
        print("Error: Invalid aadhar number")
        return

    # connect python with mysql with your hostname, database, user and password
    db = mysql.connector.connect(host='localhost',
                                database='election',
                                user='root',
                                password='mysql123')

    # create cursor object
    cursor = db.cursor()

    query = "SELECT id, aadhar FROM voters"
    result = cursor.execute(query)
    flag = 0
    for t in result:
        if t[0] == id or t[3] == aadhar:
            flag = 1
            break

    if flag == 1:
        print("Error: id or aadhar number already exists in the database")
        db.close()
        return

    query = "SELECT name FROM constituencies"
    result = cursor.execute(query)
    flag = 0
    for t in result:
        if t[0] == constituency:
            flag = 1
            break

    # constituency is not in the constituencies table
    if flag == 0:
        print("Error: unknown constituency")
        db.close()
        return

    if vote == "ABSENT":
        vote = "NULL"

    query = "INSERT INTO voters VALUES ( " + str(id) + ", " + str(name) + ", " + str(age) + ", " + str(aadhar) + ", " + str(vote) + ", " + str(constituency) + " )"
    cursor.execute(query)

    # terminate connection
    db.close()



def update_voter_age(id, aadhar, new_age):
    # Error check
    if len(str(aadhar)) != 12:
        print("Error: Invalid aadhar number")
        return

    # connect python with mysql with your hostname, database, user and password
    db = mysql.connector.connect(host='localhost',
                                database='election',
                                user='root',
                                password='mysql123')

    # create cursor object
    cursor = db.cursor()

    query = "UPDATE TABLE voters SET age = " + str(new_age) + " WHERE id = " + str(id) + " AND aadhar_number = " + str(aadhar)
    cursor.execute(query)

    # terminate connection
    db.close()



def add_party(name, leader, symbol, type):
    # connect python with mysql with your hostname, database, user and password
    db = mysql.connector.connect(host='localhost',
                                database='election',
                                user='root',
                                password='mysql123')

    # create cursor object
    cursor = db.cursor()

    query = "INSERT INTO political_parties VALUES ( " + str(name) + ", " + str(leader) + ", " + str(symbol) + ", " + str(type) + " )"
    cursor.execute(query)

    # terminate connection
    db.close()



def dispatch(ch):
    """
    Function that maps helper functions to option entered
    """

    if(ch == 1):
        name = input("Enter the candidate name: ")
        VOTE(name)
    elif(ch == 2):
        name = input("Enter the constituency name: ")
        WINNER(name)
    elif(ch == 3):
        name = input("Enter the party name: ")
        PARTY(name)
    elif(ch == 4):
        name = input("Enter the party name: ")
        total_party_votes(name)
    elif(ch == 5):
        constituency = input("Enter the constituency: ")
        voter_turnover(constituency)
    elif(ch == 6):
        voter_id = input("Enter the voter id: ")
        name = input("Enter the name of voter: ")
        age = input("Enter voter's age: ")
        aadhar = input("Enter 12-digit aadhar number of voter: ")
        check = input("Would you like to vote for a party? (y/n): ")
        if check == 'y':
            vote = input("Enter party voted for: ")
        else:
            vote = "ABSENT"
        constituency = input("Enter the constituency the voter is registered in: ")
        add_voter(voter_id, name, age, aadhar, vote, constituency)
    elif(ch == 7):
        voter_id = input("Enter the voter id: ")
        aadhar = input("Enter 12-digit aadhar number of voter: ")
        age = input("Enter voter's age: ")
        update_voter_age(voter_id, aadhar, age)
    elif(ch == 8):
        name = input("Enter the name of the party: ")
        leader = input("Enter party leader: ")
        symbol = input("Enter party symbol (as one word): ")
        type = input("Enter party type (regional/national): ")
        add_party(name, leader, symbol, type)
    else:
        print("Error: Invalid Option")


# Global
# while(1):
    # tmp = sp.call('clear', shell=True)
    
    # # Can be skipped if you want to hardcode username and password
    # username = input("Username: ")
    # password = input("Password: ")

    # try:
    #     # Set db name accordingly which have been create by you
    #     # Set host to the server's address if you don't want to use local SQL server 
    #     con = pymysql.connect(host='localhost',
    #                           # port=30306,
    #                           user="root",
    #                           password="password",
    #                           db='election',
    #                           cursorclass=pymysql.cursors.DictCursor)
    #     tmp = sp.call('clear', shell=True)

    #     if(con.open):
    #         print("Connected")
    #     else:
    #         print("Failed to connect")

    #     tmp = input("Enter any key to CONTINUE>")

    #     with con.cursor() as cur:
    while(1):
        # tmp = sp.call('clear', shell=True)
        # Here taking example of election miniworld
        print("1. Count the number of votes for a candidate")                               # VOTE(candidate_name)
        print("2. Find the winner of an election in a constituency")                        # WINNER(constituency)
        print("3. Display a list of all constituencies where a party won in an election")   # PARTY(party_name) 
        print("4. Count the number of votes for a party in an election")                    # total_party_votes(party_name)
        print("5. Voter turnover in a constituency")
        print("6. Add a new voter")
        print("7. Change voter age")
        print("8. Add political party")
        print("9. Logout")                                                                  # exit
        ch = int(input("Enter choice> "))
        # tmp = sp.call('clear', shell=True)
        if ch == 9:
            exit()
        else:
            dispatch(ch)
            tmp = input("Enter any key to CONTINUE>")

    # except Exception as e:
    #     tmp = sp.call('clear', shell=True)
    #     print(e)
    #     print("Connection Refused: Either username or password is incorrect or user doesn't have access to database")
    #     tmp = input("Enter any key to CONTINUE>")
