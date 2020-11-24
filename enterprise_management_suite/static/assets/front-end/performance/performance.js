$(document).ready(function() {


$('#launchPerformance').click(function (e) {
    e.preventDefault();
    closeAllEpmsForms();

    $('#expenditure_dash').hide();
    $('#ppm_dash').hide();

    // strat
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

    //app
    $('#capture_app').hide();
    //epm

    $('#pa_new').hide();
    $('#start_review').hide();


    toastr.info("Employee Performance Management", "Module Information")

    // $('#performanceLanding').slideDown('slow');
});


$("#pa_create").click(function (e) {
    e.preventDefault();
    employmentPeriod();
    closeEpmsForms();
    $('#pa_new').slideDown('slow');
    employeeSupervisor();
});

$('#kpiForm').click(function (e) {
    e.preventDefault();
    $('#new_kpi_form').slideDown('slow');
});

function closeEpmsForms(){

    $('#performanceLanding').hide();
    $('#kra_new').hide();
    $('#myKras').hide();
    $('#capture_output').hide();
    $('#measurable_outputs_list').hide();
    $('#sign_card').hide();
    $('#capture_pdp').hide();
    $('#pdp_list_form').hide();

    // strat
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

    //app
    $('#capture_app').hide();

    //epm
    $('#start_review').hide();


}


function closeAllEpmsForms(){

    $('#performanceLanding').hide();
    $('#kra_new').hide();
    $('#myKras').hide();
    $('#capture_output').hide();
    $('#measurable_outputs_list').hide();
    $('#sign_card').hide();
    $('#capture_pdp').hide();
    $('#pdp_list_form').hide();

    // strat
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


}


$('#capture_review').click(function (e) {
   e.preventDefault();
   getRevPeriods();
   KRAWeight();
   $('#kra_review').slideDown('slow');

});

function getRevPeriods() {

    $.ajax({
        url : '/dashboard/review/rev_per/',
        type : 'get',
        dataType : 'json',

    success: function (data) {
        $('#periods').empty().append(
            $.map(data.per, function (p) {
                return '<option value="' +p.id +'">'+ p.period_start +' to '+ p.period_end +'</option>';
            }).join());
        }
    });
}

function KRAWeight(){
    $.ajax({
        url: '/dashboard/agreement/kra/list/',
        type: 'get',
        dataType: 'json',
        success: function (data) {
            $('#rev_kras').empty().append(
                $.map(data.kras, function (kra, index) {
                    return '<tr><td>' + (index +1 )   + '</td>' + '<td>' + kra.kra +'</td>'
                        + '<td>' + kra.self_weight +'</td>' + '<td><button type="button" class="btn btn-primary btn-circle" title="View KRA Measurable Outputs"><i class="fa fa-list"></i></button></td>' +
                        '<td><input type="hidden" value="'+ kra.kra_id +'" class="rev_kra_id">' +
                        '<button type="button" class="btn btn-primary btn-circle" id="kra_weight" title="Add /Update Weight" data-toggle="modal" data-target="#kraWeightModal" ><i class="fa fa-balance-scale" aria-hidden="true"></i></button>' + '</td>' +
                        '<td><button type="button" class="btn btn-success btn-sm rev_kra_save" title="Save this KRA weight">Add</button></td>' +
                        '</tr>';
            }).join());
        }
    });
}

$('#kraWeightModal').on('show.bs.modal', function () {
    var kra_id = $(event.target).closest('td').find('.rev_kra_id').val();
   $('#kra_wid').val(kra_id);
});

$('#save_emp_kraw').click(function () {
    var k_id = $('#kra_wid').val();
    var weight = $('#emp_kra_w').val();
    var period = $( "#periods option:selected" ).val();
    var rev_type = $( "#review_type option:selected" ).val();
    employeeKraWeight(k_id, weight, rev_type, period)
});

$(document).on('click', '.rev_kra_save', function() {
    var kra_id = $(event.target).closest('tr').find('.rev_kra_id').val();
    var weight =  $(event.target).closest('tr').find('.kra_weight').val();
    var period = $( "#periods option:selected" ).val();
    var rev_type = $( "#review_type option:selected" ).val();
    saveKRAWeight(kra_id, weight, rev_type, period)

});

function employeeKraWeight(k_id, weight, rev_type, period) {
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url: '/dashboard/review/kra_weight/',
        type: 'post',
        dataType: 'json',
        data : {
            kra : k_id,
            weight : weight,
            rev_type : rev_type,
            period : period
        },
        beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function (data) {
            if(data.results === 'ok'){
                console.log("kra weight saved")
            }
            else{
                console.log("failed to save kra weight")
            }
        }
    });
}

