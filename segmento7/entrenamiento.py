import numpy as np

# -------------------------------
# Codificación en 7 segmentos
X = np.array([
    [1,1,1,1,1,1,0],  # 0
    [0,1,1,0,0,0,0],  # 1
    [1,1,0,1,1,0,1],  # 2
    [1,1,1,1,0,0,1],  # 3
    [0,1,1,0,0,1,1],  # 4
    [1,0,1,1,0,1,1],  # 5
    [1,0,1,1,1,1,1],  # 6
    [1,1,1,0,0,0,0],  # 7
    [1,1,1,1,1,1,1],  # 8
    [1,1,1,1,0,1,1]   # 9
])
X_bias = np.hstack((np.ones((X.shape[0], 1)), X))  # (10,8)

# Salidas: [<=5, Par, Primo]
D = np.array([
    [1,1,0], [1,0,0], [1,1,1], [1,0,1], [1,1,0],
    [1,0,1], [0,1,0], [0,0,1], [0,1,0], [0,0,0]
])

# -------------------------------
# Parámetros
eta = 0.1
max_epochs = 100
threshold = 0
n_inputs = X_bias.shape[1]
n_outputs = D.shape[1]
W = np.random.uniform(-0.5, 0.5, size=(n_outputs, n_inputs))

def step(x): return np.where(x > threshold, 1, 0)

# -------------------------------
# Entrenamiento
for epoch in range(max_epochs):
    total_errors = 0
    for i in range(len(X_bias)):
        x = X_bias[i]
        d = D[i]
        y = step(W @ x)
        e = d - y
        total_errors += np.sum(np.abs(e))
        for j in range(n_outputs):
            W[j] += eta * e[j] * x
    if total_errors == 0:
        break

# -------------------------------
# Guardar pesos en .txt
np.savetxt("pesos_entrenados.txt", W, fmt="%.4f")
print("\n✅ Pesos entrenados guardados en 'pesos_entrenados.txt'")
