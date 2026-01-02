"""
演示 chenmo - 可编程元叙事引擎 的使用
"""

from chenmo import *

def demo_basic_operations():
    """演示基本操作"""
    print("=== 演示基本操作 ===")
    
    # 创建新作品（持久）
    print("\n1. 注册新作品 neural_frontier:")
    l.neural_frontier.novies(
        log_works="Neural Frontier",
        log_person=["Kai", "Dr. Aris Thorne"]
    )
    
    # 为 Kai 定义特质
    print("\n2. 为 Kai 定义人物特质:")
    p.neural_frontier.kai(
        traits=["cyber_jockey", "addicted_to_stimulants"],
        constraints=["no_corpo_loyalty"]
    )
    
    # 临时实验：赛博格侦探（隔离）
    print("\n3. 创建临时作品 cyber_noir:")
    l.temps_cyber_noir.novies(
        log_person=["Detective Voss"],
        log_thing=["Neural Lace v3.1"]
    )
    
    # 查看已创建的实体
    print("\n4. 查看 Kai 的人物信息:")
    i.neural_frontier.kai(target='p')
    
    print("\n5. 查看 Cyber Noir 侦探信息:")
    i.temps_cyber_noir.voss(target='p')

def demo_core_operations():
    """演示内核操作"""
    print("\n\n=== 演示内核操作 ===")
    
    # 首先创建 Dune 作品
    print("\n1. 创建 Dune 作品:")
    l.dune.novies(
        log_works="Dune universe with spice economy"
    )
    
    # 定义 Dune 的香料经济内核
    print("\n2. 定义 Dune 香料经济内核:")
    c.dune.spice_economy(
        axioms=["water_is_gold", "spice_enables_navigation"],
        constraints=["no_atomic_weapons"]
    )
    
    # 首先创建 Neuromancer 作品
    print("\n3. 创建 Neuromancer 作品:")
    l.neuromancer.novies(
        log_works="Neuromancer cyberpunk universe"
    )
    
    # 定义 Neuromancer 的人物内核
    print("\n4. 定义 Case 的人物特质:")
    p.neuromancer.case(
        traits=["cyber_jockey", "addicted_to_stimulants"],
        constraints=["no_corpo_loyalty"]
    )
    
    # 查看内核和人物
    print("\n5. 查看香料经济内核:")
    i.dune.spice_economy(target='c')
    
    print("\n6. 查看 Case 人物信息:")
    i.neuromancer.case(target='p')

def demo_advanced_operations():
    """演示高级操作"""
    print("\n\n=== 演示高级操作 ===")
    
    # 混合两个作品的人物
    print("\n1. 混合 Neuromancer 的 Case 和 Blade Runner 的 Deckard:")
    mix_op = x.mxd
    mix_in_op = mix_op.in_()
    mix_in_op(
        sources=[("neuromancer", "case"), ("blade_runner", "deckard")],
        weights=[0.7, 0.3],
        target_type="p",
        toas="cyber_investigator"
    )
    
    # 创建镜像：Paul 的弗雷曼人版本
    print("\n2. 创建 Paul 的镜像（弗雷曼人版本）:")
    # 首先需要创建 Paul
    p.dune.paul(
        traits=["duke's_heir", "bene_gesserit_conditioned"],
        constraints=["honor_bound"]
    )
    
    m.dune.paul(
        mp="paul",
        r="raised_by_fremen_after_bene_gesserit_failure",
        as_sub="paul_fremen"
    )
    
    # 转义：创建新的作品
    print("\n3. 转义 Blade Runner 作品:")
    # 首先需要有一个源作品
    l.blade_runner.novies(
        log_works="Blade Runner 2049",
        log_person=["Deckard", "Rachael"]
    )
    
    t.blade_runner.novies(
        toas="la_2099",
        rcd="br_2049_official"
    )
    
    print("\n4. 检查混合结果:")
    i.cyber_investigator.novies(target='p')

def demo_story_reasoning():
    """演示故事推演"""
    print("\n\n=== 演示故事推演 ===")
    
    # 注册 Avatar 中的角色
    print("\n1. 注册 Avatar 中的角色:")
    l.avatar.spider(
        log_person="Human orphan born on Pandora; lungs incompatible with Terran air"
    )
    l.avatar.eywa(
        log_person="Pandoran planetary consciousness",
        log_settings=["responds_to_extinction_threat"]
    )
    
    # 定义 Eywa 的特质
    p.avatar.eywa(
        traits=["planetary_consciousness", "life_preserver"],
        constraints=["protect_natural_balance"]
    )
    
    # 推演情节：Eywa 救助人类孤儿
    print("\n2. 推演情节：Eywa 救助人类孤儿:")
    r.avatar.spider(
        when=("spider.o2_level < 0.1 and eywa.attentive == True"),
        then="eywa_grants_pandoran_respiration",
        outcome={
            "spider.physiology": "+native_respiration",
            "world_state": "hybrid_acknowledged"
        }
    )
    
    # 查看推演结果
    print("\n3. 查看推演日志:")
    try:
        import json
        from pathlib import Path
        log_path = Path.home() / '.chenmo' / 'works' / 'avatar' / 'novies' / 'narrative_log.json'
        if log_path.exists():
            with open(log_path, 'r', encoding='utf-8') as f:
                log = json.load(f)
            print(f"Narrative log: {log}")
    except Exception as e:
        print(f"Could not read narrative log: {e}")

def main():
    """主函数，运行所有演示"""
    print("🚀 开始演示 chenmo - 可编程元叙事引擎")
    print("设定即代码，宇宙可部署，推演可编程，创想可注册。")
    
    try:
        demo_basic_operations()
        demo_core_operations()
        demo_advanced_operations()
        demo_story_reasoning()
        
        print("\n\n✅ 演示完成！")
        print("\n总结：")
        print("- d: 部署作品")
        print("- l: 注册新实体")
        print("- c: 定义内核/法则")
        print("- p: 定义人物")
        print("- x: 混合多个源")
        print("- m: 创建镜像/变体")
        print("- t: 转义/派生作品")
        print("- r: 推演情节")
        print("- i: 查看实体")
        
    except Exception as e:
        print(f"\n❌ 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()