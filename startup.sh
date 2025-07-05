#!/bin/bash
pip install --upgrade pip
pip install -r requirements.txt
exec streamlit run app.py --server.port=8000 --server.address=0.0.0.0 --server.enableCORS=false --server.enableXsrfProtection=false
