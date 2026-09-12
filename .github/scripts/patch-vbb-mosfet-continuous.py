from pathlib import Path

p = Path('Virtual_Breadboard/js/circuit.js')
s = p.read_text()

def rep(old, new, name):
    global s
    if old not in s:
        raise SystemExit(name + ' anchor not found')
    s = s.replace(old, new, 1)

rep(
'''  const MOSFET_OFF_LEAKAGE_G = 2e-9;''',
'''  const MOSFET_OFF_LEAKAGE_G = 2e-9;
  // Precision channel model: square-law (Shichman-Hodges-class) large-signal
  // MOSFET with channel-length modulation. beta is calibrated so the low-Vds
  // slope at 2.5 V of overdrive matches the existing part's declared RDS(on).
  // The legacy threshold + fixed-RDS(on) model remains the default.
  const MOSFET_BETA_CAL_VOV = 2.5;
  const MOSFET_CHANNEL_LAMBDA = 0.02; // 1/V, modest channel-length modulation
  function mosfetChannelCurrent(c, vg, vd, vs, tempC) {
    const spec = mosfetSpec(c);
    const polarity = c.type === 'pmos' ? -1 : 1;
    const tempScale = Math.max(0.1, 1 + MOSFET_RDSON_TEMPCO * ((tempC == null ? 25 : tempC) - 25));
    const rdsEff = Math.max(spec.rdsOn * tempScale, 1e-6);
    const beta = 1 / (rdsEff * MOSFET_BETA_CAL_VOV);
    const vdsSigned = polarity * (vd - vs);
    let vgsEff;
    let vdsEff;
    let currentSign;
    if (vdsSigned >= 0) {
      vgsEff = polarity * (vg - vs);
      vdsEff = vdsSigned;
      currentSign = polarity;
    } else {
      // An enhanced MOSFET channel is bidirectional. When current reverses,
      // the lower-potential terminal becomes the effective source for the
      // channel equation; the explicit body diode remains a separate path.
      vgsEff = polarity * (vg - vd);
      vdsEff = -vdsSigned;
      currentSign = -polarity;
    }
    const vth = Math.abs(spec.vth);
    const vov = vgsEff - vth;
    if (!(vov > 0) || !(vdsEff > 0)) return 0;
    let id;
    if (vdsEff < vov) {
      id = beta * (vov * vdsEff - 0.5 * vdsEff * vdsEff) * (1 + MOSFET_CHANNEL_LAMBDA * vdsEff);
    } else {
      id = 0.5 * beta * vov * vov * (1 + MOSFET_CHANNEL_LAMBDA * vdsEff);
    }
    return currentSign * id;
  }
  function mosfetChannelRegion(c, vg, vd, vs) {
    const spec = mosfetSpec(c);
    const polarity = c.type === 'pmos' ? -1 : 1;
    const forward = polarity * (vd - vs) >= 0;
    const sourceV = forward ? vs : vd;
    const vgsEff = polarity * (vg - sourceV);
    const vdsEff = Math.abs(polarity * (vd - vs));
    const vov = vgsEff - Math.abs(spec.vth);
    if (!(vov > 0)) return 'cutoff';
    return vdsEff < vov ? 'triode' : 'saturation';
  }
  function mosfetChannelLinearization(c, vg, vd, vs, tempC) {
    const h = 1e-5;
    const id = mosfetChannelCurrent(c, vg, vd, vs, tempC);
    const gm = (mosfetChannelCurrent(c, vg + h, vd, vs, tempC) - mosfetChannelCurrent(c, vg - h, vd, vs, tempC)) / (2 * h);
    const gdd = (mosfetChannelCurrent(c, vg, vd + h, vs, tempC) - mosfetChannelCurrent(c, vg, vd - h, vs, tempC)) / (2 * h);
    const gss = (mosfetChannelCurrent(c, vg, vd, vs + h, tempC) - mosfetChannelCurrent(c, vg, vd, vs - h, tempC)) / (2 * h);
    return { id, gm, gdd, gss, ieq: id - gm * vg - gdd * vd - gss * vs };
  }''',
'MOSFET helper')

rep(
'''            if (this._fetChannelState.get(c.id)) {
              // real RDS(on) drift with the channel's OWN temperature --
              // silicon channel resistance rises with temperature, the
              // same direction (and rough magnitude) every real MOSFET
              // datasheet's RDS(on)-vs-T curve shows
              const rdsEff = spec.rdsOn * (1 + MOSFET_RDSON_TEMPCO * (tempOf(c.id) - 25));
              const g = 1 / rdsEff;
              stampG(d, d, g);
              stampG(s, s, g);
              stampG(d, s, -g);
              stampG(s, d, -g);
            }''',
'''            const continuousMosfet = solverOptions && solverOptions.mosfetModel === 'continuous';
            if (continuousMosfet) {
              const vg0 = previousVoltages.get(uf.find(c.gate)) || 0;
              const vd0 = previousVoltages.get(uf.find(c.drain)) || 0;
              const vs0 = previousVoltages.get(uf.find(c.source)) || 0;
              const lin = mosfetChannelLinearization(c, vg0, vd0, vs0, tempOf(c.id));
              // Newton Jacobian for drain->source channel current Id(Vg,Vd,Vs).
              // Drain KCL gets +Id; source KCL gets the exact opposite.
              stampG(d, g_, lin.gm); stampG(d, d, lin.gdd); stampG(d, s, lin.gss);
              stampG(s, g_, -lin.gm); stampG(s, d, -lin.gdd); stampG(s, s, -lin.gss);
              stampI(d, -lin.ieq); stampI(s, lin.ieq);
            } else if (this._fetChannelState.get(c.id)) {
              // real RDS(on) drift with the channel's OWN temperature --
              // silicon channel resistance rises with temperature, the
              // same direction (and rough magnitude) every real MOSFET
              // datasheet's RDS(on)-vs-T curve shows
              const rdsEff = spec.rdsOn * (1 + MOSFET_RDSON_TEMPCO * (tempOf(c.id) - 25));
              const g = 1 / rdsEff;
              stampG(d, d, g);
              stampG(s, s, g);
              stampG(d, s, -g);
              stampG(s, d, -g);
            }''',
'MOSFET stamp')

