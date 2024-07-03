import json
from datetime import datetime

def log_crew_response(company, response):
    timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    filename = f"{company}_{timestamp}.json"
    
    log_entry = {
        "company": company,
        "timestamp": timestamp,
        "response": response
    }
    
    with open(filename, 'w') as f:
        json.dump(log_entry, f, indent=4)
    
    print(f"Response logged to {filename}")