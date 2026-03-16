from datetime import datetime, timedelta
import calendar

def calculate_initial_payment(monthly_rent, move_in_date):
    """
    Calculates the initial payment based on the "Coolsun 15-Day Rule".
    
    Logic:
    1. Daily Rate = Monthly Rent / 30 (Standardized)
    2. If move-in <= 15th: Pay pro-rata for remaining days of current month.
    3. If move-in > 15th: Pay pro-rata + Full Next Month Rent.
    
    Returns:
        dict: {
            'prorated_amount': float,
            'next_month_advance': float,
            'total_initial_rent': float,
            'days_billed': int,
            'description': str
        }
    """
    if isinstance(move_in_date, str):
        try:
            # Safely extract just the YYYY-MM-DD if frontend sends a full ISO timestamp
            clean_date_str = move_in_date.split('T')[0]
            move_in_date = datetime.strptime(clean_date_str, '%Y-%m-%d').date()
        except Exception:
            # Fallback to today to avoid 500 crash killing the UI
            move_in_date = datetime.utcnow().date()
            
    year = move_in_date.year
    month = move_in_date.month
    day = move_in_date.day
    
    # Standardize month to 30 days for daily rate calculation as per common hostel practice
    # Or use actual days in month. Let's use actual days for precision if needed, 
    # but "Rent / 30" is a standard hostel heuristic. Let's stick to Rent / 30 for simplicity 
    # unless specified otherwise.
    daily_rate = monthly_rent / 30
    
    # Calculate days remaining in current month (inclusive of move-in date)
    # Using actual calendar days for the remaining count
    _, days_in_month = calendar.monthrange(year, month)
    remaining_days = days_in_month - day + 1
    
    prorated_amount = round(remaining_days * daily_rate, 2)
    next_month_advance = 0.0
    description = f"Pro-rata for {remaining_days} days ({move_in_date} to end of month)"
    
    # The 15-Day Rule
    if day > 15:
        next_month_advance = float(monthly_rent)
        description += " + Next Month Advance (Move-in after 15th)"
        
    total_initial_rent = prorated_amount + next_month_advance
    
    return {
        'prorated_amount': prorated_amount,
        'next_month_advance': next_month_advance,
        'total_initial_rent': total_initial_rent,
        'days_billed': remaining_days,
        'description': description
    }
