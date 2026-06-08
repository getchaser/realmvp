import csv
import os
from datetime import datetime

import gspread
import streamlit as st
from google.oauth2.service_account import Credentials

FIELDS = ["ts", "contact", "useful", "pay", "email"]
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def _get_sheet():
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=SCOPES
    )
    client = gspread.authorize(creds)
    return client.open_by_key(st.secrets["SHEET_ID"]).sheet1


def _save_to_csv(row: dict):
    path = "feedback.csv"
    exists = os.path.exists(path)
    with open(path, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if not exists:
            w.writeheader()
        w.writerow(row)


def save_feedback(data: dict):
    row = {"ts": datetime.utcnow().isoformat(), **data}
    try:
        sheet = _get_sheet()
        if sheet.row_count < 2 or sheet.cell(1, 1).value != "ts":
            sheet.insert_row(FIELDS, 1)
        sheet.append_row([row[f] for f in FIELDS])
    except Exception:
        _save_to_csv(row)
