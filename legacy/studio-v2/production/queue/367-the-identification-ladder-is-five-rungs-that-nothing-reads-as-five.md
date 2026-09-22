line: simulation (Core/Acquaintance.cs, Core/Perception.cs, Game/Witnesses.cs)
spec: A RED TEAM ARGUED that the identification ladder produces a BINARY
  between anonymous and instantly caught. JAFAR ASKED FOR IT TO BE CHECKED
  AGAINST THE REAL IMPLEMENTATION BEFORE BEING TREATED AS TRUE, because it
  reasoned about a file that does not exist; the rungs live in
  `Core/Acquaintance.cs`.

  CHECKED 2026-09-16. THE ARGUMENT HALF SURVIVES, AND THE HALF THAT SURVIVES
  IS THE ONE THAT MATTERS.

  WHERE IT IS WRONG. Identification is NOT binary. `Perception.IdRung`
  (Perception.cs:160-177) returns 0 to 4, and rungs 1, 2 and 3 are silhouette,
  distinguishing mark and face, driven by distance, light and facing WITH NO
  FAMILIARITY AT ALL. A stranger is not anonymous: they can be seen in
  outline, picked out by a limp, or face-identified, none of which requires
  anyone to know who you are.

  WHERE IT IS RIGHT, AND THIS IS THE FINDING. FAMILIARITY ITSELF IS BINARY IN
  EFFECT. The ladder declares FIVE values:

      Stranger 0.00   HeardOfYou 0.20   Known 0.50   Close 0.80   Household 1.00

  and there are exactly TWO consumers of familiarity in the whole tree, both
  asking the same single question, `>= RecognitionFamiliarity` at 0.35:

      Perception.cs:172   familiarity >= RecognitionFamiliarity && metres <= ...
      Witnesses.cs:215    if (Acquaintance.CanNameYou(v.Familiarity)) KnowsYou++;

  So Stranger and HeardOfYou are INDISTINGUISHABLE, and Known, Close and
  Household are INDISTINGUISHABLE. Five declared rungs behave as two classes.
  The file's own comment says "The ordering is the part that carries meaning"
  and NOTHING READS THE ORDERING.
acceptance: either the rungs' ordering is read by something (and what reads it
  is named, with the behaviour that differs between Known, Close and Household
  stated), or the ladder says in its own comment that it is a two-class test
  today and the middle values are reserved rather than live
max_sessions: 1
status: READY 2026-09-16, filed and NOT started. Raised by Jafar from a red
  team, and RE-CHECKED AT THE SOURCE BEFORE BEING BELIEVED, which is what he
  asked for and which changed the finding rather than confirming it.

  THIS IS HIS OWN RULE OF THIS MORNING, THIRD INSTANCE IN A DAY: a declared
  value that nothing consults is decoration. `HeardOfYou = 0.20` carries
  fourteen lines of comment explaining why gossip must sit below recognition,
  and its only effect is to fail the same comparison `Stranger` fails.
  `Close = 0.80` is documented for recognition at twenty-five metres in the
  dark, and nothing distinguishes it from `Known`.

  WHY THIS IS NOT MERELY TIDYING, and it connects to queue 364: a two-class
  familiarity test is exactly the shape that makes the town close one way. If
  the only question ever asked is "can they name you", there is no room for a
  town that half-knows you, suspects you, or has heard something and is not
  sure. The middle of the ladder is where a route back would live.

  ONE THING NOT TO DO: do not delete the middle rungs to make the ladder honest
  about being binary. The values are a design statement that predates the
  consumers, and the right direction is almost certainly to read them rather
  than to remove them. Establish what should differ between Known, Close and
  Household BEFORE changing either side.
