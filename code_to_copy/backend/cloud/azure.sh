
# scratch commands ----------------------------------------

az cloud set -n AzureChinaCloud  # if az is for China, please switch to China Cloud first

az account list

az account set --subscription "e033d461-1923-44a7-872b-78f1d35a86dd"
# - 这个也是必要的，不然后面那些在具体sub下操作的命令都无法生效
# - 另外要检查你的账号是不是真的有权限(后来只有SC-*账号有权限了)
# - NOTE: 我感觉切换账号的时候，有可能这一步会导致出现问题 !!!!!!

az extension list-available


az extension add --name image-copy-extension

az image copy --source-resource-group "Fin-Cluster" --source-object-name "GPUTemplate" --target-location australiaeast --target-resource-group "Fin-Cluster"


az vm disk list

az vm run-command invoke --resource-group fintech --name Server --scripts "sudo ufw disable" --command-id RunShellScript


# 制作虚拟机镜像


az vm deallocate \
   --resource-group "Fin-Cluster" \
   --name "GPU-Client02"

az vm generalize \
   --resource-group "Fin-Cluster" \
   --name "GPU-Client02"

az image create \
   --resource-group "Fin-Cluster" \
   --name 'GPUTemplate2.0' --source "GPU-Client02"


# 虚拟机状态
# 当前可用的虚拟
# - CPU-Client01~CPU-Client14
# - 960核是极限
# - GPU-Client01

# CPU-Client01 jianfeng在用


# 常用 commmands -----------------------------------------------
# 更详细用法参考: https://docs.microsoft.com/en-us/cli/azure/?view=azure-cli-latest

# 创建虚拟机
# GPUTempate这个Image可以同时支持CPU和GPU

az vm create \
  --resource-group Fin-Cluster \
  --name CPU-Client07 \
  --image GPUTemplate \
  --size Standard_E64s_v3 \
  --admin-username xiaoyang \
  --ssh-key-value ~/.ssh/id_rsa.pub



# start vm

az vm start -n CPU-Client07 -g Fin-Cluster


# shutdown vm

az vm deallocate -n CPU-Client07 -g Fin-Cluster

for i in 6 5 
do
    az vm deallocate -n CPU-Client0$i -g Fin-Cluster
done


# delete vm
az vm delete -n CPU-Client07 -g Fin-Cluster



# 批量创建CPU虚拟机
for i in `seq -f '%02.0f' 8 15`
do
    az vm create \
      --resource-group Fin-Cluster \
      --name CPU-Client$i \
      --image GPUTemplate \
      --size Standard_E64s_v3 \
      --admin-username xiaoyang \
      --ssh-key-value ~/.ssh/id_rsa.pub

    az vm deallocate -n CPU-Client$i -g Fin-Cluster
done

# 批量创建GPU虚拟机
for i in `seq -f '%02.0f' 2 2`
do
    az vm create \
      --resource-group Fin-Cluster \
      --name GPU-Client$i \
      --image 'GPUTemplate2.0' \
      --size Standard_NV12_Promo \
      --admin-username xiaoyang \
      --ssh-key-value ~/.ssh/id_rsa.pub

    # az vm deallocate -n CPU-Client$i -g Fin-Cluster
done


# 网络相关

az vm open-port -g Fin-Cluster -n GPU-Client02 --port 3389-3389 --priority 100

az vm open-port -g Fin-Cluster -n QlibServer --port 3389-3389 --priority 100


# 看一个特定 network security group
az network nsg rule list -g Fin-Cluster02  --nsg-name "security_port"

az network nsg rule create -g Fin-Cluster02  --nsg-name "security_port"   --destination-port-ranges "5444"  -n "weiturui" --source-address-prefixes  139.219.14.69 --priority "1001"
