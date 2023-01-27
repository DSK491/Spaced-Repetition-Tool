import os
import datetime
from datetime import timedelta
import sys
import sqlite3


INT1, INT2, INT3 = 1, 3, 15
today = datetime.date.today()
# Open Database
DBH = sqlite3.connect('Repetition Database.sqlite')
db = DBH.cursor()
# try:
#     #print('try')
#     db.execute(f"Update Info SET Value = {today.strftime('%d%m%y')} WHERE Key = 'Last Updated'")
#     DBH.commit()
# except:
#     print('Database is locked')
#     sys.exit(1)
# Menu Items
main_menu = ['Add Data', 'View/Log Data', 'Modify Data', 'Misc', 'Quit']
add_menu = ['Date', 'Semester', 'Subject', 'Topic', 'Module', 'Details']
path = []
# print(today)
# time.sleep(5)

def Abort():
    print('\nToo many attempts')
    input("Press Enter to return to main menu...")
# Center aligns text passed as argument
terlen = 0
def Print_Center(text):
    global terlen
    terlen = os.get_terminal_size()[0]
    #terlen = 80
    print(text.center(terlen))

# Introduction
def Intro():
    global path
    os.system('clear')
    Print_Center('Spaced Repetition Tool')
    # print(path)
    for i in path:
        print(i, end='')
    print('')
        
# Creates new table with argument passed as table name
def New_Table(sem, title):
    db.execute(f"CREATE TABLE IF NOT EXISTS S{sem + title} (Date TEXT, Topic TEXT, Module INTEGER, Details TEXT, Date1 TEXT, Status1 INTEGER, Date2 TEXT, Status2 INTEGER, Date3 TEXT, Status3 INTEGER)")

# Update statuses
def Update_Data():
    presdate = today.strftime('%d/%m/%y')
    Tablenamecur = db.execute("SELECT name from sqlite_schema")
    tablenames = list()
    #Adds subject names to a list
    for val in Tablenamecur:
        if 'S' in val[0]:
            tablenames.append(val[0])
    for table in tablenames:
        # print(table)
        num = 1
        while num <= 3:
            # print(num)
            DBH.execute(f"UPDATE {table} SET Status{num} = -1 WHERE Date{num} = \'{presdate}\'")
            Datecur = DBH.execute(f"SELECT Date{num} FROM {table}")
            for posdate in Datecur:
                # print(posdate, end = ' ')
                POSDATE = datetime.datetime.strptime(posdate[0], '%d/%m/%y')
                PRESDATE = datetime.datetime.strptime(presdate, '%d/%m/%y')
                # Overdue case
                if POSDATE < PRESDATE:
                    db.execute(f"UPDATE {table} SET Status{num} = -2 WHERE Date{num} = \'{posdate[0]}\' AND Status{num} != 1")
                    # print('overdue')
                # Future case
                if POSDATE > PRESDATE:
                    db.execute(f"UPDATE {table} SET Status{num} = 0 WHERE Date{num} = \'{posdate[0]}\' AND Status{num} != 1")
                    # print('not yet due')
            num += 1
    DBH.commit()
    print('Statuses updated.\n')

# Main menu
def Main_Menu():
    global main_menu
    global path
    path = []
    Intro()
    i = 0
    index = -1
    
    # if last updated date is not today run Update_Data() and update last updated date
    LASTUPCUR = db.execute("SELECT Value FROM Info WHERE Key = 'Last Updated'")
    for x in LASTUPCUR: LUpdated = x[0]
    if str(datetime.datetime.strptime(LUpdated, "%d%m%y")).split()[0] != str(datetime.date.today()):
        Update_Data()
    try:
        db.execute(f"Update Info SET Value = {today.strftime('%d%m%y')} WHERE Key = 'Last Updated'")
        DBH.commit()
    except:
        print('Database is locked')
        sys.exit(1)
    
    print('Perform action:')
    for item in range(len(main_menu)):
        print(f"{item+1}) {main_menu[item]}")

    # 3 Attempts to get input
    while i < 3:
        try:
            index = input("\nIndex of submenu: ").strip()
            if index == '':
                print(f'Enter an index between 1 and {len(main_menu)}')
            elif int(index) < len(main_menu) + 1 and int(index) > 0:
                path.append('\nMenu Path: ')
                path.append(main_menu[int(index) - 1] + ' > ')
                return int(index)
            else:
                print(f'Enter valid index between 1 and {len(main_menu)}')
        except:
            print('Enter Integers Only')
        i += 1
    sys.exit('\n\nProgram Aborted: Too Many Attempts\n\n')

