
# `chenmo` —— 可编程元叙事引擎  V2.5+  
> **Deploy, Register, Mix, Inspect, Reason, Import, Search, Generate, Update, and Output Structured Fictional Universes**

`chenmo` 是一个面向**高设定密度虚构世界**（如硬科幻、生态宇宙、文明模拟、赛博朋克）的 Python 领域特定语言（DSL）库。它允许你用**精确的类 Python 语句**操控虚构宇宙的全生命周期：

- **部署**（`d`）与**更新**（`u`）设定包  
- **注册**（`l`）本地创想，支持**嵌套引用已有内核或镜像**  
- **混合**（`x`）多源设定，按权重杂交进化  
- **提取**内核（`c`）、人物（`p`）  
- **创建**镜像（`m`）、转义（`t`）  
- **推演**（`r`）**原生情节发展**（仅限当前作品已声明实体）  
- **查看**（`i`）任意实体元信息  
- **搜索**（`s` / `cm.search`）官方与本地作品及实体  
- **快速引用**（`cm.frm` / `cm.inport`）用于叙事构建阶段  
- **LLM 辅助生成**（`cm.llm`）支持**叙事文本**与**结构化世界构建**  
- **智能输出与更新**（`cm.print`）区分小说段落与宇宙定义，并支持安全合并  

> **“设定即代码，宇宙可部署，推演可编程，创想可注册，思想需显式授权，生成需结构对齐，输出需格式分离，更新需策略可控。”**

---

> ###### PS: 这最初是一个**虚构设定**，用于元叙事小说内部设定，但现在 **`chenmo` 原型已真实存在**！  
> 你可通过 `pip install chenmo` 安装基础版本，但什么也做不了。  
> 目前仅支持（`l`, `i`, ）的部分功能，且没有文件写入，可同时作为**创作工具（目前不可行）**与**小说元素**。
> 
>  ***warning***  **仅概念产品**

---

## 📜 完整语句语法规范（全覆盖）

所有语句遵循统一结构：  
**`[操作头].[作品名].[下名](参数...)`**

### 路径补全规则
- 若省略 `[下名]`，自动补全为 **`novies`**（保留下名，代表主叙事本体）  
  例：`d.neuromancer` → `d.neuromancer.novies`  
- **`novies` 语义**：指代作品的**小说/电影主干**，**几乎不可能被用作角色名**，避免命名冲突。
- **路径前缀语义**：
  - 以 `temps.` 开头的路径（如 `temps.cyber_demo`）为**临时作品**  
    → 数据写入 `~/.chenmo/temps/works/`，**会话有效，需手动清理**
  - 其他路径为**持久作品**  
    → 数据写入 `~/.chenmo/works/`，**自动注册到全局命名空间**

---

## 💾 存储与命名空间（核心规范）

`chenmo` 的所有数据持久化严格遵循以下文件系统布局：

```text
~/.chenmo/
├── works/                 # 持久化作品（全局命名空间）
│   └── <作品名>/          # ← 作品名 = 命名空间根（必须全局唯一）
│       ├── manifest.json
│       ├── novies/        # 主叙事内容
│       ├── cores/         # 内核：物理、生态、社会法则（含 mindcore）
│       ├── personas/      # 人物本体（p）与认知模型（*_mindcore.json）
│       └── tech/          # 科技、装置、载具
│
└── temps/                 # 临时会话空间（完全隔离）
    └── works/
        └── <作品名>/      # ← 临时作品名可重复，但限于 temps/ 域内
            ├── manifest.json
            └── ...（同上）
```

### 命名原则（【致命】级别）
> **命名冲突 = 宇宙污染 = 推演崩溃**

- ✅ **必须使用源作品官方标识符**  
  例：《阿凡达》中的星球意识应命名为 `eywa`，**禁止使用 `eva`、`ava`、`lilith` 等高冲突词**（因与《EVA》《Ex Machina》等 IP 冲突）
- ✅ **原创实体需具备上下文区分度**  
  例：`dr_leno`、`bio_net_core_7`，避免 `helper`、`god`、`ai`、`neo` 等通用词
- ✅ **所有引用必须带作品前缀**  
  例：`i.avatar.eywa(...)` 正确；`i.eywa(...)` 非法（未指定命名空间）
- ❌ **禁止无作品名的裸操作**  
  `l.spider(...)` 将被拒绝或强制重定向至 `temps.anon`

