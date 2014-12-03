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

    var consumption = {};

    socket.on('internet_usage', function(payload) {
        payload = JSON.parse(payload);

        var html = '';
        var ips = Object.keys(payload).sort();

        var gross_speed = get_gross_speed(payload, ips);
        for(var i = 0 ; i < ips.length ; i++)
        {
            var data = [];
            var ip = ips[i];

            var details = payload[ip];

            data.push(ip);
            data.push(details['name']);
            data.push(details['mac']);

            var tcp = check_undefined_speed(details['tcp']);
            data.push(tcp);

            var udp = check_undefined_speed(details['udp']);
            data.push(udp);

            var total = tcp + udp;
            data.push(total);


            var percentage = total / gross_speed * 100;
            data.push(percentage.toFixed(0) + "%");


            if( isNaN(consumption[ip]) )
                consumption[ip] = 0;

            consumption[ip] += total;

            data.push(consumption[ip]);


            var total_consumption = get_total_consumption(consumption);
            percentage = consumption[ip] / total_consumption * 100;
            data.push(percentage.toFixed(0) + "%");


            html = html.concat(draw_row(data));
        }

        $("#usage-table").html(html);
    });
});

function draw_row(data) {
    html = '<tr>';
    for(var i = 0; i < data.length; i++) {
        var det = data[i];
        if( det === undefined || det == 'NaN') {
            det = '';
        }
        var td_html = "<td>" + det + "</td>";
        html = html.concat(td_html);
    }
    html = html.concat('</tr>');
    return html;
}

function check_undefined_speed(speed) {
    if( speed === undefined) {
        return 0;
    }
    else {
        return speed;
    }
}

function get_gross_speed(payload, ips) {
    var gross_speed = 0;
    for(var i = 0 ; i < ips.length ; i++) {
        var details = payload[ips[i]];
        gross_speed += check_undefined_speed(details['tcp']) +
            check_undefined_speed(details['udp']);
    }
    return gross_speed;
}

function get_total_consumption(consumption_list) {
    var total_consumption = 0;

    var keys = Object.keys(consumption_list);
    for( var i = 0 ; i < keys.length ; i++ ) {
        total_consumption += consumption_list[keys[i]];
    }
    return total_consumption;
}
