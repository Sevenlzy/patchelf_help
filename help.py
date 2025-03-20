import os
import subprocess
from pathlib import Path

# 配置项
GLIBC_ALL_IN_ONE_FILE = "/home/alen/alen/tools/glibc-all-in-one/old_list"
GLIBC_ALL_IN_ONE_PATH = "/home/alen/alen/tools/glibc-all-in-one"
LIBS_BASE = "/home/alen/alen/tools/glibc-all-in-one/libs"

def update_glibc_list():
    """更新glibc版本列表"""
    try:
        subprocess.run(
            ["./update_list"],
            cwd=GLIBC_ALL_IN_ONE_PATH,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n[!] 更新版本列表失败: {str(e)}")
        return False

def download_glibc_version(version):
    """下载指定版本的glibc"""
    try:
        result = subprocess.run(
            ["./download_old", version],
            cwd=GLIBC_ALL_IN_ONE_PATH,
            check=True,
            capture_output=True,
            text=True
        )
        if "Download failed" in result.stderr:
            print(f"\n[!] 下载失败: {result.stderr}")
            return False
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n[!] 下载命令执行失败: {e.stderr}")
        return False

def check_and_download(version):
    """检查并下载缺失的版本"""
    version_dir = os.path.join(LIBS_BASE, version)
    
    if os.path.exists(version_dir):
        return True
    
    print(f"\n[!] 检测到版本 {version} 未安装")
    choice = input("是否立即下载？(y/N): ").lower()
    
    if choice != 'y':
        print("[*] 已取消下载")
        return False

    if not update_glibc_list():
        return False

    available_versions = get_available_versions()
    if version not in available_versions:
        print(f"\n[!] 错误：版本 {version} 不存在于可用列表")
        print("当前可用版本：")
        print('\n'.join(available_versions))
        return False

    print(f"\n[*] 正在下载 {version} ...")
    if download_glibc_version(version):
        print("[+] 下载完成")
        return os.path.exists(version_dir)
    return False

def get_available_versions():
    """从 list 文件中获取可用 glibc 版本列表"""
    list_file = Path(GLIBC_ALL_IN_ONE_FILE)
    if not list_file.exists():
        print(f"\n[!] 版本列表文件 {GLIBC_ALL_IN_ONE_FILE} 不存在")
        return []
    return list_file.read_text().splitlines()

def select_version():
    """选择 glibc 版本并返回版本目录"""
    available_versions = get_available_versions()
    if not available_versions:
        print("\n[!] 没有可用的 glibc 版本")
        exit(1)

    print("\n可用 glibc 版本：")
    for i, version in enumerate(available_versions, 1):
        print(f"{i}. {version}")

    while True:
        try:
            choice = int(input("\n请输入版本序号："))
            if 1 <= choice <= len(available_versions):
                selected_version = available_versions[choice - 1]
                version_dir = os.path.join(LIBS_BASE, selected_version)
                return version_dir
            else:
                print("序号无效，请重新输入！")
        except ValueError:
            print("请输入有效的数字序号！")

def get_lib_paths(version_dir):
    """获取 ld 和 libc 路径（示例实现，需根据实际调整）"""
    ld_path = os.path.join(version_dir, "ld-linux-x86-64.so.2")
    libc_path = os.path.join(version_dir, "libc.so.6")
    return ld_path, libc_path

def get_executable():
    """获取要修补的可执行文件（示例实现）"""
    return input("请输入可执行文件路径：")

def main():
    version_dir = select_version()
    version_name = os.path.basename(version_dir)
    
    if not check_and_download(version_name):
        exit(1)
    
    ld_path, libc_path = get_lib_paths(version_dir)
    executable = get_executable()
    
    try:
        subprocess.run(["patchelf", "--set-interpreter", ld_path, executable], check=True)
        subprocess.run(["patchelf", "--replace-needed", "libc.so.6", libc_path, executable], check=True)
        print("\n[+] 操作成功完成！")
    except subprocess.CalledProcessError as e:
        print(f"\n[!] 错误：{str(e)}")
        exit(1)

if __name__ == "__main__":
    main()