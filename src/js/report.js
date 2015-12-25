/**
 * Created by vitaliyharchenko on 25.12.15.
 */
var User = {
    constructor: function(first_name, last_name, phone, status) {
        this.first_name = first_name;
        this.last_name = last_name;
        this.phone = phone;
        this.status = status;
    }
}

$(function(){
    var users = [];

    var subscribed_string = '{{users}}'.replace(/&quot;/g,"\"");
    var subscribed_users = jQuery.parseJSON(subscribed_string);


    for(var i=0; i<subscribed_users.length; i++) {
        var pk = subscribed_users[i]['pk'];
        var fields = subscribed_users[i]['fields'];
        fields['id'] = pk;
        users[pk] = fields;
    };

    console.log(users);

    var table = '';

    table += '<table>';

    users.forEach(function(item, i, users){
        table += '<td>';
        table += '<tr>' + item['first_name'] + '</tr>';
        table += '<tr>' + item['last_name'] + '</tr>';
        table += '</td>';
    });
    table += '</table>';

    console.log(table);
    $(".userspane").html(function() {
        return table;
    });
});