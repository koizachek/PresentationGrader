# Case-Text (Kontext für die Bewertung)

Extrahiert aus `1_Meditec_Teaching case_2026.pdf`. Lehrmaterial von Prof. Jan Marco Leimeister (IWI-HSG); nur zur Nutzung innerhalb der Lehrveranstaltung, nicht weiterverbreiten.

Pre-read Teaching case – Updated version (May, 2026)

From Products to Intelligent Services:
AI-Driven Transformation of a Medical
Equipment Manufacturer
Prof. Jan Marco Leimeister
Institute of Information Management (IWI HSG), University of St. Gallen, St. Gallen, Switzerland

This teaching case is intended for classroom discussion only and is not to be copied, distributed, or cited without the express
permission of the author.

Abstract
Meditec is a German manufacturer of instruments for surgeries. The company is quality leader in this
sector and supplies many German and international hospitals. However, the opportunities for
differentiation against competitors decrease continuously. New competitors from emerging markets
are challenging the market position of established companies in this industry. Most critically,
Meditec’s key patents on its proprietary sterile container technology, the company’s highest-margin
product line, are set to expire within eighteen months, eliminating one of its last remaining sources of
competitive differentiation. Meditec is therefore forced to fundamentally rethink its strategy and
business model in order to survive in this novel competitive environment. The management of
Meditec is weighing several strategic paths: an AI-enabled product-service system that transforms the
company into a customer-centric solution provider, a focused repositioning around premium single-
use instruments, or various forms of partnership or sale. The teaching case positions the servitization
option as a twin transformation, a simultaneous digital and sustainability transformation, and
introduces AI as a central enabler for orchestrating complex service delivery across organizational
boundaries. Digital twins, as described by Attaran and Celik (2023), provide the conceptual and
technological foundation for tracking instruments throughout their lifecycle. This teaching case helps
in understanding the role of IT and AI in product-service systems (PSS) and PSS-based business
models, while also surfacing the strategic alternatives that a family-owned Mittelstand company must
weigh against servitization. The case illustrates why IT and intelligent AI agents would be necessary
to establish a PSS-based business model, why a customer-centric view matters for this kind of
business model, and how ownership structure shapes the strategic decision.

Keywords: technology-driven organizational change (technochange); IT project management; product-
service systems (PSS); customer-centric business model; agentic AI; digital twins; conversational
agents; teaching case

Introduction
‘Sally, compared to your competitors, your products are well above the average price for surgical
equipment. You know that in recent years, the medical engineering industry, and especially the
surgical equipment sector, has seen a number of new international companies on the scene which have
grown to significant players on the domestic market. Furthermore, serving as the head of medical
equipment procurement for our institution, I increasingly have to initialize open competitive bidding
processes directed by the German state government and the European Union to guarantee fair
bidding,’ says Tim, head of medical equipment procurement at the public mid-sized Marien Hospital
in Northern Germany.

Sally works as a manager in the sales and distribution department at Meditec, a national leading
manufacturer of surgical instruments, and supplier of Marien Hospital. She counters with, ‘I know
about the governmental regimentations on competitive bidding processes, especially in the public
sector and the recent developments within the medical engineering industry. We have formed a task
force to closely monitor the development within the industrial branch and product portfolio of our top
five competitors. I have to admit that in comparison to close competitors, our products are priced
high, but there is one justification for this high difference in pricing, and, Tim, you and your surgeons
know it is the best quality – quality made in Germany!’ Tim nods and says, ‘I agree, quality of
surgical equipment is not only a differentiation factor to competitors within the medical engineering
branch and plays a significant role in decision making in competitive bidding processes, but it is also
fundamental for the medical treatment of our patients and the basis for an excellent national health
care system. Nevertheless, I have observed immense enhancements in product quality of international
medical engineering companies, especially from emerging markets, during the last few years of
attendance at the Medica and CompaMed international trade fairs. Sally, you have to admit that
companies like Hangyong have caught up to national quality standards and generated sound cost and
performance ratios. Additionally, the municipal and state funding on expenses and investments is
stagnating, the hospital management board has introduced stricter conditions for procurement
activities, and Sally you can see my hands are getting more and more tied.’

