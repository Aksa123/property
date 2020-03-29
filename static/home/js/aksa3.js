var comment_form = document.querySelector("#comment-form")
var comment_list = document.querySelector(".comment-list")
var blog_id = parseInt(comment_form.querySelector("[name=blog_id]").value)
var csrf = comment_form.querySelector("[name=csrfmiddlewaretoken]").value
var comment_form_title = comment_form.parentElement.querySelector("h4.comment-title").innerHTML
var comment_form_content = ""
var comment_parent = 0 // default
var main = 0 // default
var parent_html = comment_list


function addReplyFunction(btn, comment_single){
    btn.addEventListener("click", function(e){
        e.preventDefault()
        comment_parent = comment_single.querySelector(".comment-id").value
        let comment_main = parseInt(comment_single.querySelector(".main").value)
        if (comment_main === 0){
            main = comment_single.querySelector(".comment-id").value
            parent_html = comment_single.parentElement.querySelector(".replay-comment-list")
        }
        else{
            main = comment_single.querySelector(".main").value
            parent_html = comment_single.parentElement.parentElement
        }
        console.log(parent_html)
        comment_form.parentElement.querySelector("h4.comment-title").innerHTML = "Reply to #" + comment_parent
        comment_form.parentElement.querySelector("[name=content]").value = "@" + comment_single.querySelector("input.user").value + "#" + comment_parent + "\n"
        console.log("reply to comment" + comment_parent )
    })
}



function initialReplyFunction(){
    let comment_items =comment_list.querySelectorAll(".comment")
    for (i=0; i<comment_items.length; i++){
        let comment_single = comment_items[i]
        let btn = comment_single.querySelector(".c-btn")
        addReplyFunction(btn, comment_single)
    }
}


function resetCommentFunction(){
    parent_html = comment_list
    main = 0
    comment_parent = 0
    comment_form.parentElement.querySelector("h4.comment-title").innerHTML = "Leave Your Comment"
    comment_form.parentElement.querySelector("[name=content]").value = ""
}



comment_form.addEventListener("submit", function(e){
    e.preventDefault()
    comment_form_content = comment_form.querySelector("[name=content]").value
    data = new FormData()
    data.append("blog_id", blog_id)
    data.append("content", comment_form_content)
    data.append("parent", comment_parent)
    data.append("main", main)

    fetch("/blogs/comment/", {
        method: "POST",
        headers: {
            "X-CSRFToken": csrf
        },
        body: data
    })
    .then(response => response.json())
    .then(function(result){
        let new_reply = '<li>' +
        '<div class="comment">' +
            '<div class="comment-avator set-bg" data-setbg="'+ result.user_avatar +'" style="background-image: url(' + result.user_avatar + ');"></div>' +
            '<div class="comment-content">' +
                '<h5>' + result.user_name + '<span> #' + result.new_comment_id + " - " + result.date + '</span></h5>' +
                '<p>' +
                comment_form_content + 
                '</p>' +
                '<button class="c-btn">Reply</button>' + 
                '<input type="hidden" class="main" value=' + result.main + '>' + 
                '<input type="hidden" class="user" value=' + result.user_name + '>' +
                '<input type="hidden" class="comment-id" value=' + result.new_comment_id + '>' +
            '</div>' +
        '</div>' +
        '<ul class="replay-comment-list"></ul>' +
        '</li>'
        
        parent_html.innerHTML += new_reply
        document.querySelector("#number-of-comments").innerHTML = parseInt(document.querySelector("#number-of-comments").innerHTML) + 1


        resetCommentFunction()
        initialReplyFunction()


    })
})

initialReplyFunction()
