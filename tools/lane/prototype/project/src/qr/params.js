// Every handling, camera and input setting in one table: default, range, step and unit, plus a note on the
// nearest Unreal Engine 5 Chaos Vehicles property. The tuning panel, the settings files and the exports are
// all generated from this table.
//
// `use` says what a setting changes: 'car' and 'cam' change the scripted drives' results, 'hand' and 'pad'
// only change how keys and a controller are read (scripted drives ignore those).
const P = [];
const add = (g, k, l, u, d, min, max, st, ue, use = 'car') => P.push({ g, k, l, u, d, min, max, st, ue, use });

// ---- Chassis
add('Chassis', 'mass', 'Mass (kerb)', 'kg', 950, 600, 1600, 5, 'UChaosWheeledVehicleMovementComponent.Mass (kg). Enter kerb mass plus driver.');
add('Chassis', 'driverMass', 'Driver', 'kg', 75, 0, 160, 5, 'Add to Mass.');
add('Chassis', 'frontWeight', 'Centre of mass position (front weight share)', '%', 62, 45, 72, 0.5, 'CenterOfMassOverride.X in cm = (frontWeight/100 - 0.5) x wheelbase x 100, forward of mid-wheelbase.');
add('Chassis', 'cgHeight', 'Centre of mass height', 'm', 0.44, 0.3, 0.8, 0.01, 'bEnableCenterOfMassOverride = true; CenterOfMassOverride.Z in cm, measured up from the ground at ride height (subtract your mesh origin height).');
add('Chassis', 'wheelbase', 'Wheelbase', 'm', 2.44, 2.1, 2.8, 0.01, 'Wheel bone positions in the skeletal mesh (cm).');
add('Chassis', 'trackF', 'Front track', 'm', 1.4, 1.2, 1.6, 0.01, 'Wheel bone positions (cm).');
add('Chassis', 'trackR', 'Rear track', 'm', 1.38, 1.2, 1.6, 0.01, 'Wheel bone positions (cm).');
add('Chassis', 'inertiaYaw', 'Yaw inertia', 'kg m2', 720, 700, 2600, 10, 'Chaos takes inertia from the physics asset. Compare, then correct with InertiaTensorScale.Z (up).');
add('Chassis', 'inertiaRoll', 'Roll inertia', 'kg m2', 360, 150, 900, 10, 'InertiaTensorScale.X (forward axis).');
add('Chassis', 'inertiaPitch', 'Pitch inertia', 'kg m2', 1300, 600, 2600, 10, 'InertiaTensorScale.Y (right axis).');
add('Chassis', 'cdA', 'Drag (drag area CdA)', 'm2', 0.72, 0.4, 1.2, 0.01, 'DragCoefficient x (ChassisWidth x ChassisHeight). Example: 0.37 with 164 cm x 113 cm.');
add('Chassis', 'liftA', 'Lift area ClA', 'm2', 0.12, 0, 0.6, 0.01, 'No direct equivalent. Leave DownforceCoefficient at 0.');