After discussing minor points in existing contractual arrangements, Tim takes leave of Sally, but
inwardly continues the conversation. ‘You do not solve my problems, Sally. All vendors just want to
sell their newest products. What we are searching for are solutions to our business and treatment
process needs, and not just new products embedding the newest technology. Actually, we need to
concentrate on our core competencies – the healing of and care for patients! We should focus more on
treatment and care processes. Further, we are looking for solutions to increase cost transparency for
our surgical instruments. It is hard to appraise the real costs and to assign them to specific treatments
or patients. In addition, many of the instruments that we sterilize are prepared for surgery but are not
used. Instruments that were prepared for surgery must be cleaned and sterilized whether they are used
or not. With an intelligent solution we could save time and money, and still boost our efficiency.
What I really need is someone who takes the entire instrument lifecycle off my hands. If someone
offered me an AI-powered system that could predict which instruments I need for tomorrow’s surgery
schedule, optimize the tray composition, and automatically trigger the right logistics, that would be a
game-changer. If you could offer me a solution that would help me solve these problems, I would
welcome you with open arms!’

This kind of discussion and contractual talk is not new to Sally. Several customers of Meditec have
increased pressure to reduce prices of offered products, especially because of increased competition
from other, mostly low wage, countries. The situation changed last week when Meditec lost one of its
most important customers, a hospital from Southern Germany, because of a cheaper offer on a
competitive bidding process to Hangyong. In a specially scheduled meeting, board managers and
business unit managers of Meditec then discussed the latest events and critical situation. The
participating managers have now identified multiple factors that have led to this critical situation. The
main factors are: the substitution of existing high-quality products with cheaper products driven by

privatizations of German hospitals, and constrictions of public financial funding. Most critically,
Meditec’s key patents on its proprietary sterile container technology, the company’s highest-margin
product line, accounting for nearly 40 percent of gross margin, are set to expire within eighteen
months. Once these patents lapse, any competitor can replicate the container design, eliminating one
of Meditec’s last remaining sources of differentiation and creating an urgent need for a fundamentally
new competitive strategy. This evolution forces managers of Meditec to react to and initiate
innovative product development processes as essential survival strategies.

Sally is on her way back to the headquarter offices when she realizes that the conversation with the
client calls for a reaction to the current situation of Meditec. She acknowledges that the current
product portfolio is excellent in terms of quality standards and diverse product ranges. Nevertheless,
products no longer guarantee a differentiation from competitors, particularly from those residing in
emerging countries. This results in offered products becoming more and more replaceable. Meditec is
in need of innovatively optimizing its product portfolio and going beyond product improvements. She
knows their products are the best in class, but the offered products do not yet provide an overall
solution for the clients’ problems. What would be an integrated solution around the set of surgical
instruments? Sally spends some time pondering this question. Sally’s enthusiasm surges as she
considers the new plan, ‘I know that the hospitals are currently not searching for new instruments. As
Tim mentioned in the client meeting, our instruments are embedded into several processes, such as
preparation, cleaning, sterilization, quality management, documentation, inventory, storage and so on.
We should help our customers with an integrated product service system in order to ease their
underlying processes. Perhaps we can support them in managing or executing one or more of these
processes? Sally realizes that Meditec could offer integrated services around the entire instrument
lifecycle, not just individual product add-ons.

Meditec
Meditec, founded in 1898 and maintaining its corporate headquarters in Hamburg, Germany, has
grown to a national leading manufacturer of surgical instruments. The company develops and markets
a product range, including surgical instruments for minimally invasive surgical (MIS) approaches
(e.g., vascular surgery), implants, as well as sterile containers (Figure 1). In order to create innovative
solutions around the handling of instruments, the company has initiated the integration of clinical
partners in its research and development activities.