> **“路径即身份” —— 同名作品在 `works/` 中仅存一份，覆盖即血缘断裂。**

---

## 🔧 操作详解（完整版）

---

### 1. `d` —— 部署（Deploy）  
从源安装设定包到本地持久空间 `~/.chenmo/works/<toas>/`

```python
d.[源作品名].[源下名](
    from="源路径",           # 可选，默认从官方仓库解析
    doad="官方包标识符",     # ← 新增：替代 from，从官方仓库下载
    to="~/.chenmo/works/",   # 固定基路径，用户不可改
    toas="本地命名"          # 必须唯一，写入 works/<toas>/
)
```

- **作用**：下载 `.narr` 包，解压至 `~/.chenmo/works/<toas>/`，注册到全局命名空间  
- **包格式**：`.narr` = ZIP + `manifest.json`，内部结构必须含 `novies/`, `cores/`, `personas/`, `tech/`
- **命名安全**：若 `toas` 已存在，系统报错 `Namespace collision: <toas> already exists`，拒绝覆盖

**示例**：
```python
d.blade_runner(doad="blade_runner_2049_base", toas="la_2049")  
# → 部署至 ~/.chenmo/works/la_2049/

d.dune.spice_economy(from="git://dune-core", toas="arrakis_econ")  
# → 部署至 ~/.chenmo/works/arrakis_econ/
```

---

### 2. `u` —— 更新（Update）  
在已有持久作品上增量合并变更，**目标路径必须存在于 `~/.chenmo/works/`**

#### 模式 A：原地更新（无 `lo`）
```python
u.[本地作品名].[本地下名](
    from="源路径",           # 必须
    to="~/.chenmo/works/[本地作品名]",  # 固定，不可改
    merge="策略"             # overlay | patch | strict | interactive
)
```

#### 模式 B：分支合并（有 `lo`）
```python
u.[本地作品名].[本地下名](
    from="源路径",           # 必须
    lo="~/.chenmo/works/[本地作品名]",  # 必须：Local Origin
    to="~/.chenmo/works/[新作品名]",    # 必须
    toas="[新作品名]",       # 可选，默认 = 新作品名
    merge="策略"
)
```

- **语义**：`merge="overlay"` 覆盖冲突字段；`"strict"` 遇冲突即失败
- **命名安全**：`toas` 若已存在，报错并中止

**示例**：
```python
u.la_2049.novies(
    from="threebody/dark_forest",
    lo="~/.chenmo/works/la_2049",
    to="~/.chenmo/works/blade_runner_df",
    toas="br_df",
    merge="overlay"
)
```

---

### 🔥 3. `l` —— 注册（Log / Register）

**从零声明新作品、人物、设定或物品**，适用于**本地创作起点**。

```python
l.[作品名].[下名](
    log_works="作品描述",                     # 仅当下名=novies 时有效
    log_person=["人物描述", ...],            # 注册至 personas/
    log_settings=["设定描述", ...],          # 注册至 cores/ 或 novies/
    log_thing=["物品/科技描述", ...]         # 注册至 tech/
)
```

#### ✅ 高级能力：**嵌套引用结构化设定**
支持内联引用**同一作品内**已有内核或镜像：
```python
log_settings= i.[作品名].[下名](target='c')   # 引用内核
log_settings= i.[作品名].[下名](target='m')   # 引用镜像（推荐用于命运映射）
```

- **语义**：注册时**内联拷贝结构**，非运行时查询
- **存储路径**：
  - 若 `[作品名]` 以 `temps.` 开头 → 写入 `~/.chenmo/temps/works/<作品名>/`
  - 否则 → 写入 `~/.chenmo/works/<作品名>/`
- **命名安全**：若持久作品名已存在，报错 `Namespace exists`

**完整示例**（安全命名）：
```python
# 创建新作品（持久）
l.neural_frontier.novies(
    log_works="Neural Frontier",
    log_person=["Kai", "Dr. Aris Thorne"]
)
# → 写入 ~/.chenmo/works/neural_frontier/

# 为 Kai 赋予“蜘蛛式”命运结构（身份撕裂）
l.neural_frontier.kai(
    log_settings= i.neural_frontier.spider_archetype(target='m')
)
# → 写入 ~/.chenmo/works/neural_frontier/personas/kai.json

# 临时实验：赛博格侦探（隔离）
l.temps.cyber_noir.novies(
    log_person=["Detective Voss"],
    log_thing=["Neural Lace v3.1"]
)
# → 写入 ~/.chenmo/temps/works/cyber_noir/
```

