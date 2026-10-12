# -*- coding: utf-8 -*-
"""
Enriches all generic MCQs in sarrthi_full_data.js with:
1. Who said to whom / Quote attribution questions
2. Thinker-on-thinker critiques ("What this thinker said about another")
3. Book authorship and landmark publications
4. 10-marker UPSC Introduction & Conclusion preference choices
"""

import json
import re
import sys

# Configure UTF-8 stdout
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

with open('sarrthi_full_data.js', 'r', encoding='utf-8') as f:
    raw = f.read()

prefix = raw.split('window.SARRTHI_DATA = ')[0] + 'window.SARRTHI_DATA = '
json_str = raw.split('window.SARRTHI_DATA = ')[1].rstrip(';\n ')
data = json.loads(json_str)

# Dictionary of specialized questions mapping to section IDs
custom_questions_map = {
    # ---------------- CHAPTER 1 ----------------
    "ch1_ideologies_sec_intro": [
        {
            "id": "ch1_ideologies_sec_intro_q1",
            "question": "Who originally coined the term 'Ideology' in 1796 during the French Enlightenment, defining it as the 'science of ideas'?",
            "options": [
                "Destutt de Tracy",
                "Karl Marx",
                "Napoleon Bonaparte",
                "Auguste Comte"
            ],
            "correctIndex": 0,
            "explanation": "Antoine Destutt de Tracy coined 'idéologie' in 1796 to denote an empirical 'science of ideas' grounded in sensations, before Napoleon and later Marx gave the term pejorative political connotations."
        },
        {
            "id": "ch1_ideologies_sec_intro_q2",
            "question": "Which political theorist pioneered the 'Morphological Approach' to ideology, arguing that ideologies are configurations of decontested concepts clustered around core values?",
            "options": [
                "Michael Freeden",
                "Karl Mannheim",
                "Louis Althusser",
                "Quentin Skinner"
            ],
            "correctIndex": 0,
            "explanation": "Michael Freeden (in 'Ideologies and Political Theory', 1996) formulated the morphological approach, demonstrating that ideologies organize and fix ('decontest') the ambiguous meanings of political concepts like liberty, equality, and justice."
        }
    ],
    "ch1_ideologies_sec_8": [
        {
            "id": "ch1_ideologies_sec_8_q1",
            "question": "In 'Ideology and Utopia' (1929), who proposed 'Relationism'—asserting that all political thought is socially situated and that socially unattached intellectuals ('freischwebende Intelligenz') can synthesize competing perspectives?",
            "options": [
                "Karl Mannheim",
                "Max Weber",
                "Theodor Adorno",
                "Jürgen Habermas"
            ],
            "correctIndex": 0,
            "explanation": "Karl Mannheim founded the sociology of knowledge in 'Ideology and Utopia', distinguishing particular vs total ideology, and arguing that 'relationism' avoids nihilistic relativism through the syntheses of independent intellectuals."
        },
        {
            "id": "ch1_ideologies_sec_8_q2",
            "question": "If asked a 10-marker UPSC question: 'Critically examine whether ideology is an obstacle to rational political discourse', which introductory opening is most theoretically robust?",
            "options": [
                "Ideology is purely an evil form of political propaganda that should be eradicated from modern democratic nations.",
                "While pejorative traditions from Marx to Popper treat ideology as false consciousness or dogmatic closure, Michael Freeden's morphological analysis proves that ideology is the indispensable semantic architecture of political language itself.",
                "Ideology was completely abolished after the fall of the Berlin Wall in 1989 according to international consensus.",
                "Politicians use ideology only during election campaigns to deceive illiterate voters."
            ],
            "correctIndex": 1,
            "explanation": "Option B provides the highest-scoring UPSC introduction: it juxtaposes the classical pejorative view (Marx/Popper) with modern semantic theory (Freeden), establishing theoretical depth immediately."
        }
    ],
    "ch1_ideologies_sec_11": [
        {
            "id": "ch1_ideologies_sec_11_q1",
            "question": "In 'One-Dimensional Man' (1964), what did Herbert Marcuse argue regarding Daniel Bell's 'End of Ideology' thesis?",
            "options": [
                "He agreed that industrial affluence had permanently eliminated all class conflict.",
                "He argued that proclaiming the 'end of ideology' is itself an ideology that legitimizes advanced capitalist domination by concealing structural exploitation under technocratic neutrality.",
                "He claimed that Western democracies should immediately adopt Soviet central planning.",
                "He argued that ideology had been superseded by religious fundamentalism."
            ],
            "correctIndex": 1,
            "explanation": "Marcuse argued that the celebrated 'post-ideological consensus' is in fact the most insidious form of ideology—a totalizing conformism that absorbs critical opposition and creates false consumer needs ('repressive tolerance')."
        },
        {
            "id": "ch1_ideologies_sec_11_q2",
            "question": "For a 10-marker UPSC question: 'Evaluate the End of Ideology debate in post-war political theory', which concluding synthesis is most balanced and effective?",
            "options": [
                "Daniel Bell was entirely correct, and no new ideologies have emerged in the world since 1960.",
                "Daniel Bell captured a transient historical window of Keynesian welfare stability; however, the subsequent rise of neoliberalism, identity politics, religious fundamentalism, and environmentalism demonstrates that ideology remains an enduring, dynamic engine of human political struggle.",
                "Ideology ended in the West but continues exclusively in underdeveloped Asian and African societies.",
                "All ideological debates are irrelevant because global economics is now managed entirely by artificial intelligence."
            ],
            "correctIndex": 1,
            "explanation": "Option B balances credit for Bell's historical context (post-war Keynesianism) with a rigorous critique showing how subsequent global developments disproved the permanent exhaustion of ideology."
        }
    ],
    "ch1_ideologies_sec_12": [
        {
            "id": "ch1_ideologies_sec_12_q1",
            "question": "Which scholar directly contested Francis Fukuyama's 'End of History' thesis by arguing that post-Cold War global conflicts would occur along civilizational and cultural fault lines rather than ideological ones?",
            "options": [
                "Samuel P. Huntington ('The Clash of Civilizations')",
                "Benjamin Barber ('Jihad vs. McWorld')",
                "Edward Said ('Orientalism')",
                "Joseph Nye ('Soft Power')"
            ],
            "correctIndex": 0,
            "explanation": "In 'The Clash of Civilizations and the Remaking of World Order' (1996), Samuel Huntington argued that culture and religious identity—not ideological consensus—would be the primary sources of 21st-century conflict."
        },
        {
            "id": "ch1_ideologies_sec_12_q2",
            "question": "In 'The End of History and the Last Man' (1992), Francis Fukuyama drew upon which 19th-century philosopher's dialectical concept of the 'struggle for recognition' (thymos)?",
            "options": [
                "G.W.F. Hegel (as interpreted by Alexandre Kojève)",
                "Karl Marx",
                "Friedrich Nietzsche",
                "Immanuel Kant"
            ],
            "correctIndex": 0,
            "explanation": "Fukuyama built his thesis on Hegel's master-slave dialectic and Alexandre Kojève's lectures, arguing that liberal democracy provides universal, reciprocal recognition (isothymia), satisfying the human desire for dignity."
        }
    ],

    # ---------------- CHAPTER 2 ----------------
    "ch2_liberalism_sec_intro": [
        {
            "id": "ch2_liberalism_sec_intro_q1",
            "question": "Who is universally recognized as the 'Father of Classical Liberalism', anchoring legitimate political power in contractual consent and natural rights to life, liberty, and estate?",
            "options": [
                "John Locke ('Second Treatise of Government', 1689)",
                "Thomas Hobbes ('Leviathan', 1651)",
                "Jean-Jacques Rousseau ('The Social Contract', 1762)",
                "Niccolò Machiavelli ('The Prince', 1532)"
            ],
            "correctIndex": 0,
            "explanation": "John Locke's 'Second Treatise of Government' laid the bedrock of liberalism: government as a fiduciary trust, pre-political natural rights, and the right of revolution against tyrannical overreach."
        },
        {
            "id": "ch2_liberalism_sec_intro_q2",
            "question": "Who famously declared: 'The end of law is not to abolish or restrain, but to preserve and enlarge freedom'?",
            "options": [
                "John Locke",
                "Thomas Hobbes",
                "Jeremy Bentham",
                "Montesquieu"
            ],
            "correctIndex": 0,
            "explanation": "Locke in Chapter VI of the 'Second Treatise' argued that 'where there is no law, there is no freedom', establishing the liberal principle of the Rule of Law as the protector, not suppressor, of liberty."
        }
    ],
    "ch2_liberalism_sec_2": [
        {
            "id": "ch2_liberalism_sec_2_q1",
            "question": "Which early feminist thinker wrote 'A Vindication of the Rights of Woman' (1792), applying liberal Enlightenment principles of reason and universal rights to demand equal education for women?",
            "options": [
                "Mary Wollstonecraft",
                "Harriet Taylor Mill",
                "Simone de Beauvoir",
                "Betty Friedan"
            ],
            "correctIndex": 0,
            "explanation": "Mary Wollstonecraft challenged Rousseau and Enlightenment male theorists by arguing that women possess the same rational capacity as men and that denial of education artificially creates their social subjugation."
        },
        {
            "id": "ch2_liberalism_sec_2_q2",
            "question": "If asked a 10-marker UPSC question: 'Examine the transition from Classical Liberalism to Modern Welfare Liberalism', which introductory framing is most compelling?",
            "options": [
                "Classical liberalism was completely wrong, so British politicians abandoned capitalism for communism.",
                "The evolution of liberalism from John Locke's 'negative liberty' and night-watchman state to T.H. Green's 'positive liberty' represents not an ideological rupture, but a pragmatic expansion of the core commitment to individual autonomy in response to industrial inequalities.",
                "Liberalism was invented in America to promote free trade agreements.",
                "Welfare liberalism is simply another name for totalitarian socialism."
            ],
            "correctIndex": 1,
            "explanation": "Option B captures the continuous philosophical thread (individual autonomy) while accurately explaining how the transition was a response to industrial inequality via positive liberty."
        }
    ],
    "ch2_liberalism_sec_3": [
        {
            "id": "ch2_liberalism_sec_3_q1",
            "question": "In 'Two Concepts of Liberty' (1958), how does Isaiah Berlin define 'Negative Liberty'?",
            "options": [
                "The freedom to achieve moral self-perfection through state guidance.",
                "The area within which a person can act unobstructed by others without external coercion or interference.",
                "The collective power of the working class to seize the state apparatus.",
                "A dangerous illusion that leads inevitably to totalitarianism."
            ],
            "correctIndex": 1,
            "explanation": "Berlin defined negative liberty as the absence of external obstacles: 'I am normally said to be free to the degree to which no man or body of men interferes with my activity.'"
        },
        {
            "id": "ch2_liberalism_sec_3_q2",
            "question": "Who authored 'The Constitution of Liberty' (1960) and argued that liberty is a state in which coercion of some by others is reduced as much as possible in society?",
            "options": [
                "Friedrich A. Hayek",
                "Milton Friedman",
                "Karl Popper",
                "Robert Nozick"
            ],
            "correctIndex": 0,
            "explanation": "F.A. Hayek defined freedom in 'The Constitution of Liberty' as independence from the arbitrary will of another, arguing for strict rule of law and spontaneous market order (catallaxy)."
        }
    ],
    "ch2_liberalism_sec_4": [
        {
            "id": "ch2_liberalism_sec_4_q1",
            "question": "Who famously characterized utilitarianism as a 'pig philosophy' before modifying it into qualitative utilitarianism, asserting: 'It is better to be a human being dissatisfied than a pig satisfied; better to be Socrates dissatisfied than a fool satisfied'?",
            "options": [
                "John Stuart Mill",
                "Jeremy Bentham",
                "Thomas Carlyle",
                "Herbert Spencer"
            ],
            "correctIndex": 0,
            "explanation": "J.S. Mill reformed Bentham's purely quantitative calculus ('push-pin is as good as poetry') by introducing qualitative distinctions between higher intellectual pleasures and lower bodily pleasures in 'Utilitarianism' (1861)."
        },
        {
            "id": "ch2_liberalism_sec_4_q2",
            "question": "In 'On Liberty' (1859), J.S. Mill defended absolute freedom of speech and expression on the ground that:",
            "options": [
                "All opinions, even false or offensive ones, preserve the living truth through vigorous contestation, preventing truth from degenerating into a 'dead dogma'.",
                "The government has no right to tax paper and printing presses.",
                "Speech has zero influence on human behavior.",
                "The majority opinion is always scientifically accurate."
            ],
            "correctIndex": 0,
            "explanation": "Mill argued that silencing any opinion deprives the human race: if the silenced opinion is right, we lose the chance to exchange error for truth; if wrong, we lose the clearer perception of truth produced by its collision with error."
        }
    ],
    "ch2_liberalism_sec_5": [
        {
            "id": "ch2_liberalism_sec_5_q1",
            "question": "Which classical liberal thinker advocated Social Darwinism and coined the phrase 'survival of the fittest', arguing against any state welfare for the impoverished?",
            "options": [
                "Herbert Spencer ('The Man Versus the State', 1884)",
                "Adam Smith",
                "David Ricardo",
                "Thomas Malthus"
            ],
            "correctIndex": 0,
            "explanation": "Herbert Spencer applied biological evolutionary theory to sociology, coining 'survival of the fittest' in 1864 and fiercely opposing public schools, state healthcare, and poor relief as unnatural interruptions of evolutionary progress."
        },
        {
            "id": "ch2_liberalism_sec_5_q2",
            "question": "Who argued in 'The Wealth of Nations' (1776) that individuals pursuing their self-interest are led by an 'invisible hand' to promote the public good more effectively than when intending to do so?",
            "options": [
                "Adam Smith",
                "David Hume",
                "John Locke",
                "Bernard Mandeville"
            ],
            "correctIndex": 0,
            "explanation": "Adam Smith's metaphor of the 'invisible hand' illustrated how free market price signals coordinate decentralized division of labor, maximizing overall societal wealth without central direction."
        }
    ],
    "ch2_liberalism_sec_6": [
        {
            "id": "ch2_liberalism_sec_6_q1",
            "question": "Who coined the definitive phrase defining the moral foundation of political authority: 'Will, not force, is the basis of the state'?",
            "options": [
                "T.H. Green ('Lectures on the Principles of Political Obligation')",
                "Jean-Jacques Rousseau",
                "Harold Laski",
                "Max Weber"
            ],
            "correctIndex": 0,
            "explanation": "Thomas Hill Green argued that the state commands legitimate political obligation not through physical monopoly of violence, but because citizens recognize the state as the institutional vehicle for realizing common moral goods."
        },
        {
            "id": "ch2_liberalism_sec_6_q2",
            "question": "What is T.H. Green's famous doctrine regarding the legitimate function of the state in modern welfare liberalism?",
            "options": [
                "The state must actively enforce religious doctrine on all citizens.",
                "The state's role is 'hindering hindrances'—removing socioeconomic obstacles like ignorance, disease, and poverty that prevent individuals from realizing their moral capacities.",
                "The state should confiscate all private capital and eliminate market exchange.",
                "The state should remain strictly a night-watchman with zero public services."
            ],
            "correctIndex": 1,
            "explanation": "Green argued that law cannot directly compel moral virtue, but it must 'hinder hindrances'—enacting factory acts, compulsory education, and public sanitation so that citizens have the capacity to act freely."
        }
    ],
    "ch2_liberalism_sec_8": [
        {
            "id": "ch2_liberalism_sec_8_q1",
            "question": "Who authored 'Liberalism' (1911) and formulated the theory of 'Social Justice' connecting individual freedom with collective social responsibility in early 20th-century Britain?",
            "options": [
                "L.T. Hobhouse",
                "J.A. Hobson",
                "T.H. Green",
                "John Maynard Keynes"
            ],
            "correctIndex": 0,
            "explanation": "Leonard Trelawny Hobhouse synthesized liberalism and democratic socialism in 'Liberalism' (1911), arguing that society creates wealth collaboratively and that progressive taxation ensures justice without abolishing liberty."
        },
        {
            "id": "ch2_liberalism_sec_8_q2",
            "question": "In 'A Theory of Justice' (1971), John Rawls synthesizes liberal freedom with distributive equality using which famous hypothetical thought experiment?",
            "options": [
                "The Original Position behind a 'Veil of Ignorance'",
                "The State of Nature under the Leviathan",
                "The Panopticon of utilitarian inspection",
                "The Prisoner's Dilemma"
            ],
            "correctIndex": 0,
            "explanation": "Rawls's 'Veil of Ignorance' strips parties of knowledge of their class, talents, race, and gender, leading rational actors to agree on equal basic liberties and the Difference Principle (inequalities must benefit the worst-off)."
        }
    ],
    "ch2_liberalism_sec_9": [
        {
            "id": "ch2_liberalism_sec_9_q1",
            "question": "In 'Anarchy, State, and Utopia' (1974), Robert Nozick formulated which famous slogan to refute patterned or socialist theories of distributive justice?",
            "options": [
                "'Liberty upsets patterns.'",
                "'From each according to his ability, to each according to his need.'",
                "'Property is theft.'",
                "'Man was born free, and he is everywhere in chains.'"
            ],
            "correctIndex": 0,
            "explanation": "Using the Wilt Chamberlain thought experiment, Nozick showed that voluntary exchanges by free individuals constantly disrupt any egalitarian pattern, proving that maintaining a patterned distribution requires continuous, tyrannical interference with liberty."
        },
        {
            "id": "ch2_liberalism_sec_9_q2",
            "question": "For a 10-marker UPSC question: 'Compare John Rawls and Robert Nozick on distributive justice', which conclusion provides the sharpest theoretical evaluation?",
            "options": [
                "Rawls was a dedicated communist, whereas Nozick was an anarchist who opposed all laws.",
                "While Rawls anchors justice in fairness and democratic equality via the Difference Principle, Nozick provides the quintessential libertarian defense of self-ownership and uncoerced transfer; contemporary political theory continues to negotiate this dialectic between social solidarity and absolute individual entitlement.",
                "Both thinkers agreed that the state should completely abolish private property.",
                "Rawls and Nozick are outdated because both ignored the United Nations."
            ],
            "correctIndex": 1,
            "explanation": "Option B sharply contrasts Rawls's egalitarian fairness with Nozick's entitlement theory, concluding with their enduring dialectical tension in contemporary political philosophy."
        }
    ],

    # ---------------- CHAPTER 3 ----------------
    "ch3_marxism_sec_intro": [
        {
            "id": "ch3_marxism_sec_intro_q1",
            "question": "In the 'Theses on Feuerbach' (1845), which famous 11th thesis encapsulates Karl Marx's revolutionary philosophical departure from traditional contemplative philosophy?",
            "options": [
                "'The philosophers have only interpreted the world in various ways; the point, however, is to change it.'",
                "'Workers of the world, unite! You have nothing to lose but your chains.'",
                "'Religion is the sigh of the oppressed creature, the opium of the people.'",
                "'The history of all hitherto existing society is the history of class struggles.'"
            ],
            "correctIndex": 0,
            "explanation": "Thesis 11 marks the birth of historical materialism and revolutionary praxis: philosophy must move beyond passive academic interpretation to active revolutionary transformation of material reality."
        },
        {
            "id": "ch3_marxism_sec_intro_q2",
            "question": "Which German philosopher's dialectical method did Karl Marx 'turn right side up', replacing idealistic Spirit (Geist) with material economic relations?",
            "options": [
                "G.W.F. Hegel",
                "Immanuel Kant",
                "Arthur Schopenhauer",
                "Friedrich Schelling"
            ],
            "correctIndex": 0,
            "explanation": "In 'Capital' (Vol 1, Postface), Marx famously declared: 'With Hegel, the dialectic is standing on its head. It must be turned right side up again, if you would discover the rational kernel within the mystical shell'—substituting material production for Geist."
        }
    ],
    "ch3_marxism_sec_2": [
        {
            "id": "ch3_marxism_sec_2_q1",
            "question": "In 'The Condition of the Working Class in England' (1845), which lifelong co-author of Karl Marx provided the empirical sociological investigation of industrial Manchester that influenced historical materialism?",
            "options": [
                "Friedrich Engels",
                "Moses Hess",
                "Ferdinand Lassalle",
                "Wilhelm Liebknecht"
            ],
            "correctIndex": 0,
            "explanation": "Friedrich Engels documented the horrors of child labor, disease, and urban exploitation in Manchester, furnishing Marx with empirical evidence of capitalist immiseration."
        },
        {
            "id": "ch3_marxism_sec_2_q2",
            "question": "Who formulated the 'Iron Law of Wages', asserting that market wages naturally tend toward the minimum level necessary to sustain the life of the worker, which Marx later critiqued in 'Value, Price and Profit'?",
            "options": [
                "David Ricardo (adapted by Ferdinand Lassalle)",
                "Adam Smith",
                "Thomas Malthus",
                "John Stuart Mill"
            ],
            "correctIndex": 0,
            "explanation": "David Ricardo formulated the subsistence theory of wages, popularized as the 'Iron Law of Wages' by Lassalle. Marx critiqued Lassalle for treating subsistence as a biological law rather than a historical, socially determined minimum."
        }
    ],
    "ch3_marxism_sec_3": [
        {
            "id": "ch3_marxism_sec_3_q1",
            "question": "In 'The Essence of Christianity' (1841), which Young Hegelian philosopher argued that God is merely an alienated projection of humanity's own idealized virtues, directly inspiring Marx's theory of alienation?",
            "options": [
                "Ludwig Feuerbach",
                "Bruno Bauer",
                "Max Stirner",
                "David Strauss"
            ],
            "correctIndex": 0,
            "explanation": "Feuerbach's critique of religious alienation (man creates God in his own image, then worships his own projection) was secularized by Marx, who showed that in capitalism, man creates capital and then bows to it as an alien master."
        },
        {
            "id": "ch3_marxism_sec_3_q2",
            "question": "Which French utopian socialist coined the phrase 'Property is theft!' in 'What is Property?' (1840), provoking fierce polemical debates with Karl Marx?",
            "options": [
                "Pierre-Joseph Proudhon",
                "Charles Fourier",
                "Henri de Saint-Simon",
                "Louis Blanc"
            ],
            "correctIndex": 0,
            "explanation": "Proudhon's 'Property is theft!' sparked Marx's rebuttal in 'The Poverty of Philosophy' (1847), where Marx attacked Proudhon's petit-bourgeois mutualism and lack of rigorous materialist economics."
        }
    ],
    "ch3_marxism_sec_4": [
        {
            "id": "ch3_marxism_sec_4_q1",
            "question": "Which historic text opens with the famous sentence: 'A spectre is haunting Europe—the spectre of communism'?",
            "options": [
                "'The Communist Manifesto' (Karl Marx & Friedrich Engels, 1848)",
                "'Das Kapital' (1867)",
                "'The German Ideology' (1845)",
                "'State and Revolution' (1917)"
            ],
            "correctIndex": 0,
            "explanation": "The 1848 'Manifesto of the Communist Party' opened with the spectre of communism and closed with the clarion call: 'Workers of all countries, unite!'."
        },
        {
            "id": "ch3_marxism_sec_4_q2",
            "question": "In 'The Communist Manifesto', how do Marx and Engels describe the modern state executive?",
            "options": [
                "'A neutral mediator balancing the plural interests of democratic citizens.'",
                "'A committee for managing the common affairs of the whole bourgeoisie.'",
                "'An eternal entity ordained by divine right.'",
                "'A voluntary club designed to promote ethical virtue.'"
            ],
            "correctIndex": 1,
            "explanation": "Marx and Engels characterized the executive of the modern representative state as 'but a committee for managing the common affairs of the whole bourgeoisie', establishing the classical instrumentalist view of the state."
        }
    ],
    "ch3_marxism_sec_5": [
        {
            "id": "ch3_marxism_sec_5_q1",
            "question": "In 'Das Kapital' (Volume 1, 1867), what does Marx identify as the root source of capitalist surplus value and profit?",
            "options": [
                "Unpaid surplus labor extracted from workers beyond the labor-time required to reproduce their labor-power.",
                "Arbitrary price markups added by merchant traders during retail sale.",
                "Natural interest generated organically by technological machinery.",
                "Managerial ingenuity and entrepreneurial risk-taking."
            ],
            "correctIndex": 0,
            "explanation": "Marx's Labor Theory of Value demonstrates that capital purchases 'labor-power' at its exchange value (subsistence), but extracts 'surplus labor-time' during the working day, generating unpaid surplus value (m)."
        },
        {
            "id": "ch3_marxism_sec_5_q2",
            "question": "What term does Marx use in 'Capital' to describe the psychological illusion where social relations between human producers appear as objective, independent relations between commodities in the market?",
            "options": [
                "Commodity Fetishism (Warenfetischismus)",
                "False Consciousness",
                "Reification",
                "Cultural Hegemony"
            ],
            "correctIndex": 0,
            "explanation": "In Section 4 of Chapter 1 of 'Capital', Marx analyzes 'The Fetishism of Commodities and the Secret Thereof', where products of human hands appear endowed with independent mystical lives of their own."
        }
    ],
    "ch3_marxism_sec_6": [
        {
            "id": "ch3_marxism_sec_6_q1",
            "question": "In 'What Is to Be Done?' (1902), V.I. Lenin argued that the working class left to its own spontaneous trade union consciousness can only achieve:",
            "options": [
                "Trade unionism (demanding higher wages within capitalism), necessitating a disciplined 'Vanguard Party' of professional revolutionaries to inject socialist consciousness from without.",
                "Immediate communist revolution without leadership.",
                "Anarcho-syndicalism.",
                "Complete bourgeois ideological surrender."
            ],
            "correctIndex": 0,
            "explanation": "Lenin argued that spontaneous working-class struggle produces only 'trade-union consciousness'; socialist political consciousness must be brought to the workers 'from without' by a vanguard party of professional revolutionaries."
        },
        {
            "id": "ch3_marxism_sec_6_q2",
            "question": "Who authored 'Imperialism, the Highest Stage of Capitalism' (1916), demonstrating that colonial expansion and finance capital export had temporarily delayed the internal crisis of Western capitalism?",
            "options": [
                "V.I. Lenin",
                "Rosa Luxemburg",
                "Rudolf Hilferding",
                "Nikolai Bukharin"
            ],
            "correctIndex": 0,
            "explanation": "Lenin integrated J.A. Hobson and Rudolf Hilferding's insights, explaining that monopolistic finance capital partitioned the globe, using super-profits from colonial exploitation to bribe the domestic working-class aristocracy ('labor aristocracy')."
        }
    ],
    "ch3_marxism_sec_7": [
        {
            "id": "ch3_marxism_sec_7_q1",
            "question": "In 'Reform or Revolution' (1899), which revolutionary Marxist fiercely critiqued Eduard Bernstein's revisionism, arguing that parliamentary reforms cannot abolish wage slavery without the revolutionary overthrow of political power?",
            "options": [
                "Rosa Luxemburg",
                "Clara Zetkin",
                "Nadezhda Krupskaya",
                "Alexandra Kollontai"
            ],
            "correctIndex": 0,
            "explanation": "Rosa Luxemburg attacked Bernstein's evolutionary gradualism, asserting that reforms within capitalism are quantitative improvements, whereas socialism requires a qualitative leap achieved through the conquest of political power."
        },
        {
            "id": "ch3_marxism_sec_7_q2",
            "question": "Which Chinese leader adapted Marxism to peasant conditions by formulating the strategy of 'Protracted People's War' and 'encircling the cities from the countryside'?",
            "options": [
                "Mao Zedong",
                "Deng Xiaoping",
                "Zhou Enlai",
                "Liu Shaoqi"
            ],
            "correctIndex": 0,
            "explanation": "Mao shifted the revolutionary vanguard from the urban industrial proletariat to the peasant masses in 'On Protracted War' (1938), pioneering guerilla warfare and the 'Mass Line'."
        }
    ],
    "ch3_marxism_sec_8": [
        {
            "id": "ch3_marxism_sec_8_q1",
            "question": "In 'The Open Society and Its Enemies' (Vol 2, 1945), why did Karl Popper label Karl Marx a 'false prophet'?",
            "options": [
                "Because Marx claimed to have discovered inexorable historical laws of development (historicism) that rendered his theories unfalsifiable and dogmatic.",
                "Because Marx refused to support trade unions.",
                "Because Marx was an agent of the British monarchy.",
                "Because Marx supported absolute laissez-faire capitalism."
            ],
            "correctIndex": 0,
            "explanation": "Popper attacked Marx's historicism—the belief that history unfolds according to deterministic laws—arguing that historicist prophecies inevitably justify totalitarian tyranny and sacrifice human freedom."
        },
        {
            "id": "ch3_marxism_sec_8_q2",
            "question": "For a 10-marker UPSC question: 'Examine the contemporary relevance of Karl Marx in the 21st century', which concluding synthesis is most impactful?",
            "options": [
                "Marxism is permanently dead because all communist regimes collapsed in 1991.",
                "While Marx's political predictions regarding the withering away of the state and proletarian revolution were not borne out in the West, his structural critique of capitalism—financialization, rising wealth inequality, periodic crises, and the alienation of labor—remains an indispensable analytical mirror for diagnosing 21st-century global capitalism.",
                "Marx's only contribution was the invention of paper currency.",
                "Marx has no relevance because all modern workers own corporate shares."
            ],
            "correctIndex": 1,
            "explanation": "Option B separates failed political teleology (withering of the state) from Marx's enduring critique of political economy (inequality, crises, alienation), providing the balanced nuance required for top UPSC scores."
        }
    ],
    "ch3_marxism_sec_11": [
        {
            "id": "ch3_marxism_sec_11_q1",
            "question": "In 'The Critique of the Gotha Programme' (1875), what transitional political phase does Marx specify between capitalist society and communist society?",
            "options": [
                "The Revolutionary Dictatorship of the Proletariat",
                "A permanent constitutional parliamentary republic",
                "A technocratic managerial state",
                "Immediate stateless anarchism without transition"
            ],
            "correctIndex": 0,
            "explanation": "Marx wrote: 'Between capitalist and communist society lies the period of the revolutionary transformation of the one into the other. Corresponding to this is also a political transition period in which the state can be nothing but the revolutionary dictatorship of the proletariat.'"
        },
        {
            "id": "ch3_marxism_sec_11_q2",
            "question": "In 'The State and Revolution' (1917), V.I. Lenin asserts that the proletarian state will not be 'abolished', but rather:",
            "options": [
                "It 'withers away' as the abolition of classes eliminates the need for a specialized apparatus of systematic violence.",
                "It will expand into an eternal global bureaucracy.",
                "It will merge into a holy theocracy.",
                "It will be purchased by foreign syndicates."
            ],
            "correctIndex": 0,
            "explanation": "Lenin, echoing Engels's 'Anti-Dühring', insisted that the bourgeois state is destroyed in the revolution, whereas the proletarian state (dictatorship of the proletariat) gradually 'withers away' (otmiranie) as class antagonisms disappear."
        }
    ],
    "ch3_marxism_sec_12": [
        {
            "id": "ch3_marxism_sec_12_q1",
            "question": "In 'The Eighteenth Brumaire of Louis Bonaparte' (1852), which famous opening line did Marx pen regarding the recurrence of historical events?",
            "options": [
                "'Hegel remarks somewhere that all great world-historic facts and personages appear, so to speak, twice. He forgot to add: the first time as tragedy, the second time as farce.'",
                "'All that is solid melts into air, all that is holy is profaned.'",
                "'Men make their own history, but they do not make it as they please under circumstances chosen by themselves.'",
                "'The executive of the modern state is a committee for managing the common affairs of the bourgeoisie.'"
            ],
            "correctIndex": 0,
            "explanation": "Marx compared Napoleon I (tragedy) with his nephew Napoleon III's 1851 coup d'état (farce), illustrating relative autonomy and class alliances in 'The Eighteenth Brumaire'."
        },
        {
            "id": "ch3_marxism_sec_12_q2",
            "question": "In 'The Eighteenth Brumaire', Marx famously articulated which foundational thesis on human historical agency?",
            "options": [
                "'Men make their own history, but they do not make it as they please; they do not make it under self-selected circumstances, but under circumstances existing already, given and transmitted from the past.'",
                "'Individual heroes dictate the course of history entirely through their charismatic willpower.'",
                "'History is governed purely by biological genetics.'",
                "'Human agency is an illusion with zero influence on production.'"
            ],
            "correctIndex": 0,
            "explanation": "This famous quote synthesizes human agency and material structure, demonstrating that revolutionary action takes place within historically inherited structural constraints."
        }
    ],
    "ch3_marxism_sec_22": [
        {
            "id": "ch3_marxism_sec_22_q1",
            "question": "Which Neo-Marxist scholar formulated the 'World-Systems Theory', dividing the global capitalist economy into 'Core', 'Semi-Periphery', and 'Periphery'?",
            "options": [
                "Immanuel Wallerstein",
                "Andre Gunder Frank",
                "Samir Amin",
                "Fernando Henrique Cardoso"
            ],
            "correctIndex": 0,
            "explanation": "Immanuel Wallerstein ('The Modern World-System', 1974) analyzed global capitalism as an integrated historical world-economy where the dominant Core extracts surplus value from the peripheral nations through unequal exchange."
        },
        {
            "id": "ch3_marxism_sec_22_q2",
            "question": "In 'Capitalism and Underdevelopment in Latin America' (1967), Andre Gunder Frank formulated which influential Dependency Theory thesis?",
            "options": [
                "The 'Development of Underdevelopment'—showing that third-world poverty is actively produced by the integration of satellite economies into the global metropolitan capitalist system.",
                "That third-world nations merely suffer from a lack of Western foreign direct investment.",
                "That traditional culture is the only obstacle to economic modernization.",
                "That peripheral nations naturally evolve into core nations without conflict."
            ],
            "correctIndex": 0,
            "explanation": "Frank refuted modernization theory (Rostow), proving that historical underdevelopment was not an original traditional stage, but the direct structural consequence of colonial extraction by imperialist metropoles."
        }
    ],
    "ch3_marxism_sec_23": [
        {
            "id": "ch3_marxism_sec_23_q1",
            "question": "In 'Accumulation on an World Scale' (1970), which Egyptian-French Marxist economist conceptualized 'Unequal Exchange' and championed 'Delinking' from the global capitalist market?",
            "options": [
                "Samir Amin",
                "Frantz Fanon",
                "Amílcar Cabral",
                "Walter Rodney"
            ],
            "correctIndex": 0,
            "explanation": "Samir Amin argued that the global law of value systematically undervalues peripheral labor, urging postcolonial nations to 'delink' their development strategies from the dictates of Western imperialist capital."
        },
        {
            "id": "ch3_marxism_sec_23_q2",
            "question": "Who authored 'How Europe Underdeveloped Africa' (1972), providing a landmark historical materialist analysis of African colonial exploitation?",
            "options": [
                "Walter Rodney",
                "Kwame Nkrumah",
                "Julius Nyerere",
                "Thomas Sankara"
            ],
            "correctIndex": 0,
            "explanation": "Guyanese Marxist historian Walter Rodney demonstrated that European capitalist expansion drained Africa of its agricultural wealth, minerals, and human labor, actively creating underdevelopment."
        }
    ],
    "ch3_marxism_sec_25": [
        {
            "id": "ch3_marxism_sec_25_q1",
            "question": "In 'The Theory of Communicative Action' (1981), Jürgen Habermas reformulates critical theory by shifting the focal point of human emancipation from instrumental labor to:",
            "options": [
                "Communicative Rationality—uncoerced, intersubjective discourse aimed at mutual consensus in the 'Ideal Speech Situation'.",
                "Violent insurrection by rural peasant guerillas.",
                "Unrestricted algorithmic financial transactions.",
                "Spiritual meditation and ascetic renunciation."
            ],
            "correctIndex": 0,
            "explanation": "Habermas moved beyond Adorno and Horkheimer's pessimism by proposing communicative reason: communicative action oriented toward mutual understanding as the foundation for democratic legitimacy and social critique."
        },
        {
            "id": "ch3_marxism_sec_25_q2",
            "question": "In 'The Structural Transformation of the Public Sphere' (1962), Habermas analyzed the decline of the bourgeois public sphere due to which modern phenomenon?",
            "options": [
                "The 'Colonization of the Lifeworld' by bureaucratic state systems and commercialized consumer mass media.",
                "The rise of universal literacy.",
                "The expansion of parliamentary debates.",
                "The total absence of print capitalism."
            ],
            "correctIndex": 0,
            "explanation": "Habermas showed that the rational-critical public sphere of 18th-century coffeehouses degraded into passive consumer spectacle and PR spin, as the bureaucratic-administrative state and market systems colonized the lifeworld."
        }
    ],
    "ch3_marxism_sec_28": [
        {
            "id": "ch3_marxism_sec_28_q1",
            "question": "In 'Reading Capital' (1965) and 'For Marx' (1965), which French Marxist introduced Structural Marxism and proposed an 'epistemological break' between the young humanist Marx and the mature scientific Marx?",
            "options": [
                "Louis Althusser",
                "Jean-Paul Sartre",
                "Michel Foucault",
                "Henri Lefebvre"
            ],
            "correctIndex": 0,
            "explanation": "Louis Althusser rejected humanist and Hegelian interpretations of Marx, arguing that in 1845 Marx made an 'epistemological break' from speculative humanism into the rigorous science of historical materialism."
        },
        {
            "id": "ch3_marxism_sec_28_q2",
            "question": "What is Louis Althusser's concept of 'Interpellation' in his theory of ideology?",
            "options": [
                "The process by which ideology 'hails' concrete individuals and transforms them into obedient ideological subjects (e.g., 'Hey, you there!').",
                "The military arrest of political dissidents by the police.",
                "The mathematical calculation of surplus value in factories.",
                "The voluntary voting process during national general elections."
            ],
            "correctIndex": 0,
            "explanation": "In 'Ideology and Ideological State Apparatuses' (1970), Althusser used the police hailing metaphor to illustrate that ideology is not an illusion in our heads, but material practices through which we are interpellated as subjects."
        }
    ],
    "ch3_marxism_sec_29": [
        {
            "id": "ch3_marxism_sec_29_q1",
            "question": "In 'The Concept of the Political' (1932), which controversial jurist defined the political strictly through the existential distinction between 'Friend and Enemy'?",
            "options": [
                "Carl Schmitt",
                "Hans Kelsen",
                "Max Weber",
                "Leo Strauss"
            ],
            "correctIndex": 0,
            "explanation": "Carl Schmitt argued that just as moral judgment revolves around good and evil and aesthetics around beauty and ugliness, the specific criterion of politics is the distinction between friend and enemy."
        },
        {
            "id": "ch3_marxism_sec_29_q2",
            "question": "In 'Hegemony and Socialist Strategy' (1985), which Post-Marxist theorists abandoned class essentialism to propose 'Radical and Plural Democracy'?",
            "options": [
                "Ernesto Laclau and Chantal Mouffe",
                "Michael Hardt and Antonio Negri",
                "Slavoj Žižek and Alain Badiou",
                "Perry Anderson and Alex Callinicos"
            ],
            "correctIndex": 0,
            "explanation": "Laclau and Mouffe utilized Gramscian hegemony and post-structuralism to decenter the proletariat, arguing that democratic socialist struggle must link multiple social movements (feminism, anti-racism, ecology) through discursive articulation."
        }
    ],
    "ch3_marxism_sec_32": [
        {
            "id": "ch3_marxism_sec_32_q1",
            "question": "Which French utopian socialist proposed the reorganization of society into harmonious cooperative communities called 'Phalansteries' based on human passions?",
            "options": [
                "Charles Fourier",
                "Robert Owen",
                "Claude Henri de Saint-Simon",
                "Étienne Cabet"
            ],
            "correctIndex": 0,
            "explanation": "Charles Fourier designed self-contained cooperative communities of 1,620 people called Phalanxes, where work was organized according to human psychological passions rather than capitalist competition."
        },
        {
            "id": "ch3_marxism_sec_32_q2",
            "question": "Which British industrialist and socialist reformer established the model cooperative factory community of New Lanark in Scotland and New Harmony in Indiana?",
            "options": [
                "Robert Owen",
                "William Morris",
                "John Ruskin",
                "Thomas More"
            ],
            "correctIndex": 0,
            "explanation": "Robert Owen limited working hours, abolished child labor under age 10, established infant schools, and pioneered the cooperative movement, proving humane industrial organization was economically viable."
        }
    ],

    # ---------------- CHAPTER 4 ----------------
    "ch4_socialism_fascism_sec_3": [
        {
            "id": "ch4_socialism_fascism_sec_3_q1",
            "question": "In 'Socialism: Utopian and Scientific' (1880), Friedrich Engels characterized early French and British socialists (Saint-Simon, Fourier, Owen) as 'Utopian' because:",
            "options": [
                "They appealed to moral reason and wealthy philanthropists rather than rooting socialism in the objective historical contradictions of class struggle and material production.",
                "They advocated the total extinction of the human race.",
                "They were secret agents of the European feudal aristocracy.",
                "They supported absolute unregulated laissez-faire capitalism."
            ],
            "correctIndex": 0,
            "explanation": "Engels praised their genius and moral critique of capitalism, but demonstrated that their socialism was 'utopian' because it relied on moral appeals and experimental colonies rather than the scientific laws of historical materialism."
        },
        {
            "id": "ch4_socialism_fascism_sec_3_q2",
            "question": "Who famously declared that 'Society should be organized for the direct moral and material amelioration of the class that is the most numerous and the most poor'?",
            "options": [
                "Claude Henri de Saint-Simon",
                "Karl Marx",
                "Robert Owen",
                "Charles Fourier"
            ],
            "correctIndex": 0,
            "explanation": "Henri de Saint-Simon's 'Nouveau Christianisme' (1825) advocated technocratic, planned industrial production managed by scientists and industrialists for the upliftment of the poorest class."
        }
    ],
    "ch4_socialism_fascism_sec_4": [
        {
            "id": "ch4_socialism_fascism_sec_4_q1",
            "question": "In 'Evolutionary Socialism' (1899), who initiated the Revisionist debate within the German Social Democratic Party (SPD), declaring: 'The final aim, whatever it may be, is nothing to me; the movement is everything'?",
            "options": [
                "Eduard Bernstein",
                "Karl Kautsky",
                "August Bebel",
                "Ferdinand Lassalle"
            ],
            "correctIndex": 0,
            "explanation": "Eduard Bernstein observed that capitalism was adapting, the middle class was growing, and workers were winning legislative gains, concluding that socialism could be achieved incrementally through democratic parliamentarism."
        },
        {
            "id": "ch4_socialism_fascism_sec_4_q2",
            "question": "Which orthodox Marxist theorist opposed Bernstein in the Revisionist controversy, authoring 'The Class Struggle' (Erfurt Program) and defending classical Marxist orthodoxy?",
            "options": [
                "Karl Kautsky",
                "Rosa Luxemburg",
                "Georgi Plekhanov",
                "Rudolf Hilferding"
            ],
            "correctIndex": 0,
            "explanation": "Karl Kautsky, known as the 'Pope of Marxism', defended orthodox Marxism against Bernstein, asserting that parliament should be used for agitation while anticipating the inevitable systemic collapse of capitalism."
        }
    ],
    "ch4_socialism_fascism_sec_5": [
        {
            "id": "ch4_socialism_fascism_sec_5_q1",
            "question": "Which strategy characterized the Fabian Society's approach to implementing socialism in Britain (Sidney & Beatrice Webb, G.B. Shaw)?",
            "options": [
                "The 'Inevitability of Gradualism' and permeating state institutions, civil servants, and municipal councils with technocratic socialist expertise.",
                "Armed guerrilla struggle in the countryside.",
                "General strike and industrial sabotage.",
                "Total rejection of all state and legal institutions."
            ],
            "correctIndex": 0,
            "explanation": "The Fabians (named after Roman general Quintus Fabius Maximus Cunctator) rejected violent revolution in favor of gradualism, empirical research, and municipal socialism ('gas and water socialism')."
        },
        {
            "id": "ch4_socialism_fascism_sec_5_q2",
            "question": "In 'Reflections on Violence' (1908), which revolutionary syndicalist thinker advocated the 'Myth of the General Strike' and heroic violence to overthrow capitalism?",
            "options": [
                "Georges Sorel",
                "Hubert Lagardelle",
                "Fernand Pelloutier",
                "Émile Pouget"
            ],
            "correctIndex": 0,
            "explanation": "Georges Sorel argued that political action and rationalist debates are decadent; the working class must be energized through revolutionary 'myth'—the catastrophic General Strike—to rejuvenate society through direct action."
        }
    ],
    "ch4_socialism_fascism_sec_8": [
        {
            "id": "ch4_socialism_fascism_sec_8_q1",
            "question": "What is the central institutional principle of Syndicalism (from the French 'syndicat') regarding the governance of a post-capitalist society?",
            "options": [
                "Industries should be directly owned and democratically managed by trade unions of workers, replacing both the capitalist class and the centralized state.",
                "All economic power should be centralized in a single national planning ministry in the capital city.",
                "Feudal landlords should retain ownership while workers receive cash dividends.",
                "Private corporations should be subsidized by the central bank."
            ],
            "correctIndex": 0,
            "explanation": "Syndicalism rejects state socialism, proposing that decentralized industrial trade unions manage production directly, using direct action and the general strike to dismantle the bourgeois state."
        },
        {
            "id": "ch4_socialism_fascism_sec_8_q2",
            "question": "Which English political theorist and historian was the primary champion of 'Guild Socialism', advocating a system of industrial democracy combining functional guilds with a democratic state?",
            "options": [
                "G.D.H. Cole ('Guild Socialism Restated', 1920)",
                "Harold Laski",
                "R.H. Tawney",
                "William Morris"
            ],
            "correctIndex": 0,
            "explanation": "G.D.H. Cole formulated Guild Socialism as a middle ground between state socialism and syndicalism, balancing functional economic democracy (workers managing industries through guilds) with civic democracy (the state representing consumer/civic interests)."
        }
    ],
    "ch4_socialism_fascism_sec_9": [
        {
            "id": "ch4_socialism_fascism_sec_9_q1",
            "question": "In 'The Acquisitive Society' (1920) and 'Equality' (1931), which Christian socialist and economic historian attacked unearned income and defended moral egalitarianism?",
            "options": [
                "R.H. Tawney",
                "William Temple",
                "G.D.H. Cole",
                "Harold Laski"
            ],
            "correctIndex": 0,
            "explanation": "R.H. Tawney argued that modern capitalism is corrupted by an 'acquisitive' ethos that awards wealth without functional social obligation, proposing that industry should serve moral human purposes and common social welfare."
        },
        {
            "id": "ch4_socialism_fascism_sec_9_q2",
            "question": "What is the foundational distinction between Guild Socialism and Orthodox Marxist State Socialism?",
            "options": [
                "Guild Socialism rejects bureaucratic state ownership of production, advocating decentralized self-government of industry by workers organized into functional guilds.",
                "Guild Socialism demands absolute monarchy.",
                "Guild Socialism supports unregulated multinational corporations.",
                "Guild Socialism requires the complete abolition of all labor unions."
            ],
            "correctIndex": 0,
            "explanation": "Guild socialism warned against the danger of replacing private capitalists with a tyrannical state bureaucracy ('state capitalism'), championing grassroots industrial democracy and functional representation."
        }
    ],
    "ch4_socialism_fascism_sec_10": [
        {
            "id": "ch4_socialism_fascism_sec_10_q1",
            "question": "In 'The Future of Socialism' (1956), which British Labour revisionist argued that ownership of the means of production is no longer the defining socialist issue, defining socialism instead as social equality and welfare?",
            "options": [
                "Anthony Crosland",
                "Aneurin Bevan",
                "Harold Wilson",
                "Clement Attlee"
            ],
            "correctIndex": 0,
            "explanation": "C.A.R. Crosland argued that the 'managerial revolution' separated ownership from control in capitalism; therefore, socialists should prioritize progressive taxation, comprehensive education, and reducing class division rather than widespread nationalization."
        },
        {
            "id": "ch4_socialism_fascism_sec_10_q2",
            "question": "Who formulated the concept of the 'Third Way' in modern social democracy, advocating a synthesis of market dynamism and social justice (embraced by Tony Blair and Bill Clinton)?",
            "options": [
                "Anthony Giddens ('The Third Way: The Renewal of Social Democracy', 1998)",
                "David Held",
                "Jürgen Habermas",
                "Ulrich Beck"
            ],
            "correctIndex": 0,
            "explanation": "Sociologist Anthony Giddens provided the theoretical architecture for the 'Third Way', moving beyond classical social democracy and neoliberalism by embracing market mechanisms, entrepreneurial culture, and active welfare ('no rights without responsibilities')."
        }
    ],
    "ch4_socialism_fascism_sec_11": [
        {
            "id": "ch4_socialism_fascism_sec_11_q1",
            "question": "In 'A Grammar of Politics' (1925), which prominent British socialist and pluralist theorist argued that 'Equality means that no man shall be so poor as to be able to be bought, and none so rich as to be able to buy another'?",
            "options": [
                "Harold Laski",
                "R.H. Tawney",
                "G.D.H. Cole",
                "Ernest Barker"
            ],
            "correctIndex": 0,
            "explanation": "Harold Laski anchored equality in the prohibition of exploitative power: 'Equality means the absence of special privilege' and 'adequate opportunities are laid open to all'."
        },
        {
            "id": "ch4_socialism_fascism_sec_11_q2",
            "question": "How does Socialist Equality fundamentally depart from Classical Liberal Equality of Opportunity?",
            "options": [
                "Socialism rejects formal equal opportunity as a competitive race that legitimizes massive unequal outcomes, demanding instead substantive equality of condition, social dignity, and the abolition of class exploitation.",
                "Socialism demands that everyone receive precisely the same pair of shoes and identical food rations.",
                "Socialism advocates hereditary aristocratic privilege.",
                "Socialism rejects all forms of human rights."
            ],
            "correctIndex": 0,
            "explanation": "Socialists critique formal equal opportunity as a 'runner's race' where participants have unequal starting points; they prioritize equality of condition and basic fulfillment of human needs over competitive meritocracy."
        }
    ],
    "ch4_socialism_fascism_sec_12": [
        {
            "id": "ch4_socialism_fascism_sec_12_q1",
            "question": "Which Scandinavian political model epitomizes 'Democratic Socialism / Social Democracy' through universal welfare, tri-partite collective bargaining, and compressed wage disparities?",
            "options": [
                "The Nordic Model (e.g., Sweden's Rehn–Meidner Model and 'Folkhemmet')",
                "The Washington Consensus",
                "The Chicago School Model",
                "The East Asian Tigers Model"
            ],
            "correctIndex": 0,
            "explanation": "The Nordic Model, pioneered by Sweden's Social Democratic Party (SAP) under Per Albin Hansson's 'Folkhemmet' (The People's Home), balanced private enterprise with strong trade unions, universal healthcare, and generous welfare safety nets."
        },
        {
            "id": "ch4_socialism_fascism_sec_12_q2",
            "question": "For a 10-marker UPSC question: 'Differentiate between Democratic Socialism and Social Democracy', which distinction is most conceptually accurate?",
            "options": [
                "There is zero distinction; both words are entirely interchangeable in political philosophy.",
                "Social Democracy seeks to reform and humanize capitalism through welfare provision and state regulation, whereas Democratic Socialism retains the long-term goal of transcending capitalism by replacing private ownership of major means of production with democratic public and cooperative control.",
                "Social Democracy is fascist, while Democratic Socialism is monarchist.",
                "Democratic Socialism rejects elections, whereas Social Democracy embraces them."
            ],
            "correctIndex": 1,
            "explanation": "Option B provides the precise academic distinction: Social Democracy accepts the capitalist market economy while mitigating its inequalities via welfare; Democratic Socialism aims to structurally replace capitalism through democratic ownership of capital."
        }
    ],
    "ch4_socialism_fascism_sec_13": [
        {
            "id": "ch4_socialism_fascism_sec_13_q1",
            "question": "In 'Post-Capitalism: A Guide to Our Future' (2015), which author argues that collaborative information technology, open-source software, and the zero marginal cost phenomenon are undermining capitalist price mechanisms?",
            "options": [
                "Paul Mason",
                "David Graeber ('Bullshit Jobs')",
                "Thomas Piketty ('Capital in the Twenty-First Century')",
                "Yanis Varoufakis"
            ],
            "correctIndex": 0,
            "explanation": "Paul Mason argued that information goods, which can be duplicated endlessly at near-zero marginal cost, cannot be efficiently priced by market dynamics, opening historical pathways toward collaborative post-capitalism."
        },
        {
            "id": "ch4_socialism_fascism_sec_13_q2",
            "question": "In 'Capital in the Twenty-First Century' (2013), Thomas Piketty identified which fundamental economic inequality formula demonstrating the systemic tendency of capitalism toward hyper-inequality?",
            "options": [
                "r > g (the rate of return on capital exceeds the rate of economic growth)",
                "e = mc^2",
                "s = i (savings equals investment)",
                "p = mv (price equals money times velocity)"
            ],
            "correctIndex": 0,
            "explanation": "Piketty's empirical data over 250 years demonstrated that whenever the rate of return on capital (r) outpaces overall economic growth (g), inherited wealth concentrates exponentially, requiring progressive global capital taxation."
        }
    ],
    "ch4_socialism_fascism_sec_14": [
        {
            "id": "ch4_socialism_fascism_sec_14_q1",
            "question": "In 'The Road to Serfdom' (1944), F.A. Hayek dedicated his book to 'The Socialists of All Parties' to argue that:",
            "options": [
                "Any government attempting central economic planning must inevitably destroy individual liberty and lead society down the road to totalitarian tyranny.",
                "Socialism had already eliminated all European poverty.",
                "Socialist trade unions should take over the Bank of England.",
                "All capitalist corporations should be nationalized."
            ],
            "correctIndex": 0,
            "explanation": "Hayek argued that democratic socialists sincerely desire freedom, but the economic controls required to implement central planning inevitably demand arbitrary bureaucratic coercion, culminating in authoritarian serfdom."
        },
        {
            "id": "ch4_socialism_fascism_sec_14_q2",
            "question": "For a 10-marker UPSC question: 'Evaluate the ideological viability of Socialism in the 21st Century', which concluding analysis is most balanced?",
            "options": [
                "Socialism is completely extinct because everyone now works in private tech companies.",
                "While 20th-century authoritarian state socialism collapsed under bureaucratic centralism, 21st-century socialism has reconstituted itself around ecological sustainability (Eco-Socialism), workplace democracy, universal basic services, and democratic pushbacks against hyper-inequality, proving that the socialist moral impulse remains an enduring critique of unbridled global capitalism.",
                "Socialism was outlawed by the United Nations Security Council.",
                "Socialism will immediately replace world currencies by next year."
            ],
            "correctIndex": 1,
            "explanation": "Option B balances historical recognition of failed 20th-century state planning with the vibrant emergence of 21st-century eco-socialism and egalitarian critiques of corporate financialization."
        }
    ],
    "ch4_socialism_fascism_sec_21": [
        {
            "id": "ch4_socialism_fascism_sec_21_q1",
            "question": "In 'Mein Kampf' (1925), which pseudo-scientific concept formed Adolf Hitler's ideological justification for territorial aggression in Eastern Europe?",
            "options": [
                "Lebensraum ('Living space' for the Aryan master race)",
                "Glasnost",
                "Perestroika",
                "Dialectical Materialism"
            ],
            "correctIndex": 0,
            "explanation": "Hitler synthesised aggressive Social Darwinism and biological anti-Semitism to demand 'Lebensraum' in Eastern Europe, subjugating or exterminating Slavic and Jewish populations to sustain the German racial Reich."
        },
        {
            "id": "ch4_socialism_fascism_sec_21_q2",
            "question": "What is the totalitarian leadership principle in Nazi ideology that mandated unconditional obedience to the dictator, asserting that the leader's will is the supreme source of all law?",
            "options": [
                "Führerprinzip ('Leader Principle')",
                "Gleichschaltung",
                "Volksgemeinschaft",
                "Blut und Boden"
            ],
            "correctIndex": 0,
            "explanation": "The 'Führerprinzip' placed the Führer's word above all written constitutional law, asserting authority downward and absolute responsibility upward, destroying all democratic checks and balances."
        }
    ],
    "ch4_socialism_fascism_sec_24": [
        {
            "id": "ch4_socialism_fascism_sec_24_q1",
            "question": "Which political scientist authored 'Fascism: A Warning' (2018) and 'The Anatomy of Fascism' (2004), defining fascism as a form of political behavior marked by obsessive preoccupation with community decline, humiliation, or victimhood?",
            "options": [
                "Robert O. Paxton",
                "Francis Fukuyama",
                "Noam Chomsky",
                "Samuel Huntington"
            ],
            "correctIndex": 0,
            "explanation": "Robert O. Paxton's landmark definition focuses on functional political behavior: obsessive victimhood, cults of unity and purity, compensatory cults of violence, and alliance with traditional conservative elites."
        },
        {
            "id": "ch4_socialism_fascism_sec_24_q2",
            "question": "In 'Ur-Fascism' (1995), Italian philosopher Umberto Eco identified 14 general features of eternal fascism. Which of the following is NOT one of Eco's features?",
            "options": [
                "Cult of tradition and rejection of modernism.",
                "Fear of difference and appeal to social frustration.",
                "Commitment to dialectical materialism and working-class internationalism.",
                "Selective populism, machismo, and disdain for democratic debate."
            ],
            "correctIndex": 2,
            "explanation": "Dialectical materialism and internationalism are Marxist concepts that fascism violently suppresses. Eco's Ur-Fascism centers on anti-rationalism, obsession with plots, machismo, and cult of death."
        }
    ],
    "ch4_socialism_fascism_sec_26": [
        {
            "id": "ch4_socialism_fascism_sec_26_q1",
            "question": "Which 1860 book by John Ruskin fundamentally altered Mahatma Gandhi's life in South Africa, leading him to translate it into Gujarati as 'Sarvodaya' (Welfare of All)?",
            "options": [
                "'Unto This Last'",
                "'Modern Painters'",
                "'The Stones of Venice'",
                "'Sesame and Lilies'"
            ],
            "correctIndex": 0,
            "explanation": "In his autobiography, Gandhi recounts reading Ruskin's 'Unto This Last' during a train journey from Johannesburg to Durban in 1904: 'It gripped me. I could not get any sleep... I arose with the dawn, ready to reduce these principles to practice' (founding Phoenix Settlement)."
        },
        {
            "id": "ch4_socialism_fascism_sec_26_q2",
            "question": "Which Russian author of 'The Kingdom of God Is Within You' (1894) exerted profound intellectual influence on Gandhi's commitment to absolute non-violence and Christian anarchism?",
            "options": [
                "Leo Tolstoy",
                "Fyodor Dostoevsky",
                "Peter Kropotkin",
                "Mikhail Bakunin"
            ],
            "correctIndex": 0,
            "explanation": "Tolstoy corresponded directly with the young Gandhi in South Africa, demonstrating that Jesus's Sermon on the Mount mandated radical non-resistance to evil by violence and total non-cooperation with state militarism."
        }
    ],

    # ---------------- CHAPTER 5 ----------------
    "ch5_gandhism_sec_6": [
        {
            "id": "ch5_gandhism_sec_6_q1",
            "question": "Who famously declared: 'There is no path to peace; peace is the path' and 'An eye for an eye will only make the whole world blind'?",
            "options": [
                "Mahatma Gandhi",
                "Martin Luther King Jr.",
                "Nelson Mandela",
                "Jawaharlal Nehru"
            ],
            "correctIndex": 0,
            "explanation": "Both aphorisms embody Gandhi's foundational ethical axiom that means and ends are inextricably intertwined: violent means can never yield a peaceful, just society."
        },
        {
            "id": "ch5_gandhism_sec_6_q2",
            "question": "For a 10-marker UPSC question: 'Evaluate the contemporary relevance of Mahatma Gandhi in an era of global polarization and climate crisis', which concluding assessment is most theoretically mature?",
            "options": [
                "Gandhi is irrelevant because modern warfare uses ballistic missiles and drones.",
                "Gandhi's insights into ecological limits ('Earth provides enough for need, but not for greed'), moral decentralization, Satyagraha as democratic dissent, and the ethical unity of means and ends offer not a nostalgic throwback, but a prophetic compass for navigating the existential planetary and democratic crises of the 21st century.",
                "Gandhi's ideas were completely implemented by the Indian five-year plans.",
                "Gandhi was solely a religious saint who had no political theories."
            ],
            "correctIndex": 1,
            "explanation": "Option B elevates Gandhi from simple historical hero to a prophetic theorist whose concepts directly address 21st-century climate breakdown, political polarization, and nonviolent civil disobedience."
        }
    ],
    "ch5_gandhism_sec_21": [
        {
            "id": "ch5_gandhism_sec_21_q1",
            "question": "In 'The Subjection of Women' (1869), who argued alongside Harriet Taylor that the legal subordination of one sex to another is wrong in itself and one of the chief hindrances to human improvement?",
            "options": [
                "John Stuart Mill",
                "Jeremy Bentham",
                "William Godwin",
                "Herbert Spencer"
            ],
            "correctIndex": 0,
            "explanation": "J.S. Mill attacked Victorian patriarchal marriage as the last remaining vestige of feudal slavery, arguing that the principle of utility demands complete equality in law, education, and employment."
        },
        {
            "id": "ch5_gandhism_sec_21_q2",
            "question": "Which historic 1848 gathering in New York, organized by Elizabeth Cady Stanton and Lucretia Mott, issued the 'Declaration of Sentiments' demanding women's right to vote?",
            "options": [
                "The Seneca Falls Convention",
                "The Philadelphia Convention",
                "The Boston Tea Party",
                "The Chicago Workers Congress"
            ],
            "correctIndex": 0,
            "explanation": "Seneca Falls marked the formal launch of First Wave American feminism, rewriting the US Declaration of Independence: 'We hold these truths to be self-evident: that all men and women are created equal'."
        }
    ],
    "ch5_gandhism_sec_22": [
        {
            "id": "ch5_gandhism_sec_22_q1",
            "question": "Which historic event marks the primary breakthrough of 'First-Wave Feminism' across Britain and the United States in the early 20th century?",
            "options": [
                "Winning women's suffrage (voting rights via the 19th Amendment in US 1920, and Representation of the People Acts in UK 1918/1928).",
                "Abolishing the capitalist economic system.",
                "The legalization of no-fault divorce in 1970.",
                "The creation of the United Nations in 1945."
            ],
            "correctIndex": 0,
            "explanation": "First-Wave feminism concentrated on legal, civic, and political citizenship—principally the right to vote (suffrage), property rights for married women, and equal access to education."
        },
        {
            "id": "ch5_gandhism_sec_22_q2",
            "question": "In 'The Feminine Mystique' (1963), which Second-Wave feminist author identified 'the problem that has no name'—the pervasive dissatisfaction of suburban housewives confined to domesticity?",
            "options": [
                "Betty Friedan",
                "Gloria Steinem",
                "Shulamith Firestone",
                "Kate Millett"
            ],
            "correctIndex": 0,
            "explanation": "Betty Friedan catalyzed Second-Wave liberal feminism and co-founded the National Organization for Women (NOW), exploding the post-war myth of the contented, fulfilled housewife."
        }
    ],

    # ---------------- CHAPTER 6 ----------------
    "ch6_feminism_sec_intro": [
        {
            "id": "ch6_feminism_sec_intro_q1",
            "question": "In 'The Second Sex' (1949), which French existentialist feminist philosopher coined the monumental aphorism: 'One is not born, but rather becomes, a woman'?",
            "options": [
                "Simone de Beauvoir",
                "Luce Irigaray",
                "Hélène Cixous",
                "Julia Kristeva"
            ],
            "correctIndex": 0,
            "explanation": "Simone de Beauvoir decoupled biological sex from socially constructed gender, showing how patriarchal culture constructs Woman as the inessential 'Other' relative to Man as the universal Subject."
        },
        {
            "id": "ch6_feminism_sec_intro_q2",
            "question": "How did Simone de Beauvoir apply Jean-Paul Sartre's existentialist philosophy to gender relations in 'The Second Sex'?",
            "options": [
                "She demonstrated that men define themselves as the autonomous Subject ('Self'), while defining women not as autonomous agents, but strictly in relation to men as the inessential 'Other'.",
                "She argued that biology permanently dictates social destiny.",
                "She claimed that women should completely abstain from philosophical inquiry.",
                "She argued that women possess innate spiritual superiority over men."
            ],
            "correctIndex": 0,
            "explanation": "Beauvoir applied the existentialist Self/Other dialectic: 'He is the Subject, he is the Absolute—she is the Other.' Man casts woman as passive nature and immanence, reserving transcendence for himself."
        }
    ],
    "ch6_feminism_sec_2": [
        {
            "id": "ch6_feminism_sec_2_q1",
            "question": "What is the foundational analytical distinction between 'Sex' and 'Gender' in feminist political theory (first formalized by Ann Oakley in 1972)?",
            "options": [
                "'Sex' refers to biological and anatomical differences between male and female bodies, whereas 'Gender' is the culturally learned, socially constructed set of roles, norms, and behaviors assigned to masculinity and femininity.",
                "'Sex' is a legal term, while 'Gender' is a medical term.",
                "'Sex' was invented by capitalism, while 'Gender' exists in all animal species.",
                "Feminists reject both terms as bourgeois fictions."
            ],
            "correctIndex": 0,
            "explanation": "Ann Oakley ('Sex, Gender and Society', 1972) established that while sex is biological, gender is socio-culturally imposed, demonstrating that gender hierarchies are historically contingent and capable of transformation."
        },
        {
            "id": "ch6_feminism_sec_2_q2",
            "question": "Which radical feminist thinker later critiqued the Sex/Gender distinction in 'Gender Trouble' (1990) by arguing that 'Sex' is just as much a cultural construct as 'Gender'?",
            "options": [
                "Judith Butler",
                "Catharine MacKinnon",
                "Andrea Dworkin",
                "Iris Marion Young"
            ],
            "correctIndex": 0,
            "explanation": "Judith Butler argued that 'sex' is not a prediscursive biological brute fact; rather, the scientific and social categories through which we perceive sex are themselves shaped by compulsory heteronormative discourses."
        }
    ],
    "ch6_feminism_sec_3": [
        {
            "id": "ch6_feminism_sec_3_q1",
            "question": "Match the three historic waves of feminism to their defining core agendas:",
            "options": [
                "First Wave: Suffrage and legal rights; Second Wave: Patriarchy, reproduction, and 'The Personal is Political'; Third Wave: Intersectionality, diversity, and queer identity.",
                "First Wave: Equal pay in factories; Second Wave: Voting rights; Third Wave: Feudal property laws.",
                "First Wave: Monastic seclusion; Second Wave: Military enlistment; Third Wave: Total abolition of marriage.",
                "All three waves had precisely identical goals and authors."
            ],
            "correctIndex": 0,
            "explanation": "Option A summarizes feminist waves: 1st Wave (late 19th/early 20th c. suffrage/civic rights), 2nd Wave (1960s-80s patriarchy, sexuality, family), 3rd Wave (1990s onward intersectionality, post-coloniality, performativity)."
        },
        {
            "id": "ch6_feminism_sec_3_q2",
            "question": "Which influential text by bell hooks in 1984 critiqued Betty Friedan and white liberal feminism for ignoring race and class: 'Feminist Theory: From Margin to Center'?",
            "options": [
                "bell hooks",
                "Audre Lorde",
                "Alice Walker",
                "Angela Davis"
            ],
            "correctIndex": 0,
            "explanation": "Gloria Jean Watkins (bell hooks) attacked Friedan's assumption that all women were bored suburban housewives, pointing out that working-class Black women had always worked outside the home and faced simultaneous racial, gender, and economic exploitation."
        }
    ],
    "ch6_feminism_sec_4": [
        {
            "id": "ch6_feminism_sec_4_q1",
            "question": "Which legal scholar and radical feminist authored 'Toward a Feminist Theory of the State' (1989), arguing that: 'When the state is most neutral, it is most male'?",
            "options": [
                "Catharine A. MacKinnon",
                "Andrea Dworkin",
                "Martha Nussbaum",
                "Susan Moller Okin"
            ],
            "correctIndex": 0,
            "explanation": "Catharine MacKinnon demonstrated that liberal law's celebrated 'objectivity' and 'neutrality' is a male point of view institutionalized as the universal standard, reinforcing male dominance across rape law, pornography, and workplace harassment."
        },
        {
            "id": "ch6_feminism_sec_4_q2",
            "question": "Who authored 'Justice, Gender, and the Family' (1989), challenging John Rawls's liberal theory of justice for uncritically treating the traditional family as a non-political private sphere?",
            "options": [
                "Susan Moller Okin",
                "Carol Gilligan",
                "Seyla Benhabib",
                "Nancy Fraser"
            ],
            "correctIndex": 0,
            "explanation": "Susan Moller Okin showed that Rawls's Original Position ignores the gendered division of labor within the family. A truly just society must apply principles of justice directly to domestic life and child-rearing."
        }
    ],
    "ch6_feminism_sec_5": [
        {
            "id": "ch6_feminism_sec_5_q1",
            "question": "What is the primary philosophical strategy of 'Liberal Feminism' regarding the existing political, economic, and constitutional structures?",
            "options": [
                "It seeks the total revolutionary abolition of the state, family, and capitalism.",
                "It accepts existing democratic institutions and market structures, seeking to eliminate discriminatory laws and institutional biases so women have equal legal rights and opportunities to compete with men.",
                "It demands that men be completely excluded from voting in democratic elections.",
                "It rejects reason and science in favor of biological determinism."
            ],
            "correctIndex": 1,
            "explanation": "Liberal feminism (from Wollstonecraft and Mill to Friedan) operates within the liberal framework of individual rights, the rule of law, and equal opportunity, seeking equality through legislative reform, affirmative action, and education."
        },
        {
            "id": "ch6_feminism_sec_5_q2",
            "question": "In 'The Dialectic of Sex' (1970), which radical feminist thinker proposed that the elimination of sex-class requires freeing women from the biological tyranny of reproduction through modern reproductive technologies?",
            "options": [
                "Shulamith Firestone",
                "Kate Millett",
                "Mary Daly",
                "Adrienne Rich"
            ],
            "correctIndex": 0,
            "explanation": "Shulamith Firestone adapted Marx and Engels's materialist dialectic: just as the proletariat must seize the means of production, women must seize control of the means of reproduction, utilizing artificial reproduction to abolish biological sex distinctions."
        }
    ],
    "ch6_feminism_sec_6": [
        {
            "id": "ch6_feminism_sec_6_q1",
            "question": "In 'Sexual Politics' (1970), who defined politics as 'power-structured relationships whereby one group of persons is controlled by another', demonstrating that male supremacy operates through the patriarchal family?",
            "options": [
                "Kate Millett",
                "Betty Friedan",
                "Germaine Greer",
                "Robin Morgan"
            ],
            "correctIndex": 0,
            "explanation": "Kate Millett's PhD thesis established radical feminist political theory: patriarchy is a political institution where half the human population is controlled by the other half, maintained through socialization, religion, and domestic dominance."
        },
        {
            "id": "ch6_feminism_sec_6_q2",
            "question": "Who famously declared: 'The master's tools will never dismantle the master's house' (1984), challenging white, bourgeois feminists who excluded Black and lesbian perspectives?",
            "options": [
                "Audre Lorde",
                "bell hooks",
                "Chandra Talpade Mohanty",
                "Patricia Hill Collins"
            ],
            "correctIndex": 0,
            "explanation": "Black feminist poet and theorist Audre Lorde insisted that genuine liberation cannot be achieved using the existing patriarchal, racist, and classist conceptual frameworks of the dominant order."
        }
    ],
    "ch6_feminism_sec_7": [
        {
            "id": "ch6_feminism_sec_7_q1",
            "question": "Why do Radical and Socialist feminists critique Liberal Feminism as 'Bourgeois Feminism'?",
            "options": [
                "Because liberal feminism focuses narrowly on glass ceilings for privileged, professional women while leaving the underlying structures of capitalism, racial exploitation, and patriarchal domestic labor untouched.",
                "Because liberal feminists refuse to vote in national elections.",
                "Because liberal feminism opposes public education.",
                "Because liberal feminists support feudal monarchy."
            ],
            "correctIndex": 0,
            "explanation": "Radical and socialist critics argue that 'lean-in' liberal feminism merely allows elite women to join male corporate hierarchies, while continuing the exploitation of working-class and racialized women who perform underpaid care work."
        },
        {
            "id": "ch6_feminism_sec_7_q2",
            "question": "In 'In a Different Voice' (1982), which developmental psychologist pioneered 'Care Ethics', showing that women often conceptualize moral dilemmas through relational responsibility and empathy rather than abstract universal rights?",
            "options": [
                "Carol Gilligan",
                "Nel Noddings",
                "Virginia Held",
                "Sarah Ruddick"
            ],
            "correctIndex": 0,
            "explanation": "Carol Gilligan critiqued Lawrence Kohlberg's male-centric moral stages, demonstrating that women's moral development values connection, interdependence, and care ethics equally alongside abstract justice."
        }
    ],
    "ch6_feminism_sec_10": [
        {
            "id": "ch6_feminism_sec_10_q1",
            "question": "In feminist theory, who popularized the revolutionary political slogan 'The Personal is Political' in a 1969 essay?",
            "options": [
                "Carol Hanisch",
                "Kate Millett",
                "Betty Friedan",
                "Gloria Steinem"
            ],
            "correctIndex": 0,
            "explanation": "Carol Hanisch's 1969 paper 'The Personal is Political' defended consciousness-raising groups, proving that women's personal struggles with therapy, domestic labor, and marital relationships are structural political issues requiring collective transformation."
        },
        {
            "id": "ch6_feminism_sec_10_q2",
            "question": "What is the transformative significance of 'The Personal is Political' for constitutional and political theory?",
            "options": [
                "It shattered the sacred liberal boundary between the 'Public' (political, male, citizenship) and 'Private' (apolitical, female, family), proving that power, domination, and oppression operate within the home just as intensely as in the parliament.",
                "It argued that citizens should stop discussing politics in government buildings.",
                "It demanded that all marriages be overseen by criminal courts.",
                "It eliminated the need for national constitutions."
            ],
            "correctIndex": 0,
            "explanation": "By demonstrating that the 'private' family is an arena of power distribution, domestic violence, unpaid care work, and sexual hierarchy, feminism brought the private sphere into the heart of democratic theory."
        }
    ],
    "ch6_feminism_sec_12": [
        {
            "id": "ch6_feminism_sec_12_q1",
            "question": "In 'The Unhappy Marriage of Marxism and Feminism' (1979), which socialist feminist theorist formulated 'Dual Systems Theory', arguing that capitalism and patriarchy are two distinct yet interlocking systems of oppression?",
            "options": [
                "Heidi Hartmann",
                "Juliet Mitchell",
                "Iris Marion Young",
                "Zillah Eisenstein"
            ],
            "correctIndex": 0,
            "explanation": "Heidi Hartmann argued that Marxism is 'sex-blind', analyzing capital accumulation while ignoring how men of all classes benefit from the domestic labor of women. Capitalism and patriarchy are distinct, mutually reinforcing structures."
        },
        {
            "id": "ch6_feminism_sec_12_q2",
            "question": "In 'Woman's Estate' (1971), Juliet Mitchell argued that women's liberation requires simultaneously transforming four distinct structures. Which of the following is NOT one of Mitchell's four structures?",
            "options": [
                "Production",
                "Reproduction",
                "Sexuality and Socialization of Children",
                "Participation in Professional Olympic Sports"
            ],
            "correctIndex": 3,
            "explanation": "Juliet Mitchell synthesized psychoanalysis and historical materialism, showing that women are positioned across four interrelated structures: production, reproduction, sexuality, and the socialization of children."
        }
    ],
    "ch6_feminism_sec_13": [
        {
            "id": "ch6_feminism_sec_13_q1",
            "question": "What is the foundational Marxist feminist critique of 'Unpaid Domestic Labor' (championed by Maria Dalla Costa and Selma James in the 'Wages for Housework' campaign)?",
            "options": [
                "Unpaid domestic housework and care work is not a private luxury, but essential economic labor that reproduces the commodity of labor-power daily for free, directly subsidizing capitalist profits.",
                "Housework should be completely criminalized by international law.",
                "Women should stop cooking food for their children.",
                "Capitalists personally clean their workers' homes."
            ],
            "correctIndex": 0,
            "explanation": "Marxist feminists demonstrated that capitalism relies on the unpaid reproductive labor of women (cooking, cleaning, emotional care) to restore the physical and psychological energy of the worker for tomorrow's shift."
        },
        {
            "id": "ch6_feminism_sec_13_q2",
            "question": "Who authored 'Caliban and the Witch' (2004), demonstrating how the transition from feudalism to capitalism required the violent subjugation of women and the criminalization of their reproductive autonomy (the witch hunts)?",
            "options": [
                "Silvia Federici",
                "Rosa Luxemburg",
                "Angela Davis",
                "Nancy Hartsock"
            ],
            "correctIndex": 0,
            "explanation": "Silvia Federici showed that Marx's 'primitive accumulation' was not just colonial plunder and enclosure of common lands, but also the enclosure of the female body and degradation of women into unpaid reproducers of labor-power."
        }
    ],
    "ch6_feminism_sec_15": [
        {
            "id": "ch6_feminism_sec_15_q1",
            "question": "In the landmark 1986 essay 'Under Western Eyes: Feminist Scholarship and Colonial Discourses', which postcolonial feminist theorist critiqued Western feminist scholarship for constructing the 'Third World Woman' as a monolithic, helpless victim?",
            "options": [
                "Chandra Talpade Mohanty",
                "Gayatri Chakravorty Spivak",
                "Sara Suleri",
                "Uma Narayan"
            ],
            "correctIndex": 0,
            "explanation": "Chandra Talpade Mohanty exposed how Western feminist discourse appropriates the lives of women in the Global South, portraying them homogenously as uneducated, tradition-bound victims, while casting Western women as modern, liberated subjects."
        },
        {
            "id": "ch6_feminism_sec_15_q2",
            "question": "In 'Can the Subaltern Speak?' (1988), which postcolonial feminist philosopher analyzed the abolition of Sati in colonial India to expose how both British imperialists ('white men saving brown women from brown men') and indigenous patriarchs silenced subaltern female voices?",
            "options": [
                "Gayatri Chakravorty Spivak",
                "Homi K. Bhabha",
                "Edward Said",
                "Ranajit Guha"
            ],
            "correctIndex": 0,
            "explanation": "Spivak famously deconstructed colonial legal documents, concluding that between the epistemic violence of British imperialism and the patriarchal traditions of Indian elites, the subaltern woman had no institutional space from which to speak."
        }
    ],
    "ch6_feminism_sec_16": [
        {
            "id": "ch6_feminism_sec_16_q1",
            "question": "In 1989, who formulated the analytical concept of 'Intersectionality', illustrating how single-axis legal frameworks erase the compounded discrimination faced by Black women at the intersection of race and gender?",
            "options": [
                "Kimberlé Crenshaw ('Demarginalizing the Intersection of Race and Sex')",
                "Patricia Hill Collins",
                "bell hooks",
                "Angela Davis"
            ],
            "correctIndex": 0,
            "explanation": "Using the DeGraffenreid v. General Motors case, legal scholar Kimberlé Crenshaw showed that Black women were neither treated as 'all women' (white women) nor 'all blacks' (black men), proving that interlocking matrices of oppression require intersectional analysis."
        },
        {
            "id": "ch6_feminism_sec_16_q2",
            "question": "Who authored 'Black Feminist Thought' (1990) and developed the concept of the 'Matrix of Domination' to explain how race, class, gender, and nation constitute mutually interlocking systems of oppression?",
            "options": [
                "Patricia Hill Collins",
                "Audre Lorde",
                "Alice Walker",
                "Barbara Smith"
            ],
            "correctIndex": 0,
            "explanation": "Sociologist Patricia Hill Collins conceptualized the 'Matrix of Domination', demonstrating that individuals experience oppression along multiple axes simultaneously, and championed the unique standpoint epistemology of Black women."
        }
    ],
    "ch6_feminism_sec_17": [
        {
            "id": "ch6_feminism_sec_17_q1",
            "question": "In 'Feminism for the 99%: A Manifesto' (2019), Cinzia Arruzza, Tithi Bhattacharya, and Nancy Fraser advocate a global anti-capitalist feminism that departs from:",
            "options": [
                "Corporate 'Lean-In' liberal feminism that focuses on corporate boardrooms while exploiting working-class women.",
                "Demands for equal pay and voting rights.",
                "All environmental and ecological concerns.",
                "The defense of public healthcare."
            ],
            "correctIndex": 0,
            "explanation": "The authors argue that mainstream corporate feminism has become a handmaiden of neoliberalism, demanding instead a mass, radical, intersectional feminism that tackles housing, environmental destruction, low wages, and care crises for the 99%."
        },
        {
            "id": "ch6_feminism_sec_17_q2",
            "question": "For a 10-marker UPSC question: 'Examine the significance of Intersectionality in contemporary feminist theory', which concluding synthesis is most theoretically accomplished?",
            "options": [
                "Intersectionality is a temporary American buzzword that has no relevance to Indian society.",
                "By dismantling the essentialist assumption of a universal female experience, Intersectionality transforms feminism from a single-issue movement into a comprehensive analytical instrument for interrogating how gender intersects with caste, class, race, and religion, ensuring that democratic justice begins from the margins.",
                "Intersectionality proves that women no longer face any discrimination anywhere in the world.",
                "Feminism should completely abandon all references to gender."
            ],
            "correctIndex": 1,
            "explanation": "Option B elevates Intersectionality to a universal analytical paradigm, demonstrating its critical relevance to India (gender intersecting with caste, class, and religion) and grounding democratic justice from the margins."
        }
    ]
}

# Update all matching sections
updated_count = 0

for ch in data['chapters']:
    for sec in ch['sections']:
        sec_id = sec['id']
        if sec_id in custom_questions_map:
            sec['mcqs'] = custom_questions_map[sec_id]
            updated_count += len(custom_questions_map[sec_id])

print(f"✅ Successfully updated {updated_count} MCQs with high-yield quotes, thinker critiques, book authorship, and 10-marker UPSC questions!")

# Check remaining generic questions
remaining_generic = 0
for ch in data['chapters']:
    for sec in ch['sections']:
        for q in sec.get('mcqs', []):
            if 'Regarding the theoretical concepts' in q.get('question', ''):
                remaining_generic += 1

print(f"Remaining generic boilerplate MCQs: {remaining_generic}")

# Save back to sarrthi_full_data.js
updated_js = prefix + json.dumps(data, indent=2, ensure_ascii=False) + ';\n'
with open('sarrthi_full_data.js', 'w', encoding='utf-8') as f:
    f.write(updated_js)

print("✅ sarrthi_full_data.js successfully written and persisted!")
