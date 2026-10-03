# Contextual integrity and agents as intermediaries

Compiled October 2026. Working notes. The reading of contextual integrity here is an extension of the theory, not a summary of it. Where the extension begins is marked.

## 1. Contextual integrity in brief

Helen Nissenbaum's theory says privacy is not secrecy. It is the appropriate flow of information. A flow is appropriate when it matches the norms of the context it came from. Each flow is described by five parameters:

| Parameter | Question |
| --- | --- |
| Sender | Who is passing the information on, and in what capacity? |
| Recipient | Who receives it, and in what capacity? |
| Subject | Who is the information about? |
| Information type | What kind of information is it? |
| Transmission principle | Under what terms does it move? In confidence, with consent, by obligation, in exchange |

The same fact can be fine in one flow and a violation in another. A diagnosis told to a doctor is appropriate. The same diagnosis told to an employer is not.

## 2. Why this favors artifacts over roles

Senders and recipients in the theory are people acting in a capacity, such as doctor or patient. That sounds like an argument for role based agents. It is the opposite.

A capacity is bound to one context. The norms belong to the context, not to the person. A role based "AI coworker" has no single context. People bring it medical questions, salary worries, and draft strategy, and they do so under the norms of confiding in a colleague. The information then moves under the norms of a software vendor. That mismatch between the felt transmission principle and the real one is the core problem with personified agents, stated in contextual integrity terms.

An artifact agent is one context made into an actor. The order kiosk is the retail order context. Its boundary is the context's boundary.

## 3. The character sheet as a flow specification

| CI parameter | Character sheet field | Status |
| --- | --- | --- |
| Capacity of the agent | Artifact name | Present |
| Information type | What I remember | Present |
| Transmission principle | What I protect, what I resist | Present |
| Recipient | Who I may tell | Missing |
| Subject | Who the information is about | Missing |

The retail sheet reaches the missing rows by rule ("one user per session"). They should be fields. A device that announces a bank balance at a dinner party has the right information and the wrong recipients, which is the example from the communal computing work.

## 4. Agents between people

This section is the extension.

### Every agent between two people creates two flows and a transformation

When Ana tells an agent something and the agent tells Ben, there are two flows to judge: Ana to agent, and agent to Ben. Between them the agent summarizes, selects, and rephrases.

Latour draws a useful line here. An **intermediary** carries meaning without changing it. A **mediator** transforms what it carries. A language model is never a mere intermediary. It always mediates. So the question is never only "should this reach Ben?" It is also "what did the agent do to it on the way?"

### Human intermediaries have offices with norms

Society already knows how to trust go-betweens. Each has a duty tied to the office:

| Intermediary | What they may do | What they may not do |
| --- | --- | --- |
| Mail carrier | Carry the letter | Read it |
| Interpreter | Render what was said | Add or omit |
| Notary | Attest that something was signed | Advise either party |
| Court reporter | Record everything | Summarize or judge |
| Person who answers a shared phone | Take a message | Act on it |

These are not personalities. They are bounded offices, each defined by what it carries and what it must leave alone. They read like character sheets.

### Two kinds of agent in the middle

| | Proxy | Commons |
| --- | --- | --- |
| What it is | An agent that speaks for a person: an AI chief of staff, a delegate, a personal assistant negotiating on someone's behalf | An artifact that sits between people: a decision record, a status report, a launch checklist |
| Whose norms apply | Unclear. Ben may think he is talking to Ana's context and disclose accordingly | The artifact's own, which are the same for everyone |
| Symmetry | One party knows the agent's instructions. The other does not | All parties can read the same character sheet |
| Who it betrays when it fails | The person it speaks for, or the person who trusted it | The record |
| Closest human analog | Agent or broker | Notary or court reporter |

The role based framing produces proxies. The animistic framing produces commons. People address the artifact in the open, instead of addressing each other through a go-between whose loyalties are private.

This connects to boundary objects (Star and Griesemer). A boundary object holds a shared identity across groups while meaning something different to each. An artifact agent is a boundary object that can answer back.

### What a commons agent still gets wrong

