# 🌌 ssprompt
简体中文 | [English]((./README-en.md))
<p>
	<p align="center">
		<img height=120 src="https://img.gejiba.com/images/e1945208195b199bd244431fd2a6efa0.png">
	</p>
	<p align="center">
		<font size=6 face="雅黑">⚡A LLM Prompt 分发管理工具⚡</font>
	<p>
	<p align="center">
		<b face="雅黑">Change the world, even a little bit.</b>
	<p>
</p>
<p align="center">
<img alt=" Python" src="https://img.shields.io/badge/Python-3.10%2B-blue"/>
<img alt="cleo" src="https://img.shields.io/badge/cleo-2.0.1-yellowgreen"/>
<img alt="license" src="https://img.shields.io/badge/license-Apache-lightgrey"/>
</p>

>自从OpenAI掀起了一轮新的AI革命，国内外众多玩家入场接受时代洗礼，一时间LLM相关技术井喷，而提示工程( prompt engineering )就在其中。   
它就像是为大语言模型（LLM）设计的"语言游戏"。通过这个"游戏"，我们可以更有效地引导 LLM 来处理问题。在真正的通用智能到来前，基于当前的LLM范式，要充分发挥LLM的优势，Prompt设计越来越复杂化，进一步Prompt的代码化，模块化会越发明显，同时写prompt将会成为AI时代人的基本技能。  
基于此，我构思创作了ssprompt，希望每个人都能利用Prompt，享受AI时代红利

## 🚀 Quick Install
### 系统依赖
Ssprompt requires Python 3.10+ 

⭐ 支持多平台使用，满足广大Prompt Engineer💻
### pip安装
`pip install ssprompt`
### Linux, macOS, Windows (WSL)
`curl -sSL https://raw.githubusercontent.com/ptonlix/ssprompt/main/install.py | python3 -`
### Windows (Powershell)
`(Invoke-WebRequest -Uri https://raw.githubusercontent.com/ptonlix/ssprompt/main/install.py -UseBasicParsing).Content | py -`


## What it can do?
ssprompt是一个Prompt分发管理工具，定义了一套Prompt分发规则，支持创建Prompt工程和拉取[Prompt Hub](https://github.com/ptonlix/PromptHub)上对应Prompt的工程文件到本地工程。


![Ssprompt Interaction](https://img.gejiba.com/images/2cb6f408c1de52e3d2e8c1fb603254ce.png)