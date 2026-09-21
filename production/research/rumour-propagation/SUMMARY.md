# How rumours actually spread, against what we assumed

Research topic 9, and the first of the ones that change the moat's design. I
compared what the research says with what our gossip code does. There are five
differences and one of them is our own two files disagreeing with each other.

## First: the famous answer is the wrong one

Anybody researching this hits Allport and Postman (1947) within a minute. Their
model says rumours get shorter as they travel: details are lost, a few are
exaggerated, the rest bends toward what the listener expected.

It does not hold up. Studies of rumours occurring naturally, rather than in a
lab, "have not found levelling and sharpening consistent with Allport and
Postman's work", and found that some rumours are actually EXTENDED as they
travel, and others barely change at all. There is even a published paper about
how badly the original study gets misquoted by the people citing it.

So the one model everyone would reach for is a 1947 laboratory result that
natural rumours do not reliably show. What survives is narrower and more useful:
rumours change as they pass, and the change is not reliably toward less. Some
grow in the telling. That is a different thing from a decay.

## The finding: two of our files disagree about the most important mechanism

Our gossip code says that when somebody hears a rumour they already hold, their
confidence goes to the higher of the two numbers and stops there. **So being told
the same thing by three different people is worth exactly as much as being told
it once by the best-placed of them.** There is no term anywhere for independent
sources.

Now compare our own informing file, which is where the player accuses somebody.
Its opening argument is: "truth is not an input. A true accusation nobody will
corroborate is ignored. A false one three people will swear to lands." And our
homicide file: "Every witness after the first. Corroboration is what turns one
person's word into a case."

So corroboration is the entire thesis of how the law weighs a claim, and the
rumour mill that produces the people who would corroborate does not model it at
all. Somebody in Meridian can be told by three neighbours that Tom did it and end
up exactly as certain as if one had told them.

The research is on the informing file's side. I am not proposing the fix, that is
design. But two of our files disagree about the single most important mechanism
either of them has, and that is worth knowing.

## Two things we chose without knowing we were choosing

**Our rumours die of weakness. Real ones die of boredom.** In our code a rumour
fades a little at every hop, and once it drops below a floor nobody repeats it.
The standard model in the literature has a third state: somebody who believes the
rumour perfectly well and has simply stopped mentioning it, because it is no
longer news.

Those make different towns. Ours says a rumour that reaches the far side of town
is a faint one. Theirs says the far side may hold it as firmly as the first
teller and just not bring it up. The second is what a small town actually feels
like, where "everyone knows and nobody says" is an ordinary Tuesday.

**Our close friendships carry information best. In reality it is the
acquaintances.** Our code multiplies a rumour's strength by how well two people
know each other, so talk moves best between close friends. The classic finding in
sociology is the opposite for reach: information crosses a network through weak
ties, because your close friends all know each other and already know what you
know.

For a town with seven districts and three rival outfits, that is the difference
between talk staying in the Hook and talk arriving at the Exchange.

## One number worth a second look

Our confidence drops to 80 percent of itself at every hop. That number sits under
a comment saying "Tunables" and I could find no measurement behind it. The
literature offers no replacement, because it does not use that shape at all. Our
own rule about never setting a threshold you have not measured applies.

## One gap that is not news

Our gossip has opportunity but no motive: people pass a rumour because they
happened to be in the same place and know each other well enough. The research
says people transmit for three reasons, to work out what is true, to get closer
to the person they are telling, and to make themselves look good. Nobody in our
mill has a reason to talk. That is the same problem our own notes describe
elsewhere as a population generator that "supplies names, not people".

## How much to trust this

Less than I would like. This is an academic topic and I read no papers, only
search summaries of abstracts and pages citing them, because the hosts are
blocked from where I work.

The one I most want read is a paper called "Gossipping Until You Get Tired of It:
A Network Model of the Adaptive Exchange of Rumors in a Small Scale Social
Environment". That title is a description of our game, and I could not open it.

I also went looking for the specific effect where hearing something repeatedly
makes you believe it more without making it any truer, which is the obvious thing
underneath the corroboration finding, and did not find it in the rumour
literature. It is a large and well-replicated field of its own and it is the next
thing worth reading.
