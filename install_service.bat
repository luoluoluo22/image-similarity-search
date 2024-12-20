@echo off
nssm install ImageSearchService "C:\path\to\python.exe" "C:\path\to\deployment\web_app.py"
nssm set ImageSearchService AppDirectory "C:\path\to\deployment"
nssm start ImageSearchService 