
document.getElementById('periodo').addEventListener('click', Change);
document.getElementById('category').addEventListener('click', Change);


function Change(){
    const per = document.getElementsByName('per');
    const universe = document.getElementById('universe').innerHTML;

    for (var i = 0; i <  per.length; i++) {
        if (per[i].checked) {
          var periodo = per[i].value
          break;
        }
    }
    const cat = document.getElementsByName('cat');
    for (var i = 0; i <  cat.length; i++) {
        if (cat[i].checked) {
        var category = cat[i].value
        break;
        }
    }
    var data = {'data': {'universe':universe, 'periodo': periodo, 'category': category}};
    console.log(data);
    fetch("/filter", {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "X-Requested-With": "XMLHttpRequest"
    }
     }).then(function(response){
         if (response.ok){
            return response.json();
         }
    }).then (
        function(data){
            console.log(data);
        }
    )}
