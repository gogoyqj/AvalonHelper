Sublime Avalon Completion Package
===============================

目测依赖sublime 自带的完成功能，根据avalon语法字典帮助开发者更便捷高效的使用avalon，在sublime 3上work ok

可以通过设置Avalon语法字典或者直接修改helper.txt文件来添加更多语法支持

-------
how to use

	1，git clone code to sublime 3/data/packages/AvalonHelper - 
	
	注意：一定是放在插件默认的安装目录下，比如是:
		
		C:\Users\username\AppData\Roaming\Sublime Text 3\Packages\AvalonHelper
		
		Mac则通过“首选项【preferences】 -> 浏览程序包【brow packages】”打开安装目录，直接拷贝过来，ps：avalonHelper的Main.sublime-menu设置可能会修改menu的效果，比如纯英文界面多出一个首选项的汉子item来 = =

	2，ms召唤出属性绑定，组件名字可以召唤出组件自动完成，data召唤出data绑定，data-组件名字召唤出组件属性自动完成(暂时未提供组件属性、接口等字典)

	3，helper.txt第一行是ms绑定，第二行是组件名字(组件名字+"="意味这个替换字符串是ms-组件名字="")，第三行是data绑定


-------
time line

2014.10.17 - 修复多次换行缩进 bug

2014.10.20 - 添加 w[idget] 召唤出组件列表功能
