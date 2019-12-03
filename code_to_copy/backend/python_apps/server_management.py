# Ansible
# Ref
# http://www.mydailytutorials.com/introduction-shell-command-module-ansible/

# 默认的 Adhoc的 command




# 设置这个可以直接在设置账号密码后直接登录
# https://stackoverflow.com/questions/23074412/how-to-set-host-key-checking-false-in-ansible-inventory-file


# 喜欢切换用户的话，可以用这个;  但是感觉好像没啥用
# --become-method su --become-user root



# 坑
# 似乎用户自己设置的环境变量

# 经典设置
# ~/.ansible.cfg
'''
[defaults]
inventory = .ansible_hosts
'''

# ~/.ansible_hosts
'''
[server]
10.0.0.4  # Server01

[clients]
CPU-Client01   #
'''

# ansible-playbook run_exp.yaml
'''
- hosts: clients
  tasks:
  - name: run exp
    shell: tmux new-session -s session_name -d 'sleep 5'
    args:
        chdir: /home/xiaoyang/repos/amc-data/
'''
