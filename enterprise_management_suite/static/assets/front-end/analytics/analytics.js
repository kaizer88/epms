$(document).ready(function() {

$('#analytics').click(function (e) {
    e.preventDefault();

    $('#capture_overview').hide();
    $('#add_strat_obj').hide();

    //ppm
    $('#list_emp_projects').hide();
    $('#capture_project').hide();
    $('#update_emp_project').hide();
    $('#add_contr').hide();
    $('#contributors').hide();

    //mtef
    $('#capture_capital_assets').hide();
    $('#capture_current_payments').hide();
    $('#capture_transfers').hide();

    //epm
    $('#pa_new').hide();
    $('#start_review').hide();

    $('#expenditure_dash').hide();
    $('#ppm_dash').hide();

    //app
    $('#capture_app').hide();


    toastr.info("Analytics Dashboard & Reports", "Module Information");
});

$('#display_ppm_analytics').click(function (e) {
    e.preventDefault();
    $('#capture_overview').hide();
    $('#capture_project').hide();
    $('#list_emp_projects').hide();
    $('#contributors').hide();
    $('#add_contr').hide();
    $('#update_emp_project').hide();
    $('#add_strat_obj').hide();
    $('#expenditure_dash').hide();
    $('#ppm_dash').fadeIn();
});


$('#display_expenditure').click(function (e) {
    e.preventDefault();
    $('#capture_overview').hide();
    $('#capture_project').hide();
    $('#list_emp_projects').hide();
    $('#contributors').hide();
    $('#add_contr').hide();
    $('#update_emp_project').hide();
    $('#add_strat_obj').hide();
    $('#ppm_dash').hide();
    $('#expenditure_dash').fadeIn();
});



var lineData = {
labels: ["January", "Feb", "March", "April"],
datasets: [
    {
        label: "National Expenditure dataset",
        backgroundColor: "rgba(26,179,148,0.5)",
        borderColor: "rgba(26,179,148,0.7)",
        pointBackgroundColor: "rgba(26,179,148,1)",
        pointBorderColor: "#fff",
        data: [506440, 500800, 600000, 550000]
    },
    {
        label: "Provincial Expenditure dataset",
        backgroundColor: "rgba(220,220,220,0.5)",
        borderColor: "rgba(220,220,220,1)",
        pointBackgroundColor: "rgba(220,220,220,1)",
        pointBorderColor: "#fff",
        data: [460500, 660000, 500000, 590000]
    }
]
};

var lineOptions = {
    responsive: true
};


var ctx = document.getElementById("lineChart").getContext("2d");
new Chart(ctx, {type: 'line', data: lineData, options:lineOptions});


/* this is for creating the csrf token
don't mess around it and don't code below
*/

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


// do no code below this line
});