# Submenu 'Add Data'
Date3Rev, Date2Rev, Date1Rev, Overdue1Rev, Overdue2Rev, Overdue3Rev, Revcomp, DateORev = [], [], [], [], [], [], [], []
#Adds subject names to a list
Tablenamecur = db.execute("SELECT name from sqlite_schema")
tablenames = list()
for val in Tablenamecur:
    if 'S' in val[0]:
        tablenames.append(val[0])

# View Today's Data
def View_Today_Data():
    global Date3Rev, Date2Rev, Date1Rev, Overdue1Rev, Overdue2Rev, Overdue3Rev, Revcomp, tablenames
    # Save due revision dates and info as lists in lists
    # DATE1
    for teams in tablenames:
        STem = DBH.execute(f"SELECT Date, Topic, Module, Details FROM {teams} WHERE Status1 = -1")
        for due in STem:
            tem = []
            tem.append(teams)
            for item in due:
                tem.append(item)
            Date1Rev.append(tem)
        # checks for overdue
        OTem = DBH.execute(f"SELECT Date, Topic, Module, Details, Date1, Date2, Date3 FROM {teams} WHERE Status1 = -2")
        for due in OTem:
            tem = []
            tem.append(teams)
            for item in due:
                tem.append(item)
            Overdue1Rev.append(tem)
    #DATE2
    for teams in tablenames:
        STem = DBH.execute(f"SELECT Date, Topic, Module, Details FROM {teams} WHERE Status2 = -1")
        for due in STem:
            tem = []
            tem.append(teams)
            # print(tem)
            # print('...')
            for item in due:
                tem.append(item)
            Date2Rev.append(tem)
        # checks for overdue
        OTem = DBH.execute(f"SELECT Date, Topic, Module, Details, Date1, Date2, Date3 FROM {teams} WHERE Status2 = -2")
        for due in OTem:
            tem = []
            tem.append(teams)
            for item in due:
                tem.append(item)
            Overdue2Rev.append(tem)
 
    #DATE3
    for teams in tablenames:
        STem = DBH.execute(f"SELECT Date, Topic, Module, Details FROM {teams} WHERE Status3 = -1")
        for due in STem:
            tem = []
            tem.append(teams)
            # print(tem)
            # print('...')
            for item in due:
                tem.append(item)
            Date3Rev.append(tem)
        # checks for overdue
        OTem = DBH.execute(f"SELECT Date, Topic, Module, Details, Date1, Date2, Date3 FROM {teams} WHERE Status3 = -2")
        for due in OTem:
            tem = []
            tem.append(teams)
            for item in due:
                tem.append(item)
            Overdue3Rev.append(tem)


def View_OtherDays_Data(date_inp):
    # print('a')
    global Date3Rev, Date2Rev, Date1Rev, Overdue1Rev, Overdue2Rev, Overdue3Rev, Revcomp, tablenames, DateORev
    # DATE1
    # print('b')
    for teams in tablenames:
        # print('c')
        for xyz in range(3):
            xyz += 1
            # print('d')
            STem = DBH.execute(f"SELECT Date, Topic, Module, Details FROM {teams} WHERE Date{xyz} = \'{date_inp}\' AND (Status{xyz} = -1 OR Status{xyz} = -2)")
            for due in STem:
                tem = []
                tem.append(teams)
                for item in due:
                    tem.append(item)
                DateORev.append(tem)

def Add_Data():
    Intro()
    global add_menu
    global date
    print('\n\nInput Data:\n')