// ---- Roll and pitch: stiffness comes from the springs and anti-roll bars, damping from the dampers
add('Roll and pitch', 'springF', 'Front spring (pitch and roll stiffness)', 'N/m', 15500, 8000, 60000, 500, 'UChaosVehicleWheel.SpringRate on the front wheel class. Epic documents N/m, but the stock value (250) only holds a car if read as N/cm: check static sag and ride frequency before converting.');
add('Roll and pitch', 'springR', 'Rear spring (pitch and roll stiffness)', 'N/m', 9000, 8000, 60000, 500, 'SpringRate on the rear wheel class (same unit caveat).');
add('Roll and pitch', 'arbF', 'Front anti-roll bar (roll stiffness)', 'N/m', 2000, 0, 30000, 250, 'RollbarScaling on the front wheels (0 to 1, no physical unit). Raise from 0.15 until M6 roll matches.');
add('Roll and pitch', 'arbR', 'Rear anti-roll bar (roll stiffness)', 'N/m', 3250, 0, 30000, 250, 'RollbarScaling on the rear wheels. More rear share = more lift-off rotation.');
add('Roll and pitch', 'bumpF', 'Front damper, bump (damping)', 'N s/m', 1500, 300, 6000, 50, 'Chaos has one SuspensionDampingRatio per wheel.');
add('Roll and pitch', 'reboundF', 'Front damper, rebound (damping)', 'N s/m', 2900, 500, 9000, 50, 'Folded into SuspensionDampingRatio (no separate rebound in Chaos).');
add('Roll and pitch', 'bumpR', 'Rear damper, bump (damping)', 'N s/m', 1200, 300, 6000, 50, 'SuspensionDampingRatio, rear wheel class.');
add('Roll and pitch', 'reboundR', 'Rear damper, rebound (damping)', 'N s/m', 2300, 500, 9000, 50, 'Folded into SuspensionDampingRatio.');
add('Roll and pitch', 'bumpTravel', 'Bump travel to stop', 'm', 0.085, 0.03, 0.2, 0.005, 'SuspensionMaxRaise (cm).');
add('Roll and pitch', 'droopTravel', 'Droop travel', 'm', 0.1, 0.03, 0.25, 0.005, 'SuspensionMaxDrop (cm).');
add('Roll and pitch', 'bumpStopRate', 'Bump stop rate', 'N/m', 120000, 20000, 400000, 5000, 'No equivalent: Chaos clamps at SuspensionMaxRaise.');
add('Roll and pitch', 'tyreRate', 'Tyre vertical rate', 'N/m', 195000, 100000, 350000, 5000, 'No equivalent: Chaos wheels have no vertical tyre spring.');
add('Roll and pitch', 'unsprungF', 'Front unsprung mass', 'kg', 34, 15, 70, 1, 'UChaosVehicleWheel.WheelMass (affects wheel spin-up only in Chaos, not hop).');
add('Roll and pitch', 'unsprungR', 'Rear unsprung mass', 'kg', 30, 15, 70, 1, 'WheelMass, rear.');

// ---- Tyres
add('Tyres', 'muLat', 'Grip (peak sideways, dry)', 'mu', 0.98, 0.5, 1.6, 0.01, 'FrictionForceMultiplier together with the surface physical material friction. Tune until M8 matches.');
add('Tyres', 'muLong', 'Traction limit (peak lengthways grip, dry)', 'mu', 1.43, 0.5, 1.6, 0.01, 'FrictionForceMultiplier (Chaos has one multiplier for both directions). Sets wheelspin and braking.');
add('Tyres', 'lockGrip', 'Locked wheel grips the same in every direction (1) or like a rolling tyre (0)', '0-1', 1, 0, 1, 0.05, 'No direct equivalent. A locked, sliding wheel uses the lengthways grip sideways too, so a slide with the wheels locked stops as quickly as straight-line braking. In Chaos: raise the friction of a wheel while it is locked, or accept a longer handbrake-turn stop (M9).');
add('Tyres', 'peakSlipAngle', 'Tyre stiffness (slip angle at peak grip)', 'deg', 8.25, 4, 16, 0.25, 'A smaller angle is a stiffer tyre. LateralSlipGraph: put the peak at this angle; without a graph Chaos uses CorneringStiffness.');
add('Tyres', 'peakSlipRatio', 'Slip ratio at peak grip', 'ratio', 0.11, 0.05, 0.25, 0.005, 'SlipThreshold (longitudinal slip where the wheel counts as spinning).');
add('Tyres', 'wetGrip', 'Wet grip factor', 'x', 0.72, 0.3, 1, 0.01, 'Friction of the wet road Physical Material relative to dry. The wet braking runs (D2) use this factor.');
add('Tyres', 'wetShapeC', 'Curve shape C in the wet (grip lost once sliding)', '', 1.4, 1.1, 1.9, 0.01, 'Lower SideSlipModifier on wet materials: wet tyres lose more once sliding. Part of the wet setting.');
add('Tyres', 'shapeC', 'Curve shape C (grip lost once sliding)', '', 1.28, 1.1, 1.8, 0.01, 'Shape of LateralSlipGraph after the peak; SideSlipModifier controls grip kept while skidding. Also sets how much a locked or handbraked wheel still grips.');
add('Tyres', 'shapeE', 'Curve roundness E', '', -1.4, -4, 0.9, 0.05, 'Shape of LateralSlipGraph before the peak.');
add('Tyres', 'loadSens', 'Load sensitivity', 'per load', 0.1, 0, 0.4, 0.01, 'No direct equivalent. WheelLoadRatio (0 to 1) scales how much weight transfer changes grip.');
add('Tyres', 'nominalLoad', 'Nominal tyre load', 'N', 2600, 1500, 5000, 50, 'Reference only.');
add('Tyres', 'relaxLat', 'Relaxation length, sideways', 'm', 0.31, 0.1, 1.5, 0.01, 'No equivalent: Chaos tyres respond instantly.');
add('Tyres', 'relaxLong', 'Relaxation length, lengthways', 'm', 0.13, 0.05, 0.6, 0.01, 'No equivalent.');
add('Tyres', 'rollRes', 'Rolling resistance', 'coef', 0.013, 0.005, 0.04, 0.001, 'No wheel property: add as a small constant drag, or raise DragCoefficient slightly.');
add('Tyres', 'tyreRadius', 'Tyre radius', 'm', 0.283, 0.24, 0.36, 0.001, 'UChaosVehicleWheel.WheelRadius (cm).');
add('Tyres', 'tyreWidth', 'Tyre width', 'm', 0.165, 0.12, 0.26, 0.005, 'WheelWidth (cm).');
add('Tyres', 'wheelInertia', 'Wheel spin inertia', 'kg m2', 0.95, 0.4, 3, 0.05, 'Derived in Chaos from WheelMass and WheelRadius (0.5 m r2): pick WheelMass to match.');
add('Tyres', 'heavyGrip', 'Grip factor, heavy rain (town only)', 'x', 0.56, 0.3, 1, 0.01, 'Friction of the soaked road Physical Material.');
add('Tyres', 'cobbleGrip', 'Grip factor, cobbles (town only)', 'x', 0.86, 0.4, 1, 0.01, 'Friction of the cobble Physical Material relative to tarmac.');
add('Tyres', 'puddleLoss', 'Grip lost in standing water (town only)', 'x', 0.35, 0, 0.8, 0.01, 'Puddle Physical Material: friction = wet friction x (1 - this), more at speed.');

