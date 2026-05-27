#!/usr/bin/env python
"""
Standalone script to send reminder emails for overdue/upcoming loans.
Run daily via cron: 0 0 * * * cd ~/Projects/vistabieb && source .venv/bin/activate && python stuur_herinneringen.py
"""

from app import create_app
from app.mail import stuur_herinneringen

if __name__ == '__main__':
    app = create_app()
    result = stuur_herinneringen(app)
    print(f"Verstuurd: {result['sent']}, Overgeslagen: {result['skipped']}, Fouten: {len(result['errors'])}")
    if result['errors']:
        for error in result['errors']:
            print(f"  - {error}")
