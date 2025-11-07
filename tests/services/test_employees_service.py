from datetime import date
from unittest.mock import Mock
from api.schemas import EmployeeCreate, EmployeeUpdate
import services.employees_service as svc
from db import models

class DummyRepoFns:
    def __init__(self):
        self.calls = []

    def create(self, db, **data):
        self.calls.append(('create', data))
        return models.Employee(**data)  # return model instance like real repo

    def update(self, db, eid, **data):
        self.calls.append(('update', eid, data))
        # Simulate existing employee mutated
        return models.Employee(id=eid, **{**data, 'email':'x@y.z','is_active':True,'is_manager':False,'first_name':data.get('first_name','A'),'last_name':'B','cnp':'12345678901','hire_date':date.today(),'base_salary':1000.0,'manager_id':None, 'created_at':date.today()})

    def delete(self, db, eid):
        self.calls.append(('delete', eid))
        return {'deleted': True}

repo = DummyRepoFns()

def test_create_employee_passes_fields(monkeypatch):
    # Patch the symbol imported into the service module
    monkeypatch.setattr('services.employees_service.repo_create_employee', repo.create)
    data = EmployeeCreate(
        email='x@y.z', first_name='A', last_name='B', cnp='12345678901', hire_date=date.today(), base_salary=1000.0
    )
    result = svc.create_employee(Mock(), data)
    assert result.email == 'x@y.z'
    assert repo.calls[-1][0] == 'create'

def test_update_employee_excludes_unset(monkeypatch):
    monkeypatch.setattr('services.employees_service.repo_update_employee', repo.update)
    patch = EmployeeUpdate(first_name='Changed')
    result = svc.update_employee(Mock(), 'emp-1', patch)
    assert result.first_name == 'Changed'
    # Ensure only provided field passed through
    last_call = repo.calls[-1]
    assert last_call[0] == 'update'
    assert last_call[2] == {'first_name': 'Changed'}

def test_delete_employee(monkeypatch):
    monkeypatch.setattr('services.employees_service.repo_delete_employee', repo.delete)
    result = svc.delete_employee(Mock(), 'emp-1')
    assert result['deleted'] is True
