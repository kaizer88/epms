$(document).ready(function() {


/* app starts */

$('#appModule').click(function (e) {
    e.preventDefault();
    $('#add_strat_obj').hide();
    $('#capture_project').hide();
    $('#list_emp_projects').hide();
    $('#contributors').hide();
    $('#add_contr').hide();
    $('#update_emp_project').hide();
    $('#expenditure_dash').hide();
    $('#ppm_dash').hide();

    //mtef
    $('#capture_capital_assets').hide();
    $('#capture_current_payments').hide();
    $('#capture_transfers').hide();


    //epm
    $('#pa_new').hide();
    $('#start_review').hide();

    $('#capture_overview').hide();
    toastr.info("Annual Performance Plan", "Module Information")
});


$('#captureAPP').click(function (e) {
    e.preventDefault();
   $('#capture_app').fadeIn();

   makeContext()

});


$('#load_objectives').click(function (e) {
    e.preventDefault();
    let subprog_id = $(".app_subprogramme option:selected" ).val();
    loadObjectives(subprog_id)
});


$('#load_outputs').click(function (e) {
    e.preventDefault();
    let obj_id = $(".app_strat_objective option:selected" ).val();
    loadOutputs(obj_id)
});

$('#load_kpis').click(function (e) {
    e.preventDefault();
    let out_id = $(".app_strat_outputs option:selected" ).val();
    loadKPIS(out_id)
});


$('#load_targets').click(function (e) {
    e.preventDefault();
    let kpi_id = $(".app_kpis option:selected" ).val();
    loadTargets(kpi_id);
});

$('#target_start_date').datepicker({
        dateFormat: 'yy-mm-dd',
        changeYear: true
    });

$('#target_end_date').datepicker({
    dateFormat: 'yy-mm-dd',
    changeYear: true
});

$('.clear_risk').click(function (e) {
    e.preventDefault();

     let risk = $('#app_risks').val();
    $('.quarterly_risks').append("<li>" + risk + "<input type='hidden' class='risks' data-risk= '" + risk + "' >" + "</li>");

    $('#app_risks').val("")
});


$('#save_app').click(function (e) {
    e.preventDefault();

    let subprog = $('.app_subprogramme option:selected').val();
    let objective = $('.app_strat_objective option:selected').val();
    let output = $('.app_strat_outputs option:selected').val();
    let kpi = $('.app_kpis option:selected').val();
    let ann_target = $('.app_annual_targets option:selected').val();

    let start = $('#target_start_date').val();
    let end = $('#target_end_date').val();
    let quarter = $(".quarter option:selected" ).val();
    let baseline = $('#baseline').val();
    let evidence = $('#evidence').val();

    let risks = $(".risks").map(function () {
            return {"risk": $(this).attr("data-risk")};
        }).get();

    saveApp(subprog, objective, output, kpi, ann_target, start, end, baseline, evidence, quarter, risks)
    });



function saveApp(subprog, objective, output, kpi, ann_target, start, end, baseline, evidence, quarter, risks) {

    let csrftoken = getCookie('csrftoken');
        $.ajax({
            url: '/dashboard/app/framework/targets/create/',
            method: 'POST',
            dataType: 'json',
            data: {
                subprog: subprog,
                objective: objective,
                output: output,
                kpi: kpi,
                ann_target: ann_target,
                start: start,
                end: end,
                baseline: baseline,
                evidence: evidence,
                quarter: quarter,
                risks: JSON.stringify({risks: risks}),
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


function loadTargets(kpi_id) {

        $.ajax({
            url: '/dashboard/app/framework/app/targets/read/',
            type: 'GET',
            dataType: 'json',
            data: { _id: kpi_id},
            success: function (data) {
                $('.app_annual_targets').empty().append(
                    $.map(data.targets, function (targets) {
                        return '<option value="' +targets.id +'">' + targets.timeframe_start_d + " > " + targets.timeframe_end_d +'</option>';
                    }).join());
            }
        });

    }


function loadObjectives(subprog_id) {

        $.ajax({
            url: '/dashboard/app/framework/app/objectives/read/',
            type: 'GET',
            dataType: 'json',
            data: { _id: subprog_id},
            success: function (data) {
                $('.app_strat_objective').empty().append(
                    $.map(data.obj, function (obj) {
                        return '<option value="' +obj.objective__id +'">' + obj.objective__objective  +'</option>';
                    }).join());
            }
        });

    }


function loadOutputs(obj_id) {

        $.ajax({
            url: '/dashboard/app/framework/app/outputs/read/',
            type: 'GET',
            dataType: 'json',
            data: { _id: obj_id},
            success: function (data) {
                $('.app_strat_outputs').empty().append(
                    $.map(data.outputs, function (outputs) {
                        return '<option value="' +outputs.id +'">' + outputs.output  +'</option>';
                    }).join());
            }
        });

    }


function loadKPIS(out_id) {

        $.ajax({
            url: '/dashboard/app/framework/app/kpi/read/',
            type: 'GET',
            dataType: 'json',
            data: { _id: out_id},
            success: function (data) {
                $('.app_kpis').empty().append(
                    $.map(data.kpi, function (kpi) {
                        return '<option value="' +kpi.id +'">' + kpi.kpi  +'</option>';
                    }).join());
            }
        });

    }

function makeContext() {

    $.ajax({
            url: '/dashboard/app/framework/app/context/read',
            type: 'GET',
            dataType: 'json',
            success: function (data) {

                 /*subprogrammes  */
                $('.app_subprogramme').empty().append(
                    $.map(data.sub, function (obj) {
                        return '<option value="' +obj.id +'">' + obj.subprogramme +'</option>';
                    }).join());

                 /* targets */
                $('.app_annual_targets').empty().append(
                    $.map(data.targets, function (obj) {
                        return '<option value="' +obj.id +'">' + obj.targets +'</option>';
                    }).join());

                 /* organisational */
                $('#app_programme').val(data.info.employee[0].programme__name);
                $('#app_branch').val(data.info.employee[0].branch__name);
                $('#app_vision').val(data.strat[0].vision);
                $('#app_mandates').val(data.strat[0].revisions);
                $('#app_mission').val(data.strat[0].mission);
                $('#app_mtef').val(data.strat[0].mtef_budget);
                $('#app_s_analysis').val(data.strat[0].analysis);
                $('#app_org_risks').val(data.strat[0].risks);


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
