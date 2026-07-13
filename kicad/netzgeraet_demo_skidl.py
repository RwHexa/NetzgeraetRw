"""
NetzgeraetRw — Demoboard (Falstad-Version, KLEINSPANNUNG, nicht isoliert)
========================================================================
Diskreter Sperrwandler-Regelkreis als LEHR-/DEMO-Board:
  12 V DC rein  ->  ~5 V raus, ~70 kHz, gemeinsame Masse (KEIN Netzbezug!).

Ideale Falstad-Bauteile -> reale ICs:
  Saegezahn-Quelle -> NE555 (Timing-Rampe)
  Komparator       -> LM393
  Fehlerverst.+Ref -> TL431
  Schalter         -> Logic-Level-MOSFET (IRLZ44N, G-D-S)

Erzeugt eine KiCad-8-Netzliste (.net) mit THT-Footprints -> Import in Pcbnew.

WICHTIG:
  * Startpunkt zum ABGLEICH auf dem Steckbrett (Frequenz, Kompensation, Gate).
  * Trafo-Dot/Phase am realen Uebertrager verifizieren.
  * T1-Footprint ist ein 4-Pin-PLATZHALTER -> durch echten Uebertrager ersetzen.
"""
import os
KI = r"C:\Program Files\KiCad\8.0\share\kicad\symbols"
os.environ["KICAD8_SYMBOL_DIR"] = KI
os.environ["KICAD_SYMBOL_DIR"]  = KI

from skidl import *
try:
    set_default_tool(KICAD8)
except NameError:
    set_default_tool(KICAD)

# ---------------- Footprints (in KiCad 8 verifiziert) ----------------
FP_R    = "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal"
FP_C    = "Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm"
FP_CP   = "Capacitor_THT:CP_Radial_D6.3mm_P2.50mm"
FP_D    = "Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal"
FP_DS   = "Diode_THT:D_DO-41_SOD81_P7.62mm_Horizontal"
FP_TO220= "Package_TO_SOT_THT:TO-220-3_Vertical"
FP_TO92 = "Package_TO_SOT_THT:TO-92_Inline"
FP_DIP8 = "Package_DIP:DIP-8_W7.62mm"
FP_CONN = "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical"
FP_TRAFO= "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical"  # Platzhalter (4 Pads)!

# ---------------- Netze ----------------
vin, gnd, vout = Net("VIN"), Net("GND"), Net("VOUT")
drain, clamp, gate, compout = Net("DRAIN"), Net("CLAMP"), Net("GATE"), Net("COMPOUT")
ramp, ctrl, fb, sec = Net("RAMP"), Net("CONTROL"), Net("FB"), Net("SEC")

# ---------------- Steckverbinder ----------------
J1 = Part("Connector_Generic", "Conn_01x02", ref="J1", value="12V DC IN", footprint=FP_CONN)
J2 = Part("Connector_Generic", "Conn_01x02", ref="J2", value="VOUT",      footprint=FP_CONN)
J1[1] += vin;  J1[2] += gnd
J2[1] += vout; J2[2] += gnd

# ---------------- Eingangssieb ----------------
Cin  = Part("Device", "C_Polarized", ref="Cin",  value="100uF/25V", footprint=FP_CP)
Cin2 = Part("Device", "C",           ref="Cin2", value="100nF",     footprint=FP_C)
Cin[1]  += vin; Cin[2]  += gnd
Cin2[1] += vin; Cin2[2] += gnd

# ---------------- Uebertrager (Flyback) ----------------
# Primaer: AB(2)=VIN, AA(1)=DRAIN | Sekundaer: SA(3)=SEC(Dot), SB(4)=GND
T1 = Part("Device", "Transformer_1P_1S", ref="T1", value="EE16, Np:Ns=2:1", footprint=FP_TRAFO)
T1[2] += vin; T1[1] += drain
T1[3] += sec; T1[4] += gnd

# ---------------- Schalttransistor (IRLZ44N = G-D-S) ----------------
Q1 = Part("Device", "Q_NMOS_GDS", ref="Q1", value="IRLZ44N", footprint=FP_TO220)
Q1[1] += gate; Q1[2] += drain; Q1[3] += gnd   # G, D, S

# ---------------- RCD-Snubber ueber Primaer ----------------
Dsn = Part("Device", "D", ref="Dsn", value="1N4148", footprint=FP_D)
Rsn = Part("Device", "R", ref="Rsn", value="100",    footprint=FP_R)
Csn = Part("Device", "C", ref="Csn", value="1nF",    footprint=FP_C)
Dsn[2] += drain; Dsn[1] += clamp              # A=DRAIN, K=CLAMP
Rsn[1] += clamp; Rsn[2] += vin
Csn[1] += clamp; Csn[2] += vin