MIS procedures feature multiple advantages in comparison to standard surgical procedures, for
example, prevention of transactions, decreased loss of blood, cooling and exsiccation during the
surgical process. Meditec positions itself as the quality leader in the MIS product sector in Germany,
and focuses on technology-oriented strategies in product development. The organization maintains a
strong customer base composed of multiple mid- and large-sized German hospitals. The company
distributes its products in over three countries (Germany, Austria and Switzerland), and is certified in
accordance with multiple ISO standards to consistently guarantee the high quality of products.
At its peak in 2006, Meditec generated revenues of $214 million with over 500 employees. By 2024,
revenue had declined to $182 million, net income had fallen to around $13 million, and the workforce
had contracted to 450 employees across three national locations, where two locations served as
manufacturing sites in Northern and Southern Germany. Figure 2 graphically depicts the
organizational divisions and units of Meditec, as well as its ecosystem. While the top-line decline of
roughly 15 percent appears modest, the underlying trajectory is alarming: revenues have fallen every
year for the past six consecutive years, gross margins have compressed from 42 percent to 28 percent
over the same period, and the company has lost market share in every product category. Competitors
from South Korea, China, Pakistan and new European entrants now match Meditec’s quality
standards at significantly lower price points, while the German hospital market has consolidated
through mergers and privatizations, with private investors demanding cost reduction and centralized
procurement introducing mandatory EU-wide competitive bidding. Internal projections show that on
the current trajectory, Meditec will be unprofitable within three to four years. Most critically,
Meditec’s key patents on its proprietary sterile container technology, the company’s highest-margin

product line, accounting for nearly 40 percent of gross margin, are set to expire within eighteen
months. Once these patents lapse, any competitor can replicate the container design, eliminating one
of Meditec’s last remaining sources of product-based differentiation. Taken together, these forces
make transformation not a strategic option but a survival necessity: the company must fundamentally
reinvent its business model before the patent cliff converges with the ongoing margin erosion to push
Meditec into structural unprofitability.

Meditec has remained family-owned across four generations. Founded by Heinrich Brandt in 1898,
the company passed to his son, then to his grandson who built it into one of Germany’s leading
surgical instrument manufacturers in the postwar decades. Today the company is led by Michael
Brandt, the fourth-generation owner-CEO, who took over from his father six years ago and holds the
majority of shares together with his immediate family. As a privately held Mittelstand company,
Meditec has never been subject to quarterly earnings pressure or external investor demands, which has
historically allowed the company to invest patiently in quality and R&D. At the same time, the
family’s deep personal identification with the product portfolio – Michael’s father personally
developed the sterile container that now faces patent expiration – creates both emotional commitment
to the company’s legacy and a potential reluctance to abandon the product-centric paradigm that built
it. Michael has been quietly testing strategic options behind the scenes – including conversations with
several external advisors – while allowing the internal team to develop its own perspective on the way
forward.

Meditec also offers a variety of product-related services. On the one hand, Meditec offers specific
training for physicians when they buy new instruments. This training helps physicians with the
application of complex instruments. It is especially important for instruments used in MIS, which
change the whole process of surgery intervention. Before physicians are able to execute MIS, they
need special training to become familiar with these novel techniques. Meditec also provides a wide
range of manuals and further information on its website for registered customers. This knowledge
base contains the long-time experience of Meditec and of its customers. On the other hand, physicians
have the possibility of introducing new ideas and requirements into the innovation process of Meditec.

Figure 1: Product portfolio of Meditec

Figure 2: Current organization and partners of Meditec

The IT-based PSS
After Sally arrives at the headquarters of Meditec, she immediately schedules a meeting with Marc
from the Marketing Division. Marc has recently joined the company as Head of Marketing. His
experience and knowledge of products, especially in the medical engineering industry, have been
incorporated into a new innovative product line at Meditec. Marc previously worked at a US medical
technology company where he witnessed firsthand how manufacturers transition from product-centric
to service-centric business models. He has been researching what US companies such as STERIS,
Intuitive Surgical, and Stryker are doing in terms of servitization and AI-enabled service delivery.
Sally is keen to discuss her thoughts and ideas for new and innovative service offerings with him.
‘I visited a client this morning and ran into the same kind of trouble we’ve had before,’ says Sally.
‘Our customers are totally satisfied with our products in terms of quality and performance, but they
cannot afford our new product series, because, as you know, our offer is more expensive compared to
our closest competitors. And now our competitors have started a discount campaign in order to
increase their market share. As a matter of fact, it is more and more complicated to differentiate our
products from our main competitors.’

