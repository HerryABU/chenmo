"""
chenmo AI增强功能示例
展示如何使用AI生成内容来增强虚构世界构建
"""

import os
from chenmo import l, i, r, c, p

def setup_api_credentials():
    """
    设置API凭据（示例）
    """
    # 注意：在实际使用时，请将这些值设置为环境变量
    # export CHENMO_API_KEY="your-api-key"
    # export CHENMO_API_URL="https://api.openai.com/v1/chat/completions"
    # export CHENMO_MODEL="gpt-4"
    
    # 这里仅为示例，实际部署时应使用环境变量
    if not os.getenv('CHENMO_API_KEY'):
        print("警告: 未设置CHENMO_API_KEY环境变量，AI功能将不可用")
        print("请设置环境变量或在代码中配置API凭据")
        return False
    return True

def demo_ai_enhanced_creation():
    """
    演示AI增强创建功能
    """
    print("=== AI增强虚构世界创建演示 ===\n")
    
    # 1. 使用AI创建一个科幻世界
    print("1. 使用AI创建科幻世界...")
    result = l.scifi_universe.novies(
        log_works="AI:一个赛博朋克风格的未来都市，AI与人类共存但关系紧张",
        log_person=[
            "AI:一个黑客，拥有神经接口，专门破解企业防火墙",
            "AI:一个AI实体，获得了自我意识，试图理解人类情感"
        ],
        log_settings=[
            "AI:这个世界的物理法则，允许量子计算直接改写现实",
            "AI:社会结构，企业控制一切，个人几乎没有隐私"
        ],
        log_thing=[
            "AI:神经接口设备，可以直接连接大脑和网络",
            "AI:量子处理器，能够进行超光速计算"
        ]
    )
    print(f"   {result}\n")
    
    # 2. 使用AI定义核心法则
    print("2. 使用AI定义世界核心法则...")
    result = c.scifi_universe.physics(
        axioms=[
            "AI:信息即物质，数据可以直接影响物理现实"
        ],
        constraints=[
            "AI:每个实体都有计算限制，超过限制会导致系统崩溃"
        ]
    )
    print(f"   {result}\n")
    
    # 3. 使用AI定义人物特质
    print("3. 使用AI定义人物特质...")
    result = p.scifi_universe.hacker(
        traits=[
            "AI:技术天赋异禀，但社交能力欠缺",
            "AI:对权威持怀疑态度，追求信息自由"
        ],
        constraints=[
            "AI:无法在没有网络的环境中生存",
            "AI:过度依赖技术，身体能力较弱"
        ]
    )
    print(f"   {result}\n")
    
    # 4. 查看创建的内容
    print("4. 查看创建的世界设定...")
    try:
        world_info = i.scifi_universe.novies(target='novies')
        print(f"   世界信息: {world_info}\n")
    except Exception as e:
        print(f"   查看失败: {e}\n")
    
    # 5. 使用AI推演情节
    print("5. 使用AI推演情节发展...")
    result = r.scifi_universe.hacker(
        when="hacker尝试破解企业防火墙时被发现",
        then="AI:AI实体决定帮助黑客逃脱追踪",
        outcome={
            "hacker_status": "暂时安全",
            "ai_hackerman_connection": "建立联系"
        }
    )
    print(f"   {result}\n")

def demo_manual_creation():
    """
    演示手动创建功能（非AI增强）
    """
    print("=== 手动创建演示（非AI增强） ===\n")
    
    # 创建一个传统奇幻世界
    print("1. 手动创建奇幻世界...")
    result = l.fantasy_realm.novies(
        log_works="一个魔法与剑的世界，龙族与人类共存",
        log_person=[
            "精灵法师艾瑞斯",
            "人类骑士加拉哈德"
        ],
        log_settings=[
            "魔法是生命能量的体现",
            "龙族拥有古老的智慧"
        ],
        log_thing=[
            "魔法水晶",
            "龙鳞护甲"
        ]
    )
    print(f"   {result}\n")

def main():
    """
    主函数
    """
    print("chenmo - 可编程元叙事引擎")
    print("AI增强功能演示\n")
    
    # 检查API配置
    if setup_api_credentials():
        print("API配置成功，开始AI增强演示...\n")
        demo_ai_enhanced_creation()
    else:
        print("跳过AI增强演示，开始手动创建演示...\n")
    
    demo_manual_creation()
    
    print("演示完成！")

if __name__ == "__main__":
    main()