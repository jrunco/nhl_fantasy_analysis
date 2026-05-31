

import numpy as np
import pandas as pd

import tkinter as tk
from tkinter import messagebox
from tkinter import font

# my custom functions
from function_library import load_summary_statistics_for_skaters
from function_library import load_realtime_statistics_for_skaters
from function_library import load_faceoffwins_statistics_for_skaters
from function_library import skater_single_season_fantasy_points


# Tell Windows to use crisp, native DPI scaling
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass  # Handles errors if run on non-Windows OS


def run_script():

    # 1. Retrieve user inputs from entry fields
    fp_skater_name = fp_skater_name_entry.get()
    fp_season = fp_season_entry.get()
    fp_goals = fp_goals_entry.get()
    fp_assists = fp_assists_entry.get()
    fp_plusminus = fp_plusminus_entry.get()
    fp_pp_goals = fp_pp_goals_entry.get()
    fp_pp_assists = fp_pp_assists_entry.get()
    fp_sh_goals = fp_sh_goals_entry.get()
    fp_sh_assists = fp_sh_assists_entry.get()
    fp_game_winning_goals = fp_game_winning_goals_entry.get()
    fp_shots = fp_shots_entry.get()
    fp_hits = fp_hits_entry.get()
    fp_blocks = fp_blocks_entry.get()
    fp_fowins = fp_fowins_entry.get()
    fp_folosses = fp_folosses_entry.get()
    fp_pims = fp_pims_entry.get()

    # 2. Logic to "run" your script based on these inputs
    result = skater_single_season_fantasy_points(
        fp_skater_name,
        fp_season,
        fp_goals,
        fp_assists,
        fp_plusminus,
        fp_pp_goals,
        fp_pp_assists,
        fp_sh_goals,
        fp_sh_assists,
        fp_game_winning_goals,
        fp_shots,
        fp_hits,
        fp_blocks,
        fp_fowins,
        fp_folosses,
        fp_pims,
        )

    output_box.insert(0, result)
    #messagebox.showinfo("# of fantasy points", result)
    #return result


# Initialize the main application window
root = tk.Tk()
root.title("The Amazing Fantasy Hockey Tool (in development)")
root.geometry("1400x800")
root.configure(bg="lightblue")

# Create labels and text entry widgets
tk.Label(root, text="Player Name:", font=("Helvetica", 24, "bold")).grid(row=0, column=0, padx=5, pady=50)
fp_skater_name_entry = tk.Entry(root, font=("Helvetica", 16, "bold"))
fp_skater_name_entry.grid(row=0, column=1, padx=5, pady=50)

tk.Label(root, text="Regular Season:", font=("Helvetica", 24, "bold")).grid(row=0, column=2, padx=5, pady=50)
fp_season_entry = tk.Entry(root, font=("Helvetica", 16, "bold"))
fp_season_entry.grid(row=0, column=3, padx=5, pady=50)

tk.Label(root, text="Fantasy Points per", font=("Helvetica", 24, "bold")).grid(row=1, column=0, columnspan=4, padx=5, pady=50)

tk.Label(root, text="Goal:", font=("Helvetica", 16, "bold")).grid(row=2, column=0, padx=5, pady=5)
fp_goals_entry = tk.Entry(root, font=("Helvetica", 16, "bold"))
fp_goals_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Assist:", font=("Helvetica", 16, "bold")).grid(row=2, column=2, padx=5, pady=5)
fp_assists_entry = tk.Entry(root, font=("Helvetica", 16, "bold"))
fp_assists_entry.grid(row=2, column=3, padx=5, pady=5)

tk.Label(root, text="PowerPlay Goal Bonus:", font=("Helvetica", 16, "bold")).grid(row=3, column=0, padx=5, pady=5)
fp_pp_goals_entry = tk.Entry(root, font=("Helvetica", 16, "bold"))
fp_pp_goals_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Label(root, text="Powerplay Assist Bonus:", font=("Helvetica", 16, "bold")).grid(row=3, column=2, padx=5, pady=5)
fp_pp_assists_entry = tk.Entry(root, font=("Helvetica", 16, "bold"))
fp_pp_assists_entry.grid(row=3, column=3, padx=5, pady=5)

tk.Label(root, text="Short-handed Goal Bonus:", font=("Helvetica", 16, "bold")).grid(row=4, column=0, padx=5, pady=5)
fp_sh_goals_entry = tk.Entry(root, font=("Helvetica", 16, "bold"))
fp_sh_goals_entry.grid(row=4, column=1, padx=5, pady=5)

