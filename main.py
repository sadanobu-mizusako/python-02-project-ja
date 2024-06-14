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
    def __init__(self, uid, uname, balance, password):
        self.id = uid
        self.uname = uname
        self.balance = balance
        self.__password = password
    
    def __getter_password(self):
        """
        安全にパスワードにアクセスするためにgetterを設定
        """
        return self.__password
    
    def authenticate_account(self, password):
        """
        パスワードの認証を行うための関数。ユーザーが入力したパスワードが正しければTrueを返す
        """
        return self.__getter_password()==password

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
    def __init__(self):
        super().__init__() # 親クラスの初期化タスク実行
        self.max_id = 0 # ユーザーIDが重複しないように最大のIDを保持
        self.current_account = None # ログイン済みのアカウントオブジェクトを保持

    def create_account(self, uname, balance, password):
        """
        アカウントの新規作成を行う
        """
        uid = str(self.max_id)
        self.max_id += 1
        account = Account(uid, uname, balance, password)
        self.save_account(account)
        self.show_info(f'アカウント {account.id} が作成されました。')
        return account
    
    def account_signin_up(self):
        """
        既存アカウントへのサインインまたは新規アカウントの作成を行う
        アカウントサインイン後、または、新規アカウントの作成後、
        self.current_accountに当該アカウントを割り当てる
        """
        while True:
            self.show_info("オプションを選択してください:\n 1. 既存のアカウントにログイン\n 2. 新規アカウントの作成")
            option = self.get_input()
            if option == '1':
                self.show_info("アカウントIDを入力してください:")
                account_id = self.get_input()
                account = self.get_account(account_id)
                if account:
                    self.current_account = account
                    if self.authenticate_account(account):
                        #パスワード認証に成功した場合ループから抜ける
                        self.show_info(f'{account.uname}としてサインインしました。')
                        break
                    else:
                        #パスワード認証に失敗した場合ループを継続する
                        pass
                else:
                    self.show_info("アカウントが見つかりません。")
            elif option == '2':
                self.show_info("名前を入力してください:")
                uname = self.get_input()
                self.show_info("初期残高を入力してください:")
                balance = float(self.get_input())
                self.show_info("パスワードを入力してください:")
                password = self.get_input()
                self.current_account = self.create_account(uname, balance, password)
                break
            else:
                self.show_info("無効なオプションです。再度選択してください。")
                #self.account_signin_up()

    def handle_user_input(self):
        while True:
            self.show_info("Enter command: \n 1: 入金 \n 2: 出金 \n 3: 送金 \n 4: ログアウト \n 5: 解約 \n 6: 口座情報")
            command = self.get_input()
            if command == '1':
                self.show_info("Enter amount to deposit:")
                amount = float(self.get_input())
                self.current_account.deposit(amount)
                self.show_info(f'New balance: {self.current_account.balance}')
            elif command == '2':
                self.show_info("Enter amount to withdraw:")
                amount = float(self.get_input())
                try:
                    self.current_account.withdraw(amount)
                    self.show_info(f'New balance: {self.current_account.balance}')
                except ValueError as e:
                    self.show_info(str(e))
            elif command == '3':
                self.show_info("Enter recipient account ID:")
                recipient_id = self.get_input()
                recipient = self.get_account(recipient_id)
                if recipient:
                    self.show_info("Enter amount to transfer:")
                    amount = float(self.get_input())
                    try:
                        self.current_account.transfer(recipient, amount)
                        self.show_info(f'Transfer successful. New balance: {self.current_account.balance}')
                    except ValueError as e:
                        self.show_info(str(e))
                else:
                    self.show_info("Recipient account not found.")
            elif command == '4':
                self.current_account = None
                self.show_info("Signed out.")
                break
            elif command == '5':
                account_id = self.current_account.id
                self.delete_account(account_id)
                self.show_info(f'Account {account_id} deleted.')
                self.current_account = None
                break
            elif command == '6':
                self.show_info(f'Account ID: {self.current_account.id}\nUsername: {self.current_account.uname}\nBalance: {self.current_account.balance}')
            else:
                self.show_info("Invalid command.")

    def wants_to_exit(self):
        while True:
            self.show_info("システムを終了しますか？: \n 1: システムを終了する \n 2: 他のアカウントで操作を継続する")
            command = self.get_input()
            if command=='1':
                return True
            elif command=='2':
                return False
            else:
                self.show_info("Invalid command.")
    
    def authenticate_account(self, account):
        """
        アカウントのパスワード認証を行う関数
        """
        self.show_info("パスワードを入力してください: ")
        password = self.get_input()
        if account.authenticate_account(password):
            self.show_info("認証に成功しました。")
            return True
        else:
            self.show_info("認証に失敗しました。")
            return False

if __name__ == '__main__':
    # システムの起動
    app = Application()
    
    # 送金先アカウントの作成
    app.create_account("mizusako", 1000, "password")
    app.create_account("tanaka", 1000, "password")
    app.create_account("mike", 1000, "password")

    # 以降はインタラクティブな操作
    while True:
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
        ## 6. 口座情報
        app.handle_user_input()

        # アプリ操作を継続するかの確認
        # 1. 終了
        # 2. 他のアカウントで継続
        if app.wants_to_exit():
            break
