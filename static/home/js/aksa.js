var comment_form = document.querySelector("#comment_form");
var reply_btn = document.querySelectorAll("button.c-btn");
var comment_parent = document.querySelector("#comment_list");
var kind = "main";
var comment_title = document.querySelector("div.comment-form-warp h4");

comment_form.addEventListener("submit", async function(event){
    event.preventDefault();
    let comment_text = comment_form.querySelector("[name=comment]").value
    if (comment_text.trim() !== "" ){
        let blog_id = parseInt(comment_form.querySelector("[name=blog_id]").value);
        let parent_id = parseInt(comment_form.querySelector("[name=parent]").value);
        let main_id = parseInt(comment_form.querySelector("[name="))
        let csrf = document.querySelector("[name='csrfmiddlewaretoken']").value; 
        var data = new FormData();

        let ourRequest = await fetch("/blogs/comment/", 
        {
            method: "POST",
            headers:{
                "X-CSRFToken": csrf
            },
            body: data
        });
        let ourResponse = await ourRequest.json();
        if (ourRequest.ok){
            console.log("status ok!");
        }
        else{
            console.log("oh, crap!");
        }

        comment_HTML = "";
        comment_HTML += 
        '<li>' +
            '<div class="comment">' +
                '<div class="comment-avator set-bg" data-setbg="'+ ourResponse.user_avatar +'" style="background-image: url(' + ourResponse.user_avatar + ');"></div>' +
                '<div class="comment-content">' +
                    '<h5>' + ourResponse.user_name + '<span> #' + ourResponse.new_comment_id + " - " + ourResponse.date + '</span></h5>' +
                    '<p>' + comment_text + '</p>'   +
                    '<button class="c-btn">Reply</button>' + 
                    '<input type="hidden" class="comment_id" value=' + ourResponse.new_comment_id + '>' + 
                    '<input type="hidden" class="reply_to" value=' + ourResponse.user_name + '>' +
                    '<input type="hidden" class="kind" value=' + kind + '>' + 
                '</div>' +
            '</div>' +
            '<ul class="replay-comment-list"></ul>' +
        '</li>';
        
        comment_parent.innerHTML += comment_HTML;
        addReplyButtonFunction(comment_parent.lastElementChild.querySelector("button.c-btn"));
        mainComment();
    }
    else{
        comment_form.querySelector("[name=comment]").setAttribute("placeholder", "Comment cannot be empty!");
    }
    
})


function mainComment(){
    comment_title.innerHTML = "Leave your comment";
    comment_parent = document.querySelector("#comment_list");
    comment_form.querySelector("[name=comment]").removeAttribute("placeholder");
    comment_form.querySelector("[name=comment]").value = "";
    kind = "main";
    comment_form.querySelector("[name=parent]").value = 0;
}


function addReplyButtonFunction(btn){
    btn.addEventListener("click", async function(event){
        event.preventDefault();
        var parent_element = btn.parentElement;
        let reply_to = parent_element.querySelector(".reply_to").value;
        let comment_id = parent_element.querySelector(".comment_id").value;
        let reply_id = parent_element.querySelector(".reply_id").value
        kind = parent_element.querySelector(".kind").value;
        comment_form.querySelector("[name=comment]").value = "@" + reply_to + " #" + comment_id + "\n";
        comment_form.querySelector("[name=parent]").value = comment_id;
        comment_form.querySelector("[name=reply_id]").value = reply_id;
        comment_title.innerHTML = "Reply to " + reply_to + "'s comment id: " + comment_id;

        if (kind==="main"){
            console.log("this is main");
            comment_parent = parent_element.parentElement.nextElementSibling;
        }
        else{
            console.log("this is reply");
            comment_parent = parent_element.parentElement.parentElement.parentElement;
            console.log(comment_parent);
        }
        kind = "reply";        
    })
}


for (let i=0; i<reply_btn.length; i++){
    let btn = reply_btn[i];
    addReplyButtonFunction(btn);
}
