$(function() {

    $('.tagged').each(function(){
        $(this).parent().parent().children(".insight").addClass($(this).attr('color')+"-highlight")
    });



    $('.gr-tag-selector').click(function(){
        $('.insight-box').slideUp(300);
        $('.gr-in-tag'+$(this).attr('tid')).slideDown(300);
        $(this).parent().children().removeClass (function (index, css) {
                    return (css.match (/(^|\s)tagged\S+/g) || []).join(' ');
                }).removeClass("tagged");

        $(this).addClass("tagged")
        $(this).addClass("tagged"+$(this).attr('color'))


        $('.insight-box').removeClass("red-border")
        $('.insight-box').removeClass("purple-border")
        $('.insight-box').removeClass("blue-border")
        $('.insight-box').removeClass("orange-border")
        $('.insight-box').removeClass("green-border")

        $('.insight-box').addClass($(this).attr('color')+"-border")

    });

  $(".tags>span").click(function() {
    $(this).toggleClass('tagged' + $(this).attr('color'));
    $(this).toggleClass('tagged');

    var tagged = $(this).hasClass("tagged");

    $.get("/setTag?tagType=" + $(this).attr('tagType') + "&bid=" + $(
        this).attr('bid') + "&d=" + tagged,
      function(data) {

      });

      if($(this).parent().children(".tagged").length == 0){
                      $(this).parent().parent().children(".insight").removeClass("red-highlight")
                      $(this).parent().parent().children(".insight").removeClass("purple-highlight")
                      $(this).parent().parent().children(".insight").removeClass("blue-highlight")
                      $(this).parent().parent().children(".insight").removeClass("orange-highlight")
                      $(this).parent().parent().children(".insight").removeClass("green-highlight")
      }else{
          $(this).parent().parent().children(".insight").addClass($(this).attr('color')+"-highlight")
      }

  });

  $(".insight").draggable({
    revert: true,
    helper: "clone"
  });

  $(".idea").droppable({
    drop: function(event, ui) {
      $(this).addClass('dropped').delay(500).queue(function(next) {
        $(this).removeClass("dropped");
        next();

      });
    },
    hoverClass: "drop-hover"

  });

  $('.commentForm').submit(function(e) {
    if ($(this).children("[name=blurb]").val() != "") {
      $.ajax({
        dataType: "json",
        type: $(this).attr('method'),
        url: $(this).attr('action'),
        data: $(this).serialize(),
        success: function(data) {
            // @TODO UNSTUB
          $(".comments,[bid=" + data.bid + "]").append('<span class="user" \
          uid="{{comment.uid}}">Lola</span>:\
          '+data.blurb);
        }
      });
      $(this).children("[name=blurb]").val('');
    }
    e.preventDefault();

  });



  $(".insight").click(function() {
    $(this).parent('div').children('.tags').toggleClass("hide");
  });
});