# ---------------- Sekundaergleichrichtung ----------------
Dout  = Part("Device", "D_Schottky", ref="Dout",  value="1N5819",    footprint=FP_DS)
Cout  = Part("Device", "C_Polarized", ref="Cout", value="220uF/16V", footprint=FP_CP)
Cout2 = Part("Device", "C",           ref="Cout2",value="100nF",     footprint=FP_C)
Rload = Part("Device", "R",           ref="Rload",value="25",        footprint=FP_R)
Dout[2] += sec; Dout[1] += vout               # A=SEC, K=VOUT
Cout[1]  += vout; Cout[2]  += gnd
Cout2[1] += vout; Cout2[2] += gnd
Rload[1] += vout; Rload[2] += gnd

# ---------------- Oszillator/Rampe: NE555 ----------------
U1  = Part("Timer", "NE555P", ref="U1", value="NE555", footprint=FP_DIP8)
U1[8] += vin; U1[1] += gnd; U1[4] += vin      # VCC, GND, RESET(aktiv)
Ra  = Part("Device", "R", ref="Ra", value="2k2",  footprint=FP_R)
Rb  = Part("Device", "R", ref="Rb", value="9k1",  footprint=FP_R)
Ct  = Part("Device", "C", ref="Ct", value="1nF",  footprint=FP_C)
Ccv = Part("Device", "C", ref="Ccv",value="10nF", footprint=FP_C)
Ra[1] += vin;    Ra[2] += U1[7]               # VCC -> DIS
Rb[1] += U1[7];  Rb[2] += ramp                # DIS -> RAMP
U1[6] += ramp;   U1[2] += ramp                # THR & TR am Rampenknoten
Ct[1] += ramp;   Ct[2] += gnd
Ccv[1] += U1[5]; Ccv[2] += gnd                # CV entkoppeln
C555 = Part("Device", "C", ref="C555", value="100nF", footprint=FP_C)
C555[1] += vin;  C555[2] += gnd

# ---------------- PWM-Komparator: LM393 ----------------
U2 = Part("Comparator", "LM393", ref="U2", value="LM393", footprint=FP_DIP8)
U2[8] += vin; U2[4] += gnd                    # V+, V-
U2[2] += ramp                                 # IN1- = Rampe
U2[3] += ctrl                                 # IN1+ = Regelspannung
U2[1] += compout                              # OUT1 (Open-Collector)
U2[5] += gnd; U2[6] += vin                    # 2. Komparator stilllegen (OUT2 offen)
C393 = Part("Device", "C", ref="C393", value="100nF", footprint=FP_C)
C393[1] += vin; C393[2] += gnd
Rpull = Part("Device", "R", ref="Rpull", value="4k7", footprint=FP_R)   # Open-Collector Pull-up
Rpull[1] += vin; Rpull[2] += compout

# ---------------- Gate-Treiber ----------------
Rg   = Part("Device", "R", ref="Rg",   value="22",  footprint=FP_R)
Rgpd = Part("Device", "R", ref="Rgpd", value="10k", footprint=FP_R)
Rg[1] += compout; Rg[2] += gate
Rgpd[1] += gate;  Rgpd[2] += gnd

# ---------------- Fehlerverstaerker/Referenz: TL431 ----------------
U3 = Part("Reference_Voltage", "TL431LP", ref="U3", value="TL431", footprint=FP_TO92)
U3[1] += fb; U3[2] += gnd; U3[3] += ctrl      # REF, A, K
Rft   = Part("Device", "R", ref="Rft",   value="10k", footprint=FP_R)   # VOUT -> FB (Sollwert 5 V)
Rfb   = Part("Device", "R", ref="Rfb",   value="10k", footprint=FP_R)   # FB -> GND
Rctrl = Part("Device", "R", ref="Rctrl", value="2k2", footprint=FP_R)   # VIN -> CONTROL
Ccomp = Part("Device", "C", ref="Ccomp", value="10nF",footprint=FP_C)   # Kompensation
Rft[1] += vout; Rft[2] += fb
Rfb[1] += fb;   Rfb[2] += gnd
Rctrl[1] += vin; Rctrl[2] += ctrl
Ccomp[1] += ctrl; Ccomp[2] += fb

# ---------------- Ausgabe ----------------
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "NetzgeraetDemo.net")
generate_netlist(file_=OUT)
print("OK: Netzliste geschrieben ->", OUT)
