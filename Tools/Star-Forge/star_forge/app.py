from __future__ import annotations
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
from .state import LEVELS, active_step, add_plan_step, assign_pair, bridge_receipt, load_state, mediator_continue, resolve_active, save_state

class CouncilApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.onewave.StarForge")
        self.state = load_state()
    def do_activate(self):
        win = MainWindow(self)
        win.present()

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="Star Forge")
        self.app = app
        self.set_default_size(1000, 720)
        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        root.set_margin_top(10); root.set_margin_bottom(10); root.set_margin_start(10); root.set_margin_end(10)
        self.set_child(root)
        title = Gtk.Label(xalign=0)
        title.set_markup("<span size='x-large' weight='bold'>Star Forge</span>")
        root.append(title)
        root.append(Gtk.Label(label="Mediator → Field → Void → Mediator", xalign=0))
        root.append(Gtk.Label(label="Reference • Test • Independent Check • No Drift • Simplicity • Ease of Use", xalign=0))
        self.status = Gtk.Label(xalign=0); root.append(self.status)
        ctl = Gtk.Box(spacing=8); root.append(ctl)
        self.loop = Gtk.Switch(active=self.state["project"].get("loop_enabled", True))
        self.loop.connect("notify::active", self.on_loop)
        ctl.append(Gtk.Label(label="Mediator loop")); ctl.append(self.loop)
        b = Gtk.Button(label="Run Mediator"); b.connect("clicked", self.on_run); ctl.append(b)
        tabs = Gtk.Notebook(); tabs.set_vexpand(True); root.append(tabs)
        tabs.append_page(self.make_plan_page(), Gtk.Label(label="Project Plan"))
        tabs.append_page(self.make_pair_page(), Gtk.Label(label="Field / Void"))
        tabs.append_page(self.make_text_page("bridges"), Gtk.Label(label="Bridges"))
        tabs.append_page(self.make_text_page("council"), Gtk.Label(label="Live Council"))
        tabs.append_page(self.make_text_page("journal"), Gtk.Label(label="Journal"))
        tabs.append_page(self.make_text_page("standards"), Gtk.Label(label="Standards"))
        tabs.append_page(self.make_text_page("toc"), Gtk.Label(label="Project Map"))
        tabs.append_page(self.make_text_page("validation"), Gtk.Label(label="Reality Validation"))
        self.refresh()

    @property
    def state(self): return self.app.state

    def make_plan_page(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.goal = Gtk.Entry(text=self.state["project"].get("goal", ""), placeholder_text="Project goal")
        self.repo = Gtk.Entry(text=self.state["project"].get("repo", ""), placeholder_text="GitHub repository")
        self.branch = Gtk.Entry(text=self.state["project"].get("base_branch", "main"), placeholder_text="Base branch")
        self.head = Gtk.Entry(text=self.state["project"].get("base_head", ""), placeholder_text="Base HEAD")
        for w in (self.goal, self.repo, self.branch, self.head): box.append(w)
        save = Gtk.Button(label="Save project reference"); save.connect("clicked", self.on_save_project); box.append(save)
        self.step_title = Gtk.Entry(placeholder_text="New step title"); box.append(self.step_title)
        self.step_goal = Gtk.Entry(placeholder_text="Step goal"); box.append(self.step_goal)
        self.level = Gtk.DropDown.new_from_strings([f"{i} — {LEVELS[i]}" for i in range(1,7)]); box.append(self.level)
        add = Gtk.Button(label="Add step to Mediator plan"); add.connect("clicked", self.on_add_step); box.append(add)
        self.plan_view = Gtk.TextView(editable=False, monospace=True)
        sc = Gtk.ScrolledWindow(); sc.set_vexpand(True); sc.set_child(self.plan_view); box.append(sc)
        return box
    def make_pair_page(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.field = Gtk.Entry(text="Field AI", placeholder_text="Field AI"); box.append(self.field)
        self.void = Gtk.Entry(text="Void AI", placeholder_text="Void AI"); box.append(self.void)
        a = Gtk.Button(label="Mediator assign current step"); a.connect("clicked", self.on_assign); box.append(a)
        self.verdict = Gtk.DropDown.new_from_strings(["ALLOW","CORRECT","HOLD","ESCALATE"]); box.append(self.verdict)
        self.evidence = Gtk.TextView(); ev = Gtk.ScrolledWindow(); ev.set_min_content_height(120); ev.set_child(self.evidence); box.append(ev)
        self.unresolved = Gtk.Entry(placeholder_text="Unresolved items"); box.append(self.unresolved)
        r = Gtk.Button(label="Mediator resolve and continue"); r.connect("clicked", self.on_resolve); box.append(r)
        self.pair_view = Gtk.TextView(editable=False, monospace=True)
        sc = Gtk.ScrolledWindow(); sc.set_vexpand(True); sc.set_child(self.pair_view); box.append(sc)
        return box

    def make_text_page(self, name):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        view = Gtk.TextView(editable=False, monospace=True)
        setattr(self, name+"_view", view)
        sc = Gtk.ScrolledWindow(); sc.set_vexpand(True); sc.set_child(view); box.append(sc)
        return box

    def text(self, view, value): view.get_buffer().set_text(value)
    def refresh(self):
        p=self.state["project"]; step=active_step(self.state)
        self.status.set_text(f"{p.get('status')} | L{p.get('active_level')} {LEVELS.get(p.get('active_level'))} | {step['title'] if step else 'no active step'} | checkpoint={p.get('checkpoint') or 'none'}")
        lines=[]
        for s in p.get("plan",[]):
            mark=">" if s["id"]==p.get("active_step_id") else " "
            lines.append(f"{mark} L{s['level']} [{s['status']}] {s['title']} :: {s['goal']}")
        self.text(self.plan_view,"\n".join(lines) or "No plan steps yet.")
        a=self.state["assignments"][-1] if self.state["assignments"] else None
        self.text(self.pair_view, "No assignment yet." if not a else f"Field={a['field']}\nVoid={a['void']}\nBridge={a['bridge']}\nBranch={a['branch']}\nStatus={a['status']}")
        bridges=[]
        for b in bridge_receipt(self.state):
            bridges.append(f"{'READY' if b['available'] else 'UNAVAILABLE'} {b['name']}\n  {b['executable'] or 'not found'}\n  {', '.join(b['capabilities'])}")
        self.text(self.bridges_view,"\n\n".join(bridges))
        self.text(self.council_view,"\n\n".join(f"{x.get('time')} {x.get('role')}\n{x.get('text','')}" for x in self.state["council"][-100:]) or "Council quiet.")
        self.text(self.journal_view,"\n\n".join(f"{j['time']} L{j['level']} {j['title']} {j['verdict']}\n{j.get('evidence')}\ncheckpoint={j.get('resulting_checkpoint')}" for j in self.state["journal"][:100]) or "No journal yet.")
        standards=self.state["project"].get("standards",{})
        std_lines=[
            f"{'ON' if standards.get('reference_required') else 'OFF'}  Reference required",
            f"{'ON' if standards.get('tests_required') else 'OFF'}  Tests required",
            f"{'ON' if standards.get('independent_void_required') else 'OFF'}  Independent Void required",
            f"{'ON' if standards.get('anti_drift_required') else 'OFF'}  Anti-drift required",
            f"{'ON' if standards.get('simplicity_first') else 'OFF'}  Simplicity first",
            f"{'ON' if standards.get('ease_of_use_first') else 'OFF'}  Ease of use first",
        ]
        self.text(self.standards_view,"\n".join(std_lines))
        toc=[]
        for e in self.state.get("toc",[]):
            toc.append(
                f"{e.get('name')} [{e.get('kind')}]\n"
                f"  path: {e.get('path') or '-'}\n"
                f"  layer: {e.get('layer') if e.get('layer') is not None else '-'}\n"
                f"  branch: {e.get('branch') or '-'}\n"
                f"  program: {e.get('program') or '-'}\n"
                f"  tests: {', '.join(e.get('tests',[])) or '-'}\n"
                f"  validation: {e.get('validation_stage') or '-'}\n"
                f"  purpose: {e.get('purpose') or '-'}\n"
                f"  protected: {'YES' if e.get('protected') else 'NO'}"
            )
        self.text(self.toc_view,"\n\n".join(toc) or "Mediator project map is empty.")
        v=self.state.get("validation",{})
        u=v.get("usefulness",{})
        lines=[
            f"Current stage: {v.get('stage','CONCEPT')}",
            "",
            "Validation ladder:",
            *[f"  {'>' if x==v.get('stage') else ' '} {x}" for x in v.get("stages",[])],
            "",
            f"Usefulness status: {u.get('status','UNPROVEN')}",
            f"Problem: {u.get('problem','') or '-'}",
            f"Expected value: {u.get('expected_user_value','') or '-'}",
            f"Simplest usable outcome: {u.get('simplest_usable_outcome','') or '-'}",
            f"Observed value: {u.get('observed_value','') or '-'}",
        ]
        self.text(self.validation_view,"\n".join(lines))
        save_state(self.state)

    def on_save_project(self,_):
        p=self.state["project"]; p["goal"]=self.goal.get_text(); p["repo"]=self.repo.get_text(); p["base_branch"]=self.branch.get_text() or "main"; p["base_head"]=self.head.get_text(); self.refresh()
    def on_add_step(self,_):
        if self.step_title.get_text().strip(): add_plan_step(self.state,self.step_title.get_text(),self.step_goal.get_text(),self.level.get_selected()+1)
        self.step_title.set_text(""); self.step_goal.set_text(""); self.refresh()
    def on_assign(self,_):
        try: assign_pair(self.state,self.field.get_text(),self.void.get_text())
        except Exception as e: self.state["council"].append({"time":"","role":"MEDIATOR","text":f"HOLD: {e}"})
        self.refresh()
    def on_resolve(self,_):
        labels=["ALLOW","CORRECT","HOLD","ESCALATE"]; verdict=labels[self.verdict.get_selected()]
        buf=self.evidence.get_buffer(); evidence=buf.get_text(buf.get_start_iter(),buf.get_end_iter(),True)
        try:
            resolve_active(self.state,verdict,evidence,self.unresolved.get_text())
            if verdict=="ALLOW" and self.state["project"].get("loop_enabled",True):
                mediator_continue(self.state,self.field.get_text(),self.void.get_text())
        except Exception as e: self.state["council"].append({"time":"","role":"MEDIATOR","text":f"HOLD: {e}"})
        self.refresh()
    def on_loop(self,switch,_): self.state["project"]["loop_enabled"]=switch.get_active(); self.refresh()
    def on_run(self,_):
        try: mediator_continue(self.state,self.field.get_text(),self.void.get_text())
        except Exception as e: self.state["council"].append({"time":"","role":"MEDIATOR","text":f"HOLD: {e}"})
        self.refresh()

def main():
    return CouncilApp().run(None)
