# STATUS

副标题：Scalable Discovery Agent 初始状态模板

## Current Focus
- 当前阶段：Bootstrap
- 当前目标：建立 research_ops 基础设施与任务系统
- 当前任务 ID：T000
- 当前工作流：Setup
- 当前运行模式：Initialization

## Current Task
- Title：Initialize `research_ops/` directory and subfolders
- Deliverable：完整目录结构 + 核心元文件 + CSV headers
- Done When：
  - `research_ops/` 目录创建完成
  - 核心子目录创建完成
  - `STATUS.md`、`TODO.md`、`RUN_LOG.md`、`DECISIONS.md`、`SOURCE_POLICY.md`、`SCORING_POLICY.md`、`LICENSE_POLICY.md` 已创建
  - 核心 CSV headers 已初始化
- Blocking Dependencies：无

## Completed In This Run
- 尚无

## Key Findings So Far
- 尚无；当前处于系统初始化阶段

## Current Assets
- 已有说明文档：`SCALABLE_DISCOVERY_AGENT.md`
- 已有任务清单：`SCALABLE_DISCOVERY_AGENT_TODO.md`
- 待创建资产：`research_ops/` 全部目录与核心注册表

## Risks / Blockers
- 需要先定义下载、缓存、manifest、删除策略，避免后续抓取时仓库膨胀
- 需要优先建立来源地图和 query registry，避免进入无序抓取
- 需要优先明确 license / retention policy，避免原始 PDF 长期堆积

## Next Best Task
- Task ID：T001
- Title：Create all core CSV headers
- Why Next：在目录创建后，统一 schema 是后续抓取、解析、链接、审计的基础

## Immediate Follow-ups
- T001 Create all core CSV headers
- T002 Create meta control files
- T005 Create license and retention policy

## Working Rules For This Run
- 只做一个原子任务
- 所有状态写入文件，不依赖聊天上下文
- 每完成一个任务，必须更新 `STATUS.md`、`TODO.md`、`RUN_LOG.md`
- 每完成一个任务，新增 1-3 个具体 follow-up tasks
- 原始下载文件默认进入 cache，解析完成后按 policy 决定是否删除

## Resume Instructions
下次恢复时：
1. 打开 `research_ops/00_meta/STATUS.md`
2. 打开 `research_ops/00_meta/TODO.md`
3. 找到 `DOING` 或最高优先级 `TODO`
4. 检查对应输出文件是否存在
5. 若部分完成则补完，若不一致则先创建 repair task