// ---- Steering
add('Steering', 'maxSteer', 'Steering lock (road-wheel angle at full lock)', 'deg', 38.5, 20, 45, 0.5, 'UChaosVehicleWheel.MaxSteerAngle on the front wheels (degrees). Here it is the mean of the two front wheels; the telemetry files carry it as max_steer_deg.');
add('Steering', 'steerSpeed', 'Steering speed (how fast the wheels follow the input)', '1/s', 7, 1, 40, 0.1, 'SteeringInputRate rise. Chaos moves the input at a fixed rate; this car follows with a first-order response, so match the measured M5 time, not this number.');
add('Steering', 'steerReturn', 'Return speed (how fast they come back to centre)', '1/s', 4.8, 1, 40, 0.1, 'SteeringInputRate fall. Match the measured M5 self-centring time.');
add('Steering', 'steerRateMax', 'Fastest steering movement', 'lock/s', 7, 0.5, 10, 0.1, 'Upper limit on how fast the wheels can swing: share of full lock per second.');
add('Steering', 'ackermann', 'Ackermann', '%', 70, 0, 100, 5, 'SteeringSetup.SteeringType = Ackermann.');
add('Steering', 'steerRatio', 'Steering ratio (steering wheel in the cabin)', ':1', 19.5, 10, 26, 0.5, 'Not a Chaos property: used for the steering wheel animation only.');

