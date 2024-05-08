$(document).ready(function() {

    var page = 2;
  
    var loadingData = false;
  
  
  
  
    function loadPosts() {
  
  if (!loadingData) {
  
    loadingData = true;
  
    $('.loading').show();
  
    $.ajax({
  
      url: '?page=' + page,
  
      type: 'GET',
  
      success: function(data) {
  
        if (data.posts.length > 0) {
  
          var row = $('<div class="row">');
  
          var postsPerRow = 4;
  
          var postsCount = 0;
  
          for (var i = 0; i < data.posts.length; i++) {
  
            var col = $('<div class="col-sm-3 mb-5">').html(data.posts[i]);
  
            row.append(col);
  
            postsCount++;
  
            if (postsCount === postsPerRow) {
  
              $('.posts-container').append(row);
  
              row = $('<div class="row">');
  
              postsCount = 0;
  
            }
  
          }
  
          if (postsCount > 0) {
  
            $('.posts-container').append(row);
  
          }
  
          page++;
  
        } else {
  
          $(window).off('scroll', handleScroll);
  
        }
  
        loadingData = false;
  
        $('.loading').hide();
  
      },
  
      error: function() {
  
        loadingData = false;
  
        $('.loading').hide();
  
      }
  
    });
  
  }
  
  }
  
  
  
  
    function handleScroll() {
  
      var scrollHeight = $(document).height();
  
      var scrollPosition = $(window).height() + $(window).scrollTop();
  
      if ((scrollHeight - scrollPosition) / scrollHeight <= 0.1) {
  
        loadPosts();
  
      }
  
    }
  
  
  
  
    $(window).on('scroll', handleScroll);
  
  });