@Echo off
title ETH_Slow_Checker Atomic 
Pushd "%~dp0"
:loop
python challenge.py
goto loop
