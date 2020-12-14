$(document).ready(function() {

/*
* Block to Capture a new project starts
*/

$('#project_start_date').datepicker({
    dateFormat: 'yy-mm-dd',
    changeYear: true

});

$('#project_end_date').datepicker({
    dateFormat: 'yy-mm-dd',
    changeYear: true

});

$('#update_project_end').datepicker({
    dateFormat: 'yy-mm-dd',
    changeYear: true

});

$('#programmesProjects').click(function (e) {
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

    //app
    $('#capture_app').hide();

    //epm
    $('#pa_new').hide();
    $('#start_review').hide();

    $('#capture_overview').hide();
    toastr.info("Programmes & Project Management", "Module Information")
});


$('#programmes').click(function (e) {
    e.preventDefault();
    let programme = $("#programmes option:selected" ).val();
    readSubprogrammes(programme)
});


<!-- === event bindings start -->

$('#addProject').click(function (e) {
    e.preventDefault();
    var name = $('#project_name').val();
    var ptype = $('#project_type').val();
    var pstart = $('#project_start_date').val();
    var pend = $('#project_end_date').val();
    var temps = $('#templates').val();
    var sponsor = $('#sponsor').val();
    var budget = $('#budget').val();
    var plan = $('#plan').val();
    var rcycle = $('#reporting_cycle').val();
    var risk = $('#risk').val();
    var comments = $('#comments').val();
    var prog = $('#programmes').val();
    var details = $('#details').val();
    var sign = $('#sign_proj').is(':checked');

    saveProject(name, ptype, pstart, pend, temps, sponsor, budget, plan, rcycle, risk, comments, prog, details, sign)
});


$('#view_projects').click(function (e) {
    e.preventDefault();
    getEmployeeProjects();
     $('#capture_overview').hide();
    $('#capture_project').hide();
    $('#contributors').hide();
    $('#add_strat_obj').hide();
    $('#add_contr').hide();
    $('#update_emp_project').hide();
    $('#expenditure_dash').hide();
    $('#ppm_dash').hide();
    $('#capture_transfers').hide();
    $('#capture_current_payments').hide();
    $('#capture_capital_assets').hide();
    $('#list_emp_projects').fadeIn();

});

$('#add_project').click(function (e) {
    e.preventDefault();
    getEmployeeInfo();
    $('#capture_overview').hide();
    $('#add_strat_obj').hide();
    $('#list_emp_projects').hide();
    $('#contributors').hide();
    $('#add_contr').hide();
    $('#update_emp_project').hide();
    $('#expenditure_dash').hide();
    $('#ppm_dash').hide();

    $('#capture_transfers').hide();
    $('#capture_current_payments').hide();
    $('#capture_capital_assets').hide();

    $('#capture_project').fadeIn();
});


$(document).on('click', '#updateEmpProject', function() {
    var proj_id = $(this).val();
    loadEmployeeProject(proj_id);
    $('#list_emp_projects').hide();
    $('#capture_overview').hide();
    $('#capture_project').hide();
    $('#contributors').hide();
    $('#add_strat_obj').hide();
    $('#add_contr').hide();
    $('#expenditure_dash').hide();
    $('#ppm_dash').hide();

    $('#capture_transfers').hide();
    $('#capture_current_payments').hide();
    $('#capture_capital_assets').hide();

    $('#update_emp_project').fadeIn();

});

$('#updateProjectProgress').click(function (e) {
    e.preventDefault();
    let name = $('#update_project_name').val();
    let temp = $('#update_templates').val();
    let sponsor = $('#update_sponsor').val();
    let budget = $('#update_budget').val();
    let plan = $('#update_plan').val();
    let status = $("#update_status option:selected" ).val();
    let risk = $('#update_risk').val();
    let comments = $('#update_comments').val();
    let details  = $('#update_details').val();
    let id = $('#pro_id').val();
    let end_date = $('#update_project_end').val();
    let sig = $('#sign_proj').is('checked');
    updateProject(name, temp, sponsor, budget, plan, status, risk, comments, details, id, end_date, sig)
});

<!-- === event bindings end -->

function readSubprogrammes(programme) {

    $.ajax({
        url: '/dashboard/ppm/subprogramme/read/',
        type: 'GET',
        dataType: 'json',
        data: {programme: programme},
        success: function (data) {
            // Populate programmes obj into a dropdown list
            $('#sub_programmes').empty().append(
                $.map(data.sub_progs, function (p) {
                    return '<option value="' +p.id +'">'+ p.name +'</option>';
                }).join());
        }
    });
}



function updateProject(name, temp, sponsor, budget, plan, status, risk, comments, details, id, end_date, sig) {

    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url: '/dashboard/ppm/update_employee_project/',
        type: 'POST',
        dataType: 'json',
        data : {
            id : id,
            name : name,
            templates : temp,
            sponsor : sponsor,
            budget : budget,
            plan : plan,
            details : details,
            risk : risk,
            comments : comments,
            status : status,
            end_date : end_date,
            sig: sig
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
            else if(data.status === 52){
                toastr.error(data.message)
                }
        }
    });
}

