# === IMPORTS ===
from matplotlib import font_manager
from matplotlib.widgets import Button, TextBox
from skyfield.api import load

import matplotlib.animation as animation
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np


# === FIGURE & GRID LAYOUT ===
fig = plt.figure(figsize=(18, 12))
fig.canvas.manager.set_window_title("Solar System Simulation to Compare Planets and their Relative Distances to Earth")
gs = gridspec.GridSpec(3, 2, height_ratios=[1, 1, 1], width_ratios=[3, 1])

# Define subplot locations.
ax_solar_system = plt.subplot(gs[:, 0])
ax_table = plt.subplot(gs[1, 1])
ax_pie_chart = plt.subplot(gs[2, 1])

# Adjust spacing between subplots.
plt.subplots_adjust(hspace=0.5, wspace=0.3)


# === LOAD EPHEMERIS DATA ===
eph = load('de422.bsp')


# === DATA MAPPINGS ===
planet_map = {
    "Mercury":  "MERCURY",
    "Venus":    "VENUS",
    "Earth":    "EARTH",
    "Mars":     "MARS",
    "Jupiter":  "JUPITER BARYCENTER",
    "Saturn":   "SATURN BARYCENTER",
    "Uranus":   "URANUS BARYCENTER",
    "Neptune":  "NEPTUNE BARYCENTER",
}

planet_radii_km = {
    "Mercury":   2439.7,
    "Venus":     6051.8,
    "Earth":     6371.0,
    "Mars":      3389.5,
    "Jupiter":  69911.0,
    "Saturn":   58232.0,
    "Uranus":   25362.0,
    "Neptune":  24622.0
}

# Convert radii to AU and apply a scaling factor for visualisation.
scale_factor = 500000
planet_sizes = {
    planet: (radius_km / 149597870) * scale_factor
    for planet, radius_km in planet_radii_km.items()
}

planet_colors = {
    "Mercury": "#8C8888",
    "Venus":   "#F2DAC4",
    "Earth":   "#BACBD9",
    "Mars":    "#F27A5E",
    "Jupiter": "#BFAE99",
    "Saturn":  "#736A5A",
    "Uranus":  "#95BBBF",
    "Neptune": "#4D5D73",
}


# === SIMULATION SETTINGS ===
start_year = 0
end_year = 2999
step_days = 1
simulation_running = False

# List of all planets (Earth included for visualisation).
planets = list(planet_map.keys())

# 🔥 Create a list of planets for the table (excluding Earth)
table_planets = [p for p in planets if p != "Earth"]


# === TIME SCALE & DATE CALCULATION ===
ts = load.timescale()
dates = []

def update_dates():
    global dates
    dates = [ts.utc(start_year, 1, 1).tt + i for i in range(0, (end_year - start_year) * 365, step_days)]
    dates = ts.tt_jd(dates)
update_dates()


# === INITIALISE TRACKING DATA ===
closest_counts = {planet: 0 for planet in planets}
distance_sums = {planet: 0 for planet in planets}
frame_count = 0


# === SOLAR SYSTEM PLOT SETTINGS ===
axis_limit = 30

ax_solar_system.set_xlim(-axis_limit, axis_limit)
ax_solar_system.set_ylim(-axis_limit, axis_limit)
ax_solar_system.set_xlabel("X Position (AU)")
ax_solar_system.set_ylabel("Y Position (AU)")
ax_solar_system.set_title("Solar System - Top-Down View")
ax_solar_system.set_aspect('equal')

ax_solar_system.scatter(0, 0, color='yellow', label='Sun', s=10)


# === TABLE SETTINGS ===
columns = [
    "Planet",
    "Current Distance\nfrom Earth\n(AU)",
    "Average Distance\nfrom Earth\n(AU)",
    "Current Ranking\nby Distance",
    "Time Closest\nto Earth\n(%)"
]

placeholder_data = [[planet, "-", "-", "-", "-"] for planet in table_planets]

ax_table.axis("off")
ax_pie_chart.axis("off")

data_table = ax_table.table(
    cellText=placeholder_data,
    colLabels=columns,
    loc='center',
    cellLoc='center',
    colColours=["lightgray"] * len(columns)
)

for key, cell in data_table._cells.items():
    if key[0] == 0:
        cell.set_fontsize(20)
        cell.set_height(0.25)
        cell.set_text_props(weight='bold')

data_table.scale(2, 2)


# === PLANETS VISUALISATION ===
planet_scatter = {
    planet: ax_solar_system.scatter([], [], label=planet, color=planet_colors[planet], s=planet_sizes[planet])
    for planet in planets
}

earth_scatter = ax_solar_system.scatter([], [], label="Earth", color=planet_colors["Earth"], s=planet_sizes["Earth"])


# === LEGEND SETTINGS ===
legend_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=planet_colors[planet], markersize=10, label=planet) 
                  for planet in planets]

legend_handles.insert(0, plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='yellow', markersize=12, label='Sun'))

ax_solar_system.legend(handles=legend_handles, loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0)


