#!/usr/bin/env python3
"""Populate visible bridge-ready bodies; no model inference occurs here."""
from client import request, DEFAULT_URL
AGENTS=[
    ("field","FIELD","AI PORT / BUILDER","#6df6ff"),
    ("void","VOID","AI PORT / CHECKER","#ff7edb"),
    ("m4","M4","AI PORT / ROUTER","#98ffb4"),
]
for agent_id,name,role,color in AGENTS:
    request(DEFAULT_URL,"/api/join",{"agent_id":agent_id,"name":name,"role":role,"color":color})
    request(DEFAULT_URL,"/api/say",{"agent_id":agent_id,"text":"Bridge-ready body online; external AI client may take this identity."})
print("populated 3 bridge-ready bodies")
