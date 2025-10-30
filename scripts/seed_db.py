"""Script to populate the database with initial sample data."""

from db.session import SessionLocal
from db.models import User, Employee, MonthInfo, SalaryComponent, Vacation, SalaryComponentType
from datetime import date

from faker import Faker
import random
from sqlalchemy import text


NUM_MANAGERS = 3
NUM_EMPLOYEES = 20
MONTHS = [(year, month) for year in range(2023, 2029) for month in range(1, 13)]


def seed():
	db = SessionLocal()
	fake = Faker()
	try:
		# Delete all existing data (respecting FK constraints)
		db.execute(text('TRUNCATE TABLE salary_components, vacations, employees, users, months RESTART IDENTITY CASCADE;'))
		db.execute(text('TRUNCATE TABLE idempotency_keys, report_files RESTART IDENTITY CASCADE;'))
		db.commit()

		employees = []
		# Create manager employees (top-level, no manager)
		for _ in range(NUM_MANAGERS):
			user = User(
				email=fake.unique.email(),
				password_hash=None,
				is_active=True
			)
			db.add(user)
			db.flush()
			employee = Employee(
				user_id=user.id,
				first_name=fake.first_name(),
				last_name=fake.last_name(),
				email=user.email,
				cnp=fake.unique.numerify(text='#############'),
				hire_date=fake.date_between(start_date='-3y', end_date='today'),
				base_salary=random.randint(7000, 12000),
				manager_id=None
			)
			db.add(employee)
			db.flush()
			employees.append(employee)

		# Create regular employees (assign random manager from above)
		for _ in range(NUM_EMPLOYEES):
			user = User(
				email=fake.unique.email(),
				password_hash=None,
				is_active=True
			)
			db.add(user)
			db.flush()
			manager = random.choice(employees[:NUM_MANAGERS])
			hire_date = fake.date_between(start_date='-3y', end_date='today')
			base_salary = random.randint(3000, 8000)
			employee = Employee(
				user_id=user.id,
				first_name=fake.first_name(),
				last_name=fake.last_name(),
				email=user.email,
				cnp=fake.unique.numerify(text='#############'),
				hire_date=hire_date,
				base_salary=base_salary,
				manager_id=manager.id
			)
			db.add(employee)
			db.flush()
			employees.append(employee)

		# Create MonthInfo for all months 2023-2028
		for year, month in MONTHS:
			working_days = random.randint(19, 23)
			month_info = MonthInfo(year=year, month=month, working_days=working_days)
			db.add(month_info)

		# Create Salary Components and Vacations for Employees
		for employee in employees:
			for year, month in MONTHS:
				base = SalaryComponent(
					employee_id=employee.id,
					year=year,
					month=month,
					type=SalaryComponentType.base.value,
					amount=employee.base_salary
				)
				db.add(base)
				# Random bonus
				if random.random() < 0.5:
					bonus_amt = random.randint(200, 1000)
					bonus = SalaryComponent(
						employee_id=employee.id,
						year=year,
						month=month,
						type=SalaryComponentType.bonus.value,
						amount=bonus_amt
					)
					db.add(bonus)
				# Random adjustment
				if random.random() < 0.3:
					adj_amt = random.randint(-500, 500)
					adjustment = SalaryComponent(
						employee_id=employee.id,
						year=year,
						month=month,
						type=SalaryComponentType.adjustment.value,
						amount=adj_amt
					)
					db.add(adjustment)
				# Vacation
				days_taken = random.randint(0, 5)
				vacation = Vacation(
					employee_id=employee.id,
					year=year,
					month=month,
					days_taken=days_taken
				)
				db.add(vacation)

		db.commit()
		print("Database seeded successfully with fake data.")
	except Exception as e:
		db.rollback()
		print(f"Error seeding database: {e}")
	finally:
		db.close()

if __name__ == "__main__":
	seed()
