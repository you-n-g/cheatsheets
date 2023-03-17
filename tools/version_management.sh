
# 目录
# - 查看操作

# # Outlines: git
# ## Outlines: 查看操作
git log -p <filename>  # 找到这个文件的所有历史 patch



# TODO: 继续merge


# BEGIN 常用基本操作 VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV

# PR相关
# https://stackoverflow.com/questions/34100048/github-create-empty-branch
# 创建空分支,  就可以对着空的分支做PR




# 基本操作主要参考  http://rogerdudler.github.io/git-guide/


# 配置
# man git config 可以看看这些配置项是干嘛的
git config --global color.ui auto # 配置自动颜色
# 配置merge
git config --global merge.tool vimdiff
git config --global mergetool.prompt false

# 忽略chmod的影响: http://stackoverflow.com/questions/1580596/how-do-i-make-git-ignore-file-mode-chmod-changes
git config core.fileMode false
# 但是默认这个配置仅仅会影响x位(需要确认到底是他仅仅管x位还是git仅仅管x位)，但是一般我们仅仅需要改变读写权限，可以chmod g+r 之类的命令代替

# 看看已经配置了哪些config
git config --list


#patch的导入导出
git format-patch master # 将patch都导出来
git format-patch -N # 将最新的N个patch都导出来
git apply <filename> # 之后再导入, 默认不加参数时是不会出现在index里的，更不会commit


# 查看历史
## 看分支图
git log --graph --oneline --decorate --all  # all 代表显示所有分支， 本来只会显示head所在的分支
git diff '@{2}' # 查看最近两次改变的合集 # diff 默认是 working dir和index比较， diff HEAD才是 working dir 和 repo比较
git reflog # 可以看到commit的纪录， 专门处理不在任何分支的commit
## 查看具体的文件
git blame -L9,+10 THE_FILE  # 可以看THE_FILE的 9 ~ 9 + 10 行是谁改过
## 查看这个commit属于哪个分支, 一些可能有其他用途的东西：http://stackoverflow.com/questions/2706797/finding-what-branch-a-git-commit-came-from
git branch --contains <commit>
## 看看head的 commit是哪个
git rev-parse HEAD


# 恢复

# 操作working directory
git checkout .  # 恢复到head版本 仅仅作用于working directory, 不包括staged
git checkout -- filename # 恢复某文件到 head 版本， --为了以防在 有和filename同名的branch时没有歧义
# - 比如 git rm 删掉的文件已经在 cache里了， 可以用这个命令恢复
git checkout c5f567 -- file1/to/restore file2/to/restore # 将指定文件恢复成指定版本 https://stackoverflow.com/a/215731
git branch -f branch-name XXX_COMMIT # 可以直接将已经有的branch 设置到指定的commit

# 操作分支指针
git reset --hard COMMIT_NAME # 我会但是会改变当前的branch指针和head指向的分支指针;
# 如果加了 --hard， working directory, staged通杀; 默认是--mixed 清除index，保留working directory(所以相当于当前文件保留，但是只改变分支指针的指向); reset 不会删除commit;
git checkout -B XXXXX # 如果需求只是把分支缓一缓，那么可以checkout到某个commit后，再用这个命令重新设置分支 (试了之后如果是直接改变HEAD指向的分支的， 还是hard更方便)


# 操作 cached/staged/index # 可以 git ls-files 看index里有什么
git rm --cached <filename>  # 从 Index 删除文件， 其他都不管； 如果以前就有，新的commit中就不会有这个文件， 有点像hg forget； 如果这个文件是最新commit之后加上的，则直接在index删除
git reset HEAD filename  # 效果是 将 index中文件恢复到 HEAD状态(即to be committed的会被消除， 但是文件不会被标记成下次删除/unstage)，  不管working directory
# - rm --cached 表示在index中删除文件;   reset表示在index中重置文件成某个版本



# 合并
git reset --merge  # merge 失败
git cherry-pick --abort  # cherry-pick 失败
git mergetool  # 当发生分支冲突的时候merge失败之后呼唤mergetool来合并
# TODO 如何Backport到以前的分支
# 根据django的案例来说，直接提交到master就行，之后会有人backport到以前的分支
# backport使用cherry-pick
git mergetool # 使用这个命令来合并分支

