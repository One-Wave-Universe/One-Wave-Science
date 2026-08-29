import tkinter as tk
from tkinter import ttk
from shared_engine import TwoStateAgent, play_game

class Arena:
    def __init__(self, root):
        self.root=root
        root.title("Two-State Parser Checkers Arena")
        root.geometry("900x700")
        self.a = TwoStateAgent("Agent A","structure",11)
        self.b = TwoStateAgent("Agent B","novelty",29)
        bar=ttk.Frame(root); bar.pack(fill="x",padx=10,pady=10)
        ttk.Button(bar,text="Play 1 game",command=lambda:self.run(1)).pack(side="left",padx=4)
        ttk.Button(bar,text="Play 25 games",command=lambda:self.run(25)).pack(side="left",padx=4)
        ttk.Button(bar,text="Play 100 games",command=lambda:self.run(100)).pack(side="left",padx=4)
        ttk.Button(bar,text="Reset agents",command=self.reset).pack(side="left",padx=4)
        self.out=tk.Text(root,wrap="word")
        self.out.pack(fill="both",expand=True,padx=10,pady=10)
        self.out.insert("end","Agent A = Field+Void+subconscious(structure)\nAgent B = Field+Void+subconscious(novelty)\n")

    def reset(self):
        self.a = TwoStateAgent("Agent A","structure",11)
        self.b = TwoStateAgent("Agent B","novelty",29)
        self.out.delete("1.0","end")
        self.out.insert("end","Agents reset.\n")

    def run(self,n):
        wins={"A":0,"B":0,"draw":0}
        for i in range(n):
            if i%2==0:
                winner,board,log=play_game(self.a,self.b)
                if winner=="r": wins["A"]+=1
                elif winner=="b": wins["B"]+=1
                else: wins["draw"]+=1
            else:
                winner,board,log=play_game(self.b,self.a)
                if winner=="r": wins["B"]+=1
                elif winner=="b": wins["A"]+=1
                else: wins["draw"]+=1
        self.out.insert("end",f"\n{n} games → A {wins['A']} | B {wins['B']} | draws {wins['draw']}\n")
        self.out.insert("end",f"A subconscious ticks: {self.a.memory.subconscious_ticks}, learned moves: {len(self.a.memory.move_scores)}\n")
        self.out.insert("end",f"B subconscious ticks: {self.b.memory.subconscious_ticks}, learned moves: {len(self.b.memory.move_scores)}\n")
        self.out.see("end")

if __name__=="__main__":
    r=tk.Tk(); Arena(r); r.mainloop()
