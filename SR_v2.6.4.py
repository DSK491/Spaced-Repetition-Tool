"""
SPACED REPETITION TOOL.

CHANGELOG:
REFER v2.6.x FOR PREVIOUS CHANGES
1. Fixed Bug with View Data.
2. Increased length of notes preview in Misc>View Notes.
3. Returning from sub-sub menu now returns at sub-menu instead of Main Menu.

1. Semester is no longer prompted in Add Menu
2. Semester can be updated in Modify Menu>Update Semester

POSSIBLE ISSUES:

Dhruva Kashyap
17 Mar 2023
"""

import os
os.system('clear')
print("\nLaunching program...\n")

import datetime
from datetime import timedelta
import sys
import sqlite3
import traceback

# Add your directory path here
# print(len(sys.argv))
if len(sys.argv) == 2:
    if sys.argv[1] == 'DEV':
        #  use this directory for testing and development
        DBDIR = ''
        DBDIR = '/Users/dhruvakashyap/Documents/PythonScripts/Spaced Repetition/'
        DBNAM = 'Repetition Database TESTING.sqlite'
        print("USING TESTING DATABASE")
        DEVMODE = 1
else:
    # use this directory for actual usage
    DBDIR = ''
    DBDIR = '/Users/dhruvakashyap/Library/Mobile Documents/com~apple~CloudDocs/Documents/'
    DBNAM = 'Spaced Repetition Database.sqlite'
    DEVMODE = 0
DBCON = DBDIR + DBNAM
# print(DBCON)

INT1, INT2, INT3 = 1, 3, 15
today = datetime.date.today()
# DBH = sqlite3.connect(f"{DBCON}")
DBH = sqlite3.connect(f"{DBCON}")
db = DBH.cursor()
# sys.exit()

# creating and initialising table Info and .Notes (first time)
db.execute('CREATE TABLE IF NOT EXISTS "Info" ("Key" TEXT, "Value" TEXT)')
db.execute('CREATE TABLE IF NOT EXISTS ".Notes" ("Note" TEXT)')
chkn = db.execute("SELECT * FROM '.Notes'")
cntn = len(db.fetchall())
# print(cntn)
# Inserts sample note into .Notes
if cntn == 0:
    db.execute("INSERT INTO '.Notes' (Note) VALUES "
               "('These are notes. You can save any text here for future"
               " reference. Please replace this note with something useful.')")

chk = db.execute("SELECT * FROM 'Info'")
cnt = len(db.fetchall())
# print(cnt)
if cnt == 0:
    db.execute("INSERT INTO Info (Key, Value) VALUES ('Semester', '0')")
    db.execute("INSERT INTO Info (Key, Value) VALUES ('Last Updated', Null)")
    db.execute("INSERT INTO Info (Key, Value) VALUES ('TMSTRT', NULL)")
    db.execute("INSERT INTO Info (Key, Value) VALUES ('TMEND', NULL)")
    db.execute("INSERT INTO Info (Key, Value) VALUES ('INT1', '1')")
    db.execute("INSERT INTO Info (Key, Value) VALUES ('INT2', '3')")
    db.execute("INSERT INTO Info (Key, Value) VALUES ('INT3', '15')")
DBH.commit()
# Setting update intervals to dates saved in database
I1 = DBH.execute("SELECT Value FROM 'Info' WHERE Key = 'INT1'")
I2 = DBH.execute("SELECT Value FROM 'Info' WHERE Key = 'INT2'")
I3 = DBH.execute("SELECT Value FROM 'Info' WHERE Key = 'INT3'")
for x in I1:
    I1 = x[0]
for x in I2:
    I2 = x[0]
for x in I3:
    I3 = x[0]
if I1 != '' and I2 != '' and I3 != '':
    if all([I1.isdigit(), I2.isdigit(), I3.isdigit()]):
        if int(I3) > int(I2) > int(I1):
            INT1, INT2, INT3 = int(I1), int(I2), int(I3)

# test mode variable
TMACTIVE = 0

main_menu = ['Add Data',
             'View/Log Data',
             'Modify Data',
             'Misc',
             'Quit']

add_menu = ['Date',
            'Semester',
            'Course',
            'Topic',
            'Module',
            'Details']

modify_menu = ['Test Mode',
               'Update Statuses',
               'Update Semester',
               'Return to Main Menu']

misc_menu = ['Notes',
             'Modify Revision Reminder Intervals',
             'Return to Main Menu']

notes_menu = ['Create new note',
              'View notes',
              'Delete note',
              'Return to Misc Menu']

path = []

# Adds subject names to a list
Tablenamecur = db.execute("SELECT name from sqlite_schema")
tablenames = []
for val in Tablenamecur:
    if 'S' in val[0]:
        tablenames.append(val[0])


# %%
def Abort():
    print('\nToo many attempts')
    input("Press Enter to return to Main Menu...")


# %% Center aligns text passed as argument
terlen, terhei = 0, 0


def Print_Center(text):
    global terlen, terhei
    terlen = os.get_terminal_size()[0]
    terhei = os.get_terminal_size()[1]
    # terlen = 80
    print(text.center(terlen))


# %% Introduction
def Intro():
    global path
    os.system('clear')
    Print_Center('Spaced Repetition Tool')
    # print(path)
    for i in path:
        print(i, end='')
    print('')


# %% Closing page
def Outro():
    global terlen, terhei
    os.system('clear')
    Print_Center('Spaced Repetition Tool')
    print('')
    Print_Center('Dhruva Kashyap')
    print('\n'*int(terhei/3))
    Print_Center("~~PROGRAM CLOSED~~")
    print('\n'*int(terhei/4))
    print('=*'*(int(terlen/2)))


# %% Creates new table with argument passed as table name
def New_Table(sem, title):
    db.execute(f"CREATE TABLE IF NOT EXISTS \"S{sem + title}\" "
               "(Date TEXT, Topic TEXT, Module INTEGER, Details TEXT, "
               "Date1 TEXT, Status1 INTEGER, Date2 TEXT, Status2 INTEGER, "
               "Date3 TEXT, Status3 INTEGER)")
    dbcmd = "MPreS" + sem + title
    db.execute("INSERT INTO Info (Key, Value) VALUES (?, ?)", (dbcmd, '1'))