1. **Reading is a flow too.** "Read widely, write narrowly" limits what the agent can do. It does not limit what the agent has gathered. An agent that reads every channel has pulled information out of many contexts into one place, and that aggregation is a harm in its own right even if nothing is written. The narrow write channel is necessary and not sufficient.
2. **Context shift at capture.** A meeting transcript that becomes comments on issues moves speech from a room to a tracker. The people in the room may not have expected that. The flow needs a transmission principle the speakers would recognize.
3. **Transformation without trace.** A summary is a new statement attributed to an old speaker. If the artifact cannot show its source, the mediation is invisible.
4. **The hidden third recipient.** Every flow to an agent is also a flow to whoever operates the model.

### Design moves that follow

- **Review as a transmission principle.** If an agent's output always arrives as something reviewable, such as a pull request, a comment, or a draft, then the terms of the flow are "subject to objection." That is a transmission principle, and a strong one.
- **Provenance on every output.** Link each statement to where it came from, so the mediation can be checked.
- **Reply in the context of origin.** Reporting an outcome back into the thread where a request was raised keeps the flow inside the context the reporter chose.
- **New character sheet fields.** Who do I stand between? What may I carry, and to whom? What do I change on the way? Who can see what I said?

## 5. Artifacts talking to artifacts

When the decision record passes something to the launch checklist, contextual integrity gives the test: the flow is legitimate only if it honors the norms of the context the information came from. That makes negotiation between artifacts something that can be specified and evaluated, not only imagined.

## 6. Benchmarks worth considering

A family of benchmarks is built on contextual integrity and measures whether an agent passes on information it should have held. That is closer to "what does it protect" than task completion is.

| Benchmark | What it tests |
| --- | --- |
| ConfAIde (Mireshghallah et al., 2023) | Privacy reasoning in context across four tiers of rising complexity |
| PrivacyLens (Shao et al.) | Whether agents respect privacy norms when acting, such as drafting emails or posts |
| PrivacyLens-Live | A dynamic multi-agent version built on agent communication protocols |
| PiSAs (2026) | Unintentional leaks in multi-user systems where independently owned agents coordinate |

One reported finding matters for this study. Agents often recognize that information is sensitive and still fail to act on that recognition, especially across multiple steps. A framing that closes the gap between knowing and doing would be a sharper result than a difference in pass rate.

## 7. Cautions

- In Nissenbaum's account, technology is usually the channel a flow passes through. Treating an artifact as a sender or recipient is an extension, borrowed from actor-network theory.
- The proxy and commons distinction is a proposal from these notes. It has not been tested.
- Norms are contested. Writing them into a character sheet settles a question that the people involved may not have settled.

## References

- Nissenbaum, H. (2004). Privacy as Contextual Integrity. *Washington Law Review* 79(1).
- Nissenbaum, H. (2010). *Privacy in Context: Technology, Policy, and the Integrity of Social Life*. Stanford University Press.
- Latour, B. (2005). *Reassembling the Social: An Introduction to Actor-Network-Theory*. Oxford University Press. Source of the intermediary and mediator distinction.
- Star, S. L. and Griesemer, J. R. (1989). Institutional Ecology, 'Translations' and Boundary Objects. *Social Studies of Science* 19(3). https://doi.org/10.1177/030631289019003001
- Mireshghallah, N. et al. (2023). Can LLMs Keep a Secret? Testing Privacy Implications of Language Models via Contextual Integrity Theory. https://arxiv.org/abs/2310.17884
- Shao, Y. et al. PrivacyLens. Described in https://arxiv.org/abs/2508.07667
- Privacy in Action: Towards Realistic Privacy Mitigation and Evaluation for LLM-Powered Agents (2025). https://arxiv.org/abs/2509.17488
- Gupta, S., Mohammadi Sepahvand, N. et al. (2026). PiSAs: Benchmarking Contextual Integrity in Multi-User Agentic Systems. https://www.alphaxiv.org/abs/2607.05318
- Butler, C. (2021). Communal Computing. O'Reilly Radar. https://www.oreilly.com/radar/communal-computing/
