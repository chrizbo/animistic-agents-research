# Pareidolia and anthropomorphism

Compiled October 2026. Working notes. Face pareidolia is research on visual perception. Applying it to language agents is an analogy, and that is marked where it happens.

## 1. What pareidolia research shows

Face pareidolia is seeing a face in an object that has none: an electrical outlet, the front of a car, a piece of toast.

| Finding | Source | Confidence |
| --- | --- | --- |
| Illusory faces are at first represented in the brain more like real faces than matched objects are. Within about 250 milliseconds the representation shifts and they are treated like ordinary objects | Wardle, Taubert, Teichmann, Baker (2020) | Read from abstract |
| The authors interpret this as a broadly tuned face detector that favors sensitivity over selectivity. It fires first and is corrected after | Same | Read from abstract |
| An illusory face is perceived as both an object and a face | Same | Read from paper text |
| People read age, emotion, and gender into illusory faces. Many more are perceived as male than female. The bias holds for male and female viewers and in black and white images | Wardle, Paranjape, Taubert, Baker (2022) | Via coverage and author interview |
| Other primates also experience face pareidolia | Reported in coverage of the same group's work | Via coverage |
| Illusory faces are found faster in visual search than matched objects | Follow-up work by the same group | Via excerpt |

## 2. The neighboring research on seeing minds

Pareidolia is about faces. The broader question, why people attribute minds to nonhumans, has its own literature.

**Three factors (Epley, Waytz, Cacioppo, 2007).** Anthropomorphism varies with three things:

| Factor | Meaning | In an organization |
| --- | --- | --- |
| Elicited agent knowledge | We reason about an unknown thing using what we know about humans, because that knowledge is the most available | A name, a title, and an avatar make human knowledge the obvious template |
| Effectance motivation | The need to understand and predict. We explain erratic things by giving them minds | An agent that behaves inconsistently invites a person-shaped explanation |
| Sociality motivation | The need for connection | Coworker framing answers this need directly |

**Unpredictability increases anthropomorphism (Waytz, Morewedge, Epley, Monteleone, Gao, Cacioppo, 2010).** Unpredictable gadgets drew more attributions of human mental states than predictable ones, and anthropomorphizing in turn satisfied the need to make sense of them.

**Older and related ideas, cited from general knowledge and not rechecked for these notes:**

- Heider and Simmel (1944). People watching simple shapes move describe them as having intentions and personalities.
- Guthrie (1993), *Faces in the Clouds*. Argues that animism and anthropomorphism are a perceptual bet. When something is ambiguous, guessing that it is alive or humanlike is the safer error.
- Reeves and Nass (1996), *The Media Equation*. People apply social rules to computers while knowing they are computers.
- Weizenbaum's observations about ELIZA. People attributed understanding to a very simple conversational program.

## 3. What this implies for agent framing

1. **Animation is not optional.** The detector fires before reflection. People will see something in an agent whether or not the designer intends it. The design choice is what cue to supply, not whether to supply one.
2. **Knowing it is software does not turn it off.** An illusory face is seen as object and face together. That matches reports of people who state plainly that an agent is not human and still talk about working with it. The hybrid position described in studies of "AI employees" is ordinary perception, not confusion.
3. **Small cues carry a large payload.** If two dots and a line bring perceived gender and emotion with them, a name and an avatar bring the whole schema of a colleague, including assumptions about who is accountable. An artifact name brings a different schema: what a checklist or a ledger does.
4. **Legibility is the real reason vendors personify.** Elicited agent knowledge explains it. The human template is the cheapest way to make an unfamiliar thing understandable. Any alternative has to supply a template that is just as easy to pick up.
5. **Consistency and personification are linked.** This is the most useful connection for this repo. If unpredictability increases anthropomorphism, then an agent's behavioral consistency is not only a performance measure. It predicts how humans will treat the agent. The study here measures consistency. Other work measures human oversight under different labels. This research suggests a chain between them that could be tested: more consistent agent, less personification, more appropriate scrutiny.

## 4. Challenges to this project's own position

- **The default template is human.** Pareidolia goes to faces, not to abstract spirits. "Animism without anthropomorphism" may be harder to achieve than the design literature suggests. A mood grid that says a kiosk is afraid is arguably a face drawn on the kiosk.
- **The source tradition wants unpredictability.** Marenko and van Allen value uncertainty in animistic design. The research above says unpredictability is what drives people to see a human. Those two cannot both be design goals for a workplace agent.
- **A character sheet may redirect and not replace.** The open question is whether giving an agent a bounded artifact identity swaps out the human template or only gives it a smaller place to sit. Nothing in this repo tests that yet.

## 5. Limits of the analogy

- Face pareidolia is fast visual perception. Interaction with a language agent unfolds over time and through language, which is a stronger and different trigger.
- The 250 millisecond correction describes vision. There is no evidence here that mind attribution to agents corrects itself in a similar way.
- Use pareidolia for the intuition and the anthropomorphism research for evidence.

## References

- Wardle, S. G., Taubert, J., Teichmann, L., Baker, C. I. (2020). Rapid and dynamic processing of face pareidolia in the human brain. *Nature Communications* 11. https://doi.org/10.1038/s41467-020-18325-8
- Wardle, S. G., Paranjape, S., Taubert, J., Baker, C. I. (2022). Illusory faces are more likely to be perceived as male than female. *PNAS* 119(5). https://doi.org/10.1073/pnas.2117413119
- Epley, N., Waytz, A., Cacioppo, J. T. (2007). On seeing human: a three-factor theory of anthropomorphism. *Psychological Review* 114(4), 864-886.
- Waytz, A., Epley, N., Cacioppo, J. T. (2010). Social Cognition Unbound: Insights Into Anthropomorphism and Dehumanization. *Current Directions in Psychological Science*. https://pmc.ncbi.nlm.nih.gov/articles/PMC4020342
- Waytz, A., Morewedge, C. K., Epley, N., Monteleone, G., Gao, J.-H., Cacioppo, J. T. (2010). Making sense by making sentient: effectance motivation increases anthropomorphism. *Journal of Personality and Social Psychology* 99(3), 410-435. https://doi.org/10.1037/a0020240
- Heider, F. and Simmel, M. (1944). An experimental study of apparent behavior. *American Journal of Psychology* 57.
- Guthrie, S. (1993). *Faces in the Clouds: A New Theory of Religion*. Oxford University Press.
- Reeves, B. and Nass, C. (1996). *The Media Equation*. Cambridge University Press.
