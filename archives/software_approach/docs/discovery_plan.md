# AC Discovery Plan

The addresses below use the documentation-only `192.0.2.0/24` range. Store real discovery targets in the ignored `secrets/local.yaml` file.

## 1. Targeted IP probing

- **Example focus**: `192.0.2.50`, `192.0.2.57`, `192.0.2.59`.
- **Action**: Scan only devices and ports you own or are authorized to test.

## 2. Advanced UDP discovery

- **Ports**: 30050, 30000, 5353 (mDNS).
- **Payloads**:
  - `DAIKIN_UDP/common/basic_info`
  - `{"method":"discover"}`
  - Empty payload.

## 3. Network fingerprinting

- **MAC OUI analysis**: Confirm which device is the AC based on vendor information.
- **Hostnames**: Check for `daikin*`, `espressif*`, or `brp*` via local name resolution.

## 4. Manual verification

Cross-reference device identifiers in the router's device list. Do not commit real MAC addresses, hostnames, or room labels.