# %%
def Update_Data():
    print("Updating Statuses...", end="")
    pars, updt = 0, 0
    presdate = today.strftime('%d/%m/%y')
    global tablenames
    for table in tablenames:
        # print("\n")
        # print(table)
        num = 1
        while num <= 3:
            # print(f"{num}", end = " ")
            # Setting status for reminders 'due today'
            db.execute(f"UPDATE \"{table}\" SET Status{num} = -1 "
                       f"WHERE (Date{num} = \"{presdate}\" "
                       f"AND Status{num} NOT IN (1, -1))")

            updt += db.rowcount
            # print(db.rowcount)
            Datecur = DBH.execute(f"SELECT Date{num} FROM \"{table}\"")
            # pars += db.rowcount
            # print(db.rowcount)
            for posdate in Datecur:
                pars += 1
                # print(posdate, end = ' ')
                POSDATE = datetime.datetime.strptime(posdate[0], '%d/%m/%y')
                PRESDATE = datetime.datetime.strptime(presdate, '%d/%m/%y')
                # Overdue case
                if POSDATE < PRESDATE:
                    # Setting status for reminders 'overdue'
                    db.execute(f"UPDATE \"{table}\" SET Status{num} = -2 "
                               f"WHERE (Date{num} = \"{posdate[0]}\" "
                               f"AND Status{num} NOT IN (1, -2, -3))")
                    updt += db.rowcount
                    # print(f"past: {db.rowcount}")
                    if POSDATE + datetime.timedelta(days=7) < PRESDATE:
                        # print('very overdue')
                        # Setting status for reminders 'overdue - won't remind'
                        db.execute(f"UPDATE \"{table}\" SET Status{num} = -3 "
                                   f"WHERE Date{num} = \"{posdate[0]}\" "
                                   f"AND (Status{num} NOT IN (1, -2, -3))")
                        updt += db.rowcount
                        # print(f"overdue: {db.rowcount}")
                        # print(POSDATE, PRESDATE)
                    # print('overdue')
                # Future case
                if POSDATE > PRESDATE:
                    # Setting status for reminders 'future'
                    db.execute(f"UPDATE \"{table}\" SET Status{num} = 0 "
                               f"WHERE Date{num} = \"{posdate[0]}\" "
                               f"AND (Status{num} NOT IN (-1, 0))")
                    updt += db.rowcount
                    # print(f"future: {db.rowcount}")
                    # print('not yet due')
            num += 1
    DBH.commit()
    print('statuses updated.')
    plupar, pluupdt = '', ''
    if pars != 1:
        plupar = 's'
    if updt != 1:
        pluupdt = 's'
    print(f"\n{pars} cell{plupar} parsed.\n{updt} cell{pluupdt} updated.")


# %%
def Main_Menu():
    global main_menu
    global path
    global today
    global TMACTIVE
    today = datetime.date.today()
    path = []
    i = 0
    index = -1
    # if last updated date is not today run Update_Data()
    # and update last updated date
    LASTUPCUR = db.execute("SELECT Value FROM 'Info' "
                           "WHERE Key = 'Last Updated'")
    for x in LASTUPCUR:
        LUpdated = x[0]
    if LUpdated is not None:
        cnd1 = str(datetime.datetime.strptime(LUpdated, "%d/%m/%y")).split()[0]
        cnd2 = str(datetime.date.today())
        if cnd1 != cnd2:
            Update_Data()
    try:
        TDY = today.strftime('%d/%m/%y')
        # print(TDY)
        db.execute(f"Update 'Info' SET Value = \"{TDY}\" "
                   "WHERE Key = 'Last Updated'")
        DBH.commit()
    except Exception:
        while True:
            try:
                db.execute(f"Update 'Info' SET Value = \"{TDY}\" "
                           "WHERE Key = 'Last Updated'")
                DBH.commit()
                break
            except Exception:
                print('\nDatabase is locked')
                trycon = input("Try again? (yes/no) ")
                # if trycon != '' and trycon != 'yes':
                if trycon not in ('', 'yes'):
                    print('\nClosing program...')
                    Outro()
                    sys.exit(1)

    Intro()
    if DEVMODE == 1:
        print('DEVELOPMENT MODE\n')
    # checking for active test mode
    TMSTRTy, TMENDy = [], []
    TMSTRTx = db.execute("SELECT Value FROM 'Info' WHERE Key = 'TMSTRT'")
    for x in TMSTRTx:
        TMSTRTy.append(x)
    TMENDx = db.execute("SELECT Value FROM 'Info' WHERE Key = 'TMEND'")
    for x in TMENDx:
        TMENDy.append(x)
    # print(TMSTRTy[0][0])
    if TMSTRTy[0][0] is not None or TMENDy[0][0] is not None:
        TMSTRT = datetime.datetime.strptime(TMSTRTy[0][0], '%d/%m/%y')
        TMEND = datetime.datetime.strptime(TMENDy[0][0], '%d/%m/%y')
        TODAY = datetime.datetime.today()
        if TODAY > TMSTRT and TODAY < TMEND:
            print('TEST MODE ACTIVE\n')
            TMACTIVE = 1
        else:
            TMACTIVE = 0

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
        except Exception:
            print('Enter Integers Only')
        i += 1

    print('\nProgram Aborted: Too Many Attempts!\n\n')
    Outro()
    sys.exit(0)


# %%
Date3Rev, Date2Rev, Date1Rev = [], [], []
Overdue1Rev, Overdue2Rev, Overdue3Rev = [], [], []
Revcomp, DateORev = [], []