// ---- Engine
add('Engine', 'engineScale', 'Engine power (scale on the torque curve)', 'x', 1.37, 0.4, 2.5, 0.01, 'Scale EngineSetup.MaxTorque by this.');
// about 60 hp at 5500 to 6000 rpm and 92 Nm at 3500: an ordinary 1.3 of the period
const TQ = [[1000, 69], [1500, 78], [2000, 84], [2500, 89], [3000, 91], [3500, 92], [4000, 91], [4500, 87], [5000, 82], [5500, 77], [6000, 70], [6500, 59]];
for (const [r, t] of TQ) add('Engine torque', 'tq' + r, r + ' rpm', 'Nm', t, 0, 260, 1, 'EngineSetup.TorqueCurve key at ' + r + ' rpm, normalised: value / MaxTorque. EngineSetup.MaxTorque = the highest value in this table.');
add('Engine', 'idleRpm', 'Idle speed', 'rpm', 850, 600, 1200, 10, 'EngineSetup.EngineIdleRPM.');
add('Engine', 'limiterRpm', 'Rev limiter', 'rpm', 6500, 5000, 8000, 50, 'EngineSetup.MaxRPM.');
add('Engine', 'redlineRpm', 'Red line (gauge)', 'rpm', 6200, 5000, 8000, 50, 'Gauge only.', 'hand');
add('Engine', 'engineInertia', 'Engine and flywheel inertia', 'kg m2', 0.14, 0.05, 0.5, 0.01, 'EngineSetup.EngineRevUpMOI (how fast revs rise).');
add('Engine', 'engineBrake0', 'Engine braking at idle', 'Nm', 9, 0, 40, 1, 'EngineSetup.EngineBrakeEffect (single value in Chaos; use the torque at about 3500 rpm).');
add('Engine', 'engineBrake1', 'Engine braking rise', 'Nm/1000rpm', 6, 0, 20, 0.5, 'Folded into EngineBrakeEffect.');
add('Engine', 'throttleLag', 'Throttle response lag', 's', 0.07, 0, 0.3, 0.01, 'ThrottleInputRate rise and fall rates on the movement component.');

// ---- Gearbox
add('Gearbox', 'g1', '1st', ':1', 3.42, 2, 5, 0.01, 'TransmissionSetup.ForwardGearRatios[0].');
add('Gearbox', 'g2', '2nd', ':1', 1.95, 1.2, 3, 0.01, 'ForwardGearRatios[1].');
add('Gearbox', 'g3', '3rd', ':1', 1.29, 0.9, 2, 0.01, 'ForwardGearRatios[2].');
add('Gearbox', 'g4', '4th', ':1', 0.95, 0.7, 1.5, 0.01, 'ForwardGearRatios[3].');
add('Gearbox', 'g5', '5th', ':1', 0.76, 0.5, 1.2, 0.01, 'ForwardGearRatios[4].');
add('Gearbox', 'gR', 'Reverse', ':1', 3.38, 2, 5, 0.01, 'TransmissionSetup.ReverseGearRatios[0].');
add('Gearbox', 'finalDrive', 'Final drive', ':1', 3.94, 2.5, 5.5, 0.01, 'TransmissionSetup.FinalRatio.');
add('Gearbox', 'autoShiftRpm', 'Automatic: upshift at full throttle', 'rpm', 6350, 4500, 7500, 50, 'TransmissionSetup.ChangeUpRPM.');
add('Gearbox', 'shiftTime', 'Shift time', 's', 0.26, 0.05, 0.8, 0.01, 'TransmissionSetup.GearChangeTime.');
add('Gearbox', 'driveEff', 'Driveline efficiency', 'x', 0.9, 0.7, 1, 0.01, 'TransmissionSetup.TransmissionEfficiency.');
add('Gearbox', 'clutchTorque', 'Clutch torque capacity', 'Nm', 260, 120, 600, 10, 'No equivalent: Chaos has no clutch model.');

// ---- Brakes
add('Brakes', 'brakeTorque', 'Brake strength (total torque, full pedal)', 'Nm', 3250, 1500, 7000, 50, 'UChaosVehicleWheel.MaxBrakeTorque per wheel: front = total x split / 2, rear = total x (1 - split) / 2. bABSEnabled = false.');
add('Brakes', 'brakeBias', 'Front to rear split (share to the front)', '%', 78, 50, 90, 0.5, 'Split of MaxBrakeTorque between the front and rear wheel classes.');
add('Brakes', 'brakeLag', 'Brake response lag', 's', 0.0, 0, 0.3, 0.01, 'BrakeInputRate rise and fall rates on the movement component.');
add('Brakes', 'handbrakeGrip', 'Handbrake grip (sideways grip the rear tyres keep with the handbrake on)', 'x', 0.29, 0.2, 1, 0.01, 'No direct equivalent: lower the rear wheels\' SideSlipModifier or FrictionForceMultiplier while the handbrake is held. 1 is plain physics: a locked tyre grips the same in every direction.');
add('Brakes', 'handbrakeDrag', 'Handbrake drag (lengthways grip the rear tyres keep with the handbrake on)', 'x', 0.7, 0.3, 1, 0.01, 'No direct equivalent: scale the rear wheels\' FrictionForceMultiplier by this while the handbrake is held (and SideSlipModifier by handbrake grip / this). 1 is plain physics. Lower, the locked rear wheels slow the car less and, because the outer wheel carries the load in a turn, hold the nose back less: the car comes round further.');
add('Brakes', 'handbrakeLag', 'Handbrake response lag (lever and cable)', 's', 0.04, 0, 0.4, 0.01, 'HandbrakeInputRate rise and fall rates on the movement component.');
add('Brakes', 'handbrakeTorque', 'Handbrake strength (torque holding the rear wheels)', 'Nm', 2500, 0, 4000, 50, 'MaxHandBrakeTorque = this / 2 on each rear wheel, bAffectedByHandbrake = true on the rear only. Enough torque locks the rear wheels; what they still grip then is set by curve shape C.');

