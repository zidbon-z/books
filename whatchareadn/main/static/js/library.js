
// Change the shelf that a book belongs to
$(document).on('change', '.book-shelf', function(e) {
  e.preventDefault();
  var googleid;
  var shelfname;
  googleid = $(this).attr("googleid");
  //shelfn = $(this).attr("value");
  select = (document).getElementById('book-shelf'+googleid);
  shelfn = select.options[select.selectedIndex].value;
    $.ajax({
        type:'POST',
        url :'/library/change_shelf/',
        data:{
            bookid: googleid,
            shelfn: shelfn,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function(html){
            getShelf();
        },
    });
});

// Change the shelf that is being displayed
function getShelf() {
  var shelf;
  shelf = document.getElementById('select-shelf').value;
  library = document.getElementById('library-body');

  $.ajax({
    type: 'POST',
    url: '/library/shelf/',
    data:{
      shelf: shelf,
      csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
    },
    success: function(response){
      console.log(response);
      document.getElementById('library-body').innerHTML = "";
      var temp2 = "";
      var shelfoptions = "";
      var shelfname = "";

      for (var shelf in response.shelves)
      {
          var shelfoption='<option value="'+response.shelves[shelf].name+'">'+response.shelves[shelf].name+'</option>'
          shelfoptions = (shelfoptions + shelfoption)
      }
      for (var book in response.books)
      {
          for (var she in response.shelves)
          {
              if (response.shelves[she].id === response.books[book].shelf_id){
                  var shelfname = response.shelves[she].name;
              }
          }

          var selfshelf = '<option value="'+shelfname+'">'+shelfname+'</option>'
          var shelfselect = (selfshelf + shelfoptions)
          var temp= '<div class="card" id="book'+response.books[book].googleid+'">' +
                      '<a id="card-link" class="detail-btn" btn-id="'+response.books[book].googleid+'" href="#">' +
                        '<div class="card-img-box">' +
                          '<img src="'+response.books[book].image_link+'" />' +
                        '</div>' +
                      '</a>' +
                      '<div class="card-body">' +
                        '<h3 class="card-title">'+response.books[book].title+'</h3>' +
                        '<div class="button-row">' +
                          '<label for="book-shelf">Shelf</label>' +
                          '<select id="book-shelf'+response.books[book].googleid+'" class="book-shelf" googleid="'+response.books[book].googleid+'" name="book-shelf" onchange="getShelf()">'+shelfselect+'</select>' +
                          '<button class="read-btn" butt-id="'+response.books[book].googleid+'">Read Book</button>' +
                          '<button class="del-btn" butt-id="'+response.books[book].googleid+'">Delete Book</button>' +
                        '</div>' +
                      '</div>' +
                    '</div>';
                   
          temp2 = (temp2 + temp);
          document.getElementById('library-body').innerHTML = temp2;
          //window.location.reload();
      }
    }
  });

};

// Exit the detail modal
$('.back-btn').click(function(){
  document.getElementsByTagName('BODY')[0].style.overflow = "auto";
  //document.getElementById('search-body').style.position = "relative";
  document.getElementById('modal').style.visibility = "hidden";
});

// Show the detail modal for the selected card
$(document).on('click', '.detail-btn', function(e) {
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
      console.log(response);

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

// Delete card from database
$(document).on('click', '.del-btn', function(e) {
  e.preventDefault();
  var buttid;
  buttid = $(this).attr("butt-id");

    $.ajax({
        type:'POST',
        url :'/library/delete_book/',
        data:{
            buttid: buttid,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function(html){
            document.getElementById('book' + buttid).remove();
        },
    });
});

// Show edit card modal
function showEditCard() {
  document.getElementsByTagName('BODY')[0].style.overflow = "hidden";
  document.getElementById('edit-shelf').style.visibility = "visible";
}

// Hide edit card modal, reset select box, and hide delete button
function hideEditCard() {
  selectElement = document.getElementById('del-shel-sel');
  selectElement.selectedIndex = 0;

  document.getElementById('del-shel-btn').style.display = "none";
  document.getElementsByTagName('BODY')[0].style.overflow = "auto";
  document.getElementById('edit-shelf').style.visibility = "hidden";

}

function showDelete() {
  document.getElementById('del-shel-btn').style.display = "initial";

}

function deleteShelf() {
  deletedShelf = document.getElementById('del-shel-sel').value;
  console.log(deletedShelf);
    $.ajax({
        type:'POST',
        url :'/library/delete_shelf/',
        data:{
            deletedShelf: deletedShelf,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function(){
            selectElement = document.getElementById('del-shel-sel');
            selectElement.selectedIndex = 0;
            document.getElementById('del-shel-btn').style.display = "none";
            window.location.reload();

        },
    });
}
