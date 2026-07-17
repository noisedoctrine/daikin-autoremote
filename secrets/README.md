# Local configuration

`local.yaml` contains private machine, network, and room information and is ignored by Git.

1. Copy `local.example.yaml` to `local.yaml`.
2. Replace the documentation values with local values.
3. Never use `git add -f` on `local.yaml`.

Passwords, login tokens, and API keys should be supplied through environment variables or a credential manager rather than YAML.