// ---- Driver aids ("mild", the default). With aids set to none, none of these act.
add('Driver aids', 'tcSlip', 'Traction control starts at (multiple of the slip at peak grip)', 'x peak', 1.4, 1, 4, 0.05, 'bTractionControlEnabled on the driven wheels; Chaos has no threshold to set, so match the wheelspin seen at launch (D1).');
add('Driver aids', 'tcCut', 'Traction control: most throttle it takes away', '0-1', 0.62, 0, 1, 0.01, 'No direct equivalent: the strength of the traction control.');
add('Driver aids', 'absSlip', 'Anti-lock holds this slip (multiple of the slip at peak grip)', 'x peak', 0.35, 0.35, 4, 0.05, 'bABSEnabled on all four wheels. Chaos holds the wheel near its slip threshold; match the dry braking distances (D2).');
add('Driver aids', 'absBand', 'Anti-lock: slip beyond that at which the brake is fully eased', 'x peak', 0.2, 0.2, 4, 0.05, 'No direct equivalent: how gently the anti-lock eases the brake.');
add('Driver aids', 'absAngle', 'Anti-lock stands back when the car slides wider than', 'deg', 9, 3, 90, 1, 'No direct equivalent. Past this body slip angle the wheels may lock, which stops a sliding car soonest and lets a handbrake turn come round.');
add('Driver aids', 'escGain', 'Stability nudge strength', 'x', 1, 0, 3, 0.05, 'No equivalent in Chaos: build as a yaw-rate correction, or leave out and match D6 recovery by hand.');
add('Driver aids', 'escHold', 'Stability nudge waits this long after the handbrake', 's', 1.5, 0, 5, 0.1, 'No equivalent: lets a handbrake turn finish before any correction.');

// ---- Camera (third person only)
add('Camera', 'camDist', 'Distance behind the car', 'm', 5.8, 3, 12, 0.1, 'SpringArm TargetArmLength (cm), measured back from the centre of mass along the ground.', 'cam');
add('Camera', 'camHeight', 'Height above the road', 'm', 1.8, 0.8, 4, 0.05, 'SpringArm origin height plus SocketOffset.Z (cm above the road).', 'cam');
add('Camera', 'camLag', 'Position lag', 's', 0.17, 0, 0.6, 0.01, 'SpringArm bEnableCameraLag = true, CameraLagSpeed = 1 / this.', 'cam');
add('Camera', 'camFovRest', 'Field of view at rest (horizontal)', 'deg', 62, 40, 100, 0.5, 'CameraComponent FieldOfView at 0 mph. Unreal counts field of view horizontally, as here.', 'cam');
add('Camera', 'camFovSpeed', 'Field of view at speed (horizontal)', 'deg', 80.5, 40, 110, 0.5, 'FieldOfView at the speed below, rising in a straight line from rest.', 'cam');
add('Camera', 'camFovMph', 'Speed for the full field of view', 'mph', 90, 30, 140, 1, 'The speed at which FieldOfView reaches the value above.', 'cam');
add('Camera', 'camFovRate', 'Field of view response', '1/s', 4, 0.5, 20, 0.5, 'Interp speed of the FieldOfView change.', 'cam');
add('Camera', 'camSwing', 'Swing behind the direction of travel', '1/s', 6.2, 1, 15, 0.1, 'SpringArm CameraRotationLagSpeed at speed (about half of it when crawling).', 'cam');

