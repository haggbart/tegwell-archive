# Tegwell

Tegwell is a geothermal energy company based in Bergen, Norway. Its ambition is to make geothermal
energy work *anywhere* — not only in the few places on Earth where hot water sits conveniently
near the surface. Tegwell calls this "geothermal anywhere", and describes it as the long-promised
holy grail of the field.

The proposition: a single installation delivering three things at once from the heat of the Earth
— local heat, hydrogen, and electricity, around the clock, in places that have none of them today.

The material gathered here is the company's public content as it stood in 2024, when the website
was last updated. The site has been offline since, and this is the complete record of what it
contained — ready to read, to reuse, or to put back up.

## Two core technologies

**Optimized Closed-Loop Well.** A coaxial (pipe-in-pipe) closed-loop well, a known concept in
shallow geothermal, taken to deep wells. The working fluid circulates in the annulus and never
contacts the formation. Tegwell's addition: *adaptive radial jets* — lateral channels branched off
the main bore and backfilled with highly conductive material (graphite-based composites), with
position and length tuned per site, to raise heat conduction from the rock into the well.
Also explored: vacuum insulated tubing (VIT), hydraulic fracturing.

**Thermoelectric Power Plant.** Modular, autonomous, effectively maintenance-free conversion of
that heat to electricity. The design goal is plug-and-play operation with minimal training, so
communities without technical staff can run one. Validated in lab tests.

## Solutions (the applications)

- **Direct Heat** – hyper-local heat at point of use; ~80% of residential electricity goes to heat/cooling.
- **Grid Power** – geothermal as sustainable base load, with batteries for peak-hour boost.
- **Hydrogen Production** – high-temperature electrolysis on site; kills the transport/storage problem. Highway H2 + EV charging stations, ports, industrial zones.
- **Industrial Applications** – 24/7 energy to off-grid industrial sites.
- **Decentralized Energy Production** – not bound by geography or geology.
- **Community Energy Hubs – "SurPlusHavens"** – the flagship concept: self-sufficient communities that generate *more* energy than they consume and push the surplus back to the surrounding region, while staying grid-interconnected for peaks.

## Positioning

The case Tegwell makes rests on three claims: impact on the global energy crisis, genuinely novel
technology, and a rapidly expanding renewable market. Throughout, the material is careful about
maturity — the technologies are described as under development and validated in lab tests rather
than commercially deployed.

## Team

| Name | Role |
|---|---|
| Tomas Finnøy | CEO |
| Sondre Slathia | CTO (production & automation) |
| Benjamin D. Smith | Geothermal Energy Engineer, PhD candidate in wellbore tech |
| Gunstein Skomedal | Specialist in Thermoelectric Technology |

## Timeline

- **2022-09** – Research collaboration with the **University of Agder**, funded by **RFF Vestland**: thermoelectric generators for fully autonomous plants; radial jet drilling and hydraulic fracturing to raise heat transfer.
- **2022-10** – Benjamin Smith brought on to research deep coaxial heat exchanger feasibility; **University of Bergen** + **Reykjavik University** collaboration. State-of-the-art simulations in **FEFLOW (DHI)** and **CMG** showed decades-long extraction is plausible.
- **2023-08** – **Patent application filed** for a method of preparing closed-loop geothermal wells for optimal heat conduction.
- **2023-10** – **Finalist (top 5) in PIVOT2023**, the startup competition run by **Project Innerspace**, a non-profit pivoting oil & gas tech and talent into geothermal.

## About this archive

Open `tegwell-archive.html` in any browser to read everything as one document. It works offline and
needs nothing installed, and `tegwell-archive.pdf` is the same document as a file to send on or
print.

Underneath those, `content/` holds every page and article as a plain text file, `images/` holds all
66 images at full resolution, and `raw/` holds a complete backup of the content database. If the
site goes back up, `content/` is the material to build it from. Editing anything in `content/` and
running `.build/build.sh` regenerates the document and the PDF.
