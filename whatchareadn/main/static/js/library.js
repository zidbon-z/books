// vim:foldmethod=marker

// Set a book's shelf{{{
// Change the shelf that a book belongs to
$(document).on('change', '.book-shelf', function(e) {
  e.preventDefault();
  // declare variables
  var googleid;
  var shelfname;
  // get the googleid of the book to change it's shelf
  googleid = $(this).attr("googleid");
  // get the shelf dropdown menu from the correct book
  select = (document).getElementById('book-shelf'+googleid);
  // get the value from the shelf dropdown
  shelfn = select.options[select.selectedIndex].value;
    // send the book and the new shelf for the book to the change_shelf view to be changed
    $.ajax({
        type:'POST',
        url :'/library/change_shelf/',
        data:{
            bookid: googleid,
            shelfn: shelfn,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function(html){
            // run the getShelf function to refresh the books and shelves
            getShelf();
        },
    });
});
//}}}

// getShelf function{{{
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

      for (var book in response.books)
      {
          var vol = response.books[book];
          // Create shelf select options for each book
          for (var she in response.shelves)
          {
              var shelf = response.shelves[she];
              if (shelf.id === vol.shelf_id){
                  // get the name of the current book's shelf
                  shelfname = shelf.name;
              }else {
                // generage option elements for all shelves owned by user except the current books shelf
                var shelfoption='<option value="'+shelf.name+'">'+shelf.name+'</option>'
                shelfoptions = (shelfoptions + shelfoption)

              };
          }
          // Create the first option with the current book's shelf
          var selfshelf = '<option value="'+shelfname+'" selected>'+shelfname+'</option>'
          // Combine the current book's shelf option with the list of all the user's other shelves
          var shelfselect = (selfshelf + shelfoptions)
          // Reset shelfoptions so it's empty for the next loop
          shelfoptions = "";

          // Loop through all the current users books and create html to display them
          var temp= '<div class="card" id="book'+vol.googleid+'">' +
                      '<a id="card-link" class="detail-btn" btn-id="'+vol.googleid+'" href="#">' +
                        '<div class="card-img-box">' +
                          '<img src="'+vol.image_link+'" />' +
                        '</div>' +
                      '</a>' +
                      '<div class="card-body">' +
                        '<h3 class="card-title">'+vol.title+'</h3>' +
                        '<div class="button-row">' +
                          '<label for="book-shelf">Shelf</label>' +
                          '<select id="book-shelf'+vol.googleid+'" class="book-shelf" googleid="'+vol.googleid+'" name="book-shelf" onchange="getShelf()">'+shelfselect+'</select>' +
                          '<button class="read-btn" butt-id="'+vol.googleid+'">Read Book</button>' +
                          '<button class="del-btn" butt-id="'+vol.googleid+'">Delete Book</button>' +
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
//}}}

// Detail modal exit button{{{
// Exit the detail modal
$('.back-btn').click(function(){
  document.getElementsByTagName('BODY')[0].style.overflow = "auto";
  //document.getElementById('search-body').style.position = "relative";
  document.getElementById('modal').style.visibility = "hidden";
});
//}}}

// Book detail modal open{{{
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
//}}}

// Delete book{{{
// Delete book from database
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
//}}}

// Open edit modal{{{
// Show edit card modal
function showEditCard() {
  document.getElementsByTagName('BODY')[0].style.overflow = "hidden";
  document.getElementById('edit-shelf').style.visibility = "visible";
}
//}}}

// Edit modal exit button{{{
// Hide edit card modal, reset select box, and hide delete button
function hideEditCard() {
  selectElement = document.getElementById('del-shel-sel');
  selectElement.selectedIndex = 0;

  document.getElementById('del-shel-btn').style.display = "none";
  document.getElementsByTagName('BODY')[0].style.overflow = "auto";
  document.getElementById('edit-shelf').style.visibility = "hidden";
}
//}}}

// Edit modal delete shelf button show{{{
// Show the delete button on the edit card modal
function showDelete() {
  document.getElementById('del-shel-btn').style.display = "initial";
}
//}}}

// Edit modal delete shelf function{{{
// Delete a shelf from the database
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
            getShelf();
            window.location.reload();
        },
    });
}
//}}}

// createShelf function{{{
// Create a new shelf for current user in the database
function createShelf() {
  // get the name of the shelf to be created from the input box
  createdShelf = document.getElementById('new-shelf-name').value;
  console.log(createdShelf);
    // send the name of the shelf to the create_shelf view to be created
    $.ajax({
        type:'POST',
        url :'/library/create_shelf/',
        data:{
            createdShelf: createdShelf,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function(){
            // refresh page
            window.location.reload();
            // reset the new shelf input box
            document.getElementById('new-shelf-name').value = "";
            // run the getShelf function to refresh the books and their shelves
            getShelf();
        },
    });
}
//}}}

// Run getShelf when the page is loaded to initially generate list of books
getShelf()
