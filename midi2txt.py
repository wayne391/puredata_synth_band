import pretty_midi


midi_data = pretty_midi.PrettyMIDI('midis/blue_comedy.mid')

all_notes = []


for instr_idx in [0, 1, 2, 3]:
    notes = midi_data.instruments[instr_idx].notes
    for note in notes:
        all_notes.append((instr_idx, note))

all_notes.sort(key=lambda x:x[1].start)
prev_time = 0

lock_map = {
    0: -1,
    1: -1,
    2: -1,
    3: -1,
    4: -1,
}

with open('score.txt', 'w') as f:
    for note in all_notes:
        instr_idx, note = note
        start_time = int(note.start * 1000)
        delta_time = start_time - prev_time

        if instr_idx == 1:
            print('drums', start_time, delta_time, note.pitch)
            if note.pitch in [35, 36]:
                f.write("{} {} 1;".format(delta_time, 'kick'))
                prev_time = start_time
            elif note.pitch in [38, 39, 40]:
                f.write("{} {} 1;".format(delta_time, 'snare'))
                prev_time = start_time
            elif note.pitch in [42, 44, 46]:
                f.write("{} {} 1;".format(delta_time, 'hihat'))
                prev_time = start_time
            else:
                continue

        elif instr_idx == 0: 
            print('bass', start_time, delta_time, note.pitch)
            f.write("{} {} {};".format(delta_time, 'bass', note.pitch))
            prev_time = start_time

        elif instr_idx == 2:
            for ii in range(5):
                if note.start > lock_map[ii]:
                    print('comp', start_time, delta_time, note.pitch)
                    print(' >>>', ii, lock_map[ii])
                    f.write("{} c{}p {};".format(delta_time, ii+1, note.pitch))
                    f.write("0 c{}d {};".format(ii+1, note.end-note.start))
                    lock_map[ii] = note.end
                    prev_time = start_time
                    break
     

        elif instr_idx == 3: 
            print('lead', start_time, delta_time, note.pitch)
            f.write("{} {} {};".format(delta_time, 'synth_lead_pitch', note.pitch))
            f.write("0 {} {};".format('synth_lead_duration', note.end-note.start))
            prev_time = start_time
        else:
            pass
        
