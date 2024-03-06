import re
from django.core.exceptions import ValidationError

def check_form(time_string):
    '''檢查用戶輸入的時間格式是否為 'hh:mm:ss' '''
    pattern = r'^\d{2,4}:\d{2}:\d{2}$' # 'hh:mm:ss' 的時間正則表達式
    content = re.match(pattern, time_string)
    if not content:
        # 若用戶輸入非 'hh:mm:ss'
        raise ValidationError("請輸入'hh:mm:ss'的時間格式") 
    
    # 若用戶輸入正確格式
    time_string = content.group()
    time_string = time_string.replace(':', ';') # 命名緣故, 所以把 ":" 換成 ";"
    return time_string

def total_seconds(time_string):
    '''把時間全部用秒計算.
       call這個函數前會先call check_form,
       所以這個的格式校驗就不那麼嚴謹.'''
    if ':' in time_string:
        time_string = time_string.replace(':', ';')
    time_string_list = time_string.split(';')
    time_int_list = []
    for element in time_string_list: 
        # 把string轉換成int
        element = int(element)
        time_int_list.append(element)       
        
    if len(time_string_list) == 3: 
        # 'hh:mm:ss'
        if time_int_list[1] >= 60 or time_int_list[2] >= 60:
            raise ValidationError("分或秒輸入錯誤")
        
        hr_to_sec = time_int_list[0]*3600
        min_to_sec = time_int_list[1]*60
        total_sec = hr_to_sec + min_to_sec + time_int_list[2]
    
    ''' 因為不接受這個格式, 所以這一段不用了
    else: 
        # 'mm:ss'
        if time_int_list[1] >= 60:
            raise ValidationError("秒輸入錯誤")
        
        min_to_sec = time_int_list[0]*60
        total_sec = min_to_sec + time_int_list[1]'''
       
    return total_sec

def format_seconds(seconds):
    ''' 把秒轉換成 "hh:mm:ss" 的時間格式 '''
    hours = seconds // 3600 
    if hours < 10: # hh要用0, 補足至少2位
        hours_str = f"0{hours}"
    else:
        hours_str = str(hours)
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60

    return f"{hours_str}:{minutes:02d}:{remaining_seconds:02d}"