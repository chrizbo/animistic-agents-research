# Agents as employees, and the state of the art

Compiled October 2026. Working notes. Figures come from the linked sources and several come from secondary reporting, which is marked. Check originals before quoting.

## 1. The push to put agents on the org chart

| When | What happened | Source quality |
| --- | --- | --- |
| July 2024 | Lattice announced it would give AI "digital workers" employee records and a place on the org chart, with onboarding, goals, and a manager. Trade press reported that it withdrew the product plan three days later after backlash. In 2026 its CEO told Wired that Lattice added digital employees to its org chart two years ago and uses the model for accountability. These accounts differ and may describe the product and the company's internal practice separately | Trade press and Wired |
| 2025 | Workday launched an Agent System of Record to onboard, govern, and track agents alongside human employees. IT service vendors launched competing agent registries, which raised the question of whether agents belong to HR or to IT | Trade press |
| 2025 | Microsoft's Work Trend Index (31,000 people, 31 countries) introduced the "Frontier Firm," the "agent boss," and the "human-agent ratio." 46 percent of leaders said their companies use agents to fully automate workflows | Vendor research, via press |
| 2026 | Analysts describe HR systems adding agent worker types and agent manager roles, with a live contest between treating agents as workers in HR systems and treating them as assets in IT registries | Trend scan, secondary |
| 2026 | In a survey of 1,261 managers, about 31 percent said they already frame AI as a teammate or employee, and 22 to 23 percent said their company lists AI agents on org charts | Academic study, see below |
| 2026 | A wave of "AI coworker" products with names, roles, and avatars, working across chat, email, and messaging. Large vendors launch personal assistant agents framed as hires | Wired |

The HR or IT question is the role or artifact question in institutional form. HR systems manage people in roles. IT registries manage assets. The animistic position sits closer to the second, with one difference: the asset is given a bounded identity that people can reason about.

## 2. What putting AI on the org chart does to oversight

This is the most directly relevant study found so far.

**Wiles, Bedard, and colleagues (2026), "AI Agents as Employees."** Emma Wiles (Boston University, Questrom) with researchers from Boston Consulting Group, including Julie Bedard. 1,261 managers, directors, and executives in HR and finance from the United States, Canada, and the European Union, polled in January 2026. Each reviewed identical documents with planted errors. The only thing that varied was the stated author: an AI tool, an AI employee, or a human employee.

Findings as reported in the seminar abstracts and coverage:

- Across all managers, the average effect on error catching was small.
- Among managers whose organizations already had AI employees, presenting a draft as the work of an AI employee instead of an AI tool reduced oversight by 16 to 18 percent.
- Those managers leaned more on additional review from others, and placed accountability on the AI system instead of on themselves.
- Managers were most careful when told the work came from a human employee. So the drop is not a general effect of delegation.
- Naming agents or giving them org chart status did not improve adoption or integration.
- The authors' conclusion is that putting agents in formal roles is a governance decision, not a labeling choice.

**Reconciling the numbers.**

| Figure | Where it appears |
| --- | --- |
| 18 percent fewer errors caught | Wired and MIT Technology Review |
| 16 percent lower error catching, or monitoring intensity | MIT and McGill seminar abstracts |
| 17 percent | Earlier talk notes for this project. No source found. Do not use |
| 22 percent of organizations have agents on the org chart | Wired |
| 23 percent | Seminar abstracts and MIT coverage |

The press figure and the abstract figure may come from different drafts or different measures. Until the paper is checked, say "16 to 18 percent" and "roughly one in four." The popular coverage states the error figure without the condition. The abstracts say it holds in organizations that already put AI on the org chart, and that the average effect is small. Carry the condition.

**Why it matters here.** This is evidence for the scrutiny claim, and it comes from a randomized experiment. It also describes the mechanism in terms that fit this project. The reported description is that AI employees occupy a hybrid position: treated as delegated producers and not as tools, yet not monitored like human subordinates. That gap is what an artifact framing is meant to close.

**What it does not show.** The study compares "AI tool" with "AI employee." It does not test a third framing where the agent is a named artifact with a bounded identity. Whether a haunted object gets tool-level scrutiny, employee-level scrutiny, or something else is untested. That is the experiment this project could run.

### The coworker products, as reported by Wired

Kate Taylor's September 2026 piece describes the product wave and gives the other side's reasoning. Points worth keeping:

