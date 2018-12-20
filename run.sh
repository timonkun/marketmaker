#!/bin/bash

nohup python main.py > /var/log/MarketMaker/running.log 2>&1 & 