---

### 🔥 4. `x` —— 混合（Mix）

**按权重融合多源设定**，生成新实体，**必须先通过 `d`/`l` 声明所有源**

```python
x.mxd.in(
    sources=[("作品1", "下名1"), ("作品2", "下名2")],  # 所有源必须已存在
    weights=[0.6, 0.4],
    target_type="c" | "p" | "t",  # c=内核, p=人物, t=科技
    toas="新实体名"
)
```

- **存储路径**：结果写入 `~/.chenmo/works/<toas>/`（持久）
- **命名安全**：`toas` 必须唯一
- **注意**：`x` 用于**设定构建**，**不用于情节推演**；`r` 不可直接调用 `x` 结果，除非先 `l` 或 `d` 注册

**示例**：
```python
x.mxd.in(
    sources=[("neuromancer", "case"), ("blade_runner", "deckard")],
    weights=[0.7, 0.3],
    target_type="p",
    toas="cyber_investigator"
)
# → 生成 ~/.chenmo/works/cyber_investigator/personas/novies.json
```

---

### 5. `f` —— 实例化（Fabricate）  
动态生成作品实例（通常由 `d` 自动调用，用户极少直接使用）

```python
f.[作品名].[下名](setting="描述字符串")
```

- **作用**：根据描述生成最小 viable 作品结构，写入 `~/.chenmo/works/[作品名]/`
- **命名安全**：若作品名已存在，报错

**示例**：
```python
f.solaris.novies(setting="Ocean planet with sentient plasma")
# → 创建 ~/.chenmo/works/solaris/ 基础结构
```

---

### 6. `c` —— 内核提取（Core）  
定义或提取底层法则，写入 `cores/`

```python
c.[作品名].[下名](
    axioms=["公理1", "公理2"],        # 不可违反的基本法则
    constraints=["约束1", "约束2"]    # 可配置的边界条件
)
```

- **存储路径**：`~/.chenmo/works/[作品名]/cores/[下名].json`
- **命名安全**：同一作品内下名必须唯一

**示例**：
```python
c.dune.spice_economy(
    axioms=["water_is_gold", "spice_enables_navigation"],
    constraints=["no_atomic_weapons"]
)
```

---

### 7. `p` —— 人物提取（Persona）  
定义人物本体身份，写入 `personas/`

```python
p.[作品名].[下名](
    traits=["特质1", "特质2"],
    constraints=["不可为行为1", "不可为行为2"]
)
```

- **存储路径**：`~/.chenmo/works/[作品名]/personas/[下名].json`
- **语义**：`p` 定义“他是谁”，是 `r` 推演的不可变基础

**示例**：
```python
p.neuromancer.case(
    traits=["cyber_jockey", "addicted_to_stimulants"],
    constraints=["no_corpo_loyalty"]
)
```

---

### 8. `m` —— 镜像（Mirror）  
创建命运变体，写入 `personas/` 作为子实体

```python
m.[作品名].[下名](
    mp="源人物名",                          # 必须存在
    r="命运变更描述",                       # 如 "raised_by_fremen"
    as_sub="新镜像名"                      # 如 "paul_fremen"
)
```

- **存储路径**：`~/.chenmo/works/[作品名]/personas/[as_sub].json`
- **语义**：`p` 说“他是谁”，`m` 说“他可能成为谁”

**示例**：
```python
m.dune.paul(
    mp="paul",
    r="raised_by_fremen_after_bene_gesserit_failure",
    as_sub="paul_fremen"
)
```

---

### 9. `t` —— 转义（Transmute）  
派生新作品，保留血缘，写入新持久路径

```python
t.[源作品名].[源下名](
    toas="新作品名",
    rcd="血缘描述"  # 如 "br_2049_official"
)
```

- **作用**：复制整个作品结构到 `~/.chenmo/works/<toas>/`，添加血缘元数据
- **命名安全**：`toas` 必须唯一

**示例**：
```python
t.blade_runner.novies(toas="la_2099", rcd="br_2049_official")
```

---

### ✅ 10. `r` —— 推演（Run）← **仅用于原生情节发展**

> **`r` 不引入新设定，不跨宇宙操作，仅在当前作品已注册实体上推导情节事件。**  
> **所有情节必须基于 `~/.chenmo/works/[作品名]/` 或 `temps/` 中已存在数据。**

