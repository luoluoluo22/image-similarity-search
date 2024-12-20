$ServerIP = "your_server_ip"
$Username = "your_username"
$Password = "your_password"
$RemotePath = "C:\path\to\deployment"

# 创建 PSSession
$SecurePassword = ConvertTo-SecureString $Password -AsPlainText -Force
$Cred = New-Object System.Management.Automation.PSCredential ($Username, $SecurePassword)
$Session = New-PSSession -ComputerName $ServerIP -Credential $Cred

# 复制文件
Copy-Item -Path ".\*" -Destination $RemotePath -ToSession $Session -Recurse -Force

# 关闭会话
Remove-PSSession $Session 