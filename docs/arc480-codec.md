# Daikin remote encoder — current repository hypothesis (unverified)

> NOT an ARC480 wire-protocol specification. This documents the unverified encoder
> constants currently in this repo. Do not treat the byte layout, timings, fields,
> or worked outputs below as ARC480 facts, and do not base new encoder code,
> captures, or tests on them until a real-remote capture identifies the exact variant.

Target: Malaysian 2025 models, `ARC480 (Stateful)` per `docs/plan.md:21` and `ARC480 or similar` per `docs/research.md:15`.
Status: encode-only hypothesis, not validated against a real remote capture (`README.md:22`).
Known conflict: public ARC480A5/A14 evidence points at DAIKIN152-style framing (152 bits / 19 bytes single transmission, ~3492/1718 header, ~433 mark, ~1529 one-space, ~25182 gap, translated fan/swing values), which materially differs from the two-frame `11 + 19` layout below. Capture is required before any ARC480 claim. Sources: `src/ir_Daikin.h` maps `ARC480A5 remote (DAIKIN152)` and cites `DaikinHeatpumpARC480A14IR` ([ir_Daikin.h](https://github.com/crankyoldgit/IRremoteESP8266/blob/master/src/ir_Daikin.h)), DAIKIN152 send path is `sendDaikin152` ([ir_Daikin.cpp](https://github.com/crankyoldgit/IRremoteESP8266/blob/master/src/ir_Daikin.cpp)), protocol list entry ([SupportedProtocols.md](https://github.com/crankyoldgit/IRremoteESP8266/blob/master/SupportedProtocols.md)).

## 1. Packet layout (repo hypothesis, unverified)

The current repo encoder emits 30 bytes as 2 frames, each with its own header and checksum. Full state is sent every transmission. This shape is an implementation assumption, not a verified ARC480 wire fact.

| Frame | Len | Content |
|---|---|---|
| F1 preamble | 11 (`src/daikin_arc480.h:26`) | `11 DA 27 00 C5 00 00 00 19 00 CK` |
| F2 state | 19 (`src/daikin_arc480.h:27`) | `11 DA 27 00 42 [5] [6] 00 [8] 00*9 CK` |

Templates: `pkg/daikin/arc480.go:35,39-44`, `src/daikin_arc480.c:14-26`.

F2 byte map:

| Offset | Field |
|---|---|
| `[0:3]` | Magic `11 DA 27 00` |
| `[4]` | Frame ID `0x42` |
| `[5]` | Mode (bits 4-6) \| Power (bit 0) |
| `[6]` | Temp `<< 1` (i.e. `Temp * 2`) |
| `[7]` | Reserved `0x00` |
| `[8]` | Fan (bits 4-7) \| Swing (bits 0-3) |
| `[9:17]` | Reserved `0x00` |
| `[18]` | Checksum |

Packing: `pkg/daikin/arc480.go:47,50,53`, `src/daikin_arc480.c:30,34,38`.

## 2. Field encodings assumed by the repo (unverified)

As coded in `pkg/daikin/arc480.go:17-23`, `src/daikin_arc480.h:16-22` (repo assumption, not verified Daikin wire values — e.g. fan/swing are passed through directly rather than translated to Daikin wire constants):

| Field | Encoding |
|---|---|
| Power | `0: OFF`, `1: ON` (F2[5] bit 0) |
| Mode | `0: AUTO`, `3: COOL`, `2: DRY`, `4: HEAT`, `6: FAN` (F2[5] bits 4-6) |
| Temp | `16-32`, stored as `Temp << 1` (F2[6]; e.g. 24 -> `0x30`) |
| Fan | `0: AUTO`, `1-5: Level`, `10: QUIET` (F2[8] bits 4-7) |
| Swing | `0: OFF`, `1: ON` (F2[8] bits 0-3, masked `0x0F`) |

No range validation is implemented; `EncodeState` never returns an error despite its signature.

## 3. Checksum used by the repo encoder

8-bit additive sum over all bytes except the last, stored in the last byte of each frame:

```go
// pkg/daikin/arc480.go:25-31; identical src/daikin_arc480.c:4-10
sum(data[0:len-1]) & 0xFF
```

Applied at `pkg/daikin/arc480.go:36,55` and `src/daikin_arc480.c:18,41`. No separate verify/decode routine exists.

## 4. IR timings assumed by the repo (unverified)

Timings agree across the repo's Go/C/Python copies, but are still unverified against a capture: `pkg/daikin/arc480.go:8-15`, `src/daikin_arc480.h:8-14`, `src/ir_engine.py:12-18`.

| Param | Value (us unless noted) |
|---|---|
| `PULSE` (bit mark, stop) | 430 |
| `ZERO_GAP` | 430 |
| `ONE_GAP` | 1290 |
| `HEADER_PULSE` / `HEADER_GAP` | 3440 / 1720 |
| `GAP_BETWEEN_FRAMES` | 35000 (F1 -> F2 only) |
| `CARRIER_HZ` | 38000 (declared in C/Python; absent in Go) |

Pulse-distance, LSB-first `(byte >> i) & 1` (`src/ir_engine.py:37-44`, `src/main.c:9-23`).
Frame envelope is `[HEADER_PULSE, HEADER_GAP] + bytes + [PULSE]` (`src/ir_engine.py:46-52`, `src/main.c:25-41`).
Single shot, no repeat code. Carrier handling is unresolved: both C and Python send the envelope via `gpioWave*`/`wave_add_generic` and note 38 kHz modulation as TODO (`src/ir_engine.py:62-83`).

## 5. Implementations in this repo

* Go `pkg/daikin/arc480.go:33-58` is the reference transcription of this repo hypothesis (not a verified ARC480 implementation); `main.go:71` calls `EncodeState`, but `sendFrames` at `main.go:91-104` is a `Printf` stub. `POST /control` defaults to `Power=1, Temp=24, Mode=3` (`main.go:56-60`) and has no Fan/Swing fields. Note: the package currently does not build — `pkg/daikin/arc480.go:3-5` imports `fmt` without use, so `go test ./pkg/daikin` and `go vet ./pkg/daikin` fail (pre-existing).
* C `src/daikin_arc480.c:12-42` mirrors Go exactly; `src/main.c:25-54` has the only complete wave TX, and `src/main.c:56-81` is a `<power> <temp> <mode>` CLI with Fan/Swing hardcoded to 0.
* Python `src/ir_engine.py:25-60` has correct wave timing but `DaikinState.get_frames()` at `src/ir_engine.py:104-116` is a stub: F1 tail hardcoded to `0x20` (correct checksum is `0xF0`, see below) and F2 payload all zeros. `src/main.py:36-61` wires it to `POST /units/{id}/control`.

## 6. Worked outputs of the current repo encoder (not ARC480 vectors)

These recompute the repo algorithm only; they do not prove ARC480 wire behavior. F1 is constant (sum `0x11+0xDA+0x27+0xC5+0x19 = 496`, `& FF = F0`):

```text
11 DA 27 00 C5 00 00 00 19 00 F0
```

Repo-encoder F2 (header `11 DA 27 00 42`, then `[5] [6] 00 [8]`, then `00*9`, then checksum):

```text
COOL 24C ON AUTO/OFF  ([5]=0x31 [6]=0x30 [8]=0x00): 11 DA 27 00 42 31 30 00 00 00 00 00 00 00 00 00 00 00 B5
COOL 24C OFF AUTO/OFF ([5]=0x30 [6]=0x30 [8]=0x00): 11 DA 27 00 42 30 30 00 00 00 00 00 00 00 00 00 00 00 B4
HEAT 26C ON Fan3/SwingON ([5]=0x41 [6]=0x34 [8]=0x31): 11 DA 27 00 42 41 34 00 31 00 00 00 00 00 00 00 00 00 FA
```

## 7. Gaps and validation needed

* No decode/receive path, no captures, no `*test*` files; directly blocks `README.md:51-53` success criteria (test vectors from captured commands, mock transmitter).
* Unvalidated variant: per `README.md:22`, capture the original remote and identify the exact variant before promoting any of the above to an ARC480 claim or basing encoder code/tests on it.
* Go package does not build: unused `fmt` import at `pkg/daikin/arc480.go:3-5` fails `go test`/`go vet` (pre-existing, this PR adds docs only).
* F2 bytes 7 and 9-17 are always zero; timer/powerful/econo/comfort bits unmapped.
* GPIO default conflict: code/config use 17 (`src/main.c:7`, `main.go:16`, `docker-compose.yml`, `.env.example`) vs build guide wiring to GPIO 25.
