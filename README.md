菜鸡的一键打patch小脚本
alias pwnhelp='python /home/alen/alen/tools/patch_help/help.py'

alen@alen:~/alen/pwn/25-6/hitcon_ctf_2019_one_punch$ pwnhelp

可用 glibc 版本：
1. 2.23-0ubuntu11.3_amd64     2. 2.23-0ubuntu11.3_i386      3. 2.23-0ubuntu3_amd64      
4. 2.23-0ubuntu3_i386         5. 2.27-3ubuntu1.5_amd64      6. 2.27-3ubuntu1.5_i386     
7. 2.27-3ubuntu1.6_amd64      8. 2.27-3ubuntu1.6_i386       9. 2.27-3ubuntu1_amd64      
10. 2.27-3ubuntu1_i386        11. 2.31-0ubuntu9.17_amd64    12. 2.31-0ubuntu9.17_i386   
13. 2.31-0ubuntu9_amd64       14. 2.31-0ubuntu9_i386        15. 2.35-0ubuntu3.9_amd64   
16. 2.35-0ubuntu3.9_i386      17. 2.35-0ubuntu3_amd64       18. 2.35-0ubuntu3_i386      
19. 2.39-0ubuntu8.4_amd64     20. 2.39-0ubuntu8.4_i386      21. 2.39-0ubuntu8_amd64     
22. 2.39-0ubuntu8_i386        23. 2.40-1ubuntu3.1_amd64     24. 2.40-1ubuntu3.1_i386    
25. 2.40-1ubuntu3_amd64       26. 2.40-1ubuntu3_i386        27. 2.41-6ubuntu1_amd64     
28. 2.41-6ubuntu1_i386        29. 2.41-6ubuntu2_amd64       30. 2.41-6ubuntu2_i386      
31. 2.21-0ubuntu4.3_amd64     32. 2.21-0ubuntu4.3_i386      33. 2.21-0ubuntu4_amd64     
34. 2.21-0ubuntu4_i386        35. 2.24-3ubuntu1_amd64       36. 2.24-3ubuntu1_i386      
37. 2.24-3ubuntu2.2_amd64     38. 2.24-3ubuntu2.2_i386      39. 2.24-9ubuntu2.2_amd64   
40. 2.24-9ubuntu2.2_i386      41. 2.24-9ubuntu2_amd64       42. 2.24-9ubuntu2_i386      
43. 2.26-0ubuntu2.1_amd64     44. 2.26-0ubuntu2.1_i386      45. 2.26-0ubuntu2_amd64     
46. 2.26-0ubuntu2_i386        47. 2.28-0ubuntu1_amd64       48. 2.28-0ubuntu1_i386      
49. 2.29-0ubuntu2_amd64       50. 2.29-0ubuntu2_i386        51. 2.30-0ubuntu2.2_amd64   
52. 2.30-0ubuntu2.2_i386      53. 2.30-0ubuntu2_amd64       54. 2.30-0ubuntu2_i386      
55. 2.32-0ubuntu3.2_amd64     56. 2.32-0ubuntu3.2_i386      57. 2.32-0ubuntu3_amd64     
58. 2.32-0ubuntu3_i386        59. 2.33-0ubuntu5_amd64       60. 2.33-0ubuntu5_i386      
61. 2.34-0ubuntu3.2_amd64     62. 2.34-0ubuntu3.2_i386      63. 2.34-0ubuntu3_amd64     
64. 2.34-0ubuntu3_i386        65. 2.36-0ubuntu4_amd64       66. 2.36-0ubuntu4_i386      
67. 2.37-0ubuntu2.2_amd64     68. 2.37-0ubuntu2.2_i386      69. 2.37-0ubuntu2_amd64     
70. 2.37-0ubuntu2_i386        71. 2.38-1ubuntu6.3_amd64     72. 2.38-1ubuntu6.3_i386    
73. 2.38-1ubuntu6_amd64       74. 2.38-1ubuntu6_i386      

请输入版本序号：49
/home/alen/alen/tools/glibc-all-in-one/libs/2.29-0ubuntu2_amd64
请输入可执行文件路径：pwn

[*] 将执行的命令：
patchelf --set-interpreter /home/alen/alen/tools/glibc-all-in-one/libs/2.29-0ubuntu2_amd64/ld-2.29.so pwn
patchelf --replace-needed /home/alen/alen/tools/glibc-all-in-one/libs/2.31-0ubuntu9.17_amd64/libc-2.31.so /home/alen/alen/tools/glibc-all-in-one/libs/2.29-0ubuntu2_amd64/libc-2.29.so pwn

[+] 操作成功完成！
alen@alen:~/alen/pwn/25-6/hitcon_ctf_2019_one_punch$ ldd pwn
	linux-vdso.so.1 (0x00007ffca9375000)
	/home/alen/alen/tools/glibc-all-in-one/libs/2.29-0ubuntu2_amd64/libc-2.29.so (0x0000712ef75e0000)
	/home/alen/alen/tools/glibc-all-in-one/libs/2.29-0ubuntu2_amd64/ld-2.29.so => /lib64/ld-linux-x86-64.so.2 (0x0000712ef77d8000)


