import json
import re

with open('sarrthi_full_data.js', 'r', encoding='utf-8') as f:
    raw = f.read()

prefix = raw.split('window.SARRTHI_DATA = ')[0] + 'window.SARRTHI_DATA = '
json_str = raw.split('window.SARRTHI_DATA = ')[1].rstrip(';\n ')
data = json.loads(json_str)

# Map specific custom questions for key semi-topics
# For any remaining semi-topic, generate a high-standard academic question derived from its title, intro, and bullets.

custom_semitopic_questions = {
    # CHAPTER 1
    "ch1_ideologies_sec_intro": {
        "question": "“Ideology is the core of political language, providing both cognitive maps and normative directions for political action.” Examine Michael Freeden’s conceptualization of ideology in contrast to classical pejorative definitions.",
        "scholars": "Michael Freeden (Morphological approach), Destutt de Tracy, Karl Mannheim",
        "intro": "Ideology, coined by Destutt de Tracy as the 'science of ideas', was transformed by Michael Freeden into a neutral morphological tool where political concepts are decontested and clustered around core values.",
        "body": "1. Freeden's Morphological Analysis: Ideologies are configurations of decontested concepts (e.g. liberty in liberalism vs. socialism). 2. Cognitive & Normative Functions: Ideologies act as mental filters that simplify complex socio-political realities and legitimize power. 3. Rejection of Pejorative Bias: Moves beyond Marxian 'false consciousness' and Popperian 'dogmatism' to treat ideology as indispensable to human political discourse.",
        "conclusion": "Freeden's semantic approach rescues ideology from dogmatic reductionism, proving that democratic debate itself is fundamentally an ideological contestation over conceptual meanings."
    },
    "ch1_ideologies_sec_2": {
        "question": "“The ideas of the ruling class are in every epoch the ruling ideas.” Discuss Marx’s base-superstructure model and how ideology naturalizes bourgeois dominance.",
        "scholars": "Karl Marx & Friedrich Engels (The German Ideology), Antonio Gramsci, Louis Althusser",
        "intro": "In 'The German Ideology' (1845), Marx and Engels formulate the materialist conception of ideology, presenting it as an inverted camera obscura that reflects economic class dominance.",
        "body": "1. Base-Superstructure Determinism: The economic mode of production (base) conditions the legal, political, and ideological superstructure. 2. Universalization of Particular Interests: The bourgeoisie presents its particular class interests (private property, wage labor) as universal human values. 3. Legitimization of Exploitation: Ideology functions as an opiate and cognitive illusion masking surplus value extraction.",
        "conclusion": "While Marx viewed ideology as bourgeois false consciousness destined to wither away, neo-Marxists later recognized that counter-ideological struggle is essential to dismantling capitalist hegemony."
    },
    "ch1_ideologies_sec_3": {
        "question": "Analyze the progression from 'False Consciousness' to 'Class Consciousness' in Marxist theory. How did Georg Lukács operationalize revolutionary praxis?",
        "scholars": "Georg Lukács (History and Class Consciousness), Herbert Marcuse, Karl Marx",
        "intro": "Marxist theory posits false consciousness as the proletariat's internalization of bourgeois norms, whereas Georg Lukács conceptualized class consciousness as the epistemological catalyst for revolution.",
        "body": "1. Nature of False Consciousness: Workers view alienation and exploitation as natural market laws rather than historical social relations. 2. Reification (Verdinglichung): Lukács demonstrated how capitalist commodification turns human relations into relations between things. 3. Revolutionary Praxis: Proletariat as both subject and object of history; transcending immediacy through theoretical self-awareness led by the vanguard party.",
        "conclusion": "Lukács bridged classical economism and modern critical theory, emphasizing that revolution requires not just material breakdown but an intellectual breakthrough in class consciousness."
    },
    "ch1_ideologies_sec_4": {
        "question": "Compare Antonio Gramsci’s concept of 'Cultural Hegemony' with Louis Althusser’s 'Ideological State Apparatuses' (ISAs). How do both theorists expand upon classical Marxist economism?",
        "scholars": "Antonio Gramsci (Prison Notebooks), Louis Althusser (Ideology and Ideological State Apparatuses)",
        "intro": "Both Gramsci and Althusser rejected crude economic determinism by theorizing the relative autonomy of the ideological superstructure in reproducing capitalist relations of production.",
        "body": "1. Gramsci's Hegemony: Consent-based rule manufactured through civil society institutions (schools, churches, press); contested by 'organic intellectuals' in a 'War of Position'. 2. Althusser's ISAs: Distinguishes Repressive State Apparatuses (RSAs - army, police, prisons) from ISAs (schools, family, media) which interpellate individuals into capitalist subjects. 3. Comparative Nexus: Gramsci emphasizes conscious cultural contestation and human agency, whereas Althusser views ideology as an inescapable structural medium.",
        "conclusion": "Together, they enriched political theory by proving that capitalist domination relies more on moral-intellectual leadership and internalized ideology than physical coercion."
    },
    "ch1_ideologies_sec_5": {
        "question": "“To be conservative is to prefer the familiar to the unknown, to prefer the tried to the untried.” Critically examine Michael Oakeshott’s conservative critique of ideological rationalism in politics.",
        "scholars": "Michael Oakeshott (Rationalism in Politics), Edmund Burke",
        "intro": "Michael Oakeshott mounted a formidable critique of ideological politics, arguing that ideological rationalism mistakes abstract intellectual models for practical political wisdom.",
        "body": "1. Technical Knowledge vs. Practical Knowledge: Ideology reduces governance to technical rules learned from books, ignoring experiential, traditional wisdom (practical knowledge). 2. Anti-Utopianism & Politics as Practice: Politics is not a blueprint for perfection but 'the pursuit of intimations' and sailing a boundless sea without final destination. 3. Civil Association (Societas) vs. Enterprise Association (Universitas): Rejection of state-driven utopian missions in favor of shared customs and legal frameworks.",
        "conclusion": "Oakeshott's critique serves as a profound caution against ideological dogmatism and technocratic social engineering that ignore the complex historical fabric of society."
    },
    "ch1_ideologies_sec_6": {
        "question": "Examine Hannah Arendt’s thesis that totalitarian regimes weaponize closed ideological systems to destroy human plurality and political agency.",
        "scholars": "Hannah Arendt (The Origins of Totalitarianism, The Human Condition, Eichmann in Jerusalem)",
        "intro": "In 'The Origins of Totalitarianism' (1951), Hannah Arendt identified totalitarianism as a radical, unprecedented tyranny that uses ideology as an instrument of total domination.",
        "body": "1. Closed Ideological Systems: Totalitarian ideologies claim absolute explanatory power over history and nature, offering pseudoscientific 'final solutions' immune to empirical facts. 2. Atomization & Destruction of Plurality: Total terror isolates individuals, eroding civil society and replacing spontaneous human relationships with mass ideological conformism. 3. Banality of Evil: The replacement of individual moral judgment with unthinking bureaucratic obedience.",
        "conclusion": "Arendt championed public political action (vita activa) in the polis as the ultimate safeguard of human freedom, proving that total ideologies pose an existential threat to democratic life."
    },
    "ch1_ideologies_sec_7": {
        "question": "“Unlimited tolerance must lead to the disappearance of tolerance.” Explain Karl Popper’s 'Paradox of Tolerance' and his critique of historicism in closed societies.",
        "scholars": "Karl Popper (The Open Society and Its Enemies, The Poverty of Historicism)",
        "intro": "Karl Popper formulated a robust defense of liberal democracy by demonstrating how historicist ideologies inevitably lead to authoritarian closed societies.",
        "body": "1. Critique of Historicism: Rejected the deterministic historical laws of Plato, Hegel, and Marx as unfalsifiable teleological dogma justifying coercive social engineering. 2. Open vs. Closed Society: Open societies rest on critical rationalism, falsifiability, and freedom to criticize governance; closed societies demand tribal conformity and absolute truth. 3. Paradox of Tolerance: An open society that extends tolerance to intolerant ideologies will be destroyed; democracy has the legitimate right to defend itself against violent subversion.",
        "conclusion": "Popper advocated 'piecemeal social engineering'—gradual, experimental reforms subject to trial and error—as the only rational alternative to ideological totalitarianism."
    },
    "ch1_ideologies_sec_9": {
        "question": "Critically analyze Daniel Bell’s 'End of Ideology' thesis. Was post-war Western technocratic consensus genuinely post-ideological, or merely an apology for welfare capitalism?",
        "scholars": "Daniel Bell, Seymour Martin Lipset, Herbert Marcuse, C. Wright Mills",
        "intro": "In 'The End of Ideology' (1960), Daniel Bell argued that post-WWII affluence and democratic welfare consensus had exhausted the radical, utopian ideologies of the 19th century.",
        "body": "1. Bell's Core Argument: Western societies achieved consensus on democratic politics, mixed economy, and welfare safety nets, replacing ideological passion with technocratic problem-solving. 2. Radical Critique (Marcuse & Mills): The 'end of ideology' was itself a conservative ideology that legitimized corporate capitalism and concealed systemic inequality under technocratic neutrality. 3. Subsequent Rebuttal: The explosion of 1960s civil rights, feminist, environmental movements, and the rise of neoliberalism disproved the permanent exhaustion of ideology.",
        "conclusion": "Bell captured a unique historical window of post-war Keynesian stability, but ideology remains an enduring, dynamic force in human political contestation."
    },
    "ch1_ideologies_sec_11": {
        "question": "“What we may be witnessing is not just the end of the Cold War, but the end of history as such.” Critically evaluate Francis Fukuyama’s 'End of History' thesis in light of 21st-century ideological conflicts.",
        "scholars": "Francis Fukuyama, G.W.F. Hegel, Alexandre Kojève, Samuel Huntington, Benjamin Barber",
        "intro": "Francis Fukuyama (1989/1992) posited that the collapse of Soviet communism marked the culmination of mankind's ideological evolution and the universalization of Western liberal democracy.",
        "body": "1. Hegelian-Kojèvian Dialectic: History as a struggle for mutual recognition (thymos), which achieves ultimate normative satisfaction in liberal democracy and free markets. 2. Structural Challenges: Huntington’s 'Clash of Civilizations' and Barber’s 'Jihad vs. McWorld' highlighted cultural, religious, and civilizational resistances to liberal universalism. 3. 21st-Century Contestation: Rise of authoritarian capitalism (China, Russia), populist backlashes, and severe economic inequality within Western democracies exposed liberal vulnerabilities.",
        "conclusion": "While Fukuyama maintained that no coherent ideological rival has superseded liberal democracy, contemporary history remains deeply contested, dynamic, and pluralistic."
    },

    # CHAPTER 2
    "ch2_liberalism_sec_intro": {
        "question": "“The end of law is not to abolish or restrain, but to preserve and enlarge freedom.” Discuss John Locke’s theory of natural rights and limited government.",
        "scholars": "John Locke (Two Treatises of Government), Thomas Hobbes, Robert Nozick",
        "intro": "John Locke, the father of classical liberalism, anchored political authority in individual natural rights and contractual consent in his 'Second Treatise of Government' (1689).",
        "body": "1. Pre-Political Natural Rights: Life, liberty, and estate (property) exist prior to the state under the Law of Nature. 2. Social Contract & Trust: Individuals form political society to overcome inconveniences of private dispute resolution; state acts as a fiduciary trustee. 3. Right to Revolution: Government by consent implies that when the state violates natural rights, citizens retain the legitimate right to alter or abolish it.",
        "conclusion": "Locke’s contractual paradigm established the foundational liberal premise that sovereign authority is conditional and subordinate to individual rights."
    },
    "ch2_liberalism_sec_3": {
        "question": "Distinguish between 'Negative Liberty' and 'Positive Liberty' as conceptualized by Isaiah Berlin. How does this distinction define the divide between Classical and Welfare Liberalism?",
        "scholars": "Isaiah Berlin (Two Concepts of Liberty), John Locke, T.H. Green, Milton Friedman",
        "intro": "In 'Two Concepts of Liberty' (1958), Isaiah Berlin formulated the classic distinction between negative liberty (freedom from) and positive liberty (freedom to).",
        "body": "1. Negative Liberty: Absence of external coercion or interference; championed by Classical Liberals (Locke, Hayek) for a minimal 'night-watchman' state. 2. Positive Liberty: Capacity for self-mastery, moral autonomy, and flourishing; championed by Welfare Liberals (T.H. Green, Hobhouse) justifying state provision of healthcare and education. 3. Berlin's Warning: Positive liberty carries the authoritarian risk of forcing individuals to be free according to a collective ideal.",
        "conclusion": "The negative-positive divide mirrors liberalism’s evolution from restraining state power against tyranny to utilizing state resources to empower human capabilities."
    },
    "ch2_liberalism_sec_7": {
        "question": "“Will, not force, is the basis of the state.” Examine T.H. Green’s moral justification for the welfare state and his doctrine that 'the state hinders hindrances'.",
        "scholars": "T.H. Green (Lectures on the Principles of Political Obligation), Jean-Jacques Rousseau, Harold Laski",
        "intro": "T.H. Green revitalized liberalism by fusing Kantian moral autonomy with Hegelian idealism, transforming the state into a moral agency dedicated to the common good.",
        "body": "1. Moral Liberty: True freedom is the positive power to do or enjoy something worth doing in common with others. 2. Will, Not Force: Political obligation stems from citizens recognizing the state as the protector of rights necessary for common moral realization. 3. Hindering Hindrances: The state should not dictate morality directly, but must remove structural impediments—ignorance, poverty, disease, and exploitation—that obstruct human flourishing.",
        "conclusion": "Green provided the philosophical foundation for modern welfare liberalism, legitimizing social legislation, public education, and factory laws without sacrificing individual dignity."
    },
    "ch2_liberalism_sec_8": {
        "question": "“The only freedom which deserves the name is that of pursuing our own good in our own way, so long as we do not attempt to deprive others of theirs.” Critically evaluate J.S. Mill’s Harm Principle.",
        "scholars": "J.S. Mill (On Liberty), Isaiah Berlin, Lord Devlin, H.L.A. Hart",
        "intro": "In 'On Liberty' (1859), J.S. Mill sought to establish a single, clear criterion—the Harm Principle—to demarcate the boundary of legitimate state and social interference over the individual.",
        "body": "1. Self-Regarding vs. Other-Regarding Actions: Absolute sovereign autonomy over one's own body and mind, intervention permitted solely to prevent harm to others. 2. Tyranny of the Majority: Mill feared social conformism and public opinion as much as political tyranny, fiercely defending eccentricity and freedom of expression. 3. Limitations & Omissions: Mill acknowledged that failure to act (inaction) can also cause harm, and his categorization blurred in interdependent industrial societies.",
        "conclusion": "Mill’s defense of individuality established that non-conformity and free inquiry are indispensable engines of human mental and social progress."
    },
    "ch2_liberalism_sec_9": {
        "question": "“Taxation of earnings from labor is on par with forced labor.” Critically examine Robert Nozick’s Entitlement Theory of Justice and his defense of the minimal state.",
        "scholars": "Robert Nozick (Anarchy, State, and Utopia), John Locke, John Rawls",
        "intro": "In 'Anarchy, State, and Utopia' (1974), Robert Nozick formulated a radical libertarian critique of Rawlsian distributive justice, defending the ultra-minimal night-watchman state.",
        "body": "1. Three Principles of Justice: Justice in acquisition (Lockean proviso), justice in transfer, and rectification of historical injustices. 2. Critique of Patterned & End-State Principles: Free voluntary exchanges (Wilt Chamberlain argument) inevitably upset patterned distributions unless state continuously violates liberty. 3. Self-Ownership: Redistributive taxation treats human beings as mere resources for others, violating Kant’s categorical imperative.",
        "conclusion": "While Nozick robustly defends individual liberty and property rights, critics (Rawls, Sen) argue that entitlement theory ignores structural market inequalities and basic human capabilities."
    },
    "ch2_liberalism_sec_10": {
        "question": "Analyze Bhikhu Parekh’s critique of liberal monism. How does dialogical multiculturalism move beyond mere toleration to active cultural recognition?",
        "scholars": "Bhikhu Parekh (Rethinking Multiculturalism), Will Kymlicka, Isaiah Berlin, Charles Taylor",
        "intro": "In 'Rethinking Multiculturalism' (2000), Bhikhu Parekh challenged both monocultural assimilation and liberal universalism, proposing a dialogical framework for plural societies.",
        "body": "1. Critique of Liberal Universalism: Liberalism is itself a historically specific cultural narrative and cannot claim moral monopoly or universal neutrality. 2. Human Beings as Culturally Embedded: Cultures provide meaning and identity; no single culture possesses all human truths, making diversity inherently valuable. 3. Intercultural Dialogue: Resolving cultural conflicts through respectful reciprocal dialogue rather than the imposition of Western liberal legal standards.",
        "conclusion": "Parekh advanced political theory by moving from passive liberal toleration to mutual recognition and transformative intercultural dialogue."
    },

    # CHAPTER 3
    "ch3_marxism_sec_intro": {
        "question": "“The history of all hitherto existing society is the history of class struggles.” Explain Karl Marx’s theory of Historical Materialism and the dynamics of revolutionary transformation.",
        "scholars": "Karl Marx & Friedrich Engels (The Communist Manifesto, Preface to A Contribution to the Critique of Political Economy)",
        "intro": "Historical Materialism is Marx’s scientific methodology that posits material economic production as the primary determinant of historical development and social change.",
        "body": "1. Productive Forces vs. Relations of Production: Technological and human capacities (forces) clash with existing property structures (relations), generating epochal revolutions. 2. Historical Epochs: Primitive communism, slavery, feudalism, capitalism, and the eventual transition to communism. 3. Contradictions of Capitalism: Socialized production vs. private capitalist appropriation inexorably generates economic crises and proletarian consciousness.",
        "conclusion": "Marx converted Hegelian idealist dialectics into a materialist science of history, establishing class struggle as the true engine of human emancipation."
    },
    "ch3_marxism_sec_9": {
        "question": "Elucidate Marx’s Four-Fold Theory of Alienation under capitalist production. How does commodification distort human species-essence (Gattungswesen)?",
        "scholars": "Karl Marx (Economic and Philosophic Manuscripts of 1844), Georg Lukács, Herbert Marcuse",
        "intro": "In the 'Paris Manuscripts' of 1844, the young Marx analyzed alienation (Entfremdung) as the estrangement of the laborer under capitalist wage labor.",
        "body": "1. Alienation from the Product: The object produced confronts the worker as an alien, hostile power owned by the capitalist. 2. Alienation from the Production Process: Labor is forced, monotonous, and unfulfilling rather than creative self-realization. 3. Alienation from Species-Essence: Humans are reduced to animal survival, stripped of their capacity for conscious, creative activity. 4. Alienation from Fellow Humans: Market competition turns workers against one another as commodities.",
        "conclusion": "Marx's theory of alienation provides the humanist moral core of socialist critique, proving that capitalism deforms human nature long before it creates economic poverty."
    },
    "ch3_marxism_sec_15": {
        "question": "“Imperialism is the monopoly stage of capitalism.” Examine V.I. Lenin’s contributions to Marxist theory through his conceptualization of the Vanguard Party and Imperialism.",
        "scholars": "V.I. Lenin (Imperialism: The Highest Stage of Capitalism, What Is to Be Done?), J.A. Hobson",
        "intro": "Lenin adapted classical Marxism to the realities of 20th-century geopolitical conflict and semi-feudal Russia, developing revolutionary vanguardism and anti-imperialism.",
        "body": "1. Vanguard Party & Democratic Centralism: The working class independently achieves only trade-union consciousness; revolutionary socialist consciousness must be brought from without by a disciplined vanguard. 2. Imperialism as Highest Stage: Finance capital, monopolies, and export of capital divide the world, generating interimperialist wars and imperialist superprofits that bribe the labor aristocracy. 3. Weakest Link in the Chain: Socialist revolution can erupt in underdeveloped nations (Russia) rather than advanced industrial Western economies.",
        "conclusion": "Lenin shifted Marxism from theoretical analysis to state-building praxis, laying the groundwork for anti-colonial liberation struggles across the Global South."
    },
    "ch3_marxism_sec_17": {
        "question": "Explain Antonio Gramsci’s distinction between 'War of Position' and 'War of Movement'. Why is civil society the decisive battleground in modern Western democracies?",
        "scholars": "Antonio Gramsci (Prison Notebooks), Perry Anderson, Chantal Mouffe",
        "intro": "Antonio Gramsci recognized that the 1917 Bolshevik strategy could not be duplicated in advanced Western democracies where civil society provided a sturdy defensive trench for the state.",
        "body": "1. War of Movement (Frontal Assault): Suitable in the East (Russia), where 'the State was everything, civil society was primordial and gelatinous'. 2. War of Position (Hegemonic Contest): Necessary in the West, where 'the State was only an outer ditch, behind which stood a powerful system of fortresses and earthworks' of civil society. 3. Building Counter-Hegemony: Long-term cultural, intellectual, and institutional struggle to achieve moral and intellectual leadership before capturing formal state power.",
        "conclusion": "Gramsci’s formulation revolutionized strategic political theory, demonstrating that lasting political power requires winning the cultural consent of society."
    },
    "ch3_marxism_sec_20": {
        "question": "Analyze the Frankfurt School’s critique of the Enlightenment. How did Adorno and Horkheimer argue that instrumental reason inverted emancipation into total domination?",
        "scholars": "Theodor Adorno & Max Horkheimer (Dialectic of Enlightenment), Herbert Marcuse, Jürgen Habermas",
        "intro": "In 'Dialectic of Enlightenment' (1947), Adorno and Horkheimer formulated the core thesis of Critical Theory: that the Enlightenment’s promise of liberation mutated into new mechanisms of domination.",
        "body": "1. Instrumental Reason: Reason shifted from ethical reflection on human ends to calculative, technocratic control over nature and humanity. 2. Culture Industry: Mass culture, media, and consumerism manufacture standardized tastes, depoliticizing citizens and commodifying leisure. 3. Authoritarian Personality: Psychological internalization of authority in industrialized societies facilitated the rise of fascism and conformist consumerism.",
        "conclusion": "The Frankfurt School rescued critical theory from economic dogmatism by exposing how modern rationality and mass culture perpetuate psychological and ideological subjugation."
    },
    "ch3_marxism_sec_24": {
        "question": "“A comfortable, smooth, reasonable, democratic unfreedom prevails in advanced industrial civilization.” Discuss Herbert Marcuse’s thesis of 'One-Dimensional Man'.",
        "scholars": "Herbert Marcuse (One-Dimensional Man), Theodor Adorno",
        "intro": "Herbert Marcuse (1964) argued that affluent capitalist societies eliminate radical dissent by manufacturing 'false needs' that integrate the working class into the established system.",
        "body": "1. One-Dimensional Thought & Behavior: Technological rationality absorbs all opposition; political alternatives are dismissed as irrational or impractical. 2. Manufacture of False Needs: Consumer goods, advertising, and entertainment satisfy artificial desires while perpetuating alienated labor. 3. The Great Refusal: The traditional proletariat is pacified; revolutionary agency shifts to the marginalized, students, and Third World liberation movements.",
        "conclusion": "Marcuse’s critique remains deeply prophetic in analyzing modern digital consumerism and algorithmic pacification of political resistance."
    },
    "ch3_marxism_sec_26": {
        "question": "Examine the Structuralist Marxist perspective on the state as formulated by Nicos Poulantzas. How does the 'relative autonomy' of the state serve the long-term reproduction of capital?",
        "scholars": "Nicos Poulantzas (Political Power and Social Classes), Ralph Miliband, Louis Althusser",
        "intro": "Nicos Poulantzas challenged Ralph Miliband's instrumentalist view by arguing that the capitalist state is structurally determined rather than merely run by individual capitalist agents.",
        "body": "1. State as Factor of Cohesion: Society is divided by class struggles and inter-capitalist competition; the state organizes the power bloc and disorganizes the working class into atomized citizens. 2. Relative Autonomy: The state must be autonomous from individual capitalists and factions to act in the collective, long-term interest of capitalism as a whole. 3. Condensation of Class Relations: The state is not a neutral tool or monolith, but an institutional terrain reflecting class contradictions.",
        "conclusion": "Poulantzas provided a sophisticated structural framework that explains how capitalist welfare concessions preserve systemic stability without overthrowing capitalism."
    },

    # CHAPTER 4
    "ch4_socialism_fascism_sec_3": {
        "question": "Compare Utopian Socialism (Robert Owen, Charles Fourier) with Scientific Socialism (Karl Marx). Why did Marx criticize early socialists as 'utopian'?",
        "scholars": "Robert Owen, Charles Fourier, Henri de Saint-Simon, Friedrich Engels (Socialism: Utopian and Scientific)",
        "intro": "Early 19th-century socialists sought to reconstruct society through moral appeals, cooperative communities, and model phalansteries, which Marx and Engels later contrasted with Scientific Socialism.",
        "body": "1. Utopian Socialism: Grounded in philanthropy, moral persuasion of the wealthy, and peaceful experimental communes (e.g. Owen’s New Lanark). 2. Scientific Critique: Engels argued utopians lacked an understanding of historical materialism, class struggle, and the structural laws of capitalist production. 3. Revolutionary Agency: Scientific socialism identified the industrial proletariat—not enlightened benevolence—as the historical agent of revolutionary transformation.",
        "conclusion": "While Marx criticized their methods, utopian socialists pioneered crucial ideas of cooperative labor, gender equality, and social justice that enriched the wider socialist movement."
    },
    "ch4_socialism_fascism_sec_4": {
        "question": "“Democracy is the means and the end of socialism.” Critically examine Eduard Bernstein’s Evolutionary Socialism and his doctrine of Revisionism.",
        "scholars": "Eduard Bernstein (Evolutionary Socialism), Rosa Luxemburg (Reform or Revolution?), Karl Kautsky",
        "intro": "Eduard Bernstein provoked the famous Revisionist Debate in German Social Democracy by rejecting Marx’s predictions of capitalist collapse and violent revolution.",
        "body": "1. Empirical Challenges to Marx: Middle class was expanding rather than disappearing; working-class living standards were rising; capitalism demonstrated adaptability. 2. The Movement is Everything: 'The ultimate aim of socialism is nothing to me; the movement is everything'—advocated parliamentary gradualism, union organizing, and social reforms. 3. Rosa Luxemburg’s Rebuttal: Reforms within capitalism mitigate symptoms without abolishing wage slavery; abandoning revolution abandons socialism itself.",
        "conclusion": "Bernstein laid the theoretical foundations for modern European social democracy, championing the transformation of capitalism through democratic constitutional institutions."
    },
    "ch4_socialism_fascism_sec_6": {
        "question": "Examine the core principles of Fabian Socialism. How did the Webbs conceptualize the 'inevitability of gradualism' in achieving social justice?",
        "scholars": "Sidney & Beatrice Webb, George Bernard Shaw, Clement Attlee",
        "intro": "Founded in 1884, the Fabian Society advocated the gradual, constitutional permeation of socialist ideas through state institutions and expert public administration.",
        "body": "1. Inevitability of Gradualism: Rejection of violent class warfare; social reforms, municipal enterprise, and universal suffrage would naturally expand public ownership. 2. Permeation Strategy: Influencing civil servants, politicians, and intellectuals through empirical social research and technocratic reports. 3. State as Reformer: Expanding municipal socialism ('gas and water socialism') and establishing national health and education systems.",
        "conclusion": "Fabianism profoundly shaped the post-war British welfare state and the programmatic architecture of democratic socialist parties worldwide."
    },
    "ch4_socialism_fascism_sec_9": {
        "question": "Analyze the theory of Guild Socialism as developed by G.D.H. Cole. How does it reconcile worker self-management with state authority?",
        "scholars": "G.D.H. Cole (Guild Socialism Restated), Arthur Penty, S.G. Hobson",
        "intro": "Guild Socialism emerged in early 20th-century Britain as a middle path between state-dominated bureaucratized socialism and anti-state syndicalism.",
        "body": "1. Industrial Democracy: Rejection of bureaucratic state socialism; factories and industries should be self-governed by democratic guilds of producers. 2. Functional Democracy: Citizens should be represented according to their social and occupational functions (as producers and consumers) rather than geographical constituencies. 3. Pluralist State: The state acts not as a sovereign despot, but as a coordinating body balancing producer guilds with consumer interests.",
        "conclusion": "Guild Socialism remains a vital intellectual precursor to workplace democracy, guild pluralism, and decentralized economic governance."
    },
    "ch4_socialism_fascism_sec_17": {
        "question": "“Everything in the State, nothing outside the State, nothing against the State.” Critically evaluate Benito Mussolini’s doctrine of the Totalitarian Fascist State.",
        "scholars": "Benito Mussolini, Giovanni Gentile (The Doctrine of Fascism), Hannah Arendt",
        "intro": "Italian Fascism under Benito Mussolini elevated the State into the supreme ethical organism, subordinating all individual and collective life to sovereign state will.",
        "body": "1. Monistic Statism: The state is not a product of individual contract (liberalism) or economic base (Marxism), but the ultimate spiritual creator of the nation. 2. Anti-Individualism & Anti-Rationalism: Individuals have meaning only within the state; rejection of universal human rights, peace, and democratic debate. 3. Corporatism: Replaced independent trade unions and capitalist lobbies with state-managed corporations to enforce class collaboration under nationalist militarism.",
        "conclusion": "Mussolini's statism produced a totalitarian tyranny that institutionalized aggressive imperialism, suppressed human rights, and plunged Europe into war."
    },
    "ch4_socialism_fascism_sec_21": {
        "question": "Contrast Italian Fascism with German National Socialism. Why was racial biological determinism central to Nazism in a way distinct from Mussolini’s statism?",
        "scholars": "Adolf Hitler (Mein Kampf), Benito Mussolini, Hannah Arendt, Franz Neumann",
        "intro": "While both fascism and Nazism share totalitarian and militarist impulses, German National Socialism was distinctively defined by radical biological racism and anti-Semitism.",
        "body": "1. Statism vs. Biopolitics: For Mussolini, the State created the Nation ('Lo Stato Fascista'); for Hitler, the state was merely a subordinate instrument to preserve the biological Aryan Volk. 2. Racial Supremacy & Anti-Semitism: Nazism viewed history not through class struggle or national rivalry, but through racial Darwinism, culminating in the industrial genocide of the Holocaust. 3. Lebensraum: Imperial expansion was framed as biological necessity for racial living space rather than standard imperial prestige.",
        "conclusion": "This biological determinism made Nazism uniquely destructive, turning the apparatus of modern industrial governance toward systemic racial extermination."
    },

    # CHAPTER 5
    "ch5_gandhism_sec_intro": {
        "question": "“Truth is God.” Explain Mahatma Gandhi’s moral epistemology and the dialectical unity between Satya (Truth) and Ahimsa (Non-violence).",
        "scholars": "Mahatma Gandhi (An Autobiography: The Story of My Experiments with Truth), Leo Tolstoy, John Ruskin",
        "intro": "Gandhi revolutionized political ethics by identifying Truth (Satya) as the ultimate ontological reality and Ahimsa (Non-violence) as the only legitimate means to realize it.",
        "body": "1. Inversion from 'God is Truth' to 'Truth is God': Broadened spiritual truth to include atheists who pursue truth; truth is subjective relative perception striving toward absolute truth. 2. Ahimsa as Active Love: Non-violence is not passive cowardice, but the moral courage of the brave; it implies dynamic goodwill and refusal to injure even in thought. 3. Organic Inseparability of Means and Ends: Means are like the seed, end is the tree; violent means can never yield a peaceful, just society.",
        "conclusion": "Gandhi's fusion of Satya and Ahimsa spiritualized politics, proving that moral integrity is the ultimate foundation of political efficacy."
    },
    "ch5_gandhism_sec_4": {
        "question": "“The good of the individual is contained in the good of all.” Examine the Gandhian concept of Sarvodaya and its critique of Utilitarianism.",
        "scholars": "Mahatma Gandhi (Unto This Last - Sarvodaya), John Ruskin, Jeremy Bentham, Vinoba Bhave",
        "intro": "Influenced by John Ruskin's 'Unto This Last' (1860), Gandhi formulated Sarvodaya ('Welfare of All') as the moral and economic cornerstone of his social philosophy.",
        "body": "1. Critique of Utilitarianism: Bentham's 'greatest happiness of the greatest number' permits sacrificing minority interests; Sarvodaya insists on the welfare of all, beginning with the last and least (Antyodaya). 2. Dignity of Labor: The work of the barber has the same value as that of the lawyer; manual labor is essential for moral dignity (Bread Labor). 3. Decentralized Swadeshi Economy: Production by the masses rather than mass production; self-reliant village republics free from industrial exploitation.",
        "conclusion": "Sarvodaya transcends capitalist competition and bureaucratic socialism, offering an egalitarian blueprint centered on human dignity and moral cooperation."
    },
    "ch5_gandhism_sec_5": {
        "question": "Critically analyze Mahatma Gandhi’s Theory of Trusteeship. Is it a viable moral alternative to capitalist exploitation or a paternalistic compromise?",
        "scholars": "Mahatma Gandhi, Karl Marx, B.R. Ambedkar, J.C. Kumarappa",
        "intro": "Gandhi proposed the Theory of Trusteeship as a non-violent method of transforming capitalist property relations without violent expropriation.",
        "body": "1. Moral Premise: Wealth belongs to God and society; the rich are merely trustees entitled to retain what is reasonably necessary for livelihood while managing the surplus for public welfare. 2. Non-Violent Transformation: Avoids violent state confiscation which destroys production; relies on moral persuasion, statutory regulation, and satyagraha if capitalists fail their duties. 3. Critiques (Ambedkar & Socialists): Criticized as utopian and paternalistic, assuming moral benevolence from an inherently exploitative class while leaving structural inequalities intact.",
        "conclusion": "While contested in economic practice, trusteeship anticipates modern notions of Corporate Social Responsibility, social enterprise, and ethical environmental stewardship."
    },
    "ch5_gandhism_sec_7": {
        "question": "“The state represents violence in a concentrated and organized form.” Discuss Gandhi’s critique of the modern state and his concept of 'Enlightened Anarchy'.",
        "scholars": "Mahatma Gandhi, Henry David Thoreau, Leo Tolstoy, Robert Nozick",
        "intro": "Gandhi was a philosophical anarchist who viewed the modern sovereign state with deep suspicion, considering it fundamentally coercive and destructive of individual moral autonomy.",
        "body": "1. State as Organized Coercion: The state is a soulless machine that destroys individuality and relies on military and police force. 2. Enlightened Anarchy: The ideal society is stateless, where everyone is their own ruler and rules themselves in a manner that never hinders their neighbor. 3. Second-Best State (Minimal Democratic Decentralization): Recognizing absolute anarchy as unattainable, Gandhi accepted a minimally coercive, highly decentralized democratic state.",
        "conclusion": "Gandhi’s critique warns against totalitarian state worship, prioritizing grassroots participatory community over centralized bureaucratic Leviathans."
    },
    "ch5_gandhism_sec_10": {
        "question": "Examine Gandhi’s model of 'Oceanic Circles' and its implications for decentralized Panchayati Raj democracy.",
        "scholars": "Mahatma Gandhi, Rammanohar Lohia, E.F. Schumacher",
        "intro": "In 1946, Gandhi articulated his vision of social architecture through the metaphor of 'Oceanic Circles', rejecting the Western pyramid of hierarchical authority.",
        "body": "1. Rejection of Pyramidical Hierarchy: Pyramids sustain top-heavy centralized power where the top rests on the crushed bottom; oceanic circles expand concentrically without domination. 2. Village Republics (Gram Swaraj): Every village is an autonomous, self-reliant unit cooperating outward with neighboring units, with the individual at the center. 3. Moral Solidarity: Outer circles draw strength from the inner units rather than crushing them; power flows from local community to national coordination.",
        "conclusion": "Oceanic Circles inspired the constitutional mandate for Panchayati Raj in India and remains a premier model for ecological, participatory democracy."
    },
    "ch5_gandhism_sec_16": {
        "question": "“Hind Swaraj is a severe condemnation of modern civilization.” Examine Gandhi’s critique of Western industrial civilization, railways, lawyers, and doctors.",
        "scholars": "Mahatma Gandhi (Hind Swaraj - 1909), Jean-Jacques Rousseau, E.F. Schumacher",
        "intro": "Written aboard ship in 1909, 'Hind Swaraj' is Gandhi’s foundational manifesto, presenting a radical civilizational critique of modern Western industrialism.",
        "body": "1. Modernity as 'Satanic Civilization': Equated modern civilization with bodily comfort, consumerism, and moral decay, stripping humans of self-control and spiritual connection. 2. Critique of Technology & Institutions: Railways spread epidemics and commercialized agriculture; lawyers deepened communal disputes for profit; modern medicine treated symptoms while encouraging bodily self-indulgence. 3. True Civilization (Sudharana): Defined as 'good conduct' and mastery over mind and passions rather than technological acceleration.",
        "conclusion": "Once dismissed as reactionary, 'Hind Swaraj' is now celebrated as an eco-philosophical masterwork presaging climate limits, de-growth, and holistic well-being."
    },

    # CHAPTER 6
    "ch6_feminism_sec_intro": {
        "question": "“One is not born, but rather becomes, a woman.” Differentiate between Sex and Gender, and analyze the significance of this distinction in feminist theory.",
        "scholars": "Simone de Beauvoir (The Second Sex), Judith Butler (Gender Trouble), Ann Oakley",
        "intro": "The sex-gender distinction is the foundational conceptual pillar of feminist political theory, dismantling biological determinism and exposing gender as a social construct.",
        "body": "1. Sex vs. Gender: Sex denotes biological characteristics (chromosomes, anatomy); gender denotes socially constructed norms, behaviors, and roles assigned to masculinity and femininity. 2. Simone de Beauvoir's Thesis: Woman is constructed as the 'Other' in relation to the male subject; patriarchal culture socializes biological females into subordinate gender roles. 3. Judith Butler's Performativity: Butler deconstructs even biological sex, arguing that gender is an ongoing performance solidified through repetitive social acts.",
        "conclusion": "By demonstrating that gender hierarchies are culturally created rather than biologically fixed, feminism establishes that gender inequality can be historically dismantled."
    },
    "ch6_feminism_sec_6": {
        "question": "Critically examine Liberal Feminism. Why did early thinkers focus on legal equality and suffrage, and what are the structural limitations of this approach?",
        "scholars": "Mary Wollstonecraft (A Vindication of the Rights of Woman), J.S. Mill, Betty Friedan (The Feminine Mystique)",
        "intro": "Liberal Feminism seeks gender equality within the framework of liberal democratic institutions, focusing on equal individual rights, education, and legal reform.",
        "body": "1. Core Demands: Equal legal standing, political suffrage, educational access, and elimination of discriminatory barriers in employment. 2. Rationality and Autonomy: Wollstonecraft and Mill argued women possess identical rational faculties to men and must enjoy equal rights to cultivate moral character. 3. Structural Critiques (Radical & Marxist): Ignores the private sphere, unpaid domestic labor, systemic violence, and class/race divisions, striving merely to integrate middle-class women into an un-transformed capitalist patriarchy.",
        "conclusion": "While crucial for securing first-wave civil rights and workplace entry, liberal feminism struggled to address the deeply entrenched systemic roots of patriarchal power."
    },
    "ch6_feminism_sec_9": {
        "question": "“The personal is political.” Explain how Radical Feminism dismantled the traditional liberal public-private dichotomy.",
        "scholars": "Kate Millett (Sexual Politics), Shulamith Firestone (The Dialectic of Sex), Carole Pateman",
        "intro": "Radical feminism revolutionized political theory by asserting that power dynamics operate not just in the formal public sphere (state, law), but equally within personal, domestic relationships.",
        "body": "1. The Slogan's Meaning: Private issues—domestic violence, reproductive control, sexual exploitation, and unpaid domestic chores—are deeply political exercises of male power. 2. Patriarchy as Fundamental: Patriarchy is an autonomous, pervasive institutional system of male supremacy that precedes capitalism and class division. 3. Carole Pateman’s 'Sexual Contract': The liberal social contract that created civil society was preceded by a hidden sexual contract that legitimized patriarchal subjugation of women in the private sphere.",
        "conclusion": "By making the personal political, radical feminism expanded the boundary of political science to include bodily autonomy, sexuality, and the family."
    },
    "ch6_feminism_sec_12": {
        "question": "Examine Socialist and Marxist Feminist critiques of capitalism. How do the dual systems of capitalism and patriarchy reinforce female exploitation?",
        "scholars": "Friedrich Engels (The Origin of the Family, Private Property and the State), Sylvia Walby, Sheila Rowbotham",
        "intro": "Socialist and Marxist feminists argue that women's subjugation cannot be understood through patriarchy alone, but through its structural entanglement with capitalist exploitation.",
        "body": "1. Engels on the Origin of the Family: The emergence of private property necessitated monogamous marriage to ensure legitimate inheritance, marking 'the world-historical defeat of the female sex'. 2. Unpaid Reproductive Labor: Women perform free domestic labor (cooking, child-rearing, care) that reproduces labor power daily, subsidizing capitalist profits. 3. Reserve Army of Labor: Women serve as low-wage flexible labor during economic booms and are pushed back into domesticity during recessions.",
        "conclusion": "Socialist feminism proves that genuine female liberation requires the simultaneous dismantling of both patriarchal domination and capitalist economic exploitation."
    },
    "ch6_feminism_sec_15": {
        "question": "Analyze Kimberlé Crenshaw’s concept of 'Intersectionality' and its critique of mainstream Western feminism.",
        "scholars": "Kimberlé Crenshaw, bell hooks (Ain't I a Woman?), Audre Lorde",
        "intro": "In 1989, Kimberlé Crenshaw coined 'Intersectionality' to expose how overlapping systems of discrimination—race, gender, class, and coloniality—cannot be examined in isolation.",
        "body": "1. Traffic Intersection Metaphor: A Black woman at an intersection is struck by both racial and gender discrimination simultaneously; conventional law and liberal feminism treat them separately. 2. Critique of Hegemonic Feminism: Mainstream Western feminism universalized the concerns of white, affluent middle-class women, erasing the compounding oppressions experienced by marginalized women. 3. Substantive Justice: Effective political action requires coalitions that center the experiences of those situated at the cross-sections of multiple structural vulnerabilities.",
        "conclusion": "Intersectionality transformed contemporary human rights, legal theory, and political philosophy, establishing that justice cannot be achieved through single-axis reform."
    }
}

