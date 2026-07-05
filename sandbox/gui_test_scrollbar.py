import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# my custom functions
from function_library import load_summary_statistics_for_skaters
from function_library import load_realtime_statistics_for_skaters
from function_library import load_faceoffwins_statistics_for_skaters
from function_library import skater_single_season_fantasy_points
from function_library import find_player_id
from function_library import get_stats_by_season
from function_library import plot_stat_per_game


# 1. Initialize Root Window
root = tk.Tk()
root.title("Scrollable Plot")
root.geometry("600x500")

# 2. Create the Matplotlib Figure (Make it wider/taller to force scrolling)


fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6), (ax7, ax8)) = plt.subplots(nrows=4, ncols=2, figsize=(18, 50))

    # 5. Populate plots with sample data
ax1.plot(range(100), range(100)) # Sample large data
ax2.plot(range(100), range(100)) # Sample large data
ax3.plot(range(100), range(100)) # Sample large data
ax4.plot(range(100), range(100)) # Sample large data
ax5.plot(range(100), range(100)) # Sample large data
ax6.plot(range(100), range(100)) # Sample large data
ax7.plot(range(100), range(100)) # Sample large data
ax8.plot(range(100), range(100)) # Sample large data

fig.tight_layout() # Ensures no overlap between plots

# 3. Create Container Frame and Outer Canvas
container = ttk.Frame(root)
container.pack(fill=tk.BOTH, expand=True)

# 4. Create Scrollable Canvas
scroll_canvas = tk.Canvas(container, highlightthickness=0)
scroll_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# 5. Add Scrollbars
v_scrollbar = ttk.Scrollbar(container, orient="vertical", command=scroll_canvas.yview)
v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

h_scrollbar = ttk.Scrollbar(container, orient="horizontal", command=scroll_canvas.xview)
h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

# 6. Configure the Canvas to recognize scrollbars
scroll_canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
scroll_canvas.bind('<Configure>', lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all")))

# 7. Embed the Matplotlib Canvas inside the scrollable canvas
canvas_widget = FigureCanvasTkAgg(fig, master=scroll_canvas)
canvas_widget.draw()

# Create a window inside the scrollable canvas to hold the FigureCanvasTkAgg
plot_window = scroll_canvas.create_window((0, 0), window=canvas_widget.get_tk_widget(), anchor="nw")

# 8. Manage resizing gracefully
def on_canvas_configure(event):
    # Adjust the inner window size to match the outer canvas size
    scroll_canvas.itemconfig(plot_window, width=event.width, height=event.height)

scroll_canvas.bind('<Configure>', on_canvas_configure)

root.mainloop()
