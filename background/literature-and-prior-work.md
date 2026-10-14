# Literature and prior work

Compiled October 2026. Working notes, not a finished review. Summaries are paraphrased from the sources linked at the end. Check the originals before quoting.

## The claim in one paragraph

Most agents are written as roles: "you are a customer service rep." This project asks whether writing an agent as an artifact works better: "you are an order kiosk, a machine that protects the order ledger." The intuition is that organizations already treat their artifacts as if they act. The roadmap resists. The budget says no. The idea has roots in three places: a design tradition called animistic design, a sociological tradition called actor-network theory, and a decade of workshops where people roleplayed as devices.

## 1. Animistic design

| Source | What it argues | Why it matters here |
| --- | --- | --- |
| Van Allen, McVeigh-Schultz, Brown, Kim, Lara (2013), *AniThings: animism and heterogeneous multiplicity* | Early prototype work with several distinct digital things, each with its own point of view, instead of one unified assistant | The first appearance of "many small spirits" over "one big helper" |
| Marenko and van Allen (2015, 2016), *Animistic design: how to reimagine digital interaction between the human and the nonhuman* | Proposes animistic design as a strategy for living with digital things. Explicitly rejects the anthropomorphic and the cute. Treats uncertainty and unpredictability as creative material. Favors multiple protagonists with different and even conflicting perspectives | The founding text. Note that it is anti-anthropomorphic, which supports the artifact over role distinction |
| Marenko (2014), *Neo-animism and design* | The philosophical groundwork, drawing on thing theory and the lives of objects | Theory lineage |
| Van Allen (2017), *Reimagining the Goals and Methods of UX for ML/AI* | Position paper arguing ML and AI systems need different UX goals than web or mobile products | The bridge from smart objects to AI systems |
| Rozendaal (2016) and Rozendaal, Boon, Kaptelinin (2019), *Objects with Intent* | Everyday things given a purpose: a lamp that wants you to sleep well, a jacket that wants you calm. Frames them as collaborative partners | Closest design precedent to "what does it protect" |
| Giaccardi, Cila, Speed, Caldwell (2016), *Thing Ethnography* and *Things as Co-Ethnographers* | Studying practices from the perspective of the things involved. Related work by Cila and colleagues studies object personas | A method precedent for character sheets written from the thing's side |
| Seymour and Van Kleek (2020), *Does Siri Have a Soul?* | Design fiction that reimagines voice assistants as kami living inside objects, to make familiar design patterns strange again | Shows the animistic lens used as a critical tool on assistants |
| Lewis, Arista, Pechawis, Kite (2018), *Making Kin with the Machines* | Indigenous epistemologies already have protocols for relating to nonhuman kin, and are better equipped for AI than frameworks that put humans at the center | The ethical anchor. "Spirits" and "haunted" are borrowed language and should be used with care and credit |
| Rozendaal, Marenko, Odom, eds. (2021), *Designing Smart Objects in Everyday Life* | Book length collection on intelligences, agencies, and ecologies of smart objects | Further reading |

**A tension to take seriously.** Marenko and van Allen value animism because it invites uncertainty and unpredictability. This study hypothesizes that animistic framing makes agents more consistent. Those pull in opposite directions. Either the hypothesis is a departure from the source tradition, or the two are talking about different layers: unpredictability in how humans imagine with a thing, consistency in how the thing holds its boundaries. The talk and the paper should say which.

## 2. Actor-network theory and its neighbors

| Source | Core idea | Memorable example |
| --- | --- | --- |
| Latour (1988, credited to Jim Johnson), *Mixing Humans and Nonhumans Together: The Sociology of a Door-Closer* | We delegate work and even morality to nonhumans. Artifacts in turn prescribe behavior back to us | A sign on a door saying the automatic door-closer is on strike |
| Latour (1992), *Where Are the Missing Masses? The Sociology of a Few Mundane Artifacts* | Sociology cannot balance its accounts without counting artifacts. Seat belts, door-closers, and keys are the missing mass that holds society together | The seat belt that will not let the car start |
| Callon (1986), *Some elements of a sociology of translation* | Networks form through four moments: problematisation, interessement, enrolment, mobilisation. Humans and nonhumans are analyzed with the same vocabulary. Spokespersons can be betrayed by those they speak for | Scallops that refuse to anchor where the scientists need them to |
| Akrich (1992), *The De-Scription of Technical Objects* | Designers inscribe a vision of the world and its users into an object. That inscription is a script. Use in the real world de-scribes it | The script as an instruction manual built into the artifact |
| Star and Griesemer (1989), *Institutional Ecology, Translations and Boundary Objects* | Boundary objects are plastic enough to adapt to each group and robust enough to keep a common identity. Four types: repositories, ideal types, coincident boundaries, standardized forms | Specimens, field notes, and maps shared by amateurs and professionals at a museum |
| Dennett (1971, 1987), *The Intentional Stance* | Three ways to predict a system: physical stance, design stance, intentional stance. We treat something as having beliefs and goals when that predicts its behavior well | The thermostat |

### How the ideas map onto an animistic agent

