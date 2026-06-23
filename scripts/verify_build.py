"""验证 CLAUDE.md 转换质量。"""
import zipfile

zf = zipfile.ZipFile("dist/creator.claude.zip")
claude_md = zf.read("CLAUDE.md").decode("utf-8")
evo_md = zf.read("EVOLUTION.md").decode("utf-8")
zf.close()

print("=== CLAUDE.md 转换检查 ===")
checks = [".codex/", ".agents/skills/"]
for pattern in checks:
    lines = [i + 1 for i, l in enumerate(claude_md.splitlines()) if pattern in l]
    if lines:
        print(f"  WARNING: 发现残留 '{pattern}' 在行: {lines}")
    else:
        print(f"  OK: 无 '{pattern}' 残留")

# 检查 AGENTS.md 引用（但排除自引用说明性文本）
lines_with_agents = [
    (i + 1, l.strip())
    for i, l in enumerate(claude_md.splitlines())
    if "AGENTS.md" in l
]
if lines_with_agents:
    print(f"  WARNING: 发现 'AGENTS.md' 残留:")
    for ln, content in lines_with_agents:
        print(f"    行 {ln}: {content}")
else:
    print("  OK: 无 'AGENTS.md' 残留")

expected = ["CLAUDE.md", ".claude/", ".claude/skills/"]
for pattern in expected:
    count = claude_md.count(pattern)
    print(f"  OK: '{pattern}' 出现 {count} 次")

print("\n=== EVOLUTION.md 转换检查 ===")
for pattern in [".codex/", "AGENTS.md"]:
    lines = [i + 1 for i, l in enumerate(evo_md.splitlines()) if pattern in l]
    if lines:
        print(f"  WARNING: 发现残留 '{pattern}' 在行: {lines}")
    else:
        print(f"  OK: 无 '{pattern}' 残留")

print("\n=== commands 检查 ===")
zf = zipfile.ZipFile("dist/creator.claude.zip")
cmd_files = [n for n in zf.namelist() if n.startswith(".claude/commands/")]
print(f"  共 {len(cmd_files)} 个 command 文件:")
for cf in sorted(cmd_files):
    content = zf.read(cf).decode("utf-8")
    has_dollar_skill = "$" in content.split("---")[-1].split("$ARGUMENTS")[0]
    status = "WARNING: 含 $skill 语法" if has_dollar_skill else "OK"
    print(f"    {cf.split('/')[-1]}: {status}")
zf.close()

print("\nDone.")
