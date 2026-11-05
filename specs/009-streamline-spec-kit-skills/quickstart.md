# Quickstart: Verifying Streamlined Spec Kit Skills

## Verification Steps

### 1. Parity Check
Verify that `.agents/` and `.claude/` remain identical:
```bash
diff -r .agents/skills .claude/skills
```
Expected output: No output (exit code 0).

### 2. Manifest Verification
Check that manifests match actual disk state:
```bash
python3 -c "
import json, hashlib, pathlib

manifest = json.loads(pathlib.Path('.specify/integrations/agy.manifest.json').read_text())
for entry in manifest.get('files', []):
    p = pathlib.Path(entry['path'])
    if p.exists():
        data = p.read_bytes()
        sha = hashlib.sha256(data).hexdigest()
        assert sha == entry['sha256'], f'Hash mismatch on {p}'
        assert len(data) == entry['size_bytes'], f'Size mismatch on {p}'
print('All manifest entries valid!')
"
```

### 3. Clean Execution Test
Test running an orchestrator check or bootstrap check:
```bash
bash -n bootstrap-speckit.sh
```