| Concept | In an organization | Character sheet field |
| --- | --- | --- |
| Delegation (Latour) | The work a team has handed to an artifact, such as a checklist that enforces review | Artifact name |
| Obligatory passage point (Callon) | The thing everyone must go through, such as the ledger or the release gate | What I protect |
| Script and prescription (Akrich, Latour) | The behavior the artifact demands of people. A system prompt is an inscription in exactly this sense | What I resist |
| Boundary object (Star and Griesemer) | Strategy docs, decision records, and status reports that mean different things to different teams and still hold together | What I remember |
| Spokesperson and betrayal (Callon) | An agent speaks for the artifact. It can misrepresent it | My blind spot |
| Intentional stance (Dennett) | Choosing to describe the artifact as wanting something because that predicts it well | Mood grid |

**Where the mapping strains.** Actor-network theory is a way of describing networks, not a recipe for designing agents. Its actants need no inner life, and a strict reading would resist talk of spirits. The honest framing is that ANT explains why artifact scoped agents feel natural in organizations. It does not predict that they perform better. That part is an empirical question, which is why this repo exists.

One more distinction worth keeping. Dennett noted a possible fourth stance above the intentional one, where a system is treated as a person. Role based agents with names and job titles invite that personal stance. Animistic agents ask for the intentional stance only, held in check by the design stance.

## 3. What existing evidence says about personas and trust

The fuller account, including the study of managers reviewing work from an "AI employee," is in [agents-as-employees-and-state-of-the-art.md](agents-as-employees-and-state-of-the-art.md). In short:

- **Personas in system prompts.** Zheng and colleagues found that adding a persona did not improve performance on factual questions, with the effect of any given persona close to random. An earlier version of the same paper had reported the opposite. A null result on raw task completion between framings is the expected baseline, and it matches this repo's preliminary pass@1 numbers.
- **Anthropomorphism and trust.** Kadambi and colleagues found that warmth drives perceived human-likeness while trust is driven mainly by competence. A longitudinal survey reported by Fortune found trust rising while perceived competence fell.
- **Scrutiny.** Wiles and colleagues ran a randomized experiment with 1,261 managers. In organizations that already put AI on the org chart, work labeled as coming from an AI employee got less oversight than the same work labeled as coming from an AI tool. This is the strongest evidence for the claim that role framing lowers human scrutiny. It compares employee with tool. It does not test an artifact framing.

## 4. Prior work this project grew out of

