import sys
from typing import List, Tuple
from modules.parse_temps import parse_raw_temps
from modules.piecewise_interpolation import piecewise_linear_interpolation, calculate_slope, calculate_intercept
from modules.global_lin_piecewise import least_squares_approximation, predict
import os
def extract_data_points(parsed_temps: List[Tuple[float, List[float]]], core_idx: int) -> List[Tuple[float, float]]:
    """
    Extract data points for interpolation from parsed temperatures.

    Args:
        parsed_temps: A list of tuples where each tuple contains a time step and a list of core temperatures.

    Returns:
        A list of tuples containing time steps and the corresponding average core temperature.
    """
    data_points = []
    for time_step, temps in parsed_temps:
        data_points.append((time_step, temps[core_idx]))
    return data_points

def write_interpolation_file(file_path, data_points, core_idx):
    with open(file_path, 'w') as f:
        for i in range(len(data_points) - 1):
            xk, yk = data_points[i]
            xk1, yk1 = data_points[i + 1]
            slope = calculate_slope(xk, yk, xk1, yk1)
            intercept = calculate_intercept(xk, yk, slope)
            f.write(f"{xk:.6f} <= x <= {xk1:.6f} ; y = {intercept:.4f} + {slope:.4f} x ; interpolation\n")

def write_least_squares_file(file_path, data_points):
    x_values = [x for x, y in data_points]
    y_values = [y for x, y in data_points]
    m, c = least_squares_approximation(x_values, y_values)
    with open(file_path, 'a') as f:
        f.write(f"{x_values[0]:.6f} <= x <= {x_values[-1]:.6f} ; y = {c:.4f} + {m:.4f} x ; least-squares\n")

def main():
     print(f"Arguments received: {sys.argv}")
     if len(sys.argv) != 2:
        print("Usage: python3 main.py sensors-2018.12.26.txt")
        sys.exit(1)

     file_path = sys.argv[1]
    
     if not os.path.isfile(file_path):
        print(f"Error: File {file_path} does not exist.")
        sys.exit(1)
    
     with open(file_path, 'r') as file:
        parsed_temps = list(parse_raw_temps(file))

     num_cores = len(parsed_temps[0][1])

     for core_idx in range(num_cores):
        data_points = extract_data_points(parsed_temps, core_idx)

        if len(data_points) < 2:
            print(f"Error: At least two data points are required for core {core_idx}.")
            continue

        output_file = f"sample-input-core-{core_idx:02}.txt"
        write_interpolation_file(output_file, data_points, core_idx)
        write_least_squares_file(output_file, data_points)

if __name__ == "__main__":
    main()