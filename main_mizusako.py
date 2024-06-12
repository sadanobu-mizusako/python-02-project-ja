from abc import ABC, abstractmethod

# Interface for storage
class IStorage(ABC):
    @abstractmethod
    def save_account(self, account):
        pass

    @abstractmethod
    def get_account(self, id):
        pass

    @abstractmethod
    def delete_account(self, id):
        pass

# Interface for user interaction
class IUserInteraction(ABC):
    @abstractmethod
    def get_input(self):
        pass

    @abstractmethod
    def show_info(self, info):
        pass

# Account class
class Account:
    def __init__(self, uid, uname, balance):
        self.id = uid
        self.uname = uname
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if self.balance < amount:
            raise ValueError('Insufficient balance')
        self.balance -= amount

    def transfer(self, to_account, amount):
        if self.balance < amount:
            raise ValueError('Insufficient balance')
        self.balance -= amount
        to_account.balance += amount

# Storage implementation using built-in data structure
class Storage(IStorage):
    def __init__(self):
        self.data = {}

    def save_account(self, account):
        self.data[account.id] = account

    def get_account(self, id):
        return self.data.get(id)

    def delete_account(self, id):
        if id in self.data:
            del self.data[id]

# User interaction implementation using command line
class CommandLineInteraction(IUserInteraction):
    def get_input(self):
        return input()

    def show_info(self, info):
        print(info)

# Main Application
class Application(Storage, CommandLineInteraction):
    max_id = 0 # ユーザーIDが重複しないように最大のIDを保持
    current_account = None # ログイン済みのアカウントオブジェクトを保持

    def create_account(self, uname, balance):
        """
        アカウントの新規作成を行う
        """
        uid = str(self.max_id)
        self.max_id += 1
        account = Account(uid, uname, balance)
        self.save_account(account)
        self.show_info(f'Account {account.id} is created.')
        return account
    
    def account_signin_up(self):
        """
        既存アカウントへのサインインまたは新規アカウントの作成を行う
        アカウントサインイン後、または、新規アカウントの作成後、
        self.current_accountに当該アカウントを割り当てる
        """
        pass

    def handle_user_input(self):
        while True:
            self.show_info("Enter command: \n 1: deposit \n 2: withdraw \n 3: transfer \n 4: exit \n 5: delete account")
            command = self.get_input()
            if command=='1':
                pass
            elif command=='2':
                pass
            elif command=='3':
                pass
            elif command=='4':
                pass
            elif command=='5':
                break
            else:
                pass # エラーメッセージを出力

if __name__ == '__main__':
    # システムの起動
    app = Application()
    
    # 送金先アカウントの作成
    app.create_account("mizusako", 1000)
    app.create_account("tanaka", 1000)
    app.create_account("mike", 1000)

    # 以降はインタラクティブな操作

    # アカウントへのログイン
    ## 1. 既存のアカウントにログイン
    ## 2. 新規アカウントの作成
    app.account_signin_up()

    # ログインしたアカウントでの操作
    ## 1. 入金
    ## 2. 出金
    ## 3. 送金
    ## 4. ログアウト
    ## 5. 解約
    app.handle_user_input()
