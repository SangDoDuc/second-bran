"""Englisch – Obama, Paris-Rede 2015 (Camden Town S. 116–117): 1 Outline der Gefahren, 2 Analyse der Sprache.
Einfaches Englisch. Zitate und Zeilen am Buchfoto geprüft (28.10.2026)."""
N = " "

HEADER_LEFT = "Englisch"
HEADER_RIGHT = "29.10.26"
TITLE = "Obama's speech at the UN climate conference in Paris (2015)"

BLOCKS = [
    ("h", "1. Dangers of climate change"),
    ("p", "In his speech at the UN climate conference in Paris in 2015, Barack Obama describes the dangers of "
          "climate change and asks world leaders to act together."),
    ("p", "First, he explains that climate change could shape this century more than any other problem and that "
          "no country is safe from it. The earth is already getting warmer, because most of the warmest years on "
          "record have happened since 2000. In Alaska he has seen the effects himself: the sea is destroying "
          "villages and coasts, the frozen soil is melting, the tundra is burning and glaciers are melting very fast."),
    ("p", "Then he warns about the future. Whole countries could disappear under water, cities could be abandoned "
          "and fields could stop producing food. This could lead to political problems and new conflicts, and many "
          "people would have to flee to other countries. Weak states and economies would not be able to cope with "
          "these problems, and the next generation would suffer most."),
    ("p", "However, Obama also says that it is not too late if all nations act together now."),

    ("h", "2. Analysis: language and communicative strategies"),
    ("p", "Obama uses many rhetorical devices to show how dangerous climate change is, to give his audience hope "
          "and to make them act."),
    ("p", f"Facts and numbers: Obama says that “fourteen of the fifteen warmest years on record have occurred "
          f"since the year 2000” (ll.{N}15-16). This shows that the danger is real and not only an opinion. As a "
          f"result, he seems serious and trustworthy."),
    ("p", f"Imagery: He describes his visit to Alaska, where “the sea is already swallowing villages” "
          f"(ll.{N}22-23). The sea is described like a monster that eats villages. This personification helps "
          f"the audience to imagine the danger."),
    ("p", f"Short sentences: “Submerged countries. Abandoned cities.” (ll.{N}30-31) paint a dark picture of the "
          f"future. The short, incomplete sentences work like a warning and create fear."),
    ("p", f"Repetition: The words “Right here. Right now.” (ll.{N}39-40) show that the world has to act "
          f"immediately. After the frightening pictures, this gives hope, because the future can still be changed."),
    ("p", f"Inclusive language: Obama often uses “we” and “our”, for example “we embrace our responsibility” "
          f"(ll.{N}49-50). As the leader of the USA, he admits that his country is part of the problem. This makes "
          f"him credible, and the audience feels like one team."),
    ("p", f"Anaphora: Several sentences start with “Here in Paris, let's” (ll.{N}75, 78, 82, 91). The repetition "
          f"shows a clear plan and calls the leaders to action."),
    ("p", f"Anecdote: Obama tells the story of a young Indonesian woman who asked him about climate change "
          f"(ll.{N}106-116). The tricolon “it wasn't about terrorism, it wasn't about the economy, it wasn't about "
          f"human rights” (ll.{N}110-112) shows that climate change is the most important topic for young people. "
          f"This appeals to the emotions of the audience."),
    ("p", f"Quotation: He quotes Martin Luther King, who said that “there is such a thing as being too late” "
          f"(ll.{N}125-126). The famous name makes the warning stronger and shows that time is running out."),
    ("p", f"Rhetorical question: “can we imagine a more worthy reward than that?” (ll.{N}145-146) makes the "
          f"listeners think about the future of their children and agree with him."),
    ("p", f"Contrast: At the end, he describes “A world that is marked not by conflict, but by cooperation” "
          f"(ll.{N}153-154). This antithesis creates a positive vision. His last words “Let's get to work.” "
          f"(l.{N}158) are a direct call to action."),
    ("p", "All in all, Obama first creates fear with facts and pictures of the dangers. Then he gives hope and "
          "finally calls on the leaders to act together. This makes his speech very convincing."),
]


def all_text():
    return " ".join([HEADER_LEFT, HEADER_RIGHT, TITLE] + [b[1].replace(N, " ") for b in BLOCKS])
