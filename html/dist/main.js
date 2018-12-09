$("body").ready(function() {
  $(".colum").each(function(x) {
    let isQuad = $(this).hasClass("colum-quadruple"),
        isDouble = $(this).hasClass("colum-double"),
        isSingle = $(this).hasClass("colum-single");
    let selector = isQuad?"colum-quadruple":isDouble?"colum-double":"colum-single";
        
    let text = $(this).find("."+selector+"-title").text()
    if (64 <= text.length) {
      let x = $(this).find("."+selector+"-body")[0]
      console.log($(x).css("height"))
//       $(x).css("font-size","-=1em")
      $(this).find("."+selector+"-title").css("font-size","-=0.4em")
      
      console.log($(x).css("height"))
    }
    console.log(x, text, selector+"-title", 64 <= text.length)
  })
  $("span.youtube").empty()
  $("small").empty()
  $("img").css("width","350px")
  
  $("p").each(function(x) {
    let c = $(this).children(),
        text = $(this).text()
    if(c.length == 0 && text.length == 0)
      $(this).empty()
    if(c.length == 1 && c[0].tagName == "BR") {
      $(this).empty()
    }
  })
})
// YouTubers Are Mad Again After YouTube Deletes Videos With Paid 