from logging import getLogger
from datetime import datetime

def log_crm_heartbeat(*args, **kwargs):
    current_date = datetime.now()

    with open('/tmp/crm_heartbeat','+a') as f:
        f.write(f'{current_date} CRM is alive!`')    

log_crm_heartbeat()
