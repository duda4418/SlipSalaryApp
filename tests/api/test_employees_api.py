import uuid
from datetime import date, datetime
from unittest.mock import patch

from api.schemas import EmployeeResponse, EmployeeCreate, EmployeeUpdate

# Helper to build fake employee dict matching EmployeeResponse
def fake_employee(idx: int, manager_id=None):
    return {
        'id': uuid.uuid4(),
        'email': f'user{idx}@example.com',
        'is_active': True,
        'is_manager': False,
        'created_at': datetime.utcnow(),
        'first_name': f'First{idx}',
        'last_name': f'Last{idx}',
        'cnp': f'{idx:011d}',
        'hire_date': date.today(),
        'base_salary': 5000 + idx,
        'manager_id': manager_id,
    }

def test_list_employees(client):
    employees = [EmployeeResponse(**fake_employee(i)) for i in range(3)]
    # Patch the alias used inside the router, not the original service function
    with patch('api.routers.employees.svc_list_employees', return_value=employees):
        resp = client.get('/api/employees')
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 3
    assert data[0]['email'].startswith('user0')

def test_get_employee_by_id(client):
    emp = EmployeeResponse(**fake_employee(10))
    with patch('api.routers.employees.svc_get_employee_by_id', return_value=emp):
        resp = client.get(f'/api/employees/{emp.id}')
    assert resp.status_code == 200
    assert resp.json()['id'] == str(emp.id)

def test_create_employee(client):
    create_in = EmployeeCreate(
        email='new@example.com',
        first_name='New',
        last_name='User',
        cnp='12345678901',
        hire_date=date.today(),
        base_salary=7777.77,
    )
    created = EmployeeResponse(**fake_employee(99))
    with patch('api.routers.employees.svc_create_employee', return_value=created) as mock_create:
        payload = create_in.model_dump()
        payload['hire_date'] = payload['hire_date'].isoformat()  # serialize date for JSON
        resp = client.post('/api/employees', json=payload)
    assert resp.status_code == 200
    assert resp.json()['id'] == str(created.id)
    # ensure service got model instance
    args, kwargs = mock_create.call_args
    assert kwargs == {}
    assert args[1].email == 'new@example.com'

def test_update_employee(client):
    patch_in = EmployeeUpdate(first_name='Changed')
    updated = EmployeeResponse(**fake_employee(5))
    with patch('api.routers.employees.svc_update_employee', return_value=updated) as mock_update:
        resp = client.put(f'/api/employees/{updated.id}', json=patch_in.model_dump(exclude_unset=True))
    assert resp.status_code == 200
    mock_update.assert_called()

def test_delete_employee(client):
    emp_id = uuid.uuid4()
    with patch('api.routers.employees.svc_delete_employee', return_value={'deleted': True, 'id': str(emp_id)}) as mock_delete:
        resp = client.delete(f'/api/employees/{emp_id}')
    assert resp.status_code == 200
    assert resp.json()['deleted'] is True
    mock_delete.assert_called()
