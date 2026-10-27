// Sighting.cs, ported (27 October 2026, phase 3's port; the 5 October sweep's G1): who saw the window go, and what
// they do. The rules' home is the Core; this is its port, checked by the Sighting* golden rows. Since the same day the
// geography too (who stands where on Quay Street at the hour, and which way they look; the Core's Sighting.cs); the
// floor trace that keeps a body off a crate stays in CrimeProbe.h, being the engine's.
#pragma once

#include <algorithm>
#include <cmath>
#include <set>
#include <string>
#include <vector>
#include "CastDay.h"

namespace LedgerCore
{
	/// What a witness files about the deed (the review's A1; Jafar's A5 ruling, 30 September).
	enum class WitnessFiles { Nothing, NoiseOnly, StoryAboutHim };

	namespace Sighting
	{
		/// The swing and the glass going: anybody with a clear line on him watched that long.
		const double DeedSeconds = 1.0;

		/// Night is the game's own, from 19:00 to 07:00; an hour outside the day wraps round it.
		inline bool NightAt(int Hour)
		{
			const int H = ((Hour % 24) + 24) % 24;
			return H >= 19 || H < 7;
		}

		/// Daylight and the lamps that reach him, saturating; a lamp's reach held to 0 to 1.
		inline double LightOnHim(bool bNight, double LampReach)
		{
			const double Day = bNight ? 0.0 : 1.0;
			const double L = std::max(0.0, std::min(1.0, LampReach));
			return std::max(0.0, std::min(1.0, Day + L - Day * L));
		}

		/// A story about him only from a sighting the witness bank has words for; a noise alone is the damage heard.
		inline WitnessFiles WhatWitnessFiles(int Rung, bool bBankHasWords)
		{
			if (Rung <= 0) return WitnessFiles::NoiseOnly;
			return bBankHasWords ? WitnessFiles::StoryAboutHim : WitnessFiles::Nothing;
		}

		/// Only somebody who saw it shouts at him.
		inline bool WitnessShouts(int Rung) { return Rung >= 1; }

		// WHO STANDS WHERE ON QUAY STREET AT THE HOUR. Street metres: x along Quay Street, z across it from its middle.

		/// Within Quay Street's own stretch.
		inline bool OnQuayStreet(double X, double Z) { return X >= -10.0 && X <= 50.0 && std::fabs(Z) <= 10.0; }

		/// The counters, the office and the cafe stand 7.5 m either side of the street's middle, behind their windows.
		inline bool IndoorPlace(double Z) { return std::fabs(Z) >= 7.0; }

		/// Where a body stands for a place: an inside place's on its own pavement, straight out from it.
		inline void BodySpot(double X, double Z, double& OutX, double& OutZ)
		{
			OutX = X;
			OutZ = IndoorPlace(Z) ? (Z > 0.0 ? 4.6 : -4.6) : Z;
		}

		/// The same, at the place's own waiting spot along its pavement (the cast file's "body_x_m").
		inline void BodySpot(const CastDay& Cast, const std::string& Place, double X, double Z, double& OutX, double& OutZ)
		{
			double BX = X;
			Cast.BodyXOf(Place, BX);
			BodySpot(BX, Z, OutX, OutZ);
		}

		/// The yaw, in degrees, that faces from one point to another (0 up the street, 90 across it towards +z).
		inline double YawToFace(double FromX, double FromZ, double ToX, double ToZ)
		{
			return std::atan2(ToZ - FromZ, ToX - FromX) * 180.0 / 3.14159265358979323846;
		}

		/// Which way somebody at a place looks: out at the street (up it from the quay, in its middle).
		inline double StreetFacingYaw(double X, double Z)
		{
			return std::fabs(Z) < 0.5 ? YawToFace(X, Z, X + 10.0, Z) : YawToFace(X, Z, X, 0.0);
		}

		/// One person on Quay Street at the hour who could see the window go.
		struct Onlooker
		{
			std::string Id, Place;
			bool bBody = false;
			double X = 0.0, Z = 0.0, YawDeg = 0.0;
		};

		/// The onlookers at an hour: everybody on Quay Street then by the town's own rule, a body at its place's waiting
		/// spot, somebody inside at their place; a person with no body who is not inside is not counted.
		inline std::vector<Onlooker> OnlookersAt(const CastDay& Cast, int Day, int Hour, const std::set<std::string>& WithBodies)
		{
			std::vector<Onlooker> Out;
			for (const std::string& Id : Cast.People())
			{
				double X = 0.0, Z = 0.0;
				std::string Place;
				if (!Cast.Where(Id, Day, Hour, X, Z) || !Cast.PlaceOf(Id, Day, Hour, Place)) continue;
				if (!Cast.OnQuayStreet(Id, Day, Hour)) continue;
				Onlooker O;
				O.Id = Id;
				O.Place = Place;
				O.bBody = WithBodies.count(Id) > 0;
				if (!O.bBody && !IndoorPlace(Z)) continue;
				if (O.bBody) { BodySpot(Cast, Place, X, Z, O.X, O.Z); }
				else { O.X = X; O.Z = Z; }
				O.YawDeg = StreetFacingYaw(O.X, O.Z);
				Out.push_back(O);
			}
			return Out;
		}
	}
}
