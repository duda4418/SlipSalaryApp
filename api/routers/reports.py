from fastapi import APIRouter

reports_router = APIRouter(prefix="/reports")

@reports_router.get("")
def list_report_files():
    pass

@reports_router.get("/{report_id}")
def get_report_file(report_id: str):
    pass

@reports_router.post("")
def create_report_file():
    pass

@reports_router.put("/{report_id}")
def update_report_file(report_id: str):
    pass

@reports_router.delete("/{report_id}")
def delete_report_file(report_id: str):
    pass
