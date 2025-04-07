import json
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from collections import defaultdict

# Загружаем данные
with open("debug_data.json", "r") as f:
    data = json.load(f)

# Группируем по эпизодам
episodes = defaultdict(list)
for row in data:
    episodes[row["episode"]].append(row)

episode_ids = sorted(episodes.keys())

# Создаем график
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)

# Линии графика
adv_line, = ax.plot([], [], label="Advantage")
val_line, = ax.plot([], [], label="Value Prediction")
tgt_line, = ax.plot([], [], label="Target Return")

ax.set_title("Episode Debug Viewer")
ax.set_xlabel("Step")
ax.set_ylabel("Value")
ax.legend()

# Слайдер
ax_slider = plt.axes([0.2, 0.05, 0.6, 0.03])
slider = Slider(ax_slider, "Episode", 0, len(episode_ids) - 1, valinit=0, valstep=1)

def update(val):
    idx = int(slider.val)
    ep = episode_ids[idx]
    rows = episodes[ep]

    steps = [r["step"] for r in rows]
    adv = [r["advantage"] for r in rows]
    valp = [r["value_pred"] for r in rows]
    tgt = [r["target"] for r in rows]

    adv_line.set_data(steps, adv)
    val_line.set_data(steps, valp)
    tgt_line.set_data(steps, tgt)

    ax.relim()
    ax.autoscale_view()
    ax.set_title(f"Episode {ep}")
    fig.canvas.draw_idle()

slider.on_changed(update)
update(0)
plt.show()
