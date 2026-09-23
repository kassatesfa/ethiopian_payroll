from ethiopian_payroll.payroll.utils.tax_calculator import (
    calculate_paye,
    calculate_employee_pension
)


def validate_salary_slip(doc, method):

    gross_pay = doc.gross_pay or 0

    pension = calculate_employee_pension(
        gross_pay
    )

    taxable_income = gross_pay - pension

    paye = calculate_paye(
        taxable_income
    )

    update_deduction(
        doc,
        "Employment Income Tax",
        paye
    )

    update_deduction(
        doc,
        "Employee Pension",
        pension
    )


def update_deduction(
    doc,
    component_name,
    amount
):

    existing = None

    for row in doc.deductions:
        if row.salary_component == component_name:
            existing = row
            break

    if existing:
        existing.amount = amount
    else:
        doc.append(
            "deductions",
            {
                "salary_component": component_name,
                "amount": amount
            }
        )
