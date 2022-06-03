[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
New-Item -Path "c:\" -Name "temp" -ItemType "directory"
Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe" -OutFile "c:/temp/python-3.8.10.exe"

c:/temp/python-3.8.10.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
