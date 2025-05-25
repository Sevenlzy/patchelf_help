import os
import glob
import subprocess

# 配置基础路径
LIBS_BASE = "/home/alen/alen/tools/glibc-all-in-one/libs"

def select_version():
    # 获取所有版本目录
    versions = [d for d in os.listdir(LIBS_BASE) 
                if os.path.isdir(os.path.join(LIBS_BASE, d))]
    versions.sort()
    
    if not versions:
        print("未找到任何glibc版本！")
        exit(1)
        
    # 显示版本列表
    print("\n可用glibc版本：")
    for i, ver in enumerate(versions, 1):
        print(f"{i}. {ver}")
    
    # 获取用户选择
    while True:
        try:
            choice = int(input("\n请输入版本序号："))
            if 1 <= choice <= len(versions):
                return os.path.join(LIBS_BASE, versions[choice-1])
            print("序号无效，请重新输入！")
        except ValueError:
            print("请输入有效数字！")

def get_lib_paths(version_dir):
    # 查找ld和libc文件
    ld = glob.glob(os.path.join(version_dir, "ld-*.so"))
    libc = glob.glob(os.path.join(version_dir, "libc-*.so"))
    
    if not ld:
        print(f"在 {version_dir} 中找不到ld文件！")
        exit(1)
    if not libc:
        print(f"在 {version_dir} 中找不到libc文件！")
        exit(1)
        
    return ld[0], libc[0]

def get_executable():
    # 获取可执行文件路径
    while True:
        path = input("\n请输入可执行文件路径：").strip()
        if os.path.isfile(path):
            return path
        print("文件不存在，请重新输入！")

def main():
    version_dir = select_version()
    ld_path, libc_path = get_lib_paths(version_dir)
    executable = get_executable()
    
    # 执行patchelf命令
    try:
        subprocess.run([
            "patchelf",
            "--set-interpreter",
            ld_path,
            executable
        ], check=True)
        
        subprocess.run([
            "patchelf",
            "--replace-needed",
            "libc.so.6",
            libc_path,
            executable
        ], check=True)
        
        print("\n操作成功完成！")
    except subprocess.CalledProcessError as e:
        print(f"\n命令执行失败：{e}")
    except Exception as e:
        print(f"\n发生错误：{str(e)}")

if __name__ == "__main__":
    main()