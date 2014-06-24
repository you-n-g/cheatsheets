

git format-patch master # 将patch都导出来
git apply <filename> # 之后再导入





# BEGIN gerrit 向开源社区提交代码篇
# 以openstack为例
# 主要参考 https://wiki.openstack.org/wiki/Gerrit_Workflow
# 次要参考 http://www.21ops.com/cloud-computing/openstack/21213.html


# 修改过的文件用 pep8 看看
pep8 <filename>
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
	* push

		* git push [origin branchname] :: 可以把指定的branch push上去，并用相同的名字， 默认的git push 相当于git push origin。 如果都不加， 就把当前的跟踪分支的修改提交到远程分支上去。
		* git push origin :branchname :: 这样可以把远程的branch删除 ????

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

	* rebase (分支衍合)

		* git rebase [主分支] [某分支] :  把某分支 rebase 到主分支上去。  如果没有某分支则是表示当前分支。
		* git rebase --onto master server client  :   取出 client 分支，找出 client 分支和 server 分支的共同祖先之后的变化，然后把它们在 master 上重演一遍

	* submodule

		* git submodule 能查看有哪些子模块。
		* git submodule update  初始化的时候只是得到子模块的指针，可以更新子模块

	* git log :   --graph 能显示分支走向。
	* git stash： 

		* git stash：  可以把当前工作目录的 状态储存起来，然后去别的分支工作，  通过加参数 还可以直接创建分支。
		* git stash list : 查看所有储存
		* git stash apply : 应用 储存， 目录不一定要干净， 不一定要和原来一个节点。 通过加参数还可以改到一半的时候取消刚刚应用的储存。

	* git blame 可以看到这个有问题的地方是谁提交的
	* git bisect 可以二分查找有问题的地方在哪里
	* 怎么才能拿下来一个非默认的 branch




github使用篇
	* key能放在个人面版里或者repo的admin页面里
	* 设置git的默认branch在repo的admin页面里!!


 
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



