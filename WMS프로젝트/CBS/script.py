import pandas as pd
import matplotlib.pyplot as plt

# 맵 읽기
WAREHOUSE_MAP = pd.read_csv('WarehouseGrid.csv', header=None).values

# 맵 시각화
plt.imshow(WAREHOUSE_MAP, cmap='gray_r')
plt.title('Warehouse Map')
plt.show()

# AGENT 좌표
AGENTS = [
    {'start': (0, 0), 'goal': (5, 9)},
    {'start': (0, 9), 'goal': (5, 0)},
    {'start': (5, 0), 'goal': (0, 9)},
    {'start': (5, 9), 'goal': (0, 0)},
    {'start': (2, 0), 'goal': (2, 9)},
    {'start': (3, 9), 'goal': (3, 0)},
    {'start': (0, 4), 'goal': (5, 4)},
    {'start': (5, 4), 'goal': (0, 4)},
]

for i, agent in enumerate(AGENTS):
    s = agent['start']
    g = agent['goal']
    s_val = WAREHOUSE_MAP[s[0], s[1]]
    g_val = WAREHOUSE_MAP[g[0], g[1]]
    print(f"Agent {i}: start={s}({s_val}), goal={g}({g_val})")