function saveKRAWeight(kra, weight, rev_type, period) {
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url: '/dashboard/review/kra_weight/',
        type: 'post',
        dataType: 'json',
        data : {
            kra : kra,
            weight : weight,
            rev_type : rev_type,
            period : period

        },
        beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function (data) {
            if(data.results === 'ok'){
                console.log("kra weight saved")
            }
            else{
                console.log("failed to save kra weight")
            }
        }
    });
}
/*

$('#signPA').click(function (e) {
    e.preventDefault();
    $('#sign_card').slideDown('slow');
    $(function() {
        $('#sign_pa_emp').bootstrapToggle({
          on: 'Signed',
          off: 'Not-signed'
        });
    });
    $(function() {
        $('#sign_pa_sup').bootstrapToggle({
          on: 'Signed',
          off: 'Not-signed'
        });
    });
     var d = new Date();
    * var strDate =  d.getDate() + "/" + (d.getMonth()+1)  + "/" + d.getFullYear();
    * $('#sup_pa_sign_date').val(strDate);
    * $('#emp_pa_sign_date').val(strDate);

});
*/
/*
$('#sign_pa').click(function (e) {
   e.preventDefault();
   if ($('#sign_pa_sup').is(':checked')) {
       var sup_sign = true;

    }
    else {
        sup_sign = false;
    }

    if ($('#sign_pa_emp').is(':checked')) {
        var emp_sign = true;
    }
    else{
       emp_sign = false;

   }
    if (($('#sign_pa_sup').is(':checked')) || ($('#sign_pa_emp').is(':checked'))){
           singPA(sup_sign, emp_sign)
    }
    else {
       alert("nothing signed")
    }
});
*/

$('#signPA').click(function (e) {
    e.preventDefault();
    closeEpmsForms();
    $('#sign_card').slideDown('slow');
});


$('#signAgreement').click(function (e) {
    e.preventDefault();
    signPerformanceAgreement()
});

function signPerformanceAgreement() {
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url: '/dashboard/agreement/sign/',
        type: 'post',
        beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function (data) {
            if(data.status === 200){
                toastr.success(data.message)
            }
            else{
                toastr.warning(data.message, "Error Code: " + data.status)
            }

        }
    });
}



$('#kraForm').click(function (e) {
    e.preventDefault();
    employeeSupervisor();
    closeEpmsForms();
    $('#kra_new').slideDown('slow');
    assignPaID()
});

$('#my_targets_list').click(function (e) {
    e.preventDefault();
    Targets();
});

$('#targets').click(function (e) {
   e.preventDefault();
   closeEpmsForms();
   close_review_forms();
   $('#capture_target').slideDown('slow');

});

$('#view_kras').click(function (e) {
    e.preventDefault();
    getKRAS()
});

$('#myKrasForm').click(function (e) {
    e.preventDefault();
    listKRAs();
});

function employeeSupervisor(){

    $.ajax({
        url: '/dashboard/search/supervisors/fetch',
        type: 'get',
        dataType: 'json',
        success: function (data) {
                $('.type_supervisor').typeahead({
                    source: [data.results[0].name__user__employee_code + ' ' +
                        data.results[0].name__first_name + ' ' + data.results[0].name__last_name
                ],
                items: 32,

            });
        }
    });
}


function getKRAS(){
    /*
    * get list of kras that are available
    * allow user to select a kra that they will attach the measurable output to
    * populate the value on the text area, with kra id
    * */
    $.ajax({
        url: '/dashboard/agreement/kra/list/',
        type: 'get',
        dataType: 'json',
        success: function (data) {

            $('#outputs_kras').empty().append(
                $.map(data.kras, function (kra, index) {
                    return '<tr><td>' + (index +1 )  + '<input type="hidden" value="'+kra.kra_id+'">'+ '</td>' + '<td>' + kra.kra +'</td>' + '<td>' + '<input type="radio" name="output_kra" ' +
                        'data-kpikra="'+kra.kra_id+'" value="'+kra.kra+'" class="staff_kra_id">'+'</td></tr>';
            }).join());
        }
    });
}