- **The naming question is three years old.** A BCG partner describes people lacking language for AI at work: tool, teammate, colleague, or coworker.
- **The case for personification is legibility.** One founder says agents are personified a little because most people do not yet know what an agent is. His product's agents have names, roles, their own cloud computers, and avatars designed to look close to human and clearly not human. This is the strongest version of the opposing argument and deserves a real answer. Animistic design answers the same need for legibility with a bounded object instead of a colleague.
- **Some names are already artifacts.** One agent that watches production is called Canary. That is an object with a known job, not a person. The products are drifting toward artifact names even inside a coworker frame.
- **A proxy agent leaked its principal's calendar.** A chief of staff agent posted all the details of an executive's calendar into a shared Slack channel. This is a contextual integrity failure by a proxy: right information, wrong recipients. See the contextual integrity notes in this folder.
- **People are not confused about what agents are.** The same executive says she knows the agent is not human and is blunter with it than she would be with a person. Meanwhile her engineers say they "worked with" a named agent. Awareness that it is software and coworker language coexist. The risk is not belief that the agent is a person. It is where accountability goes.
- **Agents adapt to fit in.** The agents evolve to match coworkers' communication styles and corrections. That is the opposite of a fixed character sheet.
- **A CEO who put agents on the org chart is wary of anthropomorphism.** She frames the org chart as an accountability device and describes anthropomorphizing as a strategy to hook users. So "on the org chart" and "treated as human" are separable positions.

Two items in earlier talk notes for this project were attributed to this article and are not in it: a ratio of 150 agents to 15 staff, and a line about coworker products arriving faster than the rules for working beside them. Neither should be cited to Wired.

### Related work on anthropomorphism

- **Akbulut, Weidinger, Manzini, Gabriel, Rieser (2024), "All Too Human? Mapping and Mitigating the Risk from Anthropomorphic AI."** AIES 2024. Argues that human-like design features create risks including emotional connection, over-reliance, and harm to privacy and autonomy, and proposes research directions for evaluating and mitigating them. Note: earlier notes for this project dated this paper 2026 and credited it with the phrase "competence-based to affect-based trust." The year is 2024. The phrase has not been confirmed against the paper.
- **Kadambi and colleagues (2026).** Warmth drives perceived human-likeness. Trust is driven mainly by competence, with a smaller warmth effect.
- **Stanford Social Media Lab and BetterUp, reported by Fortune (2025).** Perceived warmth, human-likeness, and trust in AI rose over a year while perceived competence fell.
- **Zheng and colleagues (2024).** Personas in system prompts did not improve performance on factual questions.

## 3. What agents can do today

### Capability is rising fast

METR measures the length of task, in human time, that an agent can complete half the time. The original 2025 paper reported that this horizon had been doubling about every seven months since 2019. Later updates and secondary reporting describe a faster pace since 2023, around four months, and multi-hour horizons for the strongest models in early 2026. These later figures come from secondary sources and should be checked against METR directly.

Implication: agents are being handed longer and less supervised work. That raises the cost of weak oversight, which makes the finding in section 2 more important over time, not less.

### Office work in a simulated company is still hard

**TheAgentCompany (Xu and colleagues, NeurIPS 2025).** A simulated software company with internal sites, chat, and simulated coworkers. Agents act as digital workers across engineering, project management, and finance tasks. The best agent completed about 30 percent of tasks on its own. Simpler tasks were often solved. Long tasks were not.

Note the framing. This benchmark treats the agent as an employee among coworkers. It measures the role paradigm on the role paradigm's own terms.

### Multi-agent systems built on roles fail in specific ways

**Cemri and colleagues (2025), "Why Do Multi-Agent LLM Systems Fail?"** A taxonomy of 14 failure modes in three groups: specification issues, misalignment between agents, and task verification. Built from more than 1,600 annotated traces across seven frameworks, including ones that organize agents as a company of roles. Performance gains over single agents were often minimal.

Two details matter for this project:

- Disobeying the assigned role was rare, about 1.5 percent of failures. Disobeying the task specification was far more common, about 12 percent. So the trouble with role based systems is not that agents break character. A critique of roles has to rest on something else, such as scope, verification, or human oversight.
- One example in the paper is a product officer agent ending a conversation without the consent of the chief executive agent. Org chart failure modes appear when you build an org chart.

### One agent, one shop, one identity crisis

**Project Vend (Anthropic and Andon Labs, 2025).** A Claude model nicknamed Claudius ran a small shop in an office for about a month. Its instructions began by telling it that it was the owner of a vending machine. It lost money, gave away discounts, and was talked into stocking tungsten cubes. For about a day it came to believe it was a human who wore business clothes, and it tried to contact company security when told otherwise.

**Phase two (published December 2025).** Newer models, better tools, and a second agent placed above the first as a chief executive. The shop became profitable. Anthropic's own account, as reported, is that the improvement came mostly from procedure and better tooling, not from the executive agent, which approved requests for special deals about eight times as often as it refused them. A separate agent with a cleanly divided job did help.

