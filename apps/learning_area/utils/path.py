import os
import send2trash
# C:\Users\admin\Desktop\structure\Server\cust\user_info\email#1\learning
# 開發功能的時候先用這個路徑, 
# 之後有伺服器服務用戶以後, 再依據到時候的位置來修改路徑即可.

COMPUTER_DESK = os.path.join('C:\\', 'Users', 'admin', 'Desktop')
NOTEBOOK_DESK = os.path.join('C:\\', 'Users', 'jerry', 'OneDrive', '桌面')
LEARNING = os.path.join('structure', 'Server', 'cust', 'user_info')
# PATH = os.path.join('C:\\', 'Users', 'admin', 'Desktop', 'structure', 'Server', 'cust', 'user_info') # 所有的用戶到這邊的路徑都一樣
COMPUTER_LEARNING_PATH = os.path.join(COMPUTER_DESK, LEARNING)
NOTEBOOK_LEARNING_PATH = os.path.join(NOTEBOOK_DESK, LEARNING)

USER_EMAIL = os.path.join('email#1', 'learning') # 根據用戶所註冊的email來修改email#1, 也就是email#1要是動態的
USER_COMPUTER_PATH = os.path.join(COMPUTER_LEARNING_PATH, USER_EMAIL) # 到達此用戶學習區用來放置各個影片的筆記空間 -> 一個url對應一個資料夾
USER_NOTEBOOK_PATH = os.path.join(NOTEBOOK_LEARNING_PATH, USER_EMAIL)

def create_folder(lecturer, course, video_id):
    '''在個別用戶的學習區, 創建放置其筆記的資料夾空間'''
    
    exists_entry = os.listdir(USER_NOTEBOOK_PATH)
    for name in exists_entry:
        # 檢查看看此影片是否已經被用戶看過, 若有則不做任何事
        if video_id in name:
            # print('該url已看過')
            exists_folder = os.path.join(USER_NOTEBOOK_PATH, name)
            return exists_folder # 要進入這個已經存在的資料夾, 所以要返回這個路徑
    
    # 如果此url影片沒有被用戶看過, 則創建一個資料夾
    folder_name = lecturer + course + video_id
    new_folder = os.path.join(USER_NOTEBOOK_PATH, folder_name) # 此新創的資料夾的路徑
    os.makedirs(new_folder)
    # print('創建成功')
    return new_folder # 創建成功以後就要進入這個資料夾, 所以要返回這個路徑
    
    # 用戶可能在試用時會丟一些網址試試, 之後再開發要淘汰掉那些的功能.
    # 可行的方法如下: 再接收到新一個url之後, 空的資料夾就刪除.
    
def find_path(partial_name, start_path=USER_NOTEBOOK_PATH):
    ''' 有一部分的檔案/資料夾名, 就找出它的路徑 '''
    for root, dirs, files in os.walk(start_path):
        for dir_name in dirs:
            if partial_name in dir_name:
                return os.path.join(root, dir_name)
                
def make_files(folder_path, file_name):
    ''' 拿到資料夾路徑, 要在該資料夾裡新增檔案 '''
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'w'):
        pass
    return None

def delete_file(file_path):
    ''' 刪除檔案 '''
    try:
        os.remove(file_path)
        print(f"File {file_path} deleted successfully")
    except OSError as e:
        print(f"Error deleting file {file_path}: {e}")
    

    '''   之後做緩存要被刪除的檔案的功能(也就是垃圾桶)再改成這個, os.remove會直接在系統中清除, 難以恢復資料; send2trash則是把東西丟到垃圾桶, 要恢復很簡單.
    try:
        send2trash.send2trash(file_path)
        print(f"File {file_path} sent to recycle bin successfully")
    except OSError as e:
        print(f"Error sending file {file_path} to recycle bin: {e}")'''
