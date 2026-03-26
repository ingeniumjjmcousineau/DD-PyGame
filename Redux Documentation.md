# Diagnostic Doll Redux — Modernization Project 

## Summary
Repair and redesign the diagnostic doll for reliability and improved interaction

---

## To‑Do List
- [ ] Fill out all relevant dimensions
- [ ] Make mechanical drawings of each spot (mounting holes etc...)
    - [ ] Eyes
    - [ ] Mouth
        - [ ] need dimensions of cutout rectangle
    - [ ] Heart
    - [ ] Wrist (hearts touch sensor)
        - [ ] Radius of wrist sensor
    - [ ] Stomach
    - [ ] Leg
        - [ ] need dimensions of cutout quadralateral

- [ ] Model/3d Print each cavity for touch sensor and/or lighting testing
    - [ ] Eyes (LCD)
    - [ ] Mouth (Airvent)
    - [ ] Stomach (Cap Touch, LEDs)
    - [ ] Leg (Cap Touch, LEDs)
    - [ ] Heart (LEDs) (This might not be required as Wrist has the sensor and does not light)
    - [ ] Wrist (Cap touch triggers Heart)

- [ ] Find sound effects
    - [ ] Heartbeat
    - [ ] Scratching
    - [ ] Eye poke?
    - [ ] Stomach gurgle
    - [ ] Breathing

- [ ] Test Cap touch modifications
- [ ] Code Eye game
    - [x] pygame eye poke 
    - [ ] audio effects
    - [ ] GPIO for integrating other sections
    - [ ] effect prioritization
---

# Hardware Sections

Dimensions in mm if not otherwise stated

## 1. Eyes
### Dimensions
#### Insert

- Width: 135
- Height: 201
- Depth: 52
- Radius of opening: 100 

#### Plate

- Width: 149
- Height: 228
- Thickness: 1/4''
- Mounting holes: Use existing as template 
- Screws: 2'' 1/4-20 Pan head

- Notes on placement: This is the LCD Holder get dimensions from waveshare site to model holder, the existing hold might work if the offset for the glass is removed

### Hardware
 
- Microcontroller interfaces: Pi 5 with 7in Waveshare DSI 
- Power requirements: 5v for pi
- PC Fan 80mm 12vdc
### Universal Dimensions

- Total depth (Plastic + Plywood): 63mm
- Pocket depth (milled into plastic): 44mm

### Notes
- Additional considerations:
- Testing notes:

---

## 2. Mouth
### Dimensions
- Note: Irregular shape at one end there is a 45mm x 17mm cutout on each side (see drawing). 
- Opening for mouth is of centre and in a rectangular cutout
- The hose is mounted to the metal plate creating a chamber for the scents, this affects the airflow and should be updated.

#### Insert

- Width: 123
- Height: 111
- Depth: 52
- Radius of opening: 100 

#### Plate

- Width: 146
- Height: 164
- Thickness: 1/4''
- Mounting holes: Use existing as template 
- Screws: 2'' 1/4-20 Pan head



### Hardware
- Actuators/sensors:
- Motor: 25mm Vdc:? Probably 5 but could be 12
- Power/interface notes:

### Notes
- Mechanical constraints:
- Integration notes:

---

## 3. Heart
### 3.1 Heart 
### Dimensions
#### Insert

- Width: 147
- Height: 147
- Depth: 52
- Radius of opening: 100 

#### Plate

- Width: 178
- Height: 184
- Thickness: 1/4''
- Mounting holes: Use existing as template 
- Screws: 2'' 1/4-20 Pan head
- Corner radius: not critical just make it big enough to not interfere (at least 4mm?)


### Hardware
- Sensors/modules: TP223 Modules with added touch surfaces to increase area and sensitivity
- Haptics/LEDs/etc.: Haptic motor driver, small haptic motor
- Controllers:
- Power:

### 3.2 Wrist
### Dimeansions
#### Insert

- Width: 123
- Height: 60
- Depth: 52

#### Plate

- Width: 159
- Height: 63
- Thickness: 1/4''
- Mounting holes: Use existing as template 
- Screws: 2'' 1/4-20 Pan head
- Corner radius: not critical just make it big enough to not interfere (at least 4mm?)


### Notes
- Behavior patterns:
- Safety considerations:

---

## 4. Stomach
### Dimensions
####  Insert
- Width: 235
- Height: 235
- Depth of cavity: 52
- Opening Radius: 188
#### Plate
- Width: 257
- Height: 265
- Thickness: 1/4''
- Mounting holes: 244 x 247
- Screws: 2'' 1/4-20 Pan head

### Hardware
- Sensors/containers:
- Boards/modules:

### Notes
- Interaction details:
- Durability concerns:

---

## 5. Leg
### Dimensions
Irregurlar Quadralateral 90deg angles between length and side a and b
####  Insert
- Width(a): 83
- Width(b): 107
- Height: 314
- Depth of cavity: 52

#### Plate
- Width(a): 125
- Width(b): 98
- Height: 349
- Thickness: 1/4''
- Mounting holes: Use existing as template 
- Screws: 2'' 1/4-20 Pan head
- Corner radius: not critical just make it big enough to not interfere (at least 4mm?)


### Hardware
- Motors/servos:
- Control boards:
- Power:

### Notes
- Weight considerations:
- Movement testing notes: