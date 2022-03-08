$(document).ready(function(){

// add book to library and display "added" label
  $('.search-add-btn').click(function(e){
    e.preventDefault();
    var addid;
    addid = $(this).attr("search-add-id");

      $.ajax({
        type:'POST',
        url : '/search/add_book/',
        data:{
            addid: addid,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function(html){
            $( '#search-add'+ addid ).hide();
            $( '#search-book-added'+ addid ).append("Added");
            document.getElementById( 'search-book-added'+ addid ).style.display = "block";
        },
      });
  });

// Show detail when image is clicked
  $('.detail-btn').click(function(e){
    e.preventDefault();
    var btnid;
    btnid = $(this).attr("btn-id");

    $.ajax({
      type: 'POST',
      url: '/book_detail/',
      data:{
        btnid: btnid,
        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
      },
      success: function(response){
        //console.log(response);

        document.getElementById('detail-card-title').innerHTML = "<strong>Title: </strong>"+response.title;
        document.getElementById('detail-card-authors').innerHTML = "<strong>Authors: </strong>"+response.authors;
        document.getElementById('detail-card-img').src = response.image_link;
        document.getElementById('detail-card-description').innerHTML = response.description;
        document.getElementById('detail-card-publisher').innerHTML = "<strong>Publisher: </strong>"+response.publisher;
        document.getElementById('detail-card-pubdate').innerHTML = "<strong>Date published: </strong>"+response.pubdate;
        document.getElementById('detail-card-isbns').innerHTML = "<strong>ISBNs: </strong>"+response.isbn10+", "+response.isbn13;
        //document.getElementById('search-body').style.position = "fixed";
        document.getElementById('modal').style.visibility = "visible";
        //document.getElementById('library-body').style.display = "none";
        document.getElementsByTagName('BODY')[0].style.overflow = "hidden";
        

      },
    });

  });

// Hide book detail and show page again
  
  $('.back-btn').click(function(){
    document.getElementsByTagName('BODY')[0].style.overflow = "auto";
    //document.getElementById('search-body').style.position = "relative";
    document.getElementById('modal').style.visibility = "hidden";

  });

});
