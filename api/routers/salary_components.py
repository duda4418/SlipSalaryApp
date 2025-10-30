from fastapi import APIRouter

salary_components_router = APIRouter(prefix="/salary_components")

@salary_components_router.get("")
def list_salary_components():
    pass

@salary_components_router.get("/{component_id}")
def get_salary_component(component_id: str):
    pass

@salary_components_router.post("")
def create_salary_component():
    pass

@salary_components_router.put("/{component_id}")
def update_salary_component(component_id: str):
    pass

@salary_components_router.delete("/{component_id}")
def delete_salary_component(component_id: str):
    pass
