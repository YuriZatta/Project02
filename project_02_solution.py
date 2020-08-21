import re
from random import randint as auto_generate
import csv
from datetime import datetime as time
from pathlib import Path

class Bank:
    """
    This class create objects/instances capable of reading and returning 
    '.csv' files. Can output and manipulate its contents as a dictionary.
    This is the main Bank, where you can do all sort of bank activities!
    Like:
    - Add New Customers
    - Withdraw Money, from client request!
    - Deposit Money, from client request!
    - Transfer Money, from client request!
    - Overdraft Protection, for client security!
    - Overdraft Charge, for our amusement!
    - Overdraft Block!
    - And generate history of transactions from all users!
    """
    """
    This class cannot:
    - Change client's password!
    - Anything from above without client credentials!
    - specific login to only one account and do all the above without
    log-in every information over and over! For client security!
    """

    def __init__(self):
        #fixing the file's path, we avoid huge mistakes! Everything done
        #will be forever saved and linked.
        self.__file_name = 'bank.csv'
        self.__bank_users_data = {}
        self.__bank_users_hist = {}
        self.bank_user_dic = {}
        self.__h_file_dir = Path("bank_history.csv")
        self.__counter = 0
        Bank.__data_to_dic(self)
        self.special_characteries = re.compile('"?!@#%&*_{[\<|>/]}:;,.¹²³£¢¬ªº°')

    # These methods beneath are related to data handling!
    def __check_content(self):
        """
        This method help us to check the full info inside the raw data. 
        To be sure that we haven't done anything wrong with it when 
        creating our dictionary later!
        """
        try:
            files = open(self.__file_name,'r')
            
            for line in files:
                
                bank_info_total = line.split(';')
               
                print(bank_info_total)
            
            files.close()
        except IOError:
            print('\nThe file inputed does not exist inside the folder!\n')
        
    def __data_to_dic(self):
        """
        This method iterates over the content of the file and outputs 
        the information in a dictionary format checking if all the 5
        infos was provided by the file. Besides the original provided
        information, this method and the followings methods creates a
        new collumn of data, the Account_Overdraft_Counter, to help us
        block or unlock accounts that are negatived!
        The data as stored:
        account_id | frst_name | last_name | password | balance_checking
        | balance_savings| Account_Overdraft_Counter
        """
        # Here I use the same code that I've used in the last homework
        bank_info = []
        # And I create this object to double check if any weird data was
        # stored by someone.
        special_characteries = re.compile('"?!@#%&*_{[\<|>/]}:;,.¹²³£¢¬ªº°')

        try:
            files = open(self.__file_name,'r')

            for line in files:
                
                bank_raw_info = (line.strip()).split(';')
                
                bank_raw_info = [x.strip() for x in bank_raw_info]
                
                bank_info.append(bank_raw_info)
                
            for user in range(len(bank_info)):
                
                user_list = bank_info[user]
                
                for index in range(len(user_list)):
                    
                    element = user_list[index]
    
                    account_id = user_list[0]
                    # Here we help the Bank staff to check if anything
                    # weird is happening!
                    if (special_characteries.search(user_list[1]) == None):
                        first_name = user_list[1]
                    else:
                        raise TypeError("--> !!! CONTACT BANK, \
                            SOMETHING WRONG !!! <--")
                    
                    if (special_characteries.search(user_list[2]) == None):
                        last_name = user_list[2]
                    else:
                        raise TypeError("\n\t--> !!! CONTACT BANK, \
                            SOMETHING WRONG WITH USER NAME !!! <--\n")
                    
                    if user_list[3].isalpha():
                        raise TypeError("\n\t--> !!! CONTACT BANK, \
                            SOMETHING WRONG WITH USER PASSWORD !!! <--\n")
                    else:
                        password = str(user_list[3])
                    # No money in the world is INT, so here we change
                    # our clients money from INT to Float!
                    balance_checking = float(user_list[4])
                    balance_savings = float(user_list[5])
                    # This one beneath is the Account_Overdraft_Counter!
                    try:
                        # It's checking if already exists, otherwise
                        # set up to 0 and incert into the data!
                        block_counter = int(user_list[6])
                    except:
                        block_counter = 0

                    self.__bank_users_data[account_id] = [
                        first_name, last_name, password, 
                        balance_checking, balance_savings, block_counter
                        ]
                    # making it public at the same time...
                    self.bank_user_dic[account_id] = [
                        first_name, last_name, password, 
                        balance_checking, balance_savings, block_counter
                        ]
                    # making some history with our Bank! Now every
                    # transaction is recorded! And we are checking if 
                    # its already exists in the computer!
                    if self.__h_file_dir.is_file():
                        Bank.__data_hist_to_dic(self)
                    else:
                        hist = {}
                        self.__bank_users_hist[account_id] = [
                            first_name, last_name, hist
                        ]
                    # hist = {}
                    # self.__bank_users_hist[account_id] = [
                    #     first_name, last_name, hist
                    # ]
            Bank.__new_file(self)
            return f'\n{self.__bank_users_data}\n'
            
            files.close()
        except IOError:
            print('\nThe file inputed does not exist inside folder!\n')
    
    def __add_new_user(self):
        """
        This method allow our class Bank to add new custumers to our
        data-base! It checks if the password is safe enough for ACME
        standards and checks if the users name is funy... And has
        special conditions to decide if the new account will have both
        checking and savings accounts, or one of the other.
        - It generates an ID randomly at the size of the original IDs!
        - It also automatically adds the new client to the history data!
        """
        f_name = input("\nPlease, incert the new user first name:\n->")
        l_name = input("\nPlease, incert the new user last name:\n->")
        new_pass = input("\nPlase, ask for the new user to enter the new password:\n->")
        money_acc = float(input("\nPlease, ask the user to deposit at least $1.00:\n->"))
        money_sav = float(input("\nPlease, ask the user to deposit at least $1.00:\n->"))
        
        if (self.special_characteries.search(f_name) == None) and (self.special_characteries.search(l_name) == None):
            first_name = f_name
            last_name = l_name
        else:
            first_name = False
            last_name = False
            print("\nInvalid character for Name or Last Name\n")
        
        if new_pass.isalpha():
            new_password = False
            print("\nWeak password\n")
        else:
            new_password = new_pass

        if money_acc < 0:
            money_acc = False
            print(f"\nTo create an new account {first_name} \
                needs to deposit any amount of money\n")
        elif money_acc == 0:
            acc_money = None
        else:
            acc_money = float(money_acc)
        
        if money_sav < 0:
            money_sav = False
            print(f"\nTo create an new account {first_name} \
                needs to deposit any amount of money\n")
        elif money_sav == 0:
            sav_money = None
        else:
            sav_money = float(money_sav)
            
        if first_name != False and last_name != False and new_password != False and acc_money != False and sav_money != False:
            if sav_money == None and acc_money != None:
                new_user_id = str(auto_generate(10000,20000))
                while new_user_id in self.__bank_users_data:
                    new_user_id = str(auto_generate(10000,20000))
                #saving_acc = None
                block_counter = 0
                self.__bank_users_data[new_user_id] = [
                            first_name, last_name, new_password, 
                            acc_money, sav_money, block_counter
                            ]
                Bank.__new_file(self)
                Bank.__update_file(self)
                print("\nMoney deposited and new Account created!\n")
                print(f"\nYour ID is: {new_user_id}")
            elif acc_money == None and sav_money != None:
                new_user_id = str(auto_generate(10000,20000))
                while new_user_id in self.__bank_users_data:
                    new_user_id = str(auto_generate(10000,20000))
                #acc_money = None
                block_counter = 0
                self.__bank_users_data[new_user_id] = [
                            first_name, last_name, new_password, 
                            acc_money, sav_money, block_counter
                            ]
                
                Bank.__new_file(self)
                Bank.__update_file(self)
                print("\nMoney deposited and new Account created!\n")
                print(f"\nYour ID is: {new_user_id}\n")

            elif acc_money == None and sav_money == None:
                print("\nAccount not created if neither Account or savings have any money!\n")
            
            else:
                new_user_id = str(auto_generate(10000,20000))
                while new_user_id in self.__bank_users_data:
                    new_user_id = str(auto_generate(10000,20000))

                block_counter = 0
                self.__bank_users_data[new_user_id] = [
                            first_name, last_name, new_password, 
                            acc_money, sav_money, block_counter
                            ]
                Bank.__new_file(self)
                Bank.__update_file(self)
                print("\nMoney deposited and new Account created!")
                print(f"\nYour ID is: {new_user_id}\n")
            hst = {}
            self.__bank_users_hist[new_user_id] = [
                        first_name, last_name, hst
                    ]

        return f'\n{self.__bank_users_data}\n'

    def __new_file(self):
        """
        This method let our instance to generate a new Python file for
        our dictionary collected from the '.csv' file. This was one of
        the many aptempts to make it safe to connect with a child class.
        I'm not sure if it has real impact over the real world, but I'll
        keep it!
        -> 'open(, write)" !!!
        """
        #self.__counter += 1
        new_file_name = (
            self.__file_name[:-4] + '.py'
        )
        try:
            new_file = open(new_file_name, 'w')
            new_file.write('user_data = {}'.format(self.__bank_users_data))
            #print("\nNew File Created!\n")
            new_file.close()
        except IOError:
            print('\nThis file already exists in folder!\n')
    
    def __update_file(self):
            """
            This method let our instance to update the .csv file which
            has all of our users data after transactions!
            -> 'open(, w)" !!!
            """
            #self.__counter += 1
            # new_file_name = (
            #     self.__file_name[:-4] + '.py'
            # )
                # update_file = open('bank_1.csv', 'w')
                # update_file.write('{}'.format(self.__bank_users_data))
            
            try:
                with open('bank.csv', 'w') as f:
                    for key in self.__bank_users_data.keys():
                        f_name = self.__bank_users_data[key][0]
                        l_name = self.__bank_users_data[key][1]
                        pwd = self.__bank_users_data[key][2]
                        acc = self.__bank_users_data[key][3]
                        sav = self.__bank_users_data[key][4]
                        flag = self.__bank_users_data[key][5]
                        f.write("%s;%s;%s;%s;%s;%s;%s\n"%(key,f_name,l_name,pwd,acc,sav,flag))
                
                #print("\nNew data Updated!\n")
                f.close()
            except IOError:
                print('\nFile could not Update!\n')
    
    def __transaction_hist(self, user_id, amount, action):
        """
        This method generates a dictionary capable of store an infinit
        amount of history data of activity at the 3rd index, without the
        need to iterate over an infinit list of indexes when storing in
        a separeted .csv file! It takes the last index, that is a dic
        and stores the obj 'h_time', which holds the exact time of the
        transaction as a new key with a STR object 'report' as a value
        that describes what happened at the moment!
        """
        # print(self.__bank_users_hist)
        # print(self.__bank_users_hist['10001'][2])
        #h_counter = 0
        
        times = time.now()
        h_time = times.strftime("%c")
        h_amount = amount
        h_action = action
        report = f"Transaction of {h_amount} from {h_action}"
        h = self.__bank_users_hist[user_id][2]
        h[h_time] = [report]
        clean_report = f"Transaction of {h_amount} from {h_action} at {h_time}"
        #h_counter += 1
        print("Your receit:", clean_report)
        
        #print(self.__bank_users_hist)

        Bank.__update_hist_file(self)

        return f'\n{self.__bank_users_hist}\n'
        
    def __data_hist_to_dic(self):
        """
        This method works almost exactly as the previously data_to_dic!
        It iterates over a .csv file which holds the history of activity
        data, and translate back to our hist_dic already in use. This
        was vital, otherwise every time this instance initiates, it
        would erase all the data of the dictionary and stores a brand
        new empty dictionary to the .csv file at the begining of this
        class execution!
        """
        bank_h_info = []
        try:
            files = open(self.__h_file_dir,'r')
            for line in files:
                bank_h_raw_info = (line.strip()).split(';')
                bank_h_raw_info = [x.strip() for x in bank_h_raw_info]
                bank_h_info.append(bank_h_raw_info)
                
            for user_h in range(len(bank_h_info)):
                user_h_list = bank_h_info[user_h]
                # here we use eval() a sick method that helps to change
                # strs that looks like dictionary into dictionary!
                for i in range(len(user_h_list)):
                    element = user_h_list[i]
                    account_id = user_h_list[0]
                    first_name = user_h_list[1]
                    last_name = user_h_list[2]
                    hist = eval(user_h_list[3])
                    self.__bank_users_hist[account_id] = [
                        first_name, last_name, hist
                    ]
            Bank.__update_hist_file(self)
            return f'\n{self.__bank_users_hist}\n'
            
            files.close()

        except IOError:
            print('\nThe file inputed does not exist inside folder!\n')

    def __update_hist_file(self):
        """
        This method let our instance to update the history file which
        has all of our users transaction data! It takes our hist_dic in
        use at the time of this class running, and stores in the .csv
        file format provided to us! And because this make our dic at
        the last index into a STR, the above/previously method is needed
        to convert [2] back into a python dictionary!
        -> 'open(, w)" !!!
        """
        try:
            with open('bank_history.csv', 'w') as d:
                for key in self.__bank_users_hist.keys():
                    f_name = self.__bank_users_hist[key][0]
                    l_name = self.__bank_users_hist[key][1]
                    hst = self.__bank_users_hist[key][2]
                    d.write("%s;%s;%s;%s\n"%(key,f_name,l_name,hst))
            
            #print("\nNew History data Updated!\n")
            d.close()
        except IOError:
            print('\nHistory File could not Update!\n')

    def __acme_layout(self, user_id):
        """
        A design choice to help the Bank's staff to check if he's doing
        the operations with the rightfull client, and not someone else!
        """
        u_a = self.__bank_users_data[user_id][1]
        u_f = self.__bank_users_data[user_id][0]
        u_i = user_id
        print("\n")
        print("#####################")
        print(f"_____{u_a}'s Accounts_____")
        print(f"Check client's documents befor proceed!\nClient's 1st name:{u_f}\nClient's last name:{u_a}\nClient's Bank ID: {user_id}")
        print("#####################")
        print("||||||__ACME__|||||||")
        return f"Check client's documents befor proceed!\nClient's 1st name:{u_f}\nClient's last name:{u_a}\nClient's Bank ID: {user_id}"
        
    def __print_hist(self):
        """
        A simple method to let the user easely check the history of
        activities in any Bank Machine!
        """
        user_id = input("\nPlease, insert ID:\n->")
        user_pass = input("\nPlease, incert your Password:\n->")
        if user_id in self.__bank_users_data:
            if user_pass in self.__bank_users_data[user_id]:
                if self.__h_file_dir.is_file():
                    Bank.__data_hist_to_dic(self)
                    p1 = self.__bank_users_hist[user_id][2]
                    
                    for key in p1:
                        p2 = p1[key]
                        print(key,p2[0])
                else:
                    for key in p1:
                        p2 = p1[key]
                        print(key,p2[0])
                    # print(self.__bank_users_hist[user_id][2])
            else:
                print("Wrong credentials!")
                return "Wrong credentials!"
        else:
            print("Wrong credentials!")
            return "Wrong credentials!"
            
    # These methods beneath are related to money transactions!
    
    def __withdraw_from_acc(self):
        """
        This method let our Bank staff to proceed along with the client
        to collect money from the Checking Account at the balcony if the
        client do not have access to his app or card!
        After receiving the User ID and the amount requested, the staff
        can check if the User's documents is the same as the Client's
        information. This will NOT block the User to log-in and make the
        transaction, but the staff can alert the manager if something
        weird is happening. 
        """
        # this is a flag to let the system knows what type of activity
        # will be recorded in the history file!
        action_done = None
        user_id = input("\nPlease, incert User ID here:\n->")
        amount = float(input("\nHow much our client wants to be collected?\n->"))
        # Calling for the layout which displays the client info for our
        # staff at the balcony.
        Bank.__acme_layout(self, user_id)
        # The user proceeds with the log-in either way!
        if Bank.__log_in(self) == True:
            # This calls for a method that checks if the user is trying 
            # to do a wrong type of operation, for example: trying to 
            # collect money from checking account, but only savings 
            # exists in the system!
            if Bank.__wrong_operation_acc(self, user_id) != False:
                # Calling for a method that check if the account is
                # currently blocked by too many overdrafts!
                if Bank.__overdraft_blocker_acc(self, user_id) != False:
                    # Calling for a method that will check if the user
                    # is doing or can do a overdraft!
                    if Bank.__overdraft_protection_acc(self, user_id) != False:
                        self.__bank_users_data[user_id][3] -= amount
                        # Calling the same method again to check if after
                        # transaction, the user would cross the protection!
                        if Bank.__overdraft_protection_acc(self, user_id) != False:
                            Bank.__overdraft_acc_charge(self, user_id)
                            Bank.__new_file(self)
                            Bank.__update_file(self)
                            a = self.__bank_users_data[user_id][3]
                            print("\nTransaction succeeded!")
                            print(f"\n{amount} was collected from yours Checking Account!")
                            print(f"\nYour Checking Account currently holds: {a}\n")
                            action_done = True
                            # Activating the method that stores history!
                            if action_done == True:
                                action = "Checking Account withdraw"
                                Bank.__transaction_hist(self, user_id, amount, action)
                                Bank.__update_hist_file(self)
                            return f"\nTransaction succeeded!\n{amount} was collected from yours Checking Account!\nYour Checking Account currently holds: {a}\n"
                        else:
                            # If the users cross the overdraft protection
                            # line, the money comes back to the account!
                            self.__bank_users_data[user_id][3] += amount
                            a = self.__bank_users_data[user_id][3]
                            print("\nTransaction denied!")
                            print("\nYou cannot have a depbt over -100,00!")
                            print(f"\n{amount} was sturned to yours Checking Account!")
                            print(f"\nYour Checking Account currently holds: {a}\n")
                            action_done = False
                            if action_done == False:
                                action = "Checking Account withdraw DENIED!"
                                Bank.__transaction_hist(self, user_id, amount, action)
                                Bank.__update_hist_file(self)
                            return f"\nTransaction denied!\n{amount} was sturned to yours Savings Account!\nYou cannot have less then 00,00 in your saving account!\nYour Savings Account currently holds: {a}\n"
                    else:
                        print("\nToo many overdrafts in this account! Operation denied!\n")
                else:
                    print("\nAccount is blocked by too many overdrafts!\n")
            else:
                print("\nThis saving account cannot do this operation, \
                first you need to create a checking account!\n")
        else:
            print("\nWrong credentials, try again!\n")
        
    def __withdraw_from_savings(self):
        """
        The same method as above, but for the savings account! All the
        individual explenations of this method was provided at the
        method above! 
        """
        action_done = None
        user_id = input("Please, incert User ID here:\n->")
        amount = float(input("How much our client wants to be collected?\n->"))
        Bank.__acme_layout(self, user_id)
        if Bank.__log_in(self) == True:
            if Bank.__overdraft_protection_savings(self, user_id) != False:
                self.__bank_users_data[user_id][4] -= amount
                if Bank.__overdraft_protection_savings(self, user_id) != False:
                    Bank.__new_file(self)
                    Bank.__update_file(self)
                    b = self.__bank_users_data[user_id][4]
                    print("\nTransaction succeeded!")
                    print(f"\n{amount} was collected from yours Savings Account!")
                    print(f"\nYour Savings Account currently holds: {b}\n")
                    action_done = True
                    if action_done == True:
                        action = "Savings Account withdraw"
                        Bank.__transaction_hist(self, user_id, amount, action)
                    return f"\nTransaction succeeded!\n{amount} was collected from yours Savings Account!\nYour Savings Account currently holds: {b}\n"
                else:
                    self.__bank_users_data[user_id][4] += amount
                    b = self.__bank_users_data[user_id][4]
                    print("\nTransaction denied!")
                    print("\nYou cannot have less then 00,00 in your saving account!")
                    print(f"\n{amount} was sturned to yours Savings Account!")
                    print(f"\nYour Savings Accounts currently holds: {b}\n")
                    action_done = False
                    if action_done == False:
                        action = "Checking Account withdraw DENIED!!!"
                        Bank.__transaction_hist(self, user_id, amount, action)
                    return f"\nTransaction denied!\n{amount} was sturned to yours Savings Account!\nYou cannot have less then 00,00 in your saving account!\nYour Savings Account currently holds: {b}\n"
            else:
                print("\nThere is no money in your savings account!\n")
        else:
            print("\nWrong credentials, try again!\n")

    def __deposit_in_acc(self):
        """
        It's the same as the methods above, but reversed! The only thing
        different here, is that there is no need for log-in! Anyone can
        come to a bank in the real world and provide only the deposited
        account information!
        Besides that, if the user tries to make a deposit into checking
        account, but this account is only savings, it will automaticaly
        send the money to the savings account without the user notice.
        Protecting the privacy of the client's account! 
        """
        action_done = None
        user_id = input("\nPlease, incert User ID here:\n->")
        f_name = input("\nPlease, incert our client first name:\n->")
        l_name = input("\nPlease, incert our client last name:\n->")
        amount = float(input("\nHow much our client wants to deposit?\n->"))
        Bank.__acme_layout(self, user_id)
        if user_id in self.__bank_users_data:
            if self.__bank_users_data[user_id][0] == f_name:
                if self.__bank_users_data[user_id][1] == l_name:
                    # This method will check if the Checking Account is
                    # available, otherwise our code will send to Savings
                    if Bank.__wrong_operation_acc(self, user_id) != False:
                        self.__bank_users_data[user_id][3] += amount
                        Bank.__overdraft_blocker_nuller(self, user_id)
                        Bank.__new_file(self)
                        Bank.__update_file(self)
                        a = self.__bank_users_data[user_id][0]
                        print(f"\n{amount} was deposited to {a}'s account!\n")
                        action_done = True
                        if action_done == True:
                                action = "Depositing into Checking Account"
                                Bank.__transaction_hist(self, user_id, amount, action)
                        return f"\n{amount} was deposited to {a}'s account!\n"
                    else:
                        # here we just sent the money to the apropriate
                        # account without the user to notice!
                        self.__bank_users_data[user_id][4] += amount
                        Bank.__new_file(self)
                        Bank.__update_file(self)
                        a = self.__bank_users_data[user_id][0]
                        print(f"\n{amount} was deposited to {a}'s account!\n")
                        action_done = False
                        if action_done == False:
                                action = "Depositing into Savings Account"
                                Bank.__transaction_hist(self, user_id, amount, action)
                        return f"\n{amount} was deposited to {a}'s account!\n"
                else:
                    print("\nWrong user information provided! Try Again!\n")
            else:
                print("\nWrong user information provided! Try Again!\n")
        else:
            print("\nUser not found!\n")

    def __deposit_in_savings(self):
        """
        The same as the method above but reversed to start with the
        savings account, if it does not exists, it'll send the money
        to the checking account without the user notecing!
        """
        action_done = None
        user_id = input("\nPlease, incert User ID here:\n->")
        f_name = input("\nPlease, incert our client first name:\n->")
        l_name = input("\nPlease, incert our client last name:\n->")
        amount = float(input("\nHow much our client wants to deposit?\n->"))
        Bank.__acme_layout(self, user_id)
        if user_id in self.__bank_users_data:
            if self.__bank_users_data[user_id][0] == f_name:
                if self.__bank_users_data[user_id][1] == l_name:
                    if Bank.__wrong_operation_sav(self, user_id) != False:
                        self.__bank_users_data[user_id][4] += amount
                        Bank.__new_file(self)
                        Bank.__update_file(self)
                        a = self.__bank_users_data[user_id][0]
                        print(f"\n{amount} was deposited to {a}'s account!\n")
                        action_done = True
                        if action_done == True:
                                action = "Depositing into Savings Account"
                                Bank.__transaction_hist(self, user_id, amount, action)
                        return f"\n{amount} was deposited to {a}'s account!\n"
                    else:
                        self.__bank_users_data[user_id][3] += amount
                        Bank.__new_file(self)
                        Bank.__update_file(self)
                        a = self.__bank_users_data[user_id][0]
                        print(f"\n{amount} was deposited to {a}'s account!\n")
                        action_done = False
                        if action_done == False:
                                action = "Depositing into Checking Account"
                                Bank.__transaction_hist(self, user_id, amount, action)
                        return f"\n{amount} was deposited to {a}'s account!\n"
                else:
                    print("\nWrong user information provided! Try Again!\n")
            else:
                print("\nWrong user information provided! Try Again!\n")
        else:
            print("\nUser not found!\n")

    def __deposit_from_acc_to_savings(self):
        """
        This method is similar to all above, it takes the client's money
        from the Checking Account and transfer to its own Savings Acc!
        But if this operation cross the overdraft line, it'll send the
        money back to the Checking Account and let the client to know
        what is happening!
        """
        action_done = None
        user_id = input("\nPlease, incert User ID here:\n->")
        amount = float(input("\nHow much our client wants to be transfered?\n->"))
        Bank.__acme_layout(self, user_id)
        if Bank.__log_in(self) == True:
            if Bank.__wrong_operation_acc(self, user_id) != False:
                if Bank.__wrong_operation_sav(self, user_id) != False:
                    if Bank.__overdraft_blocker_acc(self, user_id) != False:
                        if Bank.__overdraft_protection_acc(self, user_id) != False:
                            self.__bank_users_data[user_id][3] -= amount
                            # Here we are checking if th Overdraft Line
                            # will or will not be crossed by the activty
                            if Bank.__overdraft_protection_acc(self, user_id) != False:
                                self.__bank_users_data[user_id][4] += amount
                                Bank.__overdraft_acc_charge(self, user_id)
                                #print(self.__bank_users_data[user_id])
                                Bank.__new_file(self)
                                Bank.__update_file(self)
                                a = self.__bank_users_data[user_id][3]
                                b = self.__bank_users_data[user_id][4]
                                print(f"\n{amount} was transfered from your Checking Account to your Savings Account!\n")
                                print(f"\nTransaction succeeded!\nYou currently have {a} in your Checking Account, \nand {b} in your Savings Account!\n")
                                action_done = True
                                if action_done == True:
                                    action = "Transfering from Checking Account to Savings Account"
                                    Bank.__transaction_hist(self, user_id, amount, action)
                                return f"\nYou currently have {a} in your Checking Account, \nand {b} in your Savings Account!\n"
                            else:
                                self.__bank_users_data[user_id][3] += amount
                                a = self.__bank_users_data[user_id][3]
                                b = self.__bank_users_data[user_id][4]
                                print("\nTransaction denied, you cannot have a depbt over -100,00\n")
                                print(f"\n{amount} was storned to your Checking Account!\n")
                                action_done = False
                                if action_done == False:
                                    action = "Transfering from Checking Account to Savings Account DENIED!!!"
                                    Bank.__transaction_hist(self, user_id, amount, action)
                                return f"\nYou currently have {a} in your Checking Account, \nand {b} in your Savings Account!\n"
                        else:
                            print("\nToo many overdrafts in this account! Operation denied!\n")
                    else:
                        print("\nAccount is blocked by too many overdrafts!\n")
                else:
                    print("\nThis checking account cannot do this operation, \
                    You do not have a savings account!\n")
            else:
                print("\nThis saving account cannot do this operation, \
                You do not have a checking account!\n")
        else:
            print("\nWrong credentials, try again!\n")

    def __collect_from_savings_to_acc(self):
        """
        The same code as above, but reversed! It collects money from our
        savings account and send to the Checking Account! If this
        operation would let the user with less then 00.00 at the Savings
        the transaction is reversed and we warn the client what happen! 
        """
        action_done = None
        user_id = input("\nPlease, incert User ID here:\n->")
        amount = float(input("\nHow much our client wants to be transfered?\n->"))
        Bank.__acme_layout(self, user_id)
        if Bank.__log_in(self) == True:
            if Bank.__wrong_operation_sav(self, user_id) != False:
                if Bank.__wrong_operation_acc(self, user_id) != False:
                    if Bank.__overdraft_protection_savings(self, user_id) != False:
                        self.__bank_users_data[user_id][4] -= amount
                        # Checking if its all good to proceed!
                        if Bank.__overdraft_protection_savings(self, user_id) != False:
                            self.__bank_users_data[user_id][3] += amount
                            Bank.__overdraft_blocker_nuller(self, user_id)
                            #print(self.__bank_users_data[user_id])
                            Bank.__new_file(self)
                            Bank.__update_file(self)
                            a = self.__bank_users_data[user_id][3]
                            b = self.__bank_users_data[user_id][4]
                            print(f"\n{amount} was transfered from your Savings Account to your Checking Account!\n")
                            print(f"\nTransaction succeeded!\nYou currently have {a} in your Checking Account, \nand {b} in your Savings Account!\n")
                            action_done = True
                            if action_done == True:
                                action = "Transfering from Savings Account to Checking Account"
                                Bank.__transaction_hist(self, user_id, amount, action)
                            return f"\nYou currently have {a} in your Checking Account, \nand {b} in your Savings Account!\n"
                        else:
                            self.__bank_users_data[user_id][4] += amount
                            a = self.__bank_users_data[user_id][3]
                            b = self.__bank_users_data[user_id][4]
                            print("\nTransaction denied, you cannot have less then 00,00 in your saving account!\n")
                            print(f"\n{amount} was storned to your Savings Account!\n")
                            action_done = False
                            if action_done == False:
                                action = "Transfering from Savings Account to Checking Account DENIED!!!"
                                Bank.__transaction_hist(self, user_id, amount, action)
                            return f"\nYou currently have {a} in your Checking Account, \nand {b} in your Savings Account!\n"
                    else:
                        print("\nTransaction denied, you cannot have less then 00,00 in your saving account!\n")
                else:
                    print("\nThis saving account cannot do this operation, \
                    You do not have a checking account!\n")
            else:
                print("\nThis checking account cannot do this operation, \
                You do not have a savings account!\n")
        else:
            print("\nWrong credentials, try again!\n")

    def __transfer_from_acc_to_another_acc(self):
        """
        The same as the methods above, but between different clients!
        And as usual, if the target client does not have Checking Acc,
        the money will go automatically to the Savings Account!
        """
        action_done = None
        user_id = input("\nPlease, incert User ID here:\n->")
        friend_id = input("\nPlease, incert the Friend User ID here:\n->")
        f_name = input("\nPlease, incert the friend first name:\n->")
        fl_name = input("\nPlease, incert the friend last name:\n->")
        amount = float(input("\nHow much our client wants to be transfered?\n->"))
        Bank.__acme_layout(self, user_id)
        if Bank.__log_in(self) == True:
            if Bank.__wrong_operation_acc(self, user_id) != False:
                if Bank.__overdraft_blocker_acc(self, user_id) != False:
                    if Bank.__overdraft_protection_savings(self, user_id) != False:
                        if friend_id in self.__bank_users_data:
                            if self.__bank_users_data[friend_id][0] == f_name:
                                if self.__bank_users_data[friend_id][1] == fl_name:
                                    self.__bank_users_data[user_id][3] -= amount
                                    if Bank.__overdraft_protection_acc(self, user_id) != False:
                                        if Bank.__wrong_operation_acc(self, friend_id) != False:
                                            self.__bank_users_data[friend_id][3] += amount
                                            Bank.__overdraft_acc_charge(self, user_id)
                                            print(f"\n{amount} was subtracted from your Checking Account!\n")
                                            # print(self.__bank_users_data[user_id])
                                            a = self.__bank_users_data[user_id][3]
                                            b = self.__bank_users_data[user_id][4]
                                            print(f"\n{amount} was transfered from your Savings Account to your Checking Account!\n")
                                            print(f"\nTransaction succeeded!\nYou currently have {a} in your Checking Account, \nand {b} in your Savings Account!\n")
                                            Bank.__new_file(self)
                                            Bank.__update_file(self)
                                            action_done = True
                                            if action_done == True:
                                                action = f"Transfering from Checking Account to {f_name}'s Account"
                                                Bank.__transaction_hist(self, user_id, amount, action)
                                            return "\nOperation succeeded!\n"
                                        else:
                                            self.__bank_users_data[friend_id][4] += amount
                                            Bank.__overdraft_acc_charge(self, user_id)
                                            print(f"\n{amount} was subtracted from your Checking Account!\n")
                                            # print(self.__bank_users_data[user_id])
                                            a = self.__bank_users_data[user_id][3]
                                            b = self.__bank_users_data[user_id][4]
                                            print(f"\n{amount} was transfered from your Savings Account to your Checking Account!\n")
                                            print(f"\nTransaction succeeded!\nYou currently have {a} in your Checking Account, \nand {b} in your Savings Account!\n")
                                            Bank.__new_file(self)
                                            Bank.__update_file(self)
                                            action_done = False
                                            if action_done == False:
                                                action = f"Transfering from Checking Account to {f_name}'s Account"
                                                Bank.__transaction_hist(self, user_id, amount, action)
                                            return "\nOperation succeeded!\n"
                                    else:
                                        self.__bank_users_data[user_id][3] += amount
                                        print("\nTransaction denied, you cannot have a depbt over -100,00\n")
                                        print(f"\n{amount} was storned to your Checking Account!\n")
                                        # print(self.__bank_users_data[user_id])
                                        a = self.__bank_users_data[user_id][3]
                                        b = self.__bank_users_data[user_id][4]
                                        print(f"\n{amount} was transfered from your Savings Account to your Checking Account!\n")
                                        print(f"\nTransaction succeeded!\nYou currently have {a} in your Checking Account, \nand {b} in your Savings Account!\n")
                                        if action_done == None:
                                            action = "Checking Account withdraw DENIED!"
                                            Bank.__transaction_hist(self, user_id, amount, action)
                                        return "\nOperation denied!\n"
                                else:
                                    print("\nWrong user information provided! Try Again!\n")
                            else:
                                print("\nWrong user information provided! Try Again!\n")
                        else:
                            print("\nUser not found!\n")
                    else:
                        print("\nTransaction denied, you cannot have less then 00,00 in your saving account!\n")
                else:
                    print("\nAccount is blocked by too many overdrafts!\n")
            else:
                print("\nThis saving account cannot do this operation, \
                You do not have a checking account!\n")
        else:
            print("\nWrong credentials, try again!\n")
    
    def __transfer_from_savings_to_another_acc(self):
        """
        The same as above, but from the current client's Checking Acc
        to another client's Savings Account!
        """
        action_done = None
        user_id = input("\nPlease, incert User ID here:\n->")
        friend_id = input("\nPlease, incert the Friend User ID here:\n->")
        f_name = input("\nPlease, incert the friend first name:\n->")
        fl_name = input("\nPlease, incert the friend last name:\n->")
        amount = float(input("\nHow much our client wants to be transfered?\n->"))
        Bank.__acme_layout(self, user_id)
        if Bank.__log_in(self) == True:
            if Bank.__wrong_operation_sav(self, user_id) != False:
                if Bank.__overdraft_protection_savings(self, user_id) != False:
                    if friend_id in self.__bank_users_data:
                        if self.__bank_users_data[friend_id][0] == f_name:
                            if self.__bank_users_data[friend_id][1] == fl_name:
                                self.__bank_users_data[user_id][4] -= amount
                                if Bank.__overdraft_protection_savings(self, user_id) != False:
                                    if Bank.__wrong_operation_acc(self, friend_id) != False:
                                        self.__bank_users_data[friend_id][3] += amount
                                        print(f"\n{amount} was subtracted from your Savings Account!\n")
                                        # print(self.__bank_users_data[user_id])
                                        a = self.__bank_users_data[user_id][3]
                                        b = self.__bank_users_data[user_id][4]
                                        print(f"\n{amount} was transfered from your Savings Account to your Checking Account!\n")
                                        print(f"\nTransaction succeeded!\nYou currently have {a} in your Checking Account, \nand {b} in your Savings Account!\n")
                                        Bank.__new_file(self)
                                        Bank.__update_file(self)
                                        action_done = True
                                        if action_done == True:
                                            action = f"Transfering from Savings Account to {f_name}'s Account"
                                            Bank.__transaction_hist(self, user_id, amount, action)
                                        return "\nOperation succeeded!\n"
                                    else:
                                        self.__bank_users_data[friend_id][4] += amount
                                        print(f"\n{amount} was subtracted from your Savings Account!\n")
                                        # print(self.__bank_users_data[user_id])
                                        a = self.__bank_users_data[user_id][3]
                                        b = self.__bank_users_data[user_id][4]
                                        print(f"\n{amount} was transfered from your Savings Account to your Checking Account!\n")
                                        print(f"\nTransaction succeeded!\nYou currently have {a} in your Checking Account, \nand {b} in your Savings Account!\n")
                                        Bank.__new_file(self)
                                        Bank.__update_file(self)
                                        action_done = False
                                        if action_done == False:
                                            action = f"Transfering from Saving Account to {f_name}'s Account"
                                            Bank.__transaction_hist(self, user_id, amount, action)
                                        return "\nOperation succeeded!\n"
                                else:
                                    self.__bank_users_data[user_id][4] += amount
                                    print("\nTransaction denied, you cannot have less then 00,00 in your saving account!\n")
                                    print(f"\n{amount} was storned to your Savings Account!\n")
                                    # print(self.__bank_users_data[user_id])
                                    a = self.__bank_users_data[user_id][3]
                                    b = self.__bank_users_data[user_id][4]
                                    print(f"\n{amount} was transfered from your Savings Account to your Checking Account!\n")
                                    print(f"\nTransaction succeeded!\nYou currently have {a} in your Checking Account, \nand {b} in your Savings Account!\n")
                                    if action_done == None:
                                        action = "Savings Account withdraw DENIED!"
                                        Bank.__transaction_hist(self, user_id, amount, action)
                                    return "\nOperation denied!\n"
                            else:
                                print("\nWrong user information provided! Try Again!\n")
                        else:
                            print("\nWrong user information provided! Try Again!\n")
                    else:
                        print("\nUser not found!\n")
                else:
                    print("\nYou do not have money in your saving account!\n")
            else:
                print("\nThis checking account cannot do this operation, \
                You do not have a savings account!\n")
        else:
            print("\nWrong credentials, try again!\n")

    def __transfer_from_acc_to_another_savings(self):
        """
        The same as above, but originally from Checking Account to 
        Checking Account! If the target user don't have a Checking Acc,
        it goes to the Savings Account!
        """
        action_done = None
        user_id = input("\nPlease, incert User ID here:\n->")
        friend_id = input("\nPlease, incert the Friend User ID here:\n->")
        f_name = input("\nPlease, incert the friend first name:\n->")
        fl_name = input("\nPlease, incert the friend last name:\n->")
        amount = float(input("\nHow much our client wants to be transfered?\n->"))
        Bank.__acme_layout(self, user_id)
        if Bank.__log_in(self) == True:
            if Bank.__wrong_operation_acc(self, user_id) != False:
                if Bank.__overdraft_blocker_acc(self, user_id) != False:
                    if Bank.__overdraft_protection_savings(self, user_id) != False:
                        if friend_id in self.__bank_users_data:
                            if self.__bank_users_data[friend_id][0] == f_name:
                                if self.__bank_users_data[friend_id][1] == fl_name:
                                    self.__bank_users_data[user_id][3] -= amount
                                    if Bank.__overdraft_protection_acc(self, user_id) != False:
                                        if Bank.__wrong_operation_sav(self, friend_id) != False:
                                            self.__bank_users_data[friend_id][4] += amount
                                            Bank.__overdraft_acc_charge(self, user_id)
                                            print(f"\n{amount} was subtracted from your Checking Account!\n")
                                            # print(self.__bank_users_data[user_id])
                                            a = self.__bank_users_data[user_id][3]
                                            b = self.__bank_users_data[user_id][4]
                                            print(f"\n{amount} was transfered from your Savings Account to your Checking Account!\n")
                                            print(f"\nTransaction succeeded!\nYou currently have {a} in your Checking Account, \nand {b} in your Savings Account!\n")
                                            Bank.__new_file(self)
                                            Bank.__update_file(self)
                                            action_done = True
                                            if action_done == True:
                                                action = f"Transfering from Checking Account to {f_name}'s Account"
                                                Bank.__transaction_hist(self, user_id, amount, action)
                                            return "\nOperation succeeded\n"
                                        else:
                                            self.__bank_users_data[friend_id][4] += amount
                                            Bank.__overdraft_acc_charge(self, user_id)
                                            print(f"\n{amount} was subtracted from your Checking Account!\n")
                                            # print(self.__bank_users_data[user_id])
                                            a = self.__bank_users_data[user_id][3]
                                            b = self.__bank_users_data[user_id][4]
                                            print(f"\n{amount} was transfered from your Savings Account to your Checking Account!\n")
                                            print(f"\nTransaction succeeded!\nYou currently have {a} in your Checking Account, \nand {b} in your Savings Account!\n")
                                            Bank.__new_file(self)
                                            Bank.__update_file(self)
                                            action_done = False
                                            if action_done == False:
                                                action = f"Transfering from Checking Account to {f_name}'s Account"
                                                Bank.__transaction_hist(self, user_id, amount, action)
                                            return "\nOperation succeeded\n"
                                    else:
                                        self.__bank_users_data[user_id][3] += amount
                                        print("\nTransaction denied, you cannot have a depbt over -100,00\n")
                                        print(f"\n{amount} was storned to your Savings Account!\n")
                                        a = self.__bank_users_data[user_id][3]
                                        b = self.__bank_users_data[user_id][4]
                                        print(f"\n{amount} was transfered from your Savings Account to your Checking Account!\n")
                                        print(f"\nTransaction succeeded!\nYou currently have {a} in your Checking Account, \nand {b} in your Savings Account!\n")
                                        # print(self.__bank_users_data[user_id])
                                        if action_done == None:
                                            action = "Checking Account withdraw DENIED!"
                                            Bank.__transaction_hist(self, user_id, amount, action)
                                        return "\nOperation denied!\n"
                                else:
                                    print("\nWrong user information provided! Try Again!\n")
                            else:
                                print("\nWrong user information provided! Try Again!\n")
                        else:
                            print("\nUser not found!\n")
                    else:
                        print("\nToo many overdrafts in this account! Operation denied!\n")
                else:
                    print("\nAccount is blocked by too many overdrafts!\n")
            else:
                print("\nThis saving account cannot do this operation, \
                You do not have a checking account!\n")
        else:
            print("\nWrong credentials, try again!\n")
    
    def __transfer_from_savings_to_another_savings(self):
        """
        The same as above again, but originally a transaction between
        two Savings Accounts from different users. 
        """
        action_done = None
        user_id = input("\nPlease, incert User ID here:\n->")
        friend_id = input("\nPlease, incert the Friend User ID here:\n->")
        f_name = input("\nPlease, incert the friend first name:\n->")
        fl_name = input("\nPlease, incert the friend last name:\n->")
        amount = float(input("\nHow much our client wants to be transfered?\n->"))
        Bank.__acme_layout(self, user_id)
        if Bank.__log_in(self) == True:
            if Bank.__wrong_operation_sav(self, user_id) != False:
                if Bank.__overdraft_protection_savings(self, user_id) != False:
                    if friend_id in self.__bank_users_data:
                        if self.__bank_users_data[friend_id][0] == f_name:
                            if self.__bank_users_data[friend_id][1] == fl_name:
                                self.__bank_users_data[user_id][4] -= amount
                                if Bank.__overdraft_protection_savings(self, user_id) != False:
                                    if Bank.__wrong_operation_sav(self, friend_id) != False:
                                        self.__bank_users_data[friend_id][4] += amount
                                        print(f"\n{amount} was subtracted from your Savings Account!\n")
                                        # print(self.__bank_users_data[user_id])
                                        a = self.__bank_users_data[user_id][3]
                                        b = self.__bank_users_data[user_id][4]
                                        print(f"\n{amount} was transfered from your Savings Account to your Checking Account!\n")
                                        print(f"\nTransaction succeeded!\nYou currently have {a} in your Checking Account, \nand {b} in your Savings Account!\n")
                                        Bank.__new_file(self)
                                        Bank.__update_file(self)
                                        action_done = True
                                        if action_done == True:
                                            action = f"Transfering from Savings Account to {f_name}'s Account"
                                            Bank.__transaction_hist(self, user_id, amount, action)
                                        return "\nOperation succeeded\n"
                                    else:
                                        self.__bank_users_data[friend_id][3] += amount
                                        print(f"\n{amount} was subtracted from your Savings Account!\n")
                                        # print(self.__bank_users_data[user_id])
                                        a = self.__bank_users_data[user_id][3]
                                        b = self.__bank_users_data[user_id][4]
                                        print(f"\n{amount} was transfered from your Savings Account to your Checking Account!\n")
                                        print(f"\nTransaction succeeded!\nYou currently have {a} in your Checking Account, \nand {b} in your Savings Account!\n")
                                        Bank.__new_file(self)
                                        Bank.__update_file(self)
                                        action_done = False
                                        if action_done == False:
                                            action = f"Transfering from Savings Account to {f_name}'s Account"
                                            Bank.__transaction_hist(self, user_id, amount, action)
                                        return "\nOperation succeeded\n"
                                else:
                                    self.__bank_users_data[user_id][4] += amount
                                    print(f"\n{amount} was storned to your Savings Account!\n")
                                    print("\nTransaction denied, you cannot have less then 00,00 in your saving account!\n")
                                    # print(self.__bank_users_data[user_id])
                                    a = self.__bank_users_data[user_id][3]
                                    b = self.__bank_users_data[user_id][4]
                                    print(f"\n{amount} was transfered from your Savings Account to your Checking Account!\n")
                                    print(f"\nTransaction succeeded!\nYou currently have {a} in your Checking Account, \nand {b} in your Savings Account!\n")
                                    if action_done == None:
                                        action = "Savings Account withdraw DENIED!"
                                        Bank.__transaction_hist(self, user_id, amount, action)
                                    return "\nOperation denied!\n"
                            else:
                                print("\nWrong user information provided! Try Again!\n")
                        else:
                            print("\nWrong user information provided! Try Again!\n")
                    else:
                        print("\nUser not found!\n")
                else:
                    print("\nToo many overdrafts in this account! Operation denied!\n")
            else:
                print("\nThis saving account cannot do this operation, \
                first you need to create a savings account!\n")
        else:
            print("\nWrong credentials, try again!\n")
    
    #Every thing from here it's related to security!
    
    def __log_in(self):
        """
        A log-in method, it'll let the client to provide the account
        credentials as an input, and our code will store every input
        as an object and check with our data if the credentials are
        correct or not!
        It only return True or False, that way we can easely use this
        method inside other methods as conditions!
        """
        user_id = input("\nPlease, insert ID:\n->")
        user_f_name = input("\nPlease, insert First Name:\n->")
        user_l_name = input("\nPlease, insert Last Name:\n->")
        user_pass = input("\nPlease, incert your Password:\n->")
        if user_id in self.__bank_users_data:
            #print("User ID found!")
            if user_f_name in self.__bank_users_data[user_id]:
                #print('First Name correct!')
                if user_l_name in self.__bank_users_data[user_id]:
                    #print('Last Name correct')
                    if user_pass in self.__bank_users_data[user_id]:
                        #print(self.__bank_users_data[user_id])
                        return True
        else:
            return False

    def __overdraft_protection_acc(self, user_id):
        """
        This simple method set up a line for overdrafts, and check if
        the client is crossing it or not, returning True or False, so
        we can call it inside other functions to make conditions!
        This method checks for the user Checking Account!
        """
        if self.__bank_users_data[user_id][3] == -100:
            return False
        else:
            return True
    def __overdraft_protection_savings(self, user_id):
        """
        Same as above, but check for the client's Savings Account!
        """
        if self.__bank_users_data[user_id][4] <= 0:
            return False
        else:
            return True

    def __overdraft_acc_charge(self, user_id):
        """
        This method check if it's needed to charge it transaction inside
        Checking Accounts looking for an Overdraft. And if not, it tells
        the client how much more money the Checking Account has available
        befor crossing the '-100' line!
        """
        if self.__bank_users_data[user_id][3] < 0:
            self.__bank_users_data[user_id][3] -= 35.0
            self.__bank_users_data[user_id][5] += 1
        else:
            available = float(100) + float(self.__bank_users_data[user_id][3])
            print(f"\nYou have {available} available to withdraw!\n")

    def __overdraft_blocker_acc(self, user_id):
        """
        A simple method that check if the Client's data has a Counter
        bigger then 1, that is always accressed when crossing the line
        of Overdraft! It returns True or False, so it can be called as
        a condition inside other methods, and if it's False, the Account
        is blocked!
        """
        if self.__bank_users_data[user_id][5] > 1:
            return False
        else:
            return True
    def __overdraft_blocker_nuller(self, user_id):
        """
        This method nulls the methods above, it checks again if our
        client's account is negative, if not, sets the Overdraft Counter
        to 0, unlocking the Client's Checking Account!
        """
        if self.__bank_users_data[user_id][3] > 0:
            self.__bank_users_data[user_id][5] = 0
        else:
            print("\nYou need to quit your debts to unlok account!\n")

    def __wrong_operation_acc(self, user_id):
        """
        A method that check if the user is doing a wrong operation, if
        the target friend's user ID does Checking Account is seted to
        None, it will return False, otherwise True. This help us to call
        this function inside the transactional methods and create
        conditions, if False, we send the money to the Savings Account!
        """
        if self.__bank_users_data[user_id][3] == None:
            return False
        else:
            return True
    def __wrong_operation_sav(self, user_id):
        """
        It's the same as above, but for Savings Account. If False, it'll
        send the money to the friends Checking Account!
        """
        if self.__bank_users_data[user_id][4] == None:
            return False
        else:
            return True


    check = property(__check_content)
    data_dic = property(__data_to_dic)
    new_file = property(__new_file)
    login = property(__log_in)
    new_user = property(__add_new_user)
    from_acc_collect = property(__withdraw_from_acc)
    from_savings_collect = property(__withdraw_from_savings)
    deposit_into_acc = property(__deposit_in_acc)
    deposit_into_savings = property(__deposit_in_savings)
    from_user_acc_to_sav = property(__deposit_from_acc_to_savings)
    from_user_sav_to_acc = property(__collect_from_savings_to_acc)
    from_user_acc_to_friends_acc = property(__transfer_from_acc_to_another_acc)
    from_user_sav_to_friends_acc = property(__transfer_from_savings_to_another_acc)
    from_user_acc_to_friends_sav = property(__transfer_from_acc_to_another_savings)
    from_user_sav_to_friends_sav = property(__transfer_from_savings_to_another_savings)
    get_hist = property(__print_hist)


