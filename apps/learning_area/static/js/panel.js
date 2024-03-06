function deletePanelShow(){
    $('#phase').on('click', 'li .delete-panel', function(){
        $('#deletePanelModal').modal('show');
        let start = $(this).closest('li').attr('start');
        let end = $(this).closest('li').attr('end');
        let url = $('#filmUrl').attr('src');
        DELETE_ITEM = {'start': start,
                       'end': end,
                       'url': url,
        };
    });
  }

  function deletePanel(){
    $('#deletePanelConfirm').click(function(){
      // 發送ajax請求
      $.ajax({
        url: "/learning/",
        type: "post",
        data: {'DELETE_ITEM': DELETE_ITEM},
        dataType: "JSON",
        success: function(res){
          if(res.status){
            /* 在前端頁面中把該筆記板標籤刪除 */
            let start = res.start;
            let end = res.end;
            $('li[start="' + start + '"][end="' + end + '"]').remove();

            /* 在緩存中刪除該筆筆記板資料 */
            let notes = JSON.parse(localStorage.getItem('lastWatchedVideoNotes')) || {}; // 拿到localStorage裡lastWatchedVideoNotes這個key的值(或空的object)
            delete notes[res.deleted_file_name.replace(/;/g, ':')]; 

            // 也在緩存中刪除該筆數據
            localStorage.setItem('lastWatchedVideoNotes', JSON.stringify(notes));

            $('#deletePanelModal').modal('hide');         
          }else{
            console.log(res.error)
            $('#deletePanelModal').modal('hide');
          }
        }
    })
  });
  }