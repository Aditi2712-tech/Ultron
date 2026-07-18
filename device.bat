@echo off
title ADB Wi-Fi Connect

echo Disconnecting previous Wi-Fi connections...
adb disconnect

echo Restarting ADB in TCP mode...
adb tcpip 5555

timeout /t 3 >nul

echo Getting phone IP...

set ip=

for /f "tokens=2" %%G in ('adb shell ip addr show wlan0 ^| findstr "inet "') do (
    for /f "tokens=1 delims=/" %%H in ("%%G") do (
        set ip=%%H
    )
)

if "%ip%"=="" (
    echo.
    echo ERROR: Could not detect phone IP.
    echo Make sure the phone is connected via USB and Wi-Fi.
    pause
    exit /b
)

echo Found phone IP: %ip%

adb connect %ip%:5555

echo.
adb devices
pause