# git pull -u 时不能将未提交的修改自动和分支合并， 所以需要先用stash将已经修改的内容存储起来
git stash  # 可以把当前工作目录的 状态储存起来，然后去别的分支工作，  通过加参数 还可以直接创建分支。
git stash list  # 查看所有储存
git stash clear  # 清除stash中的所有内容
git stash apply  # 应用 储存， 目录不一定要干净， 不一定要和原来一个节点。 通过加参数还可以改到一半的时候取消刚刚应用的储存。



# 提交: 我体验到真正的逻辑是 先看本地 branch track 哪个repo，然后去找相应repo的url，优先用pushurl (push 和 pull可以不一样)
git remote set-url --push origin git@github.com:you-n-g/multiverso.git   #  设置代码库的push url 和改 .git/config 效果一样
git push  [-u] [<repository> [<refspec>...]]
    # 相当于向repository 提交， 对应规则是 refspec; repository 省略相当于 orign
    # refspec 格式为 <src>:<dst>
        # 省略<src> 相当于删除dst , 即  git push origin :branchname
        # 省略:<dst>相当于将同名branch同步到orign中
    # -u 表示上传成功后自动设置本地branch track 相应的 remote branch,  似乎只有没设置过时有效？？
        # git branch --set-upstream-to origin/my_branch : 如果已经设置过，那么可以手动用这个命令设置当前brach , 和改 .git/config 效果一样
        # git pull 也支持这个参数， 设置过了就别平时没事就加这个参数了
git push -f origin HEAD^:master  # 案例: 想反悔一个commit时， 将本地HEAD的上一个commit强行提交到master分支，这样本地不变，repo恢复一个




# 管理submodule
#查看
git submodule 能查看有哪些子模块。

#添加
git submodule add GIT_URL [PATH] # 加完后会在 .gitmodules 中加东西

#初始化
git submodule init # 初始化的时候只是得到子模块的指针
git submodule update # 可以更新子模块

git submodule update --init --recursive # 其实千言万语可以汇成一句话……


# fork后，用项目repo的内容 更新本地repo
# TODO 等待消化， 取自 docker-从入门到实践 http://yeasy.gitbooks.io/docker_practice/
git	remote	add	upstream	https://github.com/yeasy/docker_practice
git	fetch	upstream 
git	checkout	master 
git	rebase	upstream/master  
# rebase 的过程中会遇到冲突，这时应该编辑，然后add，**千万不要commit**，然后继续rebase
# 比如你开发到一半，别的commit对你有影响，这时你rebase然后继续开发会更好
<<EOF * rebase (分支衍合)
git rebase [主分支] [某分支] :  把某分支 rebase 到主分支上去，相当于把某分支从主分支的接连处剪下来，然后接到主分支的尾巴上去
- 如果没指定 某分支 则是 用当前分支当某分支
- 如果同时没指定 主分支 则用 branch.<某分支>.remote 和 branch.<某分支>.merge 来当主分支
git rebase --onto master server client  :   取出 client 分支，找出 client 分支和 server 分支的共同祖先之后的变化，然后把它们(client分支上的变化)在 master 上重演一遍
如果 apply 失败则 会产生 .git/rebase-apply 这个文件
rebase 的好处在于少了个merge，branch会cleaner
EOF
git	push -f	origin	master  # 需要force push的原因是rebase后整个branch和 origin的 branch分叉了


# 清除文件
# http://stackoverflow.com/questions/673407/how-do-i-clear-my-local-working-directory-in-git
git clean -d -x -f
# -d 表示删文件夹， -x 表示包括gitignore 中的文件， -f 换成 -n会先让你看一眼删什么。


# 特殊文件
.git/info/exclude 起到和GITIGNORE一样的作用　# http://stackoverflow.com/questions/1753070/git-ignore-files-only-locally