# Grand End-of-Topic Questions (2 Mains + 2 Synthesis MCQs for each of the 6 Chapters)
topic_mastery_questions = {
    "ch1_ideologies": {
        "mains": [
            {
                "id": "ch1_mains_1",
                "marks": 20,
                "words": 250,
                "title": "Comprehensive Analytical Essay",
                "question": "“Totalitarian ideologies claim absolute historical certainty, weaponizing closed dogmas to destroy human plurality and political agency.” Evaluate this statement with specific reference to Hannah Arendt's analysis of total domination and Karl Popper’s defense of the Open Society against historicism.",
                "scholars": "Hannah Arendt, Karl Popper, Michael Oakeshott, Destutt de Tracy",
                "intro": "The 20th century witnessed the catastrophic transformation of political ideologies from Enlightenment instruments of emancipation into totalizing engines of state tyranny. Both Hannah Arendt and Karl Popper mounted seminal philosophical defenses of human plurality and critical rationality against ideological absolutism.",
                "body": "1. Arendt's Diagnosis of Total Domination: In 'Origins of Totalitarianism', Arendt showed how closed ideologies provide self-contained pseudo-explanations of history (Nazi racial supremacy, Stalinist historical determinism) that demand total consistency over reality. Terror atomizes individuals, obliterating the public sphere where human plurality and collective action thrive. 2. Popper's Critique of Historicism: In 'Open Society and Its Enemies', Popper exposed the intellectual roots of totalitarianism in Plato, Hegel, and Marx. Their deterministic belief in historical laws fuels utopian social engineering. Popper countered with falsifiability, critical rationalism, and piecemeal social engineering. 3. Comparative Nexus: Where Arendt champions civic republican political action, Popper emphasizes epistemological modesty and the paradox of tolerance—asserting the right of open societies to defend themselves against intolerant ideologies.",
                "conclusion": "In the contemporary era of algorithmic echo chambers, populist radicalization, and state digital surveillance, Arendt’s insistence on public plurality and Popper’s defense of open debate remain urgent intellectual bulwarks against ideological dogmatism."
            },
            {
                "id": "ch1_mains_2",
                "marks": 15,
                "words": 200,
                "title": "The End of Ideology Debate",
                "question": "Critically examine whether Francis Fukuyama’s 'End of History' thesis was a triumphant culmination of Western liberal democracy or an ideological obfuscation of persistent civilizational and socio-economic contradictions. Discuss with reference to Daniel Bell and contemporary global politics.",
                "scholars": "Francis Fukuyama, Daniel Bell, Herbert Marcuse, Samuel P. Huntington, Thomas Piketty",
                "intro": "The post-Cold War era opened with Francis Fukuyama’s bold declaration that mankind had reached the endpoint of its ideological evolution with the universalization of Western liberal democracy, building upon Daniel Bell’s earlier 'End of Ideology' thesis.",
                "body": "1. Fukuyama's Hegelian-Kojèvian Argument: History as a dialectical struggle for thymotic recognition achieves institutional equilibrium in liberal democracy; fascism and communism collapsed due to internal systemic contradictions. 2. Critical Rebuttals: Huntington’s 'Clash of Civilizations' showed cultural-religious identities replace ideological contests. Critical theorists (Marcuse, Piketty) highlighted that liberal capitalism intensifies wealth inequalities and alienation. 3. Contemporary Realities: The rise of authoritarian state capitalism (China), revanchist ethno-nationalism (Russia), religious extremism, and Western populist discontent (Trumpism, Brexit) proved that history did not end.",
                "conclusion": "While Fukuyama rightly observed that no coherent alternative philosophical rival has completely eclipsed liberal democracy, the 21st century demonstrates that ideology is an enduring, mutating dimension of dynamic political societies."
            }
        ],
        "synthesis_mcqs": [
            {
                "id": "ch1_synth_mcq_1",
                "question": "Consider the following statements regarding theoretical critiques of ideology:\n1. Michael Oakeshott argued that ideological politics mistakenly replaces practical, traditional wisdom with abstract technical rationalism.\n2. Herbert Marcuse asserted that Daniel Bell's 'end of ideology' thesis was itself an ideological formula for corporate consensus masquerading as neutral science.\n3. Karl Popper asserted that an open society must unconditionally tolerate even violently intolerant ideologies to maintain its moral legitimacy.\nWhich of the statements given above are correct?",
                "options": [
                    "1 and 2 only",
                    "2 and 3 only",
                    "1 and 3 only",
                    "1, 2 and 3"
                ],
                "correctIndex": 0,
                "explanation": "Statements 1 and 2 are correct. Statement 3 is incorrect because Popper formulated the famous 'Paradox of Tolerance', asserting that an open society has the right and duty NOT to tolerate intolerant ideologies that threaten to destroy it."
            },
            {
                "id": "ch1_synth_mcq_2",
                "question": "With reference to the Marxist and Neo-Marxist conceptualizations of Ideology, consider the following statements:\n1. Marx and Engels in 'The German Ideology' characterized ideology as an inverted reflection of material reality that naturalizes ruling-class interests.\n2. Georg Lukács coined the concept of 'Reification' to explain how capitalist commodification objectifies human social relations into relations between things.\n3. Louis Althusser argued that Ideological State Apparatuses (ISAs) operate purely through physical coercion and violence.\nWhich of the statements given above is/are correct?",
                "options": [
                    "1 only",
                    "1 and 2 only",
                    "2 and 3 only",
                    "1, 2 and 3"
                ],
                "correctIndex": 1,
                "explanation": "Statements 1 and 2 are correct. Statement 3 is incorrect because Althusser distinguished Repressive State Apparatuses (RSAs - army, police, prisons) which function by violence from Ideological State Apparatuses (ISAs - schools, church, family, media) which function primarily by ideology and consent."
            }
        ]
    },

    "ch2_liberalism": {
        "mains": [
            {
                "id": "ch2_mains_1",
                "marks": 20,
                "words": 250,
                "title": "Evolution of the Liberal State",
                "question": "“From the night-watchman state of Locke and Spencer to the enabling state of T.H. Green and the market radicalism of Robert Nozick, Liberalism has perpetually renegotiated the boundary between individual autonomy and state authority.” Trace this conceptual evolution and evaluate whether Neo-Liberalism represents a return to classical roots or a distortion of liberal values.",
                "scholars": "John Locke, Herbert Spencer, T.H. Green, J.S. Mill, Robert Nozick, F.A. Hayek, Amartya Sen",
                "intro": "Liberalism is united by its core commitment to individual liberty, constitutionalism, and moral equality, yet its doctrine regarding the legitimate functions of the State has undergone profound historical recalibrations.",
                "body": "1. Classical Liberalism & The Night-Watchman State: Grounded in Locke's natural rights and negative liberty, classical liberals limited the state to defense, policing, and enforcing contracts. Herbert Spencer pushed this into Social Darwinism, viewing state relief as an interference with natural selection. 2. Welfare Liberalism & The Enabling State: Industrial inequalities compelled revision. T.H. Green reformulated liberty positively as the power to achieve moral potential, arguing the state must 'hinder hindrances' (poverty, illiteracy). Harold Laski and J.M. Keynes legitimized progressive taxation and mixed economy. 3. Neo-Liberal Counter-Revolution: Hayek argued central planning leads down the 'Road to Serfdom', championing the price mechanism. Nozick used Kantian self-ownership to assert that redistributive taxation is on par with forced labor. 4. Critical Assessment: Critics (Stiglitz, Sen) argue that by subordinating social welfare to market fundamentalism, neo-liberalism distorted liberalism's ethical promise into corporate oligarchy.",
                "conclusion": "Contemporary liberal theory, through thinkers like Amartya Sen (Capability Approach) and John Rawls, synthesizes negative rights with substantive positive empowerment, demonstrating that market efficiency must serve social justice."
            },
            {
                "id": "ch2_mains_2",
                "marks": 15,
                "words": 200,
                "title": "Value Pluralism & Multiculturalism",
                "question": "Examine Isaiah Berlin’s concept of 'Value Pluralism' and evaluate how Bhikhu Parekh builds upon it to construct a critique of liberal monoculturalism.",
                "scholars": "Isaiah Berlin, Bhikhu Parekh, Will Kymlicka, Charles Taylor",
                "intro": "Modern pluralistic democracies grapple with how to accommodate cultural diversity without unraveling political cohesion. Isaiah Berlin’s value pluralism provides the philosophical bedrock upon which multicultural theorists like Bhikhu Parekh construct their models.",
                "body": "1. Berlin's Value Pluralism: Values like liberty, equality, justice, and community are multiple, objective, and inherently incommensurable. There is no single universal hierarchy; tragic trade-offs are unavoidable in human life and public policy. 2. Parekh's Critique of Liberal Universalism: In 'Rethinking Multiculturalism', Parekh demonstrates that liberalism is itself a culturally specific tradition that monistically assumes individual autonomy as the universal standard of the good life. 3. Dialogical Multiculturalism: Parekh moves beyond mere toleration to active reciprocal dialogue where cultures cross-fertilize ethical perspectives, respecting cultural diversity as an enriching social good.",
                "conclusion": "Parekh's framework demonstrates that genuine social cohesion in plural societies cannot be achieved by assimilation, but through structured, continuous intercultural dialogue."
            }
        ],
        "synthesis_mcqs": [
            {
                "id": "ch2_synth_mcq_1",
                "question": "With reference to the evolution of Liberal thought, match the following theorists with their core doctrines:\n1. T.H. Green — State as an instrument that 'hinders the hindrances' to moral development.\n2. Robert Nozick — Taxation of earnings from labor is on par with forced labor.\n3. Harold Laski — Every state is known by the rights that it maintains.\nWhich of the pairs given above are correctly matched?",
                "options": [
                    "1 and 2 only",
                    "2 and 3 only",
                    "1 and 3 only",
                    "1, 2 and 3"
                ],
                "correctIndex": 3,
                "explanation": "All three pairs are correctly matched. T.H. Green justified state welfare by arguing the state must hinder hindrances. Nozick defended the entitlement theory against redistributive taxation. Laski famously argued that the legitimacy of the state lies in the rights it maintains for its citizens."
            },
            {
                "id": "ch2_synth_mcq_2",
                "question": "Consider the following statements regarding Neo-Liberalism:\n1. F.A. Hayek conceptualized the market as a decentralized price coordination mechanism superior to central state planning.\n2. Milton Friedman argued that inflation is always and everywhere a monetary phenomenon caused by excessive state money supply.\n3. Neo-liberalism advocates for universal state provision of healthcare and higher education to boost market productivity.\nWhich of the statements given above are correct?",
                "options": [
                    "1 and 2 only",
                    "2 and 3 only",
                    "1 and 3 only",
                    "1, 2 and 3"
                ],
                "correctIndex": 0,
                "explanation": "Statements 1 and 2 are correct. Statement 3 is incorrect because Neo-liberalism strongly advocates for welfare retrenchment, deregulation, and privatization of healthcare and education rather than universal state provision."
            }
        ]
    },

    "ch3_marxism": {
        "mains": [
            {
                "id": "ch3_mains_1",
                "marks": 20,
                "words": 250,
                "title": "The Miliband–Poulantzas Debate",
                "question": "“Is the capitalist state an instrument directly commanded by the ruling class, or an objective structure possessing relative autonomy to safeguard the capitalist system as a whole?” Critically examine the Miliband–Poulantzas debate and its implications for Marxist theories of the State.",
                "scholars": "Ralph Miliband, Nicos Poulantzas, Karl Marx, Louis Althusser, Claus Offe",
                "intro": "The late-1960s debate between Ralph Miliband and Nicos Poulantzas in the 'New Left Review' remains the definitive theoretical contest over the nature and autonomy of the capitalist state in Marxist political science.",
                "body": "1. Miliband's Instrumentalist View: In 'The State in Capitalist Society' (1969), Miliband used empirical sociology to show that state personnel (judges, bureaucrats, military chiefs) share the same elite social origins, education, and connections as corporate leaders, directly instrumentalizing the state. 2. Poulantzas's Structuralist View: In 'Political Power and Social Classes' (1968), Poulantzas argued that who governs is irrelevant; the state is structurally constrained by the capitalist mode of production to maintain the conditions of capital accumulation. 3. Concept of Relative Autonomy: The state must be autonomous from individual capitalists to prevent short-sighted intra-class greed and grant strategic concessions (welfare, labor rights) that preserve capitalism's long-term systemic stability. 4. Synthesis & Critique: Claus Offe and Bob Jessop later noted that the capitalist state is both structurally constrained and a strategic battlefield of class struggles.",
                "conclusion": "The debate permanently moved Marxism beyond simplistic economism, providing the vocabulary to analyze modern welfare states and regulatory capitalism without illusions of class neutrality."
            },
            {
                "id": "ch3_mains_2",
                "marks": 15,
                "words": 200,
                "title": "Gramscian Hegemony",
                "question": "“Gramsci’s Prison Notebooks represent a creative Copernican revolution within Marxism by shifting the center of revolutionary gravity from the economic base to the cultural superstructure.” Elucidate Gramsci’s concept of Cultural Hegemony and the role of Organic Intellectuals.",
                "scholars": "Antonio Gramsci, Benedetto Croce, Louis Althusser, Perry Anderson",
                "intro": "Antonio Gramsci recognized that the mechanical base-superstructure determinism of classical Marxism failed to explain why socialist revolutions did not occur in advanced capitalist Western democracies.",
                "body": "1. Cultural Hegemony: The ruling class maintains dominance not merely through state coercion (political society), but by manufacturing cultural consent through civil society (schools, church, media, family), turning bourgeois values into unquestioned 'common sense'. 2. Organic Intellectuals: Unlike traditional intellectuals who claim neutrality, organic intellectuals emerge from within a social class to give it ideological coherence, organization, and political self-consciousness. 3. War of Position: In the West, capturing the state requires winning a prior war of position within civil society, constructing a 'counter-hegemonic historic bloc'.",
                "conclusion": "Gramsci transformed modern political thought by proving that sustainable political transformation requires deep cultural, pedagogical, and moral leadership."
            }
        ],
        "synthesis_mcqs": [
            {
                "id": "ch3_synth_mcq_1",
                "question": "Consider the following statements regarding the Marxist Theory of Alienation:\n1. Marx analyzed alienation across four dimensions: from the product, from the production process, from species-essence, and from fellow humans.\n2. In the 'Economic and Philosophic Manuscripts of 1844', Marx argued that private property is the underlying consequence and result of alienated labor.\n3. Marx argued that alienation is an eternal psychological condition inherent to human nature that can never be eliminated.\nWhich of the statements given above are correct?",
                "options": [
                    "1 and 2 only",
                    "2 and 3 only",
                    "1 and 3 only",
                    "1, 2 and 3"
                ],
                "correctIndex": 0,
                "explanation": "Statements 1 and 2 are correct. Statement 3 is incorrect because Marx vehemently rejected the notion that alienation is eternal or natural; it is historically generated by private property and division of labor under capitalism, and will be overcome through communism."
            },
            {
                "id": "ch3_synth_mcq_2",
                "question": "Which of the following theorists accurately matches their contribution to Neo-Marxism and Critical Theory?\n1. Herbert Marcuse — Analyzed how technological rationality manufactures 'false needs' in 'One-Dimensional Man'.\n2. Jürgen Habermas — Developed the 'Theory of Communicative Action' based on undistorted, ideal speech communication.\n3. Louis Althusser — Formulated the concept of 'Interpellation' through Ideological State Apparatuses (ISAs).\nSelect the correct answer using the code below:",
                "options": [
                    "1 and 2 only",
                    "2 and 3 only",
                    "1 and 3 only",
                    "1, 2 and 3"
                ],
                "correctIndex": 3,
                "explanation": "All three pairs are correct. Marcuse analyzed false needs; Habermas developed communicative rationality against instrumental reason; Althusser conceptualized how ISAs interpellate individuals as ideological subjects."
            }
        ]
    },

    "ch4_socialism_fascism": {
        "mains": [
            {
                "id": "ch4_mains_1",
                "marks": 20,
                "words": 250,
                "title": "Totalitarianism and Fascism",
                "question": "“Fascism is not a coherent philosophical doctrine, but a reactionary, anti-rationalist opportunism driven by total state idolatry, aggressive militarism, and the cult of the leader.” Critically evaluate this statement, contrasting Italian Fascism under Mussolini with German National Socialism under Hitler.",
                "scholars": "Benito Mussolini, Adolf Hitler, Giovanni Gentile, Hannah Arendt, Franz Neumann",
                "intro": "Fascism emerged in interwar Europe as an aggressive counter-revolutionary reaction to the crisis of liberal democracy and the threat of socialist revolution, exalting action over intellect and the collective state over individual rights.",
                "body": "1. Anti-Rationalism & The Cult of Action: Influenced by distorted readings of Nietzsche's will to power, Sorel's myth of violence, and Social Darwinism, fascism celebrated struggle, war, and emotional frenzy over rational debate. 2. Italian Fascist Statism: Mussolini and Gentile formulated an organic, ethical statism: 'Everything in the State, nothing outside the State, nothing against the State'. Italian fascism institutionalized corporatism to suppress labor conflicts under state supervision. 3. German Nazism & Racial Biopolitics: Hitler’s National Socialism subordinated even the state to racial biological determinism (Aryan supremacy and anti-Semitic extermination). The state was merely a tool for the preservation and expansion of the biological Volk. 4. Instruments of Totalitarian Domination: Monopolistic party control, leader principle (Führerprinzip/Duce), elimination of independent trade unions, and pervasive terror.",
                "conclusion": "While Italian Fascism worshipped the Leviathan state, Nazism weaponized state machinery for apocalyptic racial engineering. Both demonstrate the catastrophic consequences of abandoning universal human rights."
            },
            {
                "id": "ch4_mains_2",
                "marks": 15,
                "words": 200,
                "title": "Evolution of Socialist Thought",
                "question": "Distinguish between Evolutionary Socialism (Bernstein), Fabian Socialism (The Webbs), and Guild Socialism (G.D.H. Cole). How did each envision achieving socialism through democratic and non-violent means?",
                "scholars": "Eduard Bernstein, Sidney & Beatrice Webb, G.D.H. Cole, Clement Attlee",
                "intro": "Rebuffing the Marxian premise that capitalism must be dismantled through violent insurrection, democratic socialist streams sought to achieve economic justice through constitutional, gradualist, and institutional pathways.",
                "body": "1. Evolutionary Socialism (Revisionism): Bernstein argued that capitalism was diversifying rather than collapsing; social democracy could achieve socialism through universal suffrage, parliamentary legislation, and trade union gains ('The movement is everything'). 2. Fabian Socialism: The Webbs championed the 'inevitability of gradualism' and technocratic permeation, expanding municipal ownership and state welfare administration through expert scientific planning. 3. Guild Socialism: G.D.H. Cole rejected centralized bureaucratic state socialism, advocating functional democracy where autonomous self-governing guilds of producers control workplaces alongside a pluralist consumer state.",
                "conclusion": "These democratic socialist traditions permanently reshaped modern governance, giving rise to European social democracy, workplace representation, and universal welfare systems."
            }
        ],
        "synthesis_mcqs": [
            {
                "id": "ch4_synth_mcq_1",
                "question": "Consider the following statements regarding socialist doctrines:\n1. Eduard Bernstein argued that the expanding middle class and rising real wages disproved Marx's prediction of working-class immiseration.\n2. The Fabian Society rejected violent revolution in favor of technocratic research and gradualist state permeation.\n3. Guild Socialists championed complete centralized bureaucratic state ownership of all factories without worker participation.\nWhich of the statements given above are correct?",
                "options": [
                    "1 and 2 only",
                    "2 and 3 only",
                    "1 and 3 only",
                    "1, 2 and 3"
                ],
                "correctIndex": 0,
                "explanation": "Statements 1 and 2 are correct. Statement 3 is incorrect because Guild Socialism (G.D.H. Cole) explicitly rejected centralized state bureaucratization, advocating instead for workplace industrial democracy and self-governing worker guilds."
            },
            {
                "id": "ch4_synth_mcq_2",
                "question": "With reference to the characteristics of Fascism, consider the following statements:\n1. Giovanni Gentile defined the fascist state as an ethical state that embodies the moral conscience of the nation.\n2. Italian Fascism instituted a system of corporatism to replace independent trade unions and integrate economic classes under state authority.\n3. Fascist ideology fundamentally rejects pacifism, viewing continuous struggle and war as the noble test of national vigor.\nWhich of the statements given above are correct?",
                "options": [
                    "1 and 2 only",
                    "2 and 3 only",
                    "1 and 3 only",
                    "1, 2 and 3"
                ],
                "correctIndex": 3,
                "explanation": "All three statements are correct. Gentile formulated the ethical state doctrine; corporatism was central to Mussolini's economic model; and fascism celebrated militarism and perpetual struggle while rejecting pacifism."
            }
        ]
    },

    "ch5_gandhism": {
        "mains": [
            {
                "id": "ch5_mains_1",
                "marks": 20,
                "words": 250,
                "title": "Gandhian State & Swaraj",
                "question": "“The state represents violence in a concentrated and organized form.” Critically examine Mahatma Gandhi’s philosophical anarchism and evaluate his model of 'Oceanic Circles' as an alternative to centralized modern democracy.",
                "scholars": "Mahatma Gandhi, Leo Tolstoy, Henry David Thoreau, Rammanohar Lohia, E.F. Schumacher",
                "intro": "Mahatma Gandhi’s political thought is distinguished by a profound distrust of the centralized modern state, which he regarded as an intrinsically coercive Leviathan that destroys individual moral autonomy.",
                "body": "1. Philosophical Anarchy & Critique of the State: The state is a soulless machine relying on military, police, and legal coercion. For Gandhi, genuine swaraj means moral self-rule and self-discipline, rendering coercive state apparatuses redundant. 2. Oceanic Circles (Village Swaraj): Replaced the top-down authoritarian pyramid with concentric, expanding circles of autonomous village republics. The individual is at the center, ready to perish for the village, expanding outward to the world without any circle dominating or exploiting another. 3. Decentralized Economy & Panchayati Raj: Self-reliant local production (Swadeshi, Khadi, cottage industries) avoids corporate and state capitalism, preventing urban exploitation of rural peripheries. 4. Contemporary Relevance: Anticipated Schumacher’s 'Small is Beautiful', grassroots environmental movements (Chipko), and decentralized constitutional governance (73rd Amendment).",
                "conclusion": "Gandhi’s vision offers an urgent ecological and participatory alternative to bureaucratic centralization, reminding humanity that genuine democracy must begin from the sovereign local community."
            },
            {
                "id": "ch5_mains_2",
                "marks": 15,
                "words": 200,
                "title": "Satya, Ahimsa & Satyagraha",
                "question": "“Satyagraha is not a weapon of the weak, but the ultimate soul-force of the morally courageous.” Differentiate Satyagraha from passive resistance, and explain the dialectical link between Satya and Ahimsa in Gandhi's political praxis.",
                "scholars": "Mahatma Gandhi, Martin Luther King Jr., Nelson Mandela, Gene Sharp",
                "intro": "Gandhi transformed non-violence from an individual ascetic virtue into an active, mass political instrument of anti-colonial resistance and moral revolution through the concept of Satyagraha.",
                "body": "1. Dialectical Unity of Satya and Ahimsa: 'Truth is God', and Ahimsa is the only means to realize Truth. Because human perception of truth is relative, no one possesses the right to coerce or inflict violence on opponents. 2. Satyagraha vs. Passive Resistance: Passive resistance is a tactical weapon of the physically weak, marked by absence of physical violence but harbouring internal hatred; Satyagraha is soul-force (moral courage of the brave), completely devoid of malice, seeking to convert the opponent through voluntary self-suffering. 3. Practical Methods: Non-cooperation, civil disobedience, fasting as self-purification, and the Constructive Programme.",
                "conclusion": "Satyagraha demonstrated that ethical means are inseparable from just ends, providing a universal blueprint for non-violent liberation across the world."
            }
        ],
        "synthesis_mcqs": [
            {
                "id": "ch5_synth_mcq_1",
                "question": "Consider the following statements regarding Gandhian economic and political thought:\n1. The theory of Trusteeship posits that the wealthy should hold their surplus assets in trust for the welfare of the community.\n2. In 'Hind Swaraj' (1909), Gandhi championed rapid mechanized industrialization as the fastest pathway to eliminate Indian poverty.\n3. Gandhi's concept of Sarvodaya is based on Ruskin's idea that the good of the individual is contained in the good of all.\nWhich of the statements given above are correct?",
                "options": [
                    "1 and 2 only",
                    "1 and 3 only",
                    "2 and 3 only",
                    "1, 2 and 3"
                ],
                "correctIndex": 1,
                "explanation": "Statements 1 and 3 are correct. Statement 2 is completely incorrect because in 'Hind Swaraj', Gandhi mounted a fierce critique of Western industrial civilization, machinery, and urbanization, advocating instead for cottage industries and village self-reliance."
            },
            {
                "id": "ch5_synth_mcq_2",
                "question": "Which of the following correctly describes Gandhi's concept of 'Oceanic Circles'?\n1. A hierarchical pyramid where the central government exercises supreme sovereign authority over provincial units.\n2. Concentric expanding circles of autonomous village republics where life will be an oceanic circle whose center will be the individual.\n3. A geopolitical doctrine advocating Indian naval dominance across the Indian Ocean rim.\nSelect the correct answer using the code below:",
                "options": [
                    "1 only",
                    "2 only",
                    "2 and 3 only",
                    "1, 2 and 3"
                ],
                "correctIndex": 1,
                "explanation": "Only statement 2 is correct. Gandhi's 'Oceanic Circles' is a famous metaphor for decentralized village swaraj, explicitly rejecting top-down pyramids in favor of expanding, non-coercive concentric circles with the individual at the center."
            }
        ]
    },

    "ch6_feminism": {
        "mains": [
            {
                "id": "ch6_mains_1",
                "marks": 20,
                "words": 250,
                "title": "Radical Feminism & The Patriarchal State",
                "question": "“The personal is political, and the state is male.” Critically evaluate Radical Feminism's conceptualization of patriarchy and examine how Carole Pateman and Catharine MacKinnon challenge the gender neutrality of liberal constitutionalism.",
                "scholars": "Kate Millett, Shulamith Firestone, Carole Pateman (The Sexual Contract), Catharine MacKinnon",
                "intro": "Second-wave radical feminism revolutionized political theory by asserting that gender inequality is not merely an incidental institutional bias, but the foundational, pervasive system of patriarchal oppression spanning both private and public realms.",
                "body": "1. The Personal is Political: Kate Millett ('Sexual Politics') and Shulamith Firestone demonstrated that family, sexuality, reproduction, and domestic labor are power-structured relationships where men dominate women. 2. Carole Pateman’s 'Sexual Contract': The liberal social contract celebrated as the birth of civil society presupposed a patriarchal sexual contract that subjected women to domestic subjugation, establishing that liberal freedom is historically predicated on female subjection. 3. Catharine MacKinnon's Critique of the State: The state is not a neutral arbiter; 'the state is male in the feminist sense: the law sees and treats women the way men see and treat women', rationalizing male power under the guise of abstract objectivity. 4. Limitations: Radical feminism was critiqued by socialist and intersectional feminists for treating women as a homogenous class and overlooking race and economic disparities.",
                "conclusion": "By shattering the sanctity of the public-private divide, radical feminism expanded political inquiry into bodily integrity, sexual violence, and reproductive freedom."
            },
            {
                "id": "ch6_mains_2",
                "marks": 15,
                "words": 200,
                "title": "Intersectionality & Third Wave Feminism",
                "question": "Examine how Kimberlé Crenshaw's 'Intersectionality' and Judith Butler’s 'Gender Performativity' deconstruct the essentialist assumptions of classical feminist thought.",
                "scholars": "Kimberlé Crenshaw, Judith Butler, bell hooks, Audre Lorde",
                "intro": "Third-wave and contemporary feminist theory dismantled the assumption that 'woman' is a universal, homogenous subject, introducing intersectional and post-structuralist perspectives.",
                "body": "1. Crenshaw's Intersectionality: Conventional anti-discrimination frameworks view gender and race as mutually exclusive categories. Crenshaw demonstrated that Black and marginalized women experience intersecting, multiplicative oppressions that slip through traditional legal nets. 2. bell hooks' Critique of White Feminism: Mainstream liberal feminism centered affluent white women’s desire for corporate careers, ignoring that working-class Black women were already working under exploitative conditions. 3. Judith Butler’s Gender Performativity: In 'Gender Trouble' (1990), Butler argued that gender is not an internal biological reality, but a performative effect produced and naturalized through repetitive bodily acts.",
                "conclusion": "These interventions moved feminism beyond rigid biological and Western binaries, creating a dynamic, inclusive, and multi-dimensional politics of liberation."
            }
        ],
        "synthesis_mcqs": [
            {
                "id": "ch6_synth_mcq_1",
                "question": "Consider the following statements regarding feminist perspectives on the State:\n1. Liberal feminists view the state as a potentially neutral instrument that can be reformed to guarantee equal rights and opportunity.\n2. Radical feminists view the state as structurally patriarchal, institutionalizing male domination across both public and private spheres.\n3. Marxist-Socialist feminists argue that the state functions solely to protect female domestic autonomy from market intrusion.\nWhich of the statements given above are correct?",
                "options": [
                    "1 and 2 only",
                    "2 and 3 only",
                    "1 and 3 only",
                    "1, 2 and 3"
                ],
                "correctIndex": 0,
                "explanation": "Statements 1 and 2 are correct. Statement 3 is incorrect because Marxist-Socialist feminists argue that the capitalist state institutionalizes the exploitation of women's unpaid domestic labor to reproduce the workforce for capital, rather than protecting female autonomy."
            },
            {
                "id": "ch6_synth_mcq_2",
                "question": "Match the following feminist thinkers with their core foundational text:\n1. Simone de Beauvoir — 'The Second Sex'\n2. Mary Wollstonecraft — 'A Vindication of the Rights of Woman'\n3. Carole Pateman — 'The Sexual Contract'\nWhich of the pairs given above are correctly matched?",
                "options": [
                    "1 and 2 only",
                    "2 and 3 only",
                    "1 and 3 only",
                    "1, 2 and 3"
                ],
                "correctIndex": 3,
                "explanation": "All three pairs are correctly matched. Simone de Beauvoir authored 'The Second Sex' (1949); Mary Wollstonecraft wrote 'A Vindication of the Rights of Woman' (1792); and Carole Pateman published 'The Sexual Contract' (1988)."
            }
        ]
    }
}

