const socket = io.connect(window.location.host);
const weights = document.getElementsByClassName("weights")[0];
const chat_wrapper = document.getElementsByClassName("main_messages_wrapper")[0];

const getCookie = (name) => {
    return document.cookie.split('; ').reduce((r, v) => {
      const parts = v.split('=')
      return parts[0] === name ? decodeURIComponent(parts[1]) : r
    }, '')
  }

const your_username = getCookie("username");


window.addEventListener("beforeunload", function () {
    socket.emit('disconnecting')
})

function send_message(){
    var message_content = document.getElementsByClassName("chat_input_box")[0].value;
    console.log(message_content);
    socket.emit("message", message_content);
    return false;
};

socket.on("new_message", function(username, new_message_content){
    
    // Craete generic message wrraper
    var message_wrapper = document.createElement("div");
    var message_p = document.createElement("p")
    message_p.setAttribute("class", "message_p")
    message_p.innerHTML = new_message_content

    if (username == "system"){
        message_wrapper.setAttribute("class", "system_message_wrapper");
        console.log("system")
    
    } else if (username == your_username){ //To do: Change to user's username
        
        message_wrapper.setAttribute("class", "message_wrapper");
        message_wrapper.setAttribute("id", "your_message_wrapper");
        message_wrapper.appendChild(message_p);


    } else{
        // Define message_wrraper
        message_wrapper.setAttribute("class", "message_wrapper");
        message_wrapper.setAttribute("id", "friend_message_wrapper");

        //Create username p element
        var username_p = document.createElement("p");
        username_p.setAttribute("class", "message_author_name");
        username_p.innerHTML = username;
        message_wrapper.appendChild(username_p)

        console.log(username);   
    };

    // Append p to message wrapper
    message_wrapper.appendChild(message_p);
    // Append message to chat wrapepr
    chat_wrapper.appendChild(message_wrapper);
    console.log("Recived: ", new_message_content, "From: ", username);

    //Scroll down
    var containerHeight = chat_wrapper.clientHeight;
    var contentHeight = chat_wrapper.scrollHeight;

    chat_wrapper.scrollTop = contentHeight - containerHeight;
});