# 对于tracked files: http://stackoverflow.com/questions/13630849/git-difference-between-assume-unchanged-and-skip-worktree/13631525#13631525
# 对于一些不会改变的文件， 比如SDK , 可以设置每次不去看它的变化， 这样可以提高git status的性能； 但是fetch下来的文件一旦变化，这里就失效了
git update-index --[no-]assume-unchanged [<file>...]
# 对于一些本地不希望和远程一样的配置文件， 可以用这个，这样就不会看它的变化， 而且服务器上变化了也不会有影响
git update-index --[no-]skip-worktree [<file>...]

# END   常用基本操作 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^






# BEGIN gerrit 向开源社区提交代码篇
# 以openstack为例
# 主要参考 https://wiki.openstack.org/wiki/Gerrit_Workflow
# 次要参考 http://www.21ops.com/cloud-computing/openstack/21213.html


# 修改过的文件用 pep8 看看
pep8 <filename>
# 每个review对应一个change， 对同一个review应该使用同一个 change, 在gerrit中能看到
# http://sinojelly.sinaapp.com/2011/08/git-changes-submitted-by-the-previous-method-pay-special-attention-to-change-id-unchanged/

# 1) 使用gerrit提供的commit-msg hook 来自动生成 change-id

# 2) 使用 amend 自动保存change-id 
git commit --amend
# 或者 reset后在新的commit中加上change-id
git reset HEAD^

# END   gerrit 向开源社区提交代码篇




操作篇
	* remote

		* git remote -v : 查看远程库的地址
		* git remote add [shortname] [url] : 可以添加远程仓库。
		* git remote show [origin]:  查看远程repo的情况
		* git remote rename origin_name local_name : 可以修改某个远程仓库在本地的命名。
		* git remote rm repo_name :  在本地删除远程仓库。

	* git fetch [REMOTE REPO] [remote_brachname:local_branchname]：从远程仓库更新到本地仓库。
	* git init:: 初始化一个git版本
	* git pull [remote-name] [branch-name] other.computer:/path/to/files ::  等价于 git fetch  + git  merge FETCH_HEAD

	* git add :  把文件放入暂存状态， 如果 untracked 就track并  放入暂存状态。
	* git rm (path|file|pattern) :  把这个删除操作放到暂存区里。 rm的时候加 --cached 相当于forget.
	* git mv : 相当于 rm 然后再 add ， 但是如果分开做git 也能知道是重命名。
	* git commit [-a] [-m LOG] [--amend]:: -m 不用调用editor 来编辑log了, -a 自动把tracked 的文件都暂存起来一起提交。     --amend表示 把当前暂存区域补上到最后一次提交中，并能重新编辑。 
	* git status :   看到现在在哪个分支下， 被改变的文件，及被暂存的文件
	* git reset [--hard] [VERSION] [files]::

		* 只加files 则是把stage 的文件变成  modified
		* 回滚到以前的某个版本,log里的东西也不见了!!! 所有新提交全抹掉!!! 加hard可以忽略当前所有改变

	* checkout :: 直接用可以看到 hg st 之类的问题

		* git checkout VERSION:: 这相当于在那个地方建一个未命名的分枝,之后再checkout -b来命名保存
			* 如果这个时候做改变,则自动创建分枝, git checkout master 可以回到原来的版本
			* 你可以选择只恢复特定文件或子目录，把这些加到该命令后面就可以了。 ???
			* 关于格式

				* git checkout "@{10 minutes ago}"
				* git checkout "@{5}" :: 回到倒数第5次保存状态


		* git checkout -b Branch_name [remote_branch] ::  等价于 git branch Branch_name,   git checkout branch_name ,  新建分支指针，然后再把HEAD指针指向它。 如果加了remote_branch， 则相当于新建和远程分支一样的分支， 相对远程分支，这个分支叫跟踪分支。   使用 --track REMOTE_BRANCH 可以直接新建跟踪分支。
		* git checkout Branch_name :: 切换分枝，即改变 Head指向的分支指针。
		* git checkout file :: 是把modified 的文件 变回去。

	* git diff [VERSION1 [VERSION2]] :: 如果不加version则当前working directory 与暂存版本的 区别, 加1个version则当状态与指定状态的区别, 加2个表示两个状态之间的区别。  如果 加  --staged 表示 当前 暂存版与 指定版本的区别。     
	* git instaweb :: 可以用浏览器看版本 , 居然还需要安装 lighttpd....