def View_Today_Data():
    global Date3Rev, Date2Rev, Date1Rev
    global Overdue1Rev, Overdue2Rev, Overdue3Rev, Revcomp, tablenames
    # Save due revision dates and info as lists in lists
    # DATE1
    for teams in tablenames:
        STem = DBH.execute("SELECT Date, Topic, Module, Details "
                           f"FROM \"{teams}\" WHERE Status1 = -1")
        for due in STem:
            tem = []
            tem.append(teams)
            for item in due:
                tem.append(item)
            Date1Rev.append(tem)
        # checks for overdue
        OTem = DBH.execute("SELECT Date, Topic, Module, Details, "
                           "Date1, Date2, Date3 "
                           f"FROM \"{teams}\" WHERE Status1 = -2")
        for due in OTem:
            tem = []
            tem.append(teams)
            for item in due:
                tem.append(item)
            Overdue1Rev.append(tem)
    # DATE2
    for teams in tablenames:
        STem = DBH.execute("SELECT Date, Topic, Module, Details "
                           f"FROM \"{teams}\" WHERE Status2 = -1")
        for due in STem:
            tem = []
            tem.append(teams)
            # print(tem)
            # print('...')
            for item in due:
                tem.append(item)
            Date2Rev.append(tem)
        # checks for overdue
        OTem = DBH.execute("SELECT Date, Topic, Module, Details, "
                           "Date1, Date2, Date3 "
                           f"FROM \"{teams}\" WHERE Status2 = -2")
        for due in OTem:
            tem = []
            tem.append(teams)
            for item in due:
                tem.append(item)
            Overdue2Rev.append(tem)

    # DATE3
    for teams in tablenames:
        STem = DBH.execute("SELECT Date, Topic, Module, Details "
                           f"FROM \"{teams}\" WHERE Status3 = -1")
        for due in STem:
            tem = []
            tem.append(teams)
            # print(tem)
            # print('...')
            for item in due:
                tem.append(item)
            Date3Rev.append(tem)
        # checks for overdue
        OTem = DBH.execute("SELECT Date, Topic, Module, Details, "
                           "Date1, Date2, Date3 "
                           f"FROM \"{teams}\" WHERE Status3 = -2")
        for due in OTem:
            tem = []
            tem.append(teams)
            for item in due:
                tem.append(item)
            Overdue3Rev.append(tem)


# %%
def View_OtherDays_Data(date_inp):
    # print('a')
    global Date3Rev, Date2Rev, Date1Rev
    global Overdue1Rev, Overdue2Rev, Overdue3Rev, Revcomp, tablenames, DateORev
    # DATE1
    # print('b')
    for teams in tablenames:
        # print('c')
        for xyz in range(3):
            xyz += 1
            # print('d')
            STem = DBH.execute("SELECT Date, Topic, Module, Details "
                               f"FROM \"{teams}\" "
                               f"WHERE Date{xyz} = \"{date_inp}\" "
                               f"AND (Status{xyz} = -1 OR Status{xyz} = -2)")
            for due in STem:
                tem = []
                tem.append(teams)
                for item in due:
                    tem.append(item)
                DateORev.append(tem)


# %%
def Test_Mode():
    global tablenames
    global path
    Intro()
    # %% accepting start date
    i = 0
    att = 0
    print("\nTest Mode postpones all revision reminders during test days.")
    print("\nIMPORTANT: THIS CANNOT BE UNDONE. "
          "PLEASE SAVE A BACKUP OF DATABASE BEFORE PROCEEDING.")
    if input("\nProceed? (yes/no) ") != 'yes':
        print("Test mode will not be enabled.")
        input("\nPress Enter to return to Main Menu...")
        return
    while i < 3:
        try:
            inpdate = input("\nStart date: DD/MM/YY ").strip()
            # bool(datetime.datetime.strptime(inpdate, '%d/%m/%y'))
            if inpdate == '':
                print('Start date field cannot be empty')
                att += 1
            elif list(inpdate).count('/') == 2:
                try:
                    bool(datetime.datetime.strptime(inpdate, '%d/%m/%y'))
                    startdate = inpdate
                    print(f'Start date saved as {startdate}\n')
                    break
                except Exception:
                    print('Invalid date')
                    att += 1
            else:
                raise Exception
        except Exception:
            print('Error.')
            att += 1
        i += 1
        if att >= 3:
            Abort()
            return
    # converts str to dimedelta object
    STARTDATE = datetime.datetime.strptime(startdate, '%d/%m/%y')

    # %% accepting end date
    i = 0
    att = 0
    while i < 3:
        try:
            inpdate = input("End date: DD/MM/YY ").strip()
            # bool(datetime.datetime.strptime(inpdate, '%d/%m/%y'))
            if inpdate == '':
                print('End date field cannot be empty')
                att += 1
            elif list(inpdate).count('/') == 2:
                try:
                    bool(datetime.datetime.strptime(inpdate, '%d/%m/%y'))
                    enddate = inpdate
                    print(f'End date saved as {enddate}\n')
                    break
                except Exception:
                    print('Invalid date')
                    att += 1
            else:
                raise Exception
        except Exception:
            print('Error.')
            att += 1
        i += 1
        if att >= 3:
            Abort()
            return
    ENDDATE = datetime.datetime.strptime(enddate, '%d/%m/%y')

    # %%
    if STARTDATE >= ENDDATE:
        print('Cannot begin Test Mode: Start date must precede End date.')
        input("\nPress enter to return to previous menu...")
        return
    tescon = input("Confirm Test Mode "
                   f"from {startdate} to {enddate} (yes/no) ").strip()
    if tescon != 'yes':
        print("Test mode will not be enabled. \n")
        input("Press Enter to return to previous menu...")
        return

    db.execute(f"UPDATE Info SET VALUE = \"{startdate}\" "
               "WHERE Key = 'TMSTRT'")
    db.execute(f"UPDATE Info SET VALUE = \"{enddate}\" "
               "WHERE Key = 'TMEND'")

    TIMEDEL = ENDDATE - STARTDATE
    # print(TIMEDEL)

    print("Saving data...", end="")

    for table in tablenames:
        num = 1
        while num <= 3:
            Datecur = DBH.execute(f"SELECT Date{num} FROM \"{table}\"")
            for posdate in Datecur:
                POSDATE = datetime.datetime.strptime(posdate[0], '%d/%m/%y')
                NEWDATE = POSDATE + TIMEDEL
                if POSDATE >= STARTDATE:
                    newdate = datetime.datetime.strftime(NEWDATE, '%d/%m/%y')
                    db.execute(f"UPDATE \"{table}\" SET Date{num} = \"{newdate}\" "
                               f"WHERE Date{num} = \"{posdate[0]}\" "
                               f"AND Status{num} != 1")

                # print(posdate, end = " ")
                # print(newdate)
            num += 1
    while True:
        try:
            # print("Saving data...", end="")
            DBH.commit()
            print("data saved!")
            break
        except Exception:
            print('failed to save data')
            trycon = input("Try again? (yes/no) ")
            # if trycon != '' and trycon != 'yes':
            if trycon not in ('', 'yes'):
                print('DATA NOT SAVED\n')
                break
    input("\nPress Enter to return to previous menu...")


