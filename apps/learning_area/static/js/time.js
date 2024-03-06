function timeDescSave(){
  $('#timeDescSave').click(function(){
      $('.time-desc-error-msg').empty(); // 先把之前輸入錯誤的錯誤訊息清掉
  
  // 獲取當前頁面學習影片的網址
  var filmUrl = $('#filmUrl').attr('src');
  var timeDesc = $("#timeDesc").serializeArray();

  timeDesc.push({name:'filmUrl', value:filmUrl});
  // 用ajax請求把使用者輸入的訊息傳到後台
  $.ajax({
      url: "/learning/",
      type: "post",
      data: timeDesc,
      dataType: "JSON",
      success: function(res){
        if(res.status===true){
          $('#timeDesc')[0].reset(); // 把使用者原本所填欄位的資料清空

          /* 在前端頁面創造這個li標籤 */
          // 創建li標籤, 裡頭包含a和strong標籤
          let li = $('<li>').attr({'start':res.data.start_time, 'end':res.data.end_time})
          let a = $('<a>').attr('href', '#');
          let strong = $('<strong>').attr('class','film-second').text(res.data.note_name_display[0]);
          let notePanelIcon = $('<i>').attr({'class': 'fa-solid fa-pen-to-square note-panel', 'style': 'margin-right:0.3rem;'})
          // 創建p標籤, 並且把它加進上面已經創好的li標籤裡
          let p = $('<p>').attr({'style': 'position:relative;',}).text(res.data.note_name_display[1]);
          let deletePanelIcon = $('<i>').attr({'class': 'fa-solid fa-trash-can delete-panel', 'style': 'position: absolute; bottom: 0; right: 0;'});
          a.append(strong);
          p.append(deletePanelIcon);
          li.append(notePanelIcon);
          li.append(a);
          li.append(p);

          // 把整個li標籤加進ul標籤
          $('#phase').append(li);

          /* 把這個新增的li標籤加到瀏覽器的緩存裡 */
          let notes = JSON.parse(localStorage.getItem('lastWatchedVideoNotes')) || {}; // 拿到localStorage裡lastWatchedVideoNotes這個key的值(或空的object)
          let newNote = {
            'start':res.data.start_time,
            'end':res.data.end_time,
          } 
          notes[res.data.note_name_display[0]+'-'+res.data.note_name_display[1]] = newNote;
          // 把新增的筆記更新到緩存中
          localStorage.setItem('lastWatchedVideoNotes', JSON.stringify(notes));

          }else if(res.status==='duplicate'){ // 輸入的時段已經存在
            alert(res.message);
          }else{
            $.each(res.errors, function(name,errorList){
              $('#id_' + name).next().text(errorList[0]);
          })
        }
      }
  })
});
}

function timeStructure(){
  $('#timeSort').click(function(){  
    var $phase = $("#phase");
    
    // 大時段包含小時段
    var $liItems = $phase.children("li");
    $liItems.each(function() {
        var $currentItem = $(this);
        var currentStart = parseInt($currentItem.attr("start"));
        var currentEnd = parseInt($currentItem.attr("end"));

        $liItems.each(function() {
            var $otherItem = $(this);
            if ($currentItem.is($otherItem)) return; // Skip comparing with itself
            var otherStart = parseInt($otherItem.attr("start"));
            var otherEnd = parseInt($otherItem.attr("end"));

            if (otherStart >= currentStart && otherEnd <= currentEnd) {
                // The other item is completely contained within the current item
                var $subList = $currentItem.children("ul");
                if (!$subList.length) {
                    $subList = $("<ul></ul>");
                    $currentItem.append($subList);
                }
                $subList.append($otherItem);
            }
        });
    });

    // 排序
    var $phase = $("#phase");

    // Sort nested <li> elements within their own layer
    $phase.find('ul').each(function() {
        var $subList = $(this);
        var subLis = $subList.children('li').get();
        subLis.sort(function(a, b) {
            var end1 = parseInt($(a).attr("end"));
            var end2 = parseInt($(b).attr("end"));

            if (end1 !== end2) {
                console.log('sort by end');
                return end1 - end2; // Sort by end attribute
            } else {
                var start1 = parseInt($(a).attr("start"));
                var start2 = parseInt($(b).attr("start"));
                console.log('sort by start');
                return start1 - start2; // Sort by start attribute if end attributes are equal
            }
        });
        $.each(subLis, function(idx, itm) { $subList.append(itm); });
    });

    // Sort the first layer of <li> elements
    var lis = $("#phase > li");

    lis.sort(function(a, b) {
        var end1 = parseInt($(a).attr("end"));
        var end2 = parseInt($(b).attr("end"));

        if (end1 !== end2) {
            console.log('sort by end');
            return end1 - end2; // Sort by end attribute
        } else {
            var start1 = parseInt($(a).attr("start"));
            var start2 = parseInt($(b).attr("start"));
            console.log('sort by start');
            return start1 - start2; // Sort by start attribute if end attributes are equal
        }
    });

    // Reorder the <li> elements in #phase
    $("#phase").empty().append(lis);
});
}

function timeControl(){
  // 點擊段落重點區的時段可以使得影片跳轉至該起始秒數
  $("#phase").on("click", "li .film-second", function(){      
    let url = $("#filmUrl").attr('src');
    let second = $(this).closest('li').attr('start'); 
    let yt = 'youtube';           
    let bili = 'bilibili';
    let urlWithTime;

    if (url.includes(yt)){ 
      // 當前影片來自YT
      let regex = /\?start=(\d+)&autoplay=1/;  // &autoplay=1為自動播放的參數, value=1就是要自動播放
      url = url.replace(regex, '')

      let ytSuffix = '?start='; 
      let autoPlay = '&autoplay=1';
      urlWithTime = url + ytSuffix + second + autoPlay;
      // console.log(urlWithTime);
    }else{
      // 當前影片來自B站
      let regex = /&t=\d+/;
      url = url.replace(regex, '')
      
      let biliSuffix = '&t=';
      urlWithTime = url + biliSuffix + second ;
      // console.log(urlWithTime);
    }

    $("#filmUrl").attr('src', urlWithTime);
  });
}