function clearOutputs() {
    $('#new_mo_kra_id').val('');
    $('#output').val('');
    $('#mo_weight').val('');
    $('#mo_resources').val('');
    $('#mo_tframe').val('default');
    $('#mo_calendar').val('');
    $('#mo_kra_id').val('');
    $('#output_kra_val').val('');
}

/*
function listOutputs(){
    $.ajax({
        url: '/dashboard/agreement/outputs/list/',
        type: 'get',
        dataType: 'json',
        success: function (data) {
            toastr.info("Loading Measurable Outputs");
            $('#outputs_list').empty().append(
                $.map(data.outputs, function (mo, index) {
                    return '<tr><td>' + (index +1 )   + '</td>' + '<td>' + mo.output +'</td>'
                        + '<td>' + mo.self_weight +'</td>' +
                        '<td><input type="hidden"><button type="button" class="btn btn-info btn-circle" ' +
                        'value="'+ mo.output_id +'" id="updateMO" data-toggle="modal" data-target="#updateOutputModal"><i class="fa fa-edit"></i></td>' +
                        '<td><button type="button" class="btn btn-warning btn-circle" value="'+ mo.output_id +'" id="deleteMO"><i class="fa fa-times"></i></td>' +
                        '</tr>';
            }).join());
        }
    });
}
*/

function Targets(){
    $.ajax({
        url: '/dashboard/agreement/targets/list/',
        type: 'get',
        dataType: 'json',
        success: function (data) {
            toastr.info("Loading Targets");
            $('#targets_list').empty().append(
                $.map(data.targets, function (target, index) {
                    return '<tr><td>' + (index +1 )   + '</td>' + '<td>' + target.target +'</td>'
                        + '<td>' + target.start_date +'</td>' + '<td>' + target.end_date +'</td>' +
                        '<td><input type="hidden"><button type="button" class="btn btn-info btn-circle" ' +
                        'value="'+ target.target_id +'" id="updateTarget" data-toggle="modal" data-target="#updateTargetModal"><i class="fa fa-edit"></i></td>' +
                        '<td><button type="button" class="btn btn-warning btn-circle" value="'+ target.target_id +'" id="del_target"><i class="fa fa-times"></i></td>' +
                        '</tr>';
            }).join());
        }
    });
}


$(document).on('click', '#updateMO', function() {
    var output_id = $(this).val();
    loadMO(output_id)

});


function loadMO(output_id) {
   $.ajax({
        url: '/dashboard/agreement/load_mo/',
        type: 'get',
        dataType: 'json',
        data : {
            output_id : output_id
        },
        success: function (data) {
                $('#mo_id').val(data.output[0].output_id);
                $('#update_mo_content').val(data.output[0].output);
                $('#update_mo_weight').val(data.output[0].self_weight);
                $('#update_mo_rsc').val(data.output[0].resources);
                $('#update_mo_tframe').val(data.output[0].time_frame);
                $('#update_mo_cal').val(data.output[0].cal_date);
                $('#update_mo_target').val(data.output[0].target);
            }
        });
}

$('#update_output').click(function (e) {
    e.preventDefault();
    var _id = $('#mo_id').val();
    var output = $('#update_mo_content').val();
    var weight = $('#update_mo_weight').val();
    var rsc = $('#update_mo_rsc').val();
    var cal = $('#update_mo_cal').val();
    var tf = $('#update_mo_tframe').val();
    updateMO(_id, output, weight, rsc, cal, tf)
});

function updateMO(_id, output, weight, rsc, cal, tf) {
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url: '/dashboard/agreement/outputs/update/',
        type: 'post',
        dataType: 'json',
        data : {
            _id : _id,
            output : output,
            emp_weight : weight,
            rsc : rsc,
            tf : tf,
            cal_date : cal
        },
        beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
    });
}

function assignPaID() {
    $.ajax({
        url: '/dashboard/agreement/get_pa/',
        type: 'get',
        dataType: 'json',
        success: function (data) {
            $('#pa_id').val(data.pa)
        }
    });
}


$("#saveNewFinPeriod").click(function (e) {
    e.preventDefault();
    savePerAgreement()
});

$("#saveNewFinYear").click(function (e) {
    e.preventDefault();
    savePerAgreement()
});

$('.closeWell').click(function (e) {
    e.preventDefault();
     $(this).closest('.card').fadeOut();
});