#%% Date Details
    i = 0
    att = 0
    date_t = today.strftime("%d %B %Y")
    while i < 3:
        try:
            date = input(f"{add_menu[0]}: DD/MM/YY ({date_t})? ").strip()
            if date == '':
                date = today.strftime('%d/%m/%y')
                print(f"Date saved as '{today.strftime('%d/%m/%y')}'\n")
                break
            elif list(date).count('/') == 2:
                try:
                    bool(datetime.datetime.strptime(date, '%d/%m/%y'))
                    print('Date saved.\n')
                    break
                except:
                    print('Invalid date')
                    att += 1
            else:
                raise Exception
        except:
            print(f'Error. Date will be saved as \'{date_t}\'')
            att += 1
        finally:
            i += 1
            if att >= 3:
                Abort()
                return

#%% Semester Details
    i = 0
    att = 0
    sem = db.execute("SELECT Value from Info WHERE Key = 'Semester' LIMIT 1").fetchall()[0][0]
    # 3 attempts to get input
    while i < 3:
        try:
            semester = input(f"{add_menu[1]}: ({sem})? ").strip()
            
            # Subject details start
            subject_list = list()
            sub_cur = db.execute('SELECT name FROM sqlite_schema')
            for val in sub_cur:
                if f'S{semester}' in val[0]:
                    subject_list.append(val[0])
            if len(subject_list) == 0:
                cont = input("Selected semester does not have any data. Proceed? (yes/no) ").strip()
                if cont == 'yes' or cont == '':
                    semester = sem
                    print('Semester saved.\n')
                    break
                else:
                    att += 1
            # Subject details end
            elif semester == '':
                semester = sem
                print(f"Semester saved as {sem}\n")
                break
            elif int(semester) > 0 and int(semester) < 9:
                print('Semester saved.\n')
                break
            else:
                print('Enter valid semester between 1 and 8')
                att += 1
        except:
            print('Enter a valid integer')
            att += 1
        i += 1
        if att >= 3:
            Abort()
            return
    db.execute(f"UPDATE Info SET Value = {semester} WHERE Key = 'Semester'")
    

#%% Subject Details
    i = 0
    j = 0
    att = 0
    att1 = 0
    # subject_list = list()
    # sub_cur = db.execute('SELECT name FROM sqlite_schema')
    # for val in sub_cur:
    #     if val[0].startswith(f'S{semester}'):
    #         subject_list.append(val[0])
    subject_list.append('  New Subject')
    #print(subject_list)
    print(f"{add_menu[2]}:")
    for val in range(len(subject_list)):
        print(f"{val + 1}) {subject_list[val][2:]}")
    # 3 Attempts to get input
    while i < 3:
        try:
            sub_i = int(input('Index of subject: '))
            if int(sub_i) > 0 and int(sub_i) < len(subject_list) + 1:
                if sub_i == len(subject_list):
                    # 3 attempts to get new subject title
                    while j < 3:
                        table_name = input('Enter name of new subject: ')
                        subcon = input(f"Confirm new subject is {table_name} (yes/no) ").strip()
                        if subcon == 'yes' or subcon == '':
                            #print('accepted...')
                            subject = 'S' + semester + table_name
                            New_Table(semester, table_name)
                            print(f'New subject saved as {subject}\n')
                            break
                        else:
                            att1 += 1
                        j += 1
                        if att1 >= 3:
                            Abort()
                    break
                else:
                    subject = subject_list[sub_i - 1]
                    print('Subject saved.\n')
                    break
            else:
                print(f'Enter index of subject between 1 and {len(subject_list)}')
                att += 1
        except:
            print('Enter a valid integer')
            att +=1
        if att >= 3:
            Abort()
            return
        i += 1

#%% Topic Details
    i = 0
    att = 0
    # att1 = 0
    while i < 3:
        try:
            topic = input(f"{add_menu[3]}: ").lstrip()
            if topic == '':
                print('Topic field cannot be empty')
                att += 1
            else:
                topcon = input(f"Confirm topic is \'{topic}\' (yes/no) ")
                if topcon == 'yes' or topcon == '':
                    print('Topic saved.\n')
                    break
                else:
                    raise Exception
        except:
            att += 1
        i += 1
        if att >= 3:
            Abort()
            return
