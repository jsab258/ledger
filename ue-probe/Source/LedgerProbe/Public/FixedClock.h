// THE SIMULATION RUNS THE SAME AT ANY FRAME RATE, 23 September: Jafar's
// addition to the slice's definition of done - "cheap to get right now and
// expensive later".
//
// THE RULE, and the whole of it: the simulation never sees a frame's length.
// Frames pour their real seconds into an accumulator; the simulation is
// stepped in whole, fixed steps drawn out of it, so sixty frames a second and
// twenty frames a second, or a stutter, give the same steps with the same
// length and therefore the same world. What is left over waits for the next
// frame, and Alpha says how far into the next step the frame stands, for
// drawing only - never for deciding anything.
//
// A GUARD AGAINST THE SPIRAL: after a long hitch (a load, a breakpoint) the
// accumulator would demand hundreds of steps in one frame and fall further
// behind; MaxStepsPerFrame caps it and the rest is dropped and counted, so
// the world slows for a moment rather than freezing - and says so.
//
// Plain C++ with no engine types, so the port's native test proves it.
#pragma once

namespace LedgerSim
{
	struct FixedClock
	{
		double StepSeconds;
		int MaxStepsPerFrame;
		double Accumulated;
		long long StepsTaken;
		long long StepsDropped;

		explicit FixedClock(double InStepSeconds = 0.1, int InMaxStepsPerFrame = 8)
			: StepSeconds(InStepSeconds > 0.0 ? InStepSeconds : 0.1),
			  MaxStepsPerFrame(InMaxStepsPerFrame > 0 ? InMaxStepsPerFrame : 1),
			  Accumulated(0.0), StepsTaken(0), StepsDropped(0) {}

		// A frame's real seconds in; how many fixed steps to run now, out.
		int Advance(double FrameSeconds)
		{
			if (FrameSeconds > 0.0) { Accumulated += FrameSeconds; }
			// COUNTED IN WHOLE STEPS, with a hair of tolerance so ten frames
			// of 0.01 s make exactly one 0.1 s step despite binary fractions.
			const double Eps = StepSeconds * 1e-9;
			int Steps = 0;
			while (Accumulated + Eps >= StepSeconds && Steps < MaxStepsPerFrame)
			{
				Accumulated -= StepSeconds;
				++Steps;
			}
			if (Accumulated + Eps >= StepSeconds)
			{
				const long long Behind = (long long)((Accumulated + Eps) / StepSeconds);
				StepsDropped += Behind;
				Accumulated -= (double)Behind * StepSeconds;
			}
			if (Accumulated < 0.0) { Accumulated = 0.0; }
			StepsTaken += Steps;
			return Steps;
		}

		// How far the frame stands into the next step, 0 to 1: for drawing
		// between two simulated states, never for the simulation.
		double Alpha() const { return Accumulated / StepSeconds; }
	};
}