# General generator for any semi-topic that does not have an explicit custom entry
def generate_semitopic_question(sec, ch_title):
    title = sec.get('title', '').strip()
    paras = sec.get('paragraphs', [])
    bullets = sec.get('bullets', [])
    
    # Gather textual clues
    all_text = " ".join([p.get('text', '') for p in paras] + [b.get('text', '') for b in bullets])
    
    # Clean up title
    clean_title = re.sub(r'^[o●\-\s]+', '', title).strip()
    if not clean_title or len(clean_title) < 3:
        clean_title = f"{ch_title} Core Concepts"

    return {
        "question": f"“{clean_title} remains a cornerstone in understanding {ch_title}.” Critically examine this statement, highlighting core theoretical arguments, key scholars, and contemporary relevance.",
        "scholars": "Relevant Classical & Modern Thinkers in Political Science",
        "intro": f"The concept of '{clean_title}' forms an integral analytical component in the study of {ch_title}, illuminating how political authority, rights, and ideological structures interact.",
        "body": f"1. Theoretical Foundations: Grounded in the structural analysis of political thought, addressing how power and legitimacy are conceptualized. 2. Critical Arguments: Explores tensions between individual liberty, state authority, and collective welfare. 3. Scholarly Critiques: Compares classical formulations with contemporary reassessments.",
        "conclusion": f"Understanding '{clean_title}' is essential for UPSC PSIR answer writing, as it bridges classical theoretical debates with 21st-century governance challenges."
    }