#%% Module Details
    i = 0
    att = 0
    # 3 attempts to get module details
    while i < 3:
        try:
            module = int(input(f"{add_menu[4]}: ").strip())
            modcon = input(f"Confirm module is {module} (yes/no) ")
            if modcon == 'yes' or modcon == '':
                print('Module saved.\n')
                break
            else:
                att += 1
        except:
            print('Enter a valid integer')
            att += 1
        i += 1
        if att >= 3:
            Abort()

#%% Details Details
    details = input(f"{add_menu[5]}: ").lstrip()
    print('Details saved.\n')
#%% Calculate future dates
    date1 = (datetime.datetime.strptime(date, '%d/%m/%y') + timedelta(days = INT1)).strftime('%d/%m/%y')
    date2 = (datetime.datetime.strptime(date, '%d/%m/%y') + timedelta(days = INT2)).strftime('%d/%m/%y')
    date3 = (datetime.datetime.strptime(date, '%d/%m/%y') + timedelta(days = INT3)).strftime('%d/%m/%y')
    # print(date1, date2, date3)
#%% Confirm and add to database
    datcon = input("Add data to database? (yes/no) ")
    if datcon != '' and datcon != 'yes':
        print('Data will not be added to database.\n')
        input("\nPress Enter to return to Main Menu...")
        return False
    dbtablename = subject
    while True:
        try:
            print('Saving data...', end = '')
            db.execute(f"INSERT INTO {dbtablename} (Date, Topic, Module, Details, Date1, Status1, Date2, Status2, Date3, Status3) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (date, topic, module, details, date1, 0, date2, 0, date3, 0))
            DBH.commit()
            print('data saved!')
            break
        except:
            print('failed to save data')
            trycon = input("Try again? (yes/no) ")
            if trycon != '' and trycon != 'yes':
                print('DATA NOT SAVED\n')
                break
    input("\nPress Enter to return to Main Menu...")

def View_Data():
    global INT1, INT2, INT3
    global Date3Rev, Date2Rev, Date1Rev, Overdue1Rev, Overdue2Rev, Overdue3Rev, Revcomp, tablenames, DateORev
    Date3Rev, Date2Rev, Date1Rev, Overdue1Rev, Overdue2Rev, Overdue3Rev, Revcomp, DateORev = [], [], [], [], [], [], [], []
    OTHERDAYSDATA = 0
    Intro()
    i = 0
    att = 0
    dateo = today.strftime('%d/%m/%y')
    # 3 attempts to receive date input
    while i < 3:
        date = input("\n\nEnter date to view data: DD/MM/YY (Today)? ")
        if date == '':
            date = dateo
            print("Viewing today's data...\n")
            View_Today_Data()
            break
        elif list(date).count('/') == 2:
            # print('x')
            try:
                bool(datetime.datetime.strptime(date, '%d/%m/%y'))
                # print(datetime.datetime.strptime(date, '%d/%m/%y'), datetime.datetime.strptime(dateo, '%d/%m/%y'))
                if datetime.datetime.strptime(date, '%d/%m/%y') > datetime.datetime.strptime(dateo, '%d/%m/%y'):
                    print("Cannot check for future dates!")
                    att += 1
                    continue
                # WILL NOT WORK BECAUSE STATUSES ARE DEFINED ALREADY
                # print('1')
                View_OtherDays_Data(date)
                print(f'Viewing data for {date}:\n')
                OTHERDAYSDATA = 1
                # print('code incomplete...viewing today\'s data instead...')
                break
            except:
                print('Invalid date')
                att += 1
        else:
            print("Enter valid dates.")
            att += 1
        i += 1
        if att >= 3:
            Abort()
            return

    # print('\n\n')
    # print(Date1Rev, Overdue1Rev)
    # print('\n\n')
    # print(Date2Rev, Overdue2Rev)
    # print('\n\n')
    # print(Date3Rev, Overdue3Rev)
    # print('\n\n')

    # Presenting Data
    if len(Date3Rev) != 0 or len(Date2Rev) != 0 or len(Date1Rev) != 0 or len(Overdue1Rev) != 0 or len(Overdue2Rev) != 0 or len(Overdue3Rev) != 0 or len(DateORev) != 0:
        print('\t{<Subject>(<Module>): <Topic> [<Details>]}\n')
    i = 0
    # INT3
    if len(Date3Rev) != 0:
        print(f'Content from {Date3Rev[0][1]} [{INT3} days ago]:\n')
        for content in Date3Rev:
            i += 1
            Revcomp.append(content)
            print(f"\t{i}) {content[0][2:]}({content[3]}): {content[2]}", end = "")
            if content[4] != '':
                print(f" [{content[4]}]")
            else:
                print('')
        print('')        
    
    # INT2
    if len(Date2Rev) != 0:
        print(f'Content from {Date2Rev[0][1]} [{INT2} days ago]:\n')
        for content in Date2Rev:
            i += 1
            Revcomp.append(content)
            print(f"\t{i}) {content[0][2:]}({content[3]}): {content[2]}", end = "")
            if content[4] != '':
                print(f" [{content[4]}]")
            else:
                print('')
        print('')
    
    # INT1
    if len(Date1Rev) != 0:
        daysago = INT1
        if daysago == 1:
            daysago = 'Yesterday'
        print(f'Content from {Date1Rev[0][1]} [{daysago}]:\n')
        for content in Date1Rev:
            i += 1
            Revcomp.append(content)
            print(f"\t{i}) {content[0][2:]}({content[3]}): {content[2]}", end = "")
            if content[4] != '':
                print(f" [{content[4]}]")
            else:
                print('')
        print('')
    
    # Other Days Data
    if len(DateORev) != 0:
        for content in DateORev:
            i += 1
            Revcomp.append(content)
            print(f"\t{i}) {content[0][2:]}({content[3]}): {content[2]}", end = "")
            if content[4] != '':
                print(f" [{content[4]}]")
            else:
                print('')
        print('')

    #%% Overdue revisions
    OVERDUEREV = 0
    if len(Overdue1Rev) != 0 or len(Overdue2Rev) != 0 or len(Overdue3Rev) != 0:
        OVERDUEREV = 1
        print('You have overdue revisions.\n')
    if OVERDUEREV == 1:
        comboverdue = Overdue3Rev + Overdue2Rev + Overdue1Rev
        for content in comboverdue:
            i += 1
            Revcomp.append(content)
            # print(content)
            print(f"\t{i}) {content[0][2:]}({content[3]}): {content[2]}", end = "")
            if content[4] != '':
                print(f" [{content[4]}]", end = '')
            if content in Overdue3Rev:
                print(f" <due on {content[7]}>")
                continue
            if content in Overdue2Rev:
                print(f" <due on {content[6]}>")
                continue
            if content in Overdue1Rev:
                print(f" <due on {content[5]}>")
                continue
            print('>')
        
    #%% Logging data
    i = 0
    att = 0
    # print(len(DateORev))
    if len(Date1Rev) != 0 or len(Date2Rev) != 0 or len(Date3Rev) != 0 or OVERDUEREV != 0 or len(DateORev) != 0: 
        print('')
        while i < 3:
            try:
                RevcompInd = input("Enter index of content to mark as revised: ").strip()
                if RevcompInd == '':
                    print('No data will be marked as revised.')
                    break
                elif int(RevcompInd) > 0 and int(RevcompInd) <= len(Revcomp):
                    rvcmpchk = Revcomp[int(RevcompInd) - 1]
                    revcon = input(f"Confirm completing {rvcmpchk[0][2:]}: {rvcmpchk[2]} (yes/no) ")
                    if revcon != 'yes' and revcon != '':
                        print("Data will not be logged.")
                        input("\nPress Enter to return to Main Menu...")
                        i += 1
                        att += 1
                        if att >= 3:
                            Abort()
                            return
                        continue
                    # print(rvcmpchk[:5])
                    # print(Date1Rev)
                    if rvcmpchk[:5] in Date1Rev:
                        # print('date1rev')
                        db.execute(f"UPDATE {rvcmpchk[0]} SET Status1 = 1 WHERE Date = \'{rvcmpchk[1]}\' AND Topic = \'{rvcmpchk[2]}\' AND Module = {rvcmpchk[3]}")
                    if rvcmpchk[:5] in Date2Rev:
                        # print('date2rev')
                        db.execute(f"UPDATE {rvcmpchk[0]} SET Status2 = 1 WHERE Date = \'{rvcmpchk[1]}\' AND Topic = \'{rvcmpchk[2]}\' AND Module = {rvcmpchk[3]}")
                    if rvcmpchk[:5] in Date3Rev:
                        # print('date3rev')
                        db.execute(f"UPDATE {rvcmpchk[0]} SET Status3 = 1 WHERE Date = \'{rvcmpchk[1]}\' AND Topic = \'{rvcmpchk[2]}\' AND Module = {rvcmpchk[3]}")
                    # print('asdfgh')
                    if OTHERDAYSDATA == 1:
                        # print('otd')
                        for abc in range(3):
                            abc += 1
                            db.execute(f"UPDATE {rvcmpchk[0]} SET Status{abc} = 1 WHERE Date = \'{rvcmpchk[1]}\' AND Date{abc} = \'{date}\' AND Topic = \'{rvcmpchk[2]}\' AND Module = {rvcmpchk[3]}")
                    # overdue completion
                    # print('asd')
                    if OVERDUEREV == 1:
                        # print(rvcmpchk)
                        # print('1')
                        # print(Overdue1Rev)
                        # print('2')
                        # print(Overdue2Rev)
                        # print('3')
                        # print(Overdue3Rev)
                        if rvcmpchk in Overdue3Rev:
                            # print('Overdue3Rev')
                            db.execute(f"UPDATE {rvcmpchk[0]} SET Status3 = 1 WHERE Date = \'{rvcmpchk[1]}\' AND Topic = \'{rvcmpchk[2]}\' AND Module = {rvcmpchk[3]}")
                        if rvcmpchk in Overdue2Rev:
                            # print('Overdue2Rev')
                            db.execute(f"UPDATE {rvcmpchk[0]} SET Status2 = 1 WHERE Date = \'{rvcmpchk[1]}\' AND Topic = \'{rvcmpchk[2]}\' AND Module = {rvcmpchk[3]}")
                        if rvcmpchk in Overdue1Rev:
                            # print('Overdue1Rev')
                            db.execute(f"UPDATE {rvcmpchk[0]} SET Status1 = 1 WHERE Date = \'{rvcmpchk[1]}\' AND Topic = \'{rvcmpchk[2]}\' AND Module = {rvcmpchk[3]}")
                        # print('this ran')
                    DBH.commit()
                    print('Data logged.')
                    break
                else:
                    print(f"Enter valid integer between 1 and {len(Revcomp)}")
                    att +=1
            except:
                print('Enter integers only')
                att += 1
            if att >= 3:
                Abort()
                return
            i += 1
    else:
        poslen = 0
        for teams in tablenames:
            ind = 1
            while ind <= 3:
                tem = db.execute(f"SELECT Status1, Status2, Status3 FROM {teams} WHERE Date{ind} = \'{date}\'")
                for i in tem:
                    poslen += 1
                ind += 1
        # print(poslen)
        if poslen != 0:
            print("All revisions completed!")
        else:
            print("No record found!")
    input("\nPress Enter to return to main menu...")
#%% End of View Data submenu


# Program runs here
while True:
    index = Main_Menu()
    if index == 1:
        Add_Data()
        # Update_Data()
    elif index == 2:
        View_Data()
    elif index == len(main_menu):
        Intro()
        print('\n\nProgram closed\n\n')
        print('*' * terlen)
        print('\n')
        break
    else:
        Intro()
        print('\nUnder Construction!')
        input("\nPress Enter to return to main menu...")    
DBH.commit()