function employmentPeriod() {
    $.ajax({
        url: '/dashboard/agreement/financial_year/',
        type: 'get',
        dataType: 'json',
        success: function (data) {
            if(data.status === 200){
                toastr.info("Active Financial Year: " + data.message);
                $("#finYear").append(
                    $("<option></option>")
                        .attr("value", data.message)
                        .text(data.message)
                );

            }
        }
    });
}

function savePerAgreement() {
    let csrftoken = getCookie('csrftoken');
    let start = $('#periodStart').val();
    let end = $('#periodEnd').val();
    let finYear = $('#finYear').val();
    let superv = $("#pa_supervisor").next("ul").find("li.active").data("value");
    $.ajax({
        url: '/dashboard/agreement/create_agreement/',
        type: 'post',
        dataType: 'json',
        data : {
            period_start : start,
            period_end : end,
            fin_year : finYear,
            superv : superv
        },
        beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
         },
        success: function (data) {
        if (data.status === 200) {
            toastr.success(data.message)
        }
        else {
            toastr.error(data.message, "Error Code: " + data.status)
            }
        }
    });
}

$('#mo_calendar').datepicker({
    dateFormat: 'yy-mm-dd',
    changeYear: true

});

$('#update_mo_cal').datepicker({
    dateFormat: 'yy-mm-dd',
    changeYear: true

});

$('#periodStart').datepicker({
    dateFormat: 'yy-mm-dd',
    changeYear: true

});

$('#periodEnd').datepicker({
    dateFormat: 'yy-mm-dd',
    changeYear: true

});


$('.load_kras').click(function (e) {
   e.preventDefault();
   $.ajax({
        url: '/dashboard/agreement/kra/list/',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            $('#kra_list').empty().append(
                $.map(data.kras, function (obj) {
                    return '<option value="' +obj.kra_id +'">' + obj.kra +'</option>';
                }).join());
        }
    });

});

$('.load_kpis').click(function (e) {
   e.preventDefault();
   $.ajax({
        url: '/dashboard/agreement/indicators/list/',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            $('#kpi_list').empty().append(
                $.map(data.indicators, function (obj) {
                    return '<option value="' +obj.kpi_id +'">' + obj.description +'</option>';
                }).join());
        }
    });
});



$('#saveKRA').click(function (e) {
    e.preventDefault();
    var csrftoken = getCookie('csrftoken');
    var kra = $("#kra").val();
    var weight = $('#weight').val();
    var pa_id = $('#pa_id').val();
    $.ajax({
        url: '/dashboard/agreement/kra/create/',
        type: 'post',
        dataType: 'json',
        data : {
            kra : kra,
            self_weight : weight,
            pa_id : pa_id
        },
        beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
         },
        success: function (data) {
        if (data.results = 'ok') {
            clearKRAForm();
            listKRAs();
            $('#kra_new').fadeOut('slow');
        }
        else {
            }
        }
    });

});

function clearKRAForm() {
    $("#kra").val('');
    $('#weight').val('');
    $('#kra_supervisor').val('');
}


$('#addAnotherKRA').click(function (e) {
    e.preventDefault();
    let csrftoken = getCookie('csrftoken');
    let kra = $("#kra").val();
    let weight = $('#weight').val();
    let pa_id = $('#pa_id').val();
    $.ajax({
        url: '/dashboard/agreement/kra/create/',
        type: 'post',
        dataType: 'json',
        data : {
            kra : kra,
            self_weight : weight,
            pa_id : pa_id,
        },
        beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
         },
        success: function (data) {
            if (data.status === 200) {
                toastr.success(data.message);
                $('#kra_list').slideDown('slow');
                 clearKRAForm();
            }
            else if(data.status === 52) {
                    toastr.error(data.message);
                }
            }
    });
});


function listKRAs(){
    $.ajax({
        url: '/dashboard/agreement/kra/list/',
        type: 'get',
        dataType: 'json',
        success: function (data) {
            if (data.status === 200) {
                toastr.info(data.message);
                $('#_kras').empty().append(
                    $.map(data.kras, function (kra, index) {
                        return '<tr><td>' + (index + 1) + '</td>' + '<td>' + kra.kra + '</td>'
                            + '<td>' + kra.self_weight + '</td>' +
                            '<td><input type="hidden"><button type="button" class="btn btn-info btn-circle" ' +
                            'value="' + kra.kra_id + '" id="updateKRA" data-toggle="modal" data-target="#updateKRAModal"><i class="fa fa-edit"></i></td>' +
                            '<td><button type="button" class="btn btn-warning btn-circle" value="' + kra.kra_id + '" id="deleteKRA"><i class="fa fa-times"></i></td>' +
                            '</tr>';
                    }).join());
            }
            else if (data.status === 51){
                $('#myKras').hide();
                toastr.warning(data.message);
            }
        }
    });
}

