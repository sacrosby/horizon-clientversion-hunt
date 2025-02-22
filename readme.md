Horizon Client Monitor
==========================
_Seth Crosby_  


## What this is
This is a simple python program that helps find legacy VMware/Omnissa Horizon VDI client versions still in production. It depends on PowerCLI from Broadcom and the recently re-released Omnissa Horizon PowerCLI modules (https://developer.omnissa.com/horizon-powercli/download/)

## Background
I'm a sometime engineer on Omnissa Horizon (formerly by VMware) VDI environments. This
is a simple tool I wrote for a very specific scenario. The environment is a sprawling 24/7 
services provider that struggles with legacy IT. In the scenario there a number of hardware 
endpoints running legacy versions of the Horizon Client (pre-8.1.0 for my purposes). 
They come and they go, but tracking them all down across the diverse geography is not 
trivial. That's the problem I'm trying to solve. Track and flag every legacy client version, 
tie it to the hardware device and user who is interacting, and you have some threads to 
chase down.

In an environment with mixed legacy versions of the Horizon client, it can be a challenge 
to get a solid picture of how many client versions are out there that are below a target
compatibility level. If you look in the Horizon console, you only see currently connected 
systems. I considered digging into the events database to see if I could extract historic 
data, but reconsidered when I realized how lightweight this temporary solution could be.


## What this is
Simply, this python program polls a Horizon Connection Server periodically and creates an 
ouput .csv that captures the following data: 

-----------------------------------------------------------------------------------
|UserName | MachineName | AgentVersion | ClientAddress | ClientVersion | StartTime|
-----------------------------------------------------------------------------------

eg. domain\scrosby, VDI-Prodv3-nnnn, 8.4.0, 10.10.10.101, SethsDevice3, 8.13.0, "1/1/2025 10:10:02AM"

Then, the program reads the .csv, filters out anything equaling or lower than ClientVersion 
of 8.0.0, deduplicates the data, does some reshuffling of columns per my preferences, and 
outputs a new single .csv file that will continue to grow as new clients are found connected
to the horizon server. It never removes old data, because we want to see every legacy client
that has connected to Horizon for a desktop for as long as this python program runs.

From there, the endpoint team can chase those legacy puppies down. 

GNU licensed, and I'm likely to improve. 
This is something I've needed to use a few times over the years. 

## Need to Know
There's a simple credentials script included that should be used under careful advisement. 
Understand the impacts of storing credentials in your profile data prior to using. You 
Should also know how to clear this before you use it. If you prefer to store credentials 
otherwise, edit away. 