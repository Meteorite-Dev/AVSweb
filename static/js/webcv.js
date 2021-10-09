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