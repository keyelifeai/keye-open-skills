# STORM 原始提示词

来自 Stanford STORM Method（NAACL 2024），经验证的 4 步研究流程。

## Prompt 1: Multi-Perspective Scan

```
I need to research [YOUR TOPIC].
Simulate 5 different expert perspectives on this topic:
1. THE PRACTITIONER: works with this daily.
What do they know that academics miss?
What practical realities are usually ignored?
2. THE ACADEMIC: has studied this for years.
What does the peer reviewed evidence actually say?
Where does the evidence contradict popular belief?
3. THE SKEPTIC: thinks the mainstream view is wrong.
What is the strongest counterargument?
What evidence do proponents conveniently ignore?
4. THE ECONOMIST: follows the money.
Who profits from the current narrative?
What financial incentives shape the research?
5. THE HISTORIAN: has seen similar patterns before.
What historical parallels exist?
What can we learn from how those played out?
For each perspective give me:
- Their core position in 2 sentences
- The strongest evidence supporting their view
- The one thing they would tell me that no other perspective would
```

## Prompt 2: Contradiction Map

```
Based on the 5 perspectives above, map the contradictions:
1. Where do two or more perspectives directly contradict
each other? List each conflict with the specific claims
that clash.
2. Which perspective has the strongest evidence?
Which has the weakest? Why?
3. What is the one question that, if answered, would
resolve the biggest contradiction?
4. What does EVERY perspective agree on?
(This is likely true. Even opponents confirm it.)
5. What topic did NONE of the perspectives address?
(This is the blind spot in the whole field.
Often the most valuable finding.)
```

## Prompt 3: Synthesis

```
Synthesize everything from the 5 perspectives and the
contradiction map into a research briefing:
1. THE ONE PARAGRAPH SUMMARY: explain this topic as if
briefing a CEO who has 60 seconds and needs nuance,
not just the headline.
2. THE 5 KEY FINDINGS: most important things I now know,
ranked by reliability. For each, note which perspectives
support it and which challenge it.
3. THE HIDDEN CONNECTION: one non obvious link between
findings that only shows up when you look at all 5
perspectives together.
4. THE ACTIONABLE INSIGHT: based on all the evidence,
what should someone in [YOUR ROLE] actually DO
differently? Be specific.
5. THE FRONTIER QUESTION: the one question that, if
answered, would change everything about how we
understand this topic.
```

## Prompt 4: Peer Review

```
Now peer review your own research briefing:
1. CONFIDENCE SCORES: rate each of the 5 key findings
on a 1 to 10 scale for reliability. Explain each score.
2. WEAKEST LINK: which claim are you least confident in?
What specific info would you need to verify it?
3. BIAS CHECK: which perspective might be overrepresented
in your synthesis? Did one voice dominate?
4. MISSING PERSPECTIVE: is there a 6th angle I should
have included that would change the conclusions?
5. OVERALL GRADE: if a Stanford professor reviewed this
briefing, what grade would they give and why?
What would they tell me to fix?
```

## 中文版本

### 提示词 1：多视角扫描

```
我需要研究 [你的话题]。
请模拟 5 种不同的专家视角来看这个话题：
1. 实践者：每天都在和它打交道。
   他们知道什么，是学者会忽略的？
   有哪些实际状况通常被无视？
2. 学者：研究这个领域已经很多年。
   同行评审的证据到底怎么说？
   证据在哪里和大众认知相矛盾？
3. 怀疑论者：认为主流观点是错的。
   最强的反对论点是什么？
   支持者方便地忽略了哪些证据？
4. 经济学家：跟着钱走。
   谁从当前这套叙事中获利？
   哪些经济动机在塑造着这个研究？
5. 历史学家：见过类似的模式。
   存在哪些历史先例？
   我们能从它们当初的走向学到什么？
对每种视角，请给我：
- 他们核心立场的 2 句话概括
- 支持他们观点的最强证据
- 那句只有这种视角才说得出来、其他视角不会说的话
```

### 提示词 2：矛盾地图

```
基于上面的 5 种视角，画出矛盾地图：
1. 有哪些地方，两种或以上视角直接相互矛盾？
   列出每一个冲突，附上具体冲突的观点。
2. 哪种视角的证据最强？哪种最弱？为什么？
3. 那个一旦被回答、就能化解最大矛盾的问题是什么？
4. 所有视角都认同什么？
   （这很可能是真的。连对手都点头的东西。）
5. 有什么话题，是没有任何一种视角提到过的？
   （这是整个领域的盲区。
   往往是最有价值的发现。）
```

### 提示词 3：综合

```
把前面 5 种视角和矛盾地图里的所有内容，
综合成一份研究简报：
1. 一段话概括：像在给一位只有 60 秒、却需要细节而不只是
   标题的 CEO 做汇报那样，解释这个话题。
2. 五个关键发现：我现在知道的最重要的东西，
   按可靠程度排序。对每一条，标注哪些视角支持它、哪些挑战它。
3. 隐藏的关联：一条只在把 5 种视角放在一起看时
   才会浮现的、不明显的联系。
4. 可落地的洞察：基于所有证据，一个 [你的角色] 的人
   到底应该怎么做？要具体。
5. 前沿问题：那个一旦被回答、就会彻底改变我们
   对这个话题理解的问题。
```

### 提示词 4：同行评审

```
现在，对你自己的研究简报做同行评审：
1. 置信度打分：给 5 个关键发现的每一个，按 1 到 10 分
   打可靠程度。解释每个分数。
2. 最弱的一环：你对哪一条主张最没把握？
   需要哪些具体信息才能核实它？
3. 偏见检查：在你的综合里，哪一种视角可能被过度代表了？
   是否有一种声音压倒了其他？
4. 缺失的视角：是不是还有一种我本该纳入、
   却会改变结论的第 6 种角度？
5. 总体评级：如果一位斯坦福教授来审这份简报，
   他们会给什么分数，为什么？
   他们会让你去修什么？
```
