# XeThru serial protocol firmware version: {{ book.version }}

This document describes the serial protocol used by the XeThru module. Firmware version: {{ book.version }}

## Notation
The following notation is used in this document:

````
<X> = Single byte
[X] = Multiple bytes
[“abc”] = [0x61,0x62,0x63] = Ascii text
[X(i)] = 32 bit Integer, 4 bytes
[X(f)] = 32 bit Float, 4 bytes
````

## Protocol format

Binary protocol using flag bytes and escaping.

Example: `<Start> + [Data] + <CRC> + <End>`

|  Flag     | bytes |
|-----------|-------|
| `<Start>` | 0x7D  |
| `<End>`   | 0x7E  |
| `<Esc>`   | 0x7F  |

### Data escaping
Escaping means that if the escape byte occurs in data, the next byte is not `<Start>`, `<End>` or `<Esc>`, but intended byte with same value as flags.

Example: `0x7D + 0x10 + 0x7F + 0x7E + 0x04 + 0xFF + 0x7E`

Here the byte 0x7E in the middle is intended, and should not be read as a <Start> flag. Therefore, there is added a <Esc> byte. After parsing for escape bytes, the data becomes:

`0x7D + 0x10 + 0x7E + 0x04 + 0xFF + 0x7E`

### Checksum
Calculated by XOR’ing all bytes, including `<Start>`.
Note that the CRC is done after escape bytes is removed. This means that CRC is also calculated before adding escape bytes.

## How it works

When powering up the sensor, it enters an idle mode. In this mode, the user can choose sensor behaviour by loading the desired sensor application. After loading the application, the user can configure the application by sending application level commands. Finally, after configuring the application, the user can send a command to start the application.

`Module reset --> Idle mode --> Load application --> Load parameters --> Run application`

If you want to change sensor behaviour, rest the module and start again. Once the application is running, it is not possible to change parameters or application without performing a reset first.



## Module level

Commands that control the module at a top level.

### Load application

Loads the desired sensor application.

Example: `<Start> + <XTS_SPC_MOD_LOADAPP> + [AppID] + <CRC> + <End>`

Response: `<Start> + <XTS_SPR_ACK> + <CRC> + <End>`

Protocol codes:

| Name | Value |
|------|-------|
| XTS_SPC_MOD_LOADAPP | 0x21 |
| XTS_SPR_ACK | 0x10 |

### Execute application

After the application is loaded, it can be configured using 'Application level' commands (see below). Then the application is executed by setting the module mode.

| Name | Value | Description |
|------|-------|-------------|
| XTS_SM_NORMAL | 0x10 | Normal sensor operating mode |
| XTS_SM_IDLE | 0x11 | Idle mode. Sensor ready but not active. |

Example: `<Start> + <XTS_SPC_MOD_SETMODE> + <XTS_SM_IDLE> + <CRC> + <End>`

Response: `<Start> + <XTS_SPR_ACK> + <CRC> + <End>`

Protocol codes:

| Name | Value |
|------|-------|
| XTS_SPC_MOD_SETMODE | 0x20 |
| XTS_SPR_ACK | 0x10 |


### Reset module

Use this command to completely reset the sensor module.

Example: `<Start> + <XTS_SPC_MOD_RESET> + <CRC> + <End>`

Response: `<Start> + <XTS_SPR_SYSTEM> + [XTS_SPRS_BOOTING(i)] + <CRC> + <End>`

Protocol codes:

| Name | Value |
|------|-------|
| XTS_SPC_MOD_RESET | 0x22 |
| XTS_SPR_SYSTEM | 0x30 |
| XTS_SPRS_BOOTING | 0x10 |


### LED control

Use this command to choose the behaviour of the sensor LED.
There are three levels of LED operations, Off, Simple and Full. Different applications may use the LED differently, but in general the three levels will behave like this:
- Off: Very simple LED indicator during startup and initialization. LED is always off in operating mode.
- Simple: More indication during startup and initialization. Simple indication during operation, e.g. fixed indication or subtle blinking.
- Full: Full indication during startup and initialization. Extensive use of blinking and colors to indicate sensor state and if possible values.

