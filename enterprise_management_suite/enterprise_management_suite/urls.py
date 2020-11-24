"""enterprise_management_suite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.views.static import serve
from home import views as home_views
from accounts import views as accounts_views
from employee_performance import views as emp_views
from programme_project import views as ppm_views
from permissions import views as perm_views
from strategy import views as strat_views
from search import views as search_views
from mtf_budget import views as mtef_views
from annual_performance import views as app_views

urlpatterns = [
                path('media/<path>', serve, {
                  'document_root': settings.MEDIA_ROOT,
                }),
                path('static/<path>', serve, {
                  'document_root': settings.STATIC_URL,
                }),
                path('admin/', admin.site.urls),

                path('dashboard/', home_views.dashboard, name='dashboard'),

                # app starts

                path('dashboard/app/framework/app/context/read', app_views.get_app_context,
                     name='get_context'
                     ),
                path('dashboard/app/framework/app/objectives/read/', app_views.get_objectives,
                     name='get_objectives'
                     ),
                path('dashboard/app/framework/app/outputs/read/', app_views.get_outputs,
                     name='get_outputs'
                     ),
                path('dashboard/app/framework/app/kpi/read/', app_views.get_kpis,
                         name='get_kpis'
                     ),
                path('dashboard/app/framework/app/targets/read/', app_views.get_annual_targets,
                        name='get_annual_targets'
                     ),

                path('dashboard/app/framework/targets/create/', app_views.create_quarterly_targets,
                        name='create_quarterly_targets'
                     ),

                # app ends

                # Mtef and Budget start


                path('dashboard/mtef/current_payments/create/', mtef_views.create_current_payments,
                     name='create_current_payments'
                     ),
                path('dashboard/mtef/capital_assets/create/', mtef_views.create_capital_assets,
                     name='create_capital_assets'
                     ),
                path('dashboard/mtef/transfers/create/', mtef_views.create_transfers,
                     name='create_transfers'
                     ),

                # Mtef and Budget end

                  # Strategy start
                path('dashboard/strategy/overview/new/', strat_views.save_new_overview, name='save_new_overview'),
                path('dashboard/strategy/overview/update/', strat_views.update_overview, name='update_overview'),
                path('dashboard/strategy/overview/sign/', strat_views.sign, name='sign_off'),
                path('dashboard/strategy/overview/', strat_views.get_or_create_overview, name='get_or_create_overview'),
                path('dashboard/strategy/get_employee_info/', strat_views.get_employee_info,
                    name='get_employee_info'
                    ),
                path('dashboard/strategy/framework/goal/create/', strat_views.create_objective_goal,
                     name="create_objective_goal"
                     ),
                path('dashboard/strategy/framework/objective/create/', strat_views.create_objective,
                     name="create_objective"
                     ),

                path('dashboard/strategy/framework/objective/read/', strat_views.read_objective,
                     name="read_objective"
                     ),
                path('dashboard/strategy/framework/imperative/create/', strat_views.create_imperative,
                     name="create_imperative"
                     ),
                path('dashboard/strategy/framework/subprogrammes/create/', strat_views.create_subprogramme,
                     name="create_subprogramme"
                     ),
                path('dashboard/strategy/framework/output/create/', strat_views.create_strategic_output,
                     name="create_strategic_output"
                     ),
                path('dashboard/strategy/framework/kpi/create/', strat_views.create_kpi, name="create_kpi"),

                path('dashboard/strategy/framework/kpi/read/', strat_views.read_kpi, name="read_kpi"),
                path('dashboard/strategy/framework/target/create/', strat_views.create_target, name="create_target"),
                path('dashboard/strategy/framework/risk/create/', strat_views.create_risk, name="create_risk"),
                path('dashboard/strategy/framework/resource/create/', strat_views.create_resource_plan,
                     name="create_resource_plan"),
                # Strategy end


                # PPM  start

                path('dashboard/ppm/update_employee_project/', ppm_views.update_project, name='update_employee_project'),
                path('dashboard/ppm/projects/project/read/', ppm_views.read_project, name='read_project'),
                path('dashboard/ppm/projects/read', ppm_views.read_projects, name='read_projects'),
                path('dashboard/ppm/add_project/', ppm_views.add_project, name='add_project'),
                path('dashboard/ppm/get_employee_info/', ppm_views.get_employee_info, name='get_employee_info'),
                path('dashboard/ppm/get_active_project/', ppm_views.get_active_project, name='get_active_project'),
                path('dashboard/perms/add_contributor/', perm_views.add_contributor, name='add_contributo'),
                path('dashboard/ppm/get_contr_project/', ppm_views.get_contr_project, name='get_contr_project'),
                path('dashboard/ppm/save_token/', ppm_views.contributor_signs, name='contributor_signs'),
                path('dashboard/ppm/contributors/read/', ppm_views.get_contributors, name='get_contributors'),
                path('dashboard/ppm/subprogramme/read/', ppm_views.read_subprogramme, name='read_subprogramme'),

                # PPM end

                # employee performance agreement (epa) start
                path('dashboard/agreement/create_agreement/', emp_views.create_agreement, name='create_agreement'),
                path('dashboard/agreement/get_pa/', emp_views.get_user_pa, name='get_user_pa'),
                path('dashboard/search/supervisors/fetch', search_views.get_supervisors, name='get_supervisors'),
                path('dashboard/agreement/financial_year/', emp_views.financial_year,
                    name='financial_year'
                    ),
                # end

                # kra start
                path('dashboard/agreement/kra/create/', emp_views.create_kra, name='create_kra'),
                path('dashboard/agreement/kra/list/', emp_views.list_kras, name='list_kras'),
                path('dashboard/agreement/kra/fetch/', emp_views.fetch_kra, name='fetch_kra'),
                path('dashboard/agreement/kra/delete/', emp_views.delete_kra, name='delete_kra'),
                path('dashboard/agreement/kra/update/', emp_views.update_kra, name='update_kra'),
                # kra ends


                # key performance indicator starts
                path('dashboard/agreement/indicators/create/', emp_views.create_key_performance_indicator, name='create_kpi'),
                path('dashboard/agreement/indicators/list/', emp_views.list_key_performance_indicator, name='list_indicators'),
                # path('dashboard/agreement/indicators/update/', emp_views.create_key_perf_indicator, name='create_kpi'),
                path('dashboard/agreement/indicators/delete/', emp_views.delete_indicator, name='delete_indicator'),
                path('dashboard/agreement/indicators/kpi/', emp_views.get_indicator, name='get_indicator'),

                # key performance indicator ends

                # targets start
                path('dashboard/agreement/targets/create/', emp_views.create_target, name='create_target'),
                path('dashboard/agreement/targets/list/', emp_views.list_targets, name='list_targets'),


                # targets end

                # outputs start
                path('dashboard/agreement/outputs/create/', emp_views.create_measurable_output, name='create_outputs'),
                path('dashboard/agreement/outputs/list/', emp_views.list_measurable_outputs, name='list_outputs'),
                path('dashboard/agreement/load_mo/', emp_views.get_measurable_output, name='get_output'),
                path('dashboard/agreement/outputs/update/', emp_views.update_mo, name='update_output'),
                path('dashboard/agreement/delete_mo/', emp_views.delete_mo, name='delete_mo'),
                # outputs end

                # training needs start
                path('dashboard/agreement/training/create/', emp_views.create_pdp, name='create_pdp'),
                path('dashboard/agreement/training/update/', emp_views.update_pdp, name='update_pdp'),
                path('dashboard/agreement/training/delete/', emp_views.delete_pdp, name='delete_pdp'),
                # path('dashboard/agreement/list_pdp/$', emp_views.list_pdps, name='list_pdps'),
                path('dashboard/agreement/training/load/', emp_views.load_pdp, name='load_pdp'),
                path('dashboard/agreement/training/list/', emp_views.list_training_needs, name='list_training_needs'),
                # training needs end

                # sign starts
                path('dashboard/agreement/sign/', emp_views.sign_agreement, name='sign_agreement'),
                path('dashboard/agreement/get_pa_sum/', emp_views.get_pa_sum, name='pa_summary'),
                # sign ends

                # performance review starts

                path('dashboard/review/update/', emp_views.review_update, name='review_update'),
                path('dashboard/review/bulk/create/', emp_views.save_bulk_review, name='save_bulk_review'),
                path('dashboard/review/kra/review/', emp_views.get_review_kra, name='get_review_kra'),

                path('confirm-employee/<persal>',
                    emp_views.confirm_employee, name='confirm_employee'
                    ),
                path('dashboard/review/rev_per', emp_views.review_periods, name='review_periods'),
                path('dashboard/review/kra/rating/update/', emp_views.save_employee_kra_rating, name='save_employee_kra_rating'),

                # performance review ends
                # user profile starts
                path('logout/', accounts_views.logout_view, name='logout'),
                path('password-reset/', accounts_views.pass_reset, name='password_reset'),
                path('password-reset/done/', accounts_views.password_reset_done, name='password_reset_done'),
                path('password-update/', accounts_views.password_update, name='password_update'),
                path('password-reset/complete/', accounts_views.password_reset_complete, name='password_complete'),
                path('profile/', accounts_views.display_profile, name='display_profile'),
                # user profile ends
                # path('reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                #     accounts_views.password_reset_confirm, name='password_reset_confirm'),
                # path('reset/done/$', accounts_views.password_reset_complete, name='password_reset_complete'),
                path('', accounts_views.auth, name='login'),
              ] + static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
