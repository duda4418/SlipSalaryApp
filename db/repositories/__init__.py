"""Repository package aggregating all repository functions for backward-compatible imports.

Allows existing imports like:
    from db.repositories import repo_create_report_file
while code is now modularized.
"""
from .employees_repo import *  # noqa: F401,F403
from .salary_components_repo import *  # noqa: F401,F403
from .vacations_repo import *  # noqa: F401,F403
from .months_repo import *  # noqa: F401,F403
from .idempotency_repo import *  # noqa: F401,F403
from .report_files_repo import *  # noqa: F401,F403
from .refresh_tokens_repo import *  # noqa: F401,F403
from .auth_repo import *  # noqa: F401,F403
from .reporting_queries import *  # noqa: F401,F403

__all__ = [
    # employees
    'repo_list_employees','repo_get_employees_by_manager','repo_get_employee_by_email','repo_get_employee_by_id','repo_create_employee','repo_update_employee','repo_delete_employee',
    # salary components
    'repo_create_salary_component','repo_update_salary_component','repo_delete_salary_component','repo_list_salary_components','repo_get_salary_component_by_id',
    # vacations
    'repo_create_vacation','repo_update_vacation','repo_delete_vacation','repo_list_vacations','repo_get_vacation_by_id',
    # months
    'repo_create_month','repo_update_month','repo_delete_month','repo_list_months','repo_get_month_by_id','repo_get_month_info_by_year_month',
    # idempotency
    'repo_create_idempotency_key','repo_update_idempotency_key','repo_delete_idempotency_key','repo_list_idempotency_keys','repo_get_idempotency_key_by_id','repo_get_idempotency_key_by_key','repo_mark_idempotency_key_succeeded',
    # report files
    'repo_create_report_file','repo_update_report_file','repo_delete_report_file','repo_list_report_files','repo_get_report_file_by_id','repo_get_report_file_by_path',
    # refresh tokens
    'repo_create_refresh_token','repo_get_refresh_token_by_hash','repo_rotate_refresh_token','repo_issue_refresh_token','repo_validate_refresh_token_and_get_user','repo_rotate_refresh_token_and_issue',
    # auth
    'repo_validate_login',
    # reporting queries
    'repo_get_manager','repo_list_subordinates','repo_list_salary_components_for_employees_month','repo_list_vacations_for_employees_month','repo_aggregate_employee_month_summary',
]
