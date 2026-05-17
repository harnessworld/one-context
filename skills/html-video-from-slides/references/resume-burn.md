# 成片断点续跑（合并 + 烧字幕）

当 **`node cli.js wav`** 已生成 `production/tmp/part_*.mp4` 与 `tmp/sub_for_burn.ass`，但进程在合并/烧字幕前中断时，**不必**重跑 Playwright 截图，也**不会**重读 `presentation.html`。

## 何时可用

| 条件 | 说明 |
|------|------|
| ✅ | `tmp/part_00.mp4` … 与 `slideDurationsSec` 页数一致 |
| ✅ | `tmp/sub_for_burn.ass` 存在（由上次 `wav` 生成） |
| ❌ 改过 `slides/presentation.html` | 画面已过期 → 删 `tmp/`，全量重跑 `wav` |
| ❌ 改过口播 / SRT / 翻页时长 | 更新 `wav-durations.json` / `sub.srt` 后全量 `wav` |

判断：`slides/presentation.html` 的 **LastWriteTime** 是否 **晚于** `tmp/part_00.mp4`。若是，禁止只续跑烧录。

## 命令

```bash
cd skills/html-video-from-slides
node scripts/finish-burn.js "path/to/production"
```

成片路径读 `timing/wav-durations.json` 的 `outputFile`（默认 `final_auto.mp4`）。日志：`production/build-result.txt`。

## 全量重跑（推荐脚本）

```powershell
skills/html-video-from-slides/scripts/run-wav-build.ps1 -Project "path/to/production"
```

写日志到 `production/video-build.log`；等价于 `npm install`（如需）+ `node cli.js wav --skip-timing-check`。