#### 语法规则
```python
r.[作品名].[下名](
    when=<条件表达式>,          # 基于 i.[作品名]... 查询结果
    then="情节事件ID",           # 预定义或内联事件名（支持中文等自然语言）
    outcome={...}               # 可选：声明状态变更（用于后续 r 或 i）
)
```

#### 关键约束
- 所有 `i(...)` 查询**必须限定在同一作品名下**
- `then` 应描述**情节事件**（如 `"eywa_grants_respiration"` 或 `"Eywa 赋予 Spider 潘多拉呼吸能力"`）
- **不可引用未通过 `l`/`d`/`u` 声明的实体**
- **不可跨作品引用**

#### ✅ 正确示例（原生、无交叉、命名安全）
```python
# 前提：avatar.spider 与 avatar.eywa 已通过 l 注册
l.avatar.spider(
    log_person="Human orphan born on Pandora; lungs incompatible with Terran air"
)
l.avatar.eywa(
    log_person="Pandoran planetary consciousness",
    log_settings=["responds_to_extinction_threat"]
)

# 推演：Eywa 介入（使用官方名 eywa，非 eva）
r.avatar.spider(
    when=(
        i.avatar.spider(target='p').o2_level < 0.1 and
        i.avatar.eywa(target='p').attentive == True
    ),
    then="Eywa 赋予 Spider 潘多拉呼吸能力",  # ← 支持中文
    outcome={
        "spider.physiology": "+native_respiration",
        "world_state": "hybrid_acknowledged"
    }
)
```

---

### 11. `i` —— 查看（Inspect）  

```python
i.[作品名].[下名](target='c' | 'p' | 'm')
```

- **作用**：返回指定实体的结构化元数据
- **存储查询路径**：
  - `target='c'` → 读取 `~/.chenmo/.../cores/[下名].json`
  - `target='p'` → 读取 `~/.chenmo/.../personas/[下名].json`
  - `target='m'` → 读取镜像 persona（通常为 persona 子类）
- **在 `l` 嵌套中**，`i... (target='m')` 用于**引用命运结构**
- **必须带作品名前缀**，否则报错 `Missing namespace`

**示例**：
```python
i.dune.paul(target='c')      # 查看内核
i.avatar.eywa(target='p')    # 查看 Eywa 本体（使用官方名）
```

---

### 🔍 12. `s` —— 搜索（Search）

#### DSL 形式
```python
s.what.what("关键词")  # 第二个 what = 作品名 或 "none"；第三个 what = 实体类型
```

#### CLI 形式
```bash
cm.search "关键词"               # ≡ cm.s.none("关键词")
cm.s <作品名> <类型> "关键词"    # 类型: p, c, t, m, all
```

- **约束**：
  - `s.none.p("x")` 非法（实体搜索必须指定作品）
  - 返回结构化结果，可用于脚本

**示例**：
```bash
cm.search "cyber"                # 搜作品名
cm.s avatar t "respiration"      # 搜《阿凡达》中的科技
```

---

### 🚀 13. `frm` / `inport` —— 叙事级快速引用

> **仅用于故事创作阶段，不持久化，会话有效**

#### CLI 单行链式写法（推荐）
```bash
cm.frm <作品标识符> inport <实体名>[:mindcore] [as <别名>]
cm.frm . inport <官方作品名>
```

#### CLI 管道风格写法（视觉分隔，等效）
```bash
cm.frm <作品标识符> | cm.inport <实体名>[:mindcore] [as <别名>]
cm.frm . | cm.inport <官方作品名>
```

> **注意**：`|` 是 `chenmo` CLI 内部连接符，**非系统管道**，仅作视觉分隔。

#### DSL 用法（脚本/Jupyter）
```python
from chenmo import frm, inport
frm("dmkj"); inport("PASIV")                  # 仅物品
frm("dmkj"); inport("inception:mindcore")     # 思想内核
frm("."); inport("Avatar")                    # 全量导入
```

#### 语义说明
| 写法 | 导入内容 | 是否含 mindcore |
|------|--------|----------------|
| `inport X` | `tech/X` 或 `personas/X` | ❌ |
| `inport X:mindcore` | `cores/X_mindcore` 或 `personas/X_mindcore` | ✅ |
| `frm . + inport Work` | 全量（novies, cores, personas, tech） | ✅ |

#### 安全机制
- 所有导入实体存于**会话内存符号表**，不写磁盘
- 自动拉取未安装的官方包至 `temps.auto_doad/`
- 命名冲突时强制要求 `as` 别名