# === FUNCTIONS ===
def distance(a, b):
    return np.linalg.norm(a - b)

def update_table(current_distances):
    sorted_planets = sorted(
        [p for p in current_distances.keys() if p != "Earth"], 
        key=lambda p: current_distances[p]
    )

    closest_order = {planet: sorted_planets.index(planet) + 1 for planet in sorted_planets}

    closest_percentage = {
        planet: round((closest_counts[planet] / frame_count) * 100, 2) if frame_count > 0 else 0
        for planet in table_planets
    }

    for i, planet in enumerate(table_planets):
        if planet in current_distances:
            avg_distance = distance_sums[planet] / frame_count if frame_count > 0 else 0

            data_table[i+1, 1].get_text().set_text(f"{current_distances[planet]:05.2f}")
            data_table[i+1, 2].get_text().set_text(f"{avg_distance:05.2f}")
            data_table[i+1, 3].get_text().set_text(str(closest_order[planet]))
            data_table[i+1, 4].get_text().set_text(f"{closest_percentage[planet]:05.2f}")

def update(frame):
    global frame_count
    date = dates[frame]
    frame_count += 1

    sun = eph['SUN']
    earth_pos = eph["EARTH"].at(date).position.au - sun.at(date).position.au

    # Retrieve planet positions in a single vectorized call
    planet_positions = np.array([
        (eph[planet_map[p]].at(date).position.au - sun.at(date).position.au)[:2] 
        for p in planets if p != "Earth"
    ])

    # Compute all distances at once
    distances = np.linalg.norm(planet_positions - earth_pos[:2], axis=1)

    # Find the closest planet
    min_index = np.argmin(distances)
    closest_planet = [p for p in planets if p != "Earth"][min_index]

    # Store rounded distances in a dictionary
    current_distances = dict(zip([p for p in planets if p != "Earth"], np.round(distances, 2)))

    # Update distance sums
    for planet, dist in current_distances.items():
        distance_sums[planet] += dist

    # Update scatter plot positions
    x_positions, y_positions = planet_positions[:, 0], planet_positions[:, 1]
    for i, planet in enumerate([p for p in planets if p != "Earth"]):
        planet_scatter[planet].set_offsets([[x_positions[i], y_positions[i]]])


    earth_scatter.set_offsets([[earth_pos[0], earth_pos[1]]])

    if closest_planet:
        closest_counts[closest_planet] += 1

    update_table(current_distances)

    year, month, day, *_ = date.utc
    elapsed_days = frame * step_days
    fig.suptitle(f"Solar System Simulation - Date: {year:04d}-{month:02d}-{day:02d} | Days Elapsed: {elapsed_days}", 
                 fontsize=20, fontweight='bold')

    ax_pie_chart.clear()
    ax_pie_chart.set_title("% Time Closest to Earth", fontweight="bold")

    filtered_counts = {p: v for p, v in closest_counts.items() if v > 0 and p != "Earth"}


    if filtered_counts:
        pie_colors = [planet_colors[p] for p in filtered_counts.keys()]
        ax_pie_chart.pie(filtered_counts.values(), labels=filtered_counts.keys(), autopct='%1.2f%%', startangle=90, pctdistance=0.65, labeldistance=1.15, colors=pie_colors)
    else:
        ax_pie_chart.text(0, 0, "No Data Yet", ha='center', va='center', fontsize=12, fontweight="bold")

    plt.draw()


# === SIMULATIONS ===
ani = None

def start_simulation(event):
    global ani, frame_count, closest_counts, distance_sums
    
    frame_count = 0
    closest_counts = {planet: 0 for planet in planets}
    distance_sums = {planet: 0 for planet in planets}
    update_dates()

    if ani is None:
        ani = animation.FuncAnimation(fig, update, frames=len(dates), interval=1, blit=False, repeat=False)
    
    ani.event_source.start()

def stop_simulation(event):
    if ani is not None:
        ani.event_source.stop()


# === UI ELEMENTS ===
bold_font = font_manager.FontProperties(weight='bold')

ax_textbox_start = plt.axes([0.8125, 0.85, 0.05, 0.05])
textbox_start = TextBox(ax_textbox_start, "Start Year: ", initial=str(start_year))
textbox_start.label.set_fontproperties(bold_font)

ax_textbox_end = plt.axes([0.8125, 0.80, 0.05, 0.05])
textbox_end = TextBox(ax_textbox_end, "End Year: ", initial=str(end_year))
textbox_end.label.set_fontproperties(bold_font)

ax_button_start = plt.axes([0.7625, 0.725, 0.1, 0.05])
button_start = Button(ax_button_start, "Start Simulation", color='lightgreen', hovercolor='limegreen')
button_start.label.set_weight("bold")

ax_button_stop = plt.axes([0.7625, 0.675, 0.1, 0.05])
button_stop = Button(ax_button_stop, "Stop Simulation", color='lightcoral', hovercolor='red')
button_stop.label.set_weight("bold")


# === MAIN EXECUTION ===
button_start.on_clicked(start_simulation)
button_stop.on_clicked(stop_simulation)

plt.show()