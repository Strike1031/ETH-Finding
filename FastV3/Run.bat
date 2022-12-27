@Echo off
title ETHChecker Atomic 
Pushd "%~dp0"
:loop
python FindETH.py
goto loop