# %%
def Modify_Intervals():
    Intro()
    print("\nDefault Revision Reminders Interval is "
          "1 Day, 3 Days and 15 Days.")
    curlis = []
    plulis = []
    i = 1
    while i <= 3:
        tem = db.execute(f"SELECT Value from Info "
                         f"WHERE Key = \"INT{i}\"")
        for x in tem:
            curlis.append(int(x[0]))
            if int(x[0]) == 1:
                plulis.append('')
            else:
                plulis.append('s')
        i += 1

    print("Current Revision Reminders Interval is "
          f"{curlis[0]} Day{plulis[0]}, {curlis[1]} Day{plulis[1]} "
          f"and {curlis[2]} Day{plulis[2]}.")

    print("\nINFO: New reminder intervals will not affect previous reminders. "
          "Effect will take place from next reminder.")

    intcon = input("\nConfirm modifying reminder interval (yes/no) ")
    if intcon != 'yes':
        print('\nReminder Intervals will not be changed.')
        input("\nPress Enter to return to previous menu...")
        return

    intlis = []
    print('')
    nums = ['first', 'second', 'third']
    for rem in range(3):
        i = 0
        att = 0
        while i < 3:
            print(f"Enter {nums[rem]} reminder interval (days) ", end="")
            posrem = input("").strip()
            if posrem == '':
                print("\nEnter an integer")
                att += 1
            elif posrem != '' and posrem.isdigit():
                intlis.append(int(posrem))
                break
            else:
                print('\nEnter integers only')
                att += 1
            if att >= 3:
                Abort()
                return
            i += 1
    # accepted and stored intervals in a list
    # list needs to be checked for validity (int3 > int2 > int1)
    if intlis[2] > intlis[1] > intlis[0]:
        remcon = input("\nUpdate reminder intervals? (yes/no) ")
        if remcon != 'yes':
            print('Data will not be updated.\n')
            input("\nPress Enter to return to previous menu...")
            return
        while True:
            print('\nUpdating data...', end="")
            i = 1
            try:
                while i <= 3:
                    db.execute(f"UPDATE Info SET Value = \"{intlis[i-1]}\" "
                               f"WHERE Key = \"INT{i}\"")
                    i += 1
                DBH.commit()
                print('data updated')
                input("Press Enter to return to previous menu...")
                break
            except Exception:
                print('failed to save data')
                trycon = input("Try again? (yes/no) ")
                # if trycon != '' and trycon != 'yes':
                if trycon not in ('', 'yes'):
                    print('DATA NOT SAVED\n')
                    break
            input("Press Enter to return to previous menu...")
    else:
        print("\nError: Third interval must be greatest "
              "and first interval smallest.")

        input("Press Enter to return to previous menu...")

#%%
def Update_sem():
    Intro()
    cursem = db.execute("SELECT Value from Info "
                     "WHERE Key = 'Semester' LIMIT 1").fetchall()[0][0]
    
    print(f"\n\nCurrent semester is {cursem}")
    #newsem = input("\nEnter new semester: ")
    i = 0
    att = 0
    while i < 3:
        try:
            newsem = input("\nEnter new semester: ").strip()
            # print(f"semester = \"{semester}\" \nsem = {sem}")
            if newsem == '' or newsem == '0':
                print('Enter a valid integer.\n')
                att += 1
                if att >= 3:
                    Abort()
                    return
                continue
            semcon = input(f"\nConfirm new semester is {newsem} (yes/no) ").strip()
            if semcon != 'yes':
                print("\nSemester will not be updated.\n")
                input("\nPress Enter to return to previous menu...")
                return
            try:
                db.execute(f"UPDATE Info SET Value = {newsem} WHERE Key = 'Semester'")
                DBH.commit()
                print("\nSemester has been updated!")
            except:
                print("Unable to save data!\n")
            input("\nPress Enter to return to previous menu...")
            return
            
        except Exception:
            print('Enter a valid integer')
            att += 1
        i += 1
        if att >= 3:
            Abort()
            return


# %%
def Notes():
    global notes_menu, path
    i = 0
    index = -1
    att = 0
    Intro()
    print('\nPerform action:')
    for item in range(len(notes_menu)):
        print(f"{item+1}) {notes_menu[item]}")

    # 3 Attempts to get input
    while i < 3:
        try:
            index = input("\nIndex of submenu: ").strip()
            if index == '':
                print(f'Enter an index between 1 and {len(notes_menu)}')
                att += 1
            elif int(index) < len(notes_menu) + 1 and int(index) > 0:
                path.append(notes_menu[int(index) - 1] + ' > ')
                index = int(index)
                break
            else:
                print(f'Enter valid index between 1 and {len(notes_menu)}')
                att += 1
        except Exception:
            print('Enter Integers Only')
            att += 1
        if att >= 3:
            Abort()
            return
        i += 1
    # print(index)
    if index == len(notes_menu):
        Intro()
        print("\nReturning to Misc Menu...")
        path.pop()
        return
    if index == 1:
        New_notes()
    elif index == 2:
        View_notes()
    elif index == 3:
        Delete_notes()
    else:
        print('Error!')
    path.pop()
    Notes()


# %%
def New_notes():
    Intro()
    # maxindcur = DBH.execute("SELECT max(\"Index\") FROM '.Notes'")
    # for x in maxindcur:
    #     maxind = int(x[0])
    #     break
    # print(maxind)
    # newind = maxind + 1
    i = 0
    att = 0
    while i < 3:
        try:
            NewNote = input("\nType new note: \n").lstrip()
            if NewNote == '':
                print('Note cannot be blank')
                att += 1
            else:
                notcon = input("\nSave note? (yes/no) ")
                # if notcon == 'yes' or notcon == '':
                if notcon in ('yes', ''):
                    # print('Saving note...', end="")
                    break
                print('Note will not be saved.')
                return
        except Exception:
            att += 1
        i += 1
        if att >= 3:
            Abort()
            return
    while True:
        db.execute("INSERT INTO '.Notes' (\"Note\") VALUES (?)", (NewNote, ))
        try:
            DBH.commit()
            print("Note saved.")
            break
        except Exception:
            print('Failed to save note.')
            trycon = input("Try again? (yes/no) ")
            # if trycon != '' and trycon != 'yes':
            if trycon not in ('', 'yes'):
                print('\nNOTE NOT SAVED')
                break

    input("\nPress Enter to return to previous menu...")


