from timeit import default_timer as timer

filenames = ["A", "B", "C", "D", "E"]
#filenames=["E"]

for file in filenames:
    print("--- START FILE {} ---".format(file))

    #
    # INPUT PARSER
    #
    t = timer()
    rides = []
    maxPoints = 0
    with open("in/{}.in".format(file)) as f:
        R, C, F, N, B, T = map(int, f.readline().split())
        print("R: {}, C: {}, F: {}, N: {}, B:{}, T:{}".format(R, C, F, N, B, T))
        rides = []
        c= 0
        for r in f.readlines():
            rides.append(list(map(lambda item: int(item), r.split())) + [c])
            maxPoints += B
            maxPoints += abs(rides[c][0]-rides[c][2]) + abs(rides[c][1]-rides[c][3])
            c += 1

    vehicles = []
    for v in range(F):
        vehicles.append([0, 0])

    print("Max points fot dataset {}: {}".format(file, maxPoints))

    #
    # CALCULATION
    #
    points = 0
    for v in vehicles:
        t = 0
        while t < T:
            bestRidePoints = -1000000
            vRides = rides.copy()
            bestRide = None
            # Filter only rides that the vehicle can complete ontime
            for r in filter(lambda r: (t + abs(v[0]-r[0]) + abs(v[1]-r[1]) + abs(r[0]-r[2]) + abs(r[1]-r[3])) <= r[5] , vRides):
                a = 0
                b = 1
                if file == 'D':
                    a = 0.25
                if file == 'E':
                    b = 100
                # Select the ride i can start first
                ridePoints = -a*(abs(r[0]-r[2]) + abs(r[1]-r[3])) - max(abs(v[0]-r[0]) + abs(v[1]-r[1]), r[4] - t)

                if r[4] - t >= abs(v[0]-r[0]) + abs(v[1]-r[1]):
                    ridePoints += b*B

                if ridePoints >= bestRidePoints:
                    bestRide = r
                    bestRidePoints = ridePoints

            if not bestRide == None:
                points += abs(bestRide[0]-bestRide[2]) + abs(bestRide[1]-bestRide[3])
                if bestRide[4] - t >= abs(v[0]-bestRide[0]) + abs(v[1]-bestRide[1]):
                    points += B

                v.append(bestRide[6])  # Add ride id to vehicle
                t = t + max(abs(v[0]-bestRide[0]) + abs(v[1]-bestRide[1]), bestRide[4] - t) + abs(bestRide[0]-bestRide[2]) + abs(bestRide[1]-bestRide[3]) # update timestamp
                v[0] = bestRide[2]  # Update vehicle coordinates
                v[1] = bestRide[3]
                rides.remove(bestRide)  # remove rides from list
                del bestRide
            else:
                break

    print("SCORED: {}".format(points))
    print("Unassigned rides: {}".format(len(rides)))

    #
    # OUTPUT
    #
    with open("{}.out".format(file), 'w') as f:
        for v in vehicles:
            v = v[2:]
            f.write("{} ".format(len(v)))
            for r in v:
                f.write("{} ".format(r))
            f.write("\n")

    print("--- END file {} --\n".format(file))