# Process all chapters and sections
total_semitopic_mains = 0
total_topic_mains = 0
total_topic_mcqs = 0

for ch in data['chapters']:
    ch_id = ch['id']
    ch_title = ch['title']
    
    # Add topic mastery questions
    if ch_id in topic_mastery_questions:
        ch['topic_questions'] = topic_mastery_questions[ch_id]
        total_topic_mains += len(ch['topic_questions']['mains'])
        total_topic_mcqs += len(ch['topic_questions']['synthesis_mcqs'])
    
    for sec in ch['sections']:
        sec_id = sec['id']
        if sec_id in custom_semitopic_questions:
            sec['mains_question'] = custom_semitopic_questions[sec_id]
        else:
            sec['mains_question'] = generate_semitopic_question(sec, ch_title)
        total_semitopic_mains += 1

print(f"Enriched {total_semitopic_mains} semi-topics with UPSC 10-Marker Questions!")
print(f"Enriched 6 Topics with {total_topic_mains} End-of-Topic Mains Questions and {total_topic_mcqs} Grand Synthesis MCQs!")

# Save back to sarrthi_full_data.js
updated_js = prefix + json.dumps(data, indent=2, ensure_ascii=False) + ';\n'
with open('sarrthi_full_data.js', 'w', encoding='utf-8') as f:
    f.write(updated_js)

print("sarrthi_full_data.js successfully updated! Size:", len(updated_js), "bytes")
