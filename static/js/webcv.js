// function for churl 
function churl(){
        var url = window.location.href;
       
        var search_params = url.searchParams;
        
        console.log(url);
        let params = new URLSearchParams(url.search);

        var data = document.getElementById('vdform').elements['videonum'].value

        console.log(data);
        //Add a third parameter.
        params.set('num', data);
        console.log(params.toString());
        window.history.replaceState('', '', "?"+params.toString())
        window.location.reload()
      }

// function for video_feed
function vd_feed_by_url(){
      var getUrlParameter = function getUrlParameter(sParam) {
      var sPageURL = window.location.search.substring(1),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

      for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
          return typeof sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
        }
      }
      return false;
    };
    var camnum = getUrlParameter('num');
    var ci = 0;
    for (i = 0; i < camnum; i++) {
      ci = ci + 1;
      $('#vidcontainer').append('<img src="' + Flask.url_for('Webcv.video_feed', {"num":ci }) + '">');
    }
}