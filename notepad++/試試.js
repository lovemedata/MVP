function timeOrder(){
      // 將段落重點的筆記板項目依時間先後做排序
      // 排序規則: 先比對終了時間，越前面的在越上面
      //          若終了時間相同，則比對起始時間，越前面的在越上面

      // Select all <li> tags inside the <ul> with id "phase"
      $('#timeSort').click(function(){
        var lis = $("#phase li");
    
        // Sort the <li> tags based on the end attribute, and then the start attribute if end attributes are equal
        lis.sort(function(a, b) {
            var end1 = parseInt($(a).attr("end"));
            var end2 = parseInt($(b).attr("end"));
            
            if (end1 !== end2) {
                return end1 - end2; // Sort by end attribute
            } else {
                var start1 = parseInt($(a).attr("start"));
                var start2 = parseInt($(b).attr("start"));
                return start1 - start2; // Sort by start attribute if end attributes are equal
            }
        });
        // Append the sorted <li> tags back to the <ul> with id "phase"
        $("#phase").empty().append(lis);
      });
    }