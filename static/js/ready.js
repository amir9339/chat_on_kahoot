const ready_btn = document.getElementsByClassName("ready")[0];
const socket = io.connect('window.location.host');
const pending_players = document.getElementsByClassName("players")[0];
const ready_players = document.getElementsByClassName("players")[1];
const weights = document.getElementsByClassName("weights")[0];


ready_btn.addEventListener("click", function() {
    this.classList.toggle("pressed")
    socket.emit('ready_state_change')
    weights.classList.toggle("pressed_weights");
    window.location.pathname = "/test"
})

socket.on('users_update', function(users){
    const ready = users.ready_users;
    const pending = users.pending_users;
    pending_players.innerHTML = pending.join(", ");
    ready_players.innerHTML = ready.join(", ");
});

window.addEventListener("beforeunload", function () {
    socket.emit('disconnecting')
})