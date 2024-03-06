import re

def yt_conversion(yt_url):
    # https://youtu.be/D7RfX84uFHw -> 這種類型的也要把它弄成可以解析
    embed_yt_url = yt_url.replace('watch?v=', 'embed/')
    if '&' in embed_yt_url:
        # 如果是從播放清單找影片過來的就需要再做這個處理
        index_of_mark = embed_yt_url.find("&")
        embed_yt_url = embed_yt_url[:index_of_mark]
    return embed_yt_url
    
def bili_conversion(bili_url):
    if '?p=' in bili_url: 
        # 從播放清單獲取的url
        index_of_question_mark = bili_url.find("?")
        single_digit = bili_url[index_of_question_mark+3]
        double_digit = bili_url[index_of_question_mark+3:index_of_question_mark+5]
        triple_digit = bili_url[index_of_question_mark+3:index_of_question_mark+6]
        quadruple_digit = bili_url[index_of_question_mark+3:index_of_question_mark+7]
        if quadruple_digit.isdecimal():
            episode = '&p=' + quadruple_digit
        elif triple_digit.isdecimal():
            episode = '&p=' + triple_digit
        elif double_digit.isdecimal():
            episode = '&p=' + double_digit
        else:
            episode = '&p=' + single_digit
        
        bili_url = bili_url[:index_of_question_mark]
        
        if bili_url.endswith('/'):
            # 去掉最後的/, 以符合嵌入式url的格式
            bili_url = bili_url[:len(bili_url)-1]
            
        embed_bili_url = bili_url.replace('www', 'player')
        embed_bili_url = embed_bili_url.replace('video/', 'player.html?bvid=')
        embed_bili_url = embed_bili_url + episode
        
        return embed_bili_url
    
    if '?' in bili_url:
        # 不是從播放清單獲取的url
        index_of_question_mark = bili_url.find("?")
        bili_url = bili_url[:index_of_question_mark]
    
    if bili_url.endswith('/'):
        # 去掉最後的/, 以符合嵌入式url的格式
        bili_url = bili_url[:len(bili_url)-1]
        
    embed_bili_url = bili_url.replace('www', 'player')
    embed_bili_url = embed_bili_url.replace('video/', 'player.html?bvid=')
    return embed_bili_url

def extract_video_id(url):
    '''從embed url中擷取出video id'''
    # youtube要排除?start={秒數}, B站要排除&t={秒數}的後綴
    # 之後youtube如果有加上要自動播放的參數就是"autoplay=1", 會把他加在秒數控制後面, 所以會是"&autoplay=1"
    
    yt_prefix = 'youtube.com/'
    bili_prefix = 'bilibili.com/'
    yt_suffix = '?start='
    bili_suffix = '&t='
    
    if yt_prefix in url:
        # 此url是YT的
        video_id_with_second = url.split('embed/')[1]
        if yt_suffix not in video_id_with_second:
            # 沒有秒數後綴訊息
            return video_id_with_second
        
        regex = r"\?start=(\d+)&autoplay=1"
        video_id = re.sub(regex, '', video_id_with_second)
        return video_id
    
    if bili_prefix in url:
        # 此url是B站的
        video_id_with_second = url.split('bvid=')[1]
        if bili_suffix not in video_id_with_second:
            # 沒有秒數後綴訊息
            return video_id_with_second
        
        regex = r"&t=\d+"
        video_id = re.sub(regex, '', video_id_with_second)
        return video_id
        
    return None
    
# result = bili_conversion('https://www.bilibili.com/video/BV1KK41167mH?p=42&vd_source=3dd15bae5592d893117773fb400ee427')
# print(result) 

# result = yt_conversion('https://www.youtube.com/watch?v=GMIvi795p2I')
# print(result)

# video_id = extract_video_id(result)
# print(video_id)