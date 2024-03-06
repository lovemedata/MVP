import os
from django.http import JsonResponse
from apps.learning_area import models
from django.views.decorators.csrf import csrf_exempt
from apps.learning_area.utils import url_conversion, forms, path, process_time
from django.shortcuts import render, redirect, HttpResponse

@csrf_exempt
def learning(request): 
    if request.method == 'GET':
        film_form = forms.FilmModelForm()
        description_form = forms.Description() 
        context = {
            'film_form': film_form,
            'description_form': description_form,
            } 
        return render(request, 'learning.html', context)
    
    if 'url' in request.POST:
    # 獲取使用者要觀看的影片基本資訊(接收ajax請求)
        form = forms.FilmModelForm(data=request.POST)
        if form.is_valid():
            # 用戶填寫正確, 就獲取填寫的內容
            lecturer = form.cleaned_data.get('lecturer')
            course = form.cleaned_data.get('course')
            url = form.cleaned_data.get('url')
            
            # 創建或查看此url影片的資料夾
            video_id = url_conversion.extract_video_id(url)
            folder_path = path.create_folder(lecturer, course, video_id)
            suffix_name_list = os.listdir(folder_path)
            name_list = [os.path.splitext(name)[0] for name in suffix_name_list]
            file_name_list = [name.replace(';', ':').split('-') for name in name_list]
            start_end_dict = {}              
            for time, description in file_name_list:
                # start_end_dict的 key是檔案名, value是字典, 字典內容為起始跟終止的秒數, 如下所示.
                start, end = time.split('~')
                start = process_time.total_seconds(start)
                end = process_time.total_seconds(end)
                start_end_dict[time + '-' + description] = {'start':start, 'end': end}
            
            context = {'status': True,
                    'lecturer': lecturer,
                    'course': course,
                    'url': url,
                    'start_end_dict': start_end_dict
                    }
            
            
            return JsonResponse(context)
            
        context = {
            'status': False,
            'errors': form.errors
        }
        return JsonResponse(context)

    
    if 'description' in request.POST:
        # 獲取使用者輸入的時間段落描述(接收ajax請求)
        form = forms.Description(data=request.POST)
        if form.is_valid():
            # 用戶填寫正確, 就獲取填寫的內容
            start = form.cleaned_data.get('start')
            end = form.cleaned_data.get('end')
            description = form.cleaned_data.get('description')
            start_time = process_time.total_seconds(start)
            end_time = process_time.total_seconds(end)         
            
            # 進入當前頁面中url影片的資料夾
            film_url = request.POST.get('filmUrl')
            video_id = url_conversion.extract_video_id(film_url)
            folder_path = path.find_path(video_id)
            # 判斷使用者輸入的時段是否已存在
            for file_name in os.listdir(folder_path):
                if start + '~' + end in file_name:
                    context = {'status': 'duplicate',
                               'message': '相同時段筆記板已存在!'}
                    return JsonResponse(context)
            
            # 建立以時段+描述命名的檔案
            note_name = start + '~' + end + '-' + description + '.txt' # 先用文檔表示, 之後要用筆記板的副檔名
            path.make_files(folder_path, note_name)
            
            note_name_display = os.path.splitext(note_name.replace(';', ':'))[0].split('-') # 要傳到前端頁面展示的時段與段落描述的樣式
            
            
            data = { # 拿到時段檔案的名稱列表, 並傳送到後台
                'note_name_display': note_name_display,
                'start_time': start_time,
                'end_time': end_time,
            }
            context = {
                'status': True,
                'data': data,          
            }
            
            return JsonResponse(context)
            
        context = {
            'status': False,
            'errors': form.errors
        }
        return JsonResponse(context)
    
    if 'DELETE_ITEM[start]' in request.POST: # 來自deletePanel發送過來的ajax請求, 試了一下在request.POST的KEY就是這樣
        # 刪除指定的筆記板
        #print(request.POST)
        #print(request.POST['DELETE_ITEM[url]'])
        url = request.POST['DELETE_ITEM[url]']
        start = int(request.POST['DELETE_ITEM[start]'])
        end = int(request.POST['DELETE_ITEM[end]'])
        video_id = url_conversion.extract_video_id(url)
        folder_path = path.find_path(video_id) # 進到當前影片資料夾
        start_time_format = process_time.format_seconds(start).replace(':', ';')
        end_time_format = process_time.format_seconds(end).replace(':', ';')
        file_time_format = start_time_format + '~' + end_time_format # 可以找到要刪除的檔案
        file_name_list = os.listdir(folder_path)
        
        file_deleted = False
        deleted_file_name = None
        for file_name in file_name_list:
            if file_time_format in file_name:
                deleted_file_name = os.path.splitext(file_name)[0]
                file_path = os.path.join(folder_path, file_name)
                os.remove(file_path)
                file_deleted = True
                break
        
        if file_deleted:
            context = {
                'status': True,
                'start': request.POST['DELETE_ITEM[start]'],
                'end': request.POST['DELETE_ITEM[end]'],
                'deleted_file_name': deleted_file_name,
                }
            return JsonResponse(context)
        
        context = {
            'status': False,
            'error': '檔案不存在或已刪除',
        }
        return JsonResponse(context)