# %%
def Delete_notes():
    Intro()
    notescur = DBH.execute("SELECT Note FROM '.Notes'")
    notes = []
    for x in notescur:
        notes.append([None, x[0]])
    print("\nViewing all notes:\n")
    for x in range(len(notes)):
        notes[x][0] = x + 1
        index = x + 1
        content = "\"" + str(notes[x][1])
        if len(content) >= 30:
            content = content[:30] + "..."
        content += "\""
        print(f"{index}) {content}")
        x += 1
    print(f"{len(notes) + 1}) Return to Main Menu")
    print('')
    i = 0
    att = 0
    noteind = None
    while i < 3:
        try:
            if att >= 3:
                Abort()
                return
            noteind = int(input("Enter index of note to delete: ").strip())
            if noteind > len(notes) + 1:
                print(f"Enter an index between 1 and {len(notes) + 1}")
                att += 1
                continue
            break
        except Exception:
            print("Enter a valid integer")
        i += 1
    
    if noteind is None:
        input("Press Enter to return to previous menu...")
        return
    if noteind == len(notes) + 1:
        Intro()
        print("\nReturning to Notes Menu...")
        return
    delnot = notes[noteind - 1][1]
    delcon = input(f"\nConfirm deleting \"{delnot[:20]}...\"? (yes/no) ")
    if delcon == 'yes':
        while True:
            try:
                db.execute("DELETE FROM \".Notes\" "
                           "WHERE Note = (?)", (delnot, ))
                DBH.commit()
                print("\nNote deleted.")
                break
            except Exception:
                print("\nFailed to delete note.")
                trycon = input("Try again? (yes/no) ")
                # if trycon != '' and trycon != 'yes':
                if trycon not in ('', 'yes'):
                    print('\nNOTE HAS NOT BEEN DELETED.')
                    break
    else:
        print("Note will not be deleted.\n")
    
    input("\nPress Enter to return to previous menu...")


# %%
def View_notes():
    Intro()
    notescur = DBH.execute("SELECT Note FROM '.Notes'")
    notes = []
    for x in notescur:
        # print(x)
        # notes.append((x[0], x[1]))
        notes.append([None, x[0]])
    # notes.append((len(notes), 'Return to Main Menu'))
    # print(notes)
    print("\nViewing all notes:\n")
    for x in range(len(notes)):
        # print(x)
        notes[x][0] = x + 1
        index = x + 1
        content = "\"" + str(notes[x][1])
        if len(content) >= 60:
            content = content[:60] + "..."
        content += "\""
        print(f"{index}) {content}")
        x += 1
    print(f"{len(notes) + 1}) Return to Notes Menu")
    print('')
    i = 0
    att = 0
    noteind = None
    while i < 3:
        try: 
            noteind = int(input("Enter index of note to view more: ").strip())
            if noteind > len(notes) + 1:
                print(f"Enter an index between 1 and {len(notes) + 1}")
                att += 1
                continue
            break
        except Exception:
            print("Enter a valid integer")
        if att >= 3:
            input("Press Enter to return to previous menu...")
            return
        i += 1
    if noteind is None:
        Abort()
        return
    if noteind == len(notes) + 1:
        Intro()
        print("\nReturning to Notes Menu...")
        return

    for i in range(len(notes)):
        if noteind == notes[i][0]:
            print(f"\n\"{notes[i][1]}\"")

    input("\nPress Enter to return to previous menu...")


# %%
def Add_Data():
    Intro()
    global add_menu
    global date
    print('\n\nInput Data:\n')

# %% Date Details
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
            if list(date).count('/') == 2:
                try:
                    bool(datetime.datetime.strptime(date, '%d/%m/%y'))
                    print(f'Date saved as {date}.\n')
                    break
                except Exception:
                    print('Invalid date')
                    att += 1
            else:
                raise Exception
        except Exception:
            print(f'Error. Date will be saved as \"{date_t}\"')
            att += 1
        i += 1
        if att >= 3:
            Abort()
            return

# %% Semester Details
    '''i = 0
    att = 0
    sem = db.execute("SELECT Value from Info "
                     "WHERE Key = 'Semester' LIMIT 1").fetchall()[0][0]

    # 3 attempts to get input
    while i < 3:
        try:
            semester = input(f"{add_menu[1]}: ({sem})? ").strip()
            # print(f"semester = \"{semester}\" \nsem = {sem}")
            # for first time usage
            if semester == '' and sem == '0':
                print('Semester value cannot be 0!')
                att += 1
                if att >= 3:
                    Abort()
                    return
                continue

            # Subject details start
            subject_list = []
            sub_cur = db.execute('SELECT name FROM sqlite_schema')
            for val in sub_cur:
                if f'S{semester}' in val[0]:
                    subject_list.append(val[0])
            if len(subject_list) == 0:
                cont = input("Selected semester does not have any data. "
                             "Proceed? (yes/no) ").strip()

                # if cont == 'yes' or cont == '':
                if cont in ('', 'yes'):
                    if semester == '':
                        semester = sem
                    # semester = int(sem)
                    # print(semester, sem)
                    print(f'Semester saved as {semester}.\n')
                    break
                att += 1
            # Subject details end
            elif semester == '':
                semester = sem
                print(f"Semester saved as {sem}\n")
                break
            elif int(semester) > 0 and int(semester) < 9:
                print(f'Semester saved as {semester}.\n')
                break
            else:
                print('Enter valid semester between 1 and 8')
                att += 1
        except Exception:
            print('Enter a valid integer')
            att += 1
        i += 1
        if att >= 3:
            Abort()
            return
    db.execute(f"UPDATE Info SET Value = {semester} WHERE Key = 'Semester'")
    '''
    semester = db.execute("SELECT Value from Info "
                     "WHERE Key = 'Semester' LIMIT 1").fetchall()[0][0]
    subject_list = []
    sub_cur = db.execute('SELECT name FROM sqlite_schema')
    for val in sub_cur:
        if f'S{semester}' in val[0]:
            subject_list.append(val[0])
    print(f"Semester: {semester}\n")

