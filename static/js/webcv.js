// video set in html
function vdset(){
  var data = document.getElementById('vdform').elements['videonum'].value;
  var divid;
  
  console.log(data)
   $('#vidcontainer').empty();
  
  for (let i =1; i<=data; i++){
    divid = "video-div-"+i.toString();
    // div
    $('#vidcontainer').append('<div class="col text-center div-inline-gray" id="'+divid+'">');
    // title
    $('#'+divid).append('<p>'+"video"+i.toString()+'</p>');
    // img
    $('#'+divid).append('<img src="' + Flask.url_for('Webcv.video_feed', {"num":i }) + '" id="video'+i.toString()+'">');

  }
}
