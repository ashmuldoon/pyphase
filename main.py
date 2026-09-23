import sys
import json
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
import numpy as np
import matplotlib.pyplot as plt

try:
    with open(sys.argv[1], encoding='utf-8') as data:
        d = json.load(data)
    data.close()
except FileNotFoundError:
    print("incorrect usage, use \"main.py [file addresss]\" (file not found error)")
    sys.exit(1)
except IndexError:
    print("incorrect usage, use \"main.py [file addresss]\" (index error)")
    sys.exit(1)
except json.JSONDecodeError:
    print("non-json (or incorrectly formatted) file passed, data must be in json format")
    sys.exit(1)

xs = np.array([item["voltage"] for item in d])
ys = np.array([item["concentration"] for item in d])
labels = np.array([item["fractal_shape"] for item in d])

unique_labels = sorted(set(labels))
label_to_int = {l: i for i, l in enumerate(unique_labels)}
z = np.array([label_to_int[l] for l in labels])

X = np.column_stack([xs, ys])

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

clf = SVC(kernel='rbf', C=1.0).fit(X_scaled, z) # do i need to acknowledge this ?
 
print('yoyo')

# adjust range once i find out what it should be ig

grid_x, grid_y = np.mgrid[
    0:10:300j,
    0:1.1:300j
]

print('issues in the scaling bit of skl')

grid_points = np.column_stack([grid_x.ravel(), grid_y.ravel()])
grid_points_scaled = scaler.transform(grid_points)
grid_z = clf.decision_function(grid_points_scaled).reshape(grid_x.shape)

fig, ax = plt.subplots()
ax.contour(grid_x, grid_y, grid_z, levels=[0], colors='k', linewidths=1)

for label in unique_labels:
    mask = np.array(labels) == label
    ax.scatter(xs[mask], ys[mask], label=label)

print('the issues in the showin, matplotlib problem')

ax.set_xlabel("Applied Voltage (V)")
ax.set_ylabel("[ZnSO4(aq)]")
ax.set_xlim(min(xs)-max(xs)/10, (max(xs)+max(xs)/10))
ax.set_ylim(min(ys)-max(ys)/10, max(ys)+max(ys)/10)
ax.legend()
plt.show()

print('success')