function loadEmployeeProject(_id) {
    $.ajax({
        url: '/dashboard/ppm/projects/project/read/',
        type: 'GET',
        dataType: 'json',
        data: {
            proj: _id
        },
        success: function (data) {

            if(data.write === false){
                $('#update_branch').val(data.project[0].branch__name).prop("disabled", "disabled");
                $('#update_component').val(data.project[0].component__name).prop("disabled", "disabled");
                $('#update_project_start').val(data.project[0].start_date).prop("disabled", "disabled");
                $('#update_project_end').val(data.project[0].end_date).prop("disabled", "disabled");
                $('#update_programme').val(data.project[0].programme__name).prop("disabled", "disabled");
                $('#number').val(data.project[0].number).prop("disabled", "disabled");
                $('#update_pm').val(data.project[0].project_manager__first_name + ' ' +
                    data.project[0].project_manager__last_name).prop("disabled", "disabled");
                $('#update_templates').val(data.project[0].templates).prop("disabled", "disabled");
                $('#update_plan').val(data.project[0].plan).prop("disabled", "disabled");
                $('#update_budget').val(data.project[0].budget).prop("disabled", "disabled");
                $('#update_risk').val(data.project[0].risk).prop("disabled", "disabled");
                $('#update_comments').val(data.project[0].comments).prop("disabled", "disabled");
                $('#update_project_type').val(data.project[0].project_type__name).prop("disabled", "disabled");
                $('#update_project_name').val(data.project[0].name).prop("disabled", "disabled");
                $('#update_sponsor').val(data.project[0].sponsor).prop("disabled", "disabled");
                $('#pro_id').val(data.project[0].id).prop("disabled", "disabled");
                $('#update_details').val(data.project[0].details).prop("disabled", "disabled");
                $('.signature').hide();
                /*
                Populate programmes obj into a dropdown list
                 */
                var status_opts = [];
                status_opts.push(data.project[0].status__name);
                $.map(data.status, function (p) {
                    status_opts.push(p.name);
                    }).join();

                $.each(status_opts, function(key, value) {
                    $('#update_status').empty().append($("<option value=' + k + '></option>")
                                .attr("value",key)
                                .text(value)
                        );
                });
                $('#update_status').prop("disabled", "disabled");
            }
            else {

                $('#update_branch').val(data.project[0].branch__name);
                $('#update_component').val(data.project[0].component__name);
                $('#update_project_start').val(data.project[0].start_date);
                $('#update_project_end').val(data.project[0].end_date);
                $('#update_programme').val(data.project[0].programme__name);
                $('#number').val(data.project[0].number);
                $('#update_pm').val(data.project[0].project_manager__first_name + ' ' +
                    data.project[0].project_manager__last_name);
                $('#update_templates').val(data.project[0].templates);
                $('#update_plan').val(data.project[0].plan);
                $('#update_budget').val(data.project[0].budget);
                $('#update_risk').val(data.project[0].risk);
                $('#update_comments').val(data.project[0].comments);
                $('#curr_project_type').val(data.project[0].project_type__name);
                $('#update_project_name').val(data.project[0].name);
                $('#update_sponsor').val(data.project[0].sponsor);
                $('#pro_id').val(data.project[0].id);
                $('#update_details').val(data.project[0].details);
                /*
                Populate programmes obj into a dropdown list
                 */

                $('#update_status').empty().append(
                    $.map(data.status, function (obj) {
                        return '<option value="' +obj.id +'">' + obj.name +'</option>';
                    }).join());
            }

        }
    });
}


