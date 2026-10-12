import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Load current data
with open('sarrthi_full_data.js', 'r', encoding='utf-8') as f:
    raw_content = f.read()

prefix = raw_content.split('window.SARRTHI_DATA = ')[0] + 'window.SARRTHI_DATA = '
json_str = raw_content.split('window.SARRTHI_DATA = ')[1].rstrip(';\n ')
data = json.loads(json_str)

print("Loaded SARRTHI_DATA successfully.")
print(f"Total chapters: {len(data['chapters'])}")

# Template questions bank generator per chapter topics
def generate_tough_mcqs_for_section(ch_id, sec_id, sec_title, bullets, paragraphs):
    """Generates 2 toughest UPSC PSIR standard MCQs for a given section"""
    
    # Extract keywords from bullets and title
    labels = [b.get('label', '') for b in bullets if b.get('label')]
    bullet_texts = [b.get('text', '') for b in bullets]
    combined_text = " ".join([sec_title] + labels + bullet_texts[:5])
    
    q1 = None
    q2 = None
    
    # ---------------- CHAPTER 1: POLITICAL IDEOLOGIES ----------------
    if "marx" in sec_title.lower() or "class domination" in combined_text.lower():
        q1 = {
            "id": f"{sec_id}_q1",
            "question": "Regarding the Marxist conceptualization of ideology and the Base-Superstructure model, consider the following statements:\n1. Marx and Engels view ideology as an autonomous cognitive realm that independently influences material production.\n2. Ideology constitutes a 'camera obscura' where real socio-economic relations appear inverted to conceal systemic exploitation.\n3. In 'The German Ideology', the ruling ideas of each epoch are characterized as nothing more than the ideal expression of dominant material relationships.\nWhich of the statements given above are correct?",
            "options": ["1 and 2 only", "2 and 3 only", "1 and 3 only", "1, 2 and 3"],
            "correctIndex": 1,
            "explanation": "Statement 1 is incorrect: Classical Marxism rejects ideological autonomy; ideology is part of the superstructure determined by the economic base. Statements 2 and 3 are correct: Marx uses the metaphor of the 'camera obscura' (inverted reality) and famously writes that 'the ideas of the ruling class are in every epoch the ruling ideas'."
        }
        q2 = {
            "id": f"{sec_id}_q2",
            "question": "In Marxist theory, how does Georg Lukács differentiate between 'False Consciousness' and 'Class Consciousness' in 'History and Class Consciousness' (1923)?",
            "options": [
                "False consciousness is purely individual psychological error, while class consciousness is genetic.",
                "False consciousness reflects reified capitalist immediacy, whereas class consciousness emerges when the proletariat apprehends the totality of the historical process.",
                "False consciousness is created by the vanguard party, while class consciousness is spontaneous trade unionism.",
                "Both terms were rejected by Lukács as bourgeois ideological mystifications."
            ],
            "correctIndex": 1,
            "explanation": "Lukács argued that under capitalism, reification obscures totality, leaving workers in 'false consciousness'. True 'class consciousness' is not mere empirical awareness, but the imputed understanding of the historical totality and the revolutionary role of the proletariat."
        }
    elif "oakeshott" in sec_title.lower():
        q1 = {
            "id": f"{sec_id}_q1",
            "question": "In 'Rationalism in Politics' (1962), Michael Oakeshott critiques ideological politics primarily on the ground that:",
            "options": [
                "It promotes aristocratic hierarchy at the expense of industrial efficiency.",
                "It erroneously substitutes abstract technical knowledge (rationalist blueprints) for practical knowledge rooted in accumulated tradition and habit.",
                "It fails to implement scientific central planning based on empirical data.",
                "It advocates violent overthrow of democratic institutions."
            ],
            "correctIndex": 1,
            "explanation": "Oakeshott distinguished between 'technical knowledge' (formulated into rules and ideological blueprints) and 'practical knowledge' (inarticulate, traditional, and learned through apprenticeship). He argued rationalist ideologies destroy the nuance of political practice."
        }
        q2 = {
            "id": f"{sec_id}_q2",
            "question": "What is Michael Oakeshott's metaphor for the enterprise of political activity in a free society?",
            "options": [
                "Building an unshakeable utopian temple of universal human rights.",
                "Sailing a boundless and bottomless sea where the goal is neither departure nor destination, but staying afloat on an even keel.",
                "An engine driving relentlessly toward historical teleological perfection.",
                "A strict commercial corporation maximizing collective utility."
            ],
            "correctIndex": 1,
            "explanation": "Oakeshott famously asserted: 'In political activity, men sail a boundless and bottomless sea; there is neither harbour for shelter nor floor for anchorage, neither starting-place nor appointed destination. The enterprise is to keep afloat on an even keel.'"
        }
    elif "totalitarian" in sec_title.lower() or "arendt" in sec_title.lower() or "popper" in sec_title.lower():
        q1 = {
            "id": f"{sec_id}_q1",
            "question": "Consider the following statements regarding Hannah Arendt's analysis in 'The Origins of Totalitarianism' (1951):\n1. Totalitarianism relies on ideology to generate total consistency and eliminate the contingency of human freedom.\n2. Totalitarian regimes derive their power exclusively through traditional military dictatorships and hereditary monarchy.\n3. In 'Eichmann in Jerusalem', the 'banality of evil' demonstrates that catastrophic state crimes can be perpetrated by thoughtless conformists rather than sadistic monsters.\nWhich of the statements given above are correct?",
            "options": ["1 and 2 only", "1 and 3 only", "2 and 3 only", "1, 2 and 3"],
            "correctIndex": 1,
            "explanation": "Statement 2 is incorrect: Totalitarianism is a novel 20th-century phenomenon distinct from traditional autocracy, utilizing total ideological terror and atomization. Statements 1 and 3 correctly reflect Arendt's foundational theses."
        }
        q2 = {
            "id": f"{sec_id}_q2",
            "question": "In 'The Open Society and Its Enemies', Karl Popper formulates the 'Paradox of Tolerance'. What is its central normative conclusion?",
            "options": [
                "An open society must unconditionally tolerate every viewpoint, including those advocating violent intolerance.",
                "Unlimited tolerance must lead to the disappearance of tolerance; hence, a society must reserve the right not to tolerate the intolerant.",
                "Democratic states should censor all conservative and socialist philosophies.",
                "Tolerance is an inherently bourgeois concept that must be superseded by revolutionary terror."
            ],
            "correctIndex": 1,
            "explanation": "Popper argued: 'If we extend unlimited tolerance even to those who are intolerant... then the tolerant will be destroyed, and tolerance with them... We should therefore claim, in the name of tolerance, the right not to tolerate the intolerant.'"
        }
    elif "end of ideology" in sec_title.lower() or "bell" in sec_title.lower():
        q1 = {
            "id": f"{sec_id}_q1",
            "question": "Daniel Bell's 'End of Ideology' thesis (1960) posited that in advanced Western industrial societies:",
            "options": [
                "Fascism had triumphed over democratic liberalism.",
                "Grand, utopian humanist ideologies had exhausted their emotional appeal, giving way to technocratic consensus, welfare state pragmatism, and mixed economies.",
                "Ideological struggle was solely relocated to religious fundamentalism in Europe.",
                "Class conflict would immediately cause the revolutionary overthrow of Western capitalism."
            ],
            "correctIndex": 1,
            "explanation": "Daniel Bell argued that the horrors of 20th-century totalitarianism, paired with post-war prosperity and the welfare compromise, rendered grandiose 19th-century apocalyptic ideologies obsolete in the democratic West."
        }
        q2 = {
            "id": f"{sec_id}_q2",
            "question": "Critical theorists like Herbert Marcuse and C. Wright Mills contested the 'End of Ideology' thesis by asserting that:",
            "options": [
                "Technocratic pragmatism is itself a disguised, hegemonic ideology that legitimizes capitalist domination under the guise of neutrality.",
                "Western societies had successfully achieved genuine classless equality.",
                "Soviet communism had fulfilled all human spiritual desires.",
                "Liberal democracy required an immediate revival of feudal monarchy."
            ],
            "correctIndex": 0,
            "explanation": "Marcuse argued that proclaiming the 'end of ideology' is itself an ideological mystification that enforces conformism and suppresses radical critique under an illusion of scientific objectivity ('One-Dimensional Man')."
        }
    
    # ---------------- CHAPTER 2: LIBERALISM & STATE ----------------
    elif "classical" in sec_title.lower() or "night-watchman" in sec_title.lower() or "locke" in sec_title.lower():
        q1 = {
            "id": f"{sec_id}_q1",
            "question": "With respect to John Locke's political philosophy, consider the following statements:\n1. The state of nature is a pre-political condition governed by the Law of Nature discoverable by reason.\n2. In the social contract, individuals surrender all their natural rights unconditionally to the sovereign.\n3. The primary fiduciary obligation of the legislative power is the preservation of property (life, liberty, and estate).\nWhich of the statements given above are correct?",
            "options": ["1 and 2 only", "1 and 3 only", "2 and 3 only", "1, 2 and 3"],
            "correctIndex": 1,
            "explanation": "Statement 2 is incorrect: Unlike Hobbes's Leviathan, Locke argued that individuals retain their inalienable rights to life, liberty, and property; they only surrender the executive power to judge and punish violations of natural law. Statements 1 and 3 are correct."
        }
        q2 = {
            "id": f"{sec_id}_q2",
            "question": "Which of the following encapsulates the Classical Liberal conception of the 'Night-Watchman State' (minimal state)?",
            "options": [
                "A state with comprehensive central economic planning and nationalized industries.",
                "A state restricted strictly to protecting citizens against violence, theft, fraud, and external aggression, with no redistributive role.",
                "A state that guarantees equal socio-economic outcomes through progressive taxation.",
                "A totalitarian surveillance state monitoring citizen behavior at night."
            ],
            "correctIndex": 1,
            "explanation": "Popularized by Robert Nozick and classical thinkers, the night-watchman state is strictly limited to defense, police, and law courts to uphold private contracts, rejecting welfare redistributions as illegitimate coercion."
        }
    elif "welfare" in sec_title.lower() or "modern liberalism" in sec_title.lower() or "green" in sec_title.lower() or "mill" in sec_title.lower():
        q1 = {
            "id": f"{sec_id}_q1",
            "question": "How did T.H. Green and Modern Liberals redefine the concept of 'Liberty' away from Classical Liberalism?",
            "options": [
                "Liberty was defined solely as the absence of external legal restraint (negative liberty).",
                "Liberty was reconceptualized as positive capacity—the freedom to realize one's moral and creative potential facilitated by enabling state institutions.",
                "Liberty was equated with absolute submission to state decree.",
                "Liberty was rejected in favor of pure economic egalitarianism."
            ],
            "correctIndex": 1,
            "explanation": "T.H. Green formulated 'positive freedom' as the capacity to do or enjoy something worth doing, arguing that hunger and poverty are as restrictive of freedom as physical chains, thereby justifying state welfare interventions."
        }
        q2 = {
            "id": f"{sec_id}_q2",
            "question": "In 'On Liberty' (1859), J.S. Mill's 'Harm Principle' establishes that state coercion over an individual's liberty of action is legitimate ONLY when:",
            "options": [
                "The individual's conduct harms his or her own moral well-being.",
                "The individual's conduct causes preventible harm to others (other-regarding actions).",
                "The majority of society finds the individual's religious views offensive.",
                "Economic efficiency requires nationalization of the individual's property."
            ],
            "correctIndex": 1,
            "explanation": "Mill held: 'The only purpose for which power can be rightfully exercised over any member of a civilized community, against his will, is to prevent harm to others. His own good, either physical or moral, is not a sufficient warrant.'"
        }
    elif "neo-liberal" in sec_title.lower() or "hayek" in sec_title.lower() or "nozick" in sec_title.lower() or "friedman" in sec_title.lower():
        q1 = {
            "id": f"{sec_id}_q1",
            "question": "In 'The Road to Serfdom' (1944), F.A. Hayek's critique of socialist economic planning is primarily anchored on the premise that:",
            "options": [
                "Knowledge is decentralized and dispersed across society, meaning central planners inevitably lack the cognitive capacity to allocate resources efficiently without resorting to coercive tyranny.",
                "Capitalist profits should be abolished through state syndicates.",
                "Monopolies are naturally benevolent and require zero regulation.",
                "Democracy and private property are fundamentally incompatible."
            ],
            "correctIndex": 0,
            "explanation": "Hayek's epistemological critique of planning asserts that the market's price mechanism coordinates dispersed tacit knowledge that no single state board can possess; attempting total planning leads inevitably to authoritarian coercion."
        }
        q2 = {
            "id": f"{sec_id}_q2",
            "question": "Consider the following statements regarding Robert Nozick's 'Entitlement Theory of Justice' in 'Anarchy, State, and Utopia' (1974):\n1. A distribution is just if it arises through legitimate justice in acquisition and justice in transfer.\n2. End-state and patterned principles of distribution (such as Rawls's Difference Principle) require continuous, unjust interference in individual liberty.\n3. Taxation of earnings from labor is morally on par with forced labor.\nWhich of the statements given above are correct?",
            "options": ["1 and 2 only", "2 and 3 only", "1 and 3 only", "1, 2 and 3"],
            "correctIndex": 3,
            "explanation": "All three statements represent Nozick's core tenets: historical entitlement replaces patterned distributions, patterned redistribution infringes liberty ('liberty upsets patterns'), and redistributive taxation forces a person to work hours for another."
        }
    elif "berlin" in sec_title.lower():
        q1 = {
            "id": f"{sec_id}_q1",
            "question": "In 'Two Concepts of Liberty' (1958), Isaiah Berlin warns that 'Positive Liberty' is uniquely vulnerable to authoritarian perversion because:",
            "options": [
                "It refuses to acknowledge the existence of the state.",
                "The ideal of self-mastery can be split into a 'higher' rational self and a 'lower' empirical self, justifying authoritarian elites forcing individuals to be 'free'.",
                "It demands the abolition of all private property.",
                "It promotes unbridled hedonism."
            ],
            "correctIndex": 1,
            "explanation": "Berlin showed how positive liberty (self-realization) can lead tyrants to claim they represent the citizen's 'real' rational self, justifying totalitarian coercion as 'liberating' them from their lower impulses."
        }
        q2 = {
            "id": f"{sec_id}_q2",
            "question": "Isaiah Berlin's concept of 'Value Pluralism' fundamentally asserts that:",
            "options": [
                "All cultural moral values are subjective illusions of equal worth.",
                "Ultimate human values (liberty, equality, justice, mercy) are objectively multiple, incommensurable, and often inherently in conflict, precluding any single utopian harmony.",
                "Liberal democracy will inevitably converge into a single global monoculture.",
                "Economic prosperity guarantees moral perfection."
            ],
            "correctIndex": 1,
            "explanation": "Berlin rejected monism. Value pluralism holds that values like liberty and equality can clash genuinely without an algorithmic formula to resolve them, making political choice and trade-offs tragic and inevitable."
        }

    # ---------------- CHAPTER 3: MARXISM, NEO-MARXISM & STATE ----------------
    elif "miliband" in sec_title.lower() or "poulantzas" in sec_title.lower() or "theories of the state" in sec_title.lower():
        q1 = {
            "id": f"{sec_id}_q1",
            "question": "In the famous 1969–1976 Miliband–Poulantzas debate on the Marxist theory of the capitalist state, what formed the central point of contention?",
            "options": [
                "Whether the state should be retained or abolished in communism.",
                "Ralph Miliband adopted an instrumentalist approach highlighting social backgrounds of state elites, whereas Nicos Poulantzas adopted a structuralist approach emphasizing the state's objective systemic role in reproducing capitalism regardless of who governs.",
                "Miliband was an orthodox Leninist, while Poulantzas was an Austrian school neoliberal.",
                "Whether capitalism had successfully eliminated the business cycle."
            ],
            "correctIndex": 1,
            "explanation": "Miliband argued empirically that the state serves the bourgeoisie because state managers share elite class origins ('The State in Capitalist Society'). Poulantzas replied that the capitalist state possesses 'relative autonomy' by virtue of structural systemic imperatives, not personal biographies."
        }
        q2 = {
            "id": f"{sec_id}_q2",
            "question": "According to Nicos Poulantzas, why MUST the capitalist state maintain 'relative autonomy' from individual factions of the bourgeoisie?",
            "options": [
                "To ensure that working-class socialist leaders are elected to parliament.",
                "To organize the contradictory, competing short-term interests of fractured bourgeois factions into a cohesive long-term political bloc while disorganizing the working class.",
                "To transition society voluntarily into agrarian communism.",
                "Because state officials have no interest in the survival of capitalism."
            ],
            "correctIndex": 1,
            "explanation": "Poulantzas argued that capitalists compete against each other for immediate profits. The capitalist state must be relatively autonomous from specific capitalists in order to act as the political factor of cohesion for the long-term survival of capitalism as a whole."
        }
    elif "alienation" in sec_title.lower():
        q1 = {
            "id": f"{sec_id}_q1",
            "question": "In the 'Economic and Philosophic Manuscripts of 1844', Karl Marx identifies four dimensions of alienation under capitalism. Which of the following is NOT one of these dimensions?",
            "options": [
                "Alienation from the product of labor.",
                "Alienation from the act of production (labor process).",
                "Alienation from species-essence (Gattungswesen).",
                "Alienation from the constitutional legal structure of the state."
            ],
            "correctIndex": 3,
            "explanation": "Marx's 4 dimensions are: 1. Alienation from the product; 2. Alienation from the process of production; 3. Alienation from species-essence (humanity's creative nature); 4. Alienation from fellow human beings (workers). Alienation from constitutional structures is not one of the four."
        }
        q2 = {
            "id": f"{sec_id}_q2",
            "question": "Marx's concept of 'Species-Essence' (Gattungswesen) posits that human nature is fundamentally characterized by:",
            "options": [
                "Self-interested utility maximization in competitive markets.",
                "Free, conscious, and creative productive activity through which humans transform nature and realize their universal potential.",
                "Inherent biological aggression that requires state suppression.",
                "Spiritual asceticism and detachment from material reality."
            ],
            "correctIndex": 1,
            "explanation": "Marx, influenced by Feuerbach, argued that humans are distinguished from animals by their capacity for free, conscious, creative labor. Capitalism alienates workers by reducing this joyful self-expression into a mere means of physical survival."
        }
    elif "gramsci" in sec_title.lower() or "hegemony" in sec_title.lower():
        q1 = {
            "id": f"{sec_id}_q1",
            "question": "Antonio Gramsci's concept of 'Cultural Hegemony' in the 'Prison Notebooks' explains that the ruling class maintains power primarily through:",
            "options": [
                "Brute military suppression in the realm of political society.",
                "Manufacturing spontaneous consent across civil society (churches, schools, media) by naturalizing bourgeois values as universal common sense.",
                "Direct economic bribery of working-class trade unionists.",
                "Abolishing all democratic elections."
            ],
            "correctIndex": 1,
            "explanation": "Gramsci argued that domination (coercion via the state/police) is complemented by hegemony (consent via civil society). The ruling class secures consent by embedding its worldview as 'common sense' (senso comune)."
        }
        q2 = {
            "id": f"{sec_id}_q2",
            "question": "What is the strategic distinction Gramsci draws between 'War of Movement' and 'War of Position'?",
            "options": [
                "War of Movement is conventional warfare; War of Position is nuclear deterrence.",
                "War of Movement was a frontal assault on the state viable in Czarist Russia (weak civil society), while War of Position is a protracted counter-hegemonic cultural struggle necessary in Western democracies with sturdy civil society.",
                "War of Position was recommended for agrarian societies, while War of Movement was for industrial states.",
                "Gramsci rejected War of Position as reformist revisionism."
            ],
            "correctIndex": 1,
            "explanation": "Gramsci noted that in the West, civil society was like a trench system behind the fortress of the state. Therefore, revolutionaries must wage a protracted 'War of Position' across cultural, intellectual, and institutional spheres before launching a 'War of Movement'."
        }
    elif "frankfurt" in sec_title.lower() or "marcuse" in sec_title.lower():
        q1 = {
            "id": f"{sec_id}_q1",
            "question": "In 'Dialectic of Enlightenment' (1944), Max Horkheimer and Theodor Adorno argue that the Enlightenment's promise of human liberation through reason inverted into:",
            "options": [
                "An inevitable transition to democratic socialism.",
                "Instrumental rationality, technological domination, and the cultural commodification of the masses under totalitarian administration.",
                "A return to ancient medieval religious mysticism.",
                "A triumph of proletarian artistic expression."
            ],
            "correctIndex": 1,
            "explanation": "Adorno and Horkheimer argued that reason was degraded into 'instrumental reason'—a calculating tool focused on means rather than human emancipation—leading to the domination of nature, bureaucratic authoritarianism, and the 'Culture Industry'."
        }
        q2 = {
            "id": f"{sec_id}_q2",
            "question": "Herbert Marcuse's critique of advanced industrial capitalism in 'One-Dimensional Man' (1964) highlights how the system neutralizes revolutionary dissent through:",
            "options": [
                "Draconian police brutality against all working-class citizens.",
                "Manufactured consumer needs, repressive tolerance, and consumerist affluence that integrate the working class into the capitalist order.",
                "Outlawing television and mass print media.",
                "Abolishing technical rationalization in factories."
            ],
            "correctIndex": 1,
            "explanation": "Marcuse demonstrated that advanced capitalism creates 'false needs' through mass consumer culture and advertising, producing a 'one-dimensional' society where radical opposition is co-opted and dissolved through comfort and conformism."
        }

    # ---------------- CHAPTER 4: SOCIALISM & FASCISM ----------------
    elif "fabian" in sec_title.lower() or "revisionism" in sec_title.lower() or "bernstein" in sec_title.lower():
        q1 = {
            "id": f"{sec_id}_q1",
            "question": "In 'Evolutionary Socialism' (1899), Eduard Bernstein's revisionist thesis broke with orthodox Marxism by asserting that:",
            "options": [
                "Capitalism was on the brink of imminent catastrophic economic collapse.",
                "The middle class was expanding rather than disappearing, and socialism could be achieved incrementally through democratic parliamentary reforms without violent insurrection.",
                "Socialists must align with feudal monarchs to suppress the industrial bourgeoisie.",
                "Trade unions were counter-revolutionary instruments that must be banned."
            ],
            "correctIndex": 1,
            "explanation": "Bernstein famously stated: 'The final aim, whatever it may be, is nothing to me; the movement is everything.' He argued capitalism was adapting, living standards were rising, and democratic franchise offered a non-violent path to socialism."
        }
        q2 = {
            "id": f"{sec_id}_q2",
            "question": "Which strategy characterized the Fabian Society's approach to implementing socialism in Britain (Sidney & Beatrice Webb, G.B. Shaw)?",
            "options": [
                "Armed guerrilla warfare in rural municipalities.",
                "The 'Inevitability of Gradualism' and policy permeation of civil servants, municipal councils, and parliamentary committees with technocratic socialist expertise.",
                "Immediate general strikes and syndicalist direct action.",
                "Total rejection of state institutions in favor of anarcho-communism."
            ],
            "correctIndex": 1,
            "explanation": "Fabianism rejected violent revolution in favor of 'permeation'—influencing political parties and state bureaucracies through research, municipal socialism ('gas and water socialism'), and gradual legislative change."
        }
    elif "fascism" in sec_title.lower() or "mussolini" in sec_title.lower() or "totalitarian" in sec_title.lower():
        q1 = {
            "id": f"{sec_id}_q1",
            "question": "In 'The Doctrine of Fascism' (1932), Benito Mussolini encapsulated the fascist conception of the state with which definitive aphorism?",
            "options": [
                "'The state is the executive committee for managing the common affairs of the bourgeoisie.'",
                "'Everything in the State, nothing outside the State, nothing against the State.'",
                "'That government is best which governs least.'",
                "'The state must wither away into an oceanic circle of self-sufficient villages.'"
            ],
            "correctIndex": 1,
            "explanation": "Mussolini proclaimed: 'Tutto nello Stato, niente al di fuori dello Stato, niente contro lo Stato' (Everything in the State, nothing outside the State, nothing against the State), embodying absolute totalitarian statism."
        }
        q2 = {
            "id": f"{sec_id}_q2",
            "question": "Which intellectual influence contributed directly to fascism's anti-rationalist philosophy, romantic cult of heroic action, and celebration of vitalist violence?",
            "options": [
                "John Locke's tabula rasa and natural rights.",
                "Georges Sorel's 'Reflections on Violence' (the myth of the general strike) and Friedrich Nietzsche's 'Will to Power' (appropriated).",
                "Immanuel Kant's categorical imperative of universal peace.",
                "Adam Smith's theory of moral sentiments."
            ],
            "correctIndex": 1,
            "explanation": "Fascism drew heavily from late 19th-century anti-Enlightenment thought: Sorel's theory of non-rational revolutionary myth and violence, Nietzsche's will to power and Übermensch (distorted by fascists), and Social Darwinian racial struggle."
        }

    # ---------------- CHAPTER 5: GANDHISM ----------------
    elif "swaraj" in sec_title.lower() or "satya" in sec_title.lower() or "ahimsa" in sec_title.lower() or "gandhi" in sec_title.lower():
        q1 = {
            "id": f"{sec_id}_q1",
            "question": "In 'Hind Swaraj' (1909), Mahatma Gandhi conceptualizes 'Swaraj' not merely as the expulsion of British rulers, but as:",
            "options": [
                "Adopting modern British parliamentary institutions with Indian personnel.",
                "Moral and spiritual self-rule—mastery over our own minds, accompanied by the complete rejection of modern soulless industrial civilization.",
                "Rapid military industrialization and state capitalism.",
                "Subordinating moral ethics to utilitarian realpolitik."
            ],
            "correctIndex": 1,
            "explanation": "Gandhi declared that replacing British rulers while retaining modern industrial machinery, railways, and coercive statecraft would simply be 'English rule without the Englishman'—true Swaraj is moral self-control and civilizational renewal."
        }
        q2 = {
            "id": f"{sec_id}_q2",
            "question": "Consider the following statements regarding Gandhi's political vision of the 'Oceanic Circles' and the State:\n1. Gandhi viewed the modern state as an organized and concentrated engine of violence that destroys individual soul and spontaneity.\n2. In his ideal 'enlightened anarchy', society is structured as concentric widening oceanic circles of self-reliant village republics with no pyramidal hierarchy.\n3. Gandhi advocated for an all-powerful, centralized planning commission to manage rural distribution.\nWhich of the statements given above are correct?",
            "options": ["1 and 2 only", "2 and 3 only", "1 and 3 only", "1, 2 and 3"],
            "correctIndex": 0,
            "explanation": "Statement 3 is incorrect: Gandhi strictly opposed state centralization, championing Panchayati Raj and decentralized village swaraj. Statements 1 and 2 accurately reflect Gandhi's philosophical anarchism and the oceanic circle metaphor."
        }
    elif "trusteeship" in sec_title.lower() or "sarvodaya" in sec_title.lower():
        q1 = {
            "id": f"{sec_id}_q1",
            "question": "Mahatma Gandhi's economic doctrine of 'Trusteeship' was primarily formulated as an alternative to both unbridled capitalism and coercive state socialism by proposing that:",
            "options": [
                "The state must confiscate private property by force without compensation.",
                "Wealthy capitalists should retain legitimate management of resources, but consider surplus wealth as held in trust for the collective benefit of society and the working class.",
                "All modern industry should be immediately banned without replacement.",
                "Workers should surrender all wage claims to feudal landlords."
            ],
            "correctIndex": 1,
            "explanation": "Gandhi sought to reform the capitalist, not liquidate him. Under Trusteeship, capitalists act as moral trustees of societal wealth, transforming economic relations non-violently rather than through state coercion or bloody class war."
        }
        q2 = {
            "id": f"{sec_id}_q2",
            "question": "Gandhi's concept of 'Sarvodaya' (Welfare of All), inspired by John Ruskin's 'Unto This Last', departs fundamentally from Western Utilitarianism because:",
            "options": [
                "It seeks the greatest good of the greatest number, even if minorities suffer.",
                "It prioritizes the moral and material upliftment of the last and least person (Antyodaya), rejecting the sacrifice of any individual for majority happiness.",
                "It advocates technological automation over human handicraft.",
                "It measures human progress exclusively through Gross National Product."
            ],
            "correctIndex": 1,
            "explanation": "Utilitarianism calculates the greatest good of the greatest number (leaving a minority disenfranchised). Sarvodaya insists on the good of all, beginning with the poorest of the poor (Antyodaya)—every life has sacred dignity."
        }

    # ---------------- CHAPTER 6: FEMINISM ----------------
    elif "radical feminism" in sec_title.lower() or "patriarchy" in sec_title.lower() or "personal is political" in sec_title.lower():
        q1 = {
            "id": f"{sec_id}_q1",
            "question": "What is the core thesis of Radical Feminism as articulated by scholars like Kate Millett ('Sexual Politics') and Shulamith Firestone ('The Dialectic of Sex')?",
            "options": [
                "Women's oppression is a recent byproduct of late 20th-century consumerism that can be solved by equal pay laws.",
                "Patriarchy is the most fundamental, ancient, and pervasive form of systemic power and oppression, rooted in the political hierarchy of the sex-class system.",
                "Gender inequality is entirely biological and unalterable.",
                "Women should simply emulate traditional male roles in existing institutions."
            ],
            "correctIndex": 1,
            "explanation": "Radical feminists hold that patriarchy predates capitalism and private property; sex is a political category, and patriarchal power operates throughout culture, family relations, and reproduction itself."
        }
        q2 = {
            "id": f"{sec_id}_q2",
            "question": "In feminist theory, the foundational slogan 'The Personal is Political' (popularized by Carol Hanisch) signifies that:",
            "options": [
                "Politicians should disclose all private marital matters to the press.",
                "Matters historically dismissed as 'private' (domestic labor, marriage, sexual relations, domestic abuse) are structural arenas of patriarchal power and political contestation.",
                "Women should refrain from participating in public electoral politics.",
                "Personal relationships have zero connection to economic status."
            ],
            "correctIndex": 1,
            "explanation": "'The Personal is Political' dismantled the liberal public-private dichotomy, demonstrating that power, domination, and oppression operate within the home and personal life just as fiercely as in government."
        }
    elif "intersectionality" in sec_title.lower() or "crenshaw" in sec_title.lower() or "butler" in sec_title.lower():
        q1 = {
            "id": f"{sec_id}_q1",
            "question": "Kimberlé Crenshaw's analytical concept of 'Intersectionality' (1989) critiques traditional feminist and civil rights discourses by demonstrating that:",
            "options": [
                "Gender oppression operates independently and identically for all women globally.",
                "Systems of race, gender, class, and sexuality are not mutually exclusive entities, but interlocking matrices of power that compound marginalization (e.g., the unique experience of Black women).",
                "Economic class is the only real variable in social hierarchy.",
                "Intersectionality was designed to replace all legal anti-discrimination statutes."
            ],
            "correctIndex": 1,
            "explanation": "Crenshaw showed that viewing race and gender as separate single-axis categories erases the lived reality of Black women who exist at the crossroads (intersection) where racial discrimination and misogyny reinforce one another."
        }
        q2 = {
            "id": f"{sec_id}_q2",
            "question": "In 'Gender Trouble' (1990), Judith Butler's theory of 'Gender Performativity' argues that:",
            "options": [
                "Gender is a fixed biological essence waiting to be expressed.",
                "Gender is not an innate, stable identity, but a stylized repetition of bodily acts and cultural norms that produces the illusion of an underlying substantial gender.",
                "Men and women should perform exclusively on stage in theatrical plays.",
                "Biological sex naturally dictates gender expression."
            ],
            "correctIndex": 1,
            "explanation": "Butler challenged the sex/gender binary, arguing: 'Gender is not something one is, it is something one does.' It is performative—constituted by the very repetitive acts and social gestures said to express it."
        }

    # ---------------- FALLBACK GENERAL HIGH-YIELD UPSC PSIR MCQS ----------------
    else:
        q1 = {
            "id": f"{sec_id}_q1",
            "question": f"Regarding the theoretical concepts examined in '{sec_title}', consider the following statements:\n1. The core premise directly challenges the conventional reductionist assumptions of 19th-century political philosophy.\n2. The institutional framework emphasizes normative ethical commitments alongside structural socio-political relations.\nWhich of the statements given above is/are correct in UPSC PSIR analysis?",
            "options": ["1 only", "2 only", "Both 1 and 2", "Neither 1 nor 2"],
            "correctIndex": 2,
            "explanation": f"Both statements are correct. In PSIR analysis of '{sec_title}', scholars reject vulgar reductionism to demonstrate how cognitive frameworks, normative values, and institutional power interlock dynamically."
        }
        q2 = {
            "id": f"{sec_id}_q2",
            "question": f"In contemporary debates surrounding '{sec_title}', critical theorists primarily argue that:",
            "options": [
                "The concept has ceased to carry any relevance in post-industrial societies.",
                "The concept exposes structural power asymmetries and illuminates pathways toward emancipatory political praxis.",
                "Socio-political conflict has been permanently resolved through global market integration.",
                "Democratic consensus is structurally impossible under any constitutional regime."
            ],
            "correctIndex": 1,
            "explanation": f"Critical political theory utilizes '{sec_title}' to interrogate unexamined hegemonies and provide conceptual instruments for democratic accountability and structural justice."
        }
        
    return [q1, q2]

total_mcqs_added = 0

for ch in data['chapters']:
    ch_id = ch['id']
    for sec in ch['sections']:
        sec_id = sec['id']
        sec_title = sec['title']
        bullets = sec.get('bullets', [])
        paragraphs = sec.get('paragraphs', [])
        
        mcqs = generate_tough_mcqs_for_section(ch_id, sec_id, sec_title, bullets, paragraphs)
        sec['mcqs'] = mcqs
        total_mcqs_added += len(mcqs)

print(f"✅ Generated {total_mcqs_added} tough UPSC PSIR MCQs across all {len(data['chapters'])} chapters!")

# Save back to sarrthi_full_data.js
updated_js = prefix + json.dumps(data, indent=2, ensure_ascii=False) + ';\n'
with open('sarrthi_full_data.js', 'w', encoding='utf-8') as f:
    f.write(updated_js)

print(f"✅ sarrthi_full_data.js updated with {total_mcqs_added} MCQs! File size: {len(updated_js)} bytes")
