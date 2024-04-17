// 搜尋欄
document.addEventListener('DOMContentLoaded', function() {
    var searchForm = document.getElementById('searchForm');
    var searchInput = document.getElementById('searchInput');

    searchForm.addEventListener('submit', function(event) {
        event.preventDefault();

        var searchTerm = encodeURIComponent(searchInput.value);
        var redirectUrl = '/movie-search/' + searchTerm;

        searchForm.action = redirectUrl;
        searchForm.submit();
    });
});




// 閱讀更多按鈕
document.addEventListener('DOMContentLoaded', function() {
    var readMoreButtons = document.querySelectorAll('.btn-readmore');

    readMoreButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault();

            var id = button.getAttribute('data-movie-id');

            var movieId = encodeURIComponent(id);
            var redirectUrl = '/movie/readmore/' + movieId;

            // 將瀏覽器導向到新的URL
            window.location.href = redirectUrl;
        });
    });
});

// 查看更多(演員)按鈕
document.addEventListener('DOMContentLoaded', function() {
    var readMoreButtons = document.querySelectorAll('.btn-secondary');

    readMoreButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault();

            var id = button.getAttribute('castId');

            var castId = encodeURIComponent(id);
            var redirectUrl = '/cast/' + castId;

            // 將瀏覽器導向到新的URL
            window.location.href = redirectUrl;
        });
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const bannerWrap = document.querySelector('.banner .banner-wrap');
    const posters = bannerWrap.querySelectorAll('img');
    let totalWidth = 0;

    // 复制第一张海报并添加到末尾
    posters.forEach(poster => {
    const posterClone = poster.cloneNode(true);
      bannerWrap.appendChild(posterClone);
  });

    // 计算所有海报和间距的总宽度
    posters.forEach(poster => {
        totalWidth += poster.offsetWidth + 10; // 每张海报间距为 10px
    });
    
    // 设置动画
    bannerWrap.style.animation = `banner-slider 180s infinite linear`; // 将动画时间从 60s 增加到 120s

    // 定义动画关键帧
    const keyframes = `@keyframes banner-slider {
      0% { transform: translate3d(0, 0, 0); }
      100% { transform: translate3d(-${totalWidth}px, 0, 0); }
  }`;

    // 将动画关键帧添加到页面
    const styleSheet = document.createElement("style");
    styleSheet.type = "text/css";
    styleSheet.innerText = keyframes;
    document.head.appendChild(styleSheet);
});


