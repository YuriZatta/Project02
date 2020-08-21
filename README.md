# ![](https://ga-dash.s3.amazonaws.com/production/assets/logo-9f88ae6c9c3871690e33280fcf557f33.png) Banking With Python

![gif](https://media.giphy.com/media/lptjRBxFKCJmFoibP3/giphy.gif)

| Language | Type          | Date  | Due | Author               |
| -------- | ------------- | ----- | ---- | -------------------- |
| Python   | Project 2 | 6/23/2020 | 7/05/2020 | Yuri |

## What I am proud of:

Everything! It's a freaking Bank App! This app is able to create and handle .csv files that can behave like a real bank and keep the log of the history of your transactions!

## Strugling about my Class choices:

The most hard thing about this project was actually to idealize/interprate what is the proper way to build a safe code for a bank that uses a Child Class! (It was a requirement to create 2 Classes)

My first instinct is to create a class full of private attributes and methods that can only be accessed by the property assignment at the botton. Like that I hope everything is safe and I'm free to change everything later if required, without get in the way of how our users are used to call for our methods. 

I strugled to understand if I'm suppose to build a Bank Class with everything private and then repeat myself copying and pasting all the privates methods inside a User Class. Every day trying to see if I've made the right decision!

So I gave up from using iheritance in this project and I have build 2 different Classes. One for Bank and another for User, but both access the same data-base. And I hope to get closer to what happens in real life this way... 

## The new ACME's file structure `bank.csv`:

```text
User ID;First Name;Last Name;Password;Floating Checking;Floating Savings;Counter_Overdraft
```

| account_id | frst_name | last_name | password | balance_checking | balance_savings| Counter
| -------- | ------------- | ----- | ---- | ---------- |---------- |---------- |
| 10001 | suresh | sigera | juagw362 | 1000.0 | 10000.0 | 0 | 
| 10002 | james | taylor | idh36%@#FGd | -100.0 | 10000.0 | 2 |
| ... | ... | ... | ... | ... | ... | ... |

## What my code does:
This Python project creates and interacts with .csv files to handle bank accounts, it can do everything a bank app can do. It creates a new .csv file to create the transaction log that can be requested by the user!

## User Manual:
### Classes and Files

* 2 classes:
    * _Bank_
    * _User_
* 2 files: 
        `bank.csv`
        `bank_history.csv`

### Class Bank:
1. Add New Customer
     * `new_user = property(__add_new_user)`
     * customer can have a checking account 
     * customer can have a savings account 
     * customer can have both a checking and a savings account 
2. Withdraw Money from Account (required login)
    * withdraw from savings
        * `from_savings_collect = property(__withdraw_from_savings)` 
    * withdraw from checking 
        * `from_acc_collect = property(__withdraw_from_acc)`
3. Deposit Money into Account (required login)
     * can deposit into savings
        * `deposit_into_savings = property(__deposit_in_savings)` 
     * can deposit into checking
        * `deposit_into_acc = property(__deposit_in_acc)` 
4. Transfer Money Between Accounts (required login)
     * can transfer from savings to checking
        * `from_user_sav_to_acc = property(__collect_from_savings_to_acc)` 
     * can transfer from checking to savings
        * `from_user_acc_to_sav = property(__deposit_from_acc_to_savings)` 
     * can transfer from checking or savings to another customer's account
        * `from_user_acc_to_friends_acc = property(__transfer_from_acc_to_another_acc)`
        * `from_user_sav_to_friends_acc = property(__transfer_from_savings_to_another_acc)`
        * `from_user_acc_to_friends_sav = property(__transfer_from_acc_to_another_savings)`
        * `from_user_sav_to_friends_sav = property(__transfer_from_savings_to_another_savings)`

5. Build Overdraft Protection (required login)
     * charge customer ACME overdraft protection fee of $35 when overdrafting
        * `def __overdraft_acc_charge(self, user_id)` 
     * prevent customer from withdrawing more than $100 USD if account is currently negative
        * `def __overdraft_protection_acc(self, user_id)`
        * `def __overdraft_protection_savings(self, user_id)`
     * deactivate the account after 2 overdrafts
        * `def __overdraft_blocker_acc(self, user_id)` 
     * reactivate the account if the customer brings the account current, paying both the overdraft amount and the resulting overdraft fees 
        * `def __overdraft_blocker_nuller(self, user_id)`
6. Display Transaction Data (You need to create another file to store the transaction history, required login)
     * index all transactions for a customer account
        * `def __transaction_hist(self, user_id, amount, action)`
        * `def __update_hist_file(self)`
        * `def __data_hist_to_dic(self)`
     * show one transaction details
        * `clean_report = f"Transaction of {h_amount} from {h_action} at {h_time}"`
     * show historical data of transactions (date and time of transaction, type of transaction, resulting balance, etc.)
        * `get_hist = property(__print_hist)`

### Class User:
1. Change Password!
     * customer can change password!
        * `change_pwd = property(__change_password)` 
     
2. Withdraw Money from Account (required login)
    * withdraw from savings
        * `from_savings_collect = property(__withdraw_from_savings)` 
    * withdraw from checking 
        * `from_acc_collect = property(__withdraw_from_acc)`
3. Deposit Money into Account (required login)
     * can deposit into savings
        * `deposit_into_savings = property(__deposit_in_savings)` 
     * can deposit into checking
        * `deposit_into_acc = property(__deposit_in_acc)` 
4. Transfer Money Between Accounts (required login)
     * can transfer from savings to checking
        * `from_user_sav_to_acc = property(__collect_from_savings_to_acc)` 
     * can transfer from checking to savings
        * `from_user_acc_to_sav = property(__deposit_from_acc_to_savings)` 
     * can transfer from checking or savings to another customer's account
        * `from_user_acc_to_friends_acc = property(__transfer_from_acc_to_another_acc)`
        * `from_user_sav_to_friends_acc = property(__transfer_from_savings_to_another_acc)`
        * `from_user_acc_to_friends_sav = property(__transfer_from_acc_to_another_savings)`
        * `from_user_sav_to_friends_sav = property(__transfer_from_savings_to_another_savings)`

5. Build Overdraft Protection (required login)
     * charge customer ACME overdraft protection fee of $35 when overdrafting
        * `def __overdraft_acc_charge(self, user_id)` 
     * prevent customer from withdrawing more than $100 USD if account is currently negative
        * `def __overdraft_protection_acc(self, user_id)`
        * `def __overdraft_protection_savings(self, user_id)`
     * deactivate the account after 2 overdrafts
        * `def __overdraft_blocker_acc(self, user_id)` 
     * reactivate the account if the customer brings the account current, paying both the overdraft amount and the resulting overdraft fees 
        * `def __overdraft_blocker_nuller(self, user_id)`
6. Display Transaction Data (You need to create another file to store the transaction history, required login)
     * index all transactions for a customer account
        * `def __transaction_hist(self, user_id, amount, action)`
        * `def __update_hist_file(self)`
        * `def __data_hist_to_dic(self)`
     * show one transaction details
        * `clean_report = f"Transaction of {h_amount} from {h_action} at {h_time}"`
     * show historical data of transactions (date and time of transaction, type of transaction, resulting balance, etc.)
        * `get_hist = property(__print_hist)`
## I did it!

![gif](https://media2.giphy.com/media/y3B74VeWI2QQE/giphy.gif)