# %% Subject Details
    i = 0
    j = 0
    att = 0
    att1 = 0
    # subject_list = list()
    # sub_cur = db.execute('SELECT name FROM sqlite_schema')
    # for val in sub_cur:
    #     if val[0].startswith(f'S{semester}'):
    #         subject_list.append(val[0])
    subject_list.append('  New Course')
    # print(subject_list)
    print(f"{add_menu[2]}:")
    for val in range(len(subject_list)):
        print(f"{val + 1}) {subject_list[val][2:]}")
    # 3 Attempts to get input
    while i < 3:
        try:
            sub_i = int(input('Index of course: '))
            if int(sub_i) > 0 and int(sub_i) < len(subject_list) + 1:
                if sub_i == len(subject_list):
                    # 3 attempts to get new subject title
                    while j < 3:
                        table_name = input('Enter name of new course: ')
                        if table_name == '':
                            print('Course name cannot be blank.')
                            att1 += 1
                            if att1 >= 3:
                                Abort()
                                return
                            continue
                        subcon = input("Confirm new course is "
                                       f"\"{table_name}\" (yes/no) ").strip()

                        # if subcon == 'yes' or subcon == '':
                        if subcon in ('', 'yes'):
                            # print('accepted...')
                            subject = 'S' + semester + table_name
                            New_Table(semester, table_name)
                            print(f'New course saved as {subject}\n')
                            break
                        att1 += 1
                        if att1 >= 3:
                            Abort()
                            return
                        j += 1
                    break
                else:
                    subject = subject_list[sub_i - 1]
                    print(f'Course saved as {subject[2:]}.\n')
                    break
            else:
                print("Enter index of course between "
                      f"1 and {len(subject_list)}")

                att += 1
        except Exception:
            print('Enter a valid integer')
            att += 1
        if att >= 3:
            Abort()
            return
        i += 1

# %% Module Details
    i = 0
    att = 0
    # 3 attempts to get module details
    while i < 3:
        try:
            moddef = 0
            modex = 'MPre' + subject
            MODCUR = DBH.execute("SELECT Value "
                                 "FROM 'Info' "
                                 f"WHERE Key = \"{modex}\"")
            for x in MODCUR:
                moddef = x[0]
                break
            if moddef != 0:
                module = input(f"{add_menu[4]}: ({moddef})? ").strip()
                if module in (''):
                    module = int(moddef)
                else:
                    module = int(module)
            else:
                module = int(input(f"{add_menu[4]}: ").strip())
            modcon = input(f"Confirm module is {module} (yes/no) ")
            if modcon in ('', 'yes'):
                print('Module saved.\n')
                break
            att += 1
        except Exception:
            print('Enter a valid integer')
            att += 1
        i += 1
        if att >= 3:
            Abort()
            return
    if moddef == 0:
        db.execute("INSERT INTO 'Info' "
                   "(Key, Value) "
                   "VALUES (?, ?)", 
                   (modex, module))
    else:
        db.execute("UPDATE 'Info' "
                   f"SET Value = \"{module}\" "
                   f"WHERE Key = \"{modex}\"")
    

# %% Topic Details
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
                topcon = input(f"Confirm topic is \"{topic}\" (yes/no) ")
                # if topcon == 'yes' or topcon == '':
                if topcon in ('', 'yes'):
                    print('Topic saved.\n')
                    break
                raise Exception
        except Exception:
            att += 1
        i += 1
        if att >= 3:
            Abort()
            return

# %% Details Details
    details = input(f"{add_menu[5]}: ").lstrip()
    print('Details saved.\n')

# %% Calculate future dates
    date1 = (datetime.datetime.strptime(date, '%d/%m/%y')
             + timedelta(days=INT1)).strftime('%d/%m/%y')

    date2 = (datetime.datetime.strptime(date, '%d/%m/%y')
             + timedelta(days=INT2)).strftime('%d/%m/%y')

    date3 = (datetime.datetime.strptime(date, '%d/%m/%y')
             + timedelta(days=INT3)).strftime('%d/%m/%y')

    # print(date1, date2, date3)

# %% Confirm and add to database
    datcon = input("Add data to database? (yes/no) ")
    # if datcon != '' and datcon != 'yes':
    if datcon not in ('', 'yes'):
        print('Data will not be added to database.\n')
        input("\nPress Enter to return to Main Menu...")
        return
    dbtablename = subject
    while True:
        try:
            print('Saving data...', end='')

            db.execute(f"INSERT INTO \"{dbtablename}\" "
                       "(Date, Topic, Module, Details, Date1, Status1, "
                       "Date2, Status2, Date3, Status3) "
                       "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (date, topic, module, details,
                        date1, 0, date2, 0, date3, 0))

            DBH.commit()
            print('data saved!')
            break
        except Exception:
            print('failed to save data')
            trycon = input("Try again? (yes/no) ")
            # if trycon != '' and trycon != 'yes':
            if trycon not in ('', 'yes'):
                print('DATA NOT SAVED\n')
                break
    input("\nPress Enter to return to Main Menu...")