// ---- Controller (standard mapping)
add('Controller', 'padDeadzone', 'Stick dead zone', '0-1', 0.1, 0, 0.5, 0.01, 'Input dead zone on the steering axis.', 'pad');
add('Controller', 'padCurve', 'Steering curve (exponent)', '', 1.5, 1, 3, 0.05, 'Exponent on the stick: above 1, small stick moves steer gently.', 'pad');
add('Controller', 'padTrigger', 'Trigger dead zone', '0-1', 0.05, 0, 0.5, 0.01, 'Input dead zone on both triggers.', 'pad');

// ---- Keyboard: keys are on or off, so they are ramped into analogue values at these rates
add('Keyboard', 'keySteerIn', 'Steering ramps in', '1/s', 6, 0.5, 12, 0.1, 'Share of full input per second while a steering key is held.', 'hand');
add('Keyboard', 'keySteerOut', 'Steering returns to centre', '1/s', 12, 0.5, 20, 0.1, 'Share of full input per second after the key is released.', 'hand');
add('Keyboard', 'keyThrottleIn', 'Throttle ramps in', '1/s', 6.5, 1, 30, 0.5, 'ThrottleInputRate rise.', 'hand');
add('Keyboard', 'keyThrottleOut', 'Throttle ramps out', '1/s', 11, 1, 30, 0.5, 'ThrottleInputRate fall.', 'hand');
add('Keyboard', 'keyBrakeIn', 'Brake ramps in', '1/s', 5.5, 1, 30, 0.5, 'BrakeInputRate rise.', 'hand');
add('Keyboard', 'keyBrakeOut', 'Brake ramps out', '1/s', 13, 1, 30, 0.5, 'BrakeInputRate fall.', 'hand');
add('Keyboard', 'keyBrakeMax', 'Brake key reaches', '0-1', 0.84, 0.3, 1, 0.01, 'Pedal travel a held brake key gives: 0.84 stops just short of locking the front wheels on a dry road.', 'hand');
add('Keyboard', 'keyThrottleEase', 'Throttle key eases while the front wheels spin', '0-1', 0.5, 0, 1, 0.05, 'Share of the throttle a held key gives up during wheelspin (no driver aids selected).', 'hand');

// ---- Help for hand driving (keys and controller). Scripted drives bypass all of it.
add('Hand driving help', 'steerReach', 'Full input asks only for the lock that is useful at speed', '0 or 1', 1, 0, 1, 1, 'SteeringSetup.SteeringCurve (max steering against speed). 0 turns this off: full input is then always full lock.', 'hand');
add('Hand driving help', 'steerOnset', 'Hand steering rate (lateral g built per second)', 'g/s', 2.6, 1, 8, 0.1, 'SteeringInputRate rise rate plus SteeringSetup.SteeringCurve: the hands turn the wheels no faster than this builds cornering force.', 'hand');
add('Hand driving help', 'handLead', 'Hands lead the car\'s steering lag', 'x', 6, 0, 12, 0.1, 'No equivalent: the hands ask for more than they want by this many times the gap, so the wheels arrive sooner. 0 leaves the full lag.', 'hand');
add('Hand driving help', 'slipWindow', 'Slip-angle window', 'x peak', 1.25, 1, 2.5, 0.05, 'No equivalent: stops the front tyres being steered far past peak slip. Approximate with SteeringCurve.', 'hand');
add('Hand driving help', 'selfAlign', 'Self-aligning strength', '0-1', 0.9, 0, 1, 0.05, 'No equivalent: hands-off countersteer toward the direction of travel.', 'hand');

export const PARAM_DEFS = P;
export const GROUPS = ['Chassis', 'Tyres', 'Steering', 'Engine', 'Engine torque', 'Gearbox', 'Brakes', 'Driver aids', 'Roll and pitch', 'Camera', 'Controller', 'Keyboard', 'Hand driving help'];
export const TORQUE_RPMS = TQ.map((t) => t[0]);
export function defaultParams() { const o = {}; for (const d of P) o[d.k] = d.d; return o; }
// True if key k changes what the scripted drives measure.
const USE = {}; for (const d of P) USE[d.k] = d.use;
export const affectsDrives = (k) => USE[k] === 'car' || USE[k] === 'cam';
