---
name: macosx-tts-repo
version: 1.0.0
description: macosx_tts
trigger_conditions:
  - 需要理解、修改或排障 macosx_tts 的代码
  - 在 macosx_tts 里定位入口、数据表、对外契约或构建方式
---

# macosx_tts 仓库技能

> 由仓库实际内容生成的骨架（README/目录/模型定义/契约/构建脚本逐项取证）。新增判断与坑位请直接在下面对应小节补充。

## 定位

**macosx_tts**

use pyobjus to call the macosx's tts engine, because the pyttsx3's macosx driver using pyobjc api can not works with plyer togather

- 远端：`https://github.com/yumoqing/macosx_tts.git`
- 默认分支：`main`（共 7 个提交）
- 最近提交：2022-09-03 `8aa40f6` bugfix
- 规模：4 个文件；Python 3

## 目录结构

- `macosx_tts/` — Python 包源码（模块本体）（2 个文件）
- 根文件：`README.md`、`setup.py`

## 代码入口（顶层 Python）

- `setup.py`
- `macosx_tts/version.py`

## 构建与运行

- `setup.py`：`macosx_tts` v?，依赖 0 项
- Python 包 `macosx_tts/`：`__init__.py`、`version.py`

## 建议阅读顺序

1. `README.md`