class User:
    """
    This class is almost a copy and paste from the previously Bank Class, but
    with no power to create new users, or to check other Accounts!
    It was modfied for User needs! 
    - It can change password!
    """
    def __init__(self):
        """
        Now it starts with the log-in, so everything is done inside one
        account only, and to access another account the code would need
        to run again!
        """
        users_id = input("\nWelcome, please incert your ID here:\n->")
        users_fst_name = input("\nSafety question: what's your First Name?\n->")
        users_lst_name = input("\nSafety question: what's your Last Name?\n->")
        users_pwd = input("\nSafety question: what's your password?\n->")
        self.__users_id = users_id
        self.__users_fst_name = users_fst_name
        self.__users_lst_name = users_lst_name
        self.__users_pwd = users_pwd
        self.__file_name = 'bank.csv'
        self.__bank_users_data = {}
        self.__bank_users_hist = {}
        self.bank_user_dic = {}
        self.__file_of_hist = Path("bank_history.csv")
        self.__counter = 0
        User.__data_to_dic(self)
        User.__log_in(self)
        User.__acme_layout(self)
        self.special_characteries = re.compile('"?!@#%&*_{[\<|>/]}:;,.¹²³£¢¬ªº°')

    # These methods beneath are related to data handling!
    
    def __data_to_dic(self):
        """
        The same as the Bank class
        """

        bank_info = []
        special_characteries = re.compile('"?!@#%&*_{[\<|>/]}:;,.¹²³£¢¬ªº°')

        try:
            files = open(self.__file_name,'r')

            for line in files:
                
                bank_raw_info = (line.strip()).split(';')
                
                bank_raw_info = [x.strip() for x in bank_raw_info]
                
                bank_info.append(bank_raw_info)
                
            for user in range(len(bank_info)):
                
                user_list = bank_info[user]
                
                for index in range(len(user_list)):
                    
                    element = user_list[index]
    
                    account_id = user_list[0]

                    if (special_characteries.search(user_list[1]) == None):
                        first_name = user_list[1]
                    else:
                        raise TypeError("--> !!! CONTACT BANK, \
                            SOMETHING WRONG !!! <--")
                    
                    if (special_characteries.search(user_list[2]) == None):
                        last_name = user_list[2]
                    else:
                        raise TypeError("\n\t--> !!! CONTACT BANK, \
                            SOMETHING WRONG WITH USER NAME !!! <--\n")
                    
                    if user_list[3].isalpha():
                        raise TypeError("\n\t--> !!! CONTACT BANK, \
                            SOMETHING WRONG WITH USER PASSWORD !!! <--\n")
                    else:
                        password = str(user_list[3])

                    balance_checking = float(user_list[4])
                    balance_savings = float(user_list[5])
                    
                    try:
                        block_counter = int(user_list[6])
                    except:
                        block_counter = 0

                    self.__bank_users_data[account_id] = [
                        first_name, last_name, password, 
                        balance_checking, balance_savings, block_counter
                        ]
                    # making it public at the same time...
                    self.bank_user_dic[account_id] = [
                        first_name, last_name, password, 
                        balance_checking, balance_savings, block_counter
                        ]
                    # making some history
                    if self.__file_of_hist.is_file():
                        User.__data_hist_to_dic(self)
                    else:
                        hist = {}
                        self.__bank_users_hist[account_id] = [
                            first_name, last_name, hist
                        ]
                    # hist = {}
                    # self.__bank_users_hist[account_id] = [
                    #     first_name, last_name, hist
                    # ]
            User.__new_file(self)
            return f'\n{self.__bank_users_data}\n'
            
            files.close()
        except IOError:
            print('\nThe file inputed does not exist inside folder!\n')
    
    def __new_file(self):
        """
        The same as Bank Class!
        """
        #self.__counter += 1
        new_file_name = (
            self.__file_name[:-4] + '.py'
        )
        try:
            new_file = open(new_file_name, 'w')
            new_file.write('user_data = {}'.format(self.__bank_users_data))
            #print("\nNew File Created!\n")
            new_file.close()
        except IOError:
            print('\nThis file already exists in folder!\n')
    
    def __update_file(self):
            """
            The same as the Bank Class!
            """
            #self.__counter += 1
            # new_file_name = (
            #     self.__file_name[:-4] + '.py'
            # )
                # update_file = open('bank_1.csv', 'w')
                # update_file.write('{}'.format(self.__bank_users_data))
            
            try:
                with open('bank.csv', 'w') as f:
                    for key in self.__bank_users_data.keys():
                        f_name = self.__bank_users_data[key][0]
                        l_name = self.__bank_users_data[key][1]
                        pwd = self.__bank_users_data[key][2]
                        acc = self.__bank_users_data[key][3]
                        sav = self.__bank_users_data[key][4]
                        flag = self.__bank_users_data[key][5]
                        f.write("%s;%s;%s;%s;%s;%s;%s\n"%(key,f_name,l_name,pwd,acc,sav,flag))
                
                #print("\nNew data Updated!\n")
                f.close()
            except IOError:
                print('\nFile could not Update!\n')
    
    def __transaction_hist(self, users_id, amount, action):
        """
        The same as the bank class!
        """
        times = time.now()
        h_time = times.strftime("%c")
        h_amount = amount
        h_action = action
        report = f"Transaction of {h_amount} from {h_action}"
        h = self.__bank_users_hist[self.__users_id][2]
        h[h_time] = [report]
        clean_report = f"Transaction of {h_amount} from {h_action} at {h_time}"
        print("Your receit:", clean_report)
        User.__update_hist_file(self)
        return f'\n{self.__bank_users_hist}\n'
        
    def __data_hist_to_dic(self):
        """
        The same as the Bank Class!
        """
        bank_h_info = []
        try:
            files = open(self.__file_of_hist,'r')
            for line in files:
                bank_h_raw_info = (line.strip()).split(';')
                bank_h_raw_info = [x.strip() for x in bank_h_raw_info]
                bank_h_info.append(bank_h_raw_info)
                
            for user_h in range(len(bank_h_info)):
                user_h_list = bank_h_info[user_h]
                
                for i in range(len(user_h_list)):
                    element = user_h_list[i]
                    account_id = user_h_list[0]
                    first_name = user_h_list[1]
                    last_name = user_h_list[2]
                    hist = eval(user_h_list[3])
                    self.__bank_users_hist[account_id] = [
                        first_name, last_name, hist
                    ]
            User.__update_hist_file(self)
            return f'\n{self.__bank_users_hist}\n'
            
            files.close()

        except IOError:
            print('\nThe file inputed does not exist inside folder!\n')

    def __update_hist_file(self):
        """
        The same as the Bank Class!
        """
        try:
            with open('bank_history.csv', 'w') as d:
                for key in self.__bank_users_hist.keys():
                    f_name = self.__bank_users_hist[key][0]
                    l_name = self.__bank_users_hist[key][1]
                    hst = self.__bank_users_hist[key][2]
                    d.write("%s;%s;%s;%s\n"%(key,f_name,l_name,hst))
            
            #print("\nNew History data Updated!\n")
            d.close()
        except IOError:
            print('\nHistory File could not Update!\n')

    def __acme_layout(self):
        """
        Similar to the bank class, but there's no need to check our
        client's credentials!
        """
        u_a = self.__bank_users_data[self.__users_id][1]
        print("\n")
        print("#####################")
        print(f"_____{u_a}'s Accounts_____")
        print("#####################")
        print("||||||__ACME__|||||||\n")
        return f"\n#####################\n||||||__{u_a}'s Accounts__|||||||\n#####################"
        
    def __print_hist(self):
        """
        Almost the same as the Bank class, but without the extra Log-in!
        """
        if self.__file_of_hist.is_file():
            User.__data_hist_to_dic(self)
            p1 = self.__bank_users_hist[self.__users_id][2]
            
            for key in p1:
                p2 = p1[key]
                print(key,p2[0])
        else:
            for key in p1:
                p2 = p1[key]
                print(key,p2[0])
        #     else:
        #         print("Wrong credentials!")
        #         return "Wrong credentials!"
        # else:
        #     print("Wrong credentials!")
        #     return "Wrong credentials!"
            
    def __change_password(self):
        """
        This method is exclusive for this User Class, and allows our
        client to change its own password!
        """
        action_done = None
        User.__acme_layout(self)
        if User.__log_in(self) == True:
            new_pwd = input("What's your new password?\n->")
            if new_pwd.isalpha():
                action_done = False
                print("\nWeak password!\nRequest denied!\nLog-in again!\n")
            else:
                self.__bank_users_data[self.__users_id][2] = new_pwd
                u_activity = "--Changing Password--"
                action_done = True
                if action_done == True:
                    action = "User Request!"
                    User.__transaction_hist(self, self.__users_id, u_activity, action)
                    User.__update_hist_file(self)
                    User.__new_file(self)
                    User.__update_file(self)
                else:
                    u_activity = "Changing Password DENIED!"
                    action = "User Request DENIED!"
                    User.__transaction_hist(self, self.__users_id, u_activity, action)
                    User.__update_hist_file(self)
            return f"\nNew password requested!\n"
        else:
            print("\nWrong credentials! Try again!\n")
            return f"\nWrong credentials! Try again!\n"
    
    # These methods beneath are related to money transactions!
    
    def __withdraw_from_acc(self):
        """
        The only difference from these methods beneath here, from the
        methods of the Bank Class, is that we do a different type of
        log-in!
        """
        action_done = None
        amount = float(input("How much you want to be collected?\n->"))
        User.__acme_layout(self)
        if User.__log_in(self) == True:
            if User.__wrong_operation_acc(self, self.__users_id) != False:
                if User.__overdraft_blocker_acc(self, self.__users_id) != False:
                    if User.__overdraft_protection_acc(self, self.__users_id) != False:
                        self.__bank_users_data[self.__users_id][3] -= amount
                        if User.__overdraft_protection_acc(self, self.__users_id) != False:
                            User.__overdraft_acc_charge(self, self.__users_id)
                            User.__new_file(self)
                            User.__update_file(self)
                            a = self.__bank_users_data[self.__users_id][3]
                            print("\nTransaction succeeded!")
                            print(f"\n{amount} was collected from yours Checking Account!")
                            print(f"\nYour Checking Account currently holds: {a}\n")
                            action_done = True
                            if action_done == True:
                                action = "Checking Account withdraw"
                                User.__transaction_hist(self, self.__users_id, amount, action)
                                User.__update_hist_file(self)
                            return f"\nTransaction succeeded!\n{amount} was collected from yours Checking Account!\nYour Checking Account currently holds: {a}\n"
                        else:
                            self.__bank_users_data[self.__users_id][3] += amount
                            a = self.__bank_users_data[self.__users_id][3]
                            print("\nTransaction denied!")
                            print("\nYou cannot have a depbt over -100,00!")
                            print(f"\n{amount} was sturned to yours Checking Account!")
                            print(f"\nYour Checking Account currently holds: {a}\n")
                            action_done = False
                            if action_done == False:
                                action = "Checking Account withdraw DENIED!"
                                User.__transaction_hist(self, self.__users_id, amount, action)
                                User.__update_hist_file(self)
                            return f"\nTransaction denied!\n{amount} was sturned to yours Savings Account!\nYou cannot have less then 00,00 in your saving account!\nYour Savings Account currently holds: {a}\n"
                    else:
                        print("\nToo many overdrafts in this account! Operation denied!\n")
                else:
                    print("\nAccount is blocked by too many overdrafts!\n")
            else:
                print("\nThis saving account cannot do this operation, \
                first you need to create a checking account!\n")
        else:
            print("\nWrong credentials, try again!\n")
        
    def __withdraw_from_savings(self):
        action_done = None
        amount = float(input("How much you want to be collected?\n->"))
        User.__acme_layout(self)
        if User.__log_in(self) == True:
            if User.__overdraft_protection_savings(self, self.__users_id) != False:
                self.__bank_users_data[self.__users_id][4] -= amount
                if User.__overdraft_protection_savings(self, self.__users_id) != False:
                    User.__new_file(self)
                    User.__update_file(self)
                    b = self.__bank_users_data[self.__users_id][4]
                    print("\nTransaction succeeded!")
                    print(f"\n{amount} was collected from yours Savings Account!")
                    print(f"\nYour Savings Account currently holds: {b}\n")
                    action_done = True
                    if action_done == True:
                        action = "Savings Account withdraw"
                        User.__transaction_hist(self, self.__users_id, amount, action)
                    return f"\nTransaction succeeded!\n{amount} was collected from yours Savings Account!\nYour Savings Account currently holds: {b}\n"
                else:
                    self.__bank_users_data[self.__users_id][4] += amount
                    b = self.__bank_users_data[self.__users_id][4]
                    print("\nTransaction denied!")
                    print("\nYou cannot have less then 00,00 in your saving account!")
                    print(f"\n{amount} was sturned to yours Savings Account!")
                    print(f"\nYour Savings Accounts currently holds: {b}\n")
                    action_done = False
                    if action_done == False:
                        action = "Checking Account withdraw DENIED!!!"
                        User.__transaction_hist(self, self.__users_id, amount, action)
                    return f"\nTransaction denied!\n{amount} was sturned to yours Savings Account!\nYou cannot have less then 00,00 in your saving account!\nYour Savings Account currently holds: {b}\n"
            else:
                print("\nThere is no money in your savings account!\n")
        else:
            print("\nWrong credentials, try again!\n")

    def __deposit_in_acc(self):
        action_done = None
        user_id = input("\nPlease, incert our client's User ID here:\n->")
        f_name = input("\nPlease, incert our client first name:\n->")
        l_name = input("\nPlease, incert our client last name:\n->")
        amount = float(input("\nHow much do you want to deposit?\n->"))
        User.__acme_layout(self)
        if user_id in self.__bank_users_data:
            if self.__bank_users_data[user_id][0] == f_name:
                if self.__bank_users_data[user_id][1] == l_name:
                    if User.__wrong_operation_acc(self, user_id) != False:
                        self.__bank_users_data[user_id][3] += amount
                        User.__overdraft_blocker_nuller(self, user_id)
                        User.__new_file(self)
                        User.__update_file(self)
                        a = self.__bank_users_data[user_id][0]
                        print(f"\n{amount} was deposited to {a}'s account!\n")
                        action_done = True
                        if action_done == True:
                                action = "Depositing into Checking Account"
                                User.__transaction_hist(self, user_id, amount, action)
                        return f"\n{amount} was deposited to {a}'s account!\n"
                    else:
                        self.__bank_users_data[user_id][4] += amount
                        User.__new_file(self)
                        User.__update_file(self)
                        a = self.__bank_users_data[user_id][0]
                        print(f"\n{amount} was deposited to {a}'s account!\n")
                        action_done = False
                        if action_done == False:
                                action = "Depositing into Savings Account"
                                User.__transaction_hist(self, user_id, amount, action)
                        return f"\n{amount} was deposited to {a}'s account!\n"
                else:
                    print("\nWrong user information provided! Try Again!\n")
            else:
                print("\nWrong user information provided! Try Again!\n")
        else:
            print("\nUser not found!\n")

    def __deposit_in_savings(self):
        action_done = None
        user_id = input("\nPlease, incert our client's User ID here:\n->")
        f_name = input("\nPlease, incert our client first name:\n->")
        l_name = input("\nPlease, incert our client last name:\n->")
        amount = float(input("\nHow much you want to deposit?\n->"))
        User.__acme_layout(self)
        if user_id in self.__bank_users_data:
            if self.__bank_users_data[user_id][0] == f_name:
                if self.__bank_users_data[user_id][1] == l_name:
                    if User.__wrong_operation_sav(self, user_id) != False:
                        self.__bank_users_data[user_id][4] += amount
                        User.__new_file(self)
                        User.__update_file(self)
                        a = self.__bank_users_data[user_id][0]
                        print(f"\n{amount} was deposited to {a}'s account!\n")
                        action_done = True
                        if action_done == True:
                                action = "Depositing into Savings Account"
                                User.__transaction_hist(self, user_id, amount, action)
                        return f"\n{amount} was deposited to {a}'s account!\n"
                    else:
                        self.__bank_users_data[user_id][3] += amount
                        User.__new_file(self)
                        User.__update_file(self)
                        a = self.__bank_users_data[user_id][0]
                        print(f"\n{amount} was deposited to {a}'s account!\n")
                        action_done = False
                        if action_done == False:
                                action = "Depositing into Checking Account"
                                User.__transaction_hist(self, user_id, amount, action)
                        return f"\n{amount} was deposited to {a}'s account!\n"
                else:
                    print("\nWrong user information provided! Try Again!\n")
            else:
                print("\nWrong user information provided! Try Again!\n")
        else:
            print("\nUser not found!\n")

    def __deposit_from_acc_to_savings(self):
        action_done = None
        amount = float(input("\nHow much you want to be transfered into your Savings Account?\n->"))
        User.__acme_layout(self)
        if User.__log_in(self) == True:
            if User.__wrong_operation_acc(self, self.__users_id) != False:
                if User.__wrong_operation_sav(self, self.__users_id) != False:
                    if User.__overdraft_blocker_acc(self, self.__users_id) != False:
                        if User.__overdraft_protection_acc(self, self.__users_id) != False:
                            self.__bank_users_data[self.__users_id][3] -= amount
                            if User.__overdraft_protection_acc(self, self.__users_id) != False:
                                self.__bank_users_data[self.__users_id][4] += amount
                                User.__overdraft_acc_charge(self, self.__users_id)
                                #print(self.__bank_users_data[self.__users_id])
                                User.__new_file(self)
                                User.__update_file(self)
                                a = self.__bank_users_data[self.__users_id][3]
                                b = self.__bank_users_data[self.__users_id][4]
                                print(f"\n{amount} was transfered from your Checking Account to your Savings Account!\n")
                                print(f"\nTransaction succeeded!\nYou currently have {a} in your Checking Account, \nand {b} in your Savings Account!\n")
                                action_done = True
                                if action_done == True:
                                    action = "Transfering from Checking Account to Savings Account"
                                    User.__transaction_hist(self, self.__users_id, amount, action)
                                return f"\nYou currently have {a} in your Checking Account, \nand {b} in your Savings Account!\n"
                            else:
                                self.__bank_users_data[self.__users_id][3] += amount
                                a = self.__bank_users_data[self.__users_id][3]
                                b = self.__bank_users_data[self.__users_id][4]
                                print("\nTransaction denied, you cannot have a depbt over -100,00\n")
                                print(f"\n{amount} was storned to your Checking Account!\n")
                                action_done = False
                                if action_done == False:
                                    action = "Transfering from Checking Account to Savings Account DENIED!!!"
                                    User.__transaction_hist(self, self.__users_id, amount, action)
                                return f"\nYou currently have {a} in your Checking Account, \nand {b} in your Savings Account!\n"
                        else:
                            print("\nToo many overdrafts in this account! Operation denied!\n")
                    else:
                        print("\nAccount is blocked by too many overdrafts!\n")
                else:
                    print("\nThis checking account cannot do this operation, \
                    You do not have a savings account!\n")
            else:
                print("\nThis saving account cannot do this operation, \
                You do not have a checking account!\n")
        else:
            print("\nWrong credentials, try again!\n")

    def __collect_from_savings_to_acc(self):
        action_done = None
        amount = float(input("\nHow much you want to be transfered to your Checking Account?\n->"))
        User.__acme_layout(self)
        if User.__log_in(self) == True:
            if User.__wrong_operation_sav(self, self.__users_id) != False:
                if User.__wrong_operation_acc(self, self.__users_id) != False:
                    if User.__overdraft_protection_savings(self, self.__users_id) != False:
                        self.__bank_users_data[self.__users_id][4] -= amount
                        if User.__overdraft_protection_savings(self, self.__users_id) != False:
                            self.__bank_users_data[self.__users_id][3] += amount
                            User.__overdraft_blocker_nuller(self, self.__users_id)
                            #print(self.__bank_users_data[self.__users_id])
                            User.__new_file(self)
                            User.__update_file(self)
                            a = self.__bank_users_data[self.__users_id][3]
                            b = self.__bank_users_data[self.__users_id][4]
                            print(f"\n{amount} was transfered from your Savings Account to your Checking Account!\n")
                            print(f"\nTransaction succeeded!\nYou currently have {a} in your Checking Account, \nand {b} in your Savings Account!\n")
                            action_done = True
                            if action_done == True:
                                action = "Transfering from Savings Account to Checking Account"
                                User.__transaction_hist(self, self.__users_id, amount, action)
                            return f"\nYou currently have {a} in your Checking Account, \nand {b} in your Savings Account!\n"
                        else:
                            self.__bank_users_data[self.__users_id][4] += amount
                            a = self.__bank_users_data[self.__users_id][3]
                            b = self.__bank_users_data[self.__users_id][4]
                            print("\nTransaction denied, you cannot have less then 00,00 in your saving account!\n")
                            print(f"\n{amount} was storned to your Savings Account!\n")
                            action_done = False
                            if action_done == False:
                                action = "Transfering from Savings Account to Checking Account DENIED!!!"
                                User.__transaction_hist(self, self.__users_id, amount, action)
                            return f"\nYou currently have {a} in your Checking Account, \nand {b} in your Savings Account!\n"
                    else:
                        print("\nTransaction denied, you cannot have less then 00,00 in your saving account!\n")
                else:
                    print("\nThis saving account cannot do this operation, \
                    You do not have a checking account!\n")
            else:
                print("\nThis checking account cannot do this operation, \
                You do not have a savings account!\n")
        else:
            print("\nWrong credentials, try again!\n")

    def __transfer_from_acc_to_another_acc(self):
        action_done = None
        friend_id = input("\nPlease, incert your Friend's User ID here:\n->")
        f_name = input("\nPlease, incert your Friend's first name:\n->")
        fl_name = input("\nPlease, incert your Friend's last name:\n->")
        amount = float(input("\nHow much you want to be transfered?\n->"))
        User.__acme_layout(self)
        if User.__log_in(self) == True:
            if User.__wrong_operation_acc(self, self.__users_id) != False:
                if User.__overdraft_blocker_acc(self, self.__users_id) != False:
                    if User.__overdraft_protection_savings(self, self.__users_id) != False:
                        if friend_id in self.__bank_users_data:
                            if self.__bank_users_data[friend_id][0] == f_name:
                                if self.__bank_users_data[friend_id][1] == fl_name:
                                    self.__bank_users_data[self.__users_id][3] -= amount
                                    if User.__overdraft_protection_acc(self, self.__users_id) != False:
                                        if User.__wrong_operation_acc(self, friend_id) != False:
                                            self.__bank_users_data[friend_id][3] += amount
                                            User.__overdraft_acc_charge(self, self.__users_id)
                                            print(f"\n{amount} was subtracted from your Checking Account!\n")
                                            # print(self.__bank_users_data[self.__users_id])
                                            a = self.__bank_users_data[self.__users_id][3]
                                            b = self.__bank_users_data[self.__users_id][4]
                                            print(f"\n{amount} was transfered from your Checking Account to your Savings Account!\n")
                                            print(f"\nTransaction succeeded!\nYou currently have {a} in your Checking Account, \nand {b} in your Savings Account!\n")
                                            User.__new_file(self)
                                            User.__update_file(self)
                                            action_done = True
                                            if action_done == True:
                                                action = f"Transfering from Checking Account to {f_name}'s Account"
                                                User.__transaction_hist(self, self.__users_id, amount, action)
                                            return "\nOperation succeeded!\n"
                                        else:
                                            self.__bank_users_data[friend_id][4] += amount
                                            User.__overdraft_acc_charge(self, self.__users_id)
                                            print(f"\n{amount} was subtracted from your Checking Account!\n")
                                            # print(self.__bank_users_data[self.__users_id])
                                            a = self.__bank_users_data[self.__users_id][3]
                                            b = self.__bank_users_data[self.__users_id][4]
                                            print(f"\n{amount} was transfered from your Checking Account to your Savings Account!\n")
                                            print(f"\nTransaction succeeded!\nYou currently have {a} in your Checking Account, \nand {b} in your Savings Account!\n")
                                            User.__new_file(self)
                                            User.__update_file(self)
                                            action_done = False
                                            if action_done == False:
                                                action = f"Transfering from Checking Account to {f_name}'s Account"
                                                User.__transaction_hist(self, self.__users_id, amount, action)
                                            return "\nOperation succeeded!\n"
                                    else:
                                        self.__bank_users_data[self.__users_id][3] += amount
                                        print("\nTransaction denied, you cannot have a depbt over -100,00\n")
                                        print(f"\n{amount} was storned to your Checking Account!\n")
                                        # print(self.__bank_users_data[self.__users_id])
                                        a = self.__bank_users_data[self.__users_id][3]
                                        b = self.__bank_users_data[self.__users_id][4]
                                        print(f"\n{amount} was transfered from your Checking Account to your Savings Account!\n")
                                        print(f"\nTransaction succeeded!\nYou currently have {a} in your Checking Account, \nand {b} in your Savings Account!\n")
                                        if action_done == None:
                                            action = "Checking Account withdraw DENIED!"
                                            User.__transaction_hist(self, self.__users_id, amount, action)
                                        return "\nOperation denied!\n"
                                else:
                                    print("\nWrong user information provided! Try Again!\n")
                            else:
                                print("\nWrong user information provided! Try Again!\n")
                        else:
                            print("\nUser not found!\n")
                    else:
                        print("\nTransaction denied, you cannot have less then 00,00 in your saving account!\n")
                else:
                    print("\nAccount is blocked by too many overdrafts!\n")
            else:
                print("\nThis saving account cannot do this operation, \
                You do not have a checking account!\n")
        else:
            print("\nWrong credentials, try again!\n")
    
    def __transfer_from_savings_to_another_acc(self):
        action_done = None
        friend_id = input("\nPlease, incert your Friend's User ID here:\n->")
        f_name = input("\nPlease, incert your Friend's first name:\n->")
        fl_name = input("\nPlease, incert your Friend's last name:\n->")
        amount = float(input("\nHow much you want to be transfered?\n->"))
        User.__acme_layout(self)
        if User.__log_in(self) == True:
            if User.__wrong_operation_sav(self, self.__users_id) != False:
                if User.__overdraft_protection_savings(self, self.__users_id) != False:
                    if friend_id in self.__bank_users_data:
                        if self.__bank_users_data[friend_id][0] == f_name:
                            if self.__bank_users_data[friend_id][1] == fl_name:
                                self.__bank_users_data[self.__users_id][4] -= amount
                                if User.__overdraft_protection_savings(self, self.__users_id) != False:
                                    if User.__wrong_operation_acc(self, friend_id) != False:
                                        self.__bank_users_data[friend_id][3] += amount
                                        print(f"\n{amount} was subtracted from your Savings Account!\n")
                                        # print(self.__bank_users_data[self.__users_id])
                                        a = self.__bank_users_data[self.__users_id][3]
                                        b = self.__bank_users_data[self.__users_id][4]
                                        print(f"\n{amount} was transfered from your Checking Account to your Savings Account!\n")
                                        print(f"\nTransaction succeeded!\nYou currently have {a} in your Checking Account, \nand {b} in your Savings Account!\n")
                                        User.__new_file(self)
                                        User.__update_file(self)
                                        action_done = True
                                        if action_done == True:
                                            action = f"Transfering from Savings Account to {f_name}'s Account"
                                            User.__transaction_hist(self, self.__users_id, amount, action)
                                        return "\nOperation succeeded!\n"
                                    else:
                                        self.__bank_users_data[friend_id][4] += amount
                                        print(f"\n{amount} was subtracted from your Savings Account!\n")
                                        # print(self.__bank_users_data[self.__users_id])
                                        a = self.__bank_users_data[self.__users_id][3]
                                        b = self.__bank_users_data[self.__users_id][4]
                                        print(f"\n{amount} was transfered from your Checking Account to your Savings Account!\n")
                                        print(f"\nTransaction succeeded!\nYou currently have {a} in your Checking Account, \nand {b} in your Savings Account!\n")
                                        User.__new_file(self)
                                        User.__update_file(self)
                                        action_done = False
                                        if action_done == False:
                                            action = f"Transfering from Saving Account to {f_name}'s Account"
                                            User.__transaction_hist(self, self.__users_id, amount, action)
                                        return "\nOperation succeeded!\n"
                                else:
                                    self.__bank_users_data[self.__users_id][4] += amount
                                    print("\nTransaction denied, you cannot have less then 00,00 in your saving account!\n")
                                    print(f"\n{amount} was storned to your Savings Account!\n")
                                    # print(self.__bank_users_data[self.__users_id])
                                    a = self.__bank_users_data[self.__users_id][3]
                                    b = self.__bank_users_data[self.__users_id][4]
                                    print(f"\n{amount} was transfered from your Checking Account to your Savings Account!\n")
                                    print(f"\nTransaction succeeded!\nYou currently have {a} in your Checking Account, \nand {b} in your Savings Account!\n")
                                    if action_done == None:
                                        action = "Savings Account withdraw DENIED!"
                                        User.__transaction_hist(self, self.__users_id, amount, action)
                                    return "\nOperation denied!\n"
                            else:
                                print("\nWrong user information provided! Try Again!\n")
                        else:
                            print("\nWrong user information provided! Try Again!\n")
                    else:
                        print("\nUser not found!\n")
                else:
                    print("\nYou do not have money in your saving account!\n")
            else:
                print("\nThis checking account cannot do this operation, \
                You do not have a savings account!\n")
        else:
            print("\nWrong credentials, try again!\n")

    def __transfer_from_acc_to_another_savings(self):
        action_done = None
        friend_id = input("\nPlease, incert your Friend's User ID here:\n->")
        f_name = input("\nPlease, incert your Friend's first name:\n->")
        fl_name = input("\nPlease, incert your Friend's last name:\n->")
        amount = float(input("\nHow much you want to be transfered?\n->"))
        User.__acme_layout(self)
        if User.__log_in(self) == True:
            if User.__wrong_operation_acc(self, self.__users_id) != False:
                if User.__overdraft_blocker_acc(self, self.__users_id) != False:
                    if User.__overdraft_protection_savings(self, self.__users_id) != False:
                        if friend_id in self.__bank_users_data:
                            if self.__bank_users_data[friend_id][0] == f_name:
                                if self.__bank_users_data[friend_id][1] == fl_name:
                                    self.__bank_users_data[self.__users_id][3] -= amount
                                    if User.__overdraft_protection_acc(self, self.__users_id) != False:
                                        if User.__wrong_operation_sav(self, friend_id) != False:
                                            self.__bank_users_data[friend_id][4] += amount
                                            User.__overdraft_acc_charge(self, self.__users_id)
                                            print(f"\n{amount} was subtracted from your Checking Account!\n")
                                            # print(self.__bank_users_data[self.__users_id])
                                            a = self.__bank_users_data[self.__users_id][3]
                                            b = self.__bank_users_data[self.__users_id][4]
                                            print(f"\n{amount} was transfered from your Checking Account to your Savings Account!\n")
                                            print(f"\nTransaction succeeded!\nYou currently have {a} in your Checking Account, \nand {b} in your Savings Account!\n")
                                            User.__new_file(self)
                                            User.__update_file(self)
                                            action_done = True
                                            if action_done == True:
                                                action = f"Transfering from Checking Account to {f_name}'s Account"
                                                User.__transaction_hist(self, self.__users_id, amount, action)
                                            return "\nOperation succeeded\n"
                                        else:
                                            self.__bank_users_data[friend_id][4] += amount
                                            User.__overdraft_acc_charge(self, self.__users_id)
                                            print(f"\n{amount} was subtracted from your Checking Account!\n")
                                            # print(self.__bank_users_data[self.__users_id])
                                            a = self.__bank_users_data[self.__users_id][3]
                                            b = self.__bank_users_data[self.__users_id][4]
                                            print(f"\n{amount} was transfered from your Checking Account to your Savings Account!\n")
                                            print(f"\nTransaction succeeded!\nYou currently have {a} in your Checking Account, \nand {b} in your Savings Account!\n")
                                            User.__new_file(self)
                                            User.__update_file(self)
                                            action_done = False
                                            if action_done == False:
                                                action = f"Transfering from Checking Account to {f_name}'s Account"
                                                User.__transaction_hist(self, self.__users_id, amount, action)
                                            return "\nOperation succeeded\n"
                                    else:
                                        self.__bank_users_data[self.__users_id][3] += amount
                                        print("\nTransaction denied, you cannot have a depbt over -100,00\n")
                                        print(f"\n{amount} was storned to your Savings Account!\n")
                                        # print(self.__bank_users_data[self.__users_id])
                                        a = self.__bank_users_data[self.__users_id][3]
                                        b = self.__bank_users_data[self.__users_id][4]
                                        print(f"\n{amount} was transfered from your Checking Account to your Savings Account!\n")
                                        print(f"\nTransaction succeeded!\nYou currently have {a} in your Checking Account, \nand {b} in your Savings Account!\n")
                                        if action_done == None:
                                            action = "Checking Account withdraw DENIED!"
                                            User.__transaction_hist(self, self.__users_id, amount, action)
                                        return "\nOperation denied!\n"
                                else:
                                    print("\nWrong user information provided! Try Again!\n")
                            else:
                                print("\nWrong user information provided! Try Again!\n")
                        else:
                            print("\nUser not found!\n")
                    else:
                        print("\nToo many overdrafts in this account! Operation denied!\n")
                else:
                    print("\nAccount is blocked by too many overdrafts!\n")
            else:
                print("\nThis saving account cannot do this operation, \
                You do not have a checking account!\n")
        else:
            print("\nWrong credentials, try again!\n")
    
    def __transfer_from_savings_to_another_savings(self):
        action_done = None
        friend_id = input("\nPlease, incert your Friend's User ID here:\n->")
        f_name = input("\nPlease, incert your Friend's first name:\n->")
        fl_name = input("\nPlease, incert your Friend's last name:\n->")
        amount = float(input("\nHow much you want to be transfered?\n->"))
        User.__acme_layout(self)
        if User.__log_in(self) == True:
            if User.__wrong_operation_sav(self, self.__users_id) != False:
                if User.__overdraft_protection_savings(self, self.__users_id) != False:
                    if friend_id in self.__bank_users_data:
                        if self.__bank_users_data[friend_id][0] == f_name:
                            if self.__bank_users_data[friend_id][1] == fl_name:
                                self.__bank_users_data[self.__users_id][4] -= amount
                                if User.__overdraft_protection_savings(self, self.__users_id) != False:
                                    if User.__wrong_operation_sav(self, friend_id) != False:
                                        self.__bank_users_data[friend_id][4] += amount
                                        print(f"\n{amount} was subtracted from your Savings Account!\n")
                                        # print(self.__bank_users_data[self.__users_id])
                                        a = self.__bank_users_data[self.__users_id][3]
                                        b = self.__bank_users_data[self.__users_id][4]
                                        print(f"\n{amount} was transfered from your Checking Account to your Savings Account!\n")
                                        print(f"\nTransaction succeeded!\nYou currently have {a} in your Checking Account, \nand {b} in your Savings Account!\n")
                                        User.__new_file(self)
                                        User.__update_file(self)
                                        action_done = True
                                        if action_done == True:
                                            action = f"Transfering from Savings Account to {f_name}'s Account"
                                            User.__transaction_hist(self, self.__users_id, amount, action)
                                        return "\nOperation succeeded\n"
                                    else:
                                        self.__bank_users_data[friend_id][3] += amount
                                        print(f"\n{amount} was subtracted from your Savings Account!\n")
                                        # print(self.__bank_users_data[self.__users_id])
                                        a = self.__bank_users_data[self.__users_id][3]
                                        b = self.__bank_users_data[self.__users_id][4]
                                        print(f"\n{amount} was transfered from your Checking Account to your Savings Account!\n")
                                        print(f"\nTransaction succeeded!\nYou currently have {a} in your Checking Account, \nand {b} in your Savings Account!\n")
                                        User.__new_file(self)
                                        User.__update_file(self)
                                        action_done = False
                                        if action_done == False:
                                            action = f"Transfering from Savings Account to {f_name}'s Account"
                                            User.__transaction_hist(self, self.__users_id, amount, action)
                                        return "\nOperation succeeded\n"
                                else:
                                    self.__bank_users_data[self.__users_id][4] += amount
                                    print(f"\n{amount} was storned to your Savings Account!\n")
                                    print("\nTransaction denied, you cannot have less then 00,00 in your saving account!\n")
                                    # print(self.__bank_users_data[self.__users_id])
                                    a = self.__bank_users_data[self.__users_id][3]
                                    b = self.__bank_users_data[self.__users_id][4]
                                    print(f"\n{amount} was transfered from your Checking Account to your Savings Account!\n")
                                    print(f"\nTransaction succeeded!\nYou currently have {a} in your Checking Account, \nand {b} in your Savings Account!\n")
                                    if action_done == None:
                                        action = "Savings Account withdraw DENIED!"
                                        User.__transaction_hist(self, self.__users_id, amount, action)
                                    return "\nOperation denied!\n"
                            else:
                                print("\nWrong user information provided! Try Again!\n")
                        else:
                            print("\nWrong user information provided! Try Again!\n")
                    else:
                        print("\nUser not found!\n")
                else:
                    print("\nToo many overdrafts in this account! Operation denied!\n")
            else:
                print("\nThis saving account cannot do this operation, \
                first you need to create a savings account!\n")
        else:
            print("\nWrong credentials, try again!\n")
    
    #Every thing from here it's related to security!
    
    def __log_in(self):
        print("\n||ACME's Sacurity||")
        print("---Log-in required!---")
        user_pass = input("\nPlease, confirm your Password to complete action:\n->")
        
        if self.__users_id in self.__bank_users_data:
            #print("User ID found!")
            if self.__users_fst_name in self.__bank_users_data[self.__users_id]:
                #print('First Name correct!')
                if self.__users_lst_name in self.__bank_users_data[self.__users_id]:
                    #print('Last Name correct')
                    if user_pass in self.__bank_users_data[self.__users_id]:
                        if user_pass == self.__users_pwd:
                            #print(self.__bank_users_data[self.__users_id])
                            return True
        else:
            return False

    def __overdraft_protection_acc(self, users_id):
        if self.__bank_users_data[self.__users_id][3] == -100:
            return False
        else:
            return True
    def __overdraft_protection_savings(self, users_id):
        if self.__bank_users_data[self.__users_id][4] <= 0:
            return False
        else:
            return True

    def __overdraft_acc_charge(self, users_id):
        if self.__bank_users_data[self.__users_id][3] < 0:
            self.__bank_users_data[self.__users_id][3] -= 35.0
            self.__bank_users_data[self.__users_id][5] += 1
        else:
            available = float(100) + float(self.__bank_users_data[self.__users_id][3])
            print(f"\nYou have {available} available to withdraw!\n")

    def __overdraft_blocker_acc(self, _users_id):
        if self.__bank_users_data[self.__users_id][5] > 1:
            return False
        else:
            return True
    def __overdraft_blocker_nuller(self, users_id):
        if self.__bank_users_data[self.__users_id][3] > 0:
            self.__bank_users_data[self.__users_id][5] = 0
        else:
            print("\nYou need to quit your debts to unlok account!\n")

    def __wrong_operation_acc(self, users_id):
        if self.__bank_users_data[self.__users_id][3] == None:
            return False
        else:
            return True
    def __wrong_operation_sav(self, _users_id):
        if self.__bank_users_data[self.__users_id][4] == None:
            return False
        else:
            return True


    # data_dic = property(__data_to_dic)
    # new_file = property(__new_file)
    # login = property(__log_in)
    from_acc_collect = property(__withdraw_from_acc)
    from_savings_collect = property(__withdraw_from_savings)
    deposit_into_acc = property(__deposit_in_acc)
    deposit_into_savings = property(__deposit_in_savings)
    from_user_acc_to_sav = property(__deposit_from_acc_to_savings)
    from_user_sav_to_acc = property(__collect_from_savings_to_acc)
    from_user_acc_to_friends_acc = property(__transfer_from_acc_to_another_acc)
    from_user_sav_to_friends_acc = property(__transfer_from_savings_to_another_acc)
    from_user_acc_to_friends_sav = property(__transfer_from_acc_to_another_savings)
    from_user_sav_to_friends_sav = property(__transfer_from_savings_to_another_savings)
    get_hist = property(__print_hist)
    change_pwd = property(__change_password)

z = Bank()
z.new_user
z.deposit_into_acc
z.deposit_into_savings
# z.from_user_acc_to_sav
# z.from_savings_collect
# z.from_acc_collect
# z.from_acc_collect
# z.from_acc_collect
# z.from_acc_collect
# z.from_user_sav_to_acc
# z.from_acc_collect
# z.from_user_sav_to_friends_sav
# z.from_user_sav_to_friends_acc
# z.from_user_acc_to_friends_acc
# z.from_user_acc_to_friends_sav
z.get_hist
# z.get_hist

k = User()
k.from_acc_collect
k.deposit_into_acc
k.deposit_into_savings
# k.from_acc_collect
# k.from_acc_collect
# k.from_acc_collect
# k.from_user_sav_to_acc
# k.from_acc_collect
# k.from_user_acc_to_friends_acc
# k.from_user_acc_to_friends_sav
# k.from_user_sav_to_friends_acc
# k.from_user_sav_to_friends_sav
# k.get_hist
k.change_pwd
k.get_hist