Sally explains to Marc how in reaction to the situation, she has started to outline requirements for
future products together with clients. In discussion with her clients, they have jointly brainstormed on
new and recently emerging needs. The clients have suggested that product improvement should not
only consider the products, but should additionally consider the processes that products are embedded
in. Specifically, the clients explained to Sally that they were looking for possibilities to reduce the
complexity of their non-core processes. Marc answers excitedly, ‘This sounds interesting, but when I
think about it, just focusing on processes would not do the trick. In order to deliver customized offers,
our starting point in creating new offers needs to be the lifecycle of our products! Let’s think about it
for a moment – changing the perspective would turn Meditec upside down! And there is another
dimension we have to consider: sustainability. A reprocessing-based model can be more sustainable
than single-use instruments, provided we build the digital infrastructure to manage it well. Some
competitors are betting on disposable instruments – that is simpler from an IT perspective, no tracking
needed, and the single-use market is growing in segments where infection control or staffing
constraints dominate. But disposable instruments also generate waste and depend heavily on stable
supply chains for plastics. Both paths have merit, and the choice has real strategic consequences. For
Meditec, our heritage, our customer relationships, and our R&D base point us toward reprocessing –
but if we choose that path, we need the digital infrastructure to make it work. The sustainable model
and the digital model then become inseparable – a twin transformation.’ As a product-oriented
company, Meditec has always been driven by innovations and improvements of products. The
company claims to be one of the quality and technology leading companies. The entire business and
product development processes are aligned to this strategy. Meditec has introduced existing services
around their products only as an addition to offered surgical instruments. The development process of
services is initiated by the marketing department after the research and development department has
introduced a novel product line. Within the existing approach, the development of products and
services is not conducted in parallel, nor is it done in an integrated way.

A lifecycle-oriented perspective on products would revolutionize the existing business model and
innovation management process applied at Meditec. Innovations would no longer be driven
exclusively by technical functionalities of products only, but by demands along the entire lifecycle of
products integrating customers’ business processes. Following the concept of digital twins (Attaran &
Celik, 2023), each instrument could receive a unique digital identity that represents its physical state,
location, usage history, sterilization records, and remaining lifecycle in real-time. These digital twins
would form the data backbone for all service delivery, enabling Meditec to track and manage
instruments throughout their entire lifecycle across organizational boundaries.
This approach would change a product-centric development process to a development process
focusing on the usage of the product and results of usage. Customers do not necessarily intend
ownership of products, but they want to use products or technology in an appropriate way within their
business processes in order to achieve specific results. With this change, Meditec could establish

novel business models in which clients would pay for the lease or rental of products, and thus only for
the actual usage of products. In the realization of such a business model, the product does not shift in
ownership: the product vendor owns the product along the entire product lifecycle, but additionally
takes on responsibility for maintenance, repair and control.

Sally and Marc consider that all of the new business models are now based on the necessary
transformation of existing business processes. The vendors are in need of monitoring process quality
because they are not only responsible for products, but also for the entire processes embedded in the
customers. For instance, pay per use business models call for tracking and tracing solutions for used
products that are facilitated in processes. Vendors therefore need to gather, analyze and manage
process information that generates new challenges. In addition, the vendor needs to build up new
competencies and skills, especially in the context of IT as an enabler for almost all of the mentioned
business models.

What the customers want
In the following 2 months, Sally and Marc organize multiple workshops with important clients. In
addition, they convince Peter, Senior Product Manager at Meditec, to join the workshops. Peter brings
in his strong technical background and gives feedback to the feasibility of innovative ideas. The
workshop participants generate requirements, discuss possible solutions and specify the most
promising ideas. Today, the workshop team will present all results and findings to Michael Brandt,
the fourth-generation owner-CEO who has led Meditec for six years. Peter from the Production
Development Team is also in attendance.

