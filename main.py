import sys
from typing import List, Tuple
from parse_temps import parse_raw_temps
from piecewise_interpolation import piecewise_linear_interpolation

def extract_data_points(parsed_temps: List[Tuple[float, List[float]]]) -> List[Tuple[float, float]]:
    """
    Extract data points for interpolation from parsed temperatures.

    Args:
        parsed_temps: A list of tuples where each tuple contains a time step and a list of core temperatures.

    Returns:
        A list of tuples containing time steps and the corresponding average core temperature.
    """
    data_points = []
    for time_step, temps in parsed_temps:
        # Use the first core temperature for simplicity; could also use average, max, etc.
        data_points.append((time_step, temps[0]))
    return data_points

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py sensors-2018.12.26.txt")
        sys.exit(1)

    file_path = sys.argv[1]
    
    with open(file_path, 'r') as file:
        parsed_temps = list(parse_raw_temps(file))

    data_points = extract_data_points(parsed_temps)

    if len(data_point) < 2:
        print("Error: At least two data point are required.")
        sys.exit(1)
    
    x_values = [x for x, y in data_points]
    min_x, max_x = min(x_values), max(x_values)
    while True:
        try:
            x = float(input(f"Enter a value of x between {min_x} and {max_x}: "))
            y = piecewise_linear_interpolation(data_points, x)
            print(f"Interpolated value at x={x}: y={y}")
        except ValueError as e:
            print(e)
            break

if __name__ == "__main__":
    main()