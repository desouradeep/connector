$(document).ready(function() {
    WEB_SOCKET_SWF_LOCATION = "/static/WebSocketMain.swf";
    WEB_SOCKET_DEBUG = true;

    // Socket.io specific code
    socket = io.connect('http://' + document.domain + ':' + location.port);

    socket.on('connect', function() {
        socket.emit('connect');
    });

    socket.on('disconnect', function() {
        socket.emit('disconnect');
    });

    socket.on('data', function(data) {
        console.log(data);
    });

    socket.on('internet_usage', function(payload) {
        payload = JSON.parse(payload);
        console.log(payload);
    });
});