**完整示例**：
```bash
# 导入《盗梦空间》PASIV 装置（仅物品）
cm.frm dmkj inport PASIV
# 或
cm.frm dmkj | cm.inport PASIV

# 导入其梦境法则（思想内核）
cm.frm dmkj inport inception:mindcore

# 全量导入《阿凡达》宇宙
cm.frm . inport Avatar
# 或
cm.frm . | cm.inport Avatar

# 带别名
cm.frm blade_runner_2049_base inport deckard as hunter
```

---

### 14. `cm.llm(...)` —— **LLM 生成接口（支持双模式）**

```python
cm.llm(
    type="openai" | "ollama" | "custom",   # 必须
    model="gpt-4o" | "llama3.1:8b",        # 必须
    apiurl=None,                           # 可选（默认按 type 推断）
    apikey=None,                           # 可选（优先读环境变量）
    mode="narrative" | "world"             # ← 默认 "narrative"
)
```

#### 行为
- 返回临时生成器对象，支持 `.generate(prompt)`
- **不持久化**，**不注册**，**不产生命名空间**
- 根据 `mode` 决定输出类型与上下文注入策略

#### 模式说明
| `mode` | 用途 | 输出格式 | 上下文注入 |
|--------|------|----------|-----------|
| `"narrative"` | 小说/场景生成 | 自然语言字符串 | 当前脚本涉及的实体定义 + `r` 规则（含中文） |
| `"world"` | 宇宙/实体构建 | 严格 JSON（符合 `chenmo` 规范） | 生成协议约束 + 命名安全规则 |

#### LLM 生成的宇宙结构规范（`mode="world"`）
```json
{
  "type": "work" | "persona" | "core" | "tech",
  "name": "实体名",
  "metadata": {
    "description": "自然语言描述（非注释，是正式键值）",
    "source_prompt": "用户原始提示",
    "generated_by": "模型名"
  },
  "data": {
    // 结构化字段
  }
}
```

#### 示例
```python
# 小说生成
gen1 = cm.llm(type="ollama", model="llama3.1", mode="narrative")
scene = gen1.generate("描写 Spider 获得潘多拉呼吸能力的瞬间")

# 世界构建
gen2 = cm.llm(type="ollama", model="llama3.1", mode="world")
world_json = gen2.generate("创建一个木星轨道上的AI修道院世界观")
```

---

### 15. `cm.print(...)` —— **智能输出与更新接口**

```python
cm.print(content, to=None, format="narrative", merge="strict")
```

| 参数 | 说明 |
|------|------|
| `content` | 字符串（`format="narrative"`）或 JSON 字符串（`format="world"`） |
| `to` | `None` → 控制台<br>`"file.txt"` → 小说输出<br>`"~/.chenmo/works/..."` → 世界构建输出 |
| `format` | `"narrative"`（默认）：输出自然语言<br>`"world"`：解析 JSON 并写入结构化文件 |
| `merge` | 仅 `format="world"` 时有效：<br>`"strict"`（默认）：存在则报错<br>`"overlay"`：覆盖冲突字段<br>`"patch"`：仅更新指定字段 |

#### 行为细则
- **`format="narrative"`**  
  - 忽略 `merge` 参数  
  - 直接写入文件或 stdout

- **`format="world"`**  
  - 解析 `content` 为 JSON  
  - 根据 `type` 和 `name` 自动路由到正确路径  
  - 若目标文件存在：
    - `merge="strict"` → 报错 `File exists`
    - `merge="overlay"` → 覆盖整个 `data` 和 `metadata`
    - `merge="patch"` → 递归合并 `data` 和 `metadata` 字段
  - 执行命名与类型安全检查

#### 示例
```python
# 小说输出
cm.print(scene, to="avatar_ch3.txt")

# 初始化新世界
cm.print(world_json, to="~/.chenmo/works/", format="world")

# 安全更新现有角色
cm.print(updated_leader, 
         to="~/.chenmo/works/mars_colony/", 
         format="world", 
         merge="patch")
```

#### CLI 等效
```bash
# 小说
echo "prompt" | cm.llm --mode narrative | cm.print --to scene.txt

# 初始化
echo "..." | cm.llm --mode world | cm.print --to ~/.chenmo/works/ --format world

# 更新
echo "..." | cm.llm --mode world | cm.print --to ~/.chenmo/works/mars/ --format world --merge patch
```

