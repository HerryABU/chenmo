#!/usr/bin/env python3
"""
测试 chenmo 库的基本功能
"""
from chenmo import d, l, i, c, p, m, t, r, x, s, llm, print, frm, inport
import json


def test_basic_operations():
    print("=== 测试 chenmo 库基本功能 ===\n")
    
    # 1. 测试注册操作 (l) - 创建新作品
    print("1. 注册新作品 'neural_frontier'...")
    result = l.neural_frontier.novies(
        log_works="Neural Frontier - A cyberpunk universe",
        log_person=["Kai", "Dr. Aris Thorne"],
        log_thing=["Neural Interface v3.0", "Quantum Encryption Device"]
    )
    print(f"   结果: {result}\n")
    
    # 2. 测试内核提取 (c) - 定义底层法则
    print("2. 提取内核 'cyber_laws'...")
    result = c.neural_frontier.cyber_laws(
        axioms=["privacy_is_sacred", "ai_rights_are_limited", "neural_data_is_owned"],
        constraints=["no_mind_control", "consent_required_for_neural_links"]
    )
    print(f"   结果: {result}\n")
    
    # 3. 测试人物提取 (p) - 定义人物本体
    print("3. 提取人物 'kai_persona'...")
    result = p.neural_frontier.kai_persona(
        traits=["cyber_jockey", "rebel_hacker", "trauma_survivor"],
        constraints=["no_corporate_loyalty", "protects_others_at_cost"]
    )
    print(f"   结果: {result}\n")
    
    # 4. 测试镜像 (m) - 创建命运变体
    print("4. 创建镜像 'kai_redeemed'...")
    result = m.neural_frontier.kai_mirror(
        mp="kai_persona",
        r="found_redemption_through_helping_others",
        as_sub="kai_redeemed"
    )
    print(f"   结果: {result}\n")
    
    # 5. 测试查看 (i) - 查看实体信息
    print("5. 查看神经前沿的内核...")
    result = i.neural_frontier.cyber_laws(target='c')
    print(f"   内核信息: {json.dumps(result, indent=2, ensure_ascii=False)}\n")
    
    # 6. 测试搜索 (s) - 搜索实体
    print("6. 搜索包含 'kai' 的实体...")
    results = s("kai")  # Search for 'kai' in all works
    for item in results:
        print(f"   发现: {item['work']}.{item['name']} (类型: {item['type']})")
    print()
    
    # 7. 测试 LLM 生成 (narrative 模式)
    print("7. 使用 LLM 生成叙事文本...")
    try:
        # 创建一个简单的LLM实例用于测试
        llm_gen = llm(type="openai", model="gpt-3.5-turbo", mode="narrative")
        # 注意：在实际环境中，这需要有效的API密钥
        # 我们跳过实际的LLM调用以避免API错误
        print("   LLM 接口已初始化 (跳过实际API调用)")
    except Exception as e:
        print(f"   LLM 初始化失败 (预期): {e}")
    
    # 8. 测试部署 (d) - 部署官方包
    print("\n8. 部署官方包 'blade_runner_demo'...")
    try:
        result = d.blade_runner_demo.novies(
            doad="blade_runner_2049_base",
            toas="la_2049"
        )
        print(f"   结果: {result}")
    except Exception as e:
        print(f"   预期的错误 (因为没有真实的官方仓库): {e}")
    
    # 9. 测试转义 (t) - 派生新作品
    print("\n9. 转义操作演示...")
    try:
        # 先创建一个基础作品用于转义
        l.demo_base.novies(log_works="Demo base work")
        result = t.demo_base.novies(
            toas="demo_derived",
            rcd="derived_from_demo_base"
        )
        print(f"   结果: {result}")
    except Exception as e:
        print(f"   转义操作: {e}")
    
    # 10. 测试混合 (x) - 混合多源设定
    print("\n10. 混合操作演示...")
    try:
        # 需要先有一些源作品
        l.source_one.novies(log_works="First source")
        l.source_two.novies(log_works="Second source")
        
        result = x.mixed_result.in_(
            sources=[("source_one", "novies"), ("source_two", "novies")],
            weights=[0.6, 0.4],
            target_type="c",
            toas="blended_universe"
        )
        print(f"   结果: {result}")
    except Exception as e:
        print(f"   混合操作: {e}")
    
    print("\n=== 测试完成 ===")


def test_cli_commands():
    print("\n=== 测试 CLI 命令 ===")
    import subprocess
    import sys
    
    # 测试列出所有作品
    try:
        result = subprocess.run([sys.executable, '-c', 'from chenmo.utils import list_all_works; print(list_all_works())'], 
                              capture_output=True, text=True, cwd='/workspace')
        print(f"CLI 列出作品: {result.stdout.strip()}")
    except Exception as e:
        print(f"CLI 测试出错: {e}")


if __name__ == "__main__":
    test_basic_operations()
    test_cli_commands()