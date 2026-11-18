# Storyboards

Every plate has one loop length L; all animations use L (or a period that divides it). The un-animated (reduced-motion)
frame is the key frame, taken at the stated time. Day and dusk share geometry.

## Hero: the tower (one-time intro 2.4 s, then 14 s). Key frame 10.5 s
Idea: a quiet island with a tower; the person is the title. Eye path: tower, name, role, sun.
| t (s) | action | easing |
|---|---|---|
| 0.1-1.6 | island rises 38 px and fades in | settle |
| 0.35-1.7 | name letters rise 26 px, 45 ms stagger | settle |
| 1.35 | role line fades in | settle |
| loop | lantern swings, flag ripples (SMIL), trees sway, birds glide, sun drifts 5 px, clouds drift | sine, linear |
Reset: nothing visible; every ambient cycle divides 14 s. Narrow: the banner text is hidden and an availability pill appears.

## Chronicle: the aqueduct conveyor (18 s). Key frame 15.8 s
Idea: a crash costs a lease timeout, not the run. Eye path: storeroom, belt, hourglass, signs.
| t (s) | action | easing | cue |
|---|---|---|---|
| 0.2-0.8 | three blocks settle on the row | land | |
| 0.3-2.6 | worker 1 walks out with a block | walk cycle | |
| 2.7-5.0 | block goes onto the belt and rides to slot 4 | land, linear | sign 1 at 5.0 |
| 8.4-9.1 | worker 2 trips: lean 26 deg then 78 deg; the block leaves his hands | land | sign 2 at 8.9 |
| 9.0-12.2 | hourglass flips and drains over 3 s; he sits dazed, faded, fenced | linear | sign 3 at 9.6 |
| 12.0-14.2 | terracotta runner enters, leaps at 13.5, catches the block mid-air | linear, land | |
| 14.2-15.5 | carries it to the next slot and places it; the slot glows | land | sign 4 at 15.4 |
| 15.6-17.2 | rewind wheel turns back; ghost dashes run back along the blocks | travel | |
| 17.0-18.0 | fenced worker walks off, hourglass resets, blocks fade | settle | |
Invariant: the row has no gap and no duplicate at any time. Narrow: signs become numbered badges.

## Inference: the workshop (16 s). Key frame 12 s
Idea: requests share a GPU and a cache; tokens stream out. Beats: 1.0 queue, 3.0 a batch of three goes in, 4.4 shelves fill,
6.2 first paper plane, 7.6 a fourth request slips in, 10-11 shelf slots free, 13.2 the next batch walks in. Reset: set B
enters at 13.2-15.0 while set A walks up to the door, so t=0 is a queue again.

## Raft: the ring village (18 s). Key frame 13.5 s
Idea: a majority elects; a minority cannot. Beats: 1.0 replicate, 4.0 the fence slides in, 4.6 two birds bounce off it,
6.5 a majority node blinks and asks for votes, 7-9.5 requests and replies, 9.2-10.6 the one crown hops, 11.5 the fence lifts,
12.2 heal birds reach the old leader. Invariants: one crown at a time; only the majority side elects.

## Assistant: the harbour shop (16 s). Key frame 12 s
Beats: 0.1-3.0 the boat arrives and its bubble pops (sign 1), 3.6 two shelves light and their results meet on the counter
(sign 2), 6.0 the reply bubble flies to the boat (sign 3), 7.6-9.4 the stopwatch arc shrinks and its label becomes "<30 s".
Two more boats bob with lanterns.

## Selected work (14 s)
Four islands on staggered clocks. SAGE: the token hops chairs 1-2-3-2-3-4-5. ResumeIQ: lines highlight and fill an 81-dot grid,
then a four-part ring fills. Plant CNN: the lens slides over the leaf, squares stack and shrink, one of eight bars lights.
SignBridge: dots appear, link into a skeleton, a letter rises, one of 29 pips steps along.

## Activity (12 s)
A ripple passes through the tiles, oldest week to newest (70 ms per week); a lighthouse beam sweeps slowly. Data comes from
the GraphQL contribution calendar; the placeholder is labelled "awaiting first run".

## Footer (12 s)
Waves lap, the lantern breathes, the sun or moon drifts; a tiny figure reads on the cliff above a line naming the three focus areas.
