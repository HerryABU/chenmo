#!/usr/bin/env python3
"""
chenmo 库使用示例
"""

from chenmo import l, p, c, i, r, d, x, m, t


def example_basic_usage():
    """
    基本使用示例
    """
    print("=== chenmo 基本使用示例 ===\n")
    
    # 1. 注册新作品
    print("1. 注册新作品...")
    result = l.neural_frontier.novies(
        log_works="Neural Frontier - A Cyberpunk Universe",
        log_person=["Kai", "Dr. Aris Thorne", "Neural Agent 7"],
        log_settings=["Neural Interface Technology", "Corporate Control"],
        log_thing=["Neural Lace v3.1", "Memory Implants", "Cyberdecks"]
    )
    print(f"   {result}")
    
    # 2. 注册人物特质
    print("\n2. 注册人物特质...")
    result = p.neural_frontier.kai(
        traits=["cyber_jockey", "addicted_to_stimulants", "elite_hacker"],
        constraints=["no_corpo_loyalty", "trusts_only_others_like_him"]
    )
    print(f"   {result}")
    
    # 3. 定义内核法则
    print("\n3. 定义内核法则...")
    result = c.neural_frontier.physics(
        axioms=["conservation_of_energy", "causality_preserved"],
        constraints=["speed_limit=c", "no_closed_timelike_curves"]
    )
    print(f"   {result}")
    
    # 4. 查看实体信息
    print("\n4. 查看实体信息...")
    info = i.neural_frontier.kai(target='p')
    print(f"   Kai persona: {info}")
    
    # 5. 创建镜像人物
    print("\n5. 创建镜像人物...")
    result = m.neural_frontier.kai(
        mp="kai",
        r="after_cyber_psychosis_recovery",
        as_sub="kai_recovered"
    )
    print(f"   {result}")
    
    # 6. 推演情节
    print("\n6. 推演情节...")
    result = r.neural_frontier.kai(
        when="neural_interface_stress > 0.8",
        then="kai_experiences_cyber_psychosis",
        outcome={
            "kai.status": "critical",
            "world_state": "increased_security"
        }
    )
    print(f"   {result}")
    
    print("\n=== 基本示例完成 ===")


def example_advanced_usage():
    """
    高级使用示例
    """
    print("\n=== chenmo 高级使用示例 ===\n")
    
    # 临时作品示例
    print("1. 创建临时作品...")
    result = l.temps.cyber_demo.novies(
        log_works="Cyberpunk Demo World",
        log_person=["Test Agent", "System Administrator"],
        log_thing=["Test Implants"]
    )
    print(f"   {result}")
    
    # 混合示例 (注意：需要先注册源作品)
    print("\n2. 混合操作示例...")
    try:
        # 混合操作需要特殊的调用方式
        result = x.mxd.in(
            sources=[("neural_frontier", "kai"), ("temps.cyber_demo", "test_agent")],
            weights=[0.7, 0.3],
            target_type="p",
            toas="hybrid_agent"
        )
        print(f"   {result}")
    except Exception as e:
        print(f"   混合操作需要先注册更多源作品或格式不正确: {e}")
        # 尝试另一种方式
        try:
            # 直接使用x操作进行混合
            result = x.test_mix.novies(
                sources=[("neural_frontier", "kai"), ("temps.cyber_demo", "test_agent")],
                weights=[0.7, 0.3],
                target_type="p",
                toas="hybrid_agent"
            )
            print(f"   替代方式: {result}")
        except Exception as e2:
            print(f"   替代方式也失败: {e2}")
    
    # 转义示例
    print("\n3. 转义操作示例...")
    try:
        result = t.neural_frontier.novies(
            toas="neural_frontier_alt",
            rcd="neural_frontier_original_with_modifications"
        )
        print(f"   {result}")
    except Exception as e:
        print(f"   转义操作: {e}")
    
    print("\n=== 高级示例完成 ===")


def example_cleanup():
    """
    清理示例数据
    """
    print("\n=== 清理示例数据 ===")
    import shutil
    from pathlib import Path
    
    # 清理示例作品
    works_to_clean = [
        "neural_frontier",
        "hybrid_agent", 
        "neural_frontier_alt"
    ]
    
    base_path = Path.home() / '.chenmo' / 'works'
    
    for work in works_to_clean:
        work_path = base_path / work
        if work_path.exists():
            shutil.rmtree(work_path)
            print(f"   已删除作品: {work}")
    
    # 清理临时作品
    temps_path = Path.home() / '.chenmo' / 'temps' / 'works' / 'cyber_demo'
    if temps_path.exists():
        shutil.rmtree(temps_path)
        print(f"   已删除临时作品: cyber_demo")
    
    print("   清理完成")


if __name__ == "__main__":
    example_basic_usage()
    example_advanced_usage()
    example_cleanup()
    print("\n🎉 所有示例执行完成！")