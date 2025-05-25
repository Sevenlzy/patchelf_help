import subprocess
import re

def get_libc_path(executable):
    try:
        # 执行 ldd 命令并获取输出
        ldd_output = subprocess.check_output(["ldd", executable], text=True)
        
        # 正则表达式匹配 libc*.so 的路径（箭头前的路径）
        match = None
        for line in ldd_output.splitlines():
            if 'libc' in line:  # 查找包含 libc 的行
                # 使用正则表达式匹配箭头前的路径
                # match = re.search(r" => (/.+libc.*\.so[^ ]*)", line)
                match = re.search(r" => (/.+libc.*\.so[^ ]*)", line)
                if match:
                    if '/lib/x86_64-linux-gnu/libc.so.6' in match.group(1):
                        return 'libc.so.6'
                    return match.group(1)  # 返回箭头前的路径
        
        raise ValueError("libc not found in ldd output.")
    
    except subprocess.CalledProcessError as e:
        print(f"ldd 执行错误: {e}")
        # exit(1)
    except ValueError as e:
        print(f"错误: {e}")
        # exit(1)


libc1 = get_libc_path('/home/alen/alen/pwn/25-4/sao/pwn')
libc2 = get_libc_path('/home/alen/alen/pwn/25-6/hitcon_ctf_2019_one_punch/pwn')
print(libc1)
print(libc2)


# from pathlib import Path

# GLIBC_ALL_IN_ONE_FILE_COMMON = "/home/alen/alen/tools/glibc-all-in-one/list"
# GLIBC_ALL_IN_ONE_FILE_OLD = "/home/alen/alen/tools/glibc-all-in-one/old_list"


# def download_glibc_version(version):
#     """下载指定版本的glibc"""
#     try:
#         # 读取文件
#         common_file_path = Path(GLIBC_ALL_IN_ONE_FILE_COMMON)
#         old_file_path = Path(GLIBC_ALL_IN_ONE_FILE_OLD)
        
#         with open(common_file_path, "r") as f:
#             common_lines = f.readlines()
        
#         with open(old_file_path, "r") as f:
#             old_lines = f.readlines()
        
#         # 打印文件内容，查看文件是否正确读取
#         # print(f"Common List Content: {common_lines}")
#         # print(f"Old List Content: {old_lines}")
        
#         # 判断版本是否存在
#         if any(version in line for line in common_lines):
#             download_script = "download"
#         elif any(version in line for line in old_lines):
#             download_script = "download_old"
#         else:
#             print(f"\n[!] 错误：版本 {version} 不存在于任何路径")
#             exit(0)
        
#         print(f"[*] 执行命令: ./{download_script} {version}")

#     except Exception as e:
#         print(f"[!] 错误：{str(e)}")

# # 测试版本号
# download_glibc_version("2.29-0ubuntu2_amd64")
# download_glibc_version("2.31-0ubuntu9.17_amd64")
# download_glibc_version("2.31-0ubuntu9_i386")