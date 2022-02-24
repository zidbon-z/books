$('.poop-btn').click(function(e){
  e.preventDefault();
  var poopid;
  poopid = $(this).attr("poop-id");

    $.ajax({
      type:'POST',
      url : '{% url 'main:adder' %}',
      data:{
          poop: poopid,
          csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
      },
      success: function(html){
          $( '#poop'+ poopid ).hide();
          $( '#poop-added'+ poopid ).append("Added");
          
      
      },
    });
});
