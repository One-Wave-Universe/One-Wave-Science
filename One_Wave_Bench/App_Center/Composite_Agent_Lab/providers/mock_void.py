PLUGIN={"id":"mock-void","name":"Mock Void","kind":"local","roles":["void"],"description":"Deterministic local Void admin test plugin"}
def call(role, packet):
    if role=="VOID_ADMIN": return {"decision":"ALLOW","inner_voice":"Reference present; bounded action allowed.","permissions":{"speak":True}}
    if role=="VOID_COMMIT": return {"commit":True,"reason":"Sandbox result returned."}
    return {}
