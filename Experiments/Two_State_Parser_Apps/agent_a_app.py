import tkinter as tk
from tkinter import ttk
from shared_engine import TwoStateAgent, initial_board

AGENT_NAME = "Agent A"
VARIANT = "structure"
SEED = 11

class App:
    def __init__(self, root):
        self.root = root
        root.title(f"{AGENT_NAME} — Two-State Parser")
        root.geometry("850x650")
        self.agent = TwoStateAgent(AGENT_NAME, VARIANT, SEED)
        self.board = initial_board()
        self.side = "r"
        top = ttk.Frame(root); top.pack(fill="x", padx=10, pady=10)
        ttk.Label(top, text=AGENT_NAME, font=("TkDefaultFont",16,"bold")).pack(side="left")
        ttk.Label(top, text=f"  Field ↔ Void | subconscious={self.agent.subconscious_rate}x | variant={VARIANT}").pack(side="left")
        controls = ttk.Frame(root); controls.pack(fill="x", padx=10)
        ttk.Button(controls, text="One decision", command=self.one_decision).pack(side="left", padx=4)
        ttk.Button(controls, text="Run 25 subconscious ticks", command=self.run_sub).pack(side="left", padx=4)
        ttk.Button(controls, text="Reset memory", command=self.reset_memory).pack(side="left", padx=4)
        self.text = tk.Text(root, wrap="word", height=30)
        self.text.pack(fill="both", expand=True, padx=10, pady=10)
        self.show_state("Ready.")

    def show_state(self, msg):
        self.text.delete("1.0","end")
        self.text.insert("end", msg+"\n\n")
        self.text.insert("end", f"Agent: {self.agent.name}\nVariant: {self.agent.variant}\n")
        self.text.insert("end", f"Subconscious ticks: {self.agent.memory.subconscious_ticks}\n")
        self.text.insert("end", f"Remembered positions: {len(self.agent.memory.recent_positions)}\n")
        self.text.insert("end", f"Learned move scores: {len(self.agent.memory.move_scores)}\n")
        self.text.insert("end", "\nFIELD proposes → VOID checks → ACCEPT/HOLD/REJECT → memory consequence → subconscious repeats\n")

    def one_decision(self):
        state, move, score = self.agent.decide(self.board, self.side)
        self.show_state(f"Decision state: {state}\nMove: {move}\nVoid score: {score:.3f}")

    def run_sub(self):
        for _ in range(25): self.agent.subconscious_tick(self.board, self.side)
        self.show_state("Ran 25 subconscious cycles.")

    def reset_memory(self):
        self.agent = TwoStateAgent(AGENT_NAME, VARIANT, SEED)
        self.show_state("Memory reset.")

if __name__ == "__main__":
    root = tk.Tk(); App(root); root.mainloop()