# %%
def View_Data():
    global INT1, INT2, INT3, TMACTIVE
    global Date3Rev, Date2Rev, Date1Rev
    global Overdue1Rev, Overdue2Rev, Overdue3Rev, Revcomp, tablenames, DateORev

    Date3Rev, Date2Rev, Date1Rev = [], [], []
    Overdue1Rev, Overdue2Rev, Overdue3Rev = [], [], []
    Revcomp, DateORev = [], []

    OTHERDAYSDATA = 0
    Intro()
    i = 0
    att = 0
    dateo = today.strftime('%d/%m/%y')
    if TMACTIVE == 1:
        print("\nTEST MODE ACTIVE", end="")
    # 3 attempts to receive date input
    while i < 3:
        date = input("\n\nEnter date to view data: DD/MM/YY (Today)? ")
        if date == '':
            date = dateo
            print("Viewing today's data...\n")
            View_Today_Data()
            break
        if list(date).count('/') == 2:
            # print('x')
            try:
                bool(datetime.datetime.strptime(date, '%d/%m/%y'))
                # print(datetime.datetime.strptime(date, '%d/%m/%y'),
                #       datetime.datetime.strptime(dateo, '%d/%m/%y'))

                cnd1 = datetime.datetime.strptime(date, '%d/%m/%y')
                cnd2 = datetime.datetime.strptime(dateo, '%d/%m/%y')
                if cnd1 > cnd2:
                    print("Cannot check for future dates!")
                    att += 1
                    continue

                # print('1')
                View_OtherDays_Data(date)
                print(f'Viewing data for {date}:\n')
                OTHERDAYSDATA = 1

                break
            except Exception:
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
    # if len(Date3Rev) != 0 or len(Date2Rev) != 0 or len(Date1Rev) != 0 or
    # len(Overdue1Rev) != 0 or len(Overdue2Rev) != 0 or
    # len(Overdue3Rev) != 0or len(DateORev) != 0:
    if any((
            len(Date3Rev) != 0,
            len(Date2Rev) != 0,
            len(Date1Rev) != 0,
            len(Overdue1Rev) != 0,
            len(Overdue2Rev) != 0,
            len(Overdue3Rev) != 0,
            len(DateORev) != 0
            )):
        print('\t{<Course>(<Module>): <Topic> [<Details>]}\n')

    # This variable is for the index of presented data
    i = 0

    # INT3
    if len(Date3Rev) != 0:
        print(f'Content from {Date3Rev[0][1]} [{INT3} days ago]:\n')
        for content in Date3Rev:
            i += 1
            Revcomp.append(content)
            print(f"\t{i}) {content[0][2:]}({content[3]}): "
                  f"{content[2]}", end="")
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
            print(f"\t{i}) {content[0][2:]}({content[3]}): "
                  f"{content[2]}", end="")

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
            print(f"\t{i}) {content[0][2:]}({content[3]}): "
                  f"{content[2]}", end="")

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
            print(f"\t{i}) {content[0][2:]}({content[3]}): "
                  f"{content[2]}", end="")

            if content[4] != '':
                print(f" [{content[4]}]")
            else:
                print('')
        print('')

    # %% Overdue revisions
    OVERDUEREV = 0
    if len(Overdue1Rev) != 0 or len(Overdue2Rev) != 0 or len(Overdue3Rev) != 0:
        OVERDUEREV = 1
        print('You have overdue revisions.\n')
    if OVERDUEREV == 1:
        comboverdue = Overdue3Rev + Overdue2Rev + Overdue1Rev
        # for x in comboverdue: print(x)
        # print('\n\n')
        revlen = len(Revcomp)
        for j in range(len(comboverdue)):
            if comboverdue[j] not in Revcomp:
                Revcomp.append(comboverdue[j])
            #     print(comboverdue[j])
            # else:
            #     print('repeat')
        # print(Revcomp)
        temRev = Revcomp[revlen:]
        # print('\n\n')
        # print(temRev)
        for content in temRev:
            i += 1
            overdueprint = []
            print(f"\t{i}) {content[0][2:]}({content[3]}): "
                  f"{content[2]}", end="")

            if content[4] != '':
                print(f" [{content[4]}]", end='')
            print(" <due on ", end="")

            # adding due dates to a list
            if content in Overdue3Rev:
                overdueprint.append(content[7])
            if content in Overdue2Rev:
                overdueprint.append(content[6])
            if content in Overdue1Rev:
                overdueprint.append(content[5])

            # printing due dates
            if len(overdueprint) == 1:
                print(overdueprint[0], end="")
            elif len(overdueprint) == 2:
                print(f"{overdueprint[0]} and {overdueprint[1]}", end="")
            elif len(overdueprint) == 3:
                print(f"{overdueprint[0]}, {overdueprint[1]} "
                      f"and {overdueprint[2]}", end="")

            else:
                print('???', end="")
            # print(overdueprint)
            print('>')

    # %% Logging data
    allinds = i
    incomlis = []
    T = 1
    while T <= allinds:
        incomlis.append(T)
        T += 1
    # print(incomlis)
    i = 0
    att = 0
    # print(len(DateORev))
    repcon = 1
    while repcon == 1:
        # if (
        #         len(Date1Rev) != 0 or
        #         len(Date2Rev) != 0 or len(Date3Rev) != 0 or
        #         OVERDUEREV != 0 or len(DateORev) != 0):
        if any((
                len(Date1Rev) != 0,
                len(Date2Rev) != 0,
                len(Date3Rev) != 0,
                len(DateORev) != 0,
                OVERDUEREV != 0
                )):

            # print(incomlis)
            print('')
            while i < 3:
                try:
                    RevcompInd = input("Enter index of content to "
                                       "mark as revised: ").strip()

                    if RevcompInd == '':
                        print('No data will be marked as revised.')
                        break
                    # elif int(RevcompInd) > 0
                    # and int(RevcompInd) <= len(Revcomp):
                    if all((int(RevcompInd) > 0,
                              int(RevcompInd) <= len(Revcomp)
                              )):

                        if int(RevcompInd) not in incomlis:
                            print("Data already logged.")
                            break
                        rvcmpchk = Revcomp[int(RevcompInd) - 1]
                        revcon = input(f"Confirm completing {rvcmpchk[0][2:]}: "
                                       f"{rvcmpchk[2]} (yes/no) ")

                        # if revcon != 'yes' and revcon != '':
                        if revcon not in ('', 'yes'):
                            print("Data will not be logged.")
                            # input("\nPress Enter to return to Main Menu...")
                            break
                        # print(rvcmpchk[:5])
                        # print(Date1Rev)
                        if rvcmpchk[:5] in Date1Rev:
                            # print('date1rev')
                            db.execute(f"UPDATE \"{rvcmpchk[0]}\" "
                                       f"SET Status1 = 1 "
                                       f"WHERE Date = \"{rvcmpchk[1]}\" "
                                       f"AND Topic = \"{rvcmpchk[2]}\" "
                                       f"AND Module = {rvcmpchk[3]}")

                        if rvcmpchk[:5] in Date2Rev:
                            # print('date2rev')
                            db.execute(f"UPDATE \"{rvcmpchk[0]}\" "
                                       f"SET Status2 = 1 "
                                       f"WHERE Date = \"{rvcmpchk[1]}\" "
                                       f"AND Topic = \"{rvcmpchk[2]}\" "
                                       f"AND Module = {rvcmpchk[3]}")

                        if rvcmpchk[:5] in Date3Rev:
                            # print('date3rev')
                            db.execute(f"UPDATE \"{rvcmpchk[0]}\" "
                                       f"SET Status3 = 1 "
                                       f"WHERE Date = \"{rvcmpchk[1]}\" "
                                       f"AND Topic = \"{rvcmpchk[2]}\" "
                                       f"AND Module = {rvcmpchk[3]}")

                        # print('asdfgh')
                        if OTHERDAYSDATA == 1:
                            # print('otd')
                            for abc in range(3):
                                abc += 1
                                db.execute(f"UPDATE \"{rvcmpchk[0]}\" "
                                           f"SET Status{abc} = 1 "
                                           f"WHERE Date = \"{rvcmpchk[1]}\" "
                                           f"AND Date{abc} = \"{date}\" "
                                           f"AND Topic = \"{rvcmpchk[2]}\" "
                                           f"AND Module = {rvcmpchk[3]}")

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
                                db.execute(f"UPDATE \"{rvcmpchk[0]}\" "
                                           f"SET Status3 = 1 "
                                           f"WHERE Date = \"{rvcmpchk[1]}\" "
                                           f"AND Topic = \"{rvcmpchk[2]}\" "
                                           f"AND Module = {rvcmpchk[3]}")

                            if rvcmpchk in Overdue2Rev:
                                # print('Overdue2Rev')
                                db.execute(f"UPDATE \"{rvcmpchk[0]}\" "
                                           f"SET Status2 = 1 "
                                           f"WHERE Date = \"{rvcmpchk[1]}\" "
                                           f"AND Topic = \"{rvcmpchk[2]}\" "
                                           f"AND Module = {rvcmpchk[3]}")

                            if rvcmpchk in Overdue1Rev:
                                # print('Overdue1Rev')
                                db.execute(f"UPDATE \"{rvcmpchk[0]}\" "
                                           f"SET Status1 = 1 "
                                           f"WHERE Date = \"{rvcmpchk[1]}\" "
                                           f"AND Topic = \"{rvcmpchk[2]}\" "
                                           f"AND Module = {rvcmpchk[3]}")

                            # print('this ran')
                        DBH.commit()
                        incomlis.remove(int(RevcompInd))
                        print('Data logged.')
                        break
                    else:
                        print("Enter valid integer between "
                              f"1 and {len(Revcomp)}")
                        att += 1
                except Exception:
                    print('Enter integers only')
                    att += 1
                if att >= 3:
                    Abort()
                    break
                i += 1
        else:
            poslen = 0
            for teams in tablenames:
                ind = 1
                while ind <= 3:
                    tem = db.execute("SELECT Status1, Status2, Status3 "
                                     f"FROM \"{teams}\" "
                                     f"WHERE Date{ind} = \"{date}\"")

                    for i in tem:
                        poslen += 1
                    ind += 1
            # print(poslen)
            if poslen != 0:
                print("All revisions completed!")
                input("\nPress Enter to return to Main Menu...")
                return
            print("No record found!")
            input("\nPress Enter to return to Main Menu...")
            return
        repcon = 0
        # print(incomlis, alcomp)
        if len(incomlis) != 0:
            repcon = input("\nPress Spacebar and Enter to log data again, "
                           "or Press Enter to return to Main Menu...")

        if len(incomlis) == 0:
            print("\nAll revisions completed!")
            input("\nPress Enter to return to Main Menu...")
            break
        if repcon == ' ':
            repcon = 1
        else:
            repcon = 0
    # input("\nPress Enter to return to Main Menu...")


