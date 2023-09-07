# 🌌 ssprompt

简体中文 | [English](<(./README-en.md)>)

<p>
	<p align="center">
		<img height=120 src="https://img.gejiba.com/images/e1945208195b199bd244431fd2a6efa0.png">
	</p>
	<p align="center">
		<img src="https://img.gejiba.com/images/605bd1bcc1a14f803f1d8f68b8c1c892.png"><br>
		<b face="雅黑">Change the world, even a little bit.</b>
	<p>
</p>
<p align="center">
<img alt=" Python" src="https://img.shields.io/badge/Python-3.10%2B-blue"/>
<img alt="cleo" src="https://img.shields.io/badge/cleo-2.0.1-yellowgreen"/>
<img alt="license" src="https://img.shields.io/badge/license-Apache-lightgrey"/>
</p>

> 自从 OpenAI 掀起了一轮新的 AI 革命，国内外众多玩家入场接受时代洗礼，一时间 LLM 相关技术井喷，而提示工程( prompt engineering )就在其中。  
> 它就像是为大语言模型（LLM）设计的"语言游戏"。通过这个"游戏"，我们可以更有效地引导 LLM 来处理问题。在真正的通用智能到来前，基于当前的 LLM 范式，要充分发挥 LLM 的优势，Prompt 设计越来越复杂化，进一步 Prompt 的代码化，模块化会越发明显，同时写 prompt 将会成为 AI 时代人的基本技能。  
> 基于此，我构思创作了 ssprompt，希望每个人都能利用 Prompt，享受 AI 时代红利

## 🚀 Quick Install

### 系统依赖

Ssprompt requires Python 3.10+

⭐ 支持多平台使用，满足广大 Prompt Engineer💻

### pip 安装

```shell
pip install ssprompt
```

### Linux, macOS, Windows (WSL)

```shell
curl -sSL https://raw.githubusercontent.com/ptonlix/ssprompt/main/install.py | python3 -
```

### Windows (Powershell)

```shell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/ptonlix/ssprompt/main/install.py -UseBasicParsing).Content | py -
```

## 🔔 What it can do?

