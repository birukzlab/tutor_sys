from flask import Blueprint, render_template, request, redirect, url_for, flash
from .pdf_generation import generate_invoice
from .email_sending import send_email_with_invoice
from .sheets_integration import get_sheet_data
from .calculations import update_billing_info

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/generate-invoice', methods=['POST'])
def generate_invoice_route():
    student_name = request.form.get('student_name')
    hours_attended = float(request.form.get('hours_attended'))
    hourly_rate = float(request.form.get('hourly_rate'))
    parent_email = request.form.get('parent_email')

    total_due = hours_attended * hourly_rate
    invoice_details = {
        "date": "2024-08-31",
        "due_date": "2024-09-15",
        "invoice_number": f"INV-{student_name.replace(' ', '_')}-{total_due}",
        "hours_attended": hours_attended,
        "hourly_rate": hourly_rate,
        "total_due": total_due
    }

    # Generate the invoice PDF
    generate_invoice(student_name, invoice_details)

    # Email the invoice
    invoice_path = f"generated_invoices/{student_name}_invoice.pdf"
    if parent_email:
        send_email_with_invoice(parent_email, student_name, invoice_path)

    flash("Invoice generated and emailed successfully!", "success")
    return redirect(url_for('main.index'))
