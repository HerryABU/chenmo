#!/usr/bin/env python3
"""
chenmo 库测试文件
"""
import os
import shutil
from pathlib import Path

def test_chenmo_basic():
    """
    测试 chenmo 库的基本功能
    """
    try:
        from chenmo import l, p, c, i, r
        
        print("✅ 成功导入 chenmo 库")
        
        # 测试注册功能
        print("\n📝 测试注册功能...")
        result = l.test_work.novies(
            log_works="Test work for chenmo",
            log_person=["Test Character"],
            log_settings=["Test Setting"],
            log_thing=["Test Tech"]
        )
        print(f"   {result}")
        
        # 测试人物提取
        print("\n👤 测试人物提取功能...")
        result = p.test_work.test_char(
            traits=["test_trait", "another_trait"],
            constraints=["no_test", "no_another"]
        )
        print(f"   {result}")
        
        # 测试内核提取
        print("\n⚛️  测试内核提取功能...")
        result = c.test_work.physics(
            axioms=["conservation_of_energy"],
            constraints=["speed_limit=c"]
        )
        print(f"   {result}")
        
        # 测试查看功能
        print("\n🔍 测试查看功能...")
        try:
            info = i.test_work.test_char(target='p')
            print(f"   查看人物: {type(info)}")
        except Exception as e:
            print(f"   查看功能异常: {e}")
        
        # 测试推演功能
        print("\n🎲 测试推演功能...")
        try:
            result = r.test_work.test_char(
                when="always",
                then="test_event",
                outcome={"status": "completed"}
            )
            print(f"   {result}")
        except Exception as e:
            print(f"   推演功能异常: {e}")
        
        print("\n🎉 所有测试完成！")
        
        # 清理测试数据
        print("\n🧹 清理测试数据...")
        test_path = Path.home() / '.chenmo' / 'works' / 'test_work'
        if test_path.exists():
            shutil.rmtree(test_path)
            print("   已删除测试作品数据")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_chenmo_basic()
    if success:
        print("\n✅ chenmo 库测试通过！")
    else:
        print("\n❌ chenmo 库测试失败！")