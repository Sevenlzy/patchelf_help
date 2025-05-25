# import os
# import re

# def get_lib_paths(version_dir):
#     """根据版本目录路径，获取 libs 子目录下的 ld 和 libc 文件路径"""
#     # 从版本目录名中提取版本号
#     dir_name = os.path.basename(version_dir)
#     match = re.search(r'^(\d+\.\d+)', dir_name)
#     if not match:
#         raise ValueError(f"无法从目录名 {dir_name} 中提取版本号")
#     version = match.group(1)  # 提取版本号，例如 "2.27"

#     # 构造 libs 子目录路径
#     libs_dir = os.path.join(version_dir, "libs", dir_name)

#     # 构造文件名
#     ld_filename = f"ld-{version}.so"
#     libc_filename = f"libc-{version}.so"

#     # 生成完整路径
#     ld_path = os.path.join(libs_dir, ld_filename)
#     libc_path = os.path.join(libs_dir, libc_filename)

#     return ld_path, libc_path

# # 示例使用
# if __name__ == "__main__":
#     version_dir = "/home/alen/alen/tools/glibc-all-in-one/2.27-3ubuntu1.5_amd64"
#     ld_path, libc_path = get_lib_paths(version_dir)
#     print(f"ld path: {ld_path}")
#     print(f"libc path: {libc_path}")



import subprocess
import re

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


libc1 = get_libc_path('/home/alen/alen/pwn/25-4/sao/pwn')
libc2 = get_libc_path('/home/alen/alen/pwn/25-6/hitcon_ctf_2019_one_punch/pwn')
print(libc1)
print(libc2)