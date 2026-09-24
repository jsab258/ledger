// WHAT EACH METAHUMAN COSTS ON THE CARD, 24 September. Jafar: "MetaHumans
// replace the Mixamo stand-ins for the slice's cast ... Measure what each
// costs on the card, since the game, the voice and the conversation model
// share it."
//
// Armed from StartupModule by -LedgerMhCost and never otherwise, like every
// other probe switch. It rides the ordinary launch (the street and the pawn
// BuildInteractiveStreet already makes), stands each cast MetaHuman three and
// a half metres in front of the camera in turn, then all of them together,
// and writes ue-mhcost.txt: the card's time per frame and the textures'
// memory for each, against the same street with nobody in it.
#pragma once

namespace LedgerMhCost
{
	void Start();
}
