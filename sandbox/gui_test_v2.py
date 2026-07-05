

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import seaborn as sns

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import font

# my custom functions
from function_library import load_summary_statistics_for_skaters
from function_library import load_realtime_statistics_for_skaters
from function_library import load_faceoffwins_statistics_for_skaters
from function_library import skater_single_season_fantasy_points
from function_library import find_player_id
from function_library import get_stats_by_season
from function_library import plot_stat_per_game


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


    """ try making plots """
    player_id = find_player_id(fp_skater_name, fp_season)

    df_plots = get_stats_by_season(player_id)

    new_window = tk.Toplevel(root)
    new_window.title("Multiple Plots Tab")
    new_window.geometry("800x500")

    # 2. Create the Notebook (Tab container)
    notebook = ttk.Notebook(new_window)
    notebook.pack(fill='both', expand=True)

    # 3. Create a Frame for the new tab
    tab = ttk.Frame(notebook)
    notebook.add(tab, text="Side-by-Side Plots")
    '''
    # 2. Create a canvas inside the main frame
    canvas = tk.Canvas(tab)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # 3. Add a vertical scrollbar to the main frame
    scrollbar = ttk.Scrollbar(tab, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # 4. Link the canvas scrolling to the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)

    # 5. Create the frame that will hold your actual widgets
    scrollable_frame = ttk.Frame(canvas)

    # 6. Embed the scrollable frame into the canvas window
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # 7. Update the scrollregion dynamically when widgets change size
    def update_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", update_scroll_region)
    '''
    # 4. Create a single Figure with side-by-side axes
    #fig, (ax1, ax2) = Figure(figsize=(7, 4), dpi=100)
    #fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(12, 5))
    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6), (ax7, ax8)) = plt.subplots(nrows=4, ncols=2, figsize=(18, 50))

    # 5. Populate plots with sample data
    plot_stat_per_game(ax1, "ax1", df_plots, False, "gamesPlayed", "Games Played per Season", "Games Played")
    plot_stat_per_game(ax2, "ax2", df_plots, False, "avgToi", "Average Time on Ice per Season", "Average Time on Ice")
    plot_stat_per_game(ax3, "ax3", df_plots, True, "goals_per_game", "Goals/Game per Season", "Goals/Game")
    plot_stat_per_game(ax4, "ax4", df_plots, True, "assists_per_game", "Assists/Game per Season", "Assists/Game")
    plot_stat_per_game(ax5, "ax5", df_plots, True, "points_per_game", "Points/Game per Season", "Points/Game")
    plot_stat_per_game(ax6, "ax6", df_plots, True, "shots_per_game", "Shots/Game per Season", "Shots/Game")
    plot_stat_per_game(ax7, "ax7", df_plots, True, "powerPlayGoals_per_game", "Power Play Goals/Game per Season", "Power Play Goals/Game")
    plot_stat_per_game(ax8, "ax8", df_plots, True, "powerPlayAssists_per_game", "Power Play Assists/Game per Season", "Power Play Assists/Game")

    fig.tight_layout() # Ensures no overlap between plots

    # 6. Embed the figure into the Tkinter Tab
    canvas = FigureCanvasTkAgg(fig, master=tab)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

    # 2. Create a canvas inside the main frame
    #canvas = tk.Canvas(tab)
    #canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # 3. Add a vertical scrollbar to the main frame
    scrollbar = ttk.Scrollbar(tab, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # 4. Link the canvas scrolling to the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)

    # 5. Create the frame that will hold your actual widgets
    scrollable_frame = ttk.Frame(canvas)

    # 6. Embed the scrollable frame into the canvas window
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # 7. Update the scrollregion dynamically when widgets change size
    def update_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", update_scroll_region)



# Initialize the main application window
root = tk.Tk()

# Create a notebook that holds the tabs
notebook = ttk.Notebook(root)

# Create tab frames
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)

# Add the tab frames to the notebook
notebook.add(tab1, text="Tab One")
notebook.add(tab2, text="Tab Two")

notebook.pack(expand=1, fill='both')


root.title("The Amazing Fantasy Hockey Tool (in development)")
root.geometry("1400x800")
root.configure(bg="lightblue")

# Create labels and text entry widgets
tk.Label(tab1, text="Player Name:", font=("Helvetica", 24, "bold")).grid(row=0, column=0, padx=5, pady=50)
fp_skater_name_entry = tk.Entry(tab1, font=("Helvetica", 16, "bold"))
fp_skater_name_entry.grid(row=0, column=1, padx=5, pady=50)

tk.Label(tab1, text="Regular Season:", font=("Helvetica", 24, "bold")).grid(row=0, column=2, padx=5, pady=50)
fp_season_entry = tk.Entry(tab1, font=("Helvetica", 16, "bold"))
fp_season_entry.grid(row=0, column=3, padx=5, pady=50)

tk.Label(tab1, text="Fantasy Points per", font=("Helvetica", 24, "bold")).grid(row=1, column=0, columnspan=4, padx=5, pady=50)