Sally initiates the meeting. ‘Today we want to talk about new business opportunities for Meditec in
order to generate additional turnover. As you all know, our product sales have stagnated.
Differentiation from our main competitors is becoming more and more difficult. Our main national
and international competitors have caught up in functionality and quality, and some of them offer
their products much cheaper than we can, which has resulted in steadily decreasing margins. The
reality is that we have already lost some of our best customers. This means we have to think
differently in order to break new ground.’ Peter adds, ‘In doing so, we also identified the sterilization
process carrying the biggest potential to ease the life of our customers. All of our customers have
mentioned complaints about this complex process. Achieving the optimum in hygiene turns out to be
a complex challenge for them. Specific requirements exist for the disinfection of surgical instruments
previous to a surgical intervention. We know that instruments have to be absolutely clean.
Unfortunately, a variety of factors influence the results of this cleaning process, which then
complicates the control of the entire sterilization process.’ (Figure 3)

‘But the sterilization process is only one module in our proposal,’ adds Marc. ‘Surgical instruments
have to pass a complex sterilization process underlying governmental regulations, and you know that
German hospitals are restricted to a single usage of surgery instruments by law. That means that used
surgical instruments must be disinfected, cleaned and sterilized immediately before they are approved
for the reuse cycle. The whole process must be controlled, and documentation is essential by
government regulations.’ ‘The sterilization process is not only labor-intensive, but hospitals are also
challenged by complex logistical requirements in which surgical instruments need to be collected,
tracked and moved in multiple steps of the process. Finally, all process steps must be documented by
law.’
‘Asset management and inventory information within the lifecycle process of surgical instruments
play a critical role. But normally, IT systems used within the sterilization process and the
implemented hospital information systems (HIS) are two separate systems. For this reason, inventory
data are not accessible for hospital employees in real-time, which can lead to redundant and
inconsistent data sets about the status of the surgical instruments.’ ‘Finally, the type and number of
instruments used for every surgery is usually known. In normal cases, more instruments are available
for physicians than are necessary. This fact impacts the sterilization process in two negative ways: the
number of instruments running through the sterilization process is not optimized, and the more

instruments that are available, the more complex the decision and search activities to find the correct
instrument during the surgery. If worse comes to worst, the physician loses too much time or makes a
wrong decision. Usually, 70 to 80 instruments are prepared on the surgery table, but only 30% to 40%
are actually used.’
‘This PSS direction is interesting,’ Michael says carefully. ‘Although we would have to develop many
competencies, processes and routines that the PSS requires, I can see why you see this as a very
important step for Meditec.’ He pauses. ‘Before we commit, I want us to be honest about the
alternatives. A premium single-use line would be technically simpler and faces real demand from
infection-control-driven customers. A partnership or even a sale could bring capabilities we cannot
build alone. I am not saying any of those is the right answer – but I want them on the table as we
develop the PSS thinking, not after. And I need to understand where AI fits in specifically, not as a
buzzword, but as a concrete enabler for specific processes in this value chain.’

Figure 3 Underlying cleaning process of surgical instruments.

IT challenges and the role of AI
New challenges arise for a product-centric company like Meditec if it wants to deliver an integrated
PSS around their existing product portfolio. It is clear that Meditec is not able to assume all tasks and
activities of the PSS, but they do want to play a key role within the potential new business model. IT
capabilities play a critical role for managing PSS. Orchestrating just-in-time processes in providing
specific instruments for surgical interventions and steering logistical partners is not feasible without
sophisticated use of IT. The project team at Meditec soon realized that the company needed to
establish an adequate information management (IM), which controls all underlying information flows
within the value network and between institutional entities for a successful introduction of the new
business model. However, the challenges for an adequate IM are numerous.

First, Meditec has to ensure that used instruments are picked up from the customer, transported to a
central sterilization service provider and brought back to the dedicated hospital. The go-and-return
logistic service is a new process because until now the company has only produced and sold
instruments, thus providing a one-way delivery service to the customer. For the newly offered PSS,
the company will then have to track and manage complex movements of instruments to multiple
clients. In this case, Meditec must now ensure an adequate information flow between Meditec, the
clients and the partner providing the logistical services.

Second, instrument-level tracking and digital twins. For a pay-per-use business model to work,
Meditec must be able to identify and track every individual instrument throughout its lifecycle. RFID
technology provides the foundation: each instrument receives a unique digital identity. Combined
with sensor data from sterilization equipment (temperature, cycle duration, cleaning parameters), this
creates a digital twin of each instrument (Attaran & Celik, 2023) — a real-time digital representation
of its physical state, location, usage history, and remaining lifecycle. These digital twins enable not

