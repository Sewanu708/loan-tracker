def calculate_risk_score(amount:float, expenses:float, income:float, term_months:float):
    debt_ratio = expenses/(income+1)
    amount_factor = min(amount/50000,1)
    term_factor = min((term_months/60),1)
    score = (0.5 * float(amount_factor)) + (0.3*float(term_factor)) + (0.2*float(debt_ratio)) 
    risk_score = round(min(max(score, 0), 1), 2)
    
    return risk_score
    