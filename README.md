

# `chenmo` —— 可编程元叙事引擎  
> **Deploy, Register, Mix, Inspect, and Reason with Structured Fictional Universes**

`chenmo` 是一个面向**高设定密度虚构世界**（如硬科幻、生态宇宙、文明模拟、赛博朋克）的 Python 领域特定语言（DSL）库。它允许你用**精确的类 Python 语句**操控虚构宇宙的全生命周期：

- **部署**（`d`）与**更新**（`u`）设定包  
- **注册**（`l`）本地创想，支持**嵌套引用已有内核或镜像**  
- **混合**（`x`）多源设定，按权重杂交进化  
- **提取**内核（`c`）、人物（`p`）  
- **创建**镜像（`m`）、转义（`t`）  
- **推演**（`r`）**原生情节发展**（仅限当前作品已声明实体）  
- **查看**（`i`）任意实体元信息  

> **“设定即代码，宇宙可部署，推演可编程，创想可注册。”**

---
>###### PS: 这是一个```虚构的```，但完全可以作为``小说设定``

---

## 🤖 AI增强功能

`chenmo` 现在支持AI增强内容生成，通过API调用AI服务来生成更丰富、更详细的内容。

### AI增强标识

在参数前加上 `AI:` 前缀即可启用AI增强功能：

- `log_works="AI:一个赛博朋克风格的未来都市..."` - AI生成世界设定
- `log_person=["AI:一个黑客，拥有神经接口..."]` - AI生成人物信息
- `log_settings=["AI:这个世界的物理法则..."]` - AI生成设定细节
- `log_thing=["AI:神经接口设备..."]` - AI生成物品/科技描述
- `axioms=["AI:信息即物质..."]` - AI生成公理
- `traits=["AI:技术天赋异禀..."]` - AI生成特质
- `then="AI:AI实体决定帮助黑客..."` - AI生成情节事件

### 配置AI服务

`chenmo` 提供了两种配置AI服务的方式：

#### 方式1：环境变量配置

```bash
export CHENMO_API_KEY="your-api-key-here"
export CHENMO_API_URL="https://api.openai.com/v1/chat/completions"  # 可选，默认值
export CHENMO_MODEL="gpt-3.5-turbo"  # 可选，默认值
```

#### 方式2：首次使用时的交互配置

首次运行 `chenmo` 时，如果未设置环境变量且配置文件不存在，系统会提示您输入API配置信息：

```
欢迎使用 chenmo 可编程元叙事引擎！
首次使用需要配置AI服务信息：
请输入API URL (例如: https://api.openai.com/v1/chat/completions): 
请输入API Key: 
请输入模型名称 (例如: gpt-4, gpt-3.5-turbo): 
配置已保存到 /home/username/.chenmo/config.json
```

配置信息将保存在 `~/.chenmo/config.json` 文件中，后续使用无需重复配置。

### AI增强示例

```python
from chenmo import l, r, i

# 使用AI生成作品和人物
l.cyberpunk.novies(
    log_works="AI:一个赛博朋克风格的未来都市， corporations控制一切，网络黑客是反抗的希望",
    log_person=["AI:一个顶尖的网络黑客，因为一次失败的神经植入手术而身体残疾", "AI:一个前公司特工，现在成为了黑市军火商"]
)

# 使用AI生成内核设定
c.cyberpunk.tech(
    axioms=["AI:神经接口技术使得意识可以上传和下载", "AI:AI监控系统控制着城市的所有摄像头和传感器"],
    constraints=["AI:未经许可的神经植入手术是非法的"]
)

# 使用AI生成人物特质
p.cyberpunk.hacker(
    traits=["AI:擅长网络渗透", "AI:对AI系统有独特的直觉", "AI:身体经过机械改造"],
    constraints=["AI:不能信任任何公司", "AI:必须保护自己的真实身份"]
)

# 在推演中使用AI生成情节事件
r.cyberpunk.hacker(
    when=i.cyberpunk.hacker(target='p').status == "cornered",
    then="AI:黑客利用城市的AI监控系统制造混乱并成功逃脱",
    outcome={
        "hacker.location": "safe_house",
        "corporation.alert_level": "high"
    }
)
```

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