tk.Label(tab1, text="Goal:", font=("Helvetica", 16, "bold")).grid(row=2, column=0, padx=5, pady=5)
fp_goals_entry = tk.Entry(tab1, font=("Helvetica", 16, "bold"))
fp_goals_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(tab1, text="Assist:", font=("Helvetica", 16, "bold")).grid(row=2, column=2, padx=5, pady=5)
fp_assists_entry = tk.Entry(tab1, font=("Helvetica", 16, "bold"))
fp_assists_entry.grid(row=2, column=3, padx=5, pady=5)

tk.Label(tab1, text="PowerPlay Goal Bonus:", font=("Helvetica", 16, "bold")).grid(row=3, column=0, padx=5, pady=5)
fp_pp_goals_entry = tk.Entry(tab1, font=("Helvetica", 16, "bold"))
fp_pp_goals_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Label(tab1, text="Powerplay Assist Bonus:", font=("Helvetica", 16, "bold")).grid(row=3, column=2, padx=5, pady=5)
fp_pp_assists_entry = tk.Entry(tab1, font=("Helvetica", 16, "bold"))
fp_pp_assists_entry.grid(row=3, column=3, padx=5, pady=5)

tk.Label(tab1, text="Short-handed Goal Bonus:", font=("Helvetica", 16, "bold")).grid(row=4, column=0, padx=5, pady=5)
fp_sh_goals_entry = tk.Entry(tab1, font=("Helvetica", 16, "bold"))
fp_sh_goals_entry.grid(row=4, column=1, padx=5, pady=5)

tk.Label(tab1, text="Short-handed Assist Bonus:", font=("Helvetica", 16, "bold")).grid(row=4, column=2, padx=5, pady=5)
fp_sh_assists_entry = tk.Entry(tab1, font=("Helvetica", 16, "bold"))
fp_sh_assists_entry.grid(row=4, column=3, padx=5, pady=5)

tk.Label(tab1, text="Plus/Minus:", font=("Helvetica", 16, "bold")).grid(row=5, column=0, padx=5, pady=5)
fp_plusminus_entry = tk.Entry(tab1, font=("Helvetica", 16, "bold"))
fp_plusminus_entry.grid(row=5, column=1, padx=5, pady=5)

tk.Label(tab1, text="Game Winning Goal Bonus:", font=("Helvetica", 16, "bold")).grid(row=5, column=2, padx=5, pady=5)
fp_game_winning_goals_entry = tk.Entry(tab1, font=("Helvetica", 16, "bold"))
fp_game_winning_goals_entry.grid(row=5, column=3, padx=5, pady=5)

tk.Label(tab1, text="Shot:", font=("Helvetica", 16, "bold")).grid(row=6, column=0, padx=5, pady=5)
fp_shots_entry = tk.Entry(tab1, font=("Helvetica", 16, "bold"))
fp_shots_entry.grid(row=6, column=1, padx=5, pady=5)

tk.Label(tab1, text="Hit:", font=("Helvetica", 16, "bold")).grid(row=6, column=2, padx=5, pady=5)
fp_hits_entry = tk.Entry(tab1, font=("Helvetica", 16, "bold"))
fp_hits_entry.grid(row=6, column=3, padx=5, pady=5)

tk.Label(tab1, text="Block:", font=("Helvetica", 16, "bold")).grid(row=7, column=0, padx=5, pady=5)
fp_blocks_entry = tk.Entry(tab1, font=("Helvetica", 16, "bold"))
fp_blocks_entry.grid(row=7, column=1, padx=5, pady=5)

tk.Label(tab1, text="Penalty Minute:", font=("Helvetica", 16, "bold")).grid(row=7, column=2, padx=5, pady=5)
fp_pims_entry = tk.Entry(tab1, font=("Helvetica", 16, "bold"))
fp_pims_entry.grid(row=7, column=3, padx=5, pady=5)

tk.Label(tab1, text="Face-off Win:", font=("Helvetica", 16, "bold")).grid(row=8, column=0, padx=5, pady=5)
fp_fowins_entry = tk.Entry(tab1, font=("Helvetica", 16, "bold"))
fp_fowins_entry.grid(row=8, column=1, padx=5, pady=5)

tk.Label(tab1, text="Face-off Loss:", font=("Helvetica", 16, "bold")).grid(row=8, column=2, padx=5, pady=5)
fp_folosses_entry = tk.Entry(tab1, font=("Helvetica", 16, "bold"))
fp_folosses_entry.grid(row=8, column=3, padx=5, pady=5)



# Create a button that triggers the run_script function
run_button = tk.Button(tab1, text="Run Script", command=run_script, font=("Helvetica", 24, "bold"))
#run_button.pack(pady=20)
run_button.grid(row=9, column=0, padx=5, pady=50)

tk.Label(tab1, text="Fantasy Points =", font=("Helvetica", 24, "bold")).grid(row=9, column=1, padx=5, pady=50)
output_box = tk.Entry(tab1, font=("Helvetica", 16, "bold"))
output_box.grid(row=9, column=2, padx=5, pady=50)


# Start the GUI event loop
root.mainloop()