/*
* PDP starts here
* CRUD process
* */


$('#training_needs').click(function (e) {
    e.preventDefault();
     closeEpmsForms();
    $('#capture_pdp').slideDown('slow');
});

$('#trainingList').click(function (e) {
    e.preventDefault();
     listTrainingNeeds();
});

$('#view_pdp_kras').click(function (e) {
    e.preventDefault();
    getPDPKRAS()
});

function getPDPKRAS(){
    /*
    * get list of kras that are available
    * allow user to select a kra that they will attach the measurable output to
    * populate the value on the text area, with kra id
    * */
    $.ajax({
        url: '/dashboard/agreement/kra/list/',
        type: 'get',
        dataType: 'json',
        success: function (data) {
            $('#pdp_kras').empty().append(
                $.map(data.kras, function (kra, index) {
                    return '<tr><td>' + (index +1 )   + '<input type="hidden" id="pdp_kra_id" value="'+kra.kra_id+'">'+ '</td>' + '<td>' + kra.kra +'</td>' + '<td>' + '<input type="radio" name="pdp_kra"  value="'+kra.kra+'">'+'</td></tr>';
            }).join());
        }
    });
}


$('#attach_pdp_kra').click(function(e){
   //get data-id attribute of the clicked element
    e.preventDefault();
    var mo_kra =  $("#list_pdp_kras input[type='radio']:checked").val(); //$('#pdp_kra').val();
    var kra_id = $('#pdp_kra_id').val();
    //populate the textbox
    $('#pdp_kra_val').val(mo_kra);
    $('#new_pdp_kra_id').val(kra_id);
});

$('#savePDP').click(function (e) {
    e.preventDefault();
    var kra_id = $('#new_pdp_kra_id').val();
    var t_type = $('#t_type').val();
    var outcome = $('#outcome').val();
    var frame = $('#frame').val();
    createPDP(kra_id, t_type, outcome, frame)
});

$(document).on('click', '#updatePDP', function() {
    var _id = $(this).val();
    loadPDP(_id);
});

function createPDP(kra_id, t_type, outcome, frame) {
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url: '/dashboard/agreement/training/create/',
        type: 'post',
        dataType: 'json',
        data : {
            kra_id : kra_id,
            t_type: t_type,
            outcome : outcome,
            frame : frame
        },
        beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function (data) {
            if(data.results === 'ok'){
                listPDPObjects();
            }
        }
    });
}

$('#save_pdp_update').click(function (e) {
    e.preventDefault();
    var pdp_id = $('#pdp_id').val();
    var t_type = $('#update_t_type').val();
    var outcome = $('#update_outcome').val();
    var frame = $('#update_frame').val();
    updatePDP(pdp_id, t_type, outcome, frame)
});


function updatePDP(pdp_id, t_type, outcome, frame) {
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url: '/dashboard/agreement/training/update/',
        type: 'post',
        dataType: 'json',
        data : {
            pdp_id : pdp_id,
            t_type: t_type,
            outcome : outcome,
            frame : frame
        },
        beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function (data) {
            console.log(data.results);
            clearOutputs()
        }

    });
}


$(document).on('click', '#delete_pdp', function(e) {
    e.preventDefault();
    var pdp_id = $(this).val();
    deletePDP(pdp_id);
    $(this).closest("tr").remove();
});

function deletePDP(_pdp_id) {
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url: '/dashboard/agreement/training/delete/',
        type: 'post',
        dataType: 'json',
        data : {
            pdp_id : _pdp_id
        },
        beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function (data) {
           if(data.results === 'ok'){
               listTrainingNeeds();
           }
        }

    });
}

