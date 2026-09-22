import sys
import json
import numpy as np
import matplotlib.pyplot as plt

start = float(sys.argv[2]) if sys.argv[2] else 0.0
end = float(sys.argv[3]) if sys.argv[3] else 10.0
x_step = float(sys.argv[4]) if sys.argv[4] else 0.1
y_step = float(sys.argv[5]) if sys.argv[5] else 0.1

try:
    with open(sys.argv[1]) as data:
        d = json.load(data)
    data.close()
except FileNotFoundError:
    print("incorrect usage, use \"main.py [file addresss]\"")
    sys.exit(1)
except IndexError:
    print("incorrect usage, use \"main.py [file addresss]\"")
    sys.exit(1)
except json.JSONDecodeError:
    print("non-json (or incorrectly formatted) file passed, data must be in json format")
    sys.exit(1)

conc_values = np.array([item["concentration"] for item in d])
voltage_values = np.array([item["concentration"] for item in d])
fractal_shapes = np.array([item["fractal_shape"] for item in d])

unique_shapes = sorted(set(fractal_shapes))
cmap = plt.get_cmap('tab10')

# nearest neighbour integration
def distance_to_data(x2, y2, x, y):
    """its a distance function im just writing this to get my linter to be quiet"""
    return np.sqrt((x2-x)^2+(y2-y)^2)

def draw_phase_line(y_data):
    """compute find and draw line seperating phases"""
    for x in np.arange(start, end, x_step):
        for y in np.arange(0, max(y_data), y_step):
            nearest_neighbour = distance_to_data(conc_values, voltage_values, x, y)
            print(nearest_neighbour)
    return 0





# plot everything

for i, shape in enumerate(unique_shapes):
    mask = fractal_shapes == shape
    plt.scatter(
        conc_values[mask],
        voltage_values[mask],
        c=[cmap(i)],
        label=shape
    )

plt.xlabel("Voltage")
plt.ylabel("Concentration")
plt.legend()
plt.show()