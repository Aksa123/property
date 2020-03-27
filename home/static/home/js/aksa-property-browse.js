var page = 1;
var page_button = document.querySelectorAll("a.page-item")
var property_list = document.querySelector(".property-list")
var url_params = new URLSearchParams(window.location.search)
var add_params = ""
const url = new URL("http://127.0.0.1:8000/browse/")

console.log(window.location.search)

function addPageButtonFunction(btn){
    btn.addEventListener("click", function(event){
        event.preventDefault();
        page = btn.querySelector("input").value
        // let url = "/browse?ajax=true&page=" + page
        // // refresh add_params so it won't overlap
        // add_params = "" 
        // for(let i of url_params.keys()){
        //     if (url_params.get(i) !== "page" && url_params.get(i) !== "ajax")
        //     add_params += "&" + i + "=" + url_params.get(i)
        // }
        // url += add_params
        
        //
        
        if (url_params.has("page")){
            url_params.set("page", page)
        }
        else{
            url_params.append("page", page)
        }        
        let fetch_url = url + "?ajax=true&" + url_params.toString()
        
        fetch(fetch_url)
        .then(function(response) {
            if (response.ok){
                console.log("success!")
            }
            else{
                console.log("fail!")
            }
            return response.json()
        },function(rejected){
            console.log("promise rejected: " + rejected) 
        })
        .then(function(properties){
            let property_item = property_list.querySelectorAll(".property-item")
            for (let i=0; i<property_item.length; i++){
                property_item[i].remove()
            }
            for (let i=0; i<properties.properties.length; i++){
                let item = properties.properties[i]
                let garage = ""
                if (item.garage){
                    garage = "Has "
                }
                else{
                    garage = "No "
                }

                property_list.innerHTML += '<div class="col-lg-4 col-md-6 property-item">'
                + '<!-- feature -->'
                + '<div class="feature-item">'
                +    '<div class="feature-pic set-bg" data-setbg="' + item.absolute_url + '" style="background-image: url(' + item.absolute_url + ');">'
                +        '<div class="sale-notic">' + item.status + '</div>'
                +    '</div>'
                +    '<div class="feature-text">'
                +        '<div class="text-center feature-title">'
                +            '<h5>' + item.name + '</h5>'
                +            '<p><i class="fa fa-map-marker"></i>' + item.address +', ' + item.city + '</p>'
                +        '</div>'
                +        '<div class="room-info-warp">'
                +            '<div class="room-info">'
                +                '<div class="rf-left">'
                +                    '<p><i class="fa fa-th-large"></i>' + item.area + ' Square foot</p>'
                +                    '<p><i class="fa fa-bed"></i>' + item.bedroom + ' Bedrooms</p>'
                +                '</div>'
                +                '<div class="rf-right">'
                +                    '<p><i class="fa fa-car"></i>' + garage + ' Garages</p>'
                +                    '<p><i class="fa fa-bath"></i>' + item.bathroom + ' Bathrooms</p>'
                +                '</div>'
                +            '</div>'
                +            '<div class="room-info">'
                +                '<div class="rf-left">'
                +                    '<p><i class="fa fa-user"></i>' + item.user + '</p>'
                +                '</div>'
                +                '<div class="rf-right">'
                +                    '<p><i class="fa fa-clock-o"></i> Built in ' + item.founded_date + '</p>'
                +                '</div>'
                +            '</div>'
                +        '</div>'
                +        '<a href="' + item.url + '" class="room-price">$' + item.price + '</a>'
                +    '</div>'
                +'</div>'
            +'</div>'
            }

            refreshPagination(properties.next_page, properties.prev_page, properties.page_list, url_params.toString())

        })
        .catch(error => console.log(error))
    }
)
}


function refreshPagination(next_page, prev_page, page_list, new_param){    
    let pagination = document.querySelector(".site-pagination")
    let page_items = pagination.querySelectorAll(".page-item")
    for (i=0; i<page_items.length; i++){
        page_items[i].remove()
    }
    let new_next_page = ""
    if (next_page > 0){
        new_next_page = '<a class="page-button next-page page-item"><input type="hidden" value=' + (parseInt(page) + 1) + '><i class="fa fa-angle-right"></i></a>'
    }

    let new_prev_page = ""
    if (prev_page > 0){
        new_prev_page = '<a class="page-button prev-page page-item"><input type="hidden" value=' + (parseInt(page) - 1) + '><i class="fa fa-angle-left"></i></a>'
    }

    let new_pages = ""
    for (j=0; j< page_list.length; j++){
        if (page_list[j] === parseInt(page)){
            new_pages += '<span class="page-item">' + page + '</span>'
        }
        else{
            new_pages +=  '<a class="page-item"><input type="hidden" value=' + page_list[j] + '>' + page_list[j] + '</a>'
        }
    }

    pagination.innerHTML += new_prev_page + new_pages + new_next_page
    let new_page_button = document.querySelectorAll("a.page-item")
    for (k=0; k<new_page_button.length; k++){
        let btn = new_page_button[k]
        addPageButtonFunction(btn)
    }

    
    window.history.pushState('', '', url + "?" + new_param);
    
    
}









for (let i=0; i< page_button.length; i++ ){
    let btn = page_button[i]
    addPageButtonFunction(btn)
    }