function saveProject(name, ptype, pstart, pend, temps, sponsor, budget, plan, rcycle, risk, comments, prog, details, sign) {
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url: '/dashboard/ppm/add_project/',
        type: 'POST',
        dataType: 'json',
        data : {
            name : name,
            p_type : ptype,
            p_start : pstart,
            p_end : pend,
            temps : temps,
            sponsor : sponsor,
            budget : budget,
            plan : plan,
            r_cycle : rcycle,
            risk : risk,
            comments : comments,
            programme : prog,
            details: details,
            sign: sign
        },
        beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function (data) {
            if(data.status === 200){
                toastr.success(data.message)
            }
            else {
                toastr.error(data.message, "Status Code:" + data.status)
            }
        }
    });
}


function getEmployeeInfo() {

     $.ajax({
        url: '/dashboard/ppm/get_employee_info/',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            $('#org').val(data.emp.organisation__name);
            $('#branch').val(data.emp.branch__name);
            $('#component').val(data.emp.component__name);
            /*
            Populate programmes obj into a dropdown list
             */
            $('#programmes').empty().append(
                $.map(data.progs, function (p) {
                    return '<option value="' +p[0].id +'">'+ p[0].name +'</option>';
                }).join());
              /*

              /*
            Populate project types into a dropdown list
             */
            $('#project_type').empty().append(
                $.map(data.types_, function (p) {
                    return '<option value="' +p.id +'">'+ p.name +'</option>';
                }).join());

        }
    });

}

function getEmployeeProjects() {
    
    $.ajax({
        url: '/dashboard/ppm/projects/read',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            $('#emp_projects').empty().append(
                $.map(data.emp_projects, function (proj, index) {
                    return '<tr><td>' + (index +1 )   + '</td>' + '<td>' + proj.name +'</td>'
                        + '<td>' + proj.programme__name +'</td>'  + '<td>' + proj.status__name +'</td>' + '<td>' + proj.start_date +'</td>' + '<td>' + proj.end_date +'</td>' +
                        '<td><input type="hidden"><button type="button" class="btn btn-info btn-circle" ' +
                        'value="'+ proj.id +'" id="updateEmpProject" data-toggle="modal" data-target="#updateEmpProjectModal"><i class="fa fa-edit"></i></td>' +
                        '<td><button type="button" class="btn btn-warning btn-circle" value="'+ proj.id +'" id="deleteProject"><i class="fa fa-times"></i></td>' +
                        '</tr>';
            }).join());
            // if(data.access == "1"){
            //     $('#updateEmpProject').attr("disabled",true);
            //     $('#deleteProject').attr("disabled",true);
            // }
        }
    })
}

/*
Block to Capture new project ends
 */


/*
Start Block  Add Project Contributor
*/


$('#add_project_contr').click(function (e) {
    e.preventDefault();
    getActiveProject();
    $('#capture_overview').hide();
    $('#capture_project').hide();
    $('#list_emp_projects').hide();
    $('#contributors').hide();
    $('#add_strat_obj').hide();
    $('#update_emp_project').hide();
    $('#expenditure_dash').hide();
    $('#ppm_dash').hide();

    $('#capture_transfers').hide();
    $('#capture_current_payments').hide();
    $('#capture_capital_assets').hide();

    $('#add_contr').fadeIn();

});


$('#save_contr').click(function (e) {
    e.preventDefault();
    let employee = $('#employee_code').val();
    let sign_pos = $('#queue_pos').val();
    let notes = $('#notes').val();
    let project = $('#project').val();
    addContributor(employee, sign_pos, notes, project)
});

function getActiveProject() {
    $.ajax({
        url: '/dashboard/ppm/get_active_project/',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            $('#project').empty().append(
                $.map(data.projects, function (obj) {
                return '<option value="' +obj.number +'">' + obj.name +'</option>';
            }).join());
        }
    });
}

function addContributor(contr, pos, notes, project){
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url: '/dashboard/perms/add_contributor/',
        type: 'POST',
        dataType: 'json',
        data : {
            employee_code: contr,
            sign_pos: pos,
            notes: notes,
            project: project
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
            if(data.status === 41){
                    toastr.error(data.message)
                }
            else if(data.status === 52){
                    toastr.error(data.message)
                }
            }
    });
}

/*
End Block to Add Project Contributor
*/


/*
Start Block view project
*/

$('#view_project').click(function (e) {
    e.preventDefault();
    loadContrProject();
    $('#contributor_project').fadeIn('slow');

});