only tracking and billing, but also predictive maintenance: patterns of wear and erosion can flow into
materials research and inform product development decisions.

The IM efforts taken must also consider the integration of HIS. Every hospital operates its own HIS
that handles information on upcoming surgeries, and lists documentation about the cleaning activities,
as well as location and status data of surgical equipment. In addition, personnel in the client hospitals
must be trained in new functionalities of the HIS. Interfaces have to be implemented for the
communication between the systems. The IT architectures of many customers, especially those of
publicly funded hospitals, have grown over many years and are highly heterogeneous, making
standardized integration a significant technical and organizational challenge.
Third, and most transformatively, AI-powered agents can serve as the intelligent interface layer that
sits on top of the data infrastructure.
Marc presents a three-level AI framework to the project team:
Level 1: Rule-based automation: RFID tags on every instrument enable automatic counting,
tracking, and documentation, eliminating manual data entry. This is mature technology, already
deployed at hospitals such as Mayo Clinic and Rush University Medical Center in the US.
Level 2: Data-driven optimization: Once usage data is accumulated through digital twins, machine
learning algorithms can predict optimal tray compositions for each surgeon and procedure type,
reducing instrument oversupply. Research at Duke University showed that automated RFID-based
tray optimization reduced oversupply by over 50 percent.
Level 3: Agentic AI: Conversational AI agents that interface with the hospital’s surgery schedule,
check real-time sterilization status and inventory levels, and proactively coordinate logistics. An SPD
technician could ask: ‘What trays do I need to prepare for tomorrow’s morning schedule?’ and receive
a prioritized preparation plan. A surgeon’s assistant could ask: ‘Is my preferred laparoscopic set
available for Thursday?’ and receive an immediate, data-backed answer. The project team identifies
three agent types: a customer-facing agent for hospital staff, an operations agent for Meditec’s own
sterilization and logistics teams, and an analytics agent for cross-customer pattern recognition.

Peter raises a hand. ‘All of this only matters if we choose the reprocessing path. If Meditec instead
pivots toward premium single-use instruments, almost none of this IT and AI complexity is required –
no digital twins, no HIS integration, no logistics orchestration. The strategic question and the IT
question are deeply linked.’ The team agrees to keep both paths visible as it develops the analysis.
Finally, the analysis of information flows allows Meditec to identify patterns of use of the
instruments. These analyses help to optimize the flow of instruments and could give input for the
product development. For example, patterns of wasting and erosion could flow in research of
materials and could be helpful for the processing of materials. The analytics agent could identify these
patterns across all customers, generating insights that no individual hospital could produce on its own,
creating a data-driven competitive advantage that deepens over time.

The Owner's Perspective
Several weeks later, Michael Brandt convenes a strategic meeting with Sally, Marc, and Peter at the
Hamburg headquarters. Photos of his great-grandfather, grandfather, and father line the wall behind
him. He picks up a sterile container from the table.
‘My family has owned Meditec for four generations. I don’t think in quarterly numbers – I think in
generations. My father developed this container, and the patent expires in eighteen months. Honestly,
I see that as much an opportunity as a threat. No hospital wants to own this box. They want sterile
instruments in the right operating room at the right time. The container is a means, not an end.’

He sets it down. ‘Over the past six months, I have engaged three strategy consultancies. Each looked
at the same data and reached a fundamentally different conclusion. The first advised aggressive AI-
enabled servitization along the lines Marc has outlined. The second argued the opposite: a 450-person
Mittelstand company cannot credibly compete as a digital platform against players ten times our size
– and recommended we abandon reprocessing entirely and reposition as a premium manufacturer of
single-use instruments. No digital twins, no AI agents, no HIS integration; the global single-use

market is growing at around eight percent annually. The third proposed neither organic path,
recommending a partial or full sale while the brand still commands a premium.’

‘The single-use option weighs on me more than I expected. Our entire conversation has assumed
reprocessing plus AI is the right model, but single-use is technically simpler, regulatorily favored in
some segments, and potentially higher-margin once you account for the service infrastructure. I am no
longer certain that the twin transformation narrative – that digital and sustainability are inseparable –
holds when single-use is seriously on the table.’

