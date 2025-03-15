# Milky Way Planets and Their Relative Distances to Earth

## Description
Milky Way Planets and Their Relative Distances to Earth is a Python-based simulation that visualises the relative distances of planets in the Solar System to Earth over time. The project utilises `matplotlib`, `skyfield`, and various Python libraries to generate dynamic visual representations, including a top-down view of the Solar System, a data table of distances, and a pie chart of how often each planet is closest to Earth.

## Demo

<p align="center">
  <img src="Demo.gif" alt="Demo" width="800">
</p>

## Getting Started

### Dependencies
- Python 3.x
- `matplotlib`
- `numpy`
- `skyfield`

You can install dependencies using:

```bash
pip install matplotlib numpy skyfield
```

### Executing the Program

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/Milky-Way-Planets-And-Their-Relative-Distances-To-Earth.git
   cd Milky-Way-Planets-And-Their-Relative-Distances-To-Earth
   ```

2. Run the script:

   ```bash
   python milky-way-planets-and-their-relative-distances-to-earth.py
   ```

## Features

- **Solar System Visualisation**: A top-down view of the Solar System, showing planetary positions relative to Earth.
- **Live Data Simulation**: Uses `skyfield` ephemeris data to calculate accurate planetary positions.
- **Dynamic Table of Distances**: Displays real-time calculations of each planet's distance from Earth.
- **Ranking System**: Sorts planets based on their distance from Earth at each simulation step.
- **Pie Chart Statistics**: Shows the percentage of time each planet is the closest to Earth during the simulation.
- **User Controls**:
  - Start and stop simulation buttons.
  - Adjustable start and end years using text boxes.
- **Color-coded Planet Representations**: Uses predefined colors for each planet to enhance visualisation.
- **Smooth Animations**: Animated updates for planetary motion and statistics.

## Roadmap

- Improve UI elements with interactive controls.
- Allow users to choose specific planets for a closer comparison.
- Add real-time speed controls for the simulation.
- Faster simulation via a game engine/PyQtGraph library.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- **Skyfield**: Used for astronomical calculations.
- **Matplotlib**: Used for visualisation and graphing.
- **NASA Ephemeris Data**: Provides planetary position data.
- **Inspired by various space simulation tools and astronomy research.**