---

## 📦 包与协议

- **包格式**：`.narr` = ZIP + `manifest.json`
- **内部结构**：
  ```text
  work.narr
  ├── manifest.json
  ├── novies/
  ├── cores/          # 内核：物理、经济、生态法则（含 mindcore.json）
  ├── personas/       # 人物本体 + 认知模型（*_mindcore.json）
  └── tech/           # 科技、装置、载具
  ```
- **manifest.json 必须包含**：
  ```json
  {
    "name": "作品名",
    "version": "1.0",
    "canonical_source": "官方ID"
  }
  ```
- **官方包标识符**：小写、无空格（如 `blade_runner_2049_base`）

---

## 🎯 设计原则（V2.5+ 完整版）

1. **`p` 定义存在，`m` 定义可能性**  
2. **`r` 仅推演原生情节，不负责设定引入**  
3. **路径即身份，命名冲突【致命】**  
4. **临时隔离：`temps.` 不污染 `works/` 命名空间**  
5. **创作分层：`l`（声明）→ `u`/`x`（组合）→ `r`（推演）**  
6. **所有引用必须带作品前缀，禁止裸标识符**  
7. **Eywa 必须拼写为 `eywa`，禁用 `eva` 等高冲突变体**  
8. **`doad` 优先于路径：官方包通过语义标识符引用**  
9. **搜索必须显式命名空间：禁止跨宇宙实体模糊匹配**  
10. **CLI 与 DSL 语义对齐**  
11. **`frm`/`inport` 是叙事快捷方式，非构建原语**  
12. **会话即沙盒：所有导入默认隔离**  
13. **智能依赖拉取：自动后台 `doad` 未安装包**  
14. **思想需显式授权：`mindcore` 必须通过 `:mindcore` 显式请求**  
15. **全量导入即全责：`frm . + inport Work` 包含 mindcore**  
16. **实体与思想分离存储：避免字段冲突**  
17. **CLI 链式语法优先：支持空格或 `|` 分隔的单行写法**  
18. **一行一意图：单行仅支持单实体导入，确保清晰与可预测性**  
19. **LLM 是外部工具，不属于任何宇宙**  
20. **`cm.print()` 是唯一输出接口，确保生成内容可追踪、可落地**  
21. **LLM 生成分双模：`narrative`（小说）与 `world`（结构化宇宙）**  
22. **`world` 模式输出必须含 `metadata.description`（自然语言作为元数据）**  
23. **`cm.print(format="world")` 自动路由到正确存储路径**  
24. **生成即合规：LLM 在约束下输出，而非自由幻想**  
25. **世界文件更新需策略可控：`merge="strict|overlay|patch"`**

---

## 🌠 适用场景

- 🧠 **快速原型宇宙**：`cm.llm(mode="world").generate("...")` → `cm.print(format="world")`  
- 📖 **AI 辅助写作**：`cm.llm(mode="narrative")` 生成场景 → `cm.print(to="draft.txt")`  
- 🔄 **安全迭代设定**：`cm.print(..., merge="patch")` 更新人物或内核  
- 🌍 **生态反乌托邦**：`d.doad("climate_collapse_core")` + LLM 扩展人物  
- 🚀 **硬科幻文明模拟**：`x` 混合 Fermi Paradox 与 AI 伦理内核，再用 LLM 生成社会描述  
- 🧬 **原生命运映射**：`r` 推演 `spider` 被 `eywa` 救赎，LLM 生成电影级场景  
- 🤖 **AI 叙事对齐测试**：在 `mindcore` 约束下生成一致剧情  
- 🎭 **同人创作沙盒**：跨宇宙组合 + LLM 生成融合故事  
- 📦 **自动化打包**：LLM 生成完整 `.narr` 结构，一键部署

---

## 📜 许可证

MIT License —— 自由用于个人与商业项目。

---

> **“以前，我们写宇宙。  
> 现在，我们部署、注册、混合、查询、合并、导入思想，并编程推演宇宙。  
> 而 LLM，只是我们手中的笔——它不创造宇宙，只帮我们写下已决定的命运，或勾勒出合规的新世界蓝图，并安全地更新它。”**

用 `chenmo`，让虚构世界运行于**逻辑、约束、叙事动力学、显式授权的思想，结构对齐的生成，以及策略可控的演化**之中。  
—— **作者：你**  
—— **存储于：`~/.chenmo/works/chenmo_docs/novies`**