tk.Label(root, text="Short-handed Assist Bonus:", font=("Helvetica", 16, "bold")).grid(row=4, column=2, padx=5, pady=5)
fp_sh_assists_entry = tk.Entry(root, font=("Helvetica", 16, "bold"))
fp_sh_assists_entry.grid(row=4, column=3, padx=5, pady=5)

tk.Label(root, text="Plus/Minus:", font=("Helvetica", 16, "bold")).grid(row=5, column=0, padx=5, pady=5)
fp_plusminus_entry = tk.Entry(root, font=("Helvetica", 16, "bold"))
fp_plusminus_entry.grid(row=5, column=1, padx=5, pady=5)

tk.Label(root, text="Game Winning Goal Bonus:", font=("Helvetica", 16, "bold")).grid(row=5, column=2, padx=5, pady=5)
fp_game_winning_goals_entry = tk.Entry(root, font=("Helvetica", 16, "bold"))
fp_game_winning_goals_entry.grid(row=5, column=3, padx=5, pady=5)

tk.Label(root, text="Shot:", font=("Helvetica", 16, "bold")).grid(row=6, column=0, padx=5, pady=5)
fp_shots_entry = tk.Entry(root, font=("Helvetica", 16, "bold"))
fp_shots_entry.grid(row=6, column=1, padx=5, pady=5)

tk.Label(root, text="Hit:", font=("Helvetica", 16, "bold")).grid(row=6, column=2, padx=5, pady=5)
fp_hits_entry = tk.Entry(root, font=("Helvetica", 16, "bold"))
fp_hits_entry.grid(row=6, column=3, padx=5, pady=5)

tk.Label(root, text="Block:", font=("Helvetica", 16, "bold")).grid(row=7, column=0, padx=5, pady=5)
fp_blocks_entry = tk.Entry(root, font=("Helvetica", 16, "bold"))
fp_blocks_entry.grid(row=7, column=1, padx=5, pady=5)

tk.Label(root, text="Penalty Minute:", font=("Helvetica", 16, "bold")).grid(row=7, column=2, padx=5, pady=5)
fp_pims_entry = tk.Entry(root, font=("Helvetica", 16, "bold"))
fp_pims_entry.grid(row=7, column=3, padx=5, pady=5)

tk.Label(root, text="Face-off Win:", font=("Helvetica", 16, "bold")).grid(row=8, column=0, padx=5, pady=5)
fp_fowins_entry = tk.Entry(root, font=("Helvetica", 16, "bold"))
fp_fowins_entry.grid(row=8, column=1, padx=5, pady=5)

tk.Label(root, text="Face-off Loss:", font=("Helvetica", 16, "bold")).grid(row=8, column=2, padx=5, pady=5)
fp_folosses_entry = tk.Entry(root, font=("Helvetica", 16, "bold"))
fp_folosses_entry.grid(row=8, column=3, padx=5, pady=5)




