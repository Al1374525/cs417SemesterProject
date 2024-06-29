
def calculate_slope(xk, yk, xk1, yk1):
    return (yk1 - yk) / (xk1 - xk)


def calculate_intercept(x, y, slope):
    return y - slope * x

def piecewise_linear_interpolation(data_points, x):
    for i in range(leng(data_points) - 1 ):
        xk, yk = data_points[i]
        xk1, yk1 = data_points[i + 1]
        if xk <= x <= xk1:
            slope = calculate_slope(xk, yk, xk1, yk1)
            intercept = calculate_intercept(xk, yk, slope)
            return slope * x + intercept
    raise ValueError("x value out of range. ")