Example: `<Start> + <XTS_SPC_MOD_SETLEDCONTROL> + <Mode> + <Reserved> + <CRC> + <End>`

Response: `<Start> + <XTS_SPR_ACK> + <CRC> + <End>`

Protocol codes:

| Mode | Value |
|------|-------|
| XT_UI_LED_MODE_OFF | 0 |
| XT_UI_LED_MODE_SIMPLE | 1 |
| XT_UI_LED_MODE_FULL | 2 |

| Name | Value |
|------|-------|
| XTS_SPC_MOD_SETLEDCONTROL | 0x24 |
| XTS_SPR_ACK | 0x10 |


## Application level

### Generic application commands

#### Set Detection Zone

Set the desired detection zone.

Example: `<Start> + <XTS_SPC_APPCOMMAND> + <XTS_SPCA_SET> + [XTS_ID_DETECTION_ZONE] + [Start(f)] + [End(f)] + <CRC> + <End>`

Response: `<Start> + <XTS_SPR_ACK> + <CRC> + <End>`


Protocol codes:

| Name | Value |
|------|-------|
| XTS_SPC_APPCOMMAND | 0x10 |
| XTS_SPCA_SET | XTS_SPCA_SET |
| XTS_ID_DETECTION_ZONE | 0x96a10a1c |
| XTS_SPR_ACK | XTS_SPR_ACK |

### Respiration application (RESP)
#### RESP Sensor status

Outputs the status of the RESP application, with data when available.

Example: `<Start> + <XTS_SPR_APPDATA> + [XTS_ID_RESP_STATUS] + [Counter(i)] + <StateCode> + [StateData(i)] + [Distance(f)] + [Movement(f)] + [SignalQuality(i)] + <CRC> + <End>`

StateCode values:

| StateCode | Value | Description | StateData |
|------|-------|-------------|-------------|
| XTS_VAL_RESP_STATE_BREATHING | 0 | Valid RPM sensing | Current RPM value |
| XTS_VAL_RESP_STATE_MOVEMENT | 1 | Detects motion, but can not identify breath | 0 |
| XTS_VAL_RESP_STATE_MOVEMENT_TRACKING | 2 | Detects motion, possible breathing soon | 0 |
| XTS_VAL_RESP_STATE_NO_MOVEMENT | 3 | No movement detected | 0 |
| XTS_VAL_RESP_STATE_INITIALIZING | 4 | No movement detected | 0 |
| XTS_VAL_RESP_STATE_ERROR | 5 | Sensor has detected some problem. StatusValue indicates problem. | 0 |
| XTS_VAL_RESP_STATE_UNKNOWN | 6 | Undefined state. | 0 |

Output:
- StateData: RPM, respirations per minute (Breathing state only).
- Distance: Distance to where respiration is detected (Breathing state only).
- Movement: Relative movement of the respiration, in mm (Breathing state only).
- SignalQuality: A measure of the signal quality giving respiration. Typically used to identify if the sensor is positioned correctly (Breathing state only).

Protocol codes:

| Name | Value |
|------|-------|
| XTS_ID_APP_RESP | 0x1423a2d6 |
| XTS_SPR_APPDATA | 0x50 |
| XTS_ID_RESP_STATUS | 0x2375fe26 |

### Presence application (PRES)
#### PRES Sensor status

Outputs the status of the PRES application, with data when available.

Example: `<Start> + <XTS_SPR_APPDATA> + [XTS_ID_PRESENCE_STATUS] + <Presence> + [Reserved(f)] + [Reserved(f)]  + [SignalQuality(i)] + <CRC> + <End>`

Output:
- Presence: Indicating presence or no presence.
- SignalQuality: A measure of the signal quality giving presence. Typically used to identify if the sensor is positioned correctly.

Protocol codes:

| Name | Value |
|------|-------|
| XTS_ID_APP_PRESENCE | 0x00288912 |
| XTS_SPR_APPDATA | 0x50 |
| XTS_ID_PRESENCE_STATUS | 0x991a52be |