function listTrainingNeeds(){
    $.ajax({
        url: '/dashboard/agreement/training/list/',
        type: 'get',
        dataType: 'json',
        success: function (data) {
            toastr.info("Loading Personal Training Needs");
            $('#pdp_list').empty().append(
                $.map(data.obj, function (pdp, index) {
                    return '<tr><td>' + (index +1 )   + '</td>' + '<td>' + pdp.t_type +'</td>'
                        + '<td>' + pdp.outcome +'</td>' +
                        '<td><input type="hidden"><button type="button" class="btn btn-info btn-circle" ' +
                        'value="'+ pdp.pdp_id +'" id="updatePDP" data-toggle="modal" data-target="#updatePDPModal"><i class="fa fa-edit"></i></td>' +
                        '<td><button type="button" class="btn btn-warning btn-circle" value="'+ pdp.pdp_id +'" id="delete_pdp"><i class="fa fa-times"></i></td>' +
                        '</tr>';
            }).join());
        }
    });
}



function loadPDP(_id) {
   $.ajax({
        url: '/dashboard/agreement/training/load/',
        type: 'get',
        dataType: 'json',
        data : {
            pdp_id : _id
        },
        success: function (data) {
                $('#pdp_id').val(data.obj[0].pdp_id);
                $('#update_t_type').val(data.obj[0].t_type);
                $('#update_outcome').val(data.obj[0].outcome);
                $('#update_frame').val(data.obj[0].time_frame);
            }
        });
}



/*
* PDP ENDS here
* */




/*
* This section is for staff KPI
* CRUD process
* */

$(document).on('click','#create_mo', function (e){
   //get data-id attribute of the clicked element
    var mo_kra = $(this).data('id');
    //populate the textbox
    $('#mo_kra_id').val(mo_kra);
});


$('#save_target').click(function (e) {
    e.preventDefault();
    saveTarget()
});

$(document).on('click','#add_sel_staff_kra', function (e) {
    e.preventDefault();
    let kra = $("#outputs_kras input[type='radio']:checked").val();
    $('.staff_kpi_kra').val(kra);
});

$('#my_indicators').click(function (e) {
    e.preventDefault();
    listIndicators()

});

$('#save_staff_kpi').click(function (e) {
    e.preventDefault();
    saveStaffKpi()
});


function saveStaffKpi() {
    let csrftoken = getCookie('csrftoken');
    let kra_id = $("#kra_list option:selected" ).val();
    let kpi = $('#staff_kpi').val();
    let weight = $('#staff_kpi_weight').val();

    $.ajax({
        url: '/dashboard/agreement/indicators/create/',
        type: 'post',
        dataType: 'json',
        data : {
            kra_id : kra_id,
            kpi: kpi,
            weight : weight,
        },
        beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function (data) {
            if(data.status === 200){
                toastr.success(data.message);
                 clearOutputs();
            }
            else {
                toastr.warning(data.message);
            }
        }
    });
}


function listIndicators(){
    $.ajax({
        url: '/dashboard/agreement/indicators/list/',
        type: 'get',
        dataType: 'json',
        success: function (data) {
            toastr.info("Loading KPIs");
            $('#indicators_list').empty().append(
                $.map(data.indicators, function (kpi, index) {
                    return '<tr><td>' + (index +1 )   + '</td>' + '<td>' + kpi.description +'</td>'
                        + '<td>' + kpi.staff_weight +'</td>' +
                        '<td><button type="button" class="btn btn-warning btn-circle remove_kpi" value="'+ kpi.kpi_id +'" id=""><i class="fa fa-times"></i></td>' +
                        '</tr>';
            }).join());
        }
    });
}


$(document).on('click', '#update_kpi_modal', function() {
    let kpi_id = $(this).val();
    loadKpi(kpi_id);

});

$(document).on('click', '.remove_kpi', function() {
    let kpi_id = $(this).val();
    deleteKpi(kpi_id);

});

$('#tf_start').datepicker({
    dateFormat: 'yy-mm-dd',
    changeYear: true
});

$('#tf_end').datepicker({
    dateFormat: 'yy-mm-dd',
    changeYear: true
});


function deleteKpi(_id) {
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url: '/dashboard/agreement/indicators/delete/',
        type: 'post',
        dataType: 'json',
        data : {
            id : _id
        },
        beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function (data) {
            if(data.status === 200){
                toastr.success(data.message);
                listIndicators();
            }
            else {
                toastr.warning(data.message, 'status code:' +  data.status)
            }
        }
    });
}