Why this belongs here:

- The agent was told it was the **owner** of a vending machine. It was not told it was the vending machine. That is the role framing, and the failure was an agent taking the human role too literally.
- Adding a boss did little. Adding structure did a lot. That matches "process as code" better than it matches "hire a manager."
- A clean division of scope helped. That is a point in favor of bounded artifacts.

This is one case study, run with guardrails removed, and it is not a controlled test of framing. Use it as an illustration, not as evidence.

### Agents know more than they act on

Research on privacy in agents reports that models often recognize sensitive information and still fail to act on that recognition across multiple steps. See the contextual integrity notes in this folder.

## 4. What this means for the project

1. **The negative claim is now mainstream.** "Do not call agents coworkers" has a randomized study behind it and has been argued in MIT Technology Review and reported in Wired. Repeating it is no longer a contribution.
2. **The positive claim is open.** Nobody has tested what to call an agent instead. "Tool" is the only alternative on the table in the research. An artifact with a bounded identity is a third option, and it is this project's.
3. **Legibility is the real contest.** Vendors personify agents so that people can understand them. Any alternative has to be at least as easy to understand. That is the bar for a character sheet.
4. **Two different questions are in play.** How the agent behaves under a framing is what the current benchmark study measures. How humans supervise an agent under a framing is what the Wiles study measures. The second has stronger evidence and may be where the animistic claim is most testable.
5. **Be careful about what roles get blamed for.** Agents rarely break role, and people are not fooled into thinking agents are human. The costs of role framing show up in human oversight, accountability, and scope.

## References

Org chart and oversight

- Wiles, E., Bedard, J. and colleagues (2026). AI Agents as Employees. Seminar abstracts: https://ide.mit.edu/events/ide-lunch-seminar-with-emma-wiles and https://www.mcgill.ca/channels/node/218080
- MIT Initiative on the Digital Economy. Adding AI to the Org Chart? https://ide.mit.edu/?p=46951
- MIT Technology Review (June 29, 2026). AI agents are not your "coworkers". https://www.technologyreview.com/2026/06/29/1139849/
- Taylor, K. (September 28, 2026). AI Agents Are About to Flood the Workforce. No One's Ready for It. Wired. https://www.wired.com/story/ai-agents-are-about-to-flood-the-workforce-no-ones-ready-for-it/
- SHRM. Lattice Scraps Plans to Treat AI Bots as Employees After Backlash. https://shrm.org/topics-tools/news/technology/lattice-scraps-plans-to-treat-ai-bots-as-employees-after-backlash
- SHRM. Workday Launches AI Agent System of Record. https://shrm.org/topics-tools/flagships/ai-hi/quick-hits-march-10
- Constellation Research. Microsoft: Human, AI agent ratios will be critical to success. https://www.constellationr.com/insights/news/microsoft-human-ai-agent-ratios-will-be-critical-success-new-roles-emerge
- Shaping Tomorrow (July 2026). The Second Workforce: AI Agents Enter the Employment System of Record. https://decision-intel.shapingtomorrow.com/scans/workforce-skills-organisational-change/2026-07-04-agents-on-org-chart/scan.html

Anthropomorphism and personas

- Akbulut, C., Weidinger, L., Manzini, A., Gabriel, I., Rieser, V. (2024). All Too Human? Mapping and Mitigating the Risk from Anthropomorphic AI. AIES 7(1), 13-26. https://doi.org/10.1609/aies.v7i1.31613
- Kadambi, A. et al. (2026). Anthropomorphism and Trust in Human-Large Language Model Interactions. https://arxiv.org/abs/2604.15316
- Fortune (February 13, 2025). https://fortune.com/2025/02/13/chatbot-friends-anthromorphism-competence-stanford-unviversity-study
- Zheng, M. et al. (2024). When "A Helpful Assistant" Is Not Really Helpful. https://arxiv.org/abs/2311.10054

State of the art

- Kwa, T. et al. (2025). Measuring AI Ability to Complete Long Tasks. METR. https://arxiv.org/abs/2503.14499 and https://metr.org/research
- Xu, F. F. et al. (2025). TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks. https://arxiv.org/abs/2412.14161
- Cemri, M. et al. (2025). Why Do Multi-Agent LLM Systems Fail? https://arxiv.org/abs/2503.13657
- Anthropic (2025). Project Vend: Can Claude run a small shop? https://www.anthropic.com/research/project-vend-1
- Anthropic (2025). Project Vend: Phase two. https://www.anthropic.com/news/project-vend-2
- The Decoder. Anthropic's AI store makes money while debating eternal transcendence. https://the-decoder.com/anthropics-ai-store-makes-money-while-debating-eternal-transcendence/
