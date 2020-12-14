$(document).ready(function() {

    $('#strategicPlanModule').click(function (e) {
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
        toastr.info("Strategic Plan & Development", "Module Information")
    });

    $('#add_overview').click(function (e) {
        e.preventDefault();
        getEmployeeInfo();
        getBranchOverview();
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

        $('#capture_overview').fadeIn();
    });

    $('.add_sa').click(function (e) {
        e.preventDefault();
        let sa_desc = $('#sa_description').val();
        $('#sa').append("<li>" + sa_desc + "<input type='hidden' data-desc= '" + sa_desc + "' >" + "</li>");
    });

    $('.add_org_risks').click(function (e) {
        e.preventDefault();
        let org_risk_desc = $('#org_risk_description').val();
        $('#risks').append("<li>" + org_risk_desc + "<input type='hidden' data-org_risk_desc= '" + org_risk_desc + "' >" + "</li>");

    });

    $('#display_sa_list').click(function (e) {
        e.preventDefault();
        $('#situational_analysis_list').fadeIn('slow');

    });

    $('#display_org_risk_list').click(function (e) {
        e.preventDefault();
        $('#org_risks_list').fadeIn('slow');

    });


// values - overview - start

    $('#display_output_goal_list').click(function (e) {
        e.preventDefault();
        $('#strat_output_goals_list').fadeIn('slow');

    });


    $('.add_output_goals').click(function (e) {
        e.preventDefault();
        let goal = $('#strat_output_goal').val();
        $('#outcome_goals').append("<li>" + goal + "<input type='hidden' data-strat_output_goal= '" + goal + "' >" + "</li>");

    });

// values - end


// strategic output goals - overview - start

    $('.value_desc').focus(function() {
        $('#values_list').fadeIn('slow');
    });
    $('.value_desc').focusout(function() {
        $('#values_list').fadeOut();
    });


    $('.add_values').click(function (e) {
        e.preventDefault();
        let desc = $('.value_desc').val();
        $('#values').append("<li>" + desc + "<input type='hidden' data-value_desc= '" + desc + "' data-value='"+ desc + "' >" + "</li>");
        });


// strategic output overview - end

    function getEmployeeInfo() {

        $.ajax({
            url: '/dashboard/strategy/get_employee_info/',
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                $('#user_branch').val(data.emp[0].branch__name);

            }
        });

    }

    function getBranchOverview() {
         $.ajax({
            url: '/dashboard/strategy/overview/',
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                if(data.is_signed === false){
                    $('#mission').val(data.overview.mission);
                    $('#values').val(data.overview.values);
                    $('#priority_p').val(data.overview.priority_programme);
                    $('#vision').val(data.overview.vision);
                    $('#goals').val(data.overview.goals);
                    $('#revisions').val(data.overview.revisions);
                    $('#risks').val(data.overview.risks);
                    $('#mtef_budget').val(data.overview.mtef_budget);
                    $('#analysis').val(data.overview.analysis);
                }
                else if (data.is_signed === true){
                    $('#mission').val(data.overview.mission).prop("disabled", "disabled");
                    $('#values').val(data.overview.values).prop("disabled", "disabled");
                    $('#priority_p').val(data.overview.priority_programme).prop("disabled", "disabled");
                    $('#vision').val(data.overview.vision).prop("disabled", "disabled");
                    $('#goals').val(data.overview.goals).prop("disabled", "disabled");
                    $('#revisions').val(data.overview.revisions).prop("disabled", "disabled");
                    $('#risks').val(data.overview.risks).prop("disabled", "disabled");
                    $('#mtef_budget').val(data.overview.mtef_budget).prop("disabled", "disabled");
                    $('#analysis').val(data.overview.analysis).prop("disabled", "disabled");
                    $('#sign_off').remove();
                }
            }
        });
    }

    function getEmployeeInfoStrat() {

        $.ajax({
            url: '/dashboard/strategy/get_employee_info/',
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                $('#employee_branch').val(data.emp[0].branch__name);

            }
        });

    }


    $('#save_overview').click(function (e) {
        e.preventDefault();
        let branch = $('#user_branch').val();
        let vision = $('#vision').val();
        let mission = $('#mission').val();
        let analysis = $('#analysis').val();
        let priority_p = $('#priority_p').val();
        let budget = $('#mtef_budget_').val();
        let revisions = $('#revisions').val();
        let values = $('#values').val();
        let goals = $('#goals').val();
        let risks = $('#risks').val();
        saveOverview(branch, vision, mission, values, analysis, priority_p, budget, revisions, risks,
            goals);
        // setTimeout(location.reload.bind(location), 4000);
    });

    $('#save_continue_overview').click(function (e) {
        e.preventDefault();
        let branch = $('#user_branch').val();
        let vision = $('#vision').val();
        let mission = $('#mission').val();
        let analysis = $('#analysis').val();
        let priority_p = $('#priority_p').val();
        let budget = $('#mtef_budget_').val();
        let revisions = $('#revisions').val();
        let values = $('#values').val();
        let goals = $('#goals').val();
        let risks = $('#risks').val();
        saveOverview(branch, vision, mission, values, analysis, priority_p, budget, revisions, risks,
            goals);
    });

    $('#sign_off').click(function () {
        signOverview();
        setTimeout(location.reload.bind(location), 4000);
    });

    function signOverview() {
        let csrftoken = getCookie('csrftoken');
        $.ajax({
            url: '/dashboard/strategy/overview/sign/',
            type: 'POST',
            dataType: 'json',
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


    function saveOverview(branch, vision, mission, values, analysis, priority_p, budget, revisions,
                          risks, goals) {
        let csrftoken = getCookie('csrftoken');
        $.ajax({
            url: '/dashboard/strategy/overview/new/',
            type: 'POST',
            dataType: 'json',
            data: {
                vision: vision,
                mission: mission,
                branch: branch,
                priority: priority_p,
                analysis: analysis,
                risks: risks,
                goals: goals,
                values: values,
                revisions: revisions,
                budget: budget
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

    /*

    Strategic objectives block start here

     */


    /*

    event handlers start
     */


    $('#add_goal').click(function (e) {
        e.preventDefault();
        let goal = $('#goal').val();
        let statement = $('#goal_stmnt').val();
        $('#goals_table').append("<li>" + "<strong>Goal: </strong>" + goal + "<strong><br>Goal Statement: </strong>" + statement + "<input type='hidden' data-statement= '" + goal + "'   data-goal= '" + goal + "' >" + "</li>");

    });

    $('#display_goals').click(function (e) {
        e.preventDefault();
        $('#list_goals').fadeIn()
    });

    $('#save_goal_statement').click(function (e) {
        e.preventDefault();
        let goal = $('#goal').val();
        let statmnt = $('#goal_stmnt').val();
        saveGoal(goal, statmnt)
    });

    $('#cap_objective').click(function (e) {
        e.preventDefault();
        getEmployeeInfoStrat();
        $('#capture_overview').hide();
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
        $('#add_strat_obj').fadeIn();
    });


    $('#display_so').click(function (e) {
        e.preventDefault();
        $('#so_list_temp').fadeIn();
    });


    $('#add_so').click(function (e) {
        e.preventDefault();
        var output = $('#so').val();
        var so_kpi = $('#so_kpi').val();
        $('#outputs_table').append("<li>" + output + " " + so_kpi + "<input type='hidden' data-so_output= '" + output + "'   data-so_kpi= '" + so_kpi + "' >" + "</li>");

    });


    $('#add_kpi_').click(function (e) {
        e.preventDefault();
        let kpi = $('#kpi_').val();
        $('#cached_kpi_list').append("<li>" + kpi + "<input type='hidden' data-kpi= '" + kpi + "' </li>");

    });


    $('#display_kpis').click(function (e) {
        e.preventDefault();
        $('#list_kpis_edit').fadeIn()
    });

    $('#display_ats').click(function (e) {
        e.preventDefault();
        $('#at_list_edit').fadeIn();

    });

    $('#save_strategic_objective').click(function (e) {
       e.preventDefault();
        alert("TEST");
    });

    $('#add_risk').click(function (e) {
        e.preventDefault();
        var desc = $('#risk_desc').val();
        var lhood = $('#risk_prob').val();
        var impact = $('#risk_impact').val();
        var mitplan = $('#risk_mit').val();
        $('#obj_r').append("<li>" + desc + "<input type='hidden' data-rdesc= '" + desc + "' " +
            "data-lhood='" + lhood + "' data-impact='" + impact + "' data-mit='" + mitplan + "'  >" + "</li>"
        );

        saveStratRisks(desc, lhood, impact, mitplan)
    });

    $('#display_risks').click(function (e) {
        e.preventDefault();
        $('#obj_risks_list').fadeIn();

    });
    $('#display_objectives').click(function (e) {
        e.preventDefault();
        $('#list_objectives').fadeIn();
    });

    $('#save_objective').click(function (e) {
        e.preventDefault();
        let objective = $('#objective').val();
        let statement = $('#statement').val();
        let baseline = $('#strat_baseline').val();
        let justification = $('#justification').val();
        let links = $('#links').val();
        saveObjective(objective, statement, baseline, justification, links)
    });

    $('.links').click(function (e) {
        e.preventDefault();
        readObjectives();
    });

    $('#save_imperatives').click(function (e) {
        e.preventDefault();
        let obj_id = $(".strategicObjectives option:selected" ).val();
        let links = $('#imperatives').val();
        createImperative(obj_id, links)
    });
    $('#save_subprogrammes').click(function (e) {
        e.preventDefault();
        let obj_id = $(".strategicObjectives option:selected" ).val();
        let subprog = $('#subprogramme').val();
        createSubprogramme(obj_id, subprog)
    });


    $('.objectives').click(function (e) {
        e.preventDefault();
        readOutputObjectives();
    });

    $('#save_output').click(function (e) {
       e.preventDefault();
       let obj_id = $("#outputStrategicObjectives option:selected" ).val();
       let output = $('#strategic_output').val();
       createStrategicOutput(obj_id, output)

    });
    $('.kpi_objectives').click(function (e) {
        e.preventDefault();
        readKPIObjectives();
    });

    $('#save_kpi').click(function (e) {
       e.preventDefault();
       let obj_id = $("#kpiStrategicObjectives option:selected" ).val();
       let kpi = $('#kpi').val();
       createKPI(obj_id, kpi);
    });

    $('.kpi').click(function (e) {
       e.preventDefault();
       readKPIs();
    });


    $('#target_start_date').datepicker({
        dateFormat: 'yy-mm-dd',
        changeYear: true
    });

    $('#target_end_date').datepicker({
        dateFormat: 'yy-mm-dd',
        changeYear: true
    });

    $('#save_target').click(function (e) {
        e.preventDefault();
        let kpi = $("#kpi_ option:selected").val();
        let year_index = $('#year_index').val();
        let start_date = $('#target_start_date').val();
        let end_date = $('#target_end_date').val();
        let baseline = $('#baseline_').val();
        let evidence = $('#evidence').val();

        createTarget(kpi, year_index, start_date, end_date, baseline, evidence);

    });

    $('#save_risk').click(function (e) {
        e.preventDefault();
        let desc = $('#risk_desc').val();
        let likelihood = $('#risk_likelihood').val();
        let impact = $('#risk_impact').val();
        let mit_plan = $('#risk_mit').val();
        createRisk(desc, likelihood, impact, mit_plan)
    });


    $('#save_plan').click(function (e) {
        e.preventDefault();
        let plan = $('#resource_plan').val();
        createPlan(plan);
    });

    function createPlan(plan) {
        let csrftoken = getCookie('csrftoken');
        $.ajax({
            url: '/dashboard/strategy/framework/resource/create/',
            method: 'POST',
            dataType: 'json',
            data: {
                plan: plan
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

    function createRisk(desc, likelihood, impact, mit_plan) {
        let csrftoken = getCookie('csrftoken');
        $.ajax({
            url: '/dashboard/strategy/framework/risk/create/',
            method: 'POST',
            dataType: 'json',
            data: {
                desc: desc,
                likelihood: likelihood,
                impact: impact,
                mit_plan: mit_plan,
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


    function readKPIs() {
         $.ajax({
            url: '/dashboard/strategy/framework/kpi/read/',
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                $('#kpi_').empty().append(
                    $.map(data.kpis, function (obj) {
                        return '<option value="' +obj.id +'">' + obj.kpi +'</option>';
                    }).join());
            }
        });
    }

    function createTarget(kpi,year_index, start_date, end_date, baseline, evidence) {
        let csrftoken = getCookie('csrftoken');
        $.ajax({
            url: '/dashboard/strategy/framework/target/create/',
            method: 'POST',
            dataType: 'json',
            data: {
                kpi: kpi,
                year_index: year_index,
                start_date: start_date,
                end_date: end_date,
                baseline: baseline,
                evidence: evidence,

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

    function createKPI(obj_id, kpi) {
        let csrftoken = getCookie('csrftoken');
        $.ajax({
            url: '/dashboard/strategy/framework/kpi/create/',
            method: 'POST',
            dataType: 'json',
            data: {
                obj_id: obj_id,
                kpi: kpi
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

    function readKPIObjectives() {
        $.ajax({
            url: '/dashboard/strategy/framework/objective/read/',
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                $('#kpiStrategicObjectives').empty().append(
                    $.map(data.objectives, function (obj) {
                        return '<option value="' +obj.id +'">' + obj.objective +'</option>';
                    }).join());
            }
        });

    }

    function createStrategicOutput(obj_id, output) {
        let csrftoken = getCookie('csrftoken');
        $.ajax({
            url: '/dashboard/strategy/framework/output/create/',
            method: 'POST',
            dataType: 'json',
            data: {
                obj_id: obj_id,
                output: output
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
    function saveObjective(objective, statement, baseline, justification, links) {
        let csrftoken = getCookie('csrftoken');
        $.ajax({
            url: '/dashboard/strategy/framework/objective/create/',
            method: 'POST',
            dataType: 'json',
            data: {
                objective: objective,
                statement: statement,
                baseline: baseline,
                justification: justification,
                links: links
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

    function saveGoal(goal, statmnt) {

        let csrftoken = getCookie('csrftoken');
        $.ajax({
            url: '/dashboard/strategy/framework/goal/create/',
            method: 'POST',
            dataType: 'json',
            data: {
                goal: goal,
                statement: statmnt
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

    function readObjectives() {

        $.ajax({
            url: '/dashboard/strategy/framework/objective/read/',
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                $('.strategicObjectives').empty().append(
                    $.map(data.objectives, function (obj) {
                        return '<option value="' +obj.id +'">' + obj.objective +'</option>';
                    }).join());
            }
        });

    }

    function readOutputObjectives() {

        $.ajax({
            url: '/dashboard/strategy/framework/objective/read/',
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                $('#outputStrategicObjectives').empty().append(
                    $.map(data.objectives, function (obj) {
                        return '<option value="' +obj.id +'">' + obj.objective +'</option>';
                    }).join());
            }
        });

    }

    function createImperative(obj_id, links) {
        let csrftoken = getCookie('csrftoken');
        $.ajax({
            url: '/dashboard/strategy/framework/imperative/create/',
            method: 'POST',
            dataType: 'json',
            data: {
                obj_id: obj_id,
                links: links
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

    function createSubprogramme(obj_id, subprog) {
        let csrftoken = getCookie('csrftoken');
        $.ajax({
            url: '/dashboard/strategy/framework/subprogrammes/create/',
            method: 'POST',
            dataType: 'json',
            data: {
                obj_id: obj_id,
                subprog: subprog
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

    $('#add_rp').click(function (e) {
        e.preventDefault();
        var rp_desc = $('#rp_desc').val();
        var docs = $('#rp_docs').val();
        $('#obj_rsc_table').append("<li>" + rp_desc + "<input type='hidden' data-rp_desc= '" + rp_desc + "' " +
            "data-docs='" + docs + " >" + "</li>"
        );
    });


/*

event handlers end
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