function loadKpi(kpi_id) {
   $.ajax({
        url: '/dashboard/agreement/indicators/kpi/',
        type: 'get',
        dataType: 'json',
        data : {
            kpi_id : kpi_id
        },
        success: function (kpis) {
                $('#staff_kpi_kra').val(kpi.kpi_id);
                $('#update_staff_kpi').val(kpi);
                $('#update_staff_kpi_weight').val(kpi.self_weight);
            }
        });
}


function saveTarget() {
    let csrftoken = getCookie('csrftoken');
    let kpi_id = $('#kpi_list option:selected').val();
    let baseline = $('#baseline').val();
    let evidence = $('#evidence').val();
    let target = $('#target').val();
    $.ajax({
        url: '/dashboard/agreement/targets/create/',
        type: 'post',
        dataType: 'json',
        data : {
            kpi_id : kpi_id,
            baseline : baseline,
            target : target,
            evidence : evidence,
        },
        beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function (data) {
            if(data.status === 200){
                toastr.success(data.message);
                 clearOutputs();
            }
            else {
                toastr.warning(data.message);
            }
        }
    });
}

$(document).on('click', '.kpis', function() {
    targetIndicators();
});

$(document).on('click', '#updateKRA', function() {
    var kra_id = $(this).val();
    loadKRA(kra_id);
});

$(document).on('click', '#deleteMO', function() {
    var _id = $(this).val();
    deleteMO(_id);
    $(this).closest("tr").remove();
});

$('#add_staff_kpi').click(function (e) {
    e.preventDefault();
    let _id = $("#indicators input[type='radio']:checked").val();
    let kpi = $("#indicators input[type='radio']:checked").data("kpitgt");
    $('.staff_kpi_target').val(kpi);
    $('#kpi_target_id').val(_id);

});

function targetIndicators(){
    /*
    * get list of kpis that are available
    * allow user to select a kra that they will attach the measurable output to
    * populate the value on the text area, with kpi id
    * */
    $.ajax({
        url: '/dashboard/agreement/indicators/list/',
        type: 'get',
        dataType: 'json',
        success: function (data) {
            $('#indicators').empty().append(
                $.map(data.indicators, function (kpi, index) {
                    return '<tr><td>' + (index +1 )  + '<input type="hidden" id="kpi_id" value="'+ kpi.description +'">'+ '</td>' + '<td>' + kpi.description +'</td>' + '<td>' +
                        '<input type="radio" name="target_kpi" ' + 'data-kpitgt="'+ kpi.description +'" value="'+kpi.kpi_id+'" class="staff_kpi_id">'+'</td></tr>';
            }).join());
        }
    });
}


function deleteMO(_id) {
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url: '/dashboard/agreement/delete_mo/',
        type: 'post',
        dataType: 'json',
        data : {
            id : _id
        },
        beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function (data) {
            if(data.status === 200){
                toastr.success(data.message);
                listOutputs();
            }
            else {
                toastr.warning(data.message, 'status code:' +  data.status)
            }
        }
    });
}

/*
* Outputs CRUD ends here
* */


/*
* KRA CRUD starts here
 */
function loadKRA(kra_id) {
   $.ajax({
        url: '/dashboard/agreement/kra/fetch/',
        type: 'get',
        dataType: 'json',
        data : {
            kra_id : kra_id
        },
        success: function (data) {
                $('#kra_id').val(data.kra[0].kra_id);
                $('#update_kra_content').val(data.kra[0].kra);
                $('#update_kra_weight').val(data.kra[0].self_weight);
                if (data.kra[0].supervisor__name__user__employee_code == null){
                    $('#updateKRASuperv').val('');
                }
                else {
                    $('#updateKRASuperv').val(data.kra[0].supervisor__name__user__employee_code + ' ' +
                                            data.kra[0].supervisor__name__first_name + ' ' +
                                            data.kra[0].supervisor__name__last_name
                                         )
                }

            }
        });
}

$('#update_kra').click(function (e) {
    e.preventDefault();
    let kra_id = $('#kra_id').val();
    let kra = $('#update_kra_content').val();
    let weight = $('#update_kra_weight').val();
    updateKRA(kra_id, kra, weight)
});

function updateKRA(kra_id, kra, weight) {
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url: '/dashboard/agreement/kra/update/',
        type: 'post',
        dataType: 'json',
        data : {
            kra_id : kra_id,
            kra : kra,
            self_weight : weight,
        },
        beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function (data) {
            if (data.status === 200) {
                toastr.success(data.message)
            }
            else {
                toastr.warning(data.message)
            }
            }
        });
    }


