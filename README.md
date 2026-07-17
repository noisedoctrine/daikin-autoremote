# daikin-autoremote

A small local smart remote for a Daikin air conditioner.

This is a pet project for experimenting with infrared control, simple schedules, and temperature-based automation. The initial goal is to make one known Daikin setup work reliably rather than build a general-purpose home automation platform.

## Goals

- Send a verified set of Daikin infrared commands.
- Control power, mode, target temperature, and fan settings.
- Save a few named profiles such as `sleep`, `cool-room`, and `away`.
- Run simple time-based schedules.
- Work locally without depending on a cloud service.
- Keep personal device configuration and network details out of the repository.

## Non-goals

For the first version, this project will not try to support every Daikin model, other air-conditioner brands, voice assistants, cloud dashboards, mobile applications, or complex deployment pipelines.

## Planned approach

1. Capture commands from the original remote and identify the protocol variant.
2. Reproduce one command reliably using an infrared transmitter.
3. Represent the intended AC state in code and encode it into verified IR frames.
4. Add a small command-line interface for manual control.
5. Add named profiles and simple scheduling.
6. Add a minimal local web interface only if it is useful in practice.

The application will track the last state it requested. Unless receive hardware or another feedback mechanism is added, that state should not be treated as confirmation that the air conditioner received the command.

## Hardware

The expected setup is a small Linux device such as a Raspberry Pi connected to an infrared LED through an appropriate driver circuit. Exact hardware, GPIO pins, and wiring will be documented after the first reliable prototype.

Do not drive a high-power infrared LED directly from a GPIO pin. Use suitable current limiting and a transistor or driver circuit.

## Configuration

Local configuration, profiles, host details, and other personal data should live under:

```text
secrets/
```

That directory is intended to be excluded from Git. Public examples should use neutral placeholders.

## Initial success criteria

The first useful version should:

- support one documented Daikin remote or protocol variant;
- reliably send power, mode, temperature, and fan commands;
- include test vectors based on captured remote commands;
- run core logic without physical hardware through a mock transmitter;
- save and apply named profiles;
- run simple local schedules; and
- require no external cloud service.

## Status

Planning and hardware validation.
