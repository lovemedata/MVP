<script src="https://www.youtube.com/iframe_api"></script> //用youtube_api可須引入這個
/* 沒有用成功, 但是如果會使用youtube_api的話應該可以很好的操控影片, 未來有需要再研究出來吧 
可以操作秒數到要到達的地方, 也可以獲取時間影片的長度和embedded url */


let player;

    function onYouTubeIframeAPIReady() {
        player = new YT.Player('filmUrl', {
            playerVars: { 'autoplay': 1,
                          'enablejsapi': 1,
                          'origin': 'https://www.youtube.com', },
            events: { 'onReady': onPlayerReady },
        });
    }

    function onPlayerReady(event) {
        player.getDuration();
        player.seekTo(100); 
    }