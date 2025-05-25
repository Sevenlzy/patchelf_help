import os
import subprocess
from pathlib import Path
import re

# 配置项
GLIBC_ALL_IN_ONE_FILE_COMMON = "/home/alen/alen/tools/glibc-all-in-one/list"
GLIBC_ALL_IN_ONE_FILE_OLD = "/home/alen/alen/tools/glibc-all-in-one/old_list"
GLIBC_ALL_IN_ONE_PATH = "/home/alen/alen/tools/glibc-all-in-one"
LIBS_BASE = "/home/alen/alen/tools/glibc-all-in-one/libs"

def update_glibc_list():
    """更新glibc版本列表"""
    try:
        subprocess.run(
            ["./update_list"],
            cwd=GLIBC_ALL_IN_ONE_PATH, #current working directory  cwd
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
        # 读取文件
        common_file_path = Path(GLIBC_ALL_IN_ONE_FILE_COMMON)
        old_file_path = Path(GLIBC_ALL_IN_ONE_FILE_OLD)
        
        with open(common_file_path, "r") as f:
            common_lines = f.readlines()
        
        with open(old_file_path, "r") as f:
            old_lines = f.readlines()
        
        # 判断版本是否存在
        if any(version in line for line in common_lines):
            download_script = "download"
        elif any(version in line for line in old_lines):
            download_script = "download_old"
        else:
            print(f"\n[!] 错误：版本 {version} 不存在于任何路径")
            exit(0)
        
        print(f"[*] 执行命令: ./{download_script} {version}")
        
        result = subprocess.run(
            [f"./{download_script}", version],  # 使用对应的下载脚本
            cwd=GLIBC_ALL_IN_ONE_PATH,  # 指定工作目录
            check=True,
            capture_output=True,
            text=True
        )
        
        # 检查是否下载成功
        if "Download failed" in result.stderr:
            print(f"\n[!] 下载失败: {result.stderr}")
            return False
        
        print(f"[+] 下载成功：{result.stdout}")
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
    # 列出两个文件路径
    list_file = [Path(GLIBC_ALL_IN_ONE_FILE_COMMON), Path(GLIBC_ALL_IN_ONE_FILE_OLD)]

    versions = []
    for file in list_file:
        # 检查每个文件是否存在
        if not file.exists():
            print(f"\n[!] 版本列表文件 {file} 不存在")
        else:
            # 如果文件存在，读取文件并合并到版本列表中
            versions.extend(file.read_text().splitlines())
    
    return versions
def select_version(target_width=28):
    """选择 glibc 版本并返回版本目录"""
    available_versions = get_available_versions()
    if not available_versions:
        print("\n[!] 没有可用的 glibc 版本")
        exit(1)

    print("\n可用 glibc 版本：")
    colunns = 3  # 每行显示的版本数量
    lines = [available_versions[i:i+colunns] for i in range(0, len(available_versions), colunns)]
    for line in lines:
        formatted_line = []  # 用于保存当前行的版本信息
        for j in range(len(line)):
            # 计算当前版本的编号
            version_number = colunns * (lines.index(line)) + j + 1  # 计算版本号
            version_str = f"{version_number}. {line[j]}"
            
            # 计算当前版本信息的长度，并补充空格使总长度达到 target_width
            spaces_to_add = target_width - len(version_str)
            formatted_line.append(f"{version_str}{' ' * spaces_to_add}")
        
        # 打印当前行，并用两个空格连接版本信息
        print("  ".join(formatted_line))

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



def get_libc_path(executable):
    try:
        # 执行 ldd 命令并获取输出
        ldd_output = subprocess.check_output(["ldd", executable], text=True)
        
        # 正则表达式匹配 libc*.so 的路径
        match = None
        for line in ldd_output.splitlines():
            if 'libc' in line:  # 查找包含 libc 的行
                # 使用正则表达式匹配路径
                match = re.search(r"/.*libc.*\.so[^ ]*", line)
                if match:
                    if '/lib/x86_64-linux-gnu/libc.so.6' in match.group(0):
                        return 'libc.so.6'
                    return match.group(0)
                
        raise ValueError("libc not found in ldd output.")
    
    except subprocess.CalledProcessError as e:
        print(f"ldd 执行错误: {e}")
        exit(1)
    except ValueError as e:
        print(f"错误: {e}")
        exit(1)


def get_lib_paths(version_dir):
    """根据版本目录路径，获取 libs 子目录下的 ld 和 libc 文件路径"""
    # 从版本目录名中提取版本号
    dir_name = os.path.basename(version_dir)
    match = re.search(r'^(\d+\.\d+)', dir_name)
    if not match:
        raise ValueError(f"无法从目录名 {dir_name} 中提取版本号")
    version = match.group(1)  # 提取版本号，例如 "2.23"

    # 构造 libs 子目录路径
    libs_dir = os.path.join(version_dir)  # 确保路径没有重复

    # 构造文件名
    ld_filename = f"ld-{version}.so"
    libc_filename = f"libc-{version}.so"

    # 生成完整路径
    print(libs_dir)
    ld_path = os.path.join(libs_dir, ld_filename)
    libc_path = os.path.join(libs_dir, libc_filename)

    return ld_path, libc_path


def get_executable():
    """获取要修补的可执行文件路径"""
    return input("请输入可执行文件路径：")

def main():
    version_dir = select_version()
    version_name = os.path.basename(version_dir)
    
    if not check_and_download(version_name):
        exit(1)
    
    ld_path, libc_path = get_lib_paths(version_dir)
    executable = get_executable()
    my_libc = get_libc_path(executable)
    
    # 打印调试信息，显示将执行的命令
    print(f"\n[*] 将执行的命令：")
    print(f"patchelf --set-interpreter {ld_path} {executable}")
    print(f"patchelf --replace-needed {my_libc} {libc_path} {executable}")
    
    try:
        subprocess.run(["patchelf", "--set-interpreter", ld_path, executable], check=True)
        subprocess.run(["patchelf", "--replace-needed", my_libc, libc_path, executable], check=True)
        print("\n[+] 操作成功完成！")
    except subprocess.CalledProcessError as e:
        print(f"\n[!] 错误：{str(e)}")
        exit(1)

if __name__ == "__main__":
    main()