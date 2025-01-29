# Standing Wave Ratio (SWR) Visualization

![SWR Animation](./swr_animation.gif)

## Overview

This repository contains a Python script that generates an animated visualization of *Standing Wave Ratio (SWR)* and the corresponding *reflection coefficient (Gamma)*. You will see three waveforms in each subplot:

1. **Forward Wave** (blue)  
2. **Reflected Wave** (red)  
3. **Total Wave** (black)  

Additionally, the script keeps track of the maximum and minimum envelopes (shown as dashed black lines). This creates a clear demonstration of how standing waves form when a wave is partially (or completely) reflected.

---

## What is SWR?

**Standing Wave Ratio (SWR)** is a measure commonly used in RF (Radio Frequency) and transmission line theory. When a wave travels down a transmission line and encounters an impedance mismatch, part of the wave is reflected back. As the forward and reflected waves interfere, standing waves can form.

If we look at voltage along the line, the Voltage Standing Wave Ratio (VSWR) is given by:

**VSWR = V_max / V_min**

where  
- V_max is the maximum voltage amplitude along the line.  
- V_min is the minimum voltage amplitude along the line.  

- If there is no reflection (perfect match), VSWR = 1.  
- If there is total reflection (complete mismatch), VSWR can be considered infinite (∞).  

Intuitively, an SWR of 1 (forward wave only, no reflection) means no standing wave is formed. A large SWR (much greater than 1) means significant reflection and more pronounced standing waves.

---

## What is Gamma (Γ)?

**Gamma (Γ)**, also known as the **reflection coefficient**, is a complex quantity that describes how much of the wave is reflected (and with what phase shift). Here, we focus on its magnitude, which ranges from 0 to 1:

- Γ = 0 means there is no reflection.
- Γ = 1 means there is total reflection.

When dealing with VSWR, the magnitude of Γ for a given VSWR is:

**Gamma = (VSWR - 1) / (VSWR + 1)**

When VSWR = ∞, Gamma = 1.

---

## Animation Explanation

Each subplot corresponds to a different VSWR:

- The **forward wave** is shown in blue.  
- The **reflected wave** is shown in red.  
- The **total wave** (the sum of forward and reflected) is shown in black.  
- The dashed black lines are the **envelope max** and **envelope min**, which highlight the standing wave peaks and troughs.

By observing each subplot, you can see how higher reflection (larger VSWR) leads to more pronounced standing waves. The envelope lines become taller and deeper as VSWR increases.

---

## How to Run the Code

1. **Dependencies**  
   - Python 3.x  
   - NumPy  
   - Matplotlib  
   - (Optional) Pillow or ImageMagick (to save the animation as a GIF)  

   You can install these via:  
   ```
   pip install numpy matplotlib pillow
   ```

2. **Obtain the Script**  
   - Clone or download this repository.  
   - Save the script as `swr.py` (or any name you prefer).

3. **Run the Script**  
   ```
   python swr.py
   ```
   - This will open a window showing the animated waves.  
   - After the animation completes, a GIF file named `swr_animation.gif` will be created in the same directory.

4. **View the Saved Animation**  
   - Open `swr_animation.gif` in any image viewer that supports GIF playback.

---

### Customizing the Script

- **VSWR Values**: Edit the `vswr_list` array to add or remove VSWR values for visualization.  
- **Wave Parameters**: Adjust amplitude (`A`), frequency (`f`), or wavelength (`lambda_`) to see different wave behaviors.  
- **Animation**:  
  - Change `n_display_frames` to control how long the animation runs.  
  - Adjust `frames_per_cycle`, `warmup_cycles`, or `warmup_frames` to tweak how the envelope is captured.  
  - Disable the `plt.show()` line if you only want to save the GIF without displaying it.

---
