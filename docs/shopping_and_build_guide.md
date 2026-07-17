# Raspberry Pi IR Blaster: Daikin AC Control Guide

This guide is designed to help you build a high-power Infrared (IR) blaster for your Raspberry Pi 4. It is optimized for a **4-meter range** and includes a flexible "MacGyver" arm to hit your ceiling AC at a 60-degree angle.

---

## 1. The Shopping List (Malaysia)

These parts are available from Malaysian online electronics suppliers or local hobby shops.

### Core Components
| Item | What to ask for | Est. Price | Why you need it |
| :--- | :--- | :--- | :--- |
| **The Bulb** | **TSAL6200 IR LED** (940nm) | RM 1.50 | This is the "high-beam" of IR LEDs. |
| **The Switch** | **PN2222** or **2N2222** Transistor | RM 0.50 | The Pi's brain is too weak to power the LED; this does the heavy lifting. |
| **The Tiny Board** | **Mini Breadboard** (25 or 170 points) | RM 3.00 | The "head" of your probe where parts are pushed in. |
| **The Brain Guard** | **1k Ohm Resistor** | RM 0.10 | Protects your Raspberry Pi from electrical damage. |
| **The Power Limiter**| **47 Ohm Resistor** | RM 0.10 | Limits the current so you don't burn out the LED. |
| **The Tether** | **Jumper Wires (Female-to-Male)** | RM 4.00 | The "cables" that connect the Pi to the head. |
| **The Arm** | **Pipe Cleaners** or **Craft Wire** | RM 1.00 | Allows you to "aim" the blaster at the ceiling. |

### Where to Buy
* **Online**: Malaysian electronics and maker suppliers.
* **In person**: A local electronics or hobby shop.

---

## 2. The "MacGyver" Arm Assembly

Since you run your Pi 4 "naked," we will use its mounting holes as an anchor.

1.  **Prepare the Arm**: Take a 15cm pipe cleaner (twist two together if they are flimsy).
2.  **Anchor it**: Feed one end through the corner mounting hole of your Pi 4 and twist it tight.
3.  **The Head**: Peel the sticky backing off your **Tiny Breadboard** and press it onto the other end of the pipe cleaner.
4.  **The Cable**: Take 4 Jumper Wires and "spiral wrap" them around the pipe cleaner like a vine on a pole.

---

## 3. Wiring the "Head" (No Soldering)

Hold the **Transistor** so the **FLAT SIDE** is facing you. The three legs are (1) Emitter, (2) Base, (3) Collector.

1.  **The Switch**: Push the Transistor into the breadboard.
2.  **The Ground**: Connect the **Left Leg (Emitter)** to the Pi's **GND (Pin 6)** using a black wire.
3.  **The Signal**:
    *   Connect the **Middle Leg (Base)** to the **1k Ohm Resistor**.
    *   Connect the other end of that resistor to the Pi's **GPIO 25 (Pin 22)** using a yellow wire.
4.  **The Bulb**:
    *   Find the **Long Leg** of the IR LED. Connect it to the **47 Ohm Resistor**.
    *   Connect the other end of that resistor to the Pi's **5V (Pin 2)** using a red wire.
    *   Connect the **Short Leg** of the IR LED to the **Right Leg (Collector)** of the transistor.

---

## 4. How to Aim and Test

1.  **Positioning**: Bend the pipe cleaner arm so the tiny breadboard is pointing directly at the corner panel of your Daikin ceiling cassette.
2.  **The "Phone Camera" Trick**: You cannot see IR light with your eyes, but your **smartphone camera** can.
    *   Open your camera app and look at the IR LED while you trigger a command from the Pi.
    *   You should see a faint purple/white flash through the screen.
3.  **Angle Check**: Since your AC is 4m away, a 1-degree tilt at the base moves the beam by ~7cm at the AC. Use the flexible arm to fine-tune the "shot."

---

## 5. Software Setup (Briefly)
Once hardware is built, you need to tell the Pi which pin you used.
Add this to your `/boot/config.txt`:
`dtoverlay=gpio-ir-tx,gpio_pin=25`