| Year | Work | What carried forward |
| --- | --- | --- |
| 2017 | *Robots need love too: Empathy Mapping for AI* (UX Collective, written at Philosophie) | An empathy map for a machine: what it does, senses, says, thinks, feels. Also the warning that an agent given too many jobs should be split into specialists |
| 2021 | *Communal Computing* series (O'Reilly Radar) | Home devices are built for one owner and live in shared spaces. Five problem areas: identity, privacy, security, experience, ownership |
| 2022 | SXSW workshop and the article *How does the Roomba really feel about dog poop?!* | Animistic design mapping plus roleplay. Worksheets gave each device a name, traits, a superpower, and emotional triggers. Shortlisted for the 2023 Interaction Design Awards |
| later | *A smart home is one that talks to itself* (UX Collective) and a Replit prototype | Devices with bounded identities negotiating in a shared channel, using an LLM to voice them |
| 2026 | *Agentics Beyond Code* (open source) | The philosophy "Artifacts over Roles": scope each workflow to the artifact it produces, not the role it replaces. Animate the artifact, not the job title. The agent drafts and the team decides |
| 2026 | Foo Camp roleplay session (June) | Character sheets for home devices, then roleplaying how they act together. The discussion prompted this study |
| 2026 | This repo | Character sheet to system prompt, tested against role based prompts |

**The character sheet has a lineage.** Five quadrants in 2017. Name, traits, superpower, and emotions in 2022. Artifact, protects, remembers, resists, blind spot, and mood grid in 2026. Each version moved away from personality and toward boundaries.

## 5. Open questions

1. **Uncertainty or consistency?** The source tradition prizes unpredictability. The hypothesis here is consistency. See the tension noted in section 1.
2. **Is the mood grid anthropomorphism by the back door?** A kiosk that is "afraid" before a one-shot operation is a useful trigger. It is also an emotion. Preliminary results suggest the mood triggers did not help and may have caused over-confirmation.
3. **Does the benchmark test the claim?** The study uses a customer service benchmark. The organizational claim is about roadmaps, releases, and decision records. Those are different settings and the gap should be named.
4. **Does an artifact framing change human scrutiny?** Employee framing lowers oversight compared with tool framing in at least one randomized study. Where a bounded artifact falls between those two is untested. This may matter more than task performance.
5. **What happens when artifacts negotiate with each other?** The roleplay sessions simulate this with people. Nothing in this repo tests it with agents yet.
6. **Borrowed language.** Animism is a living practice for many people. Credit the sources and avoid treating it as a gimmick.

## References

Animistic design

- Marenko, B. and van Allen, P. (2016). Animistic design: how to reimagine digital interaction between the human and the nonhuman. *Digital Creativity* 27(1), 52-70. https://doi.org/10.1080/14626268.2016.1145127 (open copy: https://ualresearchonline.arts.ac.uk/id/eprint/9065/)
- Marenko, B. and van Allen, P. (2015). Reimagining Interaction Through Animistic Design. Participatory Innovation Conference. https://pin-c.sdu.dk/assets/reimagining-interaction-through-animistic-design---betti-marenko%2c-philip-van-allen---492-499---pinc-2015.pdf
- Marenko, B. (2014). Neo-animism and design. *Design and Culture*.
- Van Allen, P., McVeigh-Schultz, J., Brown, B., Kim, H. M., Lara, D. (2013). AniThings: animism and heterogeneous multiplicity. CHI Extended Abstracts, 2247-2256.
- Van Allen, P. (2017). Reimagining the Goals and Methods of UX for ML/AI. AAAI Spring Symposia. https://www.academia.edu/35538774/Reimagining_the_Goals_and_Methods_of_UX_for_ML_AI
- Rozendaal, M. (2016). Objects with intent: a new paradigm for interaction design. *Interactions* 23(3), 62. https://interactions.acm.org/archive/view/may-june-2016/objects-with-intent-A-new-paradigm-for-interaction-design
- Rozendaal, M., Boon, B., Kaptelinin, V. (2019). Objects with Intent: Designing Everyday Things as Collaborative Partners. *ACM Transactions on Computer-Human Interaction* 26(4).
- Giaccardi, E., Cila, N., Speed, C., Caldwell, M. (2016). Thing Ethnography: Doing Design Research with Non-Humans. DIS '16, 377-387. https://research.tudelft.nl/en/publications/thing-ethnography-doing-design-research-with-non-humans/
- Giaccardi, E., Speed, C., Cila, N., Caldwell, M. (2016). Things as Co-Ethnographers. In *Design Anthropological Futures*. Bloomsbury.
- Seymour, W. and Van Kleek, M. (2020). Does Siri Have a Soul? Exploring Voice Assistants Through Shinto Design Fictions. CHI Extended Abstracts. https://arxiv.org/abs/2003.03207
- Lewis, J. E., Arista, N., Pechawis, A., Kite, S. (2018). Making Kin with the Machines. *Journal of Design and Science*. https://jods.mitpress.mit.edu/pub/lewis-arista-pechawis-kite/release/1
- Rozendaal, M., Marenko, B., Odom, W., eds. (2021). *Designing Smart Objects in Everyday Life: Intelligences, Agencies, Ecologies*. Bloomsbury.

Actor-network theory and neighbors

- Latour, B., credited to Jim Johnson (1988). Mixing Humans and Nonhumans Together: The Sociology of a Door-Closer. *Social Problems* 35, 298-310. http://www.bruno-latour.fr/node/279.html
- Latour, B. (1992). Where Are the Missing Masses? The Sociology of a Few Mundane Artifacts. In Bijker and Law, eds., *Shaping Technology/Building Society*. MIT Press, 225-259. http://www.bruno-latour.fr/node/258.html
- Callon, M. (1986). Some elements of a sociology of translation: domestication of the scallops and the fishermen of St Brieuc Bay. In Law, ed., *Power, Action and Belief*. Routledge, 196-223.
- Akrich, M. (1992). The De-Scription of Technical Objects. In Bijker and Law, eds., *Shaping Technology/Building Society*. MIT Press, 205-224.
- Star, S. L. and Griesemer, J. R. (1989). Institutional Ecology, 'Translations' and Boundary Objects. *Social Studies of Science* 19(3), 387-420. https://doi.org/10.1177/030631289019003001
- Dennett, D. (1987). *The Intentional Stance*. MIT Press. Overview: https://en.wikipedia.org/wiki/Intentional_stance

Personas and trust

- See [agents-as-employees-and-state-of-the-art.md](agents-as-employees-and-state-of-the-art.md) for the full list.
- Zheng, M., Pei, J., Logeswaran, L., Lee, M., Jurgens, D. (2024). When "A Helpful Assistant" Is Not Really Helpful. Findings of EMNLP. https://arxiv.org/abs/2311.10054
- Kadambi, A. et al. (2026). Anthropomorphism and Trust in Human-Large Language Model Interactions. https://arxiv.org/abs/2604.15316

Prior work

- Butler, C. (2017). Robots need love too: Empathy Mapping for AI. https://uxdesign.cc/robots-need-love-too-empathy-mapping-for-ai-59585ad3548d
- Butler, C. (2021). Communal Computing. O'Reilly Radar. https://www.oreilly.com/radar/communal-computing/
- Butler, C. (2022). How does the Roomba really feel about dog poop?! https://uxdesign.cc/how-does-the-roomba-really-feel-about-dog-poop-c590bcfb8834
- Butler, C. A smart home is one that talks to itself. https://uxdesign.cc/a-smart-home-is-one-that-talks-to-itself-58bb9222d893
- Butler, C. (2026). Agentics Beyond Code. https://github.com/chrizbo/agentics-beyond-code