He glances at the photos on the wall. ‘So: commit fully to the AI-enabled service model? Pivot to
premium single-use? Pursue a hybrid? Find a partner who brings the software capabilities we lack? Or
sell while the brand still has value? Four generations are watching me from this wall. I genuinely do
not know. What would you recommend?’

Conclusion
The management of Meditec faces a fundamental strategic decision. The traditional product-centric
business model that built the company over four generations is no longer sufficient to secure its
future: margins are eroding, competitors from emerging markets have closed the quality gap, and the
patent cliff on the sterile container technology is eighteen months away.
What remains genuinely open is the direction of the response. One path leads toward a customer-
centric, AI-enabled product-service system built on digital twins, agentic AI, and deep integration into
hospital processes – a twin transformation in which the digital and the sustainable reinforce each
other. A second path leads in the opposite direction: a focused repositioning around premium single-
use instruments that sidesteps the IT and service complexity altogether. A third path involves
partnerships, joint ventures, or a partial or full sale that brings in capabilities – or capital – that
Meditec cannot build alone in the available time.
Each path implies a different role for IT, AI, and data. Each demands different competencies, different
partners, and a different organizational identity. Each carries a different risk profile, and each makes a
different bet about where competitive advantage will lie in the medical equipment industry over the
next decade.
For Michael Brandt and his team, the central question is no longer whether to transform, but which
transformation to commit to and whether a 450-person family-owned Mittelstand company can
credibly execute the chosen path. The journey has just begun, and the most consequential decision
still lies ahead.

Appendix
Comparison table of five US medtech companies showing servitization models and best practices
US industry examples for the Meditec teaching case. All data from publicly available corporate sources (2024/2025).
Companies presented for educational purposes only.

Company PSS type How it works Key metrics IT / AI role

STERIS Offsite reprocessing Per-tray fee model 150M+ instruments Real-time instrument
centers (ORCs): transforms hospital processed/year. 24h tracking across
Result-
hospitals send dirty CapEx (sterilization turnaround. organizations.
oriented
trays, receive sterile- equipment, facility) into Addresses SPD Automated compliance
ready trays back OpEx. Pick-up and staffing shortages documentation. HIS
within 24 hours delivery via climate- directly. integration for surgery
controlled trucks. Full scheduling.
documentation included.

Company PSS type How it works Key metrics IT / AI role

Intuitive Razor-and-blade System placement is the 85% revenue from Platform lock-in
Surgical platform: da Vinci entry point; instruments recurring sources. through embedded
systems placed at and service are the 10,800+ systems workflows. Surgeon
Use-
hospitals generate business. Instruments installed. 20%+ training ecosystem.
oriented
recurring demand for designed for limited use procedure growth. Usage data for product
single-use cycles, must be replaced development.
instruments and regularly.
service contracts

Stryker End-to-end digital Integrates pre-op $22.6B revenue. AI-powered predictive
ecosystem: Mako planning, robotic surgery 2M+ robotic analytics. Digital twins
Result-
robotics + care.ai execution, and post-op procedures. Only for patient outcomes.
oriented
ambient intelligence monitoring into one data player building Ambient sensing for
+ AI analytics across platform. Digital twin of complete end-to-end OR workflow
the full patient each patient journey. view. optimization.
journey

Crothall Complete takeover Hospital transfers the Up to 62% Centralized process
Healthcare of the hospital's entire SPD function to productivity gain. management.
sterile processing Crothall. Crothall deploys 25-50% error Standardized training
Full
department: own trained technicians, reduction. ~90% and quality protocols.
outsourcing
staff, processes, and implements standardized compliance Performance
quality systems processes, manages improvement. dashboards for hospital
deployed on-site compliance and management.
documentation.

References
Attaran, M. & Celik, B.G. (2023). Digital Twin: Benefits, use cases, challenges, and opportunities.
Decision Analytics Journal, 6, 100165.
Markus, M.L. (2004). Technochange management: using IT to drive organizational change. Journal of
Information Technology, 19, pp. 4–20.
Tukker, A. (2004). Eight types of product-service system: eight ways to sustainability? Business
Strategy and the Environment, 13, pp. 246–260.
