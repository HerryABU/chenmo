"""
测试AI功能是否正确集成
"""

import os
from chenmo.api import APIClient, get_api_client

def test_api_client_creation():
    """测试API客户端创建"""
    print("测试API客户端创建...")
    
    # 测试默认配置
    client = APIClient()
    print(f"  API URL: {client.api_url}")
    print(f"  Model: {client.model}")
    print(f"  Has API Key: {bool(client.api_key)}")
    
    # 测试环境变量配置
    os.environ['CHENMO_API_KEY'] = 'test-key'
    os.environ['CHENMO_API_URL'] = 'https://test-api.com/v1/chat'
    os.environ['CHENMO_MODEL'] = 'gpt-test'
    
    client2 = APIClient()
    print(f"  测试环境变量配置 - API URL: {client2.api_url}")
    print(f"  测试环境变量配置 - Model: {client2.model}")
    
    # 恢复环境变量
    del os.environ['CHENMO_API_KEY']
    del os.environ['CHENMO_API_URL']
    del os.environ['CHENMO_MODEL']
    
    print("  ✓ API客户端创建测试完成\n")

def test_get_api_client():
    """测试获取全局API客户端"""
    print("测试获取全局API客户端...")
    
    client1 = get_api_client()
    client2 = get_api_client()
    
    assert client1 is client2, "全局客户端应该返回同一个实例"
    print("  ✓ 全局API客户端测试完成\n")

def test_mock_generation():
    """测试生成功能（模拟）"""
    print("测试生成功能...")
    
    # 创建一个没有API密钥的客户端来测试错误处理
    client = APIClient(api_key="", api_url="https://invalid-url.com")
    
    # 测试内容生成
    result = client.generate_content("Hello, world!")
    print(f"  内容生成结果: {result}")
    
    # 测试角色生成
    result = client.generate_character("A brave knight")
    print(f"  角色生成结果: {result}")
    
    # 测试世界设定生成
    result = client.generate_world_setting("A cyberpunk city")
    print(f"  世界设定生成结果: {result}")
    
    # 测试情节事件生成
    result = client.generate_plot_event("Context", "Condition")
    print(f"  情节事件生成结果: {result}")
    
    print("  ✓ 生成功能测试完成\n")

def main():
    """主测试函数"""
    print("开始测试AI功能集成...\n")
    
    test_api_client_creation()
    test_get_api_client()
    test_mock_generation()
    
    print("所有测试完成！")

if __name__ == "__main__":
    main()