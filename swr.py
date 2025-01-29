import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def vswr_to_gamma(vswr):
    """
    Convert a given VSWR to the magnitude of the reflection coefficient Gamma.
    If VSWR is infinite, return 1.
    """
    if np.isinf(vswr):
        return 1.0
    return (vswr - 1) / (vswr + 1)

# List of VSWR values we want to visualize
vswr_list = [np.inf, 5, 4, 3, 2, 1]

# Wave parameters
A = 1.0               # amplitude of the forward wave
f = 1.0               # frequency (Hz)
omega = 2.0 * np.pi * f   # angular frequency
lambda_ = 1.0         # wavelength
k = 2.0 * np.pi / lambda_ # wave number

# Animation / timing parameters
dt = 0.02             # time step between frames
frames_per_cycle = int(1 / (f * dt))  # how many frames in one wave cycle (approx 50 if f=1 and dt=0.02)

warmup_cycles = 2     # how many cycles to run in the "background"
warmup_frames = warmup_cycles * frames_per_cycle
time_offset = warmup_frames * dt  # the offset in seconds at which our displayed animation will start

# Space range for plotting
x_min, x_max = 0, 2
n_points = 200
x = np.linspace(x_min, x_max, n_points)

# Create a figure with one subplot per VSWR
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(12, 6))
axes = axes.flatten()  # Flatten so we can iterate easily

# We'll store line objects so we can update them in the animation
lines_forward = []
lines_reflected = []
lines_total = []
lines_env_max = []
lines_env_min = []

# We also need arrays to store the running max and min for the envelope
max_vals = []
min_vals = []

############################
# 1) INITIALIZE PLOTS
############################
for i, vswr in enumerate(vswr_list):
    ax = axes[i]
    gamma = vswr_to_gamma(vswr)

    # At time = 0 (just for initial plot)
    V_f0 = A * np.cos(omega * 0 - k * x)
    V_r0 = gamma * A * np.cos(omega * 0 + k * x)
    V_tot0 = V_f0 + V_r0

    # Plot forward, reflected, and total waves
    ln_f, = ax.plot(x, V_f0, 'b', label='Forward')
    ln_r, = ax.plot(x, V_r0, 'r', label='Reflected')
    ln_t, = ax.plot(x, V_tot0, 'k', label='Total')

    # Envelope lines (start them at the initial total wave; will be updated)
    ln_env_max, = ax.plot(x, V_tot0, 'k--', alpha=0.5, label='Envelope')
    ln_env_min, = ax.plot(x, V_tot0, 'k--', alpha=0.5)

    # Initialize running max and min for each subplot
    max_vals.append(np.copy(V_tot0))
    min_vals.append(np.copy(V_tot0))

    # Store the line objects
    lines_forward.append(ln_f)
    lines_reflected.append(ln_r)
    lines_total.append(ln_t)
    lines_env_max.append(ln_env_max)
    lines_env_min.append(ln_env_min)

    # Title and legend
    if np.isinf(vswr):
        title_str = f"VSWR = ∞ (Gamma = 1)"
    else:
        title_str = f"VSWR = {vswr}: Γ = {gamma:.2f}"
    ax.set_title(title_str)
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(-2, 2)
    ax.legend(loc='upper right')
    ax.grid(True)

plt.tight_layout()


############################
# 2) WARM-UP (BACKGROUND)
############################
# Run a certain number of frames to fill out the min/max envelopes
for frame in range(warmup_frames):
    t = frame * dt  # time
    for i, vswr in enumerate(vswr_list):
        gamma = vswr_to_gamma(vswr)
        V_f = A * np.cos(omega * t - k * x)
        V_r = gamma * A * np.cos(omega * t + k * x)
        V_tot = V_f + V_r

        # Update envelope tracking (but do NOT update or draw lines yet)
        max_vals[i] = np.maximum(max_vals[i], V_tot)
        min_vals[i] = np.minimum(min_vals[i], V_tot)


############################
# 3) ANIMATION UPDATE
############################
def update(frame):
    # Start from time_offset so we see a "steady-state" wave
    t = time_offset + frame * dt

    updated_artists = []
    for i, vswr in enumerate(vswr_list):
        gamma = vswr_to_gamma(vswr)

        # Compute waveforms at time t
        V_f = A * np.cos(omega * t - k * x)
        V_r = gamma * A * np.cos(omega * t + k * x)
        V_tot = V_f + V_r

        # Update the forward, reflected, total wave lines
        lines_forward[i].set_ydata(V_f)
        lines_reflected[i].set_ydata(V_r)
        lines_total[i].set_ydata(V_tot)

        # The envelopes won't change anymore if we've captured the full wave range
        # But let's keep them updated if you want to track the wave after offset
        max_vals[i] = np.maximum(max_vals[i], V_tot)
        min_vals[i] = np.minimum(min_vals[i], V_tot)

        lines_env_max[i].set_ydata(max_vals[i])
        lines_env_min[i].set_ydata(min_vals[i])

        updated_artists.extend([
            lines_forward[i],
            lines_reflected[i],
            lines_total[i],
            lines_env_max[i],
            lines_env_min[i]
        ])

    return updated_artists

# Create the animation
n_display_frames = 200  # how many frames to display after warm-up
ani = FuncAnimation(fig, update, frames=n_display_frames, interval=50, blit=True)

############################
# 4) SHOW OR SAVE
############################
# Option 1: Show the animation (comment out if you want to only save)
plt.show()

# Option 2: Save to a high-resolution GIF (requires pillow or ImageMagick)
# ani.save('swr_animation.gif', writer='pillow', fps=20, dpi=150)
