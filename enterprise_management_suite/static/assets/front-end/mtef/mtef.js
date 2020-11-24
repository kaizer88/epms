$(document).ready(function() {


$('#mtef_budget').click(function (e) {
    e.preventDefault();
    toastr.info("MTEF & Budget", "Module Information");
    $('#add_strat_obj').hide();
    $('#capture_project').hide();
    $('#list_emp_projects').hide();
    $('#contributors').hide();
    $('#add_contr').hide();
    $('#update_emp_project').hide();
    $('#expenditure_dash').hide();
    $('#ppm_dash').hide();
    $('#capture_overview').hide();
    $('#capture_capital_assets').hide();
    $('#capture_current_payments').hide();
    $('#capture_transfers').hide();
    //app
    $('#capture_app').hide();


});

$('#current_payments').click(function (e) {
    e.preventDefault();
    $('#add_strat_obj').hide();
    $('#capture_project').hide();
    $('#list_emp_projects').hide();
    $('#contributors').hide();
    $('#add_contr').hide();
    $('#update_emp_project').hide();
    $('#expenditure_dash').hide();
    $('#ppm_dash').hide();
    $('#capture_overview').hide();
    $('#capture_transfers').hide();
    $('#capture_capital_assets').hide();
    $('#capture_current_payments').fadeIn();
});


$('#transfers').click(function (e) {
    e.preventDefault();
    $('#add_strat_obj').hide();
    $('#capture_project').hide();
    $('#list_emp_projects').hide();
    $('#contributors').hide();
    $('#add_contr').hide();
    $('#update_emp_project').hide();
    $('#expenditure_dash').hide();
    $('#ppm_dash').hide();
    $('#capture_overview').hide();
    $('#capture_current_payments').hide();
    $('#capture_capital_assets').hide();
    $('#capture_transfers').fadeIn();

});


$('#capital_assets').click(function (e) {
    e.preventDefault();
    $('#add_strat_obj').hide();
    $('#capture_project').hide();
    $('#list_emp_projects').hide();
    $('#contributors').hide();
    $('#add_contr').hide();
    $('#update_emp_project').hide();
    $('#expenditure_dash').hide();
    $('#ppm_dash').hide();
    $('#capture_overview').hide();
    $('#capture_current_payments').hide();
    $('#capture_transfers').hide();
    $('#capture_capital_assets').fadeIn();

});


$('#save_current_payments').click(function (e) {
    e.preventDefault();
    let compensation = $('#compensation_employees').val();
    saveCurrentPayments(compensation)
});


$('#save_capital_assets').click(function (e) {
    e.preventDefault();
    let fixed_accounts = $('#fixed_accounts').val();
    let intangible_assets = $('#intangible_assets').val();
    let machinery = $('#machinery').val();
    saveCapitalAssets(fixed_accounts, intangible_assets, machinery)
});


$('#save_transfers').click(function (e) {
    e.preventDefault();
    let dept_agencies = $('#dept_agencies').val();
    let social_benefits = $('#social_benefits').val();
    let non_profit_inst = $('#non_profit_inst').val();
    saveTransfers(dept_agencies, social_benefits, non_profit_inst)
});


function saveCurrentPayments(compensation) {
        let csrftoken = getCookie('csrftoken');
        $.ajax({
            url: '/dashboard/mtef/current_payments/create/',
            type: 'POST',
            dataType: 'json',
            data: {compensation: compensation},
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            success: function (data) {
            if(data.status === 200) {
                toastr.success(data.message)
                }
            else if(data.status === 52){
                toastr.error(data.message)
                }
            }
        });
    }

function saveCapitalAssets(accounts, assets, machinery){

        let csrftoken = getCookie('csrftoken');
        $.ajax({
            url: '/dashboard/mtef/capital_assets/create/',
            type: 'POST',
            dataType: 'json',
            data: {
                accounts: accounts,
                assets: assets,
                machinery: machinery
            },
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            success: function (data) {
            if(data.status === 200) {
                toastr.success(data.message)
                }
            else if(data.status === 52){
                toastr.error(data.message)
                }
            }
        });
    }

function saveTransfers(dept_agencies, social_benefits, non_profit_inst){

        let csrftoken = getCookie('csrftoken');
        $.ajax({
            url: '/dashboard/mtef/transfers/create/',
            type: 'POST',
            dataType: 'json',
            data: {
                agencies: dept_agencies,
                benefits: social_benefits,
                institutes: non_profit_inst
            },
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            success: function (data) {
            if(data.status === 200) {
                toastr.success(data.message)
                }
            else if(data.status === 52){
                toastr.error(data.message)
                }
            }
        });
    }




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
