
    # Author: William Wall

    wrsig = 100
    sn_thr = 8

    rmean = power - power
    rsig = power - power
    rmed = power - power

    for ii in range(len(power)):
        bi = ii-wrsig
        if bi < 0:
            bi = 0
        ei = ii+wrsig+1
        if ei > len(power):
            ei = len(power)
        rmean[ii] = np.mean(power[bi:ei])
        rsig[ii] = np.std(power[bi:ei])
        rmed[ii] = np.median(power[bi:ei])

    thresh = rmean + sn_thr*rsig
    rdat = 1.*power
    loc_thr = power > thresh
    rdat[loc_thr] = rmed[loc_thr]
    num_pk = len(np.where(loc_thr)[0])
    num_pks = 1*num_pk

    counter = 0
    while num_pks != 0:
        counter = counter + 1
        for ii in range(len(rdat)):
            bi = ii-wrsig
            if bi < 0:
                bi = 0
            ei = ii+wrsig+1
            if ei > len(rdat):
                ei = len(rdat)
            rmean[ii] = np.mean(rdat[bi:ei])
            rsig[ii] = np.std(rdat[bi:ei])
            rmed[ii] = np.median(rdat[bi:ei])
        thresh = rmean + sn_thr*rsig
        loc_thr = rdat > thresh
        rdat[loc_thr] = rmed[loc_thr]
        num_pks = len(np.where(loc_thr)[0])

    ind = np.where(power > thresh)[0].tolist()

    # End of William's code.

   spec_width = 30
    spec_start = 5

    # Get rid of events that are within 30 seconds of each other.
    i = 1
    while True:
        if i >= len(ind):
            break
        if (ind[i] - ind[i-1])*dt < 30:
            del ind[i]
        else:
            i += 1

    print(f"Found {len(ind)} events.")

    for i in ind:
        datetime_event = datetime_started + datetime.timedelta(seconds=i*dt)

        db["events"].append({
            "file_path": iq_filename,
            "file_index": i,
            "power": power[i],
            "datetime_readable": datetime_event.strftime("%Y-%m-%d %H:%M:%S"),
            "datetime_str": datetime_event.strftime('%Y-%m-%d_%H-%M-%S'),
            "interference": False,
        })