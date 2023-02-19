const ul = document.getElementById("cupcake-list")


$('#add').click(function(event){
   event.preventDefault();
   add_cupcake();

})

async function show_cupcakes(){
    let response = await axios.get("/api/cupcakes");
    let cupcakes = response.data.cupcakes;
    for (let i = 0; i < Object.keys(cupcakes).length; i++) {
        let li = document.createElement("li");
        li.setAttribute("id", cupcakes[i].id)
        ul.append(li);
        let cupcakeLi = document.getElementById(cupcakes[i].id);
        cupcakeLi.innerText = cupcakes[i].flavor;
    }
}

async function add_cupcake(){
    let flavor = $("#flavor-input").val();
    let size = $("#size-input").val();
    let rating = $("#rating-input").val()
    let image = $("#image-input").val();
    let response = await axios.post('/api/cupcakes', {
        "flavor": flavor,
        "size": size,
        "rating": rating,
        "image": image
    })
    let cupcakes = response.data;
    let li = document.createElement("li");
    li.setAttribute("id", cupcakes.cupcake.id)
    ul.append(li);
    let cupcakeLi = document.getElementById(cupcakes.cupcake.id);
    cupcakeLi.innerText = flavor;
}

$(document).ready(function() {
    show_cupcakes();
});