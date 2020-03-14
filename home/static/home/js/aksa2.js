var comment_form = document.querySelector("#comment-form")
var comment_id = comment_form.querySelector("[name=parent]").value
var main = comment_form.querySelector("[name=main]").value
var name = ""
var kind = "main"
var blog_id = comment_form.querySelector("[name=blog_id]").value
var content = comment_form.querySelector("[name=content]").value
var content_title = comment_form.parentElement.querySelector("h4.comment-title")
var comment_list = document.querySelector(".comment-list")
var parent_html = comment_list


function addReplyFunction(btn, comment){
        btn.addEventListener("click", function(e){
            e.preventDefault()
            let comment_main = comment.querySelector("input.main").value
            let comment_name = comment.querySelector("input.name").value
            let comment_parent = comment.querySelector("input.parent").value
            let comment_kind = comment.querySelector("input.kind").value

            main = comment_main
            reply_to = comment_repy_to
            parent = comment_parent
            kind = "reply"

            content_title.innerHTML = "Reply to " + reply_to + "'s comment ID: " + parent
            content =  "@" + reply_to + "\n"

            if (kind === "reply" && main !== 0){
                parent_html = comment.parentElement.parentElement
                console.log("reply")
                console.log(main)
                console.log(parent_html)
            }
            else{
                parent_html = comment_list
                console.log("main")
                console.log(main)
                console.log(parent_html)
            }
            

        })
    }


comment_form.addEventListener("submit", function(e){
    e.preventDefault()
    let csrf = document.querySelector("[name=csrfmiddlewaretoken]").value
    content = comment_form.querySelector("[name=content]").value
    data = new FormData()
    data.append("blog_id", blog_id)
    data.append("content", content)
    data.append("parent", parent)
    data.append("main", main)

    fetch("/blogs/comment/", {
        method: "POST",
        headers: {
            "X-CSRFToken": csrf
        },
        body: data
    })
    .then(function(response){
        console.log("ajax success!")
        return response.json()
    }, function(response){
        console.log("ajax failed!")
    })
    .then(function(result){
        console.log(parent_html)
        console.log(parent)
        parent_html.innerHTML += 
        '<li>' +
            '<div class="comment">' +
                '<div class="comment-avator set-bg" data-setbg="'+ result.user_avatar +'" style="background-image: url(' + result.user_avatar + ');"></div>' +
                '<div class="comment-content">' +
                    '<h5>' + result.user_name + '<span> #' + result.new_comment_id + " - " + result.date + '</span></h5>' +
                    '<p>' + content + '</p>'   +
                    '<button class="c-btn">Reply</button>' + 
                    '<input type="hidden" class="main" value=' + main + '>' + 
                    '<input type="hidden" class="reply-to" value=' + result.user_name + '>' +
                    '<input type="hidden" class="parent" value=' + result.new_comment_id + '>' +
                    '<input type="hidden" class="kind" value=' + kind + '>' + 
                '</div>' +
            '</div>' +
            '<ul class="replay-comment-list"></ul>' +
        '</li>'

        content = ""
        content_title = "Leave a message"
        kind = "main"

        comment_last = parent_html.lastElementChild.querySelector(".comment")
        comment_last_btn = comment_last.querySelector("button.c-btn")
        document.querySelector("#number-of-comments").innerHTML = parseInt(document.querySelector("#number-of-comments").innerHTML) + 1
        addReplyFunction(comment_last_btn, comment_last)
    })
    
})





function initialReplyFunction(){
    let comment_all = comment_list.querySelectorAll(".comment")
    for (i=0; i< comment_all.length; i++){
        let comment = comment_all[i]
        let btn = comment.querySelector("button.c-btn")
        addReplyFunction(btn, comment)
    }
}

initialReplyFunction()