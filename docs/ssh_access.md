# SSH Access & Revocation Guide

This document describes how to grant and revoke SSH access without committing private host details.

## Connection details

Store the real SSH user, host, and identity path in the ignored `secrets/local.yaml` file. The commands below use placeholders deliberately.

## 1. Set up access on Windows

Run these commands in PowerShell. Use a strong passphrase when `ssh-keygen` prompts for one.

```powershell
$SshUser = "<SSH_USER>"
$SshHost = "<SSH_HOST>"
$IdentityFile = "$HOME\.ssh\daikin_project"

ssh-keygen -t ed25519 -f $IdentityFile

type "$IdentityFile.pub" | ssh "$SshUser@$SshHost" "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

## 2. Verify access

```powershell
ssh -i $IdentityFile "$SshUser@$SshHost"
```

## 3. Revoke access on the Raspberry Pi

```bash
sed -i "/daikin_project/d" ~/.ssh/authorized_keys
```

To remove the local key files from Windows:

```powershell
Remove-Item "$IdentityFile", "$IdentityFile.pub"
```