function loadContrProject() {
    $.ajax({
        url: '/dashboard/ppm/get_contr_project/',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            $('#con_branch').val(data.project[0].branch__name);
            $('#con_component').val(data.project[0].component__name);
            $('#con_start_date').val(data.project[0].start_date);
            $('#con_end_date').val(data.project[0].end_date);
            $('#con_programme').val(data.project[0].programme__name);
            $('#con_project_no').val(data.project[0].number);
            $('#con_proj_manager').val(data.project[0].project_manager__first_name + ' ' +
                data.project[0].project_manager__last_name);
            $('#con_templates').val(data.project[0].templates);
            $('#con_plan').val(data.project[0].plan);
            $('#con_budget').val(data.project[0].budget);
            $('#con_risk').val(data.project[0].risk);
            $('#con_comments').val(data.project[0].comments);
            $('#con_type').val(data.project[0].project_type__name);
            $('#con_name').val(data.project[0].name);
            $('#con_sponsor').val(data.project[0].sponsor);
            $('#number').val(data.project[0].number);
            $('#con_details').val(data.project[0].details);
            $('#con_manager').val(data.project[0].project_manager__first_name + " " + data.project[0].project_manager__last_name);
            /*
            Populate programmes obj into a dropdown list
             */
            var status_opts = [];
            status_opts.push(data.project[0].status__name);
            $.map(data.status, function (p) {
                status_opts.push(p.name);
                }).join();

            $.each(status_opts, function(key, value) {
                $('#con_status').append($("<option value=' + k + '></option>")
                            .attr("value",key)
                            .text(value)
                    );
            });
             if(data.access == '1'){
                $('input[name=con_token]').attr("disabled",true);
                $('#con_signed').attr("disabled",true);
             }
        }
    });
}

$('#con_signed').click(function (e) {
    e.preventDefault();
    var token = $('input[name=con_token]:checked').val();
    var proj = $('#number').val();
    saveToken(token, proj)
});


function saveToken(token, proj) {

    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url: '/dashboard/ppm/save_token/',
        type: 'POST',
        dataType: 'json',
        data : {
            token : token,
            project: proj
        },
        beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function (data) {
            if(data.results === 'OK'){
                console.log(data.message)
            }
            else {
                console.log(data.message)
            }
        }
    });
}

/*
End Block view project
*/


/*
Start Block view contributors
*/

$('#view_contributors').click(function (e) {
    e.preventDefault();
    projectContributors();
    $('#capture_overview').hide();
    $('#capture_project').hide();
    $('#list_emp_projects').hide();
    $('#add_strat_obj').hide();
    $('#add_contr').hide();
    $('#update_emp_project').hide();
    $('#expenditure_dash').hide();
    $('#ppm_dash').hide();

    $('#capture_transfers').hide();
    $('#capture_current_payments').hide();
    $('#capture_capital_assets').hide();

    $('#contributors').fadeIn();
});


function projectContributors() {

    $.ajax({
        url: '/dashboard/ppm/contributors/read/',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            $('#proj_contr').empty().append(
                $.map(data.people, function (person, index) {
                    return '<tr><td>' + (index +1 )   + '</td>' + '<td>' + person.employee__first_name +'</td>'
                        + '<td>' + person.employee__last_name +'</td>' + '<td>' + person.project__name +'</td>' + '<td>' + person.employee__user__employee_code +'</td>' + '<td>' + person.queue_position +'</td>' +
                        '<td><input type="hidden"><button type="button" class="btn btn-info btn-circle" ' +
                        'value="'+ '' +'" id="#" data-toggle="modal" data-target="#"><i class="fa fa-edit"></i></td>' +
                        '<td><button type="button" class="btn btn-warning btn-circle" value="'+ '' +'" id=""><i class="fa fa-times"></i></td>' +
                        '</tr>';
            }).join());
        }
    })
}

 $('.sign').click(function () {
      $('#sign_proj').prop('checked', false);
        swal({
            title: "Are you sure you want to sign?",
            text: "You will not be able to undo this step after submitting",
            type: "info",
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "Yes, sign it",
            closeOnConfirm: false
        }, function () {
            swal("Signed", "Your signature has been added successfully", "success");
             $('#sign_proj').prop('checked', true);
        });
    });
/*
End Block view contributors
*/




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