# %%
def Modify_Data():
    global modify_menu
    global path
    Intro()
    i = 0
    att = 0
    index = -1
    print('\nPerform action:')
    for item in range(len(modify_menu)):
        print(f"{item+1}) {modify_menu[item]}")

    # 3 Attempts to get input
    while i < 3:
        try:
            index = input("\nIndex of submenu: ").strip()
            if index == '':
                print(f'Enter an index between 1 and {len(modify_menu)}')
                att += 1
            elif int(index) <= len(modify_menu) and int(index) > 0:
                path.append(modify_menu[int(index) - 1] + ' > ')
                index = int(index)
                break
            else:
                print(f'Enter valid index between 1 and {len(modify_menu)}')
                att += 1
        except Exception:
            print('Enter Integers Only')
            att += 1
        if att >= 3:
            Abort()
            return
        i += 1

    # Performing the action
    # if index == 1:
    if index == len(modify_menu):
        Intro()
        print("\nReturning to Main Menu...")
        return
    if index == 1:
        Test_Mode()
    elif index == 2:
        Intro()
        print('\n')
        Update_Data()
        input("\nPress Enter to return to previous menu...")
    elif index == 3:
        Update_sem()
    else:
        Intro()
        print('\nUnder Construction!')
        input("\nPress Enter to return to previous menu...")
    path.pop()
    Modify_Data()


# %%
def Misc_Info():
    global misc_menu
    global path
    Intro()
    i = 0
    att = 0
    index = -1
    print('\nPerform action:')
    for item in range(len(misc_menu)):
        print(f"{item+1}) {misc_menu[item]}")

    while i < 3:
        try:
            index = input("\nIndex of submenu: ").strip()
            if index == '':
                print(f'Enter an index between 1 and {len(misc_menu)}')
                att += 1
            elif int(index) <= len(misc_menu) and int(index) > 0:
                path.append(misc_menu[int(index) - 1] + ' > ')
                index = int(index)
                break
            else:
                print(f'Enter valid index between 1 and {len(misc_menu)}')
                att += 1
        except Exception:
            print('Enter Integers Only')
            att += 1
        if att >= 3:
            Abort()
            return
        i += 1
    if index == len(misc_menu):
        Intro()
        print("\nReturning to Main Menu...")
        return
    if index == 1:
        Notes()
    elif index == 2:
        Modify_Intervals()
    path.pop()
    Misc_Info()
    

# %%
def main():
    while True:
        index = Main_Menu()
        if index == 1:
            Add_Data()
        elif index == 2:
            View_Data()
        elif index == 3:
            Modify_Data()
        elif index == 4:
            Misc_Info()
        elif index == len(main_menu):
            Outro()
            break
        else:
            Intro()
            print('\nUnder Construction!')
            input("\nPress Enter to return to Main Menu...")


# %% Program runs here
if __name__ == "__main__":
    try:
        main()
    except Exception as E:
        os.system('clear')
        print("\nCongratulations! You've broken the code!")
        print("\nIMPORTANT: Unsaved data may or may not be saved.")
        savcon = input("\nSave error messages as text file? (yes/no) ").strip()
        # if savcon == 'yes' or savcon == '':
        if savcon in ('', 'yes'):
            print("\nSaving error messages...", end="")
            error = "".join(traceback.TracebackException.from_exception(E).format())
            texfil = DBDIR + "errors.txt"
            fhand = open(texfil, "a")
            date = str(datetime.datetime.now()) + '\n'
            fhand.write(date)
            fhand.write(error)
            fhand.write("\n\n")
            fhand.close()
            print("messages saved!\n\n")
            print('*'*terlen)
        else:
            print("\nMessages will not be saved.\n\n")
            print('*'*terlen)
    finally:
        DBH.commit()
        DBH.close()
