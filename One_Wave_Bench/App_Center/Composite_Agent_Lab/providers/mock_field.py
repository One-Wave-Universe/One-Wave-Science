PLUGIN={"id":"mock-field","name":"Mock Field","kind":"local","roles":["field"],"description":"Deterministic local Field test plugin"}
def call(role, packet):
    if role=="FIELD_PERCEIVE": return {"perception":str(packet.get("world",{}).get("input","")),"proposal":{"kind":"speak"},"plan":{"step":"respond"}}
    if role=="FIELD_ACT": return {"action":{"kind":"speak"},"speech":"Field received the input and Void allowed the action."}
    return {}
