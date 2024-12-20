@echo off
cd C:\apps\image_search

:: 停止服务
nssm stop ImageSearch

:: 更新代码
git pull

:: 更新依赖
call venv\Scripts\activate
pip install -r requirements.txt

:: 重启服务
nssm start ImageSearch 