git branch [branch name] :: 可以查看branch或者新建分支指针, 不加参数会列出分支清单。[--merged] 可以查看当前分支的直接上游

	* git branch -d branch_name :: 可以删除一个branch, 如果该分支还未合并，删除会提示错误， 如果要强行删除，加上 -D
	* git branch -m branch_name :: 可以重命名一个branch
	* git branch -a :: 可以把远程的和本地的branch全列出来
	*  git branch --set-upstream local_branch repo/repo_branch :: 设置push的时候怎么push


	* git merge branch_name :: 把branch里的东西合并到当前branch。 如果是单线的合并，则 直接把分支指针都指向最新Tree，称作(Fast Forward).  GIT合并之后， 会把需要人工合并的内容在git status 中标记为 unmerged、unstaged， 人工merge之后， 用 add 把它标记为已经合并的状态就行了。
	* git cherry-pick SHA1_HASH :: 把另一个分枝里的东西直接拿过来,　但会留本地文件??　与merge有什么区别啊>> === 怎么?? ===
	* git tag

		* git tag  -a  -m MESSAGE [version] :  可以给指定版本加tag标记
		* git show 可以查看所有的tag详细信息
		* git push <reponame> <tagname> 可以提交指定tag
		* git  push <reponame> --tags  可以把所有tags 提交上去。



	* git log :   --graph 能显示分支走向。

	* git blame 可以看到这个有问题的地方是谁提交的
	* git bisect 可以二分查找有问题的地方在哪里
	* 怎么才能拿下来一个非默认的 branch




github使用篇
	* key能放在个人面版里或者repo的admin页面里
	* 设置git的默认branch在repo的admin页面里!!


# # Outlines: mercurial

# VVVVVVVVVVVVVVVVVVV mercurial VVVVVVVVVVVVVVVVVVVVV

# VV .hg/hgrc VV
[ui]
username = Young Yang
merge = vimdiff

[paths]                                                  
default = ssh://hg@bitbucket.org/XXX

[extensions]
churn =

# ^^ .hg/hgrc ^^

 
mercurial
	* hg revert -r N DIR:: revert to vertion N

		* hg revert --all -r a9f5b790937f (yk版)

	* hg update -r N:: update to vertion N, if N is not given, it will be updated to the newest version; if DIR is not given, it's ./
	* hg parents 可以查看当前的 Working directory 的版本号
	* bitbucket.org/account 里可以添加publickey , 这个key是针对用户的
	* .hgignore :: 可以看哪些文件需要被忽略 ,放在repo的根目录下, 不是.ssh 里, 每行匹配一个文件, 使用wizard card 匹配
	* hg forget 等价于 hg remove -Af :: 把文件从repo里去掉但不从本地去掉
	* hg addremove:: 把不匹配.hgignore里的新文件add, 把丢失的文件remove
	* hg serve:: 开一个端口让图形化看hg的版本
	* hg pull -r REV REPO :: 可以clone指定版本
	* hg log -r a:b :: 可以看 a ~ b 的log
	* hg resolve -t vimdiff . :: 可以选择使用哪个工具来 merge
	* hg rollback :: 不用任何参数就直接把上一个changeset删除... == 针对特定节点导入导出 ==
	* hg export CHANGESET..... > PATCH.diff
	* hg import [--no-commit] DIFFFILES..... :: 如果有 --no-commit 就不会生成新的节点 == branch 的处理 ==
	* hg branch 可以查看我在哪个branch下
	* 在 branch 之间切换使用 update
	* hg branches 显示当前的branches
	* branch 在产生head的时候就产生了， 如果有兴趣可以 使用 hg branch NAME 给branch取名
	* hg branch --close-branch 可以关闭这个 branch, 这样就不会在 branches 里出现

		* 正确关闭 分支的方法 来自  http://stackoverflow.com/questions/2237222/how-to-correctly-close-a-feature-branch-in-mercurial
			* 先 commit close branch 
			* 然后再merge ， 这样就  branches 和  heads 就不会有多余的东西了



