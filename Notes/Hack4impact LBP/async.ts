function fetchdata(){
    fetch('')
    .then(Response => Response.json())
    .then(data => console.log(data))
}