rep(
'''        previousVoltages = new Map(voltages);

        mosfets.forEach((f) => {''',
'''        mosfets.forEach((f) => {''',
'defer previous voltages')

rep(
'''          const vgs = vg - vs;
          const channelShouldBeOn = f.type === 'nmos' ? vgs > spec.vth : vgs < spec.vth;
          if (channelShouldBeOn !== this._fetChannelState.get(f.id)) {
            this._fetChannelState.set(f.id, channelShouldBeOn);
            changed = true;
          }''',
'''          const vgs = vg - vs;
          const continuousMosfet = solverOptions && solverOptions.mosfetModel === 'continuous';
          if (continuousMosfet) {
            const pvg = previousVoltages.get(uf.find(f.gate)) || 0;
            const pvs = previousVoltages.get(uf.find(f.source)) || 0;
            const pvd = previousVoltages.get(uf.find(f.drain)) || 0;
            const delta = Math.max(Math.abs(vg - pvg), Math.abs(vs - pvs), Math.abs(vd - pvd));
            if (delta > 1e-8) changed = true;
          } else {
            const channelShouldBeOn = f.type === 'nmos' ? vgs > spec.vth : vgs < spec.vth;
            if (channelShouldBeOn !== this._fetChannelState.get(f.id)) {
              this._fetChannelState.set(f.id, channelShouldBeOn);
              changed = true;
            }
          }''',
'MOSFET convergence/state')

rep(
'''          }
        });

        comparators.forEach((cp) => {''',
'''          }
        });
        previousVoltages = new Map(voltages);

        comparators.forEach((cp) => {''',
'commit previous voltages')

rep(
'''        diodeModel: solverOptions && solverOptions.diodeModel === 'newton' ? 'newton' : 'simple',
      };''',
'''        diodeModel: solverOptions && solverOptions.diodeModel === 'newton' ? 'newton' : 'simple',
        mosfetModel: solverOptions && solverOptions.mosfetModel === 'continuous' ? 'continuous' : 'simple',
      };''',
'solver metadata')

rep(
'''          const rdsEff = spec.rdsOn * (1 + MOSFET_RDSON_TEMPCO * (tempOf(c.id) - 25));
          const channelI = this._fetChannelState.get(c.id) ? (vd - vs) / rdsEff : 0;
          I = channelI + (vd - vs) * MOSFET_OFF_LEAKAGE_G;
          // self-heating from real channel conduction loss only (switching
          // loss is not modeled -- a real device's dominant loss at these
          // small currents/frequencies is conduction, not switching)
          updateTemp(c.id, channelI * channelI * rdsEff, THERMAL_SPEC.mosfet);''',
'''          const rdsEff = spec.rdsOn * (1 + MOSFET_RDSON_TEMPCO * (tempOf(c.id) - 25));
          const continuousMosfet = solverOptions && solverOptions.mosfetModel === 'continuous';
          const channelI = continuousMosfet
            ? mosfetChannelCurrent(c, vg, vd, vs, tempOf(c.id))
            : (this._fetChannelState.get(c.id) ? (vd - vs) / rdsEff : 0);
          I = channelI + (vd - vs) * MOSFET_OFF_LEAKAGE_G;
          // self-heating from real channel conduction loss only (switching
          // loss is not modeled -- a real device's dominant loss at these
          // small currents/frequencies is conduction, not switching)
          const channelPower = continuousMosfet ? Math.abs(channelI * (vd - vs)) : channelI * channelI * rdsEff;
          updateTemp(c.id, channelPower, THERMAL_SPEC.mosfet);''',
'MOSFET current')

rep(
'''      const mosfetStates = new Map();
      mosfets.forEach((f) => mosfetStates.set(f.id, {
        channelOn: this._fetChannelState.get(f.id),
        bodyDiodeOn: this._fetDiodeState.get(f.id),
      }));''',
'''      const mosfetStates = new Map();
      mosfets.forEach((f) => {
        const continuousMosfet = solverOptions && solverOptions.mosfetModel === 'continuous';
        const vg = voltages.get(uf.find(f.gate)) || 0;
        const vd = voltages.get(uf.find(f.drain)) || 0;
        const vs = voltages.get(uf.find(f.source)) || 0;
        const channelRegion = continuousMosfet ? mosfetChannelRegion(f, vg, vd, vs) : (this._fetChannelState.get(f.id) ? 'on' : 'cutoff');
        mosfetStates.set(f.id, {
          channelOn: continuousMosfet ? channelRegion !== 'cutoff' : this._fetChannelState.get(f.id),
          channelRegion,
          model: continuousMosfet ? 'continuous' : 'simple',
          bodyDiodeOn: this._fetDiodeState.get(f.id),
        });
      });''',
'MOSFET states')

rep(
'''    AC_RINT, MTJ_RINT, NMOS_PARTS, PMOS_PARTS, mosfetSpec, COMPARATOR_SPEC,''',
'''    AC_RINT, MTJ_RINT, NMOS_PARTS, PMOS_PARTS, mosfetSpec, mosfetChannelCurrent, mosfetChannelRegion, MOSFET_BETA_CAL_VOV, MOSFET_CHANNEL_LAMBDA, COMPARATOR_SPEC,''',
'exports')

p.write_text(s)
