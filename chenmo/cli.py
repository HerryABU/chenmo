"""
命令行接口模块
提供CLI访问功能
"""
import argparse
import sys
import json
from . import d, u, l, x, f, c, p, m, t, r, i, s, llm, print, frm, inport
from .utils import list_all_works, clean_temp_files


def main():
    parser = argparse.ArgumentParser(description='可编程元叙事引擎 - chenmo')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 添加各种子命令
    # deploy command
    deploy_parser = subparsers.add_parser('deploy', aliases=['d'], help='部署作品')
    deploy_parser.add_argument('work_name', help='作品名称')
    deploy_parser.add_argument('--from', dest='from_path', help='源路径')
    deploy_parser.add_argument('--doad', help='官方包标识符')
    deploy_parser.add_argument('--toas', help='本地命名')
    
    # update command
    update_parser = subparsers.add_parser('update', aliases=['u'], help='更新作品')
    update_parser.add_argument('work_name', help='作品名称')
    update_parser.add_argument('--from', dest='from_path', help='源路径')
    update_parser.add_argument('--lo', help='本地起源')
    update_parser.add_argument('--toas', help='新作品名')
    update_parser.add_argument('--merge', choices=['overlay', 'patch', 'strict'], default='overlay', help='合并策略')
    
    # register command
    register_parser = subparsers.add_parser('register', aliases=['l'], help='注册新作品')
    register_parser.add_argument('work_name', help='作品名称')
    register_parser.add_argument('--log-works', help='作品描述')
    register_parser.add_argument('--log-person', nargs='*', help='人物描述')
    register_parser.add_argument('--log-settings', nargs='*', help='设定描述')
    register_parser.add_argument('--log-thing', nargs='*', help='物品/科技描述')
    
    # search command
    search_parser = subparsers.add_parser('search', aliases=['s'], help='搜索作品或实体')
    search_parser.add_argument('keyword', help='搜索关键词')
    search_parser.add_argument('--work', help='限制搜索范围到特定作品')
    search_parser.add_argument('--type', choices=['p', 'c', 't', 'm', 'all'], help='实体类型')
    
    # llm command
    llm_parser = subparsers.add_parser('llm', help='LLM生成接口')
    llm_parser.add_argument('--type', choices=['openai', 'ollama', 'custom'], default='openai', help='LLM类型')
    llm_parser.add_argument('--model', default='gpt-4o', help='模型名称')
    llm_parser.add_argument('--mode', choices=['narrative', 'world'], default='narrative', help='生成模式')
    llm_parser.add_argument('prompt', nargs='?', help='提示词')
    
    # frm/inport command
    frm_parser = subparsers.add_parser('frm', help='快速引用接口')
    frm_parser.add_argument('identifier', help='作品标识符')
    frm_parser.add_argument('action', choices=['inport'], help='动作')
    frm_parser.add_argument('entity', help='实体名称')
    frm_parser.add_argument('--as', dest='alias', help='别名')
    
    # list command
    list_parser = subparsers.add_parser('list', help='列出所有作品')
    
    # clean command
    clean_parser = subparsers.add_parser('clean', help='清理临时文件')
    
    # print command
    print_parser = subparsers.add_parser('print', help='输出内容')
    print_parser.add_argument('content', nargs='?', help='内容')
    print_parser.add_argument('--to', help='输出到文件')
    print_parser.add_argument('--format', choices=['narrative', 'world'], default='narrative', help='格式')
    print_parser.add_argument('--merge', choices=['strict', 'overlay', 'patch'], default='strict', help='合并策略')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command in ['deploy', 'd']:
        result = d(args.work_name, from_path=getattr(args, 'from_path', None), 
                   doad=args.doad, toas=args.toas)
        print(result)
        
    elif args.command in ['update', 'u']:
        result = u(args.work_name, from_path=getattr(args, 'from_path', None),
                   lo=args.lo, toas=args.toas, merge=args.merge)
        print(result)
        
    elif args.command in ['register', 'l']:
        result = l(args.work_name, 
                   log_works=args.log_works,
                   log_person=args.log_person or [],
                   log_settings=args.log_settings or [],
                   log_thing=args.log_thing or [])
        print(result)
        
    elif args.command in ['search', 's']:
        result = s(args.keyword, work_filter=args.work)
        for item in result:
            print(f"Work: {item['work']}, Name: {item['name']}, Type: {item['type']}")
        
    elif args.command == 'llm':
        if not args.prompt:
            print("错误: 需要提供提示词")
            return
            
        llm_instance = llm(type=args.type, model=args.model, mode=args.mode)
        generated = llm_instance.generate(args.prompt)
        print(generated)
        
    elif args.command == 'frm':
        if args.action == 'inport':
            frm_result = frm(args.identifier)
            import_result = inport(args.entity, as_alias=args.alias)
            print(import_result)
        
    elif args.command == 'list':
        works = list_all_works()
        print("所有作品:")
        for work_type, work_name in works:
            print(f"  [{work_type}] {work_name}")
    
    elif args.command == 'clean':
        clean_temp_files()
        print("临时文件已清理")
    
    elif args.command == 'print':
        if not args.content:
            print("错误: 需要提供内容")
            return
            
        print(args.content, to=args.to, format=args.format, merge=args.merge)


if __name__ == '__main__':
    main()