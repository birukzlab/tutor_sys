def calculate_hours_attended(attendance_data, student_name):
    """Calculate total hours attended for a given student."""
    hours_attended = sum(1 for row in attendance_data if row[0] == student_name and row[2] == 'P')
    return hours_attended

def calculate_total_due(hours_attended, hourly_rate):
    """Calculate total amount due based on hours attended and hourly rate."""
    return hours_attended * hourly_rate

def update_billing_info(billing_data, attendance_data):
    """Update billing information with calculated hours attended and total amount due."""
    for row in billing_data[1:]:  # Skip header row
        student_name = row[0]
        hourly_rate = float(row[2])
        hours_attended = calculate_hours_attended(attendance_data, student_name)
        total_due = calculate_total_due(hours_attended, hourly_rate)
        row[1] = hours_attended  # Update Hours Attended
        row[3] = total_due        # Update Total Amount Due

    return billing_data
