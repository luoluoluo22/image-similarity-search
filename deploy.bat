@echo off
set SERVER_IP=your_server_ip
set SERVER_USER=your_username
set SERVER_PATH=C:\path\to\deployment

:: 创建必要的文件夹
mkdir %SERVER_PATH%\images
mkdir %SERVER_PATH%\uploads
mkdir %SERVER_PATH%\templates

:: 复制文件
xcopy /Y image_search.py %SERVER_PATH%
xcopy /Y web_app.py %SERVER_PATH%
xcopy /Y requirements.txt %SERVER_PATH%
xcopy /Y templates\*.* %SERVER_PATH%\templates\ 