**ssprompt**是一个 Prompt 分发管理工具，定义了一套 Prompt 分发规则  
支持创建 Prompt 工程和拉取[Prompt Hub](https://github.com/ptonlix/PromptHub)上对应 Prompt 的工程文件到本地工程

![Ssprompt Interaction](https://img.gejiba.com/images/2cb6f408c1de52e3d2e8c1fb603254ce.png)

_注：以下为 0.5.0 第一版 ssprompt 的内容介绍，项目还在持续完善，如有疏漏或不足之处请包涵了解，谢谢~_

![ssprompt show](https://img.gejiba.com/images/343c5e8b220f5e498f1a192ece4b14d4.gif)

### 命令介绍

- ssprompt new -> 新建一个新的 Prompt 工程，指定工程目录，Prompt 类型等参数
- ssprompt init -> 基于当前目录，引导创建一个 Prompt 工程
- ssprompt add -> 添加一个不同 Prompt 类型和相关依赖到 metafile，并生成相应的 Prompt 工程目录（工程配置文件）
- ssprompt show -> 展示本地 Prompt 工程的基本信息（metafile）或拉取 PromptHub 上对应工程的信息
- ssprompt pull -> 拉取远端工程到本地项目中，相关工程可以引用 Prompt 文件或代码
- ssprompt list -> 展示当前版本 ssprompt 支持的命令
- ssprompt about -> 展示 ssprompt 的介绍和版本信息
- ssprompt version -> 展示 ssprompt 的版本信息

更多命令参数详情，请使用`ssprompt [command] -h`进一步了解

### Metafile 介绍

ssprompt 通过定义 prompt 工程的 Meta 文件来约束管理 Prompt 分发规则和内容  
ssprompt 关于 prompt 定义了四种类型的 Prompt

- Text
- Json
- Yaml
- Python

可以按需生成对应的 Prompt 上传到 PromptHub 进行分发  
metafile 以 Prompt 工程名称命名,如 prompt_project.yaml ，是 ssprompt 管理 Prompt 分发的关键

注：上述类型结合参考了 langchain 和 haystack

```yaml
#Prompt工程基础信息
meta:
  name: open #工程名称
  author:
    - ptonlix <baird0917@163.com>
  description: ""
  license: MIT #Prompt工程遵循的协议
  llm: #Prompt支持的LLM模型
    - gpt-3.5-turbo
  readme_format: md #Readme文件格式
  tag: #Prompt工程相关类型领域，如question-generation common为公共领域
    - common
  version: 0.1.0 #版本号

#Text类型的Prompt
text_prompt:
  dirname: text #目录名称, 默认为text

#Json类型的Prompt
json_prompt:
  dirname: json #目录名称，默认为json
  list: #支持多个json类型子工程
    - dependencies:
        langchain: 0.0.266 #json解析依赖的三方库版本号，如langchain等
      name: example #子工程名，对应生成工程目录名

#Yaml类型的prompt
yaml_prompt:
  dirname: yaml #目录名称，默认为yaml
  list: #支持多个yaml类型子工程
    - dependencies:
        langchain: 0.0.266 #yaml解析依赖的三方库版本号，如langchain等
      name: example #子工程名，对应生成工程目录名

#Python类型的Prompt
python_prompt: #目录名称，默认为yaml
  dirname: python #目录名称，默认为yaml
  list: #支持多个yaml类型子工程
    - dependencies:
        langchain: 0.0.266 #Python库引用的三方库版本号，如langchain等
      name: example #子工程名，对应生成工程目录名
```

#### 版本依赖规则

当前版本支持三种版本依赖规则

- Caret requirements
  - ^1.2.3
- Tilde requirements
  - ~1.2.3
- Wildcard requirements
  - 1.2.\*
- laster
  - 支持最新版本

## 🌊 PromptHub

目前 ssprompt 生成的 Prompt 工程，依赖 Git 管理，通过 Git 将 Prompt 工程上传到 Git 仓库以便 ssprompt 拉取引用

当前默认 PromptHub 托管在 GitHub [ptonlix/PromptHub](https://github.com/ptonlix/PromptHub)

目前 PromptHub 的 Prompt 工程还在持续建设中 🕜

后续会陆续收集和建设更多 Prompt 工程发布到我们 PromptHub ☁️

🍗 欢迎大家上传自己的 Prompt 到 PromptHub，共建一个开源的 Prompt 生态

#### GitHub Token

由于目前 GitHub API 请求访问限制，不采用 authentication 访问，会限制一个小时只能访问 60 次，导致使用 ssprompt 频繁拉取工程时存在 403 限制请求

**推荐在使用 ssprompt 时，设置 GitHub Personal access tokens 到环境变量**

```shell
export GITHUB_ACCESS_KEY=`Your GitHub Token`
```

## 🚩 Roadmap

- [x] 搭建 ssprompt 初步框架，完善基本功能
- [ ] 完善 ssprompt 命令
  - [x] pull 命令支持拉取特定类型 Prompt 工程到本地
  - [ ] show 命令支持展示更多 PromptHub 信息
- [ ] 搭建和完善 PromptHub
  - [ ] 收集全网优秀的 Prompt 案例，使用 ssprompt 构建工程并上传到 PromptHub
- [ ] ssprompt 网站与文档建设
  - [ ] ssprompt 说明文档
  - [ ] PromptHub 网站建设

## 🌏 项目交流讨论

<img height=240 src="https://img.gejiba.com/images/f0cf4242e87615dff574806169f9732a.png"/>

🎉 扫码联系作者，如果你也对本项目感兴趣，欢迎加入 ssprompt 项目群参与讨论交流。

## 💥 贡献

欢迎大家贡献力量，一起共建 ssprompt，您可以做任何有益事情

- 报告错误
- 建议改进
- 文档贡献
- 代码贡献  
  ...  
  👏👏👏
