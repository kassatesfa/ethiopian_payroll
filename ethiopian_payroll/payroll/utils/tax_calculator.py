import frappe


def get_active_tax_rule():
    rules = frappe.get_all(
        "Ethiopian Tax Rule",
        filters={"active": 1},
        limit=1
    )

    if not rules:
        return None

    return frappe.get_doc(
        "Ethiopian Tax Rule",
        rules[0].name
    )


def calculate_paye(taxable_income):
    rule = get_active_tax_rule()

    if not rule:
        return 0

    for row in rule.tax_brackets:
        upper = row.upper_limit or 999999999

        if row.lower_limit <= taxable_income <= upper:
            return (
                taxable_income * row.tax_rate / 100
            ) - (row.deduction or 0)

    return 0


def calculate_employee_pension(gross_salary):
    rule = get_active_tax_rule()

    if not rule:
        return 0

    return (
        gross_salary
        * rule.employee_pension_rate
        / 100
    )
