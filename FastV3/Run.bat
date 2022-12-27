@Echo off
title ETH_FAST_Checker Atomic 
Pushd "%~dp0"
:loop
python FindETH.py
goto loop