```
~/.chenmo/
├── works/                 # 持久化作品（全局命名空间）
│   └── <作品名>/          # ← 作品名 = 命名空间根（必须全局唯一）
│       ├── manifest.json
│       ├── novies/        # 主叙事内容
│       ├── cores/         # 内核：物理、生态、社会法则
│       ├── personas/      # 人物本体（p）
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

> **“路径即身份” —— 同名作品(但可以使用"_"特指某一个分支)在 `works/` 中仅存一份，覆盖即血缘断裂。**

---

## 🔧 操作详解（完整版）

---

### 1. `d` —— 部署（Deploy）  
从源安装设定包到本地持久空间 `~/.chenmo/works/<toas>/`

```python
d.[源作品名].[源下名](
    from="源路径",           # 可选，默认从官方仓库解析
    to="~/.chenmo/works/",   # 固定基路径，用户不可改
    toas="本地命名"          # 必须唯一，写入 works/<toas>/
)
```

- **作用**：下载 `.narr` 包，解压至 `~/.chenmo/works/<toas>/`，注册到全局命名空间  
- **包格式**：`.narr` = ZIP + `manifest.json`，内部结构必须含 `novies/`, `cores/`, `personas/`, `tech/`
- **命名安全**：若 `toas` 已存在，系统报错 `Namespace collision: <toas> already exists`，拒绝覆盖

**示例**：
```python
d.blade_runner(toas="la_2049")  
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
    then="情节事件ID",           # 预定义或内联事件名（非台词）
    outcome={...}               # 可选：声明状态变更（用于后续 r 或 i）
)
```

#### 关键约束
- 所有 `i(...)` 查询**必须限定在同一作品名下**
- `then` 应描述**情节事件**（如 `"eywa_grants_respiration"`），**非角色台词**
- **不可引用未通过 `l`/`d`/`u` 声明的实体**
- **不可跨作品引用**（如 `r.avatar.spider(when=i.neuromancer.ava...)` 非法）

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
    then="eywa_grants_pandoran_respiration",
    outcome={
        "spider.physiology": "+native_respiration",
        "world_state": "hybrid_acknowledged"
    }
)
```

> 此操作仅依赖 `~/.chenmo/works/avatar/` 内已存在设定，**无需 `x`、`u` 或外部引用**。

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

## 📦 包与协议

- **包格式**：`.narr` = ZIP + `manifest.json`
- **内部结构**：
  ```
  work.narr
  ├── manifest.json
  ├── novies/
  ├── cores/          # 内核：物理、经济、生态法则
  ├── personas/       # 人物本体
  └── tech/           # 科技、装置、载具
  ```
- **manifest.json 必须包含**：
  ```json
  {
    "name": "作品名",
    "version": "1.0",
    "canonical_source": "可选官方源标识"
  }
  ```

---

## 🎯 设计原则（完整版）

1. **`p` 定义存在，`m` 定义可能性**  
2. **`r` 仅推演原生情节，不负责设定引入**  
3. **路径即身份，命名冲突【致命】**  
4. **临时隔离：`temps.` 不污染 `works/` 命名空间**  
5. **创作分层：`l`（声明）→ `u`/`x`（组合）→ `r`（推演）**  
6. **所有引用必须带作品前缀，禁止裸标识符**  
7. **Eywa 必须拼写为 `eywa`，禁用 `eva` 等高冲突变体**

---

## 🌠 适用场景

- 🧠 **赛博朋克角色构建**：身份撕裂、神经植入、公司奴役（基于已注册 `p`/`m`）  
- 🌍 **生态反乌托邦**：资源枯竭、气候难民、新社会契约（基于 `c` 内核）  
- 🚀 **硬科幻文明模拟**：星际政治、AI 伦理、费米悖论  
- 🧬 **原生命运映射**：如“蜘蛛式孤儿”在《阿凡达》宇宙中被 `eywa` 救赎  
- 🤖 **AI 叙事对齐测试**：在强约束下生成一致剧情（`r` 严格遵守 `p`/`c`）

---

## 📜 许可证

MIT License —— 自由用于个人与商业项目。

---

> **“以前，我们写宇宙。  
> 现在，我们部署、注册、混合、查询、合并、并编程推演宇宙。”**

用 `chenmo`，让虚构世界运行于**逻辑、约束与叙事动力学**之中。  
—— **作者：你**  
—— **存储于：`~/.chenmo/works/chenmo_docs/novies`**