"""
tk.Label(root, text="Player Name:", font=("Helvetica", 24, "bold")).grid(row=0, column=1, padx=5, pady=50)
fp_skater_name_entry = tk.Entry(root, font=("Helvetica", 16, "bold"))
fp_skater_name_entry.grid(row=0, column=2, padx=5, pady=50)

tk.Label(root, text="Regular Season:", font=("Helvetica", 24, "bold")).grid(row=0, column=3, padx=5, pady=50)
fp_season_entry = tk.Entry(root, font=("Helvetica", 16, "bold"))
fp_season_entry.grid(row=0, column=4, padx=5, pady=50)

tk.Label(root, text="Fantasy Points per:", font=("Helvetica", 24, "bold")).grid(row=1, column=2, padx=5, pady=50)

tk.Label(root, text="Goal:", font=("Helvetica", 16, "bold")).grid(row=2, column=0, padx=5, pady=5)
fp_goals_entry = tk.Entry(root, font=("Helvetica", 16, "bold"))
fp_goals_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Assist:", font=("Helvetica", 16, "bold")).grid(row=2, column=2, padx=5, pady=5)
fp_assists_entry = tk.Entry(root, font=("Helvetica", 16, "bold"))
fp_assists_entry.grid(row=2, column=3, padx=5, pady=5)

tk.Label(root, text="Plus/Minus:", font=("Helvetica", 16, "bold")).grid(row=2, column=4, padx=5, pady=5)
fp_plusminus_entry = tk.Entry(root, font=("Helvetica", 16, "bold"))
fp_plusminus_entry.grid(row=2, column=5, padx=5, pady=5)

tk.Label(root, text="PowerPlay Goal Bonus:", font=("Helvetica", 16, "bold")).grid(row=3, column=0, padx=5, pady=5)
fp_pp_goals_entry = tk.Entry(root, font=("Helvetica", 16, "bold"))
fp_pp_goals_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Label(root, text="Powerplay Assist Bonus:", font=("Helvetica", 16, "bold")).grid(row=3, column=2, padx=5, pady=5)
fp_pp_assists_entry = tk.Entry(root, font=("Helvetica", 16, "bold"))
fp_pp_assists_entry.grid(row=3, column=3, padx=5, pady=5)

tk.Label(root, text="Short-handed Goal Bonus:", font=("Helvetica", 16, "bold")).grid(row=4, column=0, padx=5, pady=5)
fp_sh_goals_entry = tk.Entry(root, font=("Helvetica", 16, "bold"))
fp_sh_goals_entry.grid(row=4, column=1, padx=5, pady=5)

tk.Label(root, text="Short-handed Assist Bonus:", font=("Helvetica", 16, "bold")).grid(row=4, column=2, padx=5, pady=5)
fp_sh_assists_entry = tk.Entry(root, font=("Helvetica", 16, "bold"))
fp_sh_assists_entry.grid(row=4, column=3, padx=5, pady=5)

tk.Label(root, text="Game Winning Goal Bonus:", font=("Helvetica", 16, "bold")).grid(row=5, column=0, padx=5, pady=5)
fp_game_winning_goals_entry = tk.Entry(root, font=("Helvetica", 16, "bold"))
fp_game_winning_goals_entry.grid(row=5, column=1, padx=5, pady=5)

tk.Label(root, text="Shot:", font=("Helvetica", 16, "bold")).grid(row=5, column=2, padx=5, pady=5)
fp_shots_entry = tk.Entry(root, font=("Helvetica", 16, "bold"))
fp_shots_entry.grid(row=5, column=3, padx=5, pady=5)

tk.Label(root, text="Hit:", font=("Helvetica", 16, "bold")).grid(row=6, column=0, padx=5, pady=5)
fp_hits_entry = tk.Entry(root, font=("Helvetica", 16, "bold"))
fp_hits_entry.grid(row=6, column=1, padx=5, pady=5)

tk.Label(root, text="Block:", font=("Helvetica", 16, "bold")).grid(row=6, column=2, padx=5, pady=5)
fp_blocks_entry = tk.Entry(root, font=("Helvetica", 16, "bold"))
fp_blocks_entry.grid(row=6, column=3, padx=5, pady=5)

tk.Label(root, text="Penalty Minute:", font=("Helvetica", 16, "bold")).grid(row=6, column=4, padx=5, pady=5)
fp_pims_entry = tk.Entry(root, font=("Helvetica", 16, "bold"))
fp_pims_entry.grid(row=6, column=5, padx=5, pady=5)

tk.Label(root, text="Face-off Win:", font=("Helvetica", 16, "bold")).grid(row=7, column=0, padx=5, pady=5)
fp_fowins_entry = tk.Entry(root, font=("Helvetica", 16, "bold"))
fp_fowins_entry.grid(row=7, column=1, padx=5, pady=5)

tk.Label(root, text="Face-off Loss:", font=("Helvetica", 16, "bold")).grid(row=7, column=2, padx=5, pady=5)
fp_folosses_entry = tk.Entry(root, font=("Helvetica", 16, "bold"))
fp_folosses_entry.grid(row=7, column=3, padx=5, pady=5)
"""



# Create a button that triggers the run_script function
run_button = tk.Button(root, text="Run Script", command=run_script, font=("Helvetica", 24, "bold"))
#run_button.pack(pady=20)
run_button.grid(row=9, column=0, padx=5, pady=50)

tk.Label(root, text="Fantasy Points =", font=("Helvetica", 24, "bold")).grid(row=9, column=1, padx=5, pady=50)
output_box = tk.Entry(root, font=("Helvetica", 16, "bold"))
output_box.grid(row=9, column=2, padx=5, pady=50)


# Start the GUI event loop
root.mainloop()
