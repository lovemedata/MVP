function filmInfoBtn(){ 
  // 點擊按鈕開啟影片基本資訊彈窗
  $('#filmInfoBtn').click(function(){
    $('#filmInfo')[0].reset(); // 把使用者原本所填欄位的資料清空
    $('.film-error-msg').empty(); // 把之前輸入錯誤的錯誤訊息清掉
    $('#filmInfoModal').modal('show'); // 再顯示彈窗
    });
  }
  
  function filmInfoSave(){
    $('#filmInfoSave').click(function(){
      // 先把之前輸入錯誤的錯誤訊息清掉
      $('.film-error-msg').empty();

      // 用ajax請求把使用者輸入的訊息傳到後台
      $.ajax({
          url: "/learning/",
          type: "post",
          data: $("#filmInfo").serialize(),
          dataType: "JSON",
          success: function(res){
            if(res.status){ 
              $("#phase").empty()
              //填寫正確就在頁面中顯示
              $("#courLectName").text(res.course+"-"+res.lecturer)
              $("#filmUrl").attr('src', res.url)
              
              //把此部影片的資訊儲存到用戶的本地瀏覽器, 以使重新整理以後還可以是這部影片及其相關資訊
              localStorage.setItem('lastWatchedVideoUrl', res.url); // 影片的url
              localStorage.setItem('lastWatchedVideoName', res.course+"-"+res.lecturer) // 課名-講者名
              localStorage.setItem('lastWatchedVideoNotes', JSON.stringify(res.start_end_dict)); // 影片的筆記
              
              // 把url影片對應的資料夾裡面的每一份筆記檔案展示在段落重點區  
              $.each(res.start_end_dict, function(key, value){ 
                nameArray = key.split("-");
                // 創建li標籤, 裡頭包含icon, a和strong標籤
                let li = $('<li>').attr({'start':value.start, 'end':value.end})
                let a = $('<a>').attr('href', '#');
                let strong = $('<strong>').attr('class','film-second').text(nameArray[0]);
                let notePanelIcon = $('<i>').attr({'class': 'fa-solid fa-pen-to-square note-panel', 'style': 'margin-right:0.3rem;'})
                // 創建p標籤, 並且把它加進上面已經創好的li標籤裡
                let p = $('<p>').attr({'style': 'position:relative;',}).text(nameArray[1]);
                let deletePanelIcon = $('<i>').attr({'class': 'fa-solid fa-trash-can delete-panel', 'style': 'position: absolute; bottom: 0; right: 0;'});
                a.append(strong);
                p.append(deletePanelIcon);
                li.append(notePanelIcon);
                li.append(a);
                li.append(p);

                // 把整個li標籤加進ul標籤
                $('#phase').append(li);
              });
              $("#filmInfoModal").modal("hide");

              }else{ 
                // 填寫錯誤就產生錯誤訊息
                $.each(res.errors, function(name,errorList){
                  $('#id_' + name).next().text(errorList[0]);
              })
            }
          }
      })
    });
    }