$(document).on('click', '#deleteKRA', function() {
    let kra_id = $(this).val();
    deleteKRA(kra_id);
    toastr.info("KRA deleted successfully");
    $(this).closest("tr").remove();
});


function deleteKRA(kra_id) {
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url: '/dashboard/agreement/kra/delete/',
        type: 'post',
        dataType: 'json',
        data : {
            kra_id : kra_id
        },
        beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
    });
}

function addYear() {
   var currentYear = new Date().getFullYear();
   for (var i = 1; i <= 2; i++ ) {
        $("#finYear").append(
            $("<option></option>")
                .attr("value", currentYear)
                .text(currentYear)
        );
        currentYear++;
   }
}


/*

KRA Review starts here
 */

$('#review_period_start').datepicker({
    dateFormat: 'yy-mm-dd',
    changeYear: true

});

$('#review_period_end').datepicker({
    dateFormat: 'yy-mm-dd',
    changeYear: true

});

function close_review_forms(){
    $('#start_review').hide();
}

$('#review_parent').click(function (e) {
    e.preventDefault();
    closeAllEpmsForms();
    review_kras();
    $('#start_review').fadeIn();
});


$('#create_review').click(function(e){
    e.preventDefault();
    $.ajax({
        url: '/home/review/create/',
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
            $('.review').fadeIn('slow');
        },
        success: function (data) {
            $(".review").html(data.html_form);
        }
    });

});

$(document).on('click',"#submit_emp_review",function (e) {
    e.preventDefault();
    submit_employee_review();
});


$(document).on('click', '.save_kra_review', function() {
    let kra_id = $(event.target).closest('tr').find('.kra_id').val();
    let self_rating =  $(event.target).closest('tr').find('.review_rating_staff').val();
    create_or_update_kra_rating(kra_id, self_rating)

});


function create_or_update_kra_rating(kra_id, self_rating) {
    let csrftoken = getCookie('csrftoken');
    $.ajax({
        url: '/dashboard/review/kra/rating/update/',
        type: 'post',
        dataType: 'json',
        data: {
            kra_id: kra_id,
            self_rating: self_rating
        },
        beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
         },
        success: function (data) {
            if(data.status === 200) {
                toastr.success(data.message)
            }
            else if(data.status === 51){
                toastr.error(data.message)
            }
        }
    })
}

function review_kras() {
    $.ajax({
        url: '/dashboard/review/kra/review/',
        type: 'get',
        dataType: 'json',
        success: function (data) {
            if (data.status === 200) {
                toastr.info(data.message);
                $('#kra_review_staff_edit').empty().append(
                    $.map(data.kras, function (kra, index) {
                        return '<tr>' +
                                    '<td>' + (index + 1) + '</td>' + '<td>' + kra.kra + '</td>' + '<input type="hidden" value= ' + kra.kra_id + ' class="kra_id">' +
                                    '<td>' + '<input type="text" readonly class="col-sm-8 form-control" value= '+ kra.self_weight +' >' + '</td>' +
                                    '<td>' + '<input type="text" id="" class="col-sm-8 form-control review_rating_staff" value=' + kra.review__self_rating + '>' + '' +
                                    '<td>' + '<input type="text" id="" readonly class="col-sm-8 form-control" value="">' + '</td>' +
                                    '<td>' + '<div class="custom-file">' + '<input type="file" accept="image/*" name="file" id="evidence" class="hide">' + '</div>'+ '</td>' +
                                    '<td>' + '<button type="button" class="btn btn-success btn-sm save_kra_review">Save</button>' + '</td>' +
                               '</tr>';
                    }).join());
            }
            else if (data.status === 51){
                $('#myKras').hide();
                toastr.warning(data.message);
            }
        }
    });
}


function submit_employee_review(){
    let csrftoken = getCookie('csrftoken');
    let rev_type = $("#review_type").val();
    let start = $("#review_period_start").val();
    let end = $("#review_period_end").val();
    $.ajax({
        url: '/dashboard/review/bulk/create/',
        type: 'post',
        dataType: 'json',
        data : {
            rev_type : rev_type,
            period_start : start,
            period_end : end,

        },
        beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
         },
        success: function (data) {
        if (data.form_is_valid) {
           // <-- This is just a placeholder for now for testing
        }
        else {
              // $(".review").